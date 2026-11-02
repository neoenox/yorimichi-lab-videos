"""戦況地図（battle_map）を大きくする：左の地図を幅1230へ、右のカードは狭く。usage: python scripts/enlarge_maps.py [--apply] slug..."""
import json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
apply = '--apply' in sys.argv; slugs = [a for a in sys.argv[1:] if not a.startswith('--')]
for s in slugs:
    p = R / 'data' / f'{s}_spec.json'; sp = json.loads(p.read_text(encoding='utf8')); n = 0
    for ch in sp['chapters']:
        sc = ch.get('scene') or []
        for m in [i for i in sc if i.get('name') == 'battle_map' and i['box'][2] == 1000]:
            m['box'] = [30, 120, 1260, 880]; n += 1
            for i in sc:
                if i.get('name') == 'pop_rows' and i.get('x0') == 1010: i['x0'] = 1280; i['x1'] = 1890; i['size'] = 40
            sc[:] = [i for i in sc if not (i.get('name') == 'pop_telop' and i.get('y', 0) > 800 and '位置' in i.get('text', ''))]
    print(s, 'maps', n)
    if apply: p.write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf8')
