"""pop_telop の下端が、同じ場面の pop_rows の上端に重なる specを探し、rows を下げる（rows は下端に収まるよう自動で縮む）。
usage: python scripts/fix_pop_overlap.py [--apply] slug..."""
import json, math, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
apply = '--apply' in sys.argv
slugs = [a for a in sys.argv[1:] if not a.startswith('--')]
def lines_of(t):
    n = 0
    for ln in t.split('\n'):
        plain = ln.replace('[[', '').replace(']]', '')
        n += max(1, math.ceil(len(plain) * 1.0 / 1.0))  # placeholder
    return n
def est_h(it):
    size = it.get('size', 100); maxw = it.get('maxw', 1500); n = 0
    for ln in it['text'].split('\n'):
        plain = ln.replace('[[', '').replace(']]', '')
        n += max(1, math.ceil(len(plain) * size * 0.98 / maxw))
    return n * int(size * 1.22) + int(size * .9)
changed = {}
for s in slugs:
    p = R / 'data' / f'{s}_spec.json'
    sp = json.loads(p.read_text(encoding='utf8')); n = 0
    for ch in sp['chapters']:
        sc = ch.get('scene') or []
        tel = [i for i in sc if i.get('name') == 'pop_telop']
        rows = [i for i in sc if i.get('name') == 'pop_rows']
        for t in tel:
            h = est_h(t); bottom = t.get('y', 500) + h / 2 + 10
            for r in rows:
                top = r.get('y0', 190)
                if bottom > top + 25 and t.get('y', 500) < top + 200:
                    new = int(bottom + 14)
                    if new > 560: continue
                    r['y0'] = new; n += 1
    if n:
        changed[s] = n
        if apply: p.write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf8')
print(changed)
