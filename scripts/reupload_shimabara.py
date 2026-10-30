"""島原・天草の乱：『島原記』の原文確認を反映した新版を、長尺・Shortともに上げ直す（クォータが戻ってから実行）。
旧版（aNSzUYvFJ_0 / g-ZzFv_3u1U）は非公開のまま予約だけ外す（削除はしない）。途中で止まっても、再実行で続きから進む（状態は data/reupload_shimabara.json）。
実行： cd E:\\rekishikaisetu-honnoji\\scripts && PYTHONUTF8=1 python reupload_shimabara.py"""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import yt_api as Y

R = Path(__file__).resolve().parents[1]
ST = R / 'data' / 'reupload_shimabara.json'
st = json.loads(ST.read_text(encoding='utf8')) if ST.exists() else {}
OLD_LONG, OLD_SHORT = 'aNSzUYvFJ_0', 'g-ZzFv_3u1U'


def save(): ST.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding='utf8')


def run(*a):
    r = subprocess.run([sys.executable, *a], cwd=str(R / 'scripts'), env={**__import__('os').environ, 'PYTHONUTF8': '1'}, capture_output=True, text=True, encoding='utf8')
    print(r.stdout[-400:], r.stderr[-300:] if r.returncode else '')
    if r.returncode: raise SystemExit('failed: ' + ' '.join(a))


def clear_schedule(vid):
    yt = Y.service()
    cur = yt.videos().list(part='status', id=vid).execute()['items'][0]['status']
    yt.videos().update(part='status', body=dict(id=vid, status=dict(privacyStatus='private', selfDeclaredMadeForKids=cur.get('selfDeclaredMadeForKids', False),
                       embeddable=cur.get('embeddable', True), license=cur.get('license', 'youtube'), containsSyntheticMedia=cur.get('containsSyntheticMedia', False)))).execute()


if 'long' not in st:
    ids = Y.load_ids()
    if ids.get('37_shimabara', {}).get('video_id') != OLD_LONG:
        st['long'] = ids['37_shimabara']['video_id']   # 前回、途中で止まった新版を使う
    else:
        Y.cmd_upload('37_shimabara', new_version=True)
        st['long'] = Y.load_ids()['37_shimabara']['video_id']
    save()
print('long', st['long'])
if not st.get('long_scheduled'):
    Y.cmd_schedule(st['long'], '2026-11-18 19:00'); clear_schedule(OLD_LONG); st['long_scheduled'] = True; save()
if not st.get('short_prepared'):
    p = R / 'data' / 'short_shimabara.json'; d = json.loads(p.read_text(encoding='utf8')); d['long_id'] = st['long']; p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf8')
    run('fix_short_links.py', 'shimabara'); run('pack_short.py', 'shimabara', '37_shimabara'); st['short_prepared'] = True; save()
if 'short' not in st:
    ids = Y.load_ids()
    if ids.get('short_shimabara', {}).get('video_id') not in (None, OLD_SHORT) and ids['short_shimabara']['video_id'] != OLD_SHORT:
        st['short'] = ids['short_shimabara']['video_id']
    else:
        Y.cmd_upload('short_shimabara', new_version=True) if 'short_shimabara' in ids else Y.cmd_upload('short_shimabara')
        st['short'] = Y.load_ids()['short_shimabara']['video_id']
    save()
print('short', st['short'])
if not st.get('short_scheduled'):
    Y.cmd_schedule(st['short'], '2026-11-18 20:00'); clear_schedule(OLD_SHORT); st['short_scheduled'] = True; save()
print('ALL DONE', st)
