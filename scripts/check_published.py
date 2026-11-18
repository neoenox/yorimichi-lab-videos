"""予約した動画が、公開されているかを確かめる(読み取りだけ)。
  python scripts/check_published.py short_solo_kamakura_seiritsu short_solo_planimal ...
台帳(data/youtube_ids.json)のキーを渡す。各動画の公開状態・予約時刻・再生数・コメント数を表示し、予約時刻を過ぎているのに private のものを「要確認」と出す。"""
import sys, json, datetime
from pathlib import Path
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))
sys.stdout.reconfigure(encoding='utf8')
import yt_api
L = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))
keys = sys.argv[1:]
ids = {k: L[k]['video_id'] for k in keys if k in L}
miss = [k for k in keys if k not in L]
s = yt_api.service()
now = datetime.datetime.now(datetime.timezone.utc)
bad = []
for it in s.videos().list(part='status,statistics', id=','.join(ids.values())).execute()['items']:
    k = next(k for k, v in ids.items() if v == it['id'])
    st, stt = it['status'], it['statistics']
    pa = st.get('publishAt')
    flag = ''
    if st['privacyStatus'] != 'public' and pa and datetime.datetime.fromisoformat(pa.replace('Z', '+00:00')) < now:
        flag = '  ← 予約時刻を過ぎたのに公開されていない(要確認)'; bad.append(k)
    print(f"{k:34s} {it['id']} {st['privacyStatus']:8s} 予約={pa} 再生={stt.get('viewCount')} コメント={stt.get('commentCount')}{flag}")
for k in miss:
    print('台帳に無い:', k)
print('結果:', '要確認あり ' + str(bad) if bad else 'すべて問題なし')
