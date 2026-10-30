"""Shortの「関連動画」に長尺を設定する作業の対象を出す。長尺とShortの両方が公開済みで、未設定のものだけ。
usage: python scripts/related_todo.py            # 対象を表示
       python scripts/related_todo.py done <ShortのID>   # 設定したら記録"""
import json, sys, glob
from pathlib import Path
R = Path(__file__).resolve().parents[1]
DONE = R / 'data' / 'related_done.json'
done = json.loads(DONE.read_text(encoding='utf8')) if DONE.exists() else []
if len(sys.argv) > 2 and sys.argv[1] == 'done':
    if sys.argv[2] not in done: done.append(sys.argv[2])
    DONE.write_text(json.dumps(done), encoding='utf8'); print('recorded', sys.argv[2]); sys.exit()
import importlib.util
sys.argv = ['x']
spec = importlib.util.spec_from_file_location('yt', R / 'scripts' / 'yt_api.py'); yt = importlib.util.module_from_spec(spec); spec.loader.exec_module(yt)
s = yt.service(); ids = yt.load_ids()
pairs = []
for f in sorted(glob.glob(str(R / 'data' / 'short_*.json'))):
    slug = Path(f).stem[6:]; k = 'short_' + slug
    d = json.loads(Path(f).read_text(encoding='utf8'))
    if k in ids and d.get('long_id'):
        pairs.append((slug, ids[k]['video_id'], d['long_id']))
vids = [x for p in pairs for x in p[1:]]
st = {}
for i in range(0, len(vids), 50):
    for v in s.videos().list(part='status,snippet', id=','.join(vids[i:i + 50])).execute()['items']:
        st[v['id']] = (v['status']['privacyStatus'], v['snippet']['title'])
for slug, sh, lg in pairs:
    if sh in done: continue
    if st.get(sh, ('',))[0] == 'public' and st.get(lg, ('',))[0] == 'public':
        print(f'TODO {slug}\tshort={sh}\tlong={lg}\t{st[lg][1]}')
