"""アップ済み動画のローカルコピーを整理する(既定はdry-run。--apply で削除)。
  python scripts/cleanup_uploaded.py            # 一覧と容量だけ
  python scripts/cleanup_uploaded.py --apply    # 削除して、記録を sigcmp_view/cleanup_<日付>.txt に書く
判定: data/youtube_ids.json の video_id を YouTube API で確認し、**実在する動画だけ**を対象にする(YouTubeに無い=唯一のコピーかもしれないので残す)。
対象: upload/<キー>/*.mp4、cache/<キー>/、out/<キー>.mp4 と muse_<キー>.mp4、sigcmp_view/<キー>.mp4 と muse_<キー>.mp4。
残すもの: 台本・data・字幕・説明欄・タグ・背景クリップ(assets)・tools・台帳に無い(未アップ)キー・YouTubeに無いキー。
名前は完全一致だけで拾う(前方一致だと、別の版 short_solo_tokyodome_map などを巻き込むため)。
"""
import sys, os, json, glob, shutil, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yt_api

H = 'E:/rekishikaisetu-honnoji'
M = H   # sigcmp_view もこのプロジェクト(honnoji)の中
apply = '--apply' in sys.argv

L = json.load(open(H + '/data/youtube_ids.json', encoding='utf8'))
ids = {k: v.get('video_id') for k, v in L.items() if v.get('video_id')}
s = yt_api.service()
exist = set()
vals = list(set(ids.values()))
for i in range(0, len(vals), 50):
    for it in s.videos().list(part='id', id=','.join(vals[i:i + 50])).execute()['items']:
        exist.add(it['id'])
A = {k for k, v in ids.items() if v in exist}


def sz(p):
    try:
        return os.path.getsize(p)
    except Exception:
        return 0


def dsz(p):
    return sum(sz(os.path.join(r, f)) for r, _, fs in os.walk(p) for f in fs)


def keyof(fname):
    b = fname[:-4]
    base = b[len('muse_'):] if b.startswith('muse_') else b
    return base if base in A else None


plan = []
for k in A:
    for f in glob.glob(H + '/upload/' + k + '/*.mp4'):
        plan.append(('upload', f.replace(chr(92), '/'), sz(f)))
    p = H + '/cache/' + k
    if os.path.isdir(p):
        plan.append(('cache', p, dsz(p)))
for d, tag in ((H + '/out', 'out'), (M + '/sigcmp_view', 'sigcmp_view')):
    for f in os.listdir(d):
        if f.endswith('.mp4') and keyof(f):
            plan.append((tag, d + '/' + f, sz(d + '/' + f)))

tot = collections.Counter()
cnt = collections.Counter()
for t, p, n in plan:
    tot[t] += n
    cnt[t] += 1
for t in tot:
    print(t, cnt[t], '件', round(tot[t] / 1e9, 2), 'GB')
print('合計', len(plan), '件', round(sum(tot.values()) / 1e9, 2), 'GB', '(削除します)' if apply else '(dry-run。--apply で削除)')

if apply:
    log = []
    for t, p, n in plan:
        try:
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
            log.append(f'{t}\t{p}\t{n}')
        except Exception as e:
            print('失敗', p, e)
    out = M + '/sigcmp_view/cleanup_' + datetime.date.today().strftime('%Y%m%d') + '.txt'
    open(out, 'w', encoding='utf8').write('削除したファイル(YouTubeに実在する動画のローカルコピーのみ)\n' + '\n'.join(log))
    print('記録', out)
