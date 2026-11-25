import glob
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))
import yt_api

s = yt_api.service()
ids = set()
for f in glob.glob(str(R / 'data' / 'short_*.json')):
    d = json.loads(Path(f).read_text(encoding='utf8'))
    if isinstance(d, dict) and d.get('long_id'):
        ids.add(d['long_id'])

found = {}
ordered = sorted(ids)
for i in range(0, len(ordered), 40):
    chunk = ordered[i:i + 40]
    res = s.videos().list(part='status', id=','.join(chunk)).execute()
    for it in res.get('items', []):
        found[it['id']] = it['status']['privacyStatus']

print('unique long_ids', len(ids), 'found', len(found))
print('missing', len(ids - set(found)))
for m in sorted(ids - set(found)):
    print('MISSING', m)
print('qzxzekd5j-I:', found.get('qzxzekd5j-I', 'MISSING'))
