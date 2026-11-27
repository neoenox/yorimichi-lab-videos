"""YouTube Analytics(視聴維持率など)を読む。アップロード用の認証(secrets/token.json)とは別のトークン(secrets/token_analytics.json)を使う。
  python scripts/yt_analytics.py auth          # 初回だけ。ブラウザが開くので、寄り道ラボのアカウントで「許可」を押す
  python scripts/yt_analytics.py videos        # 公開Shortsの 平均視聴時間・平均視聴率・視聴回数 を、台帳の全公開動画で一覧
  python scripts/yt_analytics.py curve <video_id>   # その動画の視聴維持率の曲線(動画の何%地点で、何%が見ているか)
事前に、Google Cloud(プロジェクト yorimichi-lab-upload)で「YouTube Analytics API」を有効にしておく。
注意：サムネイルのインプレッション数・クリック率は、Analytics APIでは取れない(Studio画面だけ)可能性が高い。"""
import json, sys, datetime
from pathlib import Path
R = Path(__file__).resolve().parents[1]
CLIENT = R / 'secrets' / 'client_secret.json'
TOKEN = R / 'secrets' / 'token_analytics.json'
SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly', 'https://www.googleapis.com/auth/youtube.readonly']
sys.stdout.reconfigure(encoding='utf8')


def auth():
    from google_auth_oauthlib.flow import InstalledAppFlow
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT), SCOPES)
    c = flow.run_local_server(port=0, prompt='consent', authorization_prompt_message='ブラウザで寄り道ラボのアカウントを選んで「許可」を押してください')
    TOKEN.write_text(c.to_json(), encoding='utf8'); print('保存しました', TOKEN)


def svc():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    if not TOKEN.exists(): sys.exit('先に: python scripts/yt_analytics.py auth')
    c = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if c.expired and c.refresh_token:
        c.refresh(Request()); TOKEN.write_text(c.to_json(), encoding='utf8')
    return build('youtubeAnalytics', 'v2', credentials=c)


def q(a, **kw):
    start = kw.pop('start', '2026-10-01'); end = kw.pop('end', datetime.date.today().isoformat())
    return a.reports().query(ids='channel==MINE', startDate=start, endDate=end, **kw).execute()


def videos():
    a = svc(); ids = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))
    names = {v['video_id']: k for k, v in ids.items() if v.get('video_id')}
    r = q(a, metrics='views,averageViewDuration,averageViewPercentage,estimatedMinutesWatched,likes', dimensions='video', sort='-views', maxResults=200)
    print('視聴回数 | 平均視聴時間(秒) | 平均視聴率(%) | 高評価 | 動画')
    for row in r.get('rows', []):
        vid, views, avd, avp, mins, likes = row
        print(f'{views:>6} | {avd:>6.1f} | {avp:>6.1f} | {likes:>3} | {names.get(vid, vid)}')


def curve(vid):
    a = svc()
    r = q(a, metrics='audienceWatchRatio,relativeRetentionPerformance', dimensions='elapsedVideoTimeRatio', filters=f'video=={vid}')
    print('動画の経過(%) | その地点で見ている割合 | 同じ長さの動画との比較(0〜1)')
    for t, w, rel in r.get('rows', []):
        print(f'{t * 100:>5.0f}% | {w * 100:>6.1f}% | {rel:.2f}')


if __name__ == '__main__':
    c = sys.argv[1] if len(sys.argv) > 1 else ''
    {'auth': auth, 'videos': videos}.get(c, lambda: curve(sys.argv[2]) if c == 'curve' else print(__doc__))()
