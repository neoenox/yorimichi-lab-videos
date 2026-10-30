"""関ヶ原の戦い用の肖像を Wikimedia Commons から取得（assets/portraits/<id>.jpg、幅1000pxの縮小版）。権利メタデータは data/portraits_sekigahara.json に記録。
429が出たら待って再試行。家康・三成・小早川秀秋は既存（data/portraits.json）。"""
import hashlib, json, re, time
from pathlib import Path
import requests
H = {'User-Agent': 'rekishikaisetu-research/1.0 (educational use; low volume)'}
ITEMS = [('otani', '大谷吉継', 'Ōtani_Yoshitsugu.jpg'), ('ukita', '宇喜多秀家', 'Ukita_Hideie.jpg'), ('shimazu', '島津義弘', 'Shimazu_Yoshihiro.jpg'),
         ('konishi', '小西行長', 'Daimyo_Konishi_Yukinaga_Ukiyo-e.jpg'), ('fukushima', '福島正則', 'Masanori_Fukushima.JPG'), ('ii', '井伊直政', 'Ii_Naomasa.jpg'), ('mori_h', '毛利秀元', '毛利秀元.jpg'), ('kuroda', '黒田長政', 'Kuroda_Nagamasa.jpg'), ('kikkawa', '吉川広家', 'Kikkawa_Hiroie.jpg')]
R = Path(__file__).resolve().parents[1]
root = R / 'assets' / 'portraits'
out = []
def get(url, **kw):
    wait = 30
    for _ in range(8):
        r = requests.get(url, headers=H, timeout=90, **kw)
        if r.status_code == 200: return r
        print('HTTP', r.status_code, 'wait', wait, flush=True); time.sleep(wait); wait = min(wait * 2, 300)
    r.raise_for_status()
for id_, name, fn in ITEMS:
    meta = get('https://commons.wikimedia.org/w/api.php', params=dict(action='query', titles='File:' + fn, prop='imageinfo', iiprop='extmetadata|url', format='json')).json()
    ii = list(meta['query']['pages'].values())[0]['imageinfo'][0]; em = ii['extmetadata']
    strip = lambda k: re.sub('<[^>]+>', '', em.get(k, {}).get('value', ''))
    p = root / (id_ + '.jpg')
    if not (p.exists() and p.stat().st_size > 10000):
        r = get('https://commons.wikimedia.org/wiki/Special:FilePath/' + fn, params={'width': 1000})
        from PIL import Image; import io
        Image.open(io.BytesIO(r.content)).convert('RGB').save(p, quality=92)
        time.sleep(8)
    out.append(dict(id=id_, name=name, file=str(p.relative_to(R)), page='https://commons.wikimedia.org/wiki/File:' + fn, license=strip('LicenseShortName'), artist=strip('Artist'),
                    desc=strip('ImageDescription')[:300], date=strip('DateTimeOriginal'), credit=strip('Credit')[:200], sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    print(id_, out[-1]['license'], '|', out[-1]['artist'][:60], '|', out[-1]['desc'][:80], flush=True)
(R / 'data' / 'portraits_sekigahara.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf8')
