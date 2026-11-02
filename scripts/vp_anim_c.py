"""自作アニメーション部品（その3）：戦況図 battle_map（「◯◯の戦い」シリーズ）。
地図の上を軍勢の駒（指揮官の肖像つき）が、文に合わせて動く。桶狭間の oke_march を一般化したもの。vp_anim.py の末尾から読み込まれる。"""
import math
from PIL import Image, ImageDraw
import vp_anim as A
from vp_anim import layer, commit, text, circle, poly, ease, T, S, WHITE
from vp_anim_b import _fadein, _dashed

_PORT = {}


def _portrait(name, r):
    """images の name（crop 付き）を、直径 2r の円形に切り出す"""
    k = (name, r)
    if k not in _PORT:
        pic = A.get_img(name, 4 * r, 4 * r)
        side = min(pic.width, pic.height)
        sq = pic.crop(((pic.width - side) // 2, 0, (pic.width + side) // 2, side)).resize((2 * r * S, 2 * r * S), Image.LANCZOS)
        mask = Image.new('L', sq.size, 0)
        ImageDraw.Draw(mask).ellipse((0, 0, sq.width - 1, sq.height - 1), fill=255)
        out = Image.new('RGBA', sq.size, (0, 0, 0, 0))
        out.paste(sq.convert('RGBA'), (0, 0), mask)
        _PORT[k] = out
    return _PORT[k]


def _hit(a, b, pad=4):
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


def _plate2(d, xy, s, size, col, anchor='lm', sub=None, avoid=None):
    """ラベル板。avoid=[(x0,y0,x1,y1),...] にぶつかるときは、上下にずらして避ける（顔写真・先に描いた板を隠さない）。板の位置は avoid に追記する"""
    f = A.F[size * S]
    w = d.textlength(s, font=f) / S
    w2 = (d.textlength(sub, font=A.F[int(size * 0.78) * S]) / S) if sub else 0
    ww = max(w, w2)
    x, y = xy
    x0 = x if anchor[0] == 'l' else (x - ww / 2 if anchor[0] == 'm' else x - ww)
    h = size * (2.0 if sub else 0.8)
    if avoid is not None:
        def rect(yy):
            return (x0 - 10, yy - size * 0.7 - 4, x0 + ww + 10, yy + (size * 1.3 + 6 if sub else size * 0.7 + 4))
        if any(_hit(rect(y), r) for r in avoid):
            step = max(10, int(size * 0.5)); best = y
            for n in range(1, 13):
                for sgn in (-1, 1):
                    yy = y + sgn * n * step
                    if not any(_hit(rect(yy), r) for r in avoid):
                        best = yy; break
                else:
                    continue
                break
            y = best
        avoid.append(rect(y))
    d.rounded_rectangle(((x0 - 10) * S, (y - size * 0.7 - 4) * S, (x0 + ww + 10) * S, (y + (size * 1.3 + 6 if sub else size * 0.7 + 4)) * S), 10 * S,
                        fill=(6, 14, 22, 215), outline=tuple(col) + (255,), width=2 * S)
    text(d, (x0, y), s, size, WHITE, 'lm')
    if sub:
        text(d, (x0, y + size * 0.85), sub, int(size * 0.78), (200, 214, 222), 'lm')


def _upto2(pts, s):
    out = [pts[0]]
    for i in range(len(pts) - 1):
        seg = math.dist(pts[i], pts[i + 1])
        if s >= seg:
            out.append(pts[i + 1])
            s -= seg
        else:
            f = s / seg if seg else 0
            out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f))
            break
    return out


def _vis(cx, o):
    return cx.on(o.get('at')) and not (o.get('until') is not None and cx.on(o['until']))


def battle_map(im, d0, cx, it, a):
    """戦況図。spec: dict(t='anim', name='battle_map', img='<imagesのキー>', box=[...], at=N, until=M,
      places=[dict(xy=(nx,ny), label, kind='castle|camp|spot', at, col, side='l|r|t|b')],
      lines=[dict(pts=[(nx,ny),...], label, at, col, dash=True, lab=(nx,ny))],
      units=[dict(label, sub, col, portrait='<imagesのキー>', pts=[(nx,ny),...], legs=[[i0,i1],...], at, until, head, lab_off, trail, dashed)],
      marks=[dict(xy, at, label, col)])
    座標 (nx,ny) は地図の左上=(0,0)、右下=(1,1)。legs[k]=[i0,i1]：文 i0 の開始から文 i1 の開始までに pts[k]→pts[k+1] へ動く。区間の外は通過点で止まる。"""
    box = it['box']
    W, H = box[2] - box[0], box[3] - box[1]
    pic = A.get_img(it['img'], W - 16, H - 16)
    px0, py0 = (W - pic.width) // 2, 8
    mp = pic.convert('RGBA')
    if a < 1:
        mp.putalpha(mp.getchannel('A').point(lambda v: int(v * a)))
    im.alpha_composite(mp, (box[0] + px0, box[1] + py0))
    mw, mh = pic.width, pic.height
    L, d = layer([0, 0, mw, mh])
    n = len(cx.segl)
    avoid = []   # 描いたラベル板・顔写真の範囲
    late = []

    def P(q):
        return (q[0] * mw, q[1] * mh)

    for ln in it.get('lines', []):
        if not _vis(cx, ln):
            continue
        k = _fadein(T(cx, ln.get('at')))
        col = tuple(ln.get('col', (255, 220, 120)))
        pts = [P(q) for q in ln['pts']]
        if ln.get('dash', False):
            for i in range(len(pts) - 1):
                _dashed(d, pts[i], pts[i + 1], col + (int(235 * k),), 6, 16, 10)
        else:
            poly(d, pts, (6, 14, 22, int(170 * k)), 12)
            poly(d, pts, col + (int(235 * k),), 7)
        if ln.get('label'):
            lx, ly = P(ln.get('lab', ln['pts'][len(ln['pts']) // 2]))
            _plate2(d, (lx + 14, ly), ln['label'], ln.get('lsize', 26), col, 'lm', avoid=avoid)
    for pl in it.get('places', []):
        if not _vis(cx, pl):
            continue
        k = _fadein(T(cx, pl.get('at')), 0.5)
        x, y = P(pl['xy'])
        col = tuple(pl.get('col', (245, 243, 232)))
        kind = pl.get('kind', 'spot')
        r = 13
        if kind == 'castle':
            d.rectangle(((x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S), fill=(16, 22, 30, int(255 * k)), outline=col + (int(255 * k),), width=4 * S)
            d.rectangle(((x - r + 5) * S, (y - r + 5) * S, (x + r - 5) * S, (y + r - 5) * S), fill=col + (int(255 * k),))
        elif kind == 'camp':
            d.polygon([(x * S, (y - r - 3) * S), ((x + r + 3) * S, (y + r) * S), ((x - r - 3) * S, (y + r) * S)], fill=col + (int(235 * k),), outline=(250, 248, 240, int(255 * k)))
        else:
            circle(d, (x, y), 11, fill=col + (int(235 * k),), outline=(250, 248, 240, int(255 * k)), w=3)
        off = {'r': (22, 0, 'lm'), 'l': (-22, 0, 'rm'), 't': (0, -34, 'mm'), 'b': (0, 40, 'mm')}[pl.get('side', 'r')]
        if pl.get('label'):
            late.append(((x + off[0], y + off[1]), pl['label'], pl.get('lsize', 24), col, off[2]))   # 駒を描いた後に、避けながら置く
    def _unit_state(u):
        pts = [P(q) for q in u['pts']]
        if len(pts) == 1 or not u.get('legs'):
            return pts, [pts[0]], pts[0]
        k = 0
        for j, (i0, _) in enumerate(u['legs']):
            if i0 < n and cx.t >= cx.st[i0]:
                k = j
        i0, i1 = u['legs'][k][0], u['legs'][k][1]
        t0 = cx.st[i0] if i0 < n else cx.st[-1]
        t1 = cx.st[i1] if i1 < n else cx.st[n - 1] + cx.segl[n - 1]['duration']
        p = 0.0 if cx.t <= t0 else min(1.0, (cx.t - t0) / max(.001, t1 - t0))
        sdist = sum(math.dist(pts[j], pts[j + 1]) for j in range(k)) + ease(p) * math.dist(pts[k], pts[k + 1])
        trav = _upto2(pts, sdist)
        return pts, trav, trav[-1]

    vis_units = [u for u in it.get('units', []) if _vis(cx, {'at': u.get('at', 0), 'until': u.get('until')})]
    states = [_unit_state(u) for u in vis_units]
    for u, (_, _, head) in zip(vis_units, states):   # 顔写真の位置を先に登録（ラベルは全員の顔を避ける）
        r = u.get('head', 26)
        avoid.append((head[0] - r - 8, head[1] - r - 8, head[0] + r + 8, head[1] + r + 8))
    heads_draw = []
    for u, (pts, trav, head) in zip(vis_units, states):
        fade = _fadein(T(cx, u.get('at', 0)), 0.5)
        col = tuple(u['col'])
        if len(trav) > 1 and u.get('trail', True):
            if u.get('dashed'):
                for i in range(len(trav) - 1):
                    _dashed(d, trav[i], trav[i + 1], col + (int(220 * fade),), 6, 14, 10)
            else:
                poly(d, trav, (6, 14, 22, int(160 * fade)), 13)
                poly(d, trav, col + (int(225 * fade),), 8)
        r = u.get('head', 26)
        heads_draw.append((u, head, fade, col, r))
        if u.get('label'):
            ox, oy = u.get('lab_off', (r + 16, -r - 6))
            ls = u.get('lsize', 26)
            top = head[1] + oy - ls * 0.7 - 4; bot = head[1] + oy + (ls * 1.3 + 6 if u.get('sub') else ls * 0.7 + 4)
            if bot > head[1] - r - 10 and top < head[1] + r + 10 and ox < r + 22:
                ox = r + 22   # 板が顔写真に重なるときは、右へ出す
            _plate2(d, (head[0] + ox, head[1] + oy), u['label'], ls, col, 'lm', sub=u.get('sub'), avoid=avoid)
    for xy_, lab_, ls_, col_, anc_ in late:
        _plate2(d, xy_, lab_, ls_, col_, anc_, avoid=avoid)
    for u, head, fade, col, r in heads_draw:   # 顔写真は最前面
        circle(d, head, r + 8 + 3 * math.sin(cx.t * 4), outline=col + (int(100 * fade),), w=2)
        circle(d, head, r + 4, fill=col + (int(255 * fade),))
        if u.get('portrait'):
            tmp = _portrait(u['portrait'], r).copy()
            if fade < 1:
                tmp.putalpha(tmp.getchannel('A').point(lambda v: int(v * fade)))
            L.alpha_composite(tmp, (int((head[0] - r) * S), int((head[1] - r) * S)))
        else:
            circle(d, head, r - 4, fill=(250, 248, 240, int(255 * fade)))
    for mk in it.get('marks', []):
        if not _vis(cx, mk):
            continue
        k = _fadein(T(cx, mk.get('at')), 0.4)
        x, y = P(mk['xy'])
        col = tuple(mk.get('col', (255, 90, 80)))
        poly(d, [(x - 14, y - 14), (x + 14, y + 14)], col + (int(255 * k),), 7)
        poly(d, [(x - 14, y + 14), (x + 14, y - 14)], col + (int(255 * k),), 7)
        if mk.get('label'):
            _plate2(d, (x + 22, y), mk['label'], mk.get('lsize', 24), col, 'lm', avoid=avoid)
    commit(im, L, [box[0] + px0, box[1] + py0, box[0] + px0 + mw, box[1] + py0 + mh], a)


DRAW_C = dict(battle_map=battle_map)
