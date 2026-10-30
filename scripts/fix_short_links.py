"""長尺の再アップロードで動画IDが変わった Short の概要欄だけを書き直す（再レンダリング不要）。
usage: python fix_short_links.py <slug> [<slug> ...]
"""
import json, re, sys
from pathlib import Path
import make_short2 as M

R = Path(__file__).resolve().parents[1]
for slug in sys.argv[1:]:
    spec = json.loads((R / 'data' / f'short_{slug}.json').read_text(encoding='utf8'))
    out = R / 'out' / f'short_{slug}_description.md'
    m = re.search(r'約(\d+)秒', out.read_text(encoding='utf8'))
    spec['sec'] = int(m.group(1)) if m else 45
    text = M.description(spec)
    out.write_text(text, encoding='utf8')
    pack = R / 'upload' / f'short_{slug}'
    if pack.is_dir():
        (pack / 'description.txt').write_text(text, encoding='utf8')
    print(slug, 'link ->', spec['long_id'], 'sec', spec['sec'], 'pack' if pack.is_dir() else 'no-pack')
