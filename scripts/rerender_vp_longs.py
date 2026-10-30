"""差し替え予定の長尺9本を、字幕52px・数字強調・1世代エンコードで作り直す。

`replace_versions.replace()` は「out/<slug>_video.mp4 が upload/<pack>/video.mp4 より新しい」ときだけ
差し替えるので、ここでは映像を作り直すだけでよい（SRT 再生成とパックへのコピーは replace 側）。

usage: python scripts/rerender_vp_longs.py [slug ...]
"""
import datetime as dt
import os
import subprocess
import sys
import time
from pathlib import Path

R = Path(__file__).resolve().parents[1]
LOG = R / 'out' / 'codex' / 'rerender_vp_longs.log'

# 差し替え日の早い順
SLUGS = ['calendar', 'einstein', 'moon', 'islands', 'magnitude', 'yakubusoku', 'leapsecond', 'sunrise', 'venus']

args = [a for a in sys.argv[1:]]
slugs = args or SLUGS

py = sys.executable
env = dict(os.environ)
env['PATH'] = str(R / 'tools' / 'ffmpeg' / 'bin') + os.pathsep + env.get('PATH', '')
env['PYTHONIOENCODING'] = 'utf8'


def say(msg):
    line = f'[{dt.datetime.now():%H:%M:%S}] {msg}'
    print(line, flush=True)
    with LOG.open('a', encoding='utf8') as f:
        f.write(line + '\n')


for slug in slugs:
    t0 = time.time()
    say(f'{slug}: 開始')
    p = subprocess.run([py, '-X', 'utf8', str(R / 'scripts' / 'vp.py'), slug, 'build'],
                       cwd=str(R), env=env)
    dt_s = time.time() - t0
    if p.returncode != 0:
        say(f'{slug}: 失敗 rc={p.returncode} {dt_s:.0f}s（続行）')
        continue
    v = R / 'out' / f'{slug}_video.mp4'
    say(f'{slug}: 完了 {dt_s:.0f}s / {v.stat().st_size / 2**20:.0f}MB')

say('すべて終了')
