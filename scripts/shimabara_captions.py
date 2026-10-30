"""島原の新版（ブラウザでアップ済み 1zReEyHdtq0 / SJsfLzzAq1c）に、字幕を付ける。APIの枠が戻ってから実行（captions.insert は約400単位×2）。
実行： cd scripts && PYTHONUTF8=1 python shimabara_captions.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import yt_api as Y
from googleapiclient.http import MediaFileUpload
yt = Y.service()
for vid, pack in [('1zReEyHdtq0', '37_shimabara'), ('SJsfLzzAq1c', 'short_shimabara')]:
    have = yt.captions().list(part='snippet', videoId=vid).execute().get('items', [])
    if any(c['snippet'].get('language') == 'ja' and not c['snippet'].get('trackKind') == 'asr' for c in have):
        print('already', vid); continue
    yt.captions().insert(part='snippet', body=dict(snippet=dict(videoId=vid, language='ja', name='', isDraft=False)),
                         media_body=MediaFileUpload(str(Y.R / 'upload' / pack / 'subtitles_ja.srt'), mimetype='application/octet-stream')).execute()
    print('captions ok', vid)
