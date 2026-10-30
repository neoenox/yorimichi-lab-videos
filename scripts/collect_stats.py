"""公開済み動画の反応（視聴回数・高評価・コメント）を YouTube Data API で集めて、data/channel_stats.jsonl に追記する。
usage:  python scripts/collect_stats.py            # 集めて追記（約1〜2ユニット）
        python scripts/collect_stats.py --report   # 型・分野・画風ごとの傾向を表示（API不要）
視聴維持率・平均視聴時間は Data API では取れない（Analytics APIの権限が未承認）ので、Studioのアナリティクスで読み、
data/studio_notes.md に追記する（48時間後・7日後）。"""
import datetime as dt
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
META = R / 'data' / 'video_meta.json'
LOG = R / 'data' / 'channel_stats.jsonl'
UPL = R / 'out' / 'codex' / 'browser_uploads.txt'
JST = dt.timezone(dt.timedelta(hours=9))


def current_videos():
    """browser_uploads.txt の最新行から {key: (video_id, publish_at)} を作る。drain は台帳から。"""
    out = {}
    for ln in UPL.read_text(encoding='utf8').splitlines():
        p = ln.split()
        if len(p) == 5 and not ln.startswith('#'):
            out[p[0]] = (p[2], dt.datetime.strptime(f'{p[3]} {p[4]}', '%Y-%m-%d %H:%M').replace(tzinfo=JST))
    ids = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))
    for k, pack in (('short_drain', 'short_drain'),):
        if pack in ids and k not in out:
            out[k] = (ids[pack]['video_id'], dt.datetime(2026, 10, 18, 20, 0, tzinfo=JST))
    if '06_drain_vortex' in ids:
        out.setdefault('drain', (ids['06_drain_vortex']['video_id'], dt.datetime(2026, 10, 18, 19, 0, tzinfo=JST)))
    return out


def collect():
    sys.path.insert(0, str(R / 'scripts'))
    import yt_api
    yt = yt_api.service()
    vids = current_videos()
    now = dt.datetime.now(JST)
    pub = {k: v for k, v in vids.items() if v[1] <= now}
    if not pub:
        print('公開済みの動画はまだありません'); return
    idmap = {v[0]: k for k, v in pub.items()}
    rows = []
    ids = list(idmap)
    for i in range(0, len(ids), 50):
        for it in yt.videos().list(part='statistics,status', id=','.join(ids[i:i + 50])).execute().get('items', []):
            s = it['statistics']
            rows.append(dict(t=now.isoformat(timespec='minutes'), key=idmap[it['id']], id=it['id'], privacy=it['status']['privacyStatus'],
                             views=int(s.get('viewCount', 0)), likes=int(s.get('likeCount', 0)), comments=int(s.get('commentCount', 0)),
                             hours=round((now - pub[idmap[it['id']]][1]).total_seconds() / 3600, 1)))
    with LOG.open('a', encoding='utf8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    for r in rows:
        print(r['key'], r['privacy'], f"{r['views']}回視聴 / 高評価{r['likes']} / コメント{r['comments']} / 公開から{r['hours']}時間")


def latest():
    last = {}
    if LOG.exists():
        for ln in LOG.read_text(encoding='utf8').splitlines():
            if ln.strip():
                r = json.loads(ln); last[r['key']] = r
    return last


def report():
    meta = json.loads(META.read_text(encoding='utf8'))
    last = latest()
    rows = []
    for k, m in meta.items():
        r = last.get(k)
        if r:
            days = max(r['hours'] / 24, 0.5)
            rows.append(dict(key=k, kind=m['kind'], structure=m['structure'], field=m['field'], thumb=m['thumb'], views=r['views'], per_day=round(r['views'] / days, 1), likes=r['likes'], hours=r['hours']))
    if not rows:
        print('まだ集計がありません（collect_stats.py を実行）'); return
    print('key / 種別 / 構成 / 分野 / サムネ / 視聴 / 1日あたり / 高評価 / 公開から時間')
    for x in sorted(rows, key=lambda z: -z['per_day']):
        print(x['key'], x['kind'], x['structure'], x['field'], x['thumb'], x['views'], x['per_day'], x['likes'], x['hours'], sep=' / ')
    for axis in ('kind', 'structure', 'field', 'thumb'):
        g = {}
        for x in rows:
            g.setdefault(x[axis], []).append(x['per_day'])
        print(f'\n[{axis}ごとの1日あたり視聴の平均]  ※本数が少ないうちは、傾向ではなく目安')
        for k, v in sorted(g.items(), key=lambda z: -sum(z[1]) / len(z[1])):
            print(f'  {k}: {sum(v) / len(v):.1f}（{len(v)}本）')


if __name__ == '__main__':
    report() if '--report' in sys.argv else collect()
