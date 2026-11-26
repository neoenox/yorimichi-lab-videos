"""台本を ChatGPT / Google AI にレビューさせる（共通部品 ytkit.review の入口）。

usage:
  python scripts/script_review.py solo_x
  python scripts/script_review.py solo_x --target chatgpt
  python scripts/script_review.py solo_x --dry-run
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('YT_PROJECT_ROOT', str(ROOT))

from ytkit.review.__main__ import main

if __name__ == '__main__':
    script = ROOT / 'data' / f'short_{sys.argv[1]}.json' if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else None
    argv = sys.argv[1:]
    if script is not None:
        argv = ['run', str(script), '--adapter', 'honnoji_json', '--project', 'rekishikaisetu-honnoji', '--slug', argv[0]] + argv[1:]
        argv += ['--out-dir', str(ROOT / 'out')]
    raise SystemExit(main(argv))
