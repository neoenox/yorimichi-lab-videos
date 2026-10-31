"""Shortの「関連動画」に長尺を設定する作業の対象を出す。長尺が公開済みで、まだ設定していないもの。
長尺が先・Shortが後（同日夜）なので、Shortが公開される前に設定を終える必要がある。24時間以内に公開される
Shortは NOW として先に出す（配られている48時間のあいだ入口が空くのを防ぐ）。
usage: python scripts/related_todo.py            # 対象を表示（TODO=公開済み、NOW=24時間以内に公開されるShort）
       python scripts/related_todo.py done <ShortのID>   # 設定したら記録"""
import datetime as dt
import json, sys, glob
from pathlib import Path
R = Path(__file__).resolve().parents[1]
JST = dt.timezone(dt.timedelta(hours=9))
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
        st[v['id']] = (v['status']['privacyStatus'], v['snippet']['title'], v['status'].get('publishAt'))
now = dt.datetime.now(dt.timezone.utc)
soon = now + dt.timedelta(hours=24)
for slug, sh, lg in pairs:
    if sh in done:
        continue
    sh_privacy, _, sh_at = st.get(sh, ('', '', None))
    lg_privacy, lg_title, _ = st.get(lg, ('', '', None))
    if lg_privacy != 'public':
        continue          # 長尺がまだ公開前。関連動画に設定できない
    if sh_privacy == 'public':
        print(f'TODO  {slug}\tshort={sh}\tlong={lg}\t{lg_title}')
    elif sh_at:
        at = dt.datetime.strptime(sh_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc)
        if at <= soon:
            # Short の公開前。ここで設定しないと、配られている48時間に入口が無い
            print(f'NOW   {slug}\tshort={sh}\t公開 {at.astimezone(JST):%m-%d %H:%M} JST\tlong={lg}\t{lg_title}')
