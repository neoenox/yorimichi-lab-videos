import glob
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))
import yt_api

s = yt_api.service()
ids = yt_api.load_ids()

# long_id を持つ Short のキーと video_id を集める
long_paired = {}
for f in sorted((R / 'data').glob('short_*.json')):
    slug = f.stem[6:]
    d = json.loads(f.read_text(encoding='utf8'))
    if not isinstance(d, dict) or not d.get('long_id'):
        continue
    k = 'short_' + slug
    if k in ids and isinstance(ids[k], dict) and ids[k].get('video_id'):
        long_paired[ids[k]['video_id']] = (k, d['long_id'])

rows = []
for vid, (key, long_id) in long_paired.items():
    items = s.videos().list(part='status', id=vid).execute().get('items', [])
    if not items:
        continue
    st = items[0]['status']
    if st.get('publishAt') and st['privacyStatus'] == 'private':
        rows.append((st['publishAt'], key, vid, long_id))
rows.sort()
for r in rows:
    print(' | '.join(r))
print('TOTAL', len(rows))
