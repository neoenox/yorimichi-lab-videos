"""browser_uploads.txt（ブラウザ投稿の記録）から、data/youtube_ids.json に無いパックを補う。

ブラウザ（Studio）で上げた動画は youtube_ids.json に載っていないことがあり、そのままだと
概要欄の更新（redesc）や予約変更を API から行えない。投稿記録を正として台帳をそろえる。

usage: python scripts/reconcile_ids.py [--dry]
"""
import json
import pathlib
import re
import sys

R = pathlib.Path(__file__).resolve().parents[1]
IDS = R / 'data' / 'youtube_ids.json'
SRC = R / 'out' / 'codex' / 'browser_uploads.txt'
VALID = re.compile(r'^(short_[a-z0-9_]+|\d{2}_[a-z0-9_]+)$')
DRY = '--dry' in sys.argv

ids = json.loads(IDS.read_text(encoding='utf8')) if IDS.exists() else {}
added = []
for line in SRC.read_text(encoding='utf8').splitlines():
    parts = line.split()
    if len(parts) < 3:
        continue
    pack, vid = parts[1], parts[2]
    if not VALID.match(pack) or len(vid) != 11:
        continue  # 「superseded browser」などの見出し行を除く
    if pack in ids:
        continue
    added.append((pack, vid))
    if not DRY:
        ids[pack] = dict(video_id=vid, privacy='private', via='browser', superseded=[])

if not DRY:
    IDS.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding='utf8')
print(('[dry] ' if DRY else '') + f'added {len(added)}')
for p, v in added:
    print('  ', p, v)
