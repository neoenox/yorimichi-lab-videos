"""字幕（日本語）をあとから添付する。APIクォータが回復したら実行する。

usage: python scripts/attach_captions.py 14_okehazama [video_id]
動画IDを省略した場合は data/youtube_ids.json の登録IDを使う。
すでに日本語トラックがある場合は何もしない（多重登録を防ぐ）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yt_api
from googleapiclient.http import MediaFileUpload


def main():
    pack = sys.argv[1]
    ids = yt_api.load_ids()
    vid = sys.argv[2] if len(sys.argv) > 2 else ids.get(pack, {}).get('video_id')
    if not vid:
        sys.exit(f'{pack} の動画IDが不明です')
    d = yt_api.R / 'upload' / pack
    srt = d / 'subtitles_ja.srt'
    if not srt.exists():
        sys.exit(f'{srt} がありません')

    yt = yt_api.service()
    existing = yt.captions().list(part='snippet', videoId=vid).execute().get('items', [])
    ja = [c for c in existing if c['snippet'].get('language') == 'ja']
    if ja:
        print(f'{vid}: 日本語字幕は登録済み ({ja[0]["id"]})')
        return

    yt.captions().insert(
        part='snippet',
        body=dict(snippet=dict(videoId=vid, language='ja', name='', isDraft=False)),
        media_body=MediaFileUpload(str(srt), mimetype='application/octet-stream'),
    ).execute()
    print(f'{vid}: 字幕を添付しました ({srt.name})')


if __name__ == '__main__':
    main()
