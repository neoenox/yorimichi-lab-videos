"""Look up coordinates for Okehazama places from the GSI address-search API.
Writes cache/oke_places.json.  Run: .venv\\Scripts\\python.exe scripts\\oke_places_lookup.py
"""
import json, time
from pathlib import Path
import requests

R = Path(__file__).resolve().parents[1]
API = 'https://msearch.gsi.go.jp/address-search/AddressSearch'

QUERIES = {
    'kiyosu': '愛知県清須市一番町 清洲城',
    'atsuta': '愛知県名古屋市熱田区神宮 熱田神宮',
    'narumi': '愛知県名古屋市緑区鳴海町 鳴海城',
    'odaka': '愛知県名古屋市緑区大高町 大高城',
    'kutsukake': '愛知県豊明市沓掛町 沓掛城',
    'zenshoji': '愛知県名古屋市緑区鳴海町 善照寺',
    'nakajima': '愛知県名古屋市緑区鳴海町 中島',
    'marune': '愛知県名古屋市緑区大高町 丸根',
    'washizu': '愛知県名古屋市緑区大高町 鷲津',
    'okehazama_den': '愛知県豊明市栄町南舘 桶狭間古戦場伝説地',
    'okehazama_park': '愛知県名古屋市緑区桶狭間北 桶狭間古戦場公園',
    'taragakubo': '愛知県豊明市沓掛町 田楽ケ窪',
    'sunpu': '静岡県静岡市葵区駿府城公園',
    'okazaki': '愛知県岡崎市康生町 岡崎城',
}

out = {}
for key, q in QUERIES.items():
    try:
        r = requests.get(API, params={'q': q}, timeout=30,
                         headers={'User-Agent': 'rekishikaisetu-research/1.0'})
        r.raise_for_status()
        js = r.json()
        if not js:
            out[key] = dict(query=q, hit=None)
            print(key, 'NO HIT')
        else:
            f = js[0]
            out[key] = dict(query=q, title=f.get('properties', {}).get('title'),
                            lon=f['geometry']['coordinates'][0], lat=f['geometry']['coordinates'][1])
            print(key, out[key]['title'], out[key]['lat'], out[key]['lon'])
    except Exception as e:  # noqa: BLE001
        out[key] = dict(query=q, error=str(e))
        print(key, 'ERROR', e)
    time.sleep(1.0)

(R / 'cache').mkdir(exist_ok=True)
(R / 'cache' / 'oke_places.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf8')
print('->', R / 'cache' / 'oke_places.json')
