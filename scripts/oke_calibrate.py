"""Estimate narration length from 09_script_v2.md for existing slugs (calibration)."""
import re, json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
for slug in ['koku', 'gdp', 'drain', 'scurvy', 'zenzen', 'calendar', 'compass', 'einstein', 'season', 'vein']:
    spec = json.loads((R / f'data/{slug}_spec.json').read_text(encoding='utf8'))
    p = R / 'docs/themes' / spec['theme_dir'] / '09_script_v2.md'
    if not p.exists():
        print(slug, 'no script'); continue
    t = p.read_text(encoding='utf8')
    chs = re.split(r'\n## ', t)[1:]
    n_sent = 0; chars = 0
    for c in chs:
        lines = [re.sub(r'〔[^〕]*〕', '', re.sub(r'^\d+\. ', '', l)).strip() for l in c.split('\n') if re.match(r'^\d+\. ', l)]
        txt = ''.join(lines)
        n_sent += len([x for x in txt.split('。') if x.strip()])
        chars += len(txt)
    tl = R / f'data/{slug}_timeline.json'
    dur = json.loads(tl.read_text(encoding='utf8'))[-1]['end'] if tl.exists() else 0
    print(f'{slug:10s} ch={len(chs):2d} sent={n_sent:3d} chars={chars:5d}'
          f'  narrated={dur:6.1f}s  chars/s={chars/dur if dur else 0:.2f}')
