"""builder3: hook_card=false の夕焼けShort(v3)を描画する。

既存の out/short_solo_sunset.mp4 / _v2.mp4 / _fv.mp4 は上書きしない。
slug=solo_sunset_v3 相当の設定で out/short_solo_sunset_v3.mp4 を出力する。
話速 1.45 はこのプロセス内だけの上書き（ytcore の既定は変更しない）。
"""
import os
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
os.environ.setdefault('YT_PROJECT_ROOT', str(R))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import procedure_gate
procedure_gate.require()

import ytcore.make_short as base
base.SPEED = 1.45
import ytcore.make_short2 as ms2

if __name__ == '__main__':
    sys.argv = ['make_short2', 'solo_sunset_v3'] + sys.argv[1:]
    ms2.main()
