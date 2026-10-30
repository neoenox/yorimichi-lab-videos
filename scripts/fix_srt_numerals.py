"""既存のSRTの、数量・回数・順序の漢数字だけを算用数字に直す（タイミングは触らない）。
usage: python scripts/fix_srt_numerals.py out/oke_subtitles.srt [--write]
hn_text.display と同じ規則（助数詞が続くものだけ数字、慣用句はそのまま）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hn_text import display

def fix(path, write):
    p = Path(path)
    blocks = p.read_text(encoding='utf8').strip().split('\n\n')
    out, changed = [], []
    for b in blocks:
        ls = b.splitlines()
        if len(ls) < 3:
            out.append(b); continue
        head, body = ls[:2], '\n'.join(ls[2:])
        new = display(body)
        if new != body:
            changed.append((head[0].split(' --> ')[0], body, new))
        out.append('\n'.join(head + [new]))
    if write:
        p.write_text('\n\n'.join(out) + '\n', encoding='utf8')
    print(f'{p.name}: {len(blocks)} cues, {len(changed)} changed' + ('' if write else ' (dry-run)'))
    for t, a, b in changed:
        print(f'  {t}  {a}  ->  {b}')
    return len(changed)

if __name__ == '__main__':
    fix(sys.argv[1], '--write' in sys.argv)
