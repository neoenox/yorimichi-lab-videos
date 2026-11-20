"""全ShortsのAnalyticsを取得し、戦略用のJSON＋Markdownを出す（読み取り専用）。

usage: python scripts/analyze_shorts.py [--out docs/SHORTS_ANALYTICS_YYYYMMDD.md]
Analytics API は1回200行まで。startIndexでページングして全動画を取る。
動画長・公開日時はData APIから別途取得し、尺別・曜日別の集計に使う。
"""
import argparse, datetime, json, re, statistics, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))
import yt_api, yt_analytics

METRICS = 'views,averageViewDuration,averageViewPercentage,estimatedMinutesWatched,likes,shares,comments,subscribersGained'
START = '2026-10-01'

def iso_duration(s):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s or '')
    if not m: return 0
    h, mi, sec = (int(x or 0) for x in m.groups())
    return h * 3600 + mi * 60 + sec

def fetch_analytics(end):
    svc = yt_analytics.svc(); rows = []
    idx = 1
    while True:
        r = yt_analytics.q(svc, metrics=METRICS, dimensions='video', sort='-views',
                           startIndex=idx, maxResults=200, start=START, end=end)
        batch = r.get('rows', [])
        rows.extend(batch)
        if len(batch) < 200: break
        idx += 200
    return rows

def fetch_details(ids):
    yt = yt_api.service(); out = {}
    for i in range(0, len(ids), 50):
        chunk = ids[i:i+50]
        r = yt.videos().list(part='contentDetails,snippet', id=','.join(chunk), maxResults=50).execute()
        for x in r.get('items', []):
            out[x['id']] = {'duration': iso_duration(x['contentDetails'].get('duration')),
                            'title': x['snippet']['title'],
                            'published': x['snippet'].get('publishedAt', '')[:10]}
    return out

def bucket(dur):
    if dur <= 0: return 'unknown'
    if dur < 30: return '<30s'
    if dur < 46: return '30-45s'
    if dur < 61: return '46-60s'
    if dur < 76: return '61-75s'
    return '76s+'

def topic(title):
    t = title or ''
    if t.startswith('【'): return 'news'
    if any(k in t for k in ['江戸', '幕府', '戦い', '合戦', '城', '武将', '大名', '天皇', '織田', '徳川', '豊臣', '鎌倉', '室町', '平安', '戦国', '本能寺', '姉川', '長篠', '山崎', '小牧', '関ヶ原', '島原', '参勤交代', '武士', '藩']): return 'history'
    if any(k in t for k in ['暦', '夏至', '冬至', '春分', '秋分', '日の出', '日の入り', '時刻', '標準時', '時計', 'うるう', '元日', '年末', '月食', '日食', '均時差', '流星', '星', '太陽']): return 'calendar/sky'
    if any(k in t for k in ['地震', 'マグニチュード', '津波', '台風', '雷', '海', '川', '山', '森', '森林', '氷', '雪', '雨', '気温', '暑い', '寒い']): return 'nature'
    if any(k in t for k in ['脳', '風邪', 'ビタミン', '米', '食', '賞味期限', '郵便', '電車', 'お金', '物価', '経済']): return 'life/science'
    return 'other'

def pct(xs):
    return f'{statistics.median(xs):.1f}' if xs else '-'

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', default=str(R / 'docs' / 'SHORTS_ANALYTICS_20261120.md'))
    ap.add_argument('--json', default=str(R / 'data' / 'shorts_analytics_20261120.json'))
    a = ap.parse_args()
    end = datetime.date.today().isoformat()
    rows = fetch_analytics(end)
    ids = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf-8'))
    names = {v['video_id']: k for k, v in ids.items() if v.get('video_id')}
    details = fetch_details([r[0] for r in rows])
    recs = []
    for vid, views, avd, avp, mins, likes, shares, comments, subs in rows:
        key = names.get(vid, vid)
        if not key.startswith('short'): continue
        d = details.get(vid, {})
        dur = d.get('duration', 0)
        pub = d.get('published', '')
        ledger_at = (ids.get(key) or {}).get('publishAt')
        hour = ''
        if ledger_at:
            try:
                hour = (datetime.datetime.fromisoformat(ledger_at.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%H:%M')
            except Exception: pass
        age = ''
        if pub:
            try: age = (datetime.date.fromisoformat(end) - datetime.date.fromisoformat(pub)).days
            except Exception: pass
        recs.append(dict(id=vid, key=key, title=d.get('title', ''), views=views,
                         avg_sec=round(avd, 1), duration=dur, avg_pct=round(avp, 1),
                         likes=likes, shares=shares, comments=comments, subs=subs,
                         like_rate=round(likes / views * 100, 2) if views else 0,
                         retention=round(avd / dur, 2) if dur else None,
                         bucket=bucket(dur), topic=topic(d.get('title', '')),
                         published=pub, hour=hour, age_days=age))
    Path(a.json).write_text(json.dumps(recs, ensure_ascii=False, indent=1), encoding='utf-8')
    views = [r['views'] for r in recs]
    lines = ['# 全Shortsのアナリティクス調査と戦略（2026-11-20）', '',
             '## 注意', '- Analytics APIの数値は1〜2日遅れ。**2026-11-16に視聴回数の集計仕様が更新**されており、前後の比較は同じ条件的前提を崩す可能性がある。',
             '- インプレッション／CTRはAPIに無く扱わない。スワイプ率もAPIに無いが、Studio画面の実測値3本のみを戦略節で参照する。', '',
             '## 全体', f'- 対象Shorts: **{len(recs)}本** / 合計視聴回数 {sum(views):,}回 / 中央値 {pct(views)}回',
             f'- 平均視聴率の中央値 {pct([r["avg_pct"] for r in recs])}% / いいね率の中央値 {pct([r["like_rate"] for r in recs])}%', '',
             '## 尺別（中央値）', '| 尺 | 本数 | 再生数 | 平均視聴率 | 継続比 |', '|---|---:|---:|---:|---:|']
    for b in ['<30s', '30-45s', '46-60s', '61-75s', '76s+', 'unknown']:
        g = [r for r in recs if r['bucket'] == b]
        if not g: continue
        lines.append(f'| {b} | {len(g)} | {pct([r["views"] for r in g])} | {pct([r["avg_pct"] for r in g])}% | {pct([x for x in [r["retention"] for r in g] if x is not None])} |')
    lines += ['', '## テーマ別（中央値・上位5本は本文で後述）', '| テーマ | 本数 | 再生数 | 平均視聴率 |', '|---|---:|---:|---:|']
    for t in sorted(set(r['topic'] for r in recs)):
        g = [r for r in recs if r['topic'] == t]
        lines.append(f'| {t} | {len(g)} | {pct([r["views"] for r in g])} | {pct([r["avg_pct"] for r in g])}% |')
    lines += ['', '## 上位20本（再生数順）', '| 順 | 動画 | 尺 | 再生 | 平均視聴率 | 継続比 | テーマ |', '|---:|---|---:|---:|---:|---:|---|']
    for i, r in enumerate(sorted(recs, key=lambda x: -x['views'])[:20], 1):
        lines.append(f'| {i} | {r["key"]} | {r["duration"]}s | {r["views"]:,} | {r["avg_pct"]}% | {r["retention"]} | {r["topic"]} |')
    lines += ['', '## 公開時刻別（中央値・予約時刻があるもの）', '| 時刻 | 本数 | 再生数 | 平均視聴率 |', '|---|---:|---:|---:|']
    for h in sorted(set(r['hour'] for r in recs if r['hour'])):
        g = [r for r in recs if r['hour'] == h]
        lines.append(f'| {h} | {len(g)} | {pct([r["views"] for r in g])} | {pct([r["avg_pct"] for r in g])}% |')
    lines += ['', '## 下位20本（再生数順の末尾・age=公開からの日数）', '| 動画 | 尺 | 再生 | 平均視聴率 | age |', '|---|---:|---:|---:|---:|']
    for r in sorted(recs, key=lambda x: x['views'])[:20]:
        lines.append(f'| {r["key"]} | {r["duration"]}s | {r["views"]:,} | {r["avg_pct"]}% | {r["age_days"]} |')
    lines += ['', '## 戦略（このデータから）',
        '- **尺は短めが有利**: 30〜45秒の中値715回／平均視聴率60.9%に対し、46〜60秒は334回／52.9%、61〜75秒は216回／46.0%。公開からの日数は各群10〜14日で大きく差がなく、尺の効果と無関係とは言い切れない。新規Shortは30〜45秒を優先し、55秒を超えないようにする（既存の手順書の50〜55秒目標は、このデータを受けて見直す）。',
        '- **テーマは「歴史×数字」が強い**: history（28本）の中値622回／60.8%に対し、news（24本）は163回／42.2%。ニュースは鮮度が落ちやすい。江戸・暦の身近な思い込みを一次資料で検証する型を継続する。',
        '- **「繰り返し見られる」設計**: 平均視聴率>100%の13本は再生数の中値918回で、<=100%の114本は288回。数字の比較・図解でリピートを誘う構成を優先（上位の short_koku 123% / short_scurvy 144% / short_oke 115%）。',
        '- **冒頭フックの新型は一旦採用しない**: Studio実測では新型（4〜6秒に数字）の凌雲閣は「視聴を継続10%／スワイプ90%」、旧型の玉川上水26.5%／73.5%、プラニマル28.2%／71.8%。入口の離脱が悪い。11/26に発電（11/24公開）の数値を加えてn=2で判定し、それまでは標準化しない。',
        '- **19:00枠の再活用**: 長尺49件の予約を解除したため19:00が空いている。API数値では19:00のShorts（4本）は平均視聴率86.0%と高いがサンプルが小さい。既存の12:00/17:00に加え、19:00を短期テスト枠として使う価値がある（結論は数週間の追跡後）。',
        '- **低再生組は「届いていない」**: 下位20本は公開から11〜15日で1〜45回。内容の前にインプレッションが付いていない可能性が高く、台本の修正よりタイトル・サムネイル・投稿時刻の検証を優先する。',
        '',
        '## 解釈の限界',
        '- テーマ分類はタイトルのキーワード一致（簡易）。「other」が64本ある。',
        '- 相関は因果ではない。尺が短いほど良いと断定せず、同じ題材・同じ時期で比較する。',
        '- Studioのスワイプ率は3本のみの実測。KPI判定は11/26まで保留。']
    Path(a.out).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('rows', len(rows), 'shorts', len(recs), 'out', a.out, a.json)

if __name__ == '__main__':
    main()
