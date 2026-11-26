"""builder2: 修正済み台本で夕焼けShortを別名(v2)に描画する。

既存の out/short_solo_sunset.mp4 と out/short_solo_sunset_fv.mp4 は上書きしない。
spec は gen_solo_sunset.py が作った data/short_solo_sunset_v2.json を使う。
話速は既存ビルドと同じ 1.45 だけをこのプロセス内で上書きする（ytcore の既定は変更しない）。
"""
import os
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
os.environ.setdefault('YT_PROJECT_ROOT', str(R))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import procedure_gate
procedure_gate.require()

import ytcore.make_short as base
base.SPEED = 1.45
import ytcore.make_short2 as ms2

if __name__ == '__main__':
    sys.argv = ['make_short2', 'solo_sunset_v2'] + sys.argv[1:]
    ms2.main()
