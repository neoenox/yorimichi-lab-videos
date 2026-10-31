"""渋谷川の動画（shibuya）の動く図。
sb_photos：同じ範囲の空中写真を、年代ごとに重ねて切り替える（at は文番号）。1枚目に、川筋と考えられる筋の印を引く。
sb_flow：上流（下水道幹線）→宮益橋→稲荷橋→地上の渋谷川、と処理水の導水。縮尺なしの模式図。
出典：国土地理院撮影の空中写真・地理院タイル（加工して作成）。"""
import math
from PIL import Image, ImageDraw
import vp_anim as A
from vp_anim import text, circle, poly, ease, T, layer, commit, GOLD, WHITE, DIM

BLUE = (110, 185, 255); DEEP = (40, 90, 150); ORG = (255, 150, 90)


def sb_photos(im, d0, cx, it, a):
    """spec: dict(t='anim', name='sb_photos', box=[...], imgs=[dict(name='aerial_1936', label='1936〜42年頃', at=1), ...],
    mark=dict(img=0, pts=[(nx,ny),...], at=2, until=4, label='川筋と考えられる筋'))"""
    box = it['box']
    W, H = box[2] - box[0], box[3] - box[1]
    base = None
    for k, e in enumerate(it['imgs']):
        if not cx.on(e['at']):
            continue
        pic = A.get_img(e['name'], W - 16, H - 16).convert('RGBA')
        k_a = min(a, cx.a(e['at']))
        if base is None:
            base = Image.new('RGBA', pic.size, (0, 0, 0, 255))
        p = pic.copy()
        if k_a < 1:
            p.putalpha(p.getchannel('A').point(lambda v: int(v * k_a)))
        base.alpha_composite(p)
        cur = k
    if base is None:
        return
    mw, mh = base.size
    m = it.get('mark')
    if m and cur == m['img'] and cx.on(m['at']) and (m.get('until') is None or not cx.on(m['until'])):
        pts = [(q[0] * mw, q[1] * mh) for q in m['pts']]
        prog = ease(T(cx, m['at']) / 2.2)
        tot = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
        s, out = tot * prog, [pts[0]]
        for i in range(len(pts) - 1):
            seg = math.dist(pts[i], pts[i + 1])
            if s >= seg:
                out.append(pts[i + 1]); s -= seg
            else:
                f = s / seg; out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)); break
        L = Image.new('RGBA', base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        if len(out) > 1:
            d.line(out, fill=(6, 14, 22, 200), width=12, joint='curve')
            d.line(out, fill=(255, 150, 90, 235), width=6, joint='curve')
        base.alpha_composite(L)
    x0, y0 = box[0] + (W - mw) // 2, box[1] + 8
    im.alpha_composite(base, (x0, y0))
    d = ImageDraw.Draw(im)
    e = it['imgs'][cur]
    f = A.F[30]
    lab = e['label']; w = d.textlength(lab, font=f)
    d.rounded_rectangle((x0 + 10, y0 + 10, x0 + 10 + w + 28, y0 + 56), 8, fill=(7, 24, 36, 235), outline=(176, 153, 100, 255), width=2)
    d.text((x0 + 24, y0 + 15), lab, font=f, fill=GOLD + (255,))
    if m and cur == m['img'] and cx.on(m['at']) and (m.get('until') is None or not cx.on(m['until'])):
        f2 = A.F[26]; l2 = m['label']; w2 = d.textlength(l2, font=f2)
        lx, ly = x0 + int(m.get('lab', (0.5, 0.9))[0] * mw) - w2 // 2, y0 + int(m.get('lab', (0.5, 0.9))[1] * mh)
        d.rounded_rectangle((lx - 12, ly - 4, lx + w2 + 12, ly + 40), 8, fill=(7, 24, 36, 235), outline=(255, 150, 90, 255), width=2)
        d.text((lx, ly), l2, font=f2, fill=(255, 190, 150, 255))


def sb_flow(im, d0, cx, it, a):
    """spec: dict(t='anim', name='sb_flow', box=[...], at=0, steps=[dict(at=a0)..dict(at=a4)]) 縮尺なしの模式図"""
    box = it['box']; at = [e['at'] for e in it['steps']]
    L, d = layer(box)
    S = A.S
    y = 230
    def X(v): return v
    def seg(x0, x1, col, w, dash=False):
        if dash:
            x = x0
            while x < x1:
                d.line([(x * S, y * S), (min(x + 26, x1) * S, y * S)], fill=col + (255,), width=int(w * S)); x += 40
        else:
            d.line([(x0 * S, y * S), (x1 * S, y * S)], fill=col + (255,), width=int(w * S))
    t = lambda i: ease(T(cx, at[i]) / 0.8) if T(cx, at[i]) >= 0 else 0
    text(d, (20, 650), '縮尺のない模式図（平成20年の東京都の資料をもとに自作）', 26, DIM)
    k1 = t(1)
    if k1 > 0:
        text(d, (40, 70), '上流と支流（宇田川・河骨川など）', 44, WHITE, 'lm', alpha=int(255 * k1))
        seg(40, 560 * k1 + 40 * (1 - k1), DEEP, 14, dash=True)
        text(d, (320, 292), '下水道幹線（地下）に変わった', 38, GOLD, 'mm', alpha=int(255 * k1))
        circle(d, (560, y), 14, fill=(7, 24, 36, 255), outline=GOLD + (255,), w=3)
        text(d, (560, 150), '宮益橋', 44, WHITE, 'mm', alpha=int(255 * k1))
    k2 = t(2)
    if k2 > 0:
        seg(560, 560 + 220 * k2, (90, 100, 110), 10, dash=True)
        text(d, (700, 292), '約200m', 38, DIM, 'mm', alpha=int(255 * k2))
        if k2 > 0.9:
            circle(d, (780, y), 14, fill=(7, 24, 36, 255), outline=GOLD + (255,), w=3)
            text(d, (780, 146), '稲荷橋', 44, WHITE, 'mm')
            text(d, (780, 198), 'ここから地上に出る', 32, DIM, 'mm')
    if k2 > 0.9:
        k3, k4 = t(3), t(4)
        w = 5 if k4 == 0 else 5 + 11 * k4
        end = 780 + 960 * ease(T(cx, at[2]) / 2.0 - .4)
        end = min(1660, max(780, end))
        seg(780, end, BLUE, w)
        if end >= 1650:
            circle(d, (1660, y), 14, fill=(7, 24, 36, 255), outline=GOLD + (255,), w=3)
            text(d, (1660, 150), '天現寺橋', 44, WHITE, 'mm')
        text(d, (1260, 292), '地上の渋谷川', 44, BLUE, 'mm')
        if k3 > 0 and k4 == 0:
            text(d, (1260, 350), 'ふだんの水量は、とても少なくなった', 44, ORG, 'mm', alpha=int(255 * k3))
        if k4 > 0:
            bx0, bx1, by0, by1 = 900, 1400, 470, 560
            d.rounded_rectangle((bx0 * S, by0 * S, bx1 * S, by1 * S), 14 * S, fill=(7, 24, 36, 240), outline=BLUE + (255,), width=3 * S)
            text(d, ((bx0 + bx1) / 2, (by0 + by1) / 2), '下水を高度に処理した水', 42, WHITE, 'mm')
            d.line([(1150 * S, by0 * S), (1150 * S, (y + 16) * S)], fill=BLUE + (255,), width=6 * S)
            d.polygon([((1150 - 14) * S, (y + 40) * S), ((1150 + 14) * S, (y + 40) * S), (1150 * S, (y + 14) * S)], fill=BLUE + (255,))
            text(d, (1150, 610), '川に流して、水を保っている', 44, GOLD, 'mm', alpha=int(255 * k4))
    commit(im, L, box, a)


DRAW_SHIBUYA = dict(sb_photos=sb_photos, sb_flow=sb_flow)


def sb_edo(im, d0, cx, it, a):
    """江戸の頃の川の模式図。spec: dict(t='anim', name='sb_edo', box=[...], at=0, steps=[dict(at=1), dict(at=2), dict(at=3)])
    steps: 水源が集まる／宇田川と合流して天現寺橋へ／水車。縮尺なし"""
    box = it['box']; at = [e['at'] for e in it['steps']]
    L, d = layer(box)
    S = A.S
    y = 300
    k = lambda i: ease(T(cx, at[i]) / 0.8) if T(cx, at[i]) >= 0 else 0
    k1, k2, k3 = k(0), k(1), k(2)
    text(d, (1780, 555), '縮尺のない模式図（平成20年の東京都の資料をもとに自作）', 28, DIM, 'ra')

    def box_(x0, y0, x1, y1, s, col):
        d.rounded_rectangle((x0 * S, y0 * S, x1 * S, y1 * S), 14 * S, fill=(7, 24, 36, 240), outline=col + (255,), width=3 * S)
        text(d, ((x0 + x1) / 2, (y0 + y1) / 2), s, 40, WHITE, 'mm')
    if k1 > 0:
        d0_ = int(255 * k1)
        box_(40, 20, 700, 100, '玉川上水の落とし水', BLUE)
        box_(40, 490, 960, 575, '湧き水（今の新宿御苑・明治神宮あたり）', BLUE)
        d.line([(340 * S, 100 * S), (340 * S, 200 * S), (600 * S, y * S)], fill=BLUE + (255,), width=6 * S, joint='curve')
        d.line([(340 * S, 500 * S), (340 * S, 400 * S), (600 * S, y * S)], fill=BLUE + (255,), width=6 * S, joint='curve')
        d.line([(600 * S, y * S), ((600 + 140 * k1) * S, y * S)], fill=BLUE + (255,), width=12 * S)
    if k2 > 0:
        end = 600 + 1060 * k2
        d.line([(600 * S, y * S), (end * S, y * S)], fill=BLUE + (255,), width=14 * S)
        text(d, (700, y + 40), '渋谷川', 48, BLUE, 'lm')
        if k2 > 0.3:
            ax = 1000
            d.line([(ax * S, 110 * S), (ax * S, y * S)], fill=(150, 215, 255, 255), width=8 * S)
            text(d, (ax + 18, 140), '宇田川と合流（渋谷駅の近く）', 40, WHITE, 'lm')
        if k2 > 0.95:
            circle(d, (1660, y), 14, fill=(7, 24, 36, 255), outline=GOLD + (255,), w=3)
            text(d, (1660, y - 50), '天現寺橋へ', 42, WHITE, 'mm')
    if k3 > 0:
        for i, xw in enumerate((1180, 1360, 1540)):
            if k3 < (i + 1) / 3 - .2:
                continue
            cy = y + 78
            circle(d, (xw, cy), 40, outline=ORG + (255,), w=5)
            for q in range(8):
                ang = q * math.pi / 4 + T(cx, at[2]) * .6
                d.line([(xw * S, cy * S), ((xw + 40 * math.cos(ang)) * S, (cy + 40 * math.sin(ang)) * S)], fill=ORG + (255,), width=4 * S)
        text(d, (1360, y + 170), '水車（いくつも営まれた）', 42, ORG, 'mm', alpha=int(255 * k3))
    commit(im, L, box, a)


DRAW_SHIBUYA['sb_edo'] = sb_edo
