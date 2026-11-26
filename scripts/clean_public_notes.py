"""既存 spec の notes から内部メモ行を削除する。

対象ラベル:
  言い過ぎを避けた点 / 使っていないこと / 使っていない / 未確認 /
  指摘 / 採用 / 不採用 / レビューで直した点 / web_fetch / 文字化け / decode
使い方:
  python scripts/clean_public_notes.py --dry
  python scripts/clean_public_notes.py --apply
"""
import glob
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
apply = '--apply' in sys.argv
LABELS = [
    '・言い過ぎを避けた', '・使っていないこと', '・使っていない：', '・未確認：',
    '・指摘：', '・採用：', '・不採用：', '・レビューで直した点',
    'web_fetch', '・文字化け', 'decode(', 'urllib', 'Python で取得', '【試作】',
]
# 「指摘もある」「〜と指摘しています」は史実の説明なので削除しない。

changed = []
for f in sorted((R / 'data').glob('short_*.json')):
    d = json.loads(f.read_text(encoding='utf8'))
    if not isinstance(d, dict) or 'notes' not in d:
        continue
    lines = d['notes'].splitlines()
    kept = []
    removed = []
    for line in lines:
        if any(label in line for label in LABELS):
            removed.append(line)
        else:
            kept.append(line)
    if not removed:
        continue
    new = '\n'.join(kept).strip() + '\n'
    changed.append((f, d['notes'], new, removed))
    if apply:
        d['notes'] = new
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf8')

print('対象:', len(changed))
for f, old, new, removed in changed[:5]:
    print(f.name, '削除行:', len(removed))
    for r in removed[:2]:
        print('  -', r[:80])
if len(changed) > 5:
    print('...')
if apply:
    print('spec を更新しました')
else:
    print('dry run（--apply で反映）')
