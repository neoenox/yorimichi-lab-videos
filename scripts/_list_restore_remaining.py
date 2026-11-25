"""ブラウザで復元すべき nolong=true の Short を、元の publishAt と一緒に出す。"""
import json
import subprocess
from pathlib import Path

R = Path(__file__).resolve().parents[1]
orig = json.loads(subprocess.check_output(
    ['git', 'show', 'HEAD:data/youtube_ids.json'], cwd=R, text=True, encoding='utf8'))
cur = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))
rows = []
for f in sorted((R / 'data').glob('short_*.json')):
    d = json.loads(f.read_text(encoding='utf8'))
    if not isinstance(d, dict) or d.get('nolong') is not True:
        continue
    key = 'short_' + f.stem[6:]
    if key not in orig or not orig[key].get('publishAt'):
        continue
    if cur.get(key, {}).get('publishAt'):
        continue  # 台帳上すでに復元済み
    # 日本時間に直す
    from datetime import datetime, timedelta, timezone
    pub = orig[key]['publishAt']
    dt = datetime.strptime(pub[:19], '%Y-%m-%dT%H:%M:%S') + timedelta(hours=9)
    rows.append((dt.strftime('%Y-%m-%d %H:%M'), key, cur.get(key, {}).get('video_id', '')))
rows.sort()
for r in rows:
    print(' | '.join(r))
print('TOTAL', len(rows))
