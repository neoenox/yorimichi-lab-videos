"""公開予約の実測チェック（YouTube API 読み取りのみ）。

usage:
  python scripts/check_slots.py            # 前日〜3日先の予約と同時刻の重複を表示
  python scripts/check_slots.py --days 7   # 範囲を広げる

なぜ必要か（2026-11-19）:
  `data/youtube_ids.json` の `publishAt` は予約時にしか書かれないため、API の実態より古い。
  台帳だけを見て重複を判断すると、11/19 19:00 の長尺2本（27_forest と 79_hibiya）のような
  同時刻予約を見落とす。台帳ではなく API を正とする。

使うAPI: `videos().list` のみ（336本で約7ユニット）。書き込みはしない。
--check-dups 相当の判定は終了コードで返す（重複あり=1）。
"""
import argparse
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
import yt_api

JST = datetime.timedelta(hours=9)


def to_jst(iso):
    if not iso:
        return None
    t = datetime.datetime.strptime(iso, '%Y-%m-%dT%H:%M:%SZ') + JST
    return t.strftime('%Y-%m-%d %H:%M')


def fetch_all(yt, ids):
    """pack -> status/snippet（50件ずつ）。"""
    items = sorted(ids.items())
    got = {}
    for i in range(0, len(items), 50):
        chunk = items[i:i + 50]
        res = yt.videos().list(part='status,snippet',
                               id=','.join(v['video_id'] for _, v in chunk),
                               maxResults=50).execute()
        for it in res.get('items', []):
            got[it['id']] = it
    return got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=3, help='何日先まで見るか（既定3）')
    ap.add_argument('--back', type=int, default=1, help='何日前から見るか（既定1）')
    a = ap.parse_args()

    ids = yt_api.load_ids()
    yt = yt_api.service()
    got = fetch_all(yt, ids)

    now = datetime.datetime.utcnow()
    lo = now - datetime.timedelta(days=a.back)
    hi = now + datetime.timedelta(days=a.days)

    rows, missing = [], []
    for pack, v in sorted(ids.items()):
        it = got.get(v['video_id'])
        if not it:
            missing.append(pack)
            continue
        st = it['status']
        pa = st.get('publishAt')
        if not pa:
            continue
        t = datetime.datetime.strptime(pa, '%Y-%m-%dT%H:%M:%SZ')
        if lo <= t <= hi:
            rows.append((pa, pack, v['video_id'], st['privacyStatus'], it['snippet']['title']))
    rows.sort()

    print(f'== 台帳 {len(ids)} 本 / API 取得 {len(got)} / 不在 {len(missing)} ==')
    if missing:
        print('  不在:', ', '.join(missing))
    print(f'== 予約: {-a.back}日 〜 +{a.days}日（JST）==')
    for pa, pack, vid, priv, title in rows:
        print(f'{to_jst(pa)} | {priv:8s} | {pack:30s} | {vid} | {title[:40]}')

    slots = {}
    for pa, pack, vid, _priv, _title in rows:
        slots.setdefault(pa, []).append(f'{pack}({vid})')
    dup = {k: v for k, v in slots.items() if len(v) > 1}
    print('== 同時刻の重複 ==')
    if not dup:
        print('  なし')
    else:
        for k, v in sorted(dup.items()):
            print(f'  NG {to_jst(k)} -> ' + ', '.join(v))
    return 1 if dup else 0


if __name__ == '__main__':
    sys.exit(main())
