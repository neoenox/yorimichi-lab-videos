"""内部メモを削除した spec から説明欄を作り直し、アップ済み動画に反映する。

使い方:
  python scripts/_fix_published_descriptions.py --dry
  python scripts/_fix_published_descriptions.py --apply
"""
import json
import os
import subprocess
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
apply = '--apply' in sys.argv
env = dict(os.environ)
env['PYTHONPATH'] = r'C:/Users/neoen/AppData/Local/Programs/Python/Python311/Lib/site-packages'
env['PYTHONUTF8'] = '1'

# 台帳のキーと spec の対応を作る
ids = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))
targets = []
for f in sorted((R / 'data').glob('short_*.json')):
    key = 'short_' + f.stem[6:]
    e = ids.get(key)
    if not isinstance(e, dict) or not e.get('video_id'):
        continue
    targets.append((key, e['video_id']))

for a in sys.argv[1:]:
    if a.startswith('--limit='):
        targets = targets[:int(a.split('=')[1])]
print('対象:', len(targets))
if not apply:
    for t in targets[:10]:
        print(*t, sep=' | ')
    sys.exit(0)

ok, fail = [], []
for key, vid in targets:
    try:
        # 説明欄ファイルを作り直す（pack_short.py は spec を読む）
        r = subprocess.run([sys.executable, str(R / 'scripts' / 'pack_short.py'), key],
                           cwd=R, capture_output=True, text=True, encoding='utf8', env=env)
        desc_path = R / 'upload' / key / 'description.txt'
        if not desc_path.exists():
            fail.append((key, 'description.txt not created'))
            continue
        # 説明欄だけ更新
        r2 = subprocess.run([sys.executable, str(R / 'scripts' / 'yt_api.py'), 'redesc', key],
                            cwd=R, capture_output=True, text=True, encoding='utf8', env=env)
        if r2.returncode:
            fail.append((key, r2.stderr[:100] or r2.stdout[:100]))
            continue
        ok.append(key)
        print('OK', key, vid)
    except Exception as e:
        fail.append((key, str(e)[:100]))

print(f'完了: 成功 {len(ok)} / 失敗 {len(fail)}')
for f in fail[:10]:
    print('FAILED', f)
