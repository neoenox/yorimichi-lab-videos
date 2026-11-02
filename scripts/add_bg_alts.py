"""各 spec の pop_bgimg に、同じ動画の他の背景写真を alts として足す（seg秒ごとに切り替わる）。
usage: python scripts/add_bg_alts.py [--apply] slug..."""
import json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
apply = '--apply' in sys.argv; slugs = [a for a in sys.argv[1:] if not a.startswith('--')]
for s in slugs:
    p = R / 'data' / f'{s}_spec.json'; sp = json.loads(p.read_text(encoding='utf8'))
    bgs = []
    for ch in sp['chapters']:
        for it in ch.get('scene') or []:
            if it.get('name') == 'pop_bgimg' and it.get('img') and it['img'] not in bgs: bgs.append(it['img'])
    n = 0
    for ch in sp['chapters']:
        for it in ch.get('scene') or []:
            if it.get('name') == 'pop_bgimg' and it.get('img'):
                alts = [b for b in bgs if b != it['img']]
                if alts: it['alts'] = alts; it.setdefault('seg', 22); n += 1
    print(s, 'bg枚数', len(bgs), '更新', n)
    if apply: p.write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf8')
