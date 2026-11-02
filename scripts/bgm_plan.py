"""BGMを、動画ごと・場面ごとに変える。魔王魂の曲（assets/bgm_maou/ の31曲）を、動画の種類に合わせて割り当てる。
- 種類：戦況(battle_map がある)／江戸(暮らし・史料)／一般(科学・数字・言葉)。種類ごとに、合う曲のプールを持つ
- 章をまとめて1区間60〜100秒にし、区間ごとに曲を替える
- プールの並びは slug のハッシュで動画ごとに変え、隣り合う区間で同じ曲を続けない。動画の最初の曲は、順に配って動画ごとに別にする
usage: python scripts/bgm_plan.py [--apply] slug...   --apply で data/<slug>_spec.json の bgm を書き換える"""
import hashlib, json, random, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
BATTLE = ['orchestra25', 'ethnic33', 'orchestra24', 'piano36', 'orchestra22', 'ethnic25', 'orchestra21', 'piano32', 'orchestra20', 'ethnic30',
          'orchestra23', 'ethnic26', 'orchestra26', 'piano40', 'orchestra19']
EDO = ['acoustic50', 'ethnic06', 'acoustic45', 'piano37', 'acoustic52', 'ethnic31', 'acoustic48', 'piano35', 'acoustic51', 'ethnic25',
       'piano34', 'acoustic47', 'piano12', 'piano38']
GENERAL = ['piano41', 'acoustic51', 'piano39', 'piano33', 'acoustic50', 'piano38', 'acoustic47', 'piano37', 'piano36', 'piano35',
           'acoustic52', 'piano34', 'piano12', 'ethnic31']
EDO_SLUGS = set('''carpenter hikyaku hikeshi kido ryo sankin twomeals sushi doyo shorui yachin yakurei literacy nukemairi travel kashihon recycle
ooka jinko hanabi hatsugatsuo oyatsu yoigoshi chushingura sakoku bath'''.split())
MIN_S = 55


def kind(slug):
    sp = json.loads((R / 'data' / f'{slug}_spec.json').read_text(encoding='utf8'))
    if any(i.get('name') == 'battle_map' for ch in sp['chapters'] for i in ch.get('scene') or []): return 'battle', BATTLE
    if slug in EDO_SLUGS: return 'edo', EDO
    return 'general', GENERAL


def plan(slug, first_idx=0):
    tl = json.loads((R / 'data' / f'{slug}_timeline.json').read_text(encoding='utf8'))
    segs, cur, dur = [], [], 0.0
    for c in tl:
        cur.append(c); dur += c['end'] - c['start']
        if dur >= MIN_S: segs.append(cur); cur, dur = [], 0.0
    if cur:
        if segs and sum(c['end'] - c['start'] for c in cur) < MIN_S * 0.6: segs[-1] += cur
        else: segs.append(cur)
    k, pool = kind(slug)
    rnd = random.Random(int(hashlib.md5(slug.encode()).hexdigest(), 16))
    rest = pool[:]; rnd.shuffle(rest)
    first = pool[first_idx % len(pool)]; rest.remove(first)
    order = [first] + rest
    out, prev = [], None
    for i, sg in enumerate(segs):
        t = order[i % len(order)]
        if t == prev: t = order[(i + 1) % len(order)]
        out.append([sg[0]['key'], sg[-1]['key'], t]); prev = t
    return k, out


if __name__ == '__main__':
    apply = '--apply' in sys.argv
    n = {'battle': 0, 'edo': 0, 'general': 0}
    for s in [a for a in sys.argv[1:] if not a.startswith('--')]:
        k, _ = kind(s); k, pl = plan(s, n[k]); n[k] += 1
        print(s, k, len(pl), '区間', [x[2] for x in pl])
        if apply:
            p = R / 'data' / f'{s}_spec.json'; sp = json.loads(p.read_text(encoding='utf8')); sp['bgm'] = pl
            p.write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf8')
