"""長尺パックのメタデータ（タイトル・概要欄・タグ）の漢数字を算用数字にそろえる。

字幕と同じ規則（hn_text.display）を使う。公開済み・公開予定のどちらでも安全（APIは触らない）。
usage:
  python scripts/fix_meta_numerals.py            # 差分の確認だけ
  python scripts/fix_meta_numerals.py --write    # 書き換え

時刻の呼び名（「九つ」など）を含む koku は対象外にする（字幕が漢字のままなので合わせる）。
"""
import difflib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hn_text

R = Path(__file__).resolve().parents[1]
SKIP = {'04_edo_ichikoku'}          # 時刻の呼び名（九つ・八つ・七つ）を漢字のまま残す
FILES = ('title.txt', 'description.txt', 'tags.txt')


def main():
    write = '--write' in sys.argv
    changed = 0
    for pack in sorted((R / 'upload').iterdir()):
        if not pack.is_dir() or pack.name.startswith('short_') or pack.name in SKIP:
            continue
        for name in FILES:
            f = pack / name
            if not f.exists():
                continue
            t = f.read_text(encoding='utf8')
            c = hn_text.display(t)
            if c == t:
                continue
            changed += 1
            sm = difflib.SequenceMatcher(None, t, c, autojunk=False)
            ops = [op for op in sm.get_opcodes() if op[0] != 'equal']
            print(f'{pack.name}/{name}: {len(ops)} 箇所')
            for tag, i1, i2, j1, j2 in ops:
                print(f'   {t[max(0, i1 - 10):i2 + 10]!r}'.replace('\\n', '⏎'))
                print(f'-> {c[max(0, j1 - 10):j2 + 10]!r}'.replace('\\n', '⏎'))
            if write:
                f.write_text(c, encoding='utf8')
    print(('書き換え ' if write else '差分 ') + f'{changed} ファイル')


if __name__ == '__main__':
    main()
