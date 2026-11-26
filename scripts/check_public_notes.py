"""data/short_*.json の notes に内部メモが混ざっていないか検査する。

使い方:
  python scripts/check_public_notes.py data/short_solo_x.json [...]

概要欄（説明欄）は視聴者向け。次のような内部作業の記述は docs/research/ に残し、notes には書かない。
- 取得方法（web_fetch / urllib / decode / 文字化け / Python で取得）
- レビュー判断の経緯（言い過ぎを避けた点 / 使っていないこと / 採用・不採用 / 指摘）
- ゲート名（needs_review / needs_research / to-spec / root の）
"""
import sys
from pathlib import Path

BAD = [
    'web_fetch', 'decode(', '文字化け', 'urllib', 'Python で取得',
    '言い過ぎを避けた', '使っていないこと', '採用', '不採用', '指摘',
    'needs_review', 'needs_research', 'to-spec', 'root の',
]

paths = []
for arg in sys.argv[1:]:
    if '*' in arg:
        paths.extend(Path('.').glob(arg))
    else:
        paths.append(Path(arg))

bad_total = 0
for p in paths:
    d = __import__('json').loads(p.read_text(encoding='utf8'))
    notes = d.get('notes', '') if isinstance(d, dict) else ''
    hits = [w for w in BAD if w in notes]
    if hits:
        bad_total += 1
        print(f'ERROR: {p}: 内部記述が残っています: {hits}')
    else:
        print(f'OK: {p}')
sys.exit(1 if bad_total else 0)
