"""チャンネルの一括整備（予約中・公開済みの動画の説明・再生リスト）。usage:
  python scripts/yt_bulk.py pairs            # Short と本編の組み合わせを表示（読むだけ）
  python scripts/yt_bulk.py link [--apply]   # Short の概要欄の1行目に、本編リンクを入れる（既にあれば何もしない）
  python scripts/yt_bulk.py playlists [--apply]   # 3シリーズの再生リストを作り、本編を入れる
APIの割り当て（1日10,000）に注意：videos.update=50、playlists.insert=50、playlistItems.insert=50。割り当て切れで止まったら翌日に続きから。"""
import sys, json, re, datetime
sys.argv_saved = sys.argv[:]; sys.argv = ['x']
sys.path.insert(0, 'scripts')
import yt_api as Y
sys.argv = sys.argv_saved
from pathlib import Path
R = Path(__file__).resolve().parents[1]
yt = Y.service()


def all_videos():
    up = yt.channels().list(part='contentDetails', mine=True).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    ids, tok = [], None
    while True:
        r = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50, pageToken=tok).execute()
        ids += [i['contentDetails']['videoId'] for i in r['items']]; tok = r.get('nextPageToken')
        if not tok: break
    rows = []
    for i in range(0, len(ids), 50):
        for v in yt.videos().list(part='status,snippet,contentDetails', id=','.join(ids[i:i + 50])).execute()['items']:
            pa = v['status'].get('publishAt')
            jst = (datetime.datetime.strptime(pa[:19], '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=9)) if pa else None
            m = re.match(r'PT(?:(\d+)M)?(?:(\d+)S)?', v['contentDetails']['duration'])
            rows.append(dict(id=v['id'], title=v['snippet']['title'], desc=v['snippet'].get('description', ''), cat=v['snippet'].get('categoryId', '27'),
                             tags=v['snippet'].get('tags', []), lang=v['snippet'].get('defaultLanguage'), privacy=v['status']['privacyStatus'], at=jst,
                             pub=v['snippet'].get('publishedAt', ''), secs=int(m.group(1) or 0) * 60 + int(m.group(2) or 0)))
    return rows


def key(r):
    return r['at'] or datetime.datetime.strptime(r['pub'][:19], '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=9)


def pairs(rows):
    longs = [r for r in rows if r['secs'] > 75 and '#Shorts' not in r['title']]
    shorts = [r for r in rows if '#Shorts' in r['title'] or r['secs'] <= 75]
    out = []
    for s in shorts:
        k = key(s)
        cand = [l for l in longs if key(l).date() == k.date()]
        if len(cand) == 1: out.append((s, cand[0]))
        elif len(cand) > 1:
            def sim(l): return len(set(re.findall(r'[一-龥ァ-ヶ]{2,}', s['title'])) & set(re.findall(r'[一-龥ァ-ヶ]{2,}', l['title'])))
            cand.sort(key=sim, reverse=True)
            if sim(cand[0]) > sim(cand[1]): out.append((s, cand[0]))
    seen=set(); res=[]
    for s_,l_ in out:
        if s_['id'] in seen: continue
        seen.add(s_['id']); res.append((s_,l_))
    return res


SERIES = [
    ('戦国の戦いを、地図と史料で確かめる', '「◯◯の戦い」を、地図と一次史料（『信長公記』など）で検証するシリーズ。通説と異論を並べて確かめます。', r'戦い|の変|の乱|桶狭間|関ヶ原|長篠'),
    ('江戸の暮らしを、資料で確かめる', '「江戸の人は〇〇だった？」を、資料と数字で確かめるシリーズ。', r'江戸|参勤|寺子屋|火消|長屋|一両|一刻|銭湯|飛脚|大工|木戸|宵越し|初鰹|花火|大岡|貸本|伊勢参り|丑の日|生類|宝くじ|おやつ|寿司|抜け参り|識字|旅人|医者|人口|リサイクル|二食|2食|成人'),
    ('科学と言葉の「誤解」を確かめる', '科学・言葉・暮らしの「本当？」を、公的な資料や論文で確かめるシリーズ。', r'.'),
]


def cmd_playlists(rows, apply):
    live = [r for r in rows if r['secs'] > 75 and '#Shorts' not in r['title'] and (r['privacy'] == 'public' or r['at'])]
    live.sort(key=key)
    existing = {p['snippet']['title']: p['id'] for p in yt.playlists().list(part='snippet', mine=True, maxResults=50).execute()['items']}
    used = set()
    for title, desc, pat in SERIES:
        mem = [r for r in live if r['id'] not in used and re.search(pat, r['title'])]
        used |= {r['id'] for r in mem}
        print(title, len(mem), '本')
        if not apply: continue
        try:
            pid = existing.get(title) or yt.playlists().insert(part='snippet,status', body=dict(snippet=dict(title=title, description=desc), status=dict(privacyStatus='public'))).execute()['id']
            if title not in existing:
                import time; time.sleep(8)
            have = set()
            tok = None
            while True:
                r = yt.playlistItems().list(part='contentDetails', playlistId=pid, maxResults=50, pageToken=tok).execute()
                have |= {i['contentDetails']['videoId'] for i in r['items']}; tok = r.get('nextPageToken')
                if not tok: break
            n = 0
            for r_ in mem:
                if r_['id'] in have: continue
                yt.playlistItems().insert(part='snippet', body=dict(snippet=dict(playlistId=pid, resourceId=dict(kind='youtube#video', videoId=r_['id'])))).execute(); n += 1
            print('  追加', n, 'playlist', pid)
        except Exception as e:
            print('停止:', str(e)[:200]); return


if __name__ == '__main__':
    cmd = sys.argv[1]; apply = '--apply' in sys.argv
    rows = all_videos()
    if cmd == 'pairs':
        P = pairs(rows)
        print(len(P), '組 / Short', sum(1 for r in rows if '#Shorts' in r['title']), '本')
        for s, l in P[:80]: print(key(s).strftime('%m/%d %H:%M'), s['id'], '->', l['id'], l['title'][:28])
    elif cmd == 'titles':
        new = json.loads((R / 'data' / 'title_new_20261103.json').read_text(encoding='utf8'))
        byid = {r['id']: r for r in rows}; n = 0
        for vid, t in new.items():
            r = byid.get(vid)
            if not r or r['title'] == t: continue
            print(vid, r['title'][:28], '=>', t[:28])
            if apply:
                body = dict(id=vid, snippet=dict(title=t, description=r['desc'], categoryId=r['cat'], tags=r['tags'], **({'defaultLanguage': r['lang']} if r['lang'] else {})))
                try:
                    yt.videos().update(part='snippet', body=body).execute(); n += 1
                except Exception as e:
                    print('停止:', str(e)[:160]); break
        print('更新', n)
    elif cmd == 'playlists':
        cmd_playlists(rows, apply)
    elif cmd == 'link':
        n = 0
        for s, l in pairs(rows):
            url = f"https://youtu.be/{l['id']}"
            if url in s['desc']: continue
            if s['privacy'] == 'public' and False: continue
            new = f"▶ 本編（くわしい検証）：{url}\n\n" + s['desc']
            print(s['id'], '本編', l['id'], s['title'][:30])
            if apply:
                body = dict(id=s['id'], snippet=dict(title=s['title'], description=new, categoryId=s['cat'], tags=s['tags'], **({'defaultLanguage': s['lang']} if s['lang'] else {})))
                try:
                    yt.videos().update(part='snippet', body=body).execute(); n += 1
                except Exception as e:
                    print('停止:', str(e)[:160]); break
        print('更新', n)

