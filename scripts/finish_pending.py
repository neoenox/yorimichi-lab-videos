"""APIクォータが回復したあとに、残りのアップロード作業をまとめて片付ける。

usage:
  python scripts/finish_pending.py --dry      # 何をするか確認だけ
  python scripts/finish_pending.py            # 実行

やること（何度実行しても安全）:
  1. Short「桶狭間」をアップロード（未登録なら）→ 2026-11-03 20:00 に公開予約 → 字幕
  2. 長尺「桶狭間」の日本語字幕を添付（未添付なら）
  3. Short「明治5年」の概要欄を、現行の長尺ID（0BUGmgyrARE）に更新
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yt_api
from googleapiclient.http import MediaFileUpload

DRY = '--dry' in sys.argv
SHORT_PACK = 'short_oke'
SHORT_AT = '2026-11-03 20:00'
LONG_PACK = '14_okehazama'
CAL_PACK = 'short_calendar'


def plan(msg):
    print(('[dry] ' if DRY else '') + msg)


def caption(yt, pack, vid):
    ja = [c for c in yt.captions().list(part='snippet', videoId=vid).execute().get('items', [])
          if c['snippet'].get('language') == 'ja']
    if ja:
        plan(f'{pack}: 字幕は登録済み')
        return
    plan(f'{pack}: 字幕を添付')
    if DRY:
        return
    yt.captions().insert(
        part='snippet',
        body=dict(snippet=dict(videoId=vid, language='ja', name='', isDraft=False)),
        media_body=MediaFileUpload(str(yt_api.R / 'upload' / pack / 'subtitles_ja.srt'),
                                   mimetype='application/octet-stream')).execute()


def main():
    ids = yt_api.load_ids()

    # 1) Short 桶狭間
    if SHORT_PACK not in ids:
        plan(f'{SHORT_PACK}: アップロード')
        if not DRY:
            yt_api.cmd_upload(SHORT_PACK)
            ids = yt_api.load_ids()
    else:
        plan(f'{SHORT_PACK}: 登録済み {ids[SHORT_PACK]["video_id"]}')

    vid = ids.get(SHORT_PACK, {}).get('video_id')
    if DRY:
        plan(f'{SHORT_PACK}: {vid} を {SHORT_AT} に公開予約')
    elif vid:
        yt = yt_api.service()
        st = yt.videos().list(part='status', id=vid).execute()['items'][0]['status']
        if st.get('publishAt'):
            plan(f'{SHORT_PACK}: 予約済み {st["publishAt"]}')
        else:
            yt_api.cmd_schedule(vid, SHORT_AT)
        caption(yt, SHORT_PACK, vid)

    # 2) 長尺 桶狭間の字幕
    long_id = ids.get(LONG_PACK, {}).get('video_id')
    if long_id:
        if DRY:
            plan(f'{LONG_PACK}: {long_id} の字幕を確認/添付')
        else:
            caption(yt_api.service(), LONG_PACK, long_id)

    # 3) Short 明治5年の概要欄
    plan(f'{CAL_PACK}: 概要欄を更新（長尺ID 0BUGmgyrARE）')
    if not DRY and CAL_PACK in ids:
        yt_api.cmd_redesc(CAL_PACK)


if __name__ == '__main__':
    main()
