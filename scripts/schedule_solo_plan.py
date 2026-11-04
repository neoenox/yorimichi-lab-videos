"""Shorts先行の日程：単独Shortを、毎日12:00と17:00に前倒しで予約する（2026-11-04 方針）。
usage:
  python scripts/schedule_solo_plan.py plan    # 日程案を data/solo_schedule_plan.json と docs/SHORTS_FIRST_SCHEDULE_20261104.md に書く（予約は変えない）
  python scripts/schedule_solo_plan.py apply   # 案どおりに予約を付け替える（ユーザーの許可を得てから）。元の日時を data/solo_schedule_undo.json に残す
  python scripts/schedule_solo_plan.py undo    # 元の日時に戻す
季節物（成人の日・雪・忠臣蔵）は、元の日付のまま動かさない。パイロット（戦国4本＋卵）を先頭に置き、残りは江戸系と一般系を交互にする。"""
import datetime
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
IDS = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))
PLAN = R / 'data' / 'solo_schedule_plan.json'
UNDO = R / 'data' / 'solo_schedule_undo.json'
STATS = R / 'out' / 'stats_1104.txt'

PILOT = ['toiteppo_sekigahara', 'sandan_nagashino', 'miso_mikata', 'anegawa_suugyou', 'tamago_jikyu']
SEASONAL = {'seijin1115', 'snow_letter', 'snow_same', 'chushingura_14_15'}
GENERAL = ['shinkansen24', 'freq_why', 'freq_move', 'takarakuji100', 'sleep14h']
START = datetime.date(2026, 11, 5)
SLOTS = ['12:00', '17:00']


def title_of(vid):
    for l in STATS.read_text(encoding='utf8').splitlines():
        p = [x.strip() for x in l.split('|')]
        if len(p) >= 7 and p[5] == vid:
            return p[6]
    return ''


def occupied():
    """今ある予約・公開のうち、これからの日時（日本時間 'YYYY-MM-DD HH:MM'）"""
    out = set()
    for l in STATS.read_text(encoding='utf8').splitlines():
        p = [x.strip() for x in l.split('|')]
        if re.match(r'\d{4}-\d\d-\d\d \d\d:\d\d$', p[0]):
            out.add(p[0])
    return out


def order():
    solo = sorted(k[11:] for k in IDS if k.startswith('short_solo_'))
    movable = [s for s in solo if s not in SEASONAL]
    rest = [s for s in movable if s not in PILOT]
    gen = [s for s in GENERAL if s in rest]
    edo = [s for s in rest if s not in gen]
    mix = []
    while gen or edo:
        if edo:
            mix.append(edo.pop(0))
        if gen:
            mix.append(gen.pop(0))
        if edo:
            mix.append(edo.pop(0))
    return PILOT + mix


def cmd_plan():
    occ = occupied()
    d, slots = START, []
    while len(slots) < 60:
        for t in SLOTS:
            w = f'{d} {t}'
            if w not in occ:
                slots.append(w)
        d += datetime.timedelta(days=1)
    seq = order()
    plan = [dict(slug='short_solo_' + s, video_id=IDS['short_solo_' + s]['video_id'], when=slots[i]) for i, s in enumerate(seq)]
    PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding='utf8')
    md = ['# Shorts先行の日程案（2026-11-04、未適用）', '',
          '単独Shortを毎日12:00と17:00に前倒しで予約する案。既存の19:00（長尺）・20:00（要約Short）はそのまま。季節物（成人の日・雪・忠臣蔵）は元の日付のまま。', '',
          '| 日時 | Short | ID |', '|---|---|---|']
    for p in plan:
        md.append(f"| {p['when']} | {p['slug'][11:]} | {p['video_id']} |")
    (R / 'docs' / 'SHORTS_FIRST_SCHEDULE_20261104.md').write_text('\n'.join(md) + '\n', encoding='utf8')
    print(len(plan), '本。最後は', plan[-1]['when'])


def cmd_apply():
    import yt_api
    plan = json.loads(PLAN.read_text(encoding='utf8'))
    undo = json.loads(UNDO.read_text(encoding='utf8')) if UNDO.exists() else {}
    yt = yt_api.service()
    for p in plan:
        vid = p['video_id']
        if vid not in undo:
            st = yt.videos().list(part='status', id=vid).execute()['items'][0]['status']
            pa = st.get('publishAt')
            old = None
            if pa:
                dt = datetime.datetime.strptime(pa[:19], '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=9)
                old = dt.strftime('%Y-%m-%d %H:%M')
            undo[vid] = old
            UNDO.write_text(json.dumps(undo, ensure_ascii=False, indent=1), encoding='utf8')
        yt_api.cmd_schedule(vid, p['when'])


def cmd_undo():
    import yt_api
    undo = json.loads(UNDO.read_text(encoding='utf8'))
    for vid, old in undo.items():
        if old:
            yt_api.cmd_schedule(vid, old)
        else:
            print(vid, '元は予約なし。手動で確認')


if __name__ == '__main__':
    {'plan': cmd_plan, 'apply': cmd_apply, 'undo': cmd_undo}[sys.argv[1]]()
