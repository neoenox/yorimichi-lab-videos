"""グラフ(driftsaw/bars/table等)が出る場面で、先に出ていた pop_rows の項目が残って重なるのを、グラフの at で消す。
usage: python scripts/fix_pop_rows_until.py [--apply] slug..."""
import json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
apply = '--apply' in sys.argv; slugs = [a for a in sys.argv[1:] if not a.startswith('--')]
POP = {'pop_bgimg', 'pop_telop', 'pop_rows', 'pop_card', 'pop_fill'}
out = {}
for s in slugs:
    p = R / 'data' / f'{s}_spec.json'; sp = json.loads(p.read_text(encoding='utf8')); n = []
    for ci, ch in enumerate(sp['chapters']):
        sc = ch.get('scene') or []
        charts = [i for i in sc if i.get('box') and i.get('name') not in POP and i.get('at') is not None and i.get('t') in ('anim', 'bars', 'table', 'line', 'stack', 'timeline', 'flow')]
        for r in [i for i in sc if i.get('name') == 'pop_rows']:
            y0 = r.get('y0', 190)
            for e in r['items']:
                for c in charts:
                    top, bot = c['box'][1], c['box'][3]
                    ey = y0  # 項目の位置は積み上げで下がるので、y0以降〜画面下端を対象に見る
                    if bot > y0 and top < 840 and e.get('at', 0) < c['at'] and (e.get('until') is None or e['until'] > c['at']):
                        e['until'] = c['at']; n.append((ci, e['text'][:12], c['at']))
    if n:
        out[s] = n
        if apply: p.write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf8')
for k, v in out.items(): print(k, len(v), v[:3])
