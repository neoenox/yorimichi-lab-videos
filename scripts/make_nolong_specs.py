"""「本編に触れない版」のspecを作る（2026-11-04）：data/nolong_targets.json の各Shortを、data/short_<slug>_nl.json に複製し、
nolong:true を付ける。notes の「出典は本編の概要欄に」は「出典は、この説明欄に」に直す。
usage: python scripts/make_nolong_specs.py → 続けて make_short2.py <slug>_nl → pack_short.py → yt_api.py upload"""
import json
import re
from pathlib import Path
R = Path(__file__).resolve().parents[1]
for slug, when, long_date in json.loads((R / 'data' / 'nolong_targets.json').read_text(encoding='utf8')):
    sp = json.loads((R / 'data' / f'short_{slug}.json').read_text(encoding='utf8'))
    sp['nolong'] = True
    sp['notes'] = re.sub(r'出典は本編の概要欄にまとめています。', '出典は、この説明欄に書いています。', sp.get('notes', ''))
    sp['notes'] = re.sub(r'詳しい根拠は、長い動画にまとめています。', '', sp['notes'])
    (R / 'data' / f'short_{slug}_nl.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf8')
print('specs written')
