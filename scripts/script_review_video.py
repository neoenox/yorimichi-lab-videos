"""完成動画を Google AI にレビューさせる（共通部品 ytkit.review の入口）。

usage:
  python scripts/script_review_video.py out/short_solo_x.mp4 --slug solo_x
  python scripts/script_review_video.py out/short_solo_x.mp4 --dry-run
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('YT_PROJECT_ROOT', str(ROOT))
os.environ.setdefault('PYTHONIOENCODING', 'utf8')

from ytkit.review.__main__ import main

if __name__ == '__main__':
    argv = sys.argv[1:]
    if argv and not argv[0].startswith('-'):
        argv = ['video', argv[0]] + argv[1:]
        if '--out-dir' not in argv:
            argv += ['--out-dir', str(ROOT / 'out')]
    raise SystemExit(main(argv))
