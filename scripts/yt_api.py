"""YouTube Data API で、upload/<pack>/ を「非公開」でアップロードする。

使い方:
  python scripts/yt_api.py auth                 # 初回のみ。ブラウザで寄り道ラボのアカウントを承認
  python scripts/yt_api.py whoami               # 認証中のチャンネルを表示
  python scripts/yt_api.py upload 03_ninja_myths [--dry] [--new-version]   # 動画・サムネ・字幕を非公開で登録（作り直したときは --new-version。旧IDは superseded に残す）
  python scripts/yt_api.py schedule <動画ID> "2026-10-23 19:00"   # 公開予約（日本時間。許可を得てから）
  python scripts/yt_api.py delete-superseded    # 作り直しで不要になった旧版（非公開のものだけ）を削除
  python scripts/yt_api.py list                 # チャンネルの動画と公開状態

方針: このスクリプトは公開しない（privacyStatus は常に private）。公開は人が Studio で行う。
認証情報は secrets/（git管理外）。アップロード済みは data/youtube_ids.json に記録し、二重投稿を防ぐ。
"""
import socket as _socket
_orig_gai = _socket.getaddrinfo


def _gai_v6_first(*a, **k):
    """この環境ではIPv4でYouTube APIに接続できない時があるので、IPv6を先に試す。"""
    r = _orig_gai(*a, **k)
    return sorted(r, key=lambda x: 0 if x[0] == _socket.AF_INET6 else 1)


_socket.getaddrinfo = _gai_v6_first

import json, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
SEC = R / 'secrets'
CLIENT = SEC / 'client_secret.json'
TOKEN = SEC / 'token.json'
IDS = R / 'data' / 'youtube_ids.json'
CHANNEL_ID = 'UCN_do9fcssctmkrNsRWOO9A'  # 寄り道ラボ
SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube.force-ssl']
CATEGORY = '27'  # Education


def creds():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    c = Credentials.from_authorized_user_file(str(TOKEN), SCOPES) if TOKEN.exists() else None
    if c and c.expired and c.refresh_token:
        c.refresh(Request())
        TOKEN.write_text(c.to_json(), encoding='utf8')
    if not c or not c.valid:
        sys.exit('未認証です。先に: python scripts/yt_api.py auth')
    return c


def service():
    from googleapiclient.discovery import build
    return build('youtube', 'v3', credentials=creds())


def cmd_auth():
    from google_auth_oauthlib.flow import InstalledAppFlow
    if not CLIENT.exists():
        sys.exit(f'{CLIENT} がありません（Google Cloud で作成した OAuth クライアントJSONを置く）')
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT), SCOPES)
    c = flow.run_local_server(port=0, prompt='consent',
                              authorization_prompt_message='ブラウザで寄り道ラボのアカウントを選んで承認してください')
    TOKEN.write_text(c.to_json(), encoding='utf8')
    cmd_whoami()


def mine(yt):
    return yt.channels().list(part='id,snippet', mine=True).execute().get('items', [])


def cmd_whoami():
    items = mine(service())
    for it in items:
        print(it['id'], it['snippet']['title'])
    if not any(it['id'] == CHANNEL_ID for it in items):
        print('!! 寄り道ラボ(%s)ではありません。個人チャンネルへは上げません。auth をやり直してください' % CHANNEL_ID)


def load_ids():
    return json.loads(IDS.read_text(encoding='utf8')) if IDS.exists() else {}


def save_ids_atomic(ids):
    """台帳の既存ファイルを途中書き込みで壊さないよう原子的に保存する。"""
    import os
    import tempfile

    IDS.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf8', dir=IDS.parent,
            prefix=IDS.name + '.', suffix='.tmp', delete=False
        ) as temp:
            temp_name = temp.name
            json.dump(ids, temp, ensure_ascii=False, indent=1)
            temp.flush()
            os.fsync(temp.fileno())
        os.replace(temp_name, IDS)
    finally:
        if temp_name is not None:
            Path(temp_name).unlink(missing_ok=True)


def cmd_upload(pack, dry=False, new_version=False):
    from googleapiclient.http import MediaFileUpload
    d = R / 'upload' / pack
    title = (d / 'title.txt').read_text(encoding='utf8').strip()
    desc = (d / 'description.txt').read_text(encoding='utf8').strip()
    tags = [t.strip() for t in (d / 'tags.txt').read_text(encoding='utf8').split(',') if t.strip()]
    assert len(title) <= 100, f'タイトルが{len(title)}字'
    assert len(desc) <= 5000, f'概要欄が{len(desc.encode("utf8"))}バイト'
    assert sum(len(t) for t in tags) <= 480, 'タグが長すぎる'
    assert '<' not in title + desc and '>' not in title + desc, '概要欄/タイトルに < > は使えない'
    ids = load_ids()
    if pack in ids and not new_version:
        sys.exit(f'{pack} は登録済み: {ids[pack]["video_id"]}（二重投稿を防ぐため中止。作り直した動画を別IDで上げるなら --new-version）')
    print(f'{pack}: 「{title}」 tags={len(tags)} desc={len(desc.encode("utf8"))}B')
    if dry:
        return
    yt = service()
    if not any(it['id'] == CHANNEL_ID for it in mine(yt)):
        sys.exit('認証中のチャンネルが寄り道ラボではありません。中止')
    body = dict(snippet=dict(title=title, description=desc, tags=tags, categoryId=CATEGORY,
                             defaultLanguage='ja', defaultAudioLanguage='ja'),
                status=dict(privacyStatus='private', selfDeclaredMadeForKids=False,
                            containsSyntheticMedia=False, embeddable=True, license='youtube'))
    req = yt.videos().insert(part='snippet,status', body=body,
                             media_body=MediaFileUpload(str(d / 'video.mp4'), chunksize=8 * 1024 * 1024, resumable=True))
    resp = None
    import time
    fails = 0
    while resp is None:
        try:
            st, resp = req.next_chunk(num_retries=5)
        except Exception as e:  # 回線の一時的な切れ（再開可能なアップロードなので、同じ位置から再試行）
            if 'quota' in str(e).lower():
                raise  # クォータ切れは待っても直らないので、すぐ上位へ
            fails += 1
            print('  retry', fails, type(e).__name__, flush=True)
            if fails > 30:
                raise
            time.sleep(min(60, 5 * fails))
            continue
        if st:
            print(f'  upload {int(st.progress() * 100)}%', flush=True)
    vid = resp['id']
    print('video id', vid, resp['status']['privacyStatus'])
    previous = ids.get(pack, {})
    ids[pack] = dict(video_id=vid, privacy=resp['status']['privacyStatus'], via='api',
                     superseded=previous.get('superseded', []) + ([previous['video_id']] if previous.get('video_id') else []),
                     deleted=previous.get('deleted', []))
    # アップロード済みIDを失わないよう原子的に記録する（失敗時は表示したIDを手動で復旧）。
    save_ids_atomic(ids)
    if (d / 'thumbnail.jpg').exists():
        yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(d / 'thumbnail.jpg'))).execute()
        print('thumbnail ok')
    if (d / 'subtitles_ja.srt').exists():
      yt.captions().insert(part='snippet', body=dict(snippet=dict(videoId=vid, language='ja', name='', isDraft=False)),
                         media_body=MediaFileUpload(str(d / 'subtitles_ja.srt'), mimetype='application/octet-stream')).execute()
      print('captions ok')


def cmd_finish(pack, vid, at=None):
    """ブラウザ（Studio）で動画本体だけを上げた場合の仕上げ。台帳に登録（旧IDは superseded へ）→ タイトル・概要欄・タグ → サムネイル → 字幕 → 公開予約（at があれば）。API枠は約2,000ユニット/本のところ、約600で済む。"""
    from googleapiclient.http import MediaFileUpload
    d = R / 'upload' / pack
    title = (d / 'title.txt').read_text(encoding='utf8').strip()
    desc = (d / 'description.txt').read_text(encoding='utf8').strip()
    tags = [t.strip() for t in (d / 'tags.txt').read_text(encoding='utf8').split(',') if t.strip()]
    assert len(title) <= 100 and len(desc) <= 5000 and '<' not in title + desc and '>' not in title + desc
    yt = service()
    if not any(it['id'] == CHANNEL_ID for it in mine(yt)):
        sys.exit('認証中のチャンネルが寄り道ラボではありません。中止')
    ids = load_ids()
    old = ids.get(pack, {}).get('video_id')
    status = dict(privacyStatus='private', selfDeclaredMadeForKids=False, embeddable=True, license='youtube')
    if at:
        import datetime as dt
        t = dt.datetime.strptime(at, '%Y-%m-%d %H:%M') - dt.timedelta(hours=9)
        status['publishAt'] = t.strftime('%Y-%m-%dT%H:%M:00Z')
    else:   # 予約済みの動画に finish しても、公開予約を消さない
        cur = yt.videos().list(part='status', id=vid).execute()['items'][0]['status']
        if cur.get('publishAt'): status['publishAt'] = cur['publishAt']
    yt.videos().update(part='snippet,status', body=dict(id=vid, snippet=dict(title=title, description=desc, tags=tags, categoryId=CATEGORY,
                       defaultLanguage='ja', defaultAudioLanguage='ja'), status=status)).execute()
    print('metadata ok', status.get('publishAt', ''))
    if (d / 'thumbnail.jpg').exists():
        yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(d / 'thumbnail.jpg'))).execute(); print('thumbnail ok')
    if (d / 'subtitles_ja.srt').exists():
        yt.captions().insert(part='snippet', body=dict(snippet=dict(videoId=vid, language='ja', name='', isDraft=False)),
                             media_body=MediaFileUpload(str(d / 'subtitles_ja.srt'), mimetype='application/octet-stream')).execute(); print('captions ok')

    # API の全工程が完了するまで旧版を削除候補にしない。
    if old != vid:
        ids[pack] = dict(video_id=vid, privacy='private', via='browser',
                         superseded=ids.get(pack, {}).get('superseded', []) + ([old] if old else []),
                         deleted=ids.get(pack, {}).get('deleted', []))
        save_ids_atomic(ids)
        print('ledger', pack, old, '->', vid)


def cmd_delete_superseded():
    """削除成功を確認した非公開動画だけを superseded から deleted に移す。

    取得不能・削除失敗は保留し、非ゼロ終了で知らせる。台帳は原子的に保存する。
    """
    yt = service()
    if not any(it['id'] == CHANNEL_ID for it in mine(yt)):
        sys.exit('認証中のチャンネルが寄り道ラボではありません。削除を中止')
    ids = load_ids()
    pending = []
    quota_exceeded = False
    for pack, rec in ids.items():
        for vid in list(rec.get('superseded', [])):
            try:
                items = yt.videos().list(part='status,snippet', id=vid).execute().get('items', [])
            except Exception as e:
                print('lookup failed; keep pending:', vid, type(e).__name__)
                pending.append(vid)
                if 'quota' in str(e).lower():
                    quota_exceeded = True
                    break
                continue
            if not items:
                # list() の空結果は「削除済み」と「権限なし」を区別できない。
                print('missing or inaccessible; keep pending:', vid)
                pending.append(vid)
                continue
            if items[0]['status']['privacyStatus'] != 'private':
                print('skip (not private); keep pending:', vid)
                pending.append(vid)
                continue
            try:
                yt.videos().delete(id=vid).execute()
            except Exception as e:
                print('delete failed; keep pending:', vid, type(e).__name__)
                pending.append(vid)
                if 'quota' in str(e).lower():
                    quota_exceeded = True
                    break
                continue
            print('deleted', vid, items[0]['snippet']['title'][:24])
            rec['superseded'].remove(vid)
            rec.setdefault('deleted', []).append(vid)
        if quota_exceeded:
            break

    # 成功した削除だけを、共通の原子的保存ヘルパーで記録する。
    save_ids_atomic(ids)
    if pending:
        sys.exit(f'削除未完了 {len(pending)} 件（台帳に保留）: {", ".join(pending)}')



def cmd_schedule(video_id, when):
    """公開予約（日本時間 'YYYY-MM-DD HH:MM'）。動画は private のまま、公開日時だけ設定する。ユーザーの許可を得てから使う。"""
    import datetime
    jst = datetime.datetime.strptime(when, '%Y-%m-%d %H:%M')
    utc = jst - datetime.timedelta(hours=9)
    yt = service()
    if not any(it.get('id') == CHANNEL_ID for it in mine(yt)):
        sys.exit('認証中のチャンネルが寄り道ラボではありません。中止')
    cur = yt.videos().list(part='status', id=video_id).execute()['items'][0]['status']
    body = dict(id=video_id, status=dict(privacyStatus='private', publishAt=utc.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                                         selfDeclaredMadeForKids=cur.get('selfDeclaredMadeForKids', False), embeddable=cur.get('embeddable', True),
                                         license=cur.get('license', 'youtube'), containsSyntheticMedia=cur.get('containsSyntheticMedia', False)))
    r = yt.videos().update(part='status', body=body).execute()
    print(video_id, r['status']['privacyStatus'], '公開予約(日本時間):', when, '->', r['status'].get('publishAt'))


def cmd_list():
    yt = service()
    up = yt.channels().list(part='contentDetails', mine=True).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    ids = [i['contentDetails']['videoId'] for i in yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50).execute()['items']]
    for v in yt.videos().list(part='snippet,status', id=','.join(ids)).execute()['items']:
        print(v['id'], v['status']['privacyStatus'], v['snippet']['title'])


def cmd_stats():
    """全動画の公開予約日時(日本時間)・再生数・高評価・長さを、公開日順に表示する。"""
    import datetime
    yt = service()
    up = yt.channels().list(part='contentDetails', mine=True).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    ids, tok = [], None
    while True:
        r = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50, pageToken=tok).execute()
        ids += [i['contentDetails']['videoId'] for i in r['items']]; tok = r.get('nextPageToken')
        if not tok: break
    rows = []
    for k in range(0, len(ids), 50):
        for v in yt.videos().list(part='snippet,status,statistics,contentDetails', id=','.join(ids[k:k + 50])).execute()['items']:
            t = v['status'].get('publishAt') or v['snippet']['publishedAt']
            jst = datetime.datetime.strptime(t[:16], '%Y-%m-%dT%H:%M') + datetime.timedelta(hours=9)
            st = v.get('statistics', {})
            rows.append((jst.strftime('%Y-%m-%d %H:%M'), v['status']['privacyStatus'], st.get('viewCount', '-'), st.get('likeCount', '-'), v['contentDetails']['duration'], v['id'], v['snippet']['title']))
    for r in sorted(rows): print(*r, sep=' | ')


def cmd_redesc(pack):
    """台帳の video_id の概要欄だけを、upload/<pack>/description.txt に更新する（タイトル・予約は変えない）。"""
    yt = service()
    if not any(it.get('id') == CHANNEL_ID for it in mine(yt)):
        sys.exit('認証中のチャンネルが寄り道ラボではありません。中止')
    ids = load_ids(); vid = ids[pack]['video_id']
    v = yt.videos().list(part='snippet', id=vid).execute()['items'][0]
    desc = (R / 'upload' / pack / 'description.txt').read_text(encoding='utf8').strip()
    assert len(desc) <= 5000 and '<' not in desc and '>' not in desc
    v['snippet']['description'] = desc
    yt.videos().update(part='snippet', body=dict(id=vid, snippet=v['snippet'])).execute(); print('description updated', pack, vid)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    {'auth': cmd_auth, 'whoami': cmd_whoami, 'list': cmd_list, 'stats': cmd_stats, 'delete-superseded': cmd_delete_superseded, 'schedule': lambda: cmd_schedule(a[1], a[2]), 'redesc': lambda: cmd_redesc(a[1]), 'finish': lambda: cmd_finish(a[1], a[2], a[3] if len(a) > 3 else None)}.get(a[0], lambda: cmd_upload(a[1], '--dry' in a, '--new-version' in a) if a[0] == 'upload' else sys.exit(__doc__))()
