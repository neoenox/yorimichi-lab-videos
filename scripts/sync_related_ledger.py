"""台帳 youtube_ids.json に回遊設定（関連動画）の情報を反映する。

各 Short エントリに次を追加する:
  "related": {
    "long_id": "<紐づく長尺の動画ID>",
    "short_id": "<Short自身の動画ID>",
    "done": true/false,
    "done_at": "<設定済みの場合の記録日>"   # 新規記録時のみ
  }

使い方:
  python scripts/sync_related_ledger.py --dry
  python scripts/sync_related_ledger.py --apply
"""
import glob
import json
import sys
from datetime import date
from pathlib import Path

R = Path(__file__).resolve().parents[1]
apply = '--apply' in sys.argv
ids_path = R / 'data' / 'youtube_ids.json'
done_path = R / 'data' / 'related_done.json'
ids = json.loads(ids_path.read_text(encoding='utf8'))
done = set(json.loads(done_path.read_text(encoding='utf8')))
today = date.today().isoformat()

changed = []
for f in sorted((R / 'data').glob('short_*.json')):
    d = json.loads(f.read_text(encoding='utf8'))
    if not isinstance(d, dict) or not d.get('long_id'):
        continue
    key = 'short_' + f.stem[6:]
    if key not in ids or not isinstance(ids[key], dict):
        continue
    short_id = ids[key].get('video_id')
    if not short_id:
        continue
    new = {
        'long_id': d['long_id'],
        'short_id': short_id,
        'done': short_id in done,
    }
    old = ids[key].get('related')
    if new['done'] and not (old or {}).get('done'):
        new['done_at'] = today
    elif (old or {}).get('done_at'):
        new['done_at'] = old['done_at']
    if old == new:
        continue
    changed.append((key, old, new))
    if apply:
        ids[key]['related'] = new

# related_done にあるのに spec の long_id から辿れなかった動画も記録する
covered = {v['related']['short_id'] for v in ids.values()
           if isinstance(v, dict) and 'related' in v}
for short_id in sorted(done - covered):
    for key, e in ids.items():
        if isinstance(e, dict) and e.get('video_id') == short_id:
            new = {
                'long_id': e.get('long_id', ''),
                'short_id': short_id,
                'done': True,
                'done_at': today,
            }
            if e.get('related') != new:
                changed.append((key, e.get('related'), new))
                if apply:
                    e['related'] = new
            break

print('更新件数:', len(changed))
for key, old, new in changed[:10]:
    print(key, '->', new)
if len(changed) > 10:
    print('...')
if apply:
    ids_path.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding='utf8')
    print('台帳を更新しました')
else:
    print('dry run（--apply で反映）')
