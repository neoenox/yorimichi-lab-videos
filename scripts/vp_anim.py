"""自作のアニメーション部品（vp.py の spec から `dict(t='anim', name='...', box=[x0,y0,x1,y1], at=N, ...)` で呼ぶ）。
外部画像は使わない。すべて Pillow で描く（2倍で描いて縮小＝なめらか）。cx.t（場面内の秒）と cx.st[i]（文 i の開始秒）で動かす。
静脈の動画（vein）で初めて使った。図は定性的な模式図で、数値・縮尺は示さない。"""
import math
from PIL import Image, ImageDraw

F = FB = None
S = 2
BRIGHT = (224, 48, 58); DARK = (122, 20, 40); SKIN = (238, 196, 165); DERMIS = (226, 160, 140); FAT = (246, 226, 150)
VEINBLUE = (92, 140, 220); WHITE = (245, 243, 232); GOLD = (239, 201, 118); DIM = (190, 205, 208); BG = (7, 24, 36)


def bind(g):
    global F, FB, get_img
    F, FB = g['F'], g['FB']
    get_img = g.get('get_img')
    try:
        import vp_anim_pop as _pp
        _pp.bind(g)
    except ImportError:
        pass


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def ease(x):
    x = min(1, max(0, x))
    return x * x * (3 - 2 * x)


def vs(box, Z):
    """仮想キャンバスの大きさ（Z倍に拡大して、boxに貼る）"""
    return (box[2] - box[0]) / Z, (box[3] - box[1]) / Z


def layer(box, Z=1.0):
    w, h = vs(box, Z)
    L = Image.new('RGBA', (int(w * S), int(h * S)), (0, 0, 0, 0))
    return L, ImageDraw.Draw(L)


def commit(im, L, box, a):
    w, h = box[2] - box[0], box[3] - box[1]
    if a < 1:
        r, g, b, al = L.split()
        L = Image.merge('RGBA', (r, g, b, al.point(lambda v: int(v * a))))
    im.alpha_composite(L.resize((w, h), Image.LANCZOS), (box[0], box[1]))


def T(cx, i):
    """文 i が始まってからの秒（まだなら負）"""
    return cx.t - cx.st[i] if (i is not None and i < len(cx.st) and cx.on(i)) else -1.0


def text(d, xy, s, size, col=WHITE, anchor='la', serif=False, alpha=255):
    f = (FB if serif else F)[size * S]
    d.text((xy[0] * S, xy[1] * S), s, font=f, fill=tuple(col[:3]) + (alpha,), anchor=anchor)


def circle(d, c, r, fill=None, outline=None, w=0):
    d.ellipse(((c[0] - r) * S, (c[1] - r) * S, (c[0] + r) * S, (c[1] + r) * S), fill=fill, outline=outline, width=int(w * S))


def poly(d, pts, col, w):
    d.line([(x * S, y * S) for x, y in pts], fill=col, width=int(w * S), joint='curve')


def arrow_head(d, p, q, col, size=16):
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    pts = [(q[0], q[1]), (q[0] - size * math.cos(a - .45), q[1] - size * math.sin(a - .45)), (q[0] - size * math.cos(a + .45), q[1] - size * math.sin(a + .45))]
    d.polygon([(x * S, y * S) for x, y in pts], fill=col)


def path_len(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def path_at(pts, s):
    s = s % path_len(pts)
    for i in range(len(pts) - 1):
        l = math.dist(pts[i], pts[i + 1])
        if s <= l:
            f = s / l if l else 0
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)
        s -= l
    return pts[-1]


def moving_dots(d, pts, col, t, n=5, r=7, speed=140):
    L = path_len(pts)
    for k in range(n):
        p = path_at(pts, t * speed + k * L / n)
        circle(d, p, r, fill=col)


# ------------------------------------------------------------------ 前腕（手首の青っぽい筋）
def forearm(im, d0, cx, it, a):
    Z = 1.5; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    t = max(0, T(cx, it.get('lens_at', 99)))
    if not it.get('lens_only'):
        # 前腕（左から右へ、手首で細くなる）
        pts = [(60, 150), (560, 120), (820, 150), (820, 330), (560, 360), (60, 330)]
        d.polygon([(x * S, y * S) for x, y in pts], fill=SKIN + (255,))
        d.rounded_rectangle((760 * S, 150 * S, 900 * S, 330 * S), 40 * S, fill=SKIN + (255,))
        for sx, sy in ((520, 230), (610, 250), (700, 215)):
            pass
        # 青っぽい筋（皮膚の下の血管の見え方）
        for pts_ in ([(120, 215), (320, 205), (520, 235), (760, 225)], [(520, 235), (610, 262), (700, 292), (800, 296)], [(330, 207), (400, 180), (470, 172)]):
            poly(d, pts_, (120, 150, 200, 150), 14)
            poly(d, pts_, (96, 130, 190, 200), 6)
        text(d, (60, 36), '手首の内側などに見える、青っぽい筋', 34, DIM)
    # 拡大鏡（中身は？）
    if cx.on(it.get('lens_at', 99)):
        k = ease(t / 0.8)
        cxy = (940, 180); R = 135 * k
        circle(d, cxy, R + 10, fill=(14, 36, 52, 255), outline=GOLD + (255,), w=6)
        poly(d, [(cxy[0] - R * .7, cxy[1] + R * .72), (cxy[0] - R * .7 - 90, cxy[1] + R * .72 + 90)], GOLD + (255,), 12)
        if k > .6:
            text(d, cxy, '？', 150, GOLD, 'mm', serif=True)
            lab = '中を流れる血は、何色？'
            d.rounded_rectangle(((cxy[0] - R - 40 - 420) * S, (cxy[1] - 30) * S, (cxy[0] - R - 24) * S, (cxy[1] + 30) * S), 14 * S, fill=(8, 20, 32, 235))
            text(d, (cxy[0] - R - 40, cxy[1]), lab, 34, WHITE, 'rm')
    commit(im, L, box, a)


# ------------------------------------------------------------------ 赤血球・ヘモグロビン・酸素
def cell(d, c, R, col, fe=True, o2=0.0, label=None):
    circle(d, c, R, fill=col + (255,))
    circle(d, c, R * .56, fill=lerp(col, (0, 0, 0), .25) + (255,))
    circle(d, (c[0] - R * .35, c[1] - R * .45), R * .13, fill=lerp(col, (255, 255, 255), .35) + (200,))
    if fe:
        for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            p = (c[0] + dx * R * .22, c[1] + dy * R * .22)
            circle(d, p, R * .1, fill=(190, 195, 205, 255), outline=(235, 238, 245, 255), w=2)
    return


def o2(d, c, r=11, alpha=255):
    circle(d, (c[0] - r * .7, c[1]), r, fill=(150, 215, 255, alpha), outline=(235, 248, 255, alpha), w=2)
    circle(d, (c[0] + r * .7, c[1]), r, fill=(150, 215, 255, alpha), outline=(235, 248, 255, alpha), w=2)


def cells(im, d0, cx, it, a):
    Z = 1.25; box = it['box']; L, d = layer(box, Z)
    t1, t2, t4, t5 = T(cx, it.get('s1', 1)), T(cx, it.get('s2', 2)), T(cx, it.get('s4', 4)), T(cx, it.get('s5', 5))
    if t4 < 0:
        c = (480, 215); R = 150
        # 酸素が近づいて結びつく（文2）
        bind_p = ease((t2 - 1.0) / 2.0) if t2 >= 0 else 0.0
        col = lerp(DARK, BRIGHT, bind_p)
        if t1 >= 0:
            cell(d, c, R, col)
            text(d, (c[0], c[1] + R + 38), '赤血球', 34, WHITE, 'mm')
            text(d, (c[0] + R + 30, c[1] - 70), 'ヘモグロビン', 34, GOLD, 'la')
            poly(d, [(c[0] + R * .25, c[1] - R * .25), (c[0] + R + 22, c[1] - 52)], GOLD + (255,), 3)
            text(d, (c[0] + R + 30, c[1] + 10), '鉄（Fe）', 30, DIM, 'la')
        if t2 >= 0:
            for k in range(4):
                ang = k * math.pi / 2 + .6
                sx, sy = c[0] + math.cos(ang) * 360, c[1] + math.sin(ang) * 200
                tx, ty = c[0] + (-1 if k % 2 == 0 else 1) * R * .22, c[1] + (-1 if k < 2 else 1) * R * .22
                f = ease((t2 - 0.3) / 2.2)
                o2(d, (sx + (tx - sx) * f, sy + (ty - sy) * f), 12, int(255 * min(1, t2 / .5)))
            text(d, (c[0] + R + 30, c[1] + 70), '酸素（O2）が結びつく', 30, (150, 215, 255), 'la')
        if cx.on(it.get('s3', 3)):
            text(d, (box[2] - box[0] - 60, 60), 'この鉄が、血液を\n赤く見せている', 38, GOLD, 'ra')
    else:
        for c, col, n, lab, sub in (((380, 215), BRIGHT, 4, '酸素が多い → 明るい赤', '動脈の血（全身へ向かう）'), ((1060, 215), DARK, 1, '酸素が少ない → 暗い赤', '静脈の血（全身から戻る）')):
            k = ease(t4 / 0.8)
            cell(d, c, 120 * k, col)
            for j in range(n):
                ang = j * math.pi / 2 + .6
                o2(d, (c[0] + math.cos(ang) * 165, c[1] + math.sin(ang) * 100), 10, int(255 * k))
            text(d, (c[0], c[1] + 165), lab, 34, WHITE, 'mm', alpha=int(255 * k))
            if t5 >= 0:
                text(d, (c[0], c[1] + 210), sub, 30, GOLD, 'mm', alpha=int(255 * min(1, t5 / .6)))
        text(d, (720, 215), '⇄', 64, DIM, 'mm')
    commit(im, L, box, a)


# ------------------------------------------------------------------ 循環（心臓・組織・肺）
def heart(d, c, r):
    for dx in (-1, 1):
        circle(d, (c[0] + dx * r * .45, c[1] - r * .25), r * .55, fill=BRIGHT + (255,))
    d.polygon([((c[0] - r) * S, (c[1] - r * .05) * S), ((c[0] + r) * S, (c[1] - r * .05) * S), (c[0] * S, (c[1] + r * 1.15) * S)], fill=BRIGHT + (255,))


def loop_paths(ox, oy, k):
    P = lambda pts: [(ox + x * k, oy + y * k) for x, y in pts]
    return dict(
        art=P([(100, -40), (290, -150), (470, -90)]),     # 心臓 → 組織（動脈）
        vein=P([(470, 100), (290, 150), (100, 40)]),      # 組織 → 心臓（静脈）
        lung_out=P([(-100, 40), (-290, 150), (-470, 100)]),  # 心臓 → 肺
        pulm=P([(-470, -90), (-290, -150), (-100, -40)]),  # 肺 → 心臓（肺静脈）
    )


def loop_draw(d, ox, oy, k, mode, t, show_pulm=False, hl=False, labels=True, small=False, lungs=True):
    p = loop_paths(ox, oy, k)
    col_art = BRIGHT if mode == 'real' else (230, 70, 70)
    col_vein = DARK if mode == 'real' else VEINBLUE
    col_lo = DARK if mode == 'real' else VEINBLUE
    col_pu = BRIGHT if mode == 'real' else (230, 70, 70)
    for key, col in ((('art', col_art), ('vein', col_vein), ('lung_out', col_lo), ('pulm', col_pu)) if lungs else (('art', col_art), ('vein', col_vein))):
        w = 18 * k
        if key == 'pulm' and hl:
            poly(d, p[key], GOLD + (255,), w + 10 * k)
        poly(d, p[key], col + (255,), w)
        moving_dots(d, p[key], (255, 255, 255, 230), t, n=4, r=max(4, 6 * k), speed=150 * k)
    heart(d, (ox, oy), 70 * k)
    d.rounded_rectangle(((ox + 470 * k - 70 * k) * S, (oy - 60 * k) * S, (ox + 470 * k + 70 * k) * S, (oy + 90 * k) * S), 16 * S, fill=(40, 70, 95, 255), outline=(150, 175, 200, 255), width=3 * S)
    if lungs:
        circle(d, (ox - 470 * k, oy + 0), 78 * k, fill=(40, 70, 95, 255), outline=(150, 175, 200, 255), w=3)
    if labels:
        fs = 28 if not small else 22
        text(d, (ox + 470 * k, oy + 15 * k), '組織', fs, WHITE, 'mm')
        if lungs:
            text(d, (ox - 470 * k, oy + 0), '肺', fs, WHITE, 'mm')
        text(d, (ox, oy + 95 * k), '心臓', fs, WHITE, 'mm')


def loop(im, d0, cx, it, a):
    Z = 1.3; box = it['box']; L, d = layer(box, Z); t = cx.t
    VW, VH = vs(box, Z); ox, oy, k = VW / 2, VH / 2 + 10, 0.95
    ps = T(cx, it.get('s_pulm', 3))
    loop_draw(d, ox, oy, k, 'real', t, show_pulm=ps >= 0, hl=(ps >= 0 and ps < 40))
    p = loop_paths(ox, oy, k)
    text(d, p['art'][1], '動脈（全身へ）', 30, WHITE, 'ms') if False else None
    text(d, (ox + 290 * k, oy - 175 * k), '動脈：全身へ', 30, WHITE, 'mm')
    text(d, (ox + 290 * k, oy + 178 * k), '静脈：全身から戻る', 30, WHITE, 'mm')
    text(d, (ox - 290 * k, oy + 178 * k), '肺へ', 30, WHITE, 'mm')
    c = GOLD if ps >= 0 else WHITE
    text(d, (ox - 290 * k, oy - 175 * k), '肺静脈：肺から戻る', 30, c, 'mm')
    if ps >= 0:
        text(d, (ox - 290 * k, oy - 215 * k), '酸素が多い（明るい赤）', 28, GOLD, 'mm')
    commit(im, L, box, a)


# ------------------------------------------------------------------ 皮膚の断面と光（模式図）
def skin(im, d0, cx, it, a):
    Z = 1.25; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    t_red = T(cx, it.get('s_red', 4)); t_blue = T(cx, it.get('s_blue', 5)); t_view = T(cx, it.get('s_view', 6))
    x0, x1 = 100, W - 100
    ys = 120
    d.rectangle((x0 * S, ys * S, x1 * S, (ys + 30) * S), fill=SKIN + (255,))                 # 表皮
    d.rectangle((x0 * S, (ys + 30) * S, x1 * S, (ys + 160) * S), fill=DERMIS + (255,))         # 真皮
    d.rectangle((x0 * S, (ys + 160) * S, x1 * S, (ys + 300) * S), fill=FAT + (255,))           # 脂肪
    text(d, (x0 + 10, ys + 36), '皮膚', 28, (90, 40, 30), 'la'); text(d, (x0 + 10, ys + 166), '脂肪', 28, (110, 90, 20), 'la')
    vc = (W * 0.66, ys + 232); vr = 46
    circle(d, vc, vr, fill=DARK + (255,), outline=(60, 10, 20, 255), w=3)
    text(d, (vc[0], vc[1]), '血', 32, (255, 220, 220), 'mm', serif=True)
    text(d, (vc[0] + vr + 18, vc[1]), '静脈（中の血は暗い赤）', 30, (90, 60, 10), 'lm')
    ex, ey = W * 0.05, 66
    circle(d, (ex, ey), 26, fill=(245, 245, 245, 255), outline=(200, 200, 200, 255), w=3); circle(d, (ex, ey), 11, fill=(40, 40, 60, 255))
    text(d, (ex + 38, ey + 4), '見る人', 26, DIM, 'lm')
    if t_red >= 0:   # 赤い光：深くまで届く
        for i in range(4):
            xs = W * (0.46 + i * 0.07)
            f = ease((t_red - i * .15) / 2.0)
            ytop = 34; ydown = ys + 270
            yy = ytop + (ydown - ytop) * f
            pts = [(xs, ytop)]
            for yk in range(int(ytop) + 26, int(yy), 26):
                pts.append((xs + (7 if (yk // 26) % 2 else -7), yk))
            pts.append((xs, yy))
            poly(d, pts, (255, 110, 110, 255), 5)
        text(d, (W * 0.52, 6), '赤い光：深くまで届く', 28, (255, 140, 140), 'la')
    if t_blue >= 0:  # 青い光：浅いところで多くが戻る
        for i in range(4):
            xs = W * (0.18 + i * 0.05)
            f = ease((t_blue - i * .15) / 1.0)
            ytop = 34; yhit = ys + 16
            yy = ytop + (yhit - ytop) * min(1, f * 2)
            poly(d, [(xs, ytop), (xs + 16 * min(1, f * 2), yy)], (110, 170, 255, 255), 5)
            if f > .5:
                r = (f - .5) * 2
                poly(d, [(xs + 16, yhit), (xs + 16 + 50 * r, yhit - (yhit - 70) * r * 0.9)], (110, 170, 255, 255), 5)
        text(d, (W * 0.16, 6), '青い光：浅く入り、多くが戻る', 28, (130, 180, 255), 'la')
    if t_view >= 0:
        text(d, (W / 2, ys + 322), '光の入り方の違いで、明るい肌では静脈が青っぽく見える（と説明されている）', 30, GOLD, 'mm')
    text(d, (W - 10, H - 4), '※光の入り方の深さの違いを示す模式図（実際の光の経路ではありません）', 26, DIM, 'rs')
    commit(im, L, box, a)


# ------------------------------------------------------------------ 肌の色と見え方
def skintone(im, d0, cx, it, a):
    Z = 1.2; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    t = T(cx, it.get('at', 0))
    for i, (tone, lab, vis) in enumerate(((SKIN, '明るい肌', 1.0), ((140, 92, 66), '濃い肌', 0.35))):
        cx0 = W * (0.25 + 0.5 * i); cy0 = 210
        d.rounded_rectangle(((cx0 - 220) * S, (cy0 - 130) * S, (cx0 + 220) * S, (cy0 + 130) * S), 30 * S, fill=tone + (255,))
        vcol = (120, 150, 200) if i == 0 else lerp((140, 92, 66), (110, 120, 150), .35)
        poly(d, [(cx0 - 180, cy0 + 10), (cx0 - 60, cy0 - 20), (cx0 + 60, cy0 + 20), (cx0 + 180, cy0 - 10)], vcol + (int(255 * ease(t / .8) * 1),), 14)
        text(d, (cx0, cy0 + 170), lab, 34, WHITE, 'mm')
        text(d, (cx0, cy0 + 215), '静脈が見えやすい' if i == 0 else '静脈が目立ちにくい', 28, GOLD if i == 0 else DIM, 'mm')
    commit(im, L, box, a)


def contrast(im, d0, cx, it, a):
    """同じ色の帯でも、周りの色で見え方が変わる（定性的な例）"""
    Z = 1.2; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    t = T(cx, it.get('at', 0)); k = ease(t / .8)
    bar = (130, 110, 150)
    for i, (bg, lab) in enumerate(((SKIN, '明るい背景'), ((70, 45, 35), '暗い背景'))):
        x = 60 + i * (W / 2)
        d.rounded_rectangle((x * S, 20 * S, (x + W / 2 - 80) * S, 230 * S), 24 * S, fill=lerp(BG, bg, k) + (255,))
        d.rounded_rectangle(((x + 60) * S, 105 * S, (x + W / 2 - 140) * S, 145 * S), 20 * S, fill=bar + (255,))
        text(d, (x + (W / 2 - 80) / 2, 262), lab, 30, WHITE, 'mm')
    text(d, (W / 2, 320), '同じ色の帯でも、周りの色で見え方が変わる（例）', 30, GOLD, 'mm')
    commit(im, L, box, a)


# ------------------------------------------------------------------ 教科書の図と実際の色
def textbook(im, d0, cx, it, a):
    Z = 1.3; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    t = cx.t
    k = 0.55
    s_legend, s_real = T(cx, it.get('s_legend', 1)), T(cx, it.get('s_real', 2))
    loop_draw(d, W * 0.27, 215, k, 'book', t, labels=True, small=True, lungs=False)
    text(d, (W * 0.27, 20), '教科書の図（全身の循環。色は区別のため）', 30, WHITE, 'mm')
    if s_legend >= 0:
        d.rounded_rectangle((W * 0.06 * S, 350 * S, W * 0.47 * S, 420 * S), 14 * S, fill=(12, 34, 50, 255), outline=GOLD + (255,), width=3 * S)
        circle(d, (W * 0.09, 385), 12, fill=VEINBLUE + (255,)); text(d, (W * 0.11, 385), '青＝静脈（動脈と区別する色）', 28, WHITE, 'lm')
    if s_real >= 0:
        kk = ease(s_real / .8)
        loop_draw(d, W * 0.73, 215, k, 'real', t, labels=True, small=True, lungs=False)
        text(d, (W * 0.73, 20), '実際の血の色', 32, GOLD, 'mm')
        d.rounded_rectangle((W * 0.53 * S, 350 * S, W * 0.94 * S, 420 * S), 14 * S, fill=(12, 34, 50, 255), outline=GOLD + (255,), width=3 * S)
        circle(d, (W * 0.56, 385), 12, fill=DARK + (255,)); text(d, (W * 0.58, 385), '全身から戻る静脈の血：暗い赤', 28, WHITE, 'lm')
    commit(im, L, box, a)


# ------------------------------------------------------------------ 偏角（真北と磁北のなす角）
def _arrow(d, o, ang_deg, length, col, w=8, k=1.0):
    """上向きを0度、西（左）へ正の角度で傾ける"""
    a = math.radians(ang_deg)
    e = (o[0] - math.sin(a) * length * k, o[1] - math.cos(a) * length * k)
    poly(d, [o, e], col, w)
    if k > .98:
        arrow_head(d, o, e, col, 26)
    return e


def decl_one(d, o, L, theta, k_true, k_mag, k_arc, lab_theta, big=True, tsize=30):
    if k_true > 0:
        e = _arrow(d, o, 0, L, GOLD + (255,), 8, k_true)
        if k_true > .9:
            text(d, (e[0], e[1] - 16), '真北', tsize, GOLD, 'mb')
    if k_mag > 0:
        e = _arrow(d, o, theta, L, (150, 215, 255, 255), 8, k_mag)
        if k_mag > .9:
            text(d, (e[0] - 10, e[1] - 16), '磁北', tsize, (150, 215, 255), 'rb')
    if k_arc > 0:
        r = L * 0.55
        n = 30
        pts = [(o[0] - math.sin(math.radians(theta * i / n)) * r, o[1] - math.cos(math.radians(theta * i / n)) * r) for i in range(int(n * k_arc) + 1)]
        if len(pts) > 1:
            poly(d, pts, (255, 255, 255, 255), 5)
        if k_arc > .9:
            text(d, (o[0] - r * 0.95, o[1] - r * 1.12), lab_theta, tsize, WHITE, 'rb')
    circle(d, o, 9, fill=WHITE + (255,))


def declination(im, d0, cx, it, a):
    Z = 1.25; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    kt = ease(T(cx, it.get('s_true', 2)) / 0.9) if T(cx, it.get('s_true', 2)) >= 0 else 0
    km = ease(T(cx, it.get('s_mag', 3)) / 0.9) if T(cx, it.get('s_mag', 3)) >= 0 else 0
    ka = ease(T(cx, it.get('s_arc', 4)) / 0.9) if T(cx, it.get('s_arc', 4)) >= 0 else 0
    decl_one(d, (W * 0.5, H - 70), H - 170, 26, kt, km, ka, '偏角', tsize=34)
    text(d, (W * 0.5, H - 28), '※角度は強調した模式図（西へずれる例）', 24, DIM, 'mm')
    commit(im, L, box, a)


def declination2(im, d0, cx, it, a):
    Z = 1.25; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    t = max(0.0, T(cx, it.get('at', 3)))
    k = ease(t / 0.9)
    for i, (name, ang) in enumerate((('札幌', 10), ('那覇', 6))):
        o = (W * (0.27 + 0.46 * i), H - 90)
        decl_one(d, o, H - 190, ang, 1.0 * k, 1.0 * k, k if t > 0.9 else 0, f'約{ang}度', tsize=30)
        text(d, (o[0], H - 40), f'{name}：西へ約{ang}度', 34, WHITE, 'mm')
    text(d, (W / 2, H - 6), '※2020年の磁気図（国土地理院）。角度は実際の大きさ', 22, DIM, 'ms')
    commit(im, L, box, a)


# ------------------------------------------------------------------ 北極側から見た、北極点と磁極の位置（模式図）
def polar(im, d0, cx, it, a):
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    c = (W / 2, H / 2 + 6); kdeg = (min(W, H) / 2 - 50) / 10.5
    for colat, lab in ((5, '北緯85度'), (10, '北緯80度')):
        circle(d, c, colat * kdeg, outline=(120, 150, 175, 255), w=2)
        text(d, (c[0] + 6, c[1] - colat * kdeg - 4), lab, 22, DIM, 'ls')
    for ang in range(0, 360, 45):
        r = 10.5 * kdeg
        poly(d, [c, (c[0] + r * math.sin(math.radians(ang)), c[1] - r * math.cos(math.radians(ang)))], (70, 95, 115, 255), 1)
    for lon, lab in ((139.298, '東経139度'), (-72.76, '西経73度')):
        r = 10.5 * kdeg
        e = (c[0] + r * math.sin(math.radians(lon)), c[1] - r * math.cos(math.radians(lon)))
        poly(d, [c, e], (110, 140, 165, 255), 2)
        text(d, (e[0], e[1] + (18 if lon > 0 else -18)), lab, 22, DIM, 'mm')
    t_c, t_m, t_l, t_g = T(cx, it.get('s_center', 2)), T(cx, it.get('s_mag', 1)), T(cx, it.get('s_line', 3)), T(cx, it.get('s_geo', 6))
    mp = (c[0] + 4.238 * kdeg * math.sin(math.radians(139.298)), c[1] - 4.238 * kdeg * math.cos(math.radians(139.298)))
    gp = (c[0] + 9.15 * kdeg * math.sin(math.radians(-72.76)), c[1] - 9.15 * kdeg * math.cos(math.radians(-72.76)))
    if t_c >= 0:
        circle(d, c, 9, fill=GOLD + (255,)); text(d, (c[0], c[1] - 24), '北極点（北緯90度）', 28, GOLD, 'mb')
    if t_m >= 0:
        k = ease(t_m / 0.6)
        circle(d, mp, 14 * k, fill=(150, 215, 255, 255), outline=WHITE + (255,), w=2)
        text(d, (mp[0] + 20, mp[1] + 4), '北の磁極' + chr(10) + '（2025年のモデル）', 28, (150, 215, 255), 'la')
    if t_l >= 0:
        poly(d, [c, mp], (255, 255, 255, 255), 3)
        text(d, ((c[0] + mp[0]) / 2 - 22, (c[1] + mp[1]) / 2 + 30), '約470 km', 28, WHITE, 'rm')
    if t_g >= 0:
        k = ease(t_g / 0.6)
        circle(d, gp, 14 * k, fill=(255, 170, 120, 255), outline=WHITE + (255,), w=2)
        text(d, (gp[0] - 14, gp[1] - 100), '地磁気極' + chr(10) + '（双極子モデル）', 28, (255, 170, 120), 'la')
        poly(d, [gp, (gp[0] - 4, gp[1] - 52)], (255, 170, 120, 255), 2)
    text(d, (W / 2, H - 14), '※北極側から見た模式図（位置関係は概略）', 22, DIM, 'ms')
    commit(im, L, box, a)


# ------------------------------------------------------------------ 公転と地軸の傾き（地球が太陽の周りを回る）
def orbit(im, d0, cx, it, a):
    Z = 0.95; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    show_axis = it.get('axis', False); show_dist = it.get('dist', False); show_hemi = it.get('hemi', False)
    R = min(W, H) / 2 - 92
    c0 = (W / 2, H / 2 + 8)
    sun = (c0[0] + R * 0.03, c0[1])      # 軌道はほぼ円（太陽が、わずかに右へずれる）
    circle(d, c0, R, outline=(120, 150, 180, 255), w=3)
    for r_, al in ((70, 60), (56, 110), (44, 255)):
        circle(d, sun, r_, fill=(255, 190, 60, al))
    circle(d, sun, 40, fill=(255, 215, 90, 255))
    text(d, (sun[0], sun[1] + 66), '太陽', 26, WHITE, 'mm')
    # 4つの位置（左＝6月ごろ、右＝12月ごろ、下＝3月、上＝9月）
    spots = {'6月ごろ': (c0[0] - R, c0[1]), '12月ごろ': (c0[0] + R, c0[1]), '3月ごろ': (c0[0], c0[1] + R), '9月ごろ': (c0[0], c0[1] - R)}
    tilt = math.radians(23.4)
    for name, p in spots.items():
        lit = (255, 255, 255, 255)
        circle(d, p, 26, fill=(70, 130, 200, 255), outline=(200, 225, 255, 255), w=2)
        if show_axis:
            # 地軸：どの位置でも同じ向き（右へ傾く）。北極側を黄色で示す
            ax = (math.sin(tilt) * 52, -math.cos(tilt) * 52)
            poly(d, [(p[0] - ax[0], p[1] - ax[1]), (p[0] + ax[0], p[1] + ax[1])], (255, 255, 255, 255), 4)
            circle(d, (p[0] + ax[0], p[1] + ax[1]), 7, fill=GOLD + (255,))
        pos = (p[0], p[1] + 56) if name in ('3月ごろ',) else ((p[0], p[1] - 62) if name == '9月ごろ' else (p[0], p[1] + 58))
        text(d, pos, name, 26, WHITE, 'mm')
    if show_hemi:
        text(d, (c0[0] - R, c0[1] - 76), '北半球：夏', 28, (255, 170, 90), 'mm')
        text(d, (c0[0] + R, c0[1] - 76), '北半球：冬', 28, (150, 200, 255), 'mm')
        text(d, (c0[0] - R, c0[1] + 96), '南半球：冬', 28, (150, 200, 255), 'mm')
        text(d, (c0[0] + R, c0[1] + 96), '南半球：夏', 28, (255, 170, 90), 'mm')
    if show_dist:
        text(d, (c0[0] - R, c0[1] + 96), '遠日点（7月）', 28, (150, 215, 255), 'mm')
        text(d, (c0[0] + R, c0[1] + 96), '近日点（1月）', 28, (255, 170, 90), 'mm')
        text(d, (W / 2, 10), '※軌道はほぼ円（図は、距離の差をわずかに誇張）', 24, DIM, 'mt')
    commit(im, L, box, a)


# ------------------------------------------------------------------ 太陽の高さと、同じ幅の光が当たる面積
def sunangle(im, d0, cx, it, a):
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    t = cx.t
    for i, (ang, title, col) in enumerate(((78, '夏至のころ：高さ 約78度', (255, 170, 90)), (32, '冬至のころ：高さ 約32度', (150, 200, 255)))):
        ox = W * (0.25 + 0.5 * i); gy = H - 110
        d.rectangle(((ox - 230) * S, gy * S, (ox + 230) * S, (gy + 16) * S), fill=(110, 90, 70, 255))
        text(d, (ox, 22), title, 30, col, 'mm')
        a_ = math.radians(ang); dx, dy = -math.cos(a_), math.sin(a_)   # 光の進む向き（下向き）
        bw = 120.0
        # 同じ幅(bw)の光の束を、地面に垂直な幅で描く：地面上の幅は bw / sin(高度)
        foot = bw / math.sin(a_)
        hx = ox; hy = gy
        for k in range(5):
            off = (k - 2) * bw / 4
            # 光線（地面の点 (hx + off', gy) へ向かう）
            px = (k - 2) * foot / 4
            end = (hx + px, gy)
            start = (end[0] - dx * 380, end[1] - dy * 380)
            poly(d, [start, end], (255, 235, 150, 230), 4)
            for m in range(4):
                s_ = ((t * 150 + m * 95) % 380)
                q = (start[0] + dx * s_, start[1] + dy * s_)
                circle(d, q, 7, fill=(255, 250, 200, 255))
        poly(d, [(hx - foot / 2, gy - 4), (hx + foot / 2, gy - 4)], col + (255,), 10)
        text(d, (ox, gy + 50), f'地面で、光が広がる幅：{foot / bw:.1f}倍', 28, col, 'mm')
    text(d, (W / 2, H - 10), '※同じ幅の光の束（光の量は同じ）。大気は無視した模式図', 24, DIM, 'ms')
    commit(im, L, box, a)


# ------------------------------------------------------------------ 月の満ち欠けと、閏月（旧暦）
def moon(d, c, r, p, col=(235, 228, 190)):
    """p: 0=新月, 0.25=上弦, 0.5=満月, 0.75=下弦。簡単な描き分け"""
    circle(d, c, r, fill=(40, 52, 75, 255), outline=(120, 135, 160, 255), w=2)
    q = p if p <= 0.5 else 1 - p
    k = math.cos(2 * math.pi * q)
    pts = [(c[0] + r * math.cos(math.radians(f)), c[1] + r * math.sin(math.radians(f))) for f in range(-90, 91, 6)]
    pts += [(c[0] + k * r * math.cos(math.radians(f)), c[1] + r * math.sin(math.radians(f))) for f in range(90, -91, -6)]
    if p > 0.5:
        pts = [(2 * c[0] - x, y) for x, y in pts]
    if q > 0.001:
        d.polygon([(x * S, y * S) for x, y in pts], fill=col + (255,))


def lunar(im, d0, cx, it, a):
    """12か月＋閏月の帯。月の満ち欠け（約29.5日）が12回で約354日、季節の1年（約365日）とずれるので、閏月を足す"""
    Z = 1.1; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    t12, t13 = T(cx, it.get('s_cycle', 1)), T(cx, it.get('s_leap', 3))
    n = 13 if t13 >= 0 else 12
    gap = (W - 120) / 13.0; r = min(gap * 0.38, 46)
    y = H * 0.42
    for i in range(12):
        k = ease((t12 - i * 0.12) / 0.5) if t12 >= 0 else 0
        if k <= 0:
            continue
        c = (60 + gap * (i + 0.5), y)
        moon(d, c, r * k, 0.5)
        text(d, (c[0], y + r + 26), f'{i + 1}', 24, DIM, 'mm')
    if t13 >= 0:
        k = ease(t13 / 0.8)
        c = (60 + gap * 12.5, y)
        circle(d, c, r * 1.25 * k, outline=GOLD + (255,), w=4)
        moon(d, c, r * k, 0.5)
        text(d, (c[0], y + r + 26), '閏月', 26, GOLD, 'mm')
    if t12 >= 0:
        text(d, (60 + gap * 6, H * 0.14), '月の満ち欠け（約29.5日）× 12か月 ＝ 約354日', 32, WHITE, 'mm')
        text(d, (60 + gap * 6, H * 0.78), '季節の1年は約365日 → 2〜3年に1度、閏月を入れて13か月の年に', 30, GOLD if t13 >= 0 else DIM, 'mm')
    commit(im, L, box, a)


# ------------------------------------------------------------------ 日付タイル（明治5年12月の日付と、西暦の対応）
def caltiles(im, d0, cx, it, a):
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    s1, s2, s3, s4 = T(cx, it.get('s_a', 4)), T(cx, it.get('s_b', 5)), T(cx, it.get('s_c', 6)), T(cx, it.get('s_skip', 7))
    tw_, th_ = 270, 270
    gap = 60
    x0 = (W - (4 * tw_ + 3 * gap)) / 2
    tiles = [('明治5年', '12月1日', '1872年12月30日', s1, False), ('明治5年', '12月2日', '1872年12月31日', s2, False),
             ('（旧暦のままなら）', '12月3日', '使われなかった日付', s4, True), ('明治6年', '1月1日', '1873年1月1日', s3, False)]
    for i, (era, jp, west, t, skip) in enumerate(tiles):
        if t < 0:
            continue
        k = ease(t / 0.6)
        x = x0 + i * (tw_ + gap); y = 30 + (1 - k) * 40
        fill = (245, 240, 225, int(255 * k)) if not skip else (60, 70, 90, int(255 * k))
        d.rounded_rectangle((x * S, y * S, (x + tw_) * S, (y + th_) * S), 22 * S, fill=fill, outline=(GOLD if not skip else DIM) + (int(255 * k),), width=4 * S)
        d.rectangle((x * S, y * S, (x + tw_) * S, (y + 70) * S), fill=((200, 70, 70, int(255 * k)) if not skip else (90, 100, 120, int(255 * k))))
        text(d, (x + tw_ / 2, y + 36), era, 26, WHITE, 'mm', alpha=int(255 * k))
        text(d, (x + tw_ / 2, y + 160), jp, 52 if not skip else 44, (50, 40, 40) if not skip else DIM, 'mm', serif=True, alpha=int(255 * k))
        text(d, (x + tw_ / 2, y + 225), west, 24, (70, 60, 60) if not skip else DIM, 'mm', alpha=int(255 * k))
        if skip:
            poly(d, [(x + 20, y + th_ - 20), (x + tw_ - 20, y + 90)], (230, 100, 100, int(255 * k)), 6)
    commit(im, L, box, a)


# ------------------------------------------------------------------ 降水確率（rain30）
def _drop(d, x, y, r, col=(120, 190, 255, 255)):
    d.polygon([(x * S, (y - r * 1.5) * S), ((x - r) * S, (y + r * 0.3) * S), ((x + r) * S, (y + r * 0.3) * S)], fill=col)
    circle(d, (x, y + r * 0.3), r, fill=col)


def rain100(im, d0, cx, it, a):
    """100回の同じ予報を並べ、pct 回に『1ミリ以上の降水あり』の印がつく（自作の模式図。実際の観測ではない）。"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    pct = it.get('pct', 30)
    s0, s1 = T(cx, it.get('s_a', 0)), T(cx, it.get('s_b', 1))
    # 配置は決まった疑似乱数（pct 個を、10x10の格子の中にばらけて置く）
    idx = sorted(range(100), key=lambda k: (k * 37 + 11) % 101)[:pct]
    rainy = set(idx)
    cell = min((W - 40) / 10, (H - 150) / 10)
    gx0 = (W - cell * 10) / 2; gy0 = 70
    text(d, (W / 2, 28), f'同じ「{pct}％」の予報が、100回出されたとき（自作の模式図）', 38, GOLD, 'mm')
    for k in range(100):
        r_, c_ = divmod(k, 10)
        x = gx0 + c_ * cell + cell / 2; y = gy0 + r_ * cell + cell / 2
        tk = s0 - k * 0.012
        if tk < 0:
            continue
        kk = ease(tk / 0.25)
        circle(d, (x, y), cell * 0.36 * kk, fill=(60, 78, 100, 255), outline=(120, 140, 160, 255), w=2)
        if k in rainy and s1 >= 0:
            kk2 = ease((s1 - (list(sorted(rainy)).index(k)) * 0.05) / 0.3)
            if kk2 > 0:
                _drop(d, x, y, cell * 0.22 * kk2)
    if s1 >= 0:
        text(d, (W / 2, H - 38), f'およそ {pct} 回で、1ミリ以上の降水がある（実際の観測結果ではありません）', 34, (150, 205, 255), 'mm')
    commit(im, L, box, a)


def blocks6(im, d0, cx, it, a):
    """1日を6時間ごとに区切る（気象庁：6時間ごとに10％単位で発表）。18時〜24時を強調。"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    s0, s1 = T(cx, it.get('s_a', 1)), T(cx, it.get('s_b', 2))
    bw = (W - 80) / 4; y0 = 120; h = 150
    for i, lab in enumerate(('0時〜6時', '6時〜12時', '12時〜18時', '18時〜24時')):
        if s0 < 0:
            break
        k = ease((s0 - i * 0.15) / 0.4)
        x = 40 + i * bw
        hi = (i == 3 and s1 >= 0)
        d.rounded_rectangle((x * S, y0 * S, (x + bw - 16) * S, (y0 + h) * S), 16 * S, fill=((70, 110, 160, int(255 * k)) if hi else (45, 62, 84, int(255 * k))),
                            outline=(GOLD if hi else (120, 140, 160)) + (int(255 * k),), width=3 * S)
        text(d, (x + (bw - 16) / 2, y0 + 40), lab, 38, WHITE, 'mm', alpha=int(255 * k))
        if hi:
            text(d, (x + (bw - 16) / 2, y0 + 100), '例：20％', 46, GOLD, 'mm')
    if s0 >= 0:
        text(d, (W / 2, 60), '降水確率は、6時間ごとに、10％単位で発表（気象庁）', 38, WHITE, 'mm')
    if s1 >= 0:
        text(d, (W / 2, y0 + h + 60), '20％の予報が100回出されたとき、およそ20回は、1ミリ以上の雨が降る', 38, (150, 205, 255), 'mm')
    commit(im, L, box, a)


def areapoint(im, d0, cx, it, a):
    """『地域の30％の面積で降る』ではなく『どの点でも同じ確率』（気象庁の定義）の対比。自作の模式図。"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    sa, sb = T(cx, it.get('s_a', 1)), T(cx, it.get('s_b', 0))
    pw = (W - 120) / 2; py0 = 90; ph = H - 220
    # 左：面積（誤解）
    for i in range(2):
        x0 = 40 + i * (pw + 40)
        d.rounded_rectangle((x0 * S, py0 * S, (x0 + pw) * S, (py0 + ph) * S), 18 * S, fill=(50, 66, 88, 255), outline=(150, 165, 185, 255), width=3 * S)
    text(d, (40 + pw / 2, 40), '地域の30％の面積で降る？', 38, (255, 170, 120), 'mm')
    text(d, (40 + pw + 40 + pw / 2, 40), '気象庁の定義：どの点でも、同じ確率', 38, (150, 205, 255), 'mm')
    if sa >= 0:
        k = ease(sa / 0.8)
        d.rectangle((40 * S, py0 * S, (40 + pw * 0.3 * k) * S, (py0 + ph) * S), fill=(100, 160, 230, 190))
        text(d, (40 + pw / 2, py0 + ph + 36), '面積の話ではありません', 34, (255, 170, 120), 'mm')
        if k > 0.9:
            poly(d, [(40 + 40, py0 + 40), (40 + pw - 40, py0 + ph - 40)], (235, 90, 80, 255), 8)
            poly(d, [(40 + pw - 40, py0 + 40), (40 + 40, py0 + ph - 40)], (235, 90, 80, 255), 8)
    if sb >= 0:
        k = ease(sb / 0.8)
        x0 = 40 + pw + 40
        for r_ in range(6):
            for c_ in range(8):
                x = x0 + 50 + c_ * (pw - 100) / 7; y = py0 + 50 + r_ * (ph - 100) / 5
                circle(d, (x, y), 15 * k, fill=(120, 190, 255, 255))
        text(d, (x0 + pw / 2, py0 + ph + 36), 'どの点でも「30％」（降る可能性）', 34, (150, 205, 255), 'mm')
    commit(im, L, box, a)


def onemm(im, d0, cx, it, a):
    """降水量の多少は示さない：弱い雨も強い雨も、『1ミリ以上』なら同じ『あり』。例の量は自作の例。"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    s0, s1 = T(cx, it.get('s_a', 0)), T(cx, it.get('s_b', 2))
    colw = (W - 160) / 2
    items = [('弱い雨の例：1ミリ', 1), ('強い雨の例：30ミリ', 12)]
    for i, (lab, n) in enumerate(items):
        if s0 < 0:
            break
        k = ease((s0 - i * 0.3) / 0.5)
        x0 = 60 + i * (colw + 40)
        d.rounded_rectangle((x0 * S, 70 * S, (x0 + colw) * S, (H - 160) * S), 18 * S, fill=(40, 56, 78, int(255 * k)), outline=(120, 140, 160, int(255 * k)), width=3 * S)
        text(d, (x0 + colw / 2, 40), lab, 38, WHITE, 'mm', alpha=int(255 * k))
        for j in range(n):
            x = x0 + 60 + (j % 6) * (colw - 120) / 5; y = 130 + (j // 6) * 90 + ((cx.t * 70 + j * 37) % 60 if k > 0.9 else 0)
            _drop(d, x, min(y, H - 190), 14 * k)
        if s1 >= 0:
            text(d, (x0 + colw / 2, H - 120), '1ミリ以上 → 「降水あり」', 34, (150, 205, 255), 'mm', alpha=int(255 * ease(s1 / 0.5)))
    if s1 >= 0:
        text(d, (W / 2, H - 50), '降水確率は、量の多さを示しません（気象庁）', 38, GOLD, 'mm')
    commit(im, L, box, a)


def calib(im, d0, cx, it, a):
    """予報の検証の考え方：横軸＝予報した確率、縦軸＝実際の出現率。理想は傾き1の直線（自作の模式図）。実際の検証結果ではない。"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    s0, s1 = T(cx, it.get('s_a', 0)), T(cx, it.get('s_b', 1))
    ox, oy = 270, H - 130; aw = W - 440; ah = H - 220
    d.line([(ox * S, oy * S), ((ox + aw) * S, oy * S)], fill=(200, 210, 220, 255), width=3 * S)
    d.line([(ox * S, oy * S), (ox * S, (oy - ah) * S)], fill=(200, 210, 220, 255), width=3 * S)
    text(d, (ox + aw / 2, oy + 70), '予報した降水確率（10％刻み）', 34, WHITE, 'mm')
    text(d, (ox - 30, oy - ah / 2), '実際の出現率', 32, WHITE, 'rm')
    for k in range(0, 11, 2):
        x = ox + aw * k / 10
        text(d, (x, oy + 28), f'{k * 10}％', 28, DIM, 'mm')
        y = oy - ah * k / 10
        text(d, (ox - 10, y), f'{k * 10}％', 28, DIM, 'rm')
    if s0 >= 0:
        k = ease(s0 / 1.0)
        x1 = ox + aw * k; y1 = oy - ah * k
        poly(d, [(ox, oy), (x1, y1)], (255, 205, 110, 255), 6)
    if s1 >= 0:
        for j in range(1, 11):
            kk = ease((s1 - j * 0.12) / 0.3)
            if kk > 0:
                circle(d, (ox + aw * j / 10, oy - ah * j / 10), 10 * kk, fill=(150, 205, 255, 255))
        text(d, (ox + aw * 0.28, oy - ah * 0.8), '理想は、予報値＝出現率（傾き1の直線）', 34, GOLD, 'mm')
    text(d, (W / 2, 22), '自作の模式図（実際の検証結果ではありません）', 28, DIM, 'mm')
    commit(im, L, box, a)



# ------------------------------------------------------------------ 月の自転と公転（moon）
def moonsync(im, d0, cx, it, a):
    """月が地球を公転しながら自転する模式図（自作）。mode: 'spin'（自転する月）／'nospin'（自転しない月）／'both'（左右に並べる）／'daynight'（太陽光と昼夜）。
    月面の赤い印は『地球に向いている側』の目印。縮尺・距離は示さない。"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    mode = it.get('mode', 'both')
    t0 = max(0.0, cx.t - 0.3)

    def panel(ox, oy, R, rot, title, col, show_sun=False):
        # 地球
        circle(d, (ox, oy), 66, fill=(70, 120, 200, 255), outline=(150, 190, 240, 255), w=3)
        text(d, (ox, oy + 100), '地球', 36, (170, 200, 240), 'mm')
        # 軌道
        circle(d, (ox, oy), R, outline=(110, 125, 145, 255), w=2)
        phi = t0 * 0.9
        mx, my = ox + R * math.cos(phi), oy - R * math.sin(phi)
        mr = 56
        circle(d, (mx, my), mr, fill=(222, 214, 190, 255), outline=(250, 245, 225, 255), w=2)
        if show_sun:
            # 太陽光は左から。光が当たらない側（右側）を暗くする
            d.pieslice(((mx - mr) * S, (my - mr) * S, (mx + mr) * S, (my + mr) * S), -90, 90, fill=(30, 38, 56, 235))
        th = rot(phi)
        px, py = mx + mr * 0.78 * math.cos(th), my - mr * 0.78 * math.sin(th)
        circle(d, (px, py), 16, fill=(235, 80, 70, 255), outline=(255, 235, 230, 255), w=2)
        text(d, (ox, oy - R - 40), title, 38, col, 'mm')

    if mode == 'both':
        R = min(W / 4 - 90, H / 2 - 130)
        panel(W * 0.25, H / 2 + 20, R, lambda phi: phi + math.pi, '自転する月（同じ面が地球を向く）', (150, 205, 255))
        panel(W * 0.75, H / 2 + 20, R, lambda phi: 0.0, 'もし、自転しない月なら', (255, 190, 130))
        text(d, (W / 2, H - 24), '赤い印：月面の、ある一か所（自作の模式図。縮尺は実際と異なります）', 32, DIM, 'mm')
    elif mode == 'daynight':
        R = min(W / 2 - 260, H / 2 - 130)
        # 太陽光
        for k in range(5):
            y = H / 2 + (k - 2) * 90
            poly(d, [(30, y), (150, y)], (255, 235, 150, 255), 5)
        text(d, (90, H / 2 - 220), '太陽光', 34, (255, 235, 150), 'mm')
        panel(W / 2 + 60, H / 2 + 20, R, lambda phi: phi + math.pi, '月は自転しながら公転（暗くなる側が入れ替わる）', (150, 205, 255), show_sun=True)
        text(d, (W / 2, H - 24), '赤い印は、地球に向いている側。位置によって、昼になったり夜になったりする（自作の模式図）', 32, DIM, 'mm')
    else:
        R = min(W / 2 - 240, H / 2 - 130)
        rot = (lambda phi: phi + math.pi) if mode == 'spin' else (lambda phi: 0.0)
        panel(W / 2, H / 2 + 20, R, rot, '自転する月' if mode == 'spin' else 'もし、自転しない月なら', (150, 205, 255) if mode == 'spin' else (255, 190, 130))
    commit(im, L, box, a)



def _egg(d, c, a_, b_, ang, fill, outline):
    pts = []
    for k in range(72):
        u = 2 * math.pi * k / 72
        x, y = a_ * math.cos(u), b_ * math.sin(u)
        pts.append((c[0] + x * math.cos(ang) - y * math.sin(ang), c[1] - (x * math.sin(ang) + y * math.cos(ang))))
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill, outline=outline)


def tidalbulge(im, d0, cx, it, a):
    """できたばかりの月のふくらみのずれ（NASA『Tidal Locking』の説明を図にした自作の模式図。縮尺・形は実際と異なる）。
    s_a: ゆがんでいる／s_b: 自転でふくらみがずれる／s_c: 重力が引き戻す／s_d: 熱として失われ自転が遅くなる／s_e: 同期した／s_f: 遠ざかる"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    sa, sb, sc, sd, se, sf = [T(cx, it.get(k, i)) for k, i in (('s_a', 0), ('s_b', 1), ('s_c', 2), ('s_d', 3), ('s_e', 4), ('s_f', 5))]
    ex, ey = W * 0.25, H * 0.5; mx0 = W * 0.68; my = H * 0.5
    mx = mx0 + (60 * ease(sf / 1.5) if sf >= 0 else 0)
    circle(d, (ex, ey), 120, fill=(70, 120, 200, 255), outline=(150, 190, 240, 255), w=3)
    text(d, (ex, ey + 160), '地球', 36, (170, 200, 240), 'mm')
    # 月（ふくらみ＝長い軸）
    ang0 = math.pi                              # 地球の方向
    ang = ang0
    if sb >= 0:
        ang = ang0 - math.radians(40) * ease(sb / 0.8)
    if sc >= 0:
        ang = ang0 - math.radians(40) * (1 - 0.6 * ease(sc / 1.2))
    if sd >= 0:
        ang = ang0 - math.radians(16) * (1 - ease(sd / 3.0))
    if se >= 0:
        ang = ang0
    hot = sd >= 0 and se < 0
    col = (235, 150, 110, 255) if hot else (222, 214, 190, 255)
    if sa >= 0:
        _egg(d, (mx, my), 100, 72, ang, col, (250, 245, 225, 255))
        text(d, (mx, my - 130), 'ふくらんだ部分（長い軸）', 32, WHITE, 'mm')
        # 地球の方向の線
        poly(d, [(mx, my), (ex + 130, ey)], (150, 170, 200, 200), 3)
    if sb >= 0 and sc < 0:
        text(d, (W / 2, H - 70), '月が自転すると、ふくらみが、地球の方向から少しずれる', 36, (255, 205, 130), 'mm')
    if sc >= 0 and sd < 0:
        poly(d, [(mx - 90, my + 60), (mx - 200, my + 20)], (150, 205, 255, 255), 8)
        arrow_head(d, (mx - 200, my + 20), (mx - 90, my + 60), (150, 205, 255, 255), 24)
        text(d, (W / 2, H - 70), '地球の重力が、そのずれを、引き戻そうとする', 36, (150, 205, 255), 'mm')
    if sd >= 0 and se < 0:
        text(d, (mx, my + 150), '熱として失われる', 34, (255, 170, 120), 'mm')
        text(d, (W / 2, H - 70), 'エネルギーが熱になり、月の自転が、だんだん遅くなる', 36, (255, 170, 120), 'mm')
    if se >= 0 and sf < 0:
        text(d, (W / 2, H - 70), '自転一回 ＝ 地球のまわりを一周する時間（同じになった）', 36, GOLD, 'mm')
    if sf >= 0:
        poly(d, [(mx + 110, my), (mx + 220, my)], (255, 205, 110, 255), 8)
        arrow_head(d, (mx + 110, my), (mx + 220, my), (255, 205, 110, 255), 24)
        text(d, (W / 2, H - 70), '潮汐力で、月は、地球から少しずつ遠ざかってきた（今も、年に約4cm）', 34, (255, 205, 110), 'mm')
    text(d, (W / 2, 28), '自作の模式図（形・距離・縮尺は実際と異なります）', 28, DIM, 'mm')
    commit(im, L, box, a)



def islemap(im, d0, cx, it, a):
    """島の数え方の模式図（自作。実在の地図ではない）。s_a: 粗い地図／s_b: 詳しい地図（数えられる陸地が増える）／s_c: 周囲長の基準で数える対象を示す。"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    sa, sb, sc = T(cx, it.get('s_a', 0)), T(cx, it.get('s_b', 1)), T(cx, it.get('s_c', 2))
    if it.get('mode') == 'both':
        import random
        rnd = random.Random(7)
        pw = (W - 160) / 2
        for i, (lab, col_) in enumerate((('粗い地図', (255, 205, 130)), ('詳しい地図', (150, 205, 255)))):
            x0 = 60 + i * (pw + 40)
            d.rounded_rectangle((x0 * S, 90 * S, (x0 + pw) * S, (H - 120) * S), 20 * S, fill=(24, 52, 86, 255), outline=(120, 150, 190, 255), width=3 * S)
            text(d, (x0 + pw / 2, 60), lab, 36, col_, 'mm')
        rr = random.Random(7)
        for k in range(70):
            fx = rr.random(); fy = rr.random(); rad = (46 if k < 12 else (26 if k < 30 else 11)) * (0.8 + 0.4 * rr.random())
            for i in range(2):
                if i == 0 and k >= 12:
                    continue
                if i == 0 and sa < 0:
                    continue
                if i == 1 and sb < 0:
                    continue
                x0 = 60 + i * (pw + 40)
                kk = ease(((sa if i == 0 else sb) - (k % 7) * 0.04) / 0.5)
                if kk > 0:
                    circle(d, (x0 + 40 + fx * (pw - 80), 130 + fy * (H - 330)), rad * 0.62 * kk, fill=(214, 200, 150, 255), outline=(245, 235, 200, 255), w=2)
        text(d, (W / 2, H - 55), '同じ海域を、細かさの異なる二つの地図で表した、自作の模式図（実在の地図ではありません）', 30, DIM, 'mm')
        commit(im, L, box, a)
        return
    d.rounded_rectangle((60 * S, 70 * S, (W - 60) * S, (H - 110) * S), 20 * S, fill=(24, 52, 86, 255), outline=(120, 150, 190, 255), width=3 * S)
    import random
    rnd = random.Random(7)
    isl = []
    for k in range(70):
        x = 120 + rnd.random() * (W - 240); y = 110 + rnd.random() * (H - 330)
        r = 46 if k < 12 else (26 if k < 30 else 11)
        isl.append((x, y, r * (0.8 + 0.4 * rnd.random()), k))
    for x, y, r, k in isl:
        big = k < 12; mid = k < 30
        vis = big if sb < 0 else True
        if sa < 0:
            continue
        if not vis:
            continue
        kk = ease((sa if big else sb - (k % 7) * 0.05) / 0.6)
        if kk <= 0:
            continue
        small = (r < 20)
        col = (214, 200, 150, 255) if not (sc >= 0 and small) else (110, 118, 130, 255)
        circle(d, (x, y), r * kk, fill=col, outline=(245, 235, 200, 255), w=2)
    if sa >= 0 and sb < 0:
        text(d, (W / 2, H - 60), '粗い地図：数えられる陸地は、少ない', 38, (255, 205, 130), 'mm')
    if sb >= 0 and sc < 0:
        text(d, (W / 2, H - 60), '詳しい地図：小さな陸地も描かれ、数えられる陸地が増える', 38, (150, 205, 255), 'mm')
    if sc >= 0:
        text(d, (W / 2, H - 60), '周囲長0.1km以上の陸地を数える（灰色は、基準未満）', 38, GOLD, 'mm')
    text(d, (W / 2, 36), '自作の模式図（実在の地図・島の位置ではありません）', 28, DIM, 'mm')
    commit(im, L, box, a)



def bulb(im, d0, cx, it, a):
    """電球のたとえ（気象庁）：マグニチュード＝電球の明るさ、震度＝離れた場所での明るさ（自作の模式図）。s_a: 電球／s_b: 離れた場所／s_c: 遠いほど暗い"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    sa, sb, sc = T(cx, it.get('s_a', 0)), T(cx, it.get('s_b', 1)), T(cx, it.get('s_c', 2))
    bx, by = 260, H / 2
    if sa >= 0:
        k = ease(sa / 0.6)
        for r in (150, 110, 70):
            circle(d, (bx, by), r * k, fill=(255, 220, 120, int(40 * k)))
        circle(d, (bx, by), 44 * k, fill=(255, 235, 150, 255), outline=(255, 250, 210, 255), w=3)
        text(d, (bx, by + 190), '電球の明るさ ＝ マグニチュード', 34, (255, 225, 140), 'mm')
        text(d, (bx, by + 235), '（一つの地震に、一つ）', 30, DIM, 'mm')
    if sb >= 0:
        for i, (dx, lab) in enumerate(((620, '近い場所'), (1000, 'やや遠い場所'), (1380, '遠い場所'))):
            kk = ease((sb - i * 0.3) / 0.5)
            if kk <= 0:
                continue
            bright = (1.0, 0.55, 0.22)[i] if sc >= 0 else 0.6
            col = (int(255 * bright), int(235 * bright), int(150 * bright), 255)
            circle(d, (dx, by), 70 * kk, fill=col, outline=(200, 210, 230, 255), w=3)
            text(d, (dx, by + 120), lab, 32, WHITE, 'mm', alpha=int(255 * kk))
            poly(d, [(bx + 60, by), (dx - 80, by)], (255, 235, 150, 110), 3)
        text(d, (1000, by - 170), '離れた場所での明るさ ＝ 震度（場所によって異なる）', 34, (150, 205, 255), 'mm')
    if sc >= 0:
        text(d, (W / 2, H - 40), '同じ電球でも、離れた場所では、周りは暗くなる（自作の模式図）', 32, DIM, 'mm')
    commit(im, L, box, a)


def shindo(im, d0, cx, it, a):
    """日本の震度の10階級（気象庁）。s_a: ゼロ〜四／s_b: 五弱〜七"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    sa, sb = T(cx, it.get('s_a', 0)), T(cx, it.get('s_b', 1))
    labs = ['0', '1', '2', '3', '4', '5弱', '5強', '6弱', '6強', '7']
    cols = [(120, 170, 220), (110, 190, 220), (110, 205, 190), (140, 215, 140), (200, 220, 120), (240, 210, 100), (245, 175, 90), (240, 130, 80), (225, 90, 80), (200, 60, 90)]
    tw = (W - 120) / 10
    for i, (lab, col) in enumerate(zip(labs, cols)):
        s = sa if i < 5 else sb
        if s < 0:
            continue
        k = ease((s - (i % 5) * 0.2) / 0.5)
        x = 60 + i * tw
        d.rounded_rectangle((x * S, (H / 2 - 110) * S, (x + tw - 14) * S, (H / 2 + 110) * S), 16 * S, fill=col + (int(255 * k),), outline=(255, 255, 255, int(200 * k)), width=3 * S)
        text(d, (x + (tw - 14) / 2, H / 2), lab, 64 if len(lab) == 1 else 52, (30, 30, 40), 'mm', alpha=int(255 * k))
    text(d, (W / 2, H / 2 - 190), '日本の震度は、全部で10階級（気象庁）', 40, WHITE, 'mm')
    commit(im, L, box, a)



# ------------------------------------------------------------------ 地図の上の軍勢（桶狭間の戦い）
def _upto(pts, s):
    """道すじの先頭から、のこり s の地点までを結んだ折れ線（末尾が先頭のいまの位置）。"""
    out = [pts[0]]
    for i in range(len(pts) - 1):
        l = math.dist(pts[i], pts[i + 1])
        if s <= l:
            f = s / l if l else 0
            out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f,
                        pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f))
            return out
        out.append(pts[i + 1])
        s -= l
    return out


def _plate(d, xy, s, size, col, pad=9):
    """地形の上でも読めるように、文字の後ろへ濃い板をしいて軍の名を出す。"""
    f = F[size * S]
    w = d.textlength(s, font=f)
    x, y = xy[0] * S, xy[1] * S
    d.rounded_rectangle((x - pad * S, y - 5 * S, x + w + pad * S, y + (size + 7) * S), 7 * S,
                        fill=(6, 16, 26, 226), outline=tuple(col) + (170,), width=2 * S)
    d.text((x, y), s, font=f, fill=(250, 248, 240, 255))


def oke_march(im, d0, cx, it, a):
    """地図の上を軍勢の印が道すじに沿って動く（桶狭間の戦いの行軍図）。

    spec: dict(t='anim', name='oke_march', img='march', box=[x0,y0,x1,y1], at=N, until=M,
               armies=[dict(col=(r,g,b), pts=[(nx,ny), ...], legs=[[i0,i1], ...],
                            label='織田軍', lab_off=(dx,dy), head=15)])
    pts は地図画像の左上(0,0)〜右下(1,1)の相対座標で、軍の通り道（通過点）を順に並べる。
    legs は pts の間の区間ごとの予定で、legs[k]=[i0,i1] は「文 i0 が始まってから、文 i1 が
    始まるまでに pts[k] から pts[k+1] へ動く」という意味（i1 が文の数なら章の終わりまで）。
    区間の外では通過点で止まっている。"""
    box = it['box']
    W, H = box[2] - box[0], box[3] - box[1]
    pic = get_img(it['img'], W - 16, H - 16)             # it_image と同じ収め方・同じ置き方
    px0, py0 = (W - pic.width) // 2, 8
    mp = pic.convert('RGBA')
    if a < 1:                                            # 出るときは薄く出す（it_image と同じ）
        mp.putalpha(mp.getchannel('A').point(lambda v: int(v * a)))
    im.alpha_composite(mp, (box[0] + px0, box[1] + py0))
    mw, mh = pic.width, pic.height                     # 印と道すじは地図の枠で切る
    L, d = layer([0, 0, mw, mh])
    n = len(cx.segl)

    def P(q):
        return (q[0] * mw, q[1] * mh)

    for am in it.get('armies', []):
        pts = [P(q) for q in am['pts']]
        legs = am['legs']
        k = 0                                            # いま何番目の区間か（まだなら 0）
        for j, (i0, _) in enumerate(legs):
            if i0 < n and cx.t >= cx.st[i0]:
                k = j
        i0, i1 = legs[k][0], legs[k][1]
        t0 = cx.st[i0]
        t1 = cx.st[i1] if i1 < n else cx.st[n - 1] + cx.segl[n - 1]['duration']
        p = 0.0 if cx.t <= t0 else min(1.0, (cx.t - t0) / max(.001, t1 - t0))
        s = sum(math.dist(pts[j], pts[j + 1]) for j in range(k))
        s += ease(p) * math.dist(pts[k], pts[k + 1])
        trav = _upto(pts, s)
        col = tuple(am['col'])
        if len(trav) > 1:                                # 通った道すじ（暗い縁＋明るい線）
            poly(d, trav, (6, 14, 22, 170), 13)
            poly(d, trav, col + (232,), 8)
        head, r = trav[-1], am.get('head', 15)
        circle(d, head, r + 7 + 4 * math.sin(cx.t * 4), outline=col + (90,), w=2)
        circle(d, head, r + 3, fill=(6, 14, 22, 210))
        circle(d, head, r, fill=col + (255,), outline=(250, 248, 240, 255), w=3)
        if am.get('label'):
            ox, oy = am.get('lab_off', (22, -52))
            _plate(d, (head[0] + ox, head[1] + oy), am['label'], am.get('lsize', 26), col)
    commit(im, L, [box[0] + px0, box[1] + py0, box[0] + px0 + mw, box[1] + py0 + mh], a)


def leapclock(im, d0, cx, it, a):
    """うるう秒の挿入（総務省）：2017年1月1日、8:59:59 → 8:59:60 → 9:00:00（日本時間）。デジタル時計の模式図（自作）。s_a/s_b/s_c"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    ss = [T(cx, it.get('s_a', 0)), T(cx, it.get('s_b', 1)), T(cx, it.get('s_c', 2))]
    labs = ['直前', '追加された1秒', '直後']; vals = ['08:59:59', '08:59:60', '09:00:00']
    pw, ph, gap = 460, 250, 70; x0 = (W - 3 * pw - 2 * gap) / 2; y0 = H / 2 - ph / 2 - 20
    for i in range(3):
        k = ease(ss[i] / 0.5)
        if k <= 0:
            continue
        x = x0 + i * (pw + gap); hot = i == 1
        d.rounded_rectangle((x * S, y0 * S, (x + pw) * S, (y0 + ph) * S), radius=22 * S, fill=(20, 18, 8, int(235 * k)) if hot else (10, 22, 36, int(235 * k)), outline=(239, 201, 118, int(255 * k)) if hot else (120, 150, 180, int(255 * k)), width=(6 if hot else 3) * S)
        text(d, (x + pw / 2, y0 + ph / 2 - 10), vals[i], 78, GOLD if hot else WHITE, 'mm', alpha=int(255 * k))
        text(d, (x + pw / 2, y0 + ph - 38), labs[i], 34, GOLD if hot else DIM, 'mm', alpha=int(255 * k))
        if i < 2 and ss[i + 1] >= 0:
            poly(d, [(x + pw + 8, y0 + ph / 2), (x + pw + gap - 8, y0 + ph / 2)], (239, 201, 118, 255), 5)
    text(d, (W / 2, y0 + ph + 70), '2017年1月1日（日本時間）　※実機の表示ではなく、仕組みを説明する自作の模式図です', 30, DIM, 'mm')
    commit(im, L, box, a)


def tolerance(im, d0, cx, it, a):
    """ずれの許容上限：0.9秒 → 3,600秒（BIPM決議5）。幅は3,600秒を全幅とした縮尺（自作の模式図）。s_a: 0.9秒／s_b: 3,600秒／s_c: 注記"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    sa, sb, sc = T(cx, it.get('s_a', 0)), T(cx, it.get('s_b', 1)), T(cx, it.get('s_c', 2))
    x0, x1 = 120, W - 120; bw = x1 - x0
    if sa >= 0:
        k = ease(sa / 0.5); y = H * 0.30
        text(d, (x0, y - 70), 'これまでの上限：0.9秒', 40, WHITE, 'la', alpha=int(255 * k))
        d.rectangle((x0 * S, (y - 4) * S, x1 * S, (y + 40) * S), outline=(120, 150, 180, int(140 * k)), width=2 * S)
        d.rectangle((x0 * S, (y - 4) * S, (x0 + max(3, bw * 0.9 / 3600)) * S, (y + 40) * S), fill=(239, 201, 118, int(255 * k)))
        text(d, (x0 + 22, y + 74), '↑ この細い線（縮尺：右端＝3,600秒）', 30, DIM, 'la', alpha=int(255 * k))
    if sb >= 0:
        k = ease(sb / 0.7); y = H * 0.62
        text(d, (x0, y - 70), '2027年5月20日からの上限：3,600秒（1時間）', 40, WHITE, 'la')
        d.rectangle((x0 * S, (y - 4) * S, (x0 + bw * k) * S, (y + 40) * S), fill=(110, 170, 235, 255))
    if sc >= 0:
        text(d, (W / 2, H - 50), '広げたのは「許容する上限」。実際のずれが、すぐ1時間になるわけではない', 34, GOLD, 'mm', alpha=int(255 * ease(sc / 0.5)))
    commit(im, L, box, a)


def driftsaw(im, d0, cx, it, a):
    """うるう秒の仕組み（自作の模式図）：二つの時刻のずれが少しずつ広がり、0.9秒の枠に近づくと1秒を入れる（または抜く）。mode='pos'：1秒を入れる／mode='neg'：1秒を抜く（負のうるう秒）。s_a：描き始める文"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    s = T(cx, it.get('s_a', 0))
    if s < 0:
        commit(im, L, box, a); return
    neg = it.get('mode', 'pos') == 'neg'
    x0, x1 = 150, W - 90; yc = H * 0.50; pps = 200.0
    ybot, ytop = yc + 0.9 * pps, yc - 0.9 * pps
    for yy in (ytop, ybot):
        poly(d, [(x0, yy), (x1, yy)], (239, 201, 118, 150), 3)
    poly(d, [(x0, yc), (x1, yc)], (120, 150, 180, 120), 2)
    text(d, (x0 - 14, ytop), '0.9秒', 30, GOLD, 'rm'); text(d, (x0 - 14, ybot), '0.9秒', 30, GOLD, 'rm'); text(d, (x0 - 14, yc), 'ずれなし', 28, DIM, 'rm')
    text(d, (W / 2, 40), '二つの時刻（原子時計をもとにした時刻と、自転に基づく時刻）の「ずれ」', 34, WHITE, 'mm')
    sg = -1 if neg else 1; teeth = 3; tw = (x1 - x0) / teeth
    pts = []
    for k in range(teeth):
        xs = x0 + k * tw
        pts.append(((xs + 6, yc - sg * 0.1 * pps), (xs + tw * 0.86, yc + sg * 0.9 * pps), 'drift'))
        pts.append(((xs + tw * 0.86, yc + sg * 0.9 * pps), (xs + tw * 0.9, yc - sg * 0.1 * pps), 'jump'))
    u = ease(s / 5.0) * len(pts)
    for i, (p, q, kind) in enumerate(pts):
        f = min(1.0, max(0.0, u - i))
        if f <= 0:
            break
        e = (p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f)
        col = (110, 170, 235, 255) if kind == 'drift' else ((255, 150, 70, 255) if neg else (239, 201, 118, 255))
        poly(d, [p, e], col, 7 if kind == 'drift' else 9)
        if kind == 'jump' and f >= 1.0 and i == 1:
            lab = '1秒を抜く（負のうるう秒）' if neg else '1秒を入れる（うるう秒）'
            text(d, (q[0] + 16, (p[1] + q[1]) / 2), lab, 30, (255, 150, 70) if neg else GOLD, 'lm')
    text(d, (W / 2, H - 36), '自作の模式図です（実測値ではありません）', 28, DIM, 'mm')
    commit(im, L, box, a)


_SUN_RISE = [27, 26, 26, 26, 26, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 26, 26, 26, 26, 27, 27, 27, 28, 28] + [29, 29, 29, 30, 30, 31, 31, 32, 33, 33, 34, 34, 35, 36, 36]   # 東京2027年6/1〜7/15 の日の出（4時＋分）
_SUN_SET = [51, 52, 52, 53, 54, 54, 55, 55, 56, 56, 57, 57, 58, 58, 58, 59, 59, 59, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1] + [1, 1, 1, 1, 1, 0, 0, 0, 0, 59, 59, 59, 58, 58, 57]   # 日の入り（18時＋分。0以下は19時台）
_SUN_NOON = [39, 39, 39, 39, 39, 40, 40, 40, 40, 40, 41, 41, 41, 41, 41, 42, 42, 42, 42, 43, 43, 43, 43, 43, 44, 44, 44, 44, 44, 45] + [45, 45, 45, 45, 46, 46, 46, 46, 46, 46, 47, 47, 47, 47, 47]   # 南中（11時＋分）


def suncurve(im, d0, cx, it, a):
    """東京の6月〜7月前半の、日の出／日の入り／南中の変化（国立天文台 暦計算室 2027年の数字、分単位）。mode='rise'|'set'|'noon'。s_a：描き始める文。夏至（6/21）に縦線、最小・最大の続く区間を強調。"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    s = T(cx, it.get('s_a', 0))
    if s < 0:
        commit(im, L, box, a); return
    mode = it.get('mode', 'rise')
    if mode == 'rise':
        vals = list(_SUN_RISE); base = 4 * 60; lab = '東京の日の出（2027年）'; hi = lambda v: v == min(_SUN_RISE); col = (255, 190, 120); fmt = lambda m: f'{m // 60}:{m % 60:02d}'
    elif mode == 'set':
        vals = [(v if v >= 51 else v + 60) for v in _SUN_SET]; base = 18 * 60; lab = '東京の日の入り（2027年）'; hi = lambda v: v == max(vals); col = (255, 150, 150); fmt = lambda m: f'{m // 60}:{m % 60:02d}'
    else:
        vals = list(_SUN_NOON); base = 11 * 60; lab = '東京の南中の時刻（2027年）'; hi = lambda v: False; col = (150, 210, 255); fmt = lambda m: f'{m // 60}:{m % 60:02d}'
    mn, mx = min(vals) - 1, max(vals) + 1
    x0, x1 = 300, W - 100; y0, y1 = 110, H - 110
    n = len(vals)
    px = lambda i: x0 + (x1 - x0) * i / (n - 1)
    py = lambda v: y1 - (y1 - y0) * (v - mn) / (mx - mn)
    text(d, (W / 2, 40), lab + '　※国立天文台 暦計算室の数字（分単位）', 32, WHITE, 'mm')
    poly(d, [(x0, y1), (x1, y1)], (120, 150, 180, 200), 2); poly(d, [(x0, y0), (x0, y1)], (120, 150, 180, 200), 2)
    for day, name in ((0, '6/1'), (20, '6/21 夏至'), (30, '7/1'), (44, '7/15')):
        text(d, (px(day), y1 + 22), name, 28, GOLD if day == 20 else DIM, 'mm')
    k = ease(s / 3.0); m = max(2, int(n * k))
    sol = px(20)
    poly(d, [(sol, y0 - 20), (sol, y1)], (239, 201, 118, 170), 3)
    pts = [(px(i), py(vals[i])) for i in range(m)]
    poly(d, pts, col + (255,), 6)
    for i in range(m):
        if hi(vals[i]):
            circle(d, (px(i), py(vals[i])), 8, fill=(239, 201, 118, 255))
    text(d, (x0 - 14, py(vals[0])), fmt(base + vals[0]), 28, DIM, 'rm')
    if k >= 1.0:
        text(d, (x0 - 14, py(vals[20])), fmt(base + vals[20]) + '（夏至）', 28, GOLD, 'rm')
        text(d, (x0 - 14, py(vals[-1])), fmt(base + vals[-1]), 28, DIM, 'rm')
    commit(im, L, box, a)


def dayline(im, d0, cx, it, a):
    """日の出・南中・日の入りの関係（国立天文台の説明をもとにした自作の模式図）。s_a：三つの印／s_b：南中が遅くなると、どちらも同じ向きにずれる"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    sa, sb = T(cx, it.get('s_a', 0)), T(cx, it.get('s_b', 1))
    x0, x1 = 160, W - 160; yc = H * 0.52
    poly(d, [(x0, yc), (x1, yc)], (120, 150, 180, 220), 4)
    pos = {'日の出': x0 + 120, '南中': (x0 + x1) / 2, '日の入り': x1 - 120}
    cols = {'日の出': (255, 190, 120), '南中': (255, 240, 170), '日の入り': (255, 150, 150)}
    shift = ease(sb / 1.2) * 70 if sb >= 0 else 0
    if sa >= 0:
        for i, (k, x) in enumerate(pos.items()):
            kk = ease((sa - i * 0.35) / 0.5)
            if kk <= 0:
                continue
            xx = x + shift
            circle(d, (xx, yc), 26 * kk, fill=cols[k] + (255,), outline=(255, 255, 255, 255), w=3)
            text(d, (xx, yc - 70), k, 38, cols[k], 'mm', alpha=int(255 * kk))
        xm = pos['南中']
        text(d, (xm - 330, yc + 90), '前', 40, DIM, 'mm'); text(d, (xm + 330, yc + 90), '後ろ', 40, DIM, 'mm')
        text(d, (W / 2, 70), '日の出と日の入りは、南中の時刻を挟んで、前と後ろに分かれる', 36, WHITE, 'mm')
    if sb >= 0:
        for k, x in pos.items():
            poly(d, [(x + 40, yc + 150), (x + 40 + shift + 40, yc + 150)], (239, 201, 118, 255), 6)
        text(d, (W / 2, H - 70), '南中が遅くなると、どちらも同じ向き（遅い方）にずれる（自作の模式図）', 34, GOLD, 'mm')
    commit(im, L, box, a)


def venusspin(im, d0, cx, it, a):
    """金星を上から見た図（自作の模式図、NASAの周期をもとにした）：公転224.701日、自転243.025日（逆向き）。経過日数を進め、自転の回転数・公転の周回数・太陽が空の同じ位置に戻った回数を数える。s_a：動き始める文"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    s = T(cx, it.get('s_a', 0))
    ox, oy, R = W * 0.30, H * 0.54, 205
    circle(d, (ox, oy), 46, fill=(255, 205, 90, 255), outline=(255, 235, 160, 255), w=3)
    for rr in (66, 88):
        circle(d, (ox, oy), rr, outline=(255, 205, 90, int(80 - (rr - 66) * 1.5)), w=2)
    text(d, (ox, oy), '太陽', 28, (60, 40, 0), 'mm')
    circle(d, (ox, oy), R, outline=(120, 150, 180, 170), w=2)
    text(d, (W / 2, 36), '上から見た金星（自作の模式図。周期はNASAの表の数字）', 38, WHITE, 'mm')
    P_ORB, P_ROT = 224.701, 243.025
    if s < 0:
        t = 0.0
    else:
        t = min(1.0, s / float(it.get('dur', 10.0))) * P_ROT
    th = 2 * math.pi * t / P_ORB
    phi = -2 * math.pi * t / P_ROT
    px, py = ox + R * math.cos(th), oy - R * math.sin(th)
    pr = 40
    circle(d, (px, py), pr, fill=(225, 190, 150, 255), outline=(255, 245, 225, 255), w=3)
    al = math.pi + phi   # 開始時は、地表の一点が太陽の方を向く（太陽が正午の位置にある）
    mx, my = px + pr * 1.7 * math.cos(al), py - pr * 1.7 * math.sin(al)
    poly(d, [(px, py), (mx, my)], (90, 190, 255, 255), 6)
    circle(d, (mx, my), 9, fill=(90, 190, 255, 255))
    be = th + math.pi
    poly(d, [(px, py), (px + pr * 1.3 * math.cos(be), py - pr * 1.3 * math.sin(be))], (255, 205, 90, 230), 4)
    ang = th - phi
    noon = int(ang / (2 * math.pi))
    rx = W * 0.62
    text(d, (rx, H * 0.16), f'経過：{t:5.1f}日', 48, WHITE, 'la')
    text(d, (rx, H * 0.30), f'自転：{t / P_ROT:.2f}回転（逆向き）', 42, (150, 210, 255), 'la')
    text(d, (rx, H * 0.42), f'公転：{t / P_ORB:.2f}周', 42, GOLD, 'la')
    text(d, (rx, H * 0.58), f'太陽が元の位置に戻った回数：{noon}回', 42, (255, 205, 150), 'la')
    text(d, (rx, H * 0.74), '青い線：地表の一点の向き', 36, (150, 210, 255), 'la')
    text(d, (rx, H * 0.82), '黄色い線：太陽の向き', 36, GOLD, 'la')
    commit(im, L, box, a)


def oceanlight(im, d0, cx, it, a):
    """海の色の模式図（NOAA・WHOIの説明をもとにした自作、数値なし）。mode='surface'：水面は空を映す（嵐の日は灰色・夕方はピンク）／水面の下は青が残る。mode='depth'：光の色が深さとともに減る（赤・オレンジは数メートルでほぼ消え、青と紫が最も深くまで届く）。"""
    Z = 1.0; box = it['box']; L, d = layer(box, Z); W, H = vs(box, Z)
    mode = it.get('mode', 'surface')
    sa, sb, sc = T(cx, it.get('s_a', 0)), T(cx, it.get('s_b', 1)), T(cx, it.get('s_c', 2))
    if mode == 'surface':
        pw, ph = 760, 400; y0 = 130
        xs = (150, 150 + pw + 100)
        if sa >= 0:
            k = ease(sa / 0.6)
            cols = [(120, 125, 135), (235, 165, 175)]
            ph_t = (sa / 3.0) % 2.0
            c0 = cols[0] if ph_t < 1.0 else cols[1]
            d.rounded_rectangle((xs[0] * S, y0 * S, (xs[0] + pw) * S, (y0 + ph) * S), radius=20 * S, fill=c0 + (int(255 * k),), outline=(255, 255, 255, int(200 * k)), width=3 * S)
            text(d, (xs[0] + pw / 2, y0 + ph / 2 - 20), '水面：空を映す', 46, WHITE, 'mm', alpha=int(255 * k))
            text(d, (xs[0] + pw / 2, y0 + ph / 2 + 50), '嵐の日は灰色、日の出・日の入りはピンク', 30, WHITE, 'mm', alpha=int(255 * k))
        if sb >= 0:
            k = ease(sb / 0.6)
            for i in range(10):
                f = i / 9.0
                col = (int(40 + 0 * f), int(130 - 40 * f), int(215 - 55 * f))
                d.rectangle((xs[1] * S, (y0 + ph * f * 0.9) * S, (xs[1] + pw) * S, (y0 + ph * (f + 0.1) * 0.9 + 4) * S), fill=col + (int(255 * k),))
            d.rounded_rectangle((xs[1] * S, y0 * S, (xs[1] + pw) * S, (y0 + ph * 0.9 + 4) * S), radius=20 * S, outline=(255, 255, 255, int(200 * k)), width=3 * S)
            text(d, (xs[1] + pw / 2, y0 + ph / 2 - 20), '水面の下：青が残る', 46, WHITE, 'mm', alpha=int(255 * k))
            text(d, (xs[1] + pw / 2, y0 + ph / 2 + 50), '青い色は、水そのものがつくる（WHOI）', 30, WHITE, 'mm', alpha=int(255 * k))
        text(d, (W / 2, 70), '水面と水中を比べた自作の模式図', 34, WHITE, 'mm')
        text(d, (W / 2, H - 50), '解説の内容を表した図です（実際の写真ではありません）', 28, DIM, 'mm')
    elif mode == 'scatter':
        k = ease(sa / 1.2) if sa >= 0 else 0
        text(d, (W / 2, 60), '青と紫の光が、水の中の粒子で散乱される様子（自作の模式図）', 34, WHITE, 'mm')
        import random
        rnd = random.Random(7)
        pts = [(W * 0.55 + rnd.uniform(-330, 330), H * 0.58 + rnd.uniform(-150, 150)) for _ in range(9)]
        sx, sy = W * 0.18, 140
        if k > 0:
            poly(d, [(sx, sy), (W * 0.55, H * 0.46)], (80, 150, 255, int(255 * k)), 10)
            for (px_, py_) in pts:
                circle(d, (px_, py_), 11, fill=(230, 235, 245, int(230 * k)))
            for (px_, py_) in pts[:6]:
                for ang in (0.5, 2.0, 3.6, 5.1):
                    kk = ease((sb - 0.6) / 1.2) if sb >= 0 else 0
                    if kk > 0:
                        poly(d, [(px_, py_), (px_ + 90 * kk * math.cos(ang), py_ + 90 * kk * math.sin(ang))], (110, 175, 255, int(200 * kk)), 4)
        if sb >= 0:
            text(d, (W / 2, H - 70), '粒子に当たった光は、いろいろな方向へ散らばる', 34, GOLD, 'mm', alpha=int(255 * ease(sb / 0.8)))
    else:
        names = [('赤', (235, 70, 60), 0.16), ('オレンジ', (245, 150, 50), 0.22), ('黄', (240, 220, 70), 0.42), ('緑', (90, 200, 110), 0.62), ('青', (70, 140, 245), 0.98), ('紫', (150, 100, 230), 0.92)]
        x0, x1 = 300, W - 140; y_top = 120; rh = 56; gap = 28
        text(d, (W / 2, 50), '光の色が、深さとともに減る様子（自作の模式図。深さの数値は示さない）', 32, WHITE, 'mm')
        text(d, (x0, y_top - 38), '水面', 30, GOLD, 'mm'); text(d, (x1, y_top - 38), '深い', 30, GOLD, 'mm')
        for i, (nm, col, ln) in enumerate(names):
            y = y_top + i * (rh + gap)
            kk = ease(sa / 2.5) if sa >= 0 else 0
            text(d, (x0 - 20, y + rh / 2), nm, 36, col, 'rm')
            d.rectangle((x0 * S, y * S, x1 * S, (y + rh) * S), outline=(120, 150, 180, 90), width=2)
            if kk > 0:
                ww = (x1 - x0) * ln * kk
                d.rectangle((x0 * S, y * S, (x0 + ww) * S, (y + rh) * S), fill=col + (230,))
        if sb >= 0:
            k = ease(sb / 0.6)
            text(d, (x0 + (x1 - x0) * 0.26, y_top + rh / 2 + 0), '数メートルで、ほぼ消える（WHOI）', 28, WHITE, 'lm', alpha=int(255 * k))
        if sc >= 0:
            k = ease(sc / 0.6)
            text(d, (x1 - 10, y_top + 4 * (rh + gap) + rh / 2 - 38), '青と紫が、最も深くまで届く', 30, GOLD, 'rm', alpha=int(255 * k))
    commit(im, L, box, a)


DRAW = dict(oceanlight=oceanlight, venusspin=venusspin, dayline=dayline, suncurve=suncurve, driftsaw=driftsaw, leapclock=leapclock, tolerance=tolerance, bulb=bulb, shindo=shindo, islemap=islemap, tidalbulge=tidalbulge, moonsync=moonsync, rain100=rain100, blocks6=blocks6, areapoint=areapoint, onemm=onemm, calib=calib, lunar=lunar, caltiles=caltiles, orbit=orbit, sunangle=sunangle, declination=declination, declination2=declination2, polar=polar, forearm=forearm, cells=cells, loop=loop, skin=skin, skintone=skintone, contrast=contrast, textbook=textbook, oke_march=oke_march)

try:
    import vp_anim_b as _b
    DRAW.update(_b.DRAW_B)
except ImportError as _e:
    print('vp_anim_b not loaded:', _e)

try:
    import vp_anim_c as _c
    DRAW.update(_c.DRAW_C)
except ImportError as _e:
    print('vp_anim_c not loaded:', _e)

try:
    import vp_anim_brain as _br
    DRAW.update(_br.DRAW_BRAIN)
except ImportError as _e:
    print('vp_anim_brain not loaded:', _e)

try:
    import vp_anim_shibuya as _sb
    DRAW.update(_sb.DRAW_SHIBUYA)
except ImportError as _e:
    print('vp_anim_shibuya not loaded:', _e)

try:
    import vp_anim_pop as _pop
    DRAW.update(_pop.DRAW_POP)
except ImportError as _e:
    print('vp_anim_pop not loaded:', _e)
