"""単独Shortを「非公開アップ→処理完了待ち→公開予約(日本時間)→台帳→API再確認」まで進める。公開日時はユーザーの許可を得てから使う。
  python scripts/solo_schedule.py <slug> "2026-11-10 00:00"
slug は solo_mito など(upload/short_<slug>/ と台帳キー short_<slug>)。公開は予約時刻まで private のまま。"""
import importlib.util, json, re, subprocess, sys, time, os
from pathlib import Path
R = Path(__file__).resolve().parents[1]
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
sys.stdout.reconfigure(encoding='utf8')
slug, when = sys.argv[1], sys.argv[2]
key = f'short_{slug}'
sys.argv = ['x']
sp = importlib.util.spec_from_file_location('yt', R / 'scripts' / 'yt_api.py'); yt = importlib.util.module_from_spec(sp); sp.loader.exec_module(yt)
r = subprocess.run([sys.executable, str(R / 'scripts' / 'yt_api.py'), 'upload', key], cwd=R, capture_output=True, text=True, encoding='utf8', errors='replace')
m = re.search(r'video id (\S+)', r.stdout)
if not m:
    print((r.stdout + r.stderr)[-900:]); sys.exit('アップに失敗: ' + slug)
vid = m.group(1)
print('アップ完了(非公開):', vid, '字幕:', 'ok' if 'captions ok' in r.stdout else '要確認')
s = yt.service()
for _ in range(90):
    v = s.videos().list(part='status', id=vid).execute()['items'][0]
    if v['status']['uploadStatus'] == 'processed': break
    time.sleep(20)
yt.cmd_schedule(vid, when)
v = s.videos().list(part='status,snippet', id=vid).execute()['items'][0]
p = R / 'data' / 'youtube_ids.json'; d = json.loads(p.read_text(encoding='utf8'))
e = d.get(key, {}); e['video_id'] = vid; e['privacy'] = v['status']['privacyStatus']; e['publishAt'] = v['status'].get('publishAt'); d[key] = e
p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf8')
print(f"確認: {slug} {vid} privacy={v['status']['privacyStatus']} upload={v['status']['uploadStatus']} publishAt={v['status'].get('publishAt')} title={v['snippet']['title']}")
