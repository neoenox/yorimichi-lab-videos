"""長尺誘導型Shortの公開予約を解除する（非公開のまま保留）。

使い方:
  python scripts/_cancel_scheduled.py --dry    # 対象だけ表示
  python scripts/_cancel_scheduled.py --apply  # 実行
"""
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))
import yt_api

apply = '--apply' in sys.argv
s = yt_api.service()
ids = yt_api.load_ids()

# long_id を持つ Short と台帳キーの対応
long_paired = {}
for f in sorted((R / 'data').glob('short_*.json')):
    slug = f.stem[6:]
    d = json.loads(f.read_text(encoding='utf8'))
    if not isinstance(d, dict) or not d.get('long_id'):
        continue
    k = 'short_' + slug
    if k in ids and isinstance(ids[k], dict) and ids[k].get('video_id'):
        long_paired[ids[k]['video_id']] = k

targets = []
for vid, key in long_paired.items():
    items = s.videos().list(part='status', id=vid).execute().get('items', [])
    if not items:
        continue
    st = items[0]['status']
    if st.get('publishAt') and st['privacyStatus'] == 'private':
        targets.append((vid, key))

targets.sort(key=lambda x: x[1])
print('対象:', len(targets))

if not apply:
    for vid, key in targets:
        print(key, vid)
    sys.exit(0)

ok, fail = [], []
for vid, key in targets:
    try:
        s.videos().update(part='status', body={
            'id': vid,
            'status': {
                'privacyStatus': 'private',
                'publishAt': None,
                'selfDeclaredMadeForKids': False,
            },
        }).execute()
        ids[key].pop('publishAt', None)
        ok.append(key)
        print('OK', key, vid)
    except Exception as e:
        fail.append((key, str(e)[:100]))
        print('FAIL', key, vid, str(e)[:100])

(R / 'data' / 'youtube_ids.json').write_text(
    json.dumps(ids, ensure_ascii=False, indent=1), encoding='utf8')
print(f'完了: 成功 {len(ok)} / 失敗 {len(fail)}')
for f in fail:
    print('FAILED', f)
