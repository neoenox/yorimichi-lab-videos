"""YouTube API のクォータが回復したあとに、溜まっている作業を1日分ずつ片付ける。

usage:
  python scripts/daily_quota_run.py --list            # 残りの作業と見積もりを表示
  python scripts/daily_quota_run.py                   # 予算内で実行（既定 9,400ユニット）
  python scripts/daily_quota_run.py --budget 9500
  python scripts/daily_quota_run.py --wait 600        # クォータ回復まで最大600分待ってから実行

1日の上限は10,000ユニット。予算を超える作業は翌日に回す（何度実行しても安全）。
実行内容と結果は out/codex/quota_run.log にも残る。
"""
import datetime as dt
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import replace_versions
import yt_api
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

R = yt_api.R
STATE = R / 'data' / 'quota_run_state.json'
LOG = R / 'out' / 'codex' / 'quota_run.log'
SHORT_AT = '2026-11-03 20:00'

# 差し替えは公開日が早い順（公開日が迫っているものを先に消化する）。
# koku(10/21 19:00) は実行時刻 16:05 だと公開まで3時間を切るため見送り。
REPLACE_ORDER = ['compass', 'gdp', 'scurvy', 'calendar', 'einstein', 'moon', 'islands', 'magnitude',
                 'yakubusoku', 'oke', 'leapsecond', 'sunrise', 'venus']

# 数字を直した Short（公開前のものだけ差し替え。koku は公開が近い、drain は公開済み）
SHORT_REPLACE = ['scurvy', 'calendar', 'moon', 'islands', 'magnitude', 'leapsecond', 'venus']
# 長尺だけ先に出て Short が無かった3本。公開は長尺の最終回のあと（20:00）
NEW_SHORTS = {'worldmap': '2026-11-11 20:00', 'honnoji': '2026-11-12 20:00', 'ninja': '2026-11-13 20:00'}
# 01/02/03 の長尺は公開予約が入っていない（private のまま）。Short と同じ日の 19:00 に入れる。
NEW_LONG_SCHEDULE = {'01_world_map_distortion': '2026-11-11 19:00',
                     '02_honnoji_incident': '2026-11-12 19:00',
                     '03_ninja_myths': '2026-11-13 19:00'}
# 旧系統（*_compose.py）で作り直した3本。予約を入れたあとに差し替える
OLD_PIPELINE = ['gm', 'hn', 'nj']


def log(msg):
    line = f'[{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {msg}'
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open('a', encoding='utf8') as f:
        f.write(line + '\n')


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding='utf8'))
    return {'done': {}, 'notes': {}, 'spent': 0}


def save_state(s):
    STATE.write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding='utf8')


def probe(yt):
    """1ユニットの呼び出しでクォータを確認。使えれば True。"""
    ids = yt_api.load_ids()
    vid = next(iter(ids.values()))['video_id']
    try:
        yt.videos().list(part='id', id=vid).execute()
        return True
    except HttpError as e:
        if 'quota' in str(e).lower():
            return False
        raise
    except Exception as e:  # ネットワーク断（TimeoutError など）も「待つ」対象にする
        log(f'疎通確認に失敗（{type(e).__name__}）。待機して再試行します')
        return False


def attach_caption(yt, pack, vid):
    ja = [c for c in yt.captions().list(part='snippet', videoId=vid).execute().get('items', [])
          if c['snippet'].get('language') == 'ja']
    if ja:
        return 'already'
    yt.captions().insert(
        part='snippet',
        body=dict(snippet=dict(videoId=vid, language='ja', name='', isDraft=False)),
        media_body=MediaFileUpload(str(R / 'upload' / pack / 'subtitles_ja.srt'),
                                   mimetype='application/octet-stream')).execute()
    return 'inserted'


# ---- 個別タスク -------------------------------------------------------------

def task_short_oke_upload(yt):
    if 'short_oke' in yt_api.load_ids():
        return 'already'
    yt_api.cmd_upload('short_oke')
    return 'uploaded'


def task_short_oke_schedule(yt):
    vid = yt_api.load_ids()['short_oke']['video_id']
    st = yt.videos().list(part='status', id=vid).execute()['items'][0]['status']
    if st.get('publishAt'):
        return f'already {st["publishAt"]}'
    yt_api.cmd_schedule(vid, SHORT_AT)
    return SHORT_AT


def task_oke_captions(yt):
    vid = yt_api.load_ids()['14_okehazama']['video_id']
    return attach_caption(yt, '14_okehazama', vid)


def task_calendar_short_redesc(yt):
    yt_api.cmd_redesc('short_calendar')
    return 'updated'


def task_short_redesc(pack):
    """概要欄だけ更新する（公開予約・タイトルは触らない）。"""
    def run(yt):
        yt_api.cmd_redesc(pack)
        return 'updated'
    return run


def task_short_oceanblue_schedule(yt):
    """oceanblue の Short は予約が未設定のまま。長尺と同じ 11/10 20:00 に入れる。"""
    vid = yt_api.load_ids()['short_oceanblue']['video_id']
    st = yt.videos().list(part='status', id=vid).execute()['items'][0]['status']
    if st.get('publishAt'):
        return f'already {st["publishAt"]}'
    yt_api.cmd_schedule(vid, '2026-11-10 20:00')
    return '2026-11-10 20:00'


def task_new_short(slug):
    """長尺だけ先に出た回の Short を、上げて公開予約まで（何度でも安全）。"""
    def run(yt):
        pack = f'short_{slug}'
        res = []
        if pack not in yt_api.load_ids():
            yt_api.cmd_upload(pack)
            res.append('uploaded')
        else:
            res.append('already')
        vid = yt_api.load_ids()[pack]['video_id']
        st = yt.videos().list(part='status', id=vid).execute()['items'][0]['status']
        if st.get('publishAt'):
            res.append(f'scheduled {st["publishAt"]}')
        else:
            yt_api.cmd_schedule(vid, NEW_SHORTS[slug])
            res.append(NEW_SHORTS[slug])
        return ' / '.join(res)
    return run


def task_schedule_long(pack, when):
    """公開予約が入っていない長尺に、公開日時を入れる（入っていれば何もしない）。"""
    def run(yt):
        vid = yt_api.load_ids()[pack]['video_id']
        st = yt.videos().list(part='status', id=vid).execute()['items'][0]['status']
        if st.get('publishAt'):
            return f'already {st["publishAt"]}'
        if st['privacyStatus'] == 'public':
            return 'public（予約できない）'
        yt_api.cmd_schedule(vid, when)
        return when
    return run


TASKS = [
    # 04_edo_ichikoku は 10/21 19:00 公開。映像は差し替えられないが、概要欄の漢数字は公開前に直せる
    ('redesc:koku', 51, lambda yt: yt_api.cmd_redesc('04_edo_ichikoku')),
    ('short_oke_upload', 2001, task_short_oke_upload),
    ('short_oke_schedule', 51, task_short_oke_schedule),
    ('oke_captions', 451, task_oke_captions),
    ('calendar_short_redesc', 51, task_calendar_short_redesc),
    ('short_venus_redesc', 51, task_short_redesc('short_venus')),
    ('short_oceanblue_redesc', 51, task_short_redesc('short_oceanblue')),
    ('short_oceanblue_schedule', 51, task_short_oceanblue_schedule),
] + [(f'replace:{s}', replace_versions.COST, (lambda yt, s=s: replace_versions.replace(s, log)))
     for s in REPLACE_ORDER] \
  + [(f'replace_short:{s}', replace_versions.COST_SHORT,
      (lambda yt, s=s: replace_versions.replace_short(s, log))) for s in SHORT_REPLACE] \
  + [(f'schedule_long:{p}', 51, task_schedule_long(p, w)) for p, w in NEW_LONG_SCHEDULE.items()] \
  + [(f'replace:{s}', replace_versions.COST, (lambda yt, s=s: replace_versions.replace(s, log)))
     for s in OLD_PIPELINE] \
  + [(f'short_upload:{s}', 2051, task_new_short(s)) for s in NEW_SHORTS]


def main():
    a = sys.argv[1:]
    budget = 9400
    if '--budget' in a:
        budget = int(a[a.index('--budget') + 1])
    wait_min = int(a[a.index('--wait') + 1]) if '--wait' in a else 0
    state = load_state()

    if '--list' in a:
        left = budget
        for tid, cost, _ in TASKS:
            mark = 'done' if tid in state['done'] else f'{cost}'
            print(f'{tid:28s} {mark}')
            left -= 0 if tid in state['done'] else cost
        print(f'合計の見積もり: {sum(c for t, c, _ in TASKS if t not in state["done"])} ユニット')
        return

    yt = yt_api.service()
    waited = 0
    while not probe(yt):
        if waited >= wait_min:
            log('クォータがまだ回復していない。終了（次回また実行してください）')
            sys.exit(2)
        log('クォータ待ち 10分')
        time.sleep(600)
        waited += 10

    spent = 0
    i = 0
    while i < len(TASKS):
        tid, cost, fn = TASKS[i]
        if tid in state['done']:
            i += 1
            continue
        if spent + cost > budget:
            log(f'予算切れ: 次回に回す {tid}（今回 {spent} / {budget}）')
            break
        log(f'start {tid} (~{cost})')
        try:
            res = fn(yt)
            state['done'][tid] = dt.datetime.now().isoformat(timespec='seconds')
            state['notes'][tid] = str(res)
            log(f'ok {tid}: {res}')
        except replace_versions.Skip as e:
            msg = str(e)
            # 「予約がまだ無い」「作り直しがまだ」は一時的なので、翌日また試す（クォータも消費しない）
            if '公開予約が無い' in msg or '作り直した' in msg or '再レンダリング' in msg:
                state['notes'][tid] = f'retry: {msg}'
                log(f'retry {tid}: {msg}')
                i += 1
                continue
            state['done'][tid] = dt.datetime.now().isoformat(timespec='seconds')
            state['notes'][tid] = f'skip: {msg}'
            log(f'skip {tid}: {msg}')
        except HttpError as e:
            if 'quota' in str(e).lower():
                state['notes'][tid] = 'quota_exceeded'
                save_state(state)
                if spent >= budget * 0.9:
                    log(f'クォータ超過 {tid}。本日の割当を使い切ったので終了')
                    sys.exit(2)
                if waited < wait_min:
                    log(f'クォータ超過 {tid}。10分待って再試行')
                    time.sleep(600)
                    waited += 10
                    continue
                log(f'クォータ超過で中断 {tid}（翌日また実行してください）')
                sys.exit(2)
            state['notes'][tid] = f'error: {str(e)[-200:]}'
            log(f'error {tid}: {str(e)[-200:]}')
        except Exception as e:
            state['notes'][tid] = f'error: {type(e).__name__} {str(e)[-160:]}'
            log(f'error {tid}: {type(e).__name__} {str(e)[-160:]}')
        spent += cost
        state['spent'] = state.get('spent', 0) + cost
        save_state(state)
        i += 1

    remaining = [t for t, _, _ in TASKS if t not in state['done']]
    log(f'done. 今回 {spent} / {budget} ユニット。残り {len(remaining)} 件' + (': ' + ', '.join(remaining) if remaining else ''))


if __name__ == '__main__':
    main()
