"""漢数字が残っている長尺を作り直す（映像に焼き込まれた字幕を算用数字にする）。

usage: python scripts/rerender_batch.py [slug ...]
  引数なし: 対象リストを順に処理（字幕に数量漢数字が残っている長尺）
動画は out/<slug>_video.mp4 に上書き。アップロード用パックは触らない（差し替えは別作業）。
"""
import json
import os
import subprocess
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
LOG = R / 'out' / 'codex' / 'rerender.log'

# 公開日が近すぎる koku(10/21)・compass(10/22) は除く
SLUGS = ['gdp', 'scurvy', 'calendar', 'einstein', 'moon', 'islands', 'magnitude',
         'yakubusoku', 'leapsecond', 'sunrise', 'venus']


def main():
    slugs = sys.argv[1:] or SLUGS
    env = dict(os.environ)
    env['PATH'] = str(R / 'tools' / 'ffmpeg' / 'bin') + os.pathsep + env['PATH']
    env['PYTHONIOENCODING'] = 'utf8'
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open('a', encoding='utf8') as log:
        for slug in slugs:
            log.write(f'=== {slug} start\n')
            log.flush()
            p = subprocess.run([sys.executable, str(R / 'scripts' / 'vp.py'), slug, 'build'],
                               cwd=str(R), env=env, capture_output=True, text=True, encoding='utf8', errors='replace')
            tail = [ln for ln in (p.stdout or '').splitlines() if ln.strip()][-2:]
            log.write(f'=== {slug} rc={p.returncode} ' + ' | '.join(tail) + '\n')
            if p.returncode != 0:
                log.write((p.stderr or '')[-1500:] + '\n')
            log.flush()
    print('done', len(slugs))


if __name__ == '__main__':
    main()
