import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))
import yt_api

s = yt_api.service()
ids = yt_api.load_ids()

# API 実測で公開予約が残っている動画だけを集める
live = {}
for key, e in ids.items():
    if not isinstance(e, dict) or not e.get('video_id'):
        continue
    live[e['video_id']] = key

rows = []
for vid, key in live.items():
    items = s.videos().list(part='status', id=vid).execute().get('items', [])
    if not items:
        continue
    st = items[0]['status']
    if st.get('publishAt') and st['privacyStatus'] == 'private':
        rows.append((st['publishAt'], key, vid))
rows.sort()
for r in rows:
    print(' | '.join(r))
print('TOTAL', len(rows))
