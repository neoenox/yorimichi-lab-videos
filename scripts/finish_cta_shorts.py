"""Studioで差し替えたShort（data/short_cta_done.json）の後始末。APIの枠が戻ってから実行（16:00 JST以降）。
1. 新Shortに日本語字幕（upload/short_<slug>/subtitles_ja.srt）を付ける（既にあればスキップ）
2. 台帳 data/youtube_ids.json の short_<slug> を新IDに更新し、旧IDを superseded に入れる
旧版の削除は別途 `yt_api.py delete-superseded`（非公開・予約なしのものだけ）。
実行： cd scripts && PYTHONUTF8=1 python finish_cta_shorts.py"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import yt_api as Y
from googleapiclient.http import MediaFileUpload

yt = Y.service()
done = json.loads((Y.R / 'data' / 'short_cta_done.json').read_text(encoding='utf8'))
ids = Y.load_ids()


def find_new(old):
    # 新IDが台帳に無い回（賤ヶ岳）は、アップロード一覧から同じ予約時刻の動画を探す
    up = yt.channels().list(part='contentDetails', mine=True).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    vids = [i['contentDetails']['videoId'] for i in yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50).execute()['items']]
    return vids


for slug, d in done.items():
    new, old = d.get('new'), d['old']
    key = 'short_' + slug
    if not new:
        want = d['publishAt']
        for v in find_new(old):
            it = yt.videos().list(part='status', id=v).execute()['items'][0]['status']
            if v != old and it.get('publishAt', '').startswith(want[:10]) and it.get('privacyStatus') == 'private':
                new = v; d['new'] = v; break
    if not new:
        print('no new id', slug); continue
    have = yt.captions().list(part='snippet', videoId=new).execute().get('items', [])
    if not any(c['snippet'].get('language') == 'ja' and c['snippet'].get('trackKind') != 'asr' for c in have):
        srt = Y.R / 'upload' / key / 'subtitles_ja.srt'
        if srt.exists():
            yt.captions().insert(part='snippet', body=dict(snippet=dict(videoId=new, language='ja', name='', isDraft=False)),
                                 media_body=MediaFileUpload(str(srt), mimetype='application/octet-stream')).execute()
            print('captions ok', slug, new)
    e = ids.setdefault(key, {})
    if e.get('video_id') != new:
        sup = e.setdefault('superseded', [])
        if old not in sup and old != '7f1J3697tlE': sup.append(old)
        e['video_id'] = new
(Y.R / 'data' / 'short_cta_done.json').write_text(json.dumps(done, ensure_ascii=False, indent=1), encoding='utf8')
Y.save_ids(ids) if hasattr(Y, 'save_ids') else (Y.R / 'data' / 'youtube_ids.json').write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding='utf8')
print('done')
