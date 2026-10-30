"""長篠・設楽原の地名を、国土地理院の住所検索APIで引く。cache/nagashino_places.json に書く（大字の代表点＝数百mずれることがある）。"""
import json, time
from pathlib import Path
import requests
R = Path(__file__).resolve().parents[1]
API = 'https://msearch.gsi.go.jp/address-search/AddressSearch'
Q = {
 'nagashino_castle': '愛知県新城市長篠 長篠城跡',
 'tobinosu': '愛知県新城市長篠 鳶ヶ巣山',
 'shidarahara': '愛知県新城市大宮 設楽原歴史資料館',
 'rengogawa': '愛知県新城市竹広 連吾川',
 'gokurakuji': '愛知県新城市大宮 極楽寺',
 'danjouyama': '愛知県新城市竹広 弾正山',
 'iouji': '愛知県新城市大宮 医王寺',
 'chausuyama': '愛知県新城市大宮 茶臼山古墳',
 'noda': '愛知県新城市豊島 野田城',
 'okazaki': '愛知県岡崎市康生町 岡崎城',
 'ushikubo': '愛知県豊川市牛久保町 牛久保城',
 'houraiji': '愛知県新城市門谷 鳳来寺',
 'shinmido': '愛知県新城市大宮 新御堂',
 'takamatsu': '愛知県新城市竹広 高松',
 'tsukude': '愛知県新城市作手 作手',
 'toyokawa_nagashino': '愛知県新城市長篠 長篠',
}
out = {}
for k, q in Q.items():
    try:
        js = requests.get(API, params={'q': q}, timeout=30, headers={'User-Agent': 'rekishikaisetu-research/1.0'}).json()
    except Exception as e:  # noqa: BLE001
        out[k] = dict(query=q, error=str(e)); print(k, 'ERR', e); continue
    if not js:
        out[k] = dict(query=q, hit=None); print(k, 'NO HIT'); continue
    f = js[0]; lon, lat = f['geometry']['coordinates']
    out[k] = dict(query=q, title=f['properties'].get('title'), lon=lon, lat=lat)
    print(k, f['properties'].get('title'), round(lon, 5), round(lat, 5))
    time.sleep(0.4)
(R / 'cache').mkdir(exist_ok=True)
(R / 'cache' / 'nagashino_places.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf8')
