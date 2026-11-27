"""YouTube Studio の Ask Studio に質問する（共通部品 ytkit.review の入口）。

usage:
  python scripts/ask_studio.py "チャンネルの調子を教えて" --slug growth
  python scripts/ask_studio.py --question-file docs/question.md --slug growth
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('PYTHONIOENCODING', 'utf8')

from ytkit.review.__main__ import main

if __name__ == '__main__':
    args = sys.argv[1:]
    if args and not args[0].startswith('-'):
        args = ['studio', args[0]] + args[1:]
    elif '--question-file' in args:
        args = ['studio'] + args
    else:
        args = ['studio'] + args
    if '--out-dir' not in args:
        args += ['--out-dir', str(ROOT / 'out')]
    raise SystemExit(main(args))
