"""公開済み動画の再生数から「長尺とShortsの落差」を出す（API不要・out/youtube_status.json を読むだけ）。

usage:
  python scripts/report_views.py                 # 表を表示（長尺・Shorts・予約・ペース）
  python scripts/report_views.py > out/views.md  # Markdownとして保存

out/youtube_status.json は、クォータのある日に
  python scripts/yt_api.py stats > out/youtube_status.txt
ではなく、収集スクリプト（過去に out/ に置いたもの）で作る。数字が古いときは取得日時を見ること。
分析の結論は docs/ANALYSIS_2026-11-01_long_zero_views.md。
"""
import datetime as dt
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parents[1]
SRC = R / 'out' / 'youtube_status.json'
JST = dt.timezone(dt.timedelta(hours=9))


def secs(dur):
    m = re.fullmatch(r'PT(?:(\d+)M)?(?:(\d+)S)?', dur or '')
    return (int(m.group(1) or 0) * 60 + int(m.group(2) or 0)) if m else 0


def dedupe(rows):
    seen = {}
    for r in rows:
        seen.setdefault(r['id'], r)
    return list(seen.values())


def main():
    if not SRC.exists():
        sys.exit(f'{SRC} がありません（先にYouTubeの状態を取得してください）')
    d = json.loads(SRC.read_text(encoding='utf8'))
    now = dt.datetime.strptime(d['now_jst'], '%Y-%m-%dT%H:%M').replace(tzinfo=JST)
    pub = dedupe(d['public_with_views'])
    sched = dedupe(d['scheduled_future'])
    priv = dedupe(d['private_unscheduled'])
    longs = [x for x in pub if secs(x['dur']) >= 120]
    shorts = [x for x in pub if secs(x['dur']) < 120]

    print(f'# 実測（{d["now_jst"]} 取得）\n')
    print('## 公開済みの長尺\n')
    print('| # | 動画ID | 公開日 | 長さ | 再生 | タイトル |')
    print('|---|---|---|---|---|---|')
    for i, x in enumerate(sorted(longs, key=lambda y: y['published_jst']), 1):
        print(f"| {i} | `{x['id']}` | {x['published_jst'][:10]} | {secs(x['dur'])}s | {x['views']} | {x['title']} |")
    lv = [x['views'] for x in longs]
    print()
    print(f"長尺 {len(longs)}本 / 合計 {sum(lv)} / 中央値 {statistics.median(lv)} / 最大 {max(lv)} / 0再生 {sum(1 for v in lv if v == 0)}本")

    print('\n## 公開済みのShorts\n')
    print('| # | 動画ID | 公開日 | 長さ | 再生 | タイトル |')
    print('|---|---|---|---|---|---|')
    for i, x in enumerate(sorted(shorts, key=lambda y: -y['views']), 1):
        print(f"| {i} | `{x['id']}` | {x['published_jst'][:10]} | {secs(x['dur'])}s | {x['views']} | {x['title']} |")
    sv = [x['views'] for x in shorts]
    print()
    print(f"Shorts {len(shorts)}本 / 合計 {sum(sv)} / 中央値 {statistics.median(sv)} / 最小 {min(sv)} 最大 {max(sv)}（{max(sv)/min(sv):.2f}倍）")
    if sum(sv):
        print(f"長尺 ÷ Shorts = {sum(lv)/sum(sv)*100:.2f}%")

    print('\n## 0再生の長尺（経過時間）\n')
    print('| 動画ID | 公開 | 経過 | タイトル |')
    print('|---|---|---|---|')
    for x in sorted(longs, key=lambda y: y['published_jst']):
        if x['views']:
            continue
        t = dt.datetime.strptime(x['published_jst'][:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=dt.timezone.utc)
        print(f"| `{x['id']}` | {x['published_jst'][:10]} | {(now-t).total_seconds()/3600:.0f}h | {x['title']} |")

    print('\n## タイトル型\n')
    print('| 群 | 本数 | 平均再生 | 「？」 | 「確かめる」 | 数字入り |')
    print('|---|---|---|---|---|---|')
    for name, rows in (('長尺', longs), ('Shorts', shorts)):
        v = [x['views'] for x in rows]
        print(f"| {name} | {len(rows)} | {sum(v)/len(v):.1f} | {sum('？' in x['title'] for x in rows)}/{len(rows)} | "
              f"{sum('確かめる' in x['title'] for x in rows)}/{len(rows)} | "
              f"{sum(bool(re.search(r'[0-9０-９]', x['title'])) for x in rows)}/{len(rows)} |")

    print('\n## 予約と空き\n')
    by_day = Counter(x['scheduled_jst'][:10] for x in sched)
    print(f"予約 {len(sched)}本（長尺 {sum(1 for x in sched if secs(x['dur']) >= 120)} / Shorts {sum(1 for x in sched if secs(x['dur']) < 120)}）"
          f" / 期間 {min(x['scheduled_jst'] for x in sched)} 〜 {max(x['scheduled_jst'] for x in sched)}")
    print(f"予約のある日 {len(by_day)}日 / 平均 {len(sched)/len(by_day):.2f}本/日 / 最大 {max(by_day.values())}本")
    multi = {k: v for k, v in by_day.items() if v > 1}
    print(f"2本以上の日: {len(multi)}日")
    long_days = {x['scheduled_jst'][:10] for x in sched if secs(x['dur']) >= 120}
    gap = [(now.date() + dt.timedelta(days=i)) for i in range(31)]
    gap = [g for g in gap if str(g) not in long_days]
    print(f"今後31日で長尺の無い日: {len(gap)}日（{', '.join(str(g) for g in gap)}）")
    print(f"\n未予約の非公開: {len(priv)}本（長尺 {sum(1 for x in priv if secs(x['dur']) >= 120)} / Shorts {sum(1 for x in priv if secs(x['dur']) < 120)}）")


if __name__ == '__main__':
    main()
