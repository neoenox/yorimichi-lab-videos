"""登録の呼びかけ版Short（make_short2.py の cta）へ、公開前のShortを作り直して差し替える。2026-10-26〜
usage:
  python scripts/replace_shorts_cta.py plan            # 差し替え対象（非公開・公開予約が未来のShort）を data/short_cta_queue.json に書く
  python scripts/replace_shorts_cta.py gen             # 対象のShortを作り直して upload/short_<slug>/ を更新（ローカルのみ。API枠を使わない）
  python scripts/replace_shorts_cta.py upload N        # 公開予約の早い順に N 本を --new-version でアップ→同じ日時に予約→旧版の予約を外す（削除はしない）
API枠：1本あたり約2,000ユニット（1日1万）。1日に最大4〜5本。旧版は非公開のまま残る（削除はユーザーの許可を得てから）。
対照群：公開済みのShort（10/18〜25公開の約1,200回ずつ）。"""
import json, subprocess, sys, shutil, re
from pathlib import Path
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
Q = R / 'data' / 'short_cta_queue.json'
DONE = R / 'data' / 'short_cta_done.json'
SKIP = {'komaki'}   # 作成時からCTA版


def plan():
    import yt_api as Y
    yt = Y.service()
    ids = Y.load_ids()
    rows = []
    for key, rec in ids.items():
        if not key.startswith('short_'):
            continue
        slug = key[6:]
        if slug in SKIP or not (R / 'data' / f'short_{slug}.json').exists():
            continue
        v = yt.videos().list(part='status', id=rec['video_id']).execute()['items']
        if not v:
            continue
        st = v[0]['status']
        if st['privacyStatus'] == 'private' and st.get('publishAt'):
            rows.append(dict(slug=slug, pack=key, old=rec['video_id'], publishAt=st['publishAt']))
    rows.sort(key=lambda r: r['publishAt'])
    Q.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf8')
    for r in rows:
        print(r['publishAt'], r['slug'], r['old'])
    print(len(rows), '本')


def gen():
    rows = json.loads(Q.read_text(encoding='utf8'))
    for r in rows:
        slug = r['slug']
        d = R / 'upload' / f'short_{slug}'
        tags = (d / 'tags.txt').read_text(encoding='utf8')
        res = subprocess.run([sys.executable, str(R / 'scripts' / 'make_short2.py'), slug], cwd=R / 'scripts', capture_output=True, text=True, encoding='utf8')
        if res.returncode != 0:
            print('FAIL', slug, res.stderr[-300:]); continue
        spec = json.loads((R / 'data' / f'short_{slug}.json').read_text(encoding='utf8'))
        desc = (R / 'out' / f'short_{slug}_description.md').read_text(encoding='utf8')
        sec = int(re.search(r'約(\d+)秒', desc).group(1))
        shutil.copyfile(R / 'out' / f'short_{slug}.mp4', d / 'video.mp4')
        shutil.copyfile(R / 'out' / f'short_{slug}_subtitles.srt', d / 'subtitles_ja.srt')
        (d / 'description.txt').write_text(desc, encoding='utf8')
        title = f"{spec['title']} 約{sec}秒で確かめる #Shorts"
        assert len(title) <= 100
        (d / 'title.txt').write_text(title + '\n', encoding='utf8')
        (d / 'tags.txt').write_text(tags, encoding='utf8')
        print('gen', slug, sec, 's', flush=True)


def upload(n):
    import yt_api as Y, datetime
    rows = json.loads(Q.read_text(encoding='utf8'))
    done = json.loads(DONE.read_text(encoding='utf8')) if DONE.exists() else {}
    todo = [r for r in rows if r['slug'] not in done][:n]
    yt = Y.service()
    for r in todo:
        try:
            cur_id = Y.load_ids().get(r['pack'], {}).get('video_id')
            if cur_id and cur_id != r['old']:
                # 前回、アップ途中（字幕のクォータ切れなど）で止まった新版がある。二重に上げず、字幕だけ付けて続行する
                from googleapiclient.http import MediaFileUpload
                d = Y.R / 'upload' / r['pack']
                print('resume', r['slug'], cur_id, flush=True)
                try:
                    yt.captions().insert(part='snippet', body=dict(snippet=dict(videoId=cur_id, language='ja', name='', isDraft=False)),
                                         media_body=MediaFileUpload(str(d / 'subtitles_ja.srt'), mimetype='application/octet-stream')).execute()
                except Exception as ce:
                    if 'quota' in str(ce).lower(): raise
                    print('  captions skip', str(ce)[:100])
            else:
                Y.cmd_upload(r['pack'], new_version=True)
        except Exception as e:
            print('STOP', r['slug'], str(e)[:200]); break
        new = Y.load_ids()[r['pack']]['video_id']
        t = datetime.datetime.strptime(r['publishAt'], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=9)
        Y.cmd_schedule(new, t.strftime('%Y-%m-%d %H:%M'))
        cur = yt.videos().list(part='status', id=r['old']).execute()['items'][0]['status']
        yt.videos().update(part='status', body=dict(id=r['old'], status=dict(privacyStatus='private', publishAt=None, selfDeclaredMadeForKids=cur.get('selfDeclaredMadeForKids', False),
                           embeddable=cur.get('embeddable', True), license=cur.get('license', 'youtube')))).execute()
        done[r['slug']] = dict(new=new, old=r['old'], publishAt=r['publishAt'])
        DONE.write_text(json.dumps(done, ensure_ascii=False, indent=1), encoding='utf8')
        print('replaced', r['slug'], r['old'], '->', new, flush=True)


if __name__ == '__main__':
    c = sys.argv[1]
    {'plan': plan, 'gen': gen}.get(c, lambda: upload(int(sys.argv[2])))()
