"""字幕に残っている「漢数字の数量」を洗い出す（display を適用しても変わる文字列＝変換漏れ）。

usage: python scripts/check_numerals.py [slug ...]     # 省略時は out/*_subtitles.srt 全部
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hn_text

R = Path(__file__).resolve().parents[1]
slugs = sys.argv[1:]
files = ([R / 'out' / f'{s}_subtitles.srt' for s in slugs] if slugs
         else sorted(R.glob('out/*_subtitles.srt')))

bad = 0
for p in files:
    if not p.exists():
        print('missing', p.name)
        continue
    diff = []
    for block in p.read_text(encoding='utf8').strip().split('\n\n'):
        lines = block.splitlines()
        if len(lines) < 3:
            continue
        text = '\n'.join(lines[2:])
        conv = hn_text.display(text)
        if conv != text:
            diff.append((text.replace('\n', ''), conv.replace('\n', '')))
    if diff:
        bad += 1
        print(f'--- {p.name}: {len(diff)} 行')
        for a, b in diff[:6]:
            print(f'   {a}')
            print(f'-> {b}')
print(f'files with leftovers: {bad} / {len(files)}')
