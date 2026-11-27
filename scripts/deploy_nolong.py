"""「本編に触れない版」を、日程の早い順に、アップ→字幕→新版を元の枠に予約→旧版の予約を外す（再開できる）。
usage: python scripts/deploy_nolong.py [最大本数]       例: deploy_nolong.py 5
進み具合：data/nolong_progress.json。APIの割り当て切れ(quotaExceeded)で止まったら、翌日に同じコマンドで続きから。
旧版は、非公開・予約なしで残す（削除はユーザー許可を得てから）。"""
import json
import re
import subprocess
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
PROG = R / 'data' / 'nolong_progress.json'
ENV = {**__import__('os').environ, 'PYTHONIOENCODING': 'utf8'}
EXTRA = {'solo_komugi_jikyu': '2026-11-24 12:00'}   # APIで予約した、予約計画の外のShort


def ids():
    return json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))


def prog_load():
    return json.loads(PROG.read_text(encoding='utf8')) if PROG.exists() else {}


def prog_save(p):
    PROG.write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding='utf8')


def run(args):
    r = subprocess.run([sys.executable] + args, cwd=str(R), env=ENV, capture_output=True, text=True, encoding='utf8')
    return r.returncode, (r.stdout or '') + (r.stderr or '')


def long_pack(long_id):
    for k, v in ids().items():
        if not k.startswith('short') and v.get('video_id') == long_id:
            return k
    raise SystemExit(f'長尺 {long_id} の台帳が見つからない')


def main():
    import yt_api
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    targets = json.loads((R / 'data' / 'nolong_targets.json').read_text(encoding='utf8'))
    plan = {}
    for r in json.loads((R / 'data' / 'solo_schedule_plan.json').read_text(encoding='utf8')):
        plan['short_' + r['slug'][6:]] = r
    p = prog_load()
    yt = None
    n_up = 0
    for slug, when, long_date in targets:   # slug = 'solo_xxx'
        st = p.setdefault(slug, {})
        if st.get('done'):
            continue
        key_nl = f'short_{slug}_nl'
        old = ids().get(f'short_{slug}')
        if not old:
            print(slug, '旧版の台帳なし。飛ばす'); continue
        # 1. アップ
        if not st.get('new_id'):
            if n_up >= limit:
                print(f'上限 {limit} 本。ここまで'); break
            sp = json.loads((R / 'data' / f'short_{slug}.json').read_text(encoding='utf8'))
            rc, out = run(['scripts/pack_short.py', f'{slug}_nl', long_pack(sp['long_id'])])
            if rc:
                print(slug, 'pack失敗', out[-200:]); break
            rc, out = run(['scripts/yt_api.py', 'upload', key_nl])
            m = re.search(r'video id (\S+)', out)
            if not m:
                print(slug, 'アップ失敗（割り当て切れの可能性）', out[-250:].replace('\n', ' ')); break
            st['new_id'] = m.group(1)
            st['captions'] = 'captions ok' in out
            n_up += 1
            prog_save(p)
            print(slug, 'アップ', st['new_id'], '字幕', st['captions'])
        yt = yt or yt_api.service()
        # 2. 字幕（アップ時に失敗していれば）
        if not st.get('captions'):
            try:
                from googleapiclient.http import MediaFileUpload
                yt.captions().insert(part='snippet', body=dict(snippet=dict(videoId=st['new_id'], language='ja', name='', isDraft=False)),
                                     media_body=MediaFileUpload(str(R / 'upload' / key_nl / 'subtitles_ja.srt'), mimetype='application/octet-stream')).execute()
                st['captions'] = True; prog_save(p)
            except Exception as e:
                print(slug, '字幕失敗', str(e)[:120]); break
        # 3. 新版を元の枠に予約
        if not st.get('scheduled'):
            when_new = plan.get(f'short_{slug}', {}).get('when') or EXTRA.get(slug)
            if not when_new:   # 予約していなかったShortは、予約しない（日程は、あとで決める）
                st['scheduled'] = 'none'; prog_save(p)
                print(slug, '元の予約なし。新版も予約しない')
                when_new = None
            try:
                if when_new is None:
                    raise StopIteration
                yt_api.cmd_schedule(st['new_id'], when_new)
                st['scheduled'] = when_new; prog_save(p)
            except StopIteration:
                pass
            except Exception as e:
                print(slug, '予約失敗', str(e)[:120]); break
        # 4. 旧版の予約を外す（非公開・予約なしにする）
        if not st.get('old_cleared') and st.get('scheduled') != 'none':
            try:
                cur = yt.videos().list(part='status', id=old['video_id']).execute()['items'][0]['status']
                body = dict(id=old['video_id'], status=dict(privacyStatus='private', selfDeclaredMadeForKids=cur.get('selfDeclaredMadeForKids', False),
                                                            embeddable=cur.get('embeddable', True), license=cur.get('license', 'youtube'),
                                                            containsSyntheticMedia=cur.get('containsSyntheticMedia', False)))
                r = yt.videos().update(part='status', body=body).execute()
                st['old_cleared'] = True
                st['old_publishAt_after'] = r['status'].get('publishAt')
                st['old_id'] = old['video_id']
                prog_save(p)
                print(slug, '旧版', old['video_id'], 'の予約を外した。残りの予約:', r['status'].get('publishAt'))
            except Exception as e:
                print(slug, '旧版の予約解除に失敗', str(e)[:120]); break
        st['done'] = True
        prog_save(p)
    done = sum(1 for v in p.values() if v.get('done'))
    print(f'完了 {done}/{len(targets)}')


if __name__ == '__main__':
    main()
