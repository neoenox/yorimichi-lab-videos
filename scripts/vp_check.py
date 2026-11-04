"""描画前の検査：python scripts/vp.py <slug> check
spec と台本（story のあと）だけを調べ、数秒で次を見つける。描画（数分〜十数分）の前に、定義の誤りを直せる。
  ・章の数・キーが、台本と spec で合っているか
  ・画像キー（img / portrait / base …）が images に在るか、ファイルが在るか、crop が正しいか
  ・anim の name が登録されているか
  ・at / until / legs が、その章の文の数の範囲に収まっているか（文番号のずれの検出に役立つ）
  ・battle_map：座標が地図の範囲か、units の pts と legs の数が合っているか
  ・pop_rows：自動で縮む量（文字が小さくなりすぎないか）、字幕の帯（y836）に届かないか
  ・pop_telop：折り返して、字幕の帯に届かないか
  ・BGM：章キーと曲ファイルが在るか
  ・どの章にも、図・テロップ・背景のどれかがあるか
終了コード：誤り（ERR）があれば 1。注意（WARN）だけなら 0。"""
import json
import sys
from pathlib import Path


def run(V, quiet=False):
    SPEC, slug, P = V['SPEC'], V['SLUG'], V['P']
    errs, warns = [], []
    E = lambda m: errs.append(m)
    W = lambda m: warns.append(m)

    sf = P(f'data/{slug}_scenes.json')
    if not sf.exists():
        E('data/%s_scenes.json が無い。先に python scripts/vp.py %s story を実行する' % (slug, slug))
        return _report(slug, errs, warns, quiet)
    scenes = json.loads(sf.read_text(encoding='utf8'))
    nsent = [len(V['sentences'](s)) for s in scenes]
    skeys = [c['key'] for c in SPEC['chapters']]
    tkeys = [s['key'] for s in scenes]
    if skeys != tkeys:
        E(f'章のキーが台本と合わない：spec={skeys} / 台本={tkeys}')
    images = SPEC.get('images') or {}
    for k, m in images.items():
        f = P(m['file'])
        if not f.exists():
            E(f'画像 {k}: ファイルが無い {m["file"]}')
        c = m.get('crop')
        if c and not (len(c) == 4 and 0 <= c[0] < c[2] <= 1 and 0 <= c[1] < c[3] <= 1):
            E(f'画像 {k}: crop が正しくない {c}')
    used = set()

    import vp_anim
    DRAW = vp_anim.DRAW
    sys.path.insert(0, str(P('scripts')))
    import vp_anim_pop as PP
    PP.bind(V)
    from PIL import Image, ImageDraw
    dm = ImageDraw.Draw(Image.new('RGBA', (8, 8)))

    def chk_idx(where, name, v, n, allow_eq=False):
        if not isinstance(v, int):
            return
        if v < 0 or v > n or (v == n and not allow_eq):
            E(f'{where}: {name}={v} が、文の数 {n}（0〜{n - 1}）の範囲外')

    def walk(o, where, n):
        if isinstance(o, dict):
            if 'at' in o:
                chk_idx(where, 'at', o['at'], n)
            if 'until' in o:
                chk_idx(where, 'until', o['until'], n, allow_eq=True)
                if isinstance(o.get('at'), int) and isinstance(o['until'], int) and o['until'] <= o['at']:
                    E(f'{where}: until={o["until"]} が at={o["at"]} 以前')
            for k in ('img', 'portrait', 'base'):
                v = o.get(k)
                if isinstance(v, str):
                    used.add(v)
                    if v not in images:
                        E(f'{where}: {k}="{v}" が images に無い')
            if o.get('t') == 'art' and isinstance(o.get('name'), str):
                used.add(o['name'])
                if o['name'] not in images:
                    E(f'{where}: art name="{o["name"]}" が images に無い')
            if 'legs' in o and isinstance(o.get('pts'), list):
                if len(o['legs']) != len(o['pts']) - 1:
                    E(f'{where}: legs {len(o["legs"])}区間 と pts {len(o["pts"])}点 が合わない（legs は pts の隣どうしの数）')
                for a, b in o['legs']:
                    chk_idx(where, 'legs[0]', a, n)
                    chk_idx(where, 'legs[1]', b, n, allow_eq=True)   # 文の数と同じ値＝章の終わりまで
                    if a >= b:
                        E(f'{where}: legs [{a},{b}] は、前から後ろの向きにする')
            for v in o.values():
                walk(v, where, n)
        elif isinstance(o, list):
            for v in o:
                walk(v, where, n)

    for ci, ch in enumerate(SPEC['chapters']):
        n = nsent[ci] if ci < len(nsent) else 0
        visual = False
        for ii, it in enumerate(ch['scene']):
            where = f'章{ci + 1} {ch["key"]} 項目{ii + 1}({it.get("name") or it["t"]})'
            if it['t'] not in V['ITEMS']:
                E(f'{where}: 部品 t="{it["t"]}" が無い')
            if it['t'] == 'anim':
                if it.get('name') not in DRAW:
                    E(f'{where}: anim name="{it.get("name")}" が登録されていない')
                if it.get('name') not in ('pop_bgimg',):
                    visual = True
            elif it['t'] not in ('shade',):
                visual = True
            walk(it, where, n)
            nm = it.get('name')
            if nm == 'battle_map':
                for grp in ('places', 'units', 'marks'):
                    for o in it.get(grp, []):
                        pts = o.get('pts') or [o.get('xy')]
                        for q in pts:
                            if q and not (-0.08 <= q[0] <= 1.08 and -0.08 <= q[1] <= 1.08):
                                W(f'{where}: {grp} の座標 {q} が地図の範囲外（0〜1）')
                if it.get('img') not in images:
                    E(f'{where}: 地図 img="{it.get("img")}" が images に無い')
            if nm == 'pop_rows':
                x0, x1, y = it.get('x0', 100), it.get('x1', 1820), it.get('y0', 190)
                size, gap = it.get('size', 40), it.get('gap', 18)
                ymax = it.get('ymax', PP.SUB_TOP)
                s0 = size
                while True:
                    f = PP.semi(size)
                    ft = PP.heavy(int(size * .86))
                    yy = y
                    for e in it['items']:
                        tg = e.get('tag')
                        tw0 = int(dm.textlength(tg, font=ft)) + 44 if tg else 0
                        ln = V['wrapn'](dm, e['text'], f, x1 - x0 - tw0 - 60)
                        yy += max(len(ln) * int(size * 1.3), int(size * 1.2)) + 30 + gap
                    if yy - gap <= ymax or size <= 24:
                        break
                    size = int(size * .92)
                    gap = max(8, int(gap * .9))
                if yy - gap > ymax:
                    E(f'{where}: 文が多すぎて、字幕の帯（y{ymax}）に届く（最小の文字でも {yy - gap}）。項目を減らすか、1つずつ入れ替える')
                elif size < s0 and size < 30:
                    W(f'{where}: 文字が {s0}→{size} まで縮む（スマホで読みにくい）。項目を分ける')
                elif size < s0 * .8:
                    W(f'{where}: 文字が {s0}→{size} に縮む')
            if nm == 'pop_telop':
                size = it.get('size', 100)
                maxw = it.get('maxw', 1500)
                txt = it['text'].replace('[[', '').replace(']]', '')
                f = PP.heavy(size)
                lines = 1
                for part in txt.split('\n'):
                    lines += int(dm.textlength(part, font=f) // maxw)
                if it.get('y', 500) + lines * size * .65 > PP.SUB_TOP + 20:
                    W(f'{where}: テロップ「{txt[:10]}…」が下に寄りすぎ（y={it.get("y")}、{lines}行）。字幕の帯にかかる')
        if not visual:
            W(f'章{ci + 1} {ch["key"]}: 図・テロップ・カードが無い（背景だけ。文字だけの章を作らない）')
        elif ci < len(nsent) and n == 0:
            E(f'章{ci + 1} {ch["key"]}: 台本に文が無い')

    # BGM
    for b in SPEC.get('bgm', []):
        if len(b) != 3:
            E(f'bgm {b}: [開始章key, 終了章key, 曲名] の形にする')
            continue
        a, c, name = b
        if a not in skeys or c not in skeys:
            E(f'bgm {b}: 章キー {a}/{c} が spec に無い')
        elif skeys.index(a) > skeys.index(c):
            E(f'bgm {b}: 開始が終了より後ろ')
        if not (P('assets/bgm_maou') / f'maou_bgm_{name}.mp3').exists():
            E(f'bgm {b}: 曲 assets/bgm_maou/maou_bgm_{name}.mp3 が無い')
    covered = set()
    for a, c, _ in SPEC.get('bgm', []):
        if a in skeys and c in skeys:
            covered |= set(range(skeys.index(a), skeys.index(c) + 1))
    if SPEC.get('bgm') and covered != set(range(len(skeys))):
        W(f'bgm が、章 {sorted(set(range(len(skeys))) - covered)} を覆っていない')
    for k in images:
        if k not in used and not k.startswith('p_'):
            W(f'画像 {k} は、どこにも使っていない')
    return _report(slug, errs, warns, quiet)


def _report(slug, errs, warns, quiet):
    if not quiet:
        for m in errs:
            print('ERR ', m)
        for m in warns:
            print('WARN', m)
        print(f'check {slug}: ERR {len(errs)} / WARN {len(warns)}' + ('  → 描画してよい' if not errs else '  → 直してから描画する'))
    return 1 if errs else 0
