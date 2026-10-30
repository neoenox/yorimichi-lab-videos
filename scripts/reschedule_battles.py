"""戦況解説（長篠・関ヶ原・山崎・賤ヶ岳・小牧）を、一般題材の早い枠と入れ替える。2026-10-26（ユーザー承認）。
usage: python scripts/reschedule_battles.py plan|apply|titles
 plan   : 現在の公開予約を読み、入れ替え後の目標日時を data/reschedule_plan.json に書く（API読み取りのみ）
 apply  : 目標日時が違う動画だけ publishAt を更新（1本50ユニット）。クォータ切れで止まったら、次の日に再実行（済みは飛ばす）
 titles : 戦況解説5本のタイトルを更新（1本50ユニット）
入れ替え：(一般題材の長尺+Short) の日時 ↔ (戦況解説の長尺+Short) の日時。Shortの無い長篠は、一般題材の組を長篠の日へ移す。"""
import json, sys, datetime
from pathlib import Path
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import yt_api as Y
PL = R / 'data' / 'reschedule_plan.json'
# (一般の長尺pack, 一般のshort pack, 戦況の長尺 id/pack, 戦況のshort id/pack)
PAIRS = [('08_zenzen_affirm', 'short_zenzen', '27_sekigahara', 'short_sekigahara'),
         ('15_moon_rotation', 'short_moon', '26_nagashino', None),
         ('17_magnitude_energy', 'short_magnitude', 'ID:jY8SSEQrBoA', 'ID:sPt2J6EYMtA'),
         ('19_leap_second', 'short_leapsecond', '28_yamazaki', 'short_yamazaki'),
         ('20_sunrise_solstice', 'short_sunrise', '29_shizugatake', 'short_shizugatake')]
TITLES = {
 '26_nagashino': '【三段撃ちは作り話？】長篠の戦い 武田軍はなぜ壊滅したのか｜地図と『信長公記』で検証',
 '27_sekigahara': '【開戦は何時？】関ヶ原の戦い 小早川秀秋はいつ寝返ったのか｜地図と史料で検証',
 '28_yamazaki': '【秀吉は遅参した？】山崎の戦い 2026年の新説と異論を比べる｜地図で解説',
 '29_shizugatake': '【五時間で五十二キロ？】賤ヶ岳の戦い 前田利家は本当に裏切ったのか｜地図と史料で検証',
 'ID:jY8SSEQrBoA': '【家康の勝ちは本当か？】小牧・長久手の戦い 新発見の秀吉朱印状で読み直す｜地図で解説'}


def vid(ids, k):
    return k[3:] if k.startswith('ID:') else ids[k]['video_id']


def cur(yt, v):
    return yt.videos().list(part='status', id=v).execute()['items'][0]['status'].get('publishAt')


def plan():
    yt = Y.service(); ids = Y.load_ids(); out = {}
    for gl, gs, bl, bs in PAIRS:
        g = [vid(ids, gl), vid(ids, gs)]
        b = [vid(ids, bl)] + ([vid(ids, bs)] if bs else [])
        gd = [cur(yt, x) for x in g]; bd = [cur(yt, x) for x in b]
        # 一般の長尺・Short → 戦況の日時へ。戦況の長尺・Short → 一般の日時へ
        out[g[0]] = bd[0]; out[g[1]] = bd[1] if bs else (datetime.datetime.strptime(bd[0], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        out[b[0]] = gd[0]
        if bs: out[b[1]] = gd[1]
        print(gl, gd, '<->', bl, bd)
    # 実際の移動：長篠(Short無し)は、一般の組を長篠の日へ移し、長篠が一般の長尺の日時へ入る（上の式のまま）
    PL.write_text(json.dumps(out, indent=1), encoding='utf8')
    print(len(out), '本')


def apply():
    yt = Y.service(); plan_ = json.loads(PL.read_text(encoding='utf8'))
    for v, t in plan_.items():
        if cur(yt, v) == t:
            continue
        st = yt.videos().list(part='status', id=v).execute()['items'][0]['status']
        try:
            yt.videos().update(part='status', body=dict(id=v, status=dict(privacyStatus='private', publishAt=t, selfDeclaredMadeForKids=st.get('selfDeclaredMadeForKids', False),
                               embeddable=st.get('embeddable', True), license=st.get('license', 'youtube'), containsSyntheticMedia=st.get('containsSyntheticMedia', False)))).execute()
            print('set', v, t, flush=True)
        except Exception as e:
            print('STOP', v, str(e)[:160]); return
    # 差し替えキューの予約日時も更新
    q = Y.R / 'data' / 'short_cta_queue.json'
    rows = json.loads(q.read_text(encoding='utf8'))
    for r in rows:
        if r['old'] in plan_:
            r['publishAt'] = plan_[r['old']]
    q.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf8')
    print('queue updated')


def titles():
    yt = Y.service(); ids = Y.load_ids()
    for k, t in TITLES.items():
        v = vid(ids, k); assert len(t) <= 100
        s = yt.videos().list(part='snippet', id=v).execute()['items'][0]['snippet']
        if s['title'] == t:
            continue
        yt.videos().update(part='snippet', body=dict(id=v, snippet=dict(title=t, description=s['description'], tags=s.get('tags', []), categoryId=s['categoryId'],
                           defaultLanguage=s.get('defaultLanguage', 'ja'), defaultAudioLanguage=s.get('defaultAudioLanguage', 'ja')))).execute()
        (R / 'upload' / (k if not k.startswith('ID:') else '32_komaki') / 'title.txt').write_text(t + '\n', encoding='utf8')
        print('title', v, t, flush=True)


if __name__ == '__main__':
    {'plan': plan, 'apply': apply, 'titles': titles}[sys.argv[1]]()
