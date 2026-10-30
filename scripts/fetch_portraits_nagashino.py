"""長篠の戦い用の肖像を、Wikimedia Commons から取得する（assets/portraits/<id>.jpg）。429（回数制限）が出たら、間を空けて再試行する。
権利の記録は docs/themes/20261127_nagashino/05_images_rights.md と data/portraits_nagashino.json。"""
import hashlib, json, sys, time
from pathlib import Path
import requests
H = {'User-Agent': 'rekishikaisetu-research/1.0 (educational use; low volume)'}
ITEMS = [
    dict(id='katsuyori', name='武田勝頼', url='https://upload.wikimedia.org/wikipedia/commons/1/19/Takeda_Katsuyori.jpg', page='https://commons.wikimedia.org/wiki/File:Takeda_Katsuyori.jpg', holder='高野山持明院', date='16世紀後半（部分）', note='作者不明。日本の著作権法で保護期間満了（Commonsの記載）'),
    dict(id='sakai_t', name='酒井忠次', url='https://upload.wikimedia.org/wikipedia/commons/e/e6/Sakai_Tadatsugu.jpg', page='https://commons.wikimedia.org/wiki/File:Sakai_Tadatsugu.jpg', holder='先求院', date='16世紀末〜17世紀初', note='日本の著作権法で保護期間満了（Commonsの記載）'),
    dict(id='baba', name='馬場信春', url='https://upload.wikimedia.org/wikipedia/commons/b/bf/Baba_Nobufusa.jpg', page='https://commons.wikimedia.org/wiki/File:Baba_Nobufusa.jpg', holder='恵林寺（信玄公宝物館）', date='江戸時代か（不確か）', note='PD-Art（忠実な複製）。制作年代は不確か'),
    dict(id='yamagata', name='山県昌景', url='https://upload.wikimedia.org/wikipedia/commons/9/93/Masakage_Yamagata.jpg', page='https://commons.wikimedia.org/wiki/File:Masakage_Yamagata.jpg', holder='不明（出典「Japon」）', date='「16世紀」とされるが根拠不明', note='作者・所蔵不明。出典が弱いので、画面では「後世の肖像（出典不明）」と注記するか、別の資料に替える'),
    dict(id='okudaira', name='奥平信昌', url='https://upload.wikimedia.org/wikipedia/commons/1/13/Okudaira_Nobumasa.jpg', page='https://commons.wikimedia.org/wiki/File:Okudaira_Nobumasa.jpg', holder='久昌院（京都府）', date='1615年ごろ（絹本着色）', note='作者不明。賛は三江紹益。Public Domain Mark'),
]
root = Path(__file__).resolve().parents[1] / 'assets' / 'portraits'
root.mkdir(parents=True, exist_ok=True)
for a in ITEMS:
    p = root / (a['id'] + '.jpg')
    if p.exists() and p.stat().st_size > 10000:
        a['file'] = str(p); a['bytes'] = p.stat().st_size; a['sha256'] = hashlib.sha256(p.read_bytes()).hexdigest(); print(a['id'], 'exists'); continue
    wait = 60
    for k in range(8):
        r = requests.get(a['url'], headers=H, timeout=90)
        if r.status_code == 200:
            break
        print(a['id'], 'HTTP', r.status_code, 'wait', wait, flush=True); time.sleep(wait); wait = min(wait * 2, 600)
    r.raise_for_status()
    p.write_bytes(r.content); a['file'] = str(p); a['bytes'] = len(r.content); a['sha256'] = hashlib.sha256(r.content).hexdigest()
    print(a['id'], 'ok', len(r.content), flush=True)
    time.sleep(20)
(root.parent.parent / 'data' / 'portraits_nagashino.json').write_text(json.dumps(ITEMS, ensure_ascii=False, indent=2), encoding='utf8')
print('done')
