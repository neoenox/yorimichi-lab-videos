"""誤って解除した nolong=true の Short の予約を復元する。

使い方:
  python scripts/_restore_nolong_schedule.py --dry
  python scripts/_restore_nolong_schedule.py --apply
"""
import json
import subprocess
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))
import yt_api

apply = '--apply' in sys.argv
orig = json.loads(subprocess.check_output(
    ['git', 'show', 'HEAD:data/youtube_ids.json'], cwd=R, text=True, encoding='utf8'))
ids = yt_api.load_ids()
s = yt_api.service()

# nolong=true の Short を対象にする
targets = []
for f in sorted((R / 'data').glob('short_*.json')):
    d = json.loads(f.read_text(encoding='utf8'))
    if not isinstance(d, dict) or d.get('nolong') is not True:
        continue
    key = 'short_' + f.stem[6:]
    if key not in orig or not orig[key].get('publishAt'):
        continue
    if key not in ids or not ids[key].get('video_id'):
        continue
    targets.append((key, ids[key]['video_id'], orig[key]['publishAt']))

if not apply:
    live = []
    for key, vid, pub in targets:
        items = s.videos().list(part='status', id=vid).execute().get('items', [])
        if items and not items[0]['status'].get('publishAt'):
            live.append((key, vid, pub))
    print('復元対象:', len(live))
    for t in live:
        print(*t, sep=' | ')
    sys.exit(0)
print('復元対象:', len(targets))

ok, fail = [], []
for key, vid, pub in targets:
    items = s.videos().list(part='status', id=vid).execute().get('items', [])
    if not items:
        continue
    if items[0]['status'].get('publishAt'):
        continue  # 既に予約が残っている場合は何もしない
    try:
        s.videos().update(part='status', body={
            'id': vid,
            'status': {
                'privacyStatus': 'private',
                'publishAt': pub,
                'selfDeclaredMadeForKids': False,
            },
        }).execute()
        ids[key]['publishAt'] = pub
        ok.append(key)
        print('OK', key, vid, pub)
    except Exception as e:
        fail.append((key, str(e)[:100]))
        print('FAIL', key, vid, str(e)[:100])

(R / 'data' / 'youtube_ids.json').write_text(
    json.dumps(ids, ensure_ascii=False, indent=1), encoding='utf8')
print(f'完了: 成功 {len(ok)} / 失敗 {len(fail)}')
for f in fail:
    print('FAILED', f)
