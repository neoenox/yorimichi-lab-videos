"""Short を作り直し、必要ならパックまで更新する。

usage: python scripts/render_shorts.py <slug> [<slug> ...]
       python scripts/render_shorts.py --list oke,scurvy,compass   # カンマ区切りでもよい
2回目以降は out/ が新しくなるだけで、パックは replace_short が実行時に更新する。
"""
import subprocess
import sys
import time
from pathlib import Path

R = Path(__file__).resolve().parents[1]
PACK = {
    'oke': '14_okehazama',
    'worldmap': '01_world_map_distortion',
    'honnoji': '02_honnoji_incident',
    'ninja': '03_ninja_myths',
}

args = sys.argv[1:]
if '--list' in args:
    args = [a for a in args if a != '--list']
slugs = [s for a in args for s in a.split(',') if s.strip()]

py = sys.executable
for slug in slugs:
    t0 = time.time()
    print(f'=== {slug} 開始', flush=True)
    p = subprocess.run([py, '-X', 'utf8', str(R / 'scripts' / 'make_short2.py'), slug],
                       cwd=str(R))
    print(f'=== {slug} 描画 rc={p.returncode} {time.time() - t0:.0f}s', flush=True)
    if p.returncode != 0:
        print(f'!!! {slug} 失敗。続行', flush=True)
        continue
    if slug in PACK:
        q = subprocess.run([py, '-X', 'utf8', str(R / 'scripts' / 'pack_short.py'), slug, PACK[slug]],
                           cwd=str(R))
        print(f'=== {slug} パック rc={q.returncode}', flush=True)
print('すべて終了', flush=True)
