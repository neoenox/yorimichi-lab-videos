"""チャンネルの傾向から、次の動画の題材を決める（候補を採点して順位をつける）。
usage: python scripts/topic_pick.py [--month 11] [--top 8] [--write docs/themes/<dir>/04_scores.md]
入力: data/channel_profile.json（既存動画・実績）、data/topic_candidates.json（候補）
考え方（詳しくは docs/TOPIC_PICK_LOGIC.md）:
  総合点 = 基礎点(問い・資料・見せ方・権利) 45% + 新しさ 15% + カテゴリの偏りの是正 10% + 既存動画との接続 10% + 実績の傾向 10% + 季節 10%
  関門: gate_blockers がある候補は落とす。資料の点が3未満は「要確認」。既存動画との重なりが大きい候補は落とす。
実績(views)が入っていないうちは、実績の傾向は中立(0.5)。Studio の数字を channel_profile.json に追記すると、伸びたカテゴリ・タグが上位に出る。
点数は目安。採用前に、骨格の事実を一次資料で確認する（関門）のはこれまでどおり。最終決定は人。"""
import argparse, json, re
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parents[1]
W = dict(base=.45, novelty=.15, balance=.10, series=.10, perf=.10, season=.10)
BASE_W = dict(hook=.35, source=.30, visual=.25, rights=.10)
OVERLAP_DROP = .5   # タグの重なり(Jaccard)がこれ以上なら「ほぼ同じ話」として落とす


def load():
    prof = json.loads((R / 'data' / 'channel_profile.json').read_text(encoding='utf8'))
    cand = json.loads((R / 'data' / 'topic_candidates.json').read_text(encoding='utf8'))['candidates']
    return prof['videos'], cand


def bigrams(s):
    s = re.sub(r'[\s、。？！「」（）()・]', '', s)
    return {s[i:i + 2] for i in range(len(s) - 1)}


def jac(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


def overlap(c, videos):
    """既存動画との重なり。タグの Jaccard と題名の2文字連続の重なりの大きいほう。最も近い動画も返す。"""
    best, who = 0.0, None
    for v in videos:
        o = max(jac(set(c['tags']), set(v['tags'])), jac(bigrams(c['title']), bigrams(v['title'])) * 1.5)
        if o > best:
            best, who = o, v['slug']
    return best, who


def perf_by(videos, key):
    """カテゴリ(またはタグ)ごとの平均再生数を、全体平均に寄せて(縮小推定)、0..1にする。実績がなければ 0.5。"""
    vs = [v for v in videos if v.get('views')]
    if len(vs) < 3:
        return {}, False
    g = sum(v['views'] for v in vs) / len(vs)
    k = 2.0
    agg = {}
    for v in vs:
        for x in ([v['cat']] if key == 'cat' else v['tags']):
            agg.setdefault(x, []).append(v['views'])
    return {x: min(1.0, ((sum(a) + k * g) / (len(a) + k)) / (2 * g)) for x, a in agg.items()}, True


def season_score(c, month):
    if not c.get('season'):
        return .5                      # 通年ネタ。季節の加点も減点もなし
    for d in range(0, 3):              # 今月〜2か月先の公開に向く
        if ((month - 1 + d) % 12) + 1 in c['season']:
            return 1.0 - .15 * d
    return .1


def score(c, videos, month):
    base = sum(c[k] / 5 * w for k, w in BASE_W.items()) / sum(BASE_W.values())
    ov, near = overlap(c, videos)
    novelty = max(0.0, 1 - ov / OVERLAP_DROP)
    share = Counter(v['cat'] for v in videos)
    balance = max(0.0, 1 - (share.get(c['cat'], 0) / max(1, len(videos))) / .3)
    ties = [t for t in c.get('ties', []) if any(v['slug'] == t for v in videos)]
    series = min(1.0, len(ties) / 2)
    pc, ok = perf_by(videos, 'cat')
    pt, _ = perf_by(videos, 'tag')
    perf = .5 if not ok else (.6 * pc.get(c['cat'], .5) + .4 * (sum(pt.get(t, .5) for t in c['tags']) / len(c['tags'])))
    seas = season_score(c, month)
    parts = dict(base=base, novelty=novelty, balance=balance, series=series, perf=perf, season=seas)
    total = 100 * sum(W[k] * parts[k] for k in W)
    flags = []
    if c['gate_blockers']:
        flags.append('関門で落ちる：' + '／'.join(c['gate_blockers']))
    if ov >= OVERLAP_DROP:
        flags.append(f'既存「{near}」とほぼ同じ話（重なり {ov:.2f}）')
    if c['source'] < 3:
        flags.append('資料の点が低い（要確認）')
    elif c['source'] == 3:
        flags.append('骨格の事実を一次資料で確かめられるか要確認')
    return dict(c=c, total=total, parts=parts, flags=flags, near=near, ov=ov, drop=bool(c['gate_blockers']) or ov >= OVERLAP_DROP, ties=ties)


def report(rows, month, top):
    out = [f'# 次の動画の題材：採点結果（公開月の想定：{month}月）', '',
           '点数は目安です。上位の候補は、採用前に「骨格の事実を一次資料で確認する」関門を通します。最終決定は人。', '',
           '| 順位 | 総合 | 題 | 問い | 新しさ | 偏り | 接続 | 実績 | 季節 | 注意 |', '|---|---|---|---|---|---|---|---|---|---|']
    ok = [r for r in rows if not r['drop']]
    for i, r in enumerate(ok[:top], 1):
        p = r['parts']; c = r['c']
        out.append(f"| {i} | **{r['total']:.0f}** | {c['title']} | {c['hook']}/5 | {p['novelty']:.2f} | {p['balance']:.2f} | {'・'.join(r['ties']) or '—'} | {p['perf']:.2f} | {p['season']:.2f} | {'；'.join(r['flags']) or '—'} |")
    dropped = [r for r in rows if r['drop']]
    if dropped:
        out += ['', '## 落とした候補', '']
        out += [f"- {r['c']['title']} … {'；'.join(r['flags'])}" for r in dropped]
    if ok:
        b = ok[0]; c = b['c']
        out += ['', '## 第1候補の次の一手', '',
                f"- 題：{c['title']}", f"- 資料の当たり：{c['source_hint']}",
                '- 手順：①骨格の事実を一次資料で確認（`08_fact_check.md`）→ ②台本v1 → ③web版ChatGPTでの台本査読 → ④vp.py で制作 → ⑤Codexの通し視聴・読み確認（Codexは評価のみ）', '']
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--month', type=int, default=None, help='公開を想定する月(1-12)。省略時は来月')
    ap.add_argument('--top', type=int, default=8)
    ap.add_argument('--write')
    a = ap.parse_args()
    import datetime
    month = a.month or ((datetime.date.today().month % 12) + 1)
    videos, cand = load()
    rows = sorted((score(c, videos, month) for c in cand), key=lambda r: -r['total'])
    txt = report(rows, month, a.top)
    if a.write:
        p = Path(a.write)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(txt, encoding='utf8')
    print(txt)


if __name__ == '__main__':
    main()
