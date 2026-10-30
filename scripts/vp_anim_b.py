"""自作アニメーション部品（その2）：経度線の地図（meridians）、15度ごとの時間の差（zones24）、GPSの測位（gpsdevice）、GPSの一方向の信号（gpstrack）。
vp_anim.py の末尾から読み込まれる（DRAW に登録）。図は模式図で、縮尺・位置は概略。"""
import math
from PIL import Image, ImageDraw
import vp_anim as A
from vp_anim import layer, commit, vs, text, circle, poly, arrow_head, ease, T, S, WHITE, GOLD, DIM, moving_dots

PANEL = (24, 52, 86, 255)
EDGE = (120, 150, 190, 255)
LINE = (150, 195, 245)
ORG = (255, 160, 100)
GRN = (130, 215, 160)
RED = (240, 100, 90)


def tlabel(d, xy, s, size, col=WHITE, anchor='mm', alpha=255, bg=(12, 34, 50)):
    """背景つきの文字（線や点の上でも読めるように）"""
    w = d.textlength(s, font=A.F[size * S]) / S
    x, y = xy
    x0 = x - w / 2 if anchor[0] == 'm' else (x if anchor[0] == 'l' else x - w)
    pad = 10
    d.rounded_rectangle(((x0 - pad) * S, (y - size * 0.75 - 4) * S, (x0 + w + pad) * S, (y + size * 0.75 + 4) * S), 10 * S, fill=bg + (int(215 * alpha / 255),))
    text(d, xy, s, size, col, anchor, alpha=alpha)


_GEO = {}


def _countries():
    if 'c' not in _GEO:
        import gm_geo
        _GEO['c'] = gm_geo.load()
    return _GEO['c']


def _fadein(t, dur=0.6):
    return ease(t / dur) if t >= 0 else 0.0


def _dashed(d, p, q, col, w=3, dash=14, gap=10):
    L = math.dist(p, q)
    if L <= 0:
        return
    n = int(L // (dash + gap)) + 1
    ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
    for i in range(n):
        s = i * (dash + gap)
        e = min(L, s + dash)
        poly(d, [(p[0] + ux * s, p[1] + uy * s), (p[0] + ux * e, p[1] + uy * e)], col, w)


# ------------------------------------------------------------------ 経度線の地図
def meridians(im, d0, cx, it, a):
    """日本付近の地図に、東経120・135・150度の線（mode='japan'）、または明石の位置（mode='akashi'）を示す。
    s_a: 3本の線／s_b: 135度を強調（グリニッジとの時差9時間）／s_c: 東京（約140度）／s_d: 国土の東西の真ん中（約138度、報道の数値）／s_e: 明石（akashiモード）"""
    box = it['box']; Z = 1.0
    L, d = layer(box, Z); W, H = vs(box, Z)
    mode = it.get('mode', 'japan')
    lon0, lon1 = it.get('lon', (119.0, 152.0)); lat0, lat1 = it.get('lat', (24.0, 46.0))
    sa, sb, sc, sd, se = (T(cx, it.get(k, None)) for k in ('s_a', 's_b', 's_c', 's_d', 's_e'))
    d.rounded_rectangle((8 * S, 8 * S, (W - 8) * S, (H - 8) * S), 20 * S, fill=PANEL, outline=EDGE, width=3 * S)
    mx0, my0, mx1, my1 = 24, 60, W - 24, H - 62          # 地図の領域
    cl = math.cos(math.radians((lat0 + lat1) / 2))
    sc_ = min((mx1 - mx0) / ((lon1 - lon0) * cl), (my1 - my0) / (lat1 - lat0))
    mw, mh = (lon1 - lon0) * cl * sc_, (lat1 - lat0) * sc_
    ox, oy = mx0 + ((mx1 - mx0) - mw) / 2, my0 + ((my1 - my0) - mh) / 2

    def P(lon, lat):
        return (ox + (lon - lon0) * cl * sc_, oy + (lat1 - lat) * sc_)

    Mp = Image.new('RGBA', (int(mw * S), int(mh * S)), (30, 70, 110, 255))
    md = ImageDraw.Draw(Mp)
    for c in _countries():
        if not c['rings']:
            continue
        nm = c['attr'].get('ADMIN', '')
        for ring in c['rings']:
            xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
            if max(xs) < lon0 - 1 or min(xs) > lon1 + 1 or max(ys) < lat0 - 1 or min(ys) > lat1 + 1:
                continue
            pts = [((x - lon0) * cl * sc_ * S, (lat1 - y) * sc_ * S) for x, y in ring]
            if len(pts) < 3:
                continue
            md.polygon(pts, fill=(112, 150, 112, 255) if nm == 'Japan' else (74, 98, 84, 255), outline=(190, 215, 190, 255))
    L.alpha_composite(Mp, (int(ox * S), int(oy * S)))
    # 経度線
    lines = it.get('lines', [120, 135, 150])
    x_at = lambda lon: P(lon, lat1)[0]
    if sa >= 0 or mode == 'akashi':
        k = ease(sa / 0.9) if mode != 'akashi' else 1.0
        for lon in lines:
            hi = (lon == 135 and (sb >= 0 or mode == 'akashi'))
            col = GOLD if hi else LINE
            x = x_at(lon)
            y_end = oy + mh * k
            poly(d, [(x, oy), (x, y_end)], col + (255,), 6 if hi else 3)
            if k > 0.9:
                text(d, (x, oy - 6), f'東経{lon}度', 28, col, 'mb')
    # 135度の説明
    if sb >= 0 and mode != 'akashi':
        k = _fadein(sb)
        x = x_at(135)
        text(d, (x + 14, oy + mh - 92), 'グリニッジより9時間進む', 26, GOLD, 'lm', alpha=int(255 * k))
        text(d, (x + 14, oy + mh - 58), '（国土のほぼ真ん中）', 26, GOLD, 'lm', alpha=int(255 * k))
    # 国土の東西の真ん中（報道の数値）
    if sd >= 0:
        k = _fadein(sd)
        x = x_at(138)
        _dashed(d, (x, oy), (x, oy + mh), (255, 190, 120, int(255 * k)), 3)
        text(d, (x + 12, oy + 28), '国土の東西の真ん中：約138度', 24, (255, 205, 150), 'lm', alpha=int(255 * k))
        text(d, (x + 12, oy + 58), '（神戸新聞の報道の数値）', 22, (255, 205, 150), 'lm', alpha=int(255 * k))
    # 東京
    if sc >= 0:
        k = _fadein(sc)
        p = P(139.69, 35.68)
        r = 10 + 5 * (1 - k)
        circle(d, p, r, fill=(255, 130, 110, int(255 * k)), outline=WHITE + (int(255 * k),), w=2)
        text(d, (p[0] + 16, p[1] + 30), '東京：約140度', 26, (255, 170, 150), 'lm', alpha=int(255 * k))
    # 明石
    if se >= 0 or (mode == 'akashi' and sa >= 0):
        k = _fadein(se if se >= 0 else sa)
        p = P(134.99, 34.65)
        for rr, al in ((26, 70), (18, 130)):
            circle(d, p, rr * (0.6 + 0.4 * k), fill=(255, 215, 90, int(al * k)))
        circle(d, p, 9, fill=GOLD + (int(255 * k),), outline=WHITE + (int(255 * k),), w=2)
        text(d, (p[0] - 18, p[1] + 38), '明石市', 30, GOLD, 'rm', alpha=int(255 * k))
        if mode == 'akashi':
            pt = P(139.69, 35.68)
            circle(d, pt, 7, fill=(255, 130, 110, 255), outline=WHITE + (255,), w=2)
            text(d, (pt[0] + 14, pt[1] + 26), '東京', 24, (255, 170, 150), 'lm')
    text(d, (W / 2, H - 28), '模式図：海岸線と国境はNatural Earth(110m)を簡略に描いたもので、線の位置は概略です', 22, DIM, 'mm')
    commit(im, L, box, a)


# ------------------------------------------------------------------ 15度ごとの時間の差
def zones24(im, d0, cx, it, a):
    """北極側から見た地球の模式図。s_a: 約1日で1周／s_b: 360度を24等分（15度）／s_c: 15度で1時間の差／s_d: 基準の線は15度の整数倍が多い"""
    box = it['box']; L, d = layer(box, 1.0); W, H = vs(box, 1.0)
    sa, sb, sc, sd = (T(cx, it.get(k, None)) for k in ('s_a', 's_b', 's_c', 's_d'))
    d.rounded_rectangle((8 * S, 8 * S, (W - 8) * S, (H - 8) * S), 20 * S, fill=PANEL, outline=EDGE, width=3 * S)
    c0 = (W / 2, H / 2 + 6); R = min(W, H) / 2 - 60
    circle(d, c0, R, fill=(36, 96, 150, 255), outline=(200, 225, 255, 255), w=4)
    circle(d, c0, R * 0.12, fill=(230, 240, 255, 255))
    # グリニッジの線（0度）は上
    if sb >= 0:
        k = ease(sb / 1.2)
        for i in range(24):
            if i / 24 > k:
                break
            ang = math.radians(-90 + i * 15)
            p = (c0[0] + R * math.cos(ang), c0[1] + R * math.sin(ang))
            q = (c0[0] + R * 0.12 * math.cos(ang), c0[1] + R * 0.12 * math.sin(ang))
            poly(d, [q, p], (190, 220, 250, 200), 2)
        if k >= 1:
            text(d, (c0[0] + R + 36, c0[1] - 6), '360° ÷ 24 ＝ 15°', 34, WHITE, 'lm')
    if sa >= 0 and sb < 0:
        text(d, (c0[0] + R + 36, c0[1] - 6), '約1日で1周（360°）', 34, WHITE, 'lm', alpha=int(255 * _fadein(sa)))
    # 自転の矢印（反時計回り）
    if sa >= 0:
        k = _fadein(sa)
        pts = [(c0[0] + (R * 0.62) * math.cos(math.radians(-90 - t)), c0[1] + (R * 0.62) * math.sin(math.radians(-90 - t))) for t in range(0, 281, 5)]
        poly(d, pts, (255, 215, 90, int(255 * k)), 5)
        arrow_head(d, pts[-2], pts[-1], (255, 215, 90, int(255 * k)), 22)
    # 15度のくさび
    if sc >= 0:
        k = _fadein(sc)
        a0, a1 = math.radians(-90), math.radians(-75)
        pts = [c0] + [(c0[0] + R * math.cos(a0 + (a1 - a0) * i / 12), c0[1] + R * math.sin(a0 + (a1 - a0) * i / 12)) for i in range(13)]
        d.polygon([(x * S, y * S) for x, y in pts], fill=(255, 215, 90, int(190 * k)))
        text(d, (c0[0] + 120, c0[1] - R - 22), '経度15度＝太陽の時刻で、1時間の差', 30, GOLD, 'lm', alpha=int(255 * k))
    # 標準時の基準の線に選ばれやすい線
    if sd >= 0:
        k = _fadein(sd)
        for i in range(24):
            ang = math.radians(-90 + i * 15)
            p = (c0[0] + R * math.cos(ang), c0[1] + R * math.sin(ang))
            circle(d, p, 9, fill=(255, 190, 120, int(255 * k)), outline=WHITE + (int(255 * k),), w=2)
        text(d, (c0[0] - R - 36, c0[1] - 8), '標準時の基準の線', 30, (255, 205, 150), 'rm', alpha=int(255 * k))
        text(d, (c0[0] - R - 36, c0[1] + 28), '15度の整数倍が、選ばれることが多い', 24, (255, 205, 150), 'rm', alpha=int(255 * k))
    text(d, (c0[0] - 14, c0[1] - R - 22), '0°（グリニッジ）', 26, WHITE, 'rm')
    poly(d, [(c0[0], c0[1] - R - 8), (c0[0], c0[1] - R * 0.12)], (255, 215, 90, 255), 4)
    text(d, (W / 2, H - 26), '北極側から見た模式図（国立天文台の説明をもとにした自作の図です）', 22, DIM, 'mm')
    commit(im, L, box, a)


# ------------------------------------------------------------------ GPSの測位
def _sat(d, c, size=1.0, col=(235, 240, 250)):
    x, y = c
    w, h = 26 * size, 18 * size
    d.rectangle(((x - w / 2) * S, (y - h / 2) * S, (x + w / 2) * S, (y + h / 2) * S), fill=col + (255,), outline=(120, 150, 190, 255), width=S)
    for sgn in (-1, 1):
        x0 = x + sgn * (w / 2 + 6 * size)
        d.rectangle(((x0 - 20 * size) * S, (y - 9 * size) * S, (x0 + 20 * size) * S, (y + 9 * size) * S), fill=(90, 150, 225, 255), outline=(200, 225, 255, 255), width=S)
    d.line(((x - w / 2) * S, y * S, (x - w / 2 - 6 * size) * S, y * S), fill=col + (255,), width=2 * S)
    d.line(((x + w / 2) * S, y * S, (x + w / 2 + 6 * size) * S, y * S), fill=col + (255,), width=2 * S)


def _phone(d, c, size=1.0, glow=0.0):
    x, y = c
    if glow > 0:
        for rr, al in ((90, 50), (62, 90)):
            circle(d, c, rr * (0.7 + 0.3 * glow), fill=(255, 215, 90, int(al * glow)))
    d.rounded_rectangle(((x - 30 * size) * S, (y - 52 * size) * S, (x + 30 * size) * S, (y + 52 * size) * S), 10 * S, fill=(20, 30, 45, 255), outline=(220, 230, 245, 255), width=3 * S)
    d.rounded_rectangle(((x - 24 * size) * S, (y - 42 * size) * S, (x + 24 * size) * S, (y + 40 * size) * S), 5 * S, fill=(40, 80, 130, 255))


def gpsdevice(im, d0, cx, it, a):
    """GPSの測位。s_a: 衛星が電波を送る→端末／s_b: 時間×光の速さ＝おおよその距離（輪）／s_c: 端末の時計のずれ／s_d: 4基以上／s_e: 求めるものは4つ／s_f: 位置が分かる"""
    box = it['box']; L, d = layer(box, 1.0); W, H = vs(box, 1.0)
    sa, sb, sc, sd, se, sf = (T(cx, it.get(k, None)) for k in ('s_a', 's_b', 's_c', 's_d', 's_e', 's_f'))
    d.rounded_rectangle((8 * S, 8 * S, (W - 8) * S, (H - 8) * S), 20 * S, fill=PANEL, outline=EDGE, width=3 * S)
    ph = (W * 0.5, H - 120)
    # 地面
    d.rectangle((24 * S, (H - 50) * S, (W - 24) * S, (H - 24) * S), fill=(48, 110, 80, 255))
    sats = [(W * 0.18, 90), (W * 0.42, 62), (W * 0.64, 70), (W * 0.86, 100)]
    shown = [sa >= 0, sd >= 0, sd >= 0, sd >= 0]
    cols = [(255, 190, 110), (150, 215, 255), (150, 235, 170), (225, 170, 255)]
    t = cx.t
    for i, (sp, on) in enumerate(zip(sats, shown)):
        if not on:
            continue
        k = _fadein(sa if i == 0 else sd)
        col = cols[i]
        _sat(d, sp, 1.7)
        # 電波（衛星→端末の一方向）
        poly(d, [sp, ph], col + (int(110 * k),), 2)
        moving_dots(d, [(sp[0] + (ph[0] - sp[0]) * 0.0, sp[1] + 24), (ph[0] + (sp[0] - ph[0]) * 0.12, ph[1] - 58 + (sp[1] - ph[1] + 58) * 0.12)], col + (int(255 * k),), t + i * 0.3, n=4, r=7, speed=210)
        if sb >= 0 and (i == 0 or sd >= 0):
            kk = ease(((sb if i == 0 else sd) - 0.1) / 0.8)
            dist = math.dist(sp, ph)
            ang = math.degrees(math.atan2(ph[1] - sp[1], ph[0] - sp[0]))
            box_ = ((sp[0] - dist) * S, (sp[1] - dist) * S, (sp[0] + dist) * S, (sp[1] + dist) * S)
            d.arc(box_, ang - 14 * kk, ang + 14 * kk, fill=col + (230,), width=4 * S)
    # ラベル
    if sa >= 0:
        text(d, (sats[0][0], 40), '衛星：位置・状態・時刻を電波で送る', 26, (255, 205, 150), 'lm', alpha=int(255 * _fadein(sa))) if False else None
        tlabel(d, (sats[0][0], 150), '位置・状態・時刻を電波で送る', 26, (255, 205, 150), 'mm', alpha=int(255 * _fadein(sa)))
    _phone(d, ph, 1.0, glow=ease(sf / 0.8) if sf >= 0 else 0)
    text(d, (ph[0], ph[1] + 70), '端末', 28, WHITE, 'mm')
    if sb >= 0:
        tlabel(d, (W * 0.5, 230), '時間 × 光の速さ ＝ おおよその距離', 32, GOLD, 'mm', alpha=int(255 * _fadein(sb)))
    if sc >= 0:
        k = _fadein(sc)
        cc = (ph[0] + 150, ph[1] - 20)
        circle(d, cc, 36, fill=(250, 250, 245, int(255 * k)), outline=(255, 120, 100, int(255 * k)), w=4)
        ang = math.radians(-90 + 25 * math.sin(t * 4))
        poly(d, [cc, (cc[0] + 24 * math.cos(ang), cc[1] + 24 * math.sin(ang))], (40, 40, 50, int(255 * k)), 4)
        tlabel(d, (cc[0] + 52, cc[1]), '端末の時計：ずれがある', 28, (255, 150, 130), 'lm', alpha=int(255 * k))
    if se >= 0:
        k = _fadein(se)
        items = ['東西', '南北', '高さ', '時計のずれ']
        x0 = 60
        text(d, (x0, H - 330), '求めるもの：4つ', 30, GOLD, 'lm', alpha=int(255 * k))
        for j, s_ in enumerate(items):
            y = H - 285 + j * 46
            d.rounded_rectangle((x0 * S, (y - 18) * S, (x0 + 200) * S, (y + 18) * S), 10 * S, fill=(12, 34, 50, int(255 * k)), outline=GOLD + (int(255 * k),), width=2 * S)
            text(d, (x0 + 100, y), s_, 26, WHITE, 'mm', alpha=int(255 * k))
    if sd >= 0:
        tlabel(d, (W - 50, H - 300), '通常は、4基以上の衛星の電波を使う', 28, WHITE, 'rm', alpha=int(255 * _fadein(sd)))
    if sf >= 0:
        tlabel(d, (ph[0] - 120, ph[1] - 10), '緯度・経度・高さが分かる', 30, GOLD, 'rm', alpha=int(255 * _fadein(sf)))
    commit(im, L, box, a)


# ------------------------------------------------------------------ GPSの一方向の信号
def gpstrack(im, d0, cx, it, a):
    """衛星→端末は一方向。s_a: 衛星が信号を送る／s_b: 灯台のように一方向／s_c: 端末の位置は衛星に届かない（GPS.govのFAQ）"""
    box = it['box']; L, d = layer(box, 1.0); W, H = vs(box, 1.0)
    sa, sb, sc = (T(cx, it.get(k, None)) for k in ('s_a', 's_b', 's_c'))
    d.rounded_rectangle((8 * S, 8 * S, (W - 8) * S, (H - 8) * S), 20 * S, fill=PANEL, outline=EDGE, width=3 * S)
    d.rectangle((24 * S, (H - 50) * S, (W - 24) * S, (H - 24) * S), fill=(48, 110, 80, 255))
    sp = (W * 0.36, 78)
    t = cx.t
    phones = [(W * 0.10, H - 105), (W * 0.36, H - 112), (W * 0.62, H - 105)]
    _sat(d, sp, 1.9)
    if sa >= 0:
        k = _fadein(sa)
        for j in range(4):                       # 広がる電波（外向き）
            rr = 40 + ((t * 120 + j * 100) % 420)
            al = int(150 * k * max(0.0, 1 - rr / 460))
            d.arc(((sp[0] - rr) * S, (sp[1] - rr) * S, (sp[0] + rr) * S, (sp[1] + rr) * S), 55, 125, fill=(150, 215, 255, al), width=4 * S)
        for i, ph in enumerate(phones):
            moving_dots(d, [(sp[0], sp[1] + 30), (ph[0], ph[1] - 62)], (150, 215, 255, int(255 * k)), t + i * 0.2, n=3, r=6, speed=200)
    for ph in phones:
        _phone(d, ph, 0.8)
    if sa >= 0:
        text(d, (sp[0] + 90, sp[1] - 4), 'GPS衛星', 30, WHITE, 'lm')
    # 灯台
    if sb >= 0:
        k = _fadein(sb)
        lx, ly = W * 0.84, H - 56
        d.polygon([((lx - 30) * S, ly * S), ((lx + 30) * S, ly * S), ((lx + 18) * S, (ly - 230) * S), ((lx - 18) * S, (ly - 230) * S)], fill=(235, 235, 240, int(255 * k)), outline=(120, 150, 190, int(255 * k)))
        d.polygon([((lx - 26) * S, (ly - 230) * S), ((lx + 26) * S, (ly - 230) * S), (lx * S, (ly - 270) * S)], fill=(230, 90, 80, int(255 * k)))
        d.rectangle(((lx - 18) * S, (ly - 262) * S, (lx + 18) * S, (ly - 232) * S), fill=(255, 235, 150, int(255 * k)))
        for sgn in (-1, 1):
            d.polygon([(lx * S, (ly - 248) * S), ((lx + sgn * 230) * S, (ly - 290) * S), ((lx + sgn * 230) * S, (ly - 206) * S)], fill=(255, 240, 160, int(70 * k)))
        tlabel(d, (lx, ly - 300), '灯台：光を出すだけ', 26, WHITE, 'mm', alpha=int(255 * k))
        tlabel(d, (W * 0.5, 190), '灯台のように、一方向に、信号を送るだけ', 32, GOLD, 'mm', alpha=int(255 * k))
    # 端末→衛星（届かない）
    if sc >= 0:
        k = _fadein(sc)
        for ph in phones[1:2]:
            _dashed(d, (ph[0] + 54, ph[1] - 66), (sp[0] + 54, sp[1] + 44), (255, 130, 110, int(200 * k)), 4)
            mid = ((ph[0] + sp[0]) / 2 + 54, (ph[1] + sp[1]) / 2 - 10)
            poly(d, [(mid[0] - 22, mid[1] - 22), (mid[0] + 22, mid[1] + 22)], (255, 90, 80, int(255 * k)), 8)
            poly(d, [(mid[0] - 22, mid[1] + 22), (mid[0] + 22, mid[1] - 22)], (255, 90, 80, int(255 * k)), 8)
        text(d, (W * 0.5 + 100, H * 0.5 + 90), '運用する政府は、端末の位置を特定できない（GPS.gov FAQ）', 26, (255, 170, 150), 'lm', alpha=int(255 * k)) if False else None
        tlabel(d, (W * 0.5 + 150, H * 0.5 + 30), '端末の位置は、衛星には届かない', 28, (255, 170, 150), 'lm', alpha=int(255 * k))
    text(d, (W / 2, H - 28), '模式図（GPS.govのFAQの説明をもとにした自作の図です）', 22, DIM, 'mm')
    commit(im, L, box, a)


DRAW_B = dict(meridians=meridians, zones24=zones24, gpsdevice=gpsdevice, gpstrack=gpstrack)
