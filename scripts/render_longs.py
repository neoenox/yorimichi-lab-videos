"""長尺3本（忍者・世界地図・本能寺）を、字幕52px・数字強調・-c copy 結合・-14 LUFS で作り直す。

usage: python scripts/render_longs.py            # nj -> gm -> hn
       python scripts/render_longs.py nj gm      # 指定だけ
"""
import datetime as dt
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

R = Path(__file__).resolve().parents[1]
py = sys.executable
order = [a for a in sys.argv[1:]] or ['nj', 'gm', 'hn']
log = R / 'out' / 'codex' / 'render_longs.log'


def say(msg):
    line = f'[{dt.datetime.now():%H:%M:%S}] {msg}'
    print(line, flush=True)
    with log.open('a', encoding='utf8') as f:
        f.write(line + '\n')


env = dict(os.environ)
env['PATH'] = str(R / 'tools' / 'ffmpeg' / 'bin') + os.pathsep + env.get('PATH', '')
env['PYTHONIOENCODING'] = 'utf8'

for slug in order:
    t0 = time.time()
    if slug == 'hn':
        # hn は 1 本だと長すぎるので 6000 フレームずつ。既存パートは古い字幕なので必ず退避する
        parts = sorted((R / 'cache').glob('hn4_part_*.mp4'))
        if parts:
            prev = R / 'cache' / f'prev_{dt.datetime.now():%Y%m%d_%H%M}_hn'
            prev.mkdir(parents=True, exist_ok=True)
            for p in parts:
                shutil.move(str(p), str(prev / p.name))
            say(f'hn: 旧パート {len(parts)} 本を {prev.name} へ退避')
        e = dict(env)
        e['CHUNK'] = '6000'
    else:
        e = env
    say(f'{slug}: 開始')
    p = subprocess.run([py, '-X', 'utf8', str(R / 'scripts' / 'rebuild_old_compose.py'), slug],
                       cwd=str(R), env=e)
    say(f'{slug}: rc={p.returncode} {time.time() - t0:.0f}s')
    if p.returncode != 0:
        say(f'{slug}: 失敗（続行）')

say('完了')
