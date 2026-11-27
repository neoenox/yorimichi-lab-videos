"""共通部品 ytcore への入口（shim）。実体は E:/yt-shorts-kit の ytcore/first_frame_preview.py。
`import first_frame_preview` も `python scripts/first_frame_preview.py ...` も、従来どおり動く。プロジェクトのルートを環境変数で渡してから呼ぶ。"""
import importlib
import os
import runpy
import sys
from pathlib import Path

os.environ.setdefault('YT_PROJECT_ROOT', str(Path(__file__).resolve().parents[1]))
if __name__ == '__main__':
    runpy.run_module('ytcore.first_frame_preview', run_name='__main__', alter_sys=True)
else:
    sys.modules[__name__] = importlib.import_module('ytcore.first_frame_preview')
