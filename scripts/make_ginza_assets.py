"""銀座（ginza）の素材を作る。国土地理院のタイルから、空中写真3年代と、標高の色別図（5mメッシュ）、
埋め立ての段階を示す模式図（fillmap_0..3）を作る。

出典：国土地理院（ort_riku10=1936〜42年頃、ort_old10=1961〜69年、seamlessphoto=全国最新写真、dem5a_png）。加工して作成。
usage: python scripts/make_ginza_assets.py [photos|relief|fillmap|all]

見せ場：江戸前島（砂州の微高地）と、その両側を埋め立てた低地の段差。銀座は砂州の先端ちかく。
fillmap は標高だけを土台に、水・砂州・埋め立ての範囲を手で描いた模式図。位置と形は模式化してある。
"""
import io, math, sys, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'assets' / 'ginza'
OUT.mkdir(parents=True, exist_ok=True)
CENTER = (35.6745, 139.7690)   # 銀座〜京橋〜築地
FRAME = (1060, 720)


def tile(l, z, x, y, ext='png'):
    return Image.open(io.BytesIO(urllib.request.urlopen(
        f'https://cyberjapandata.gsi.go.jp/xyz/{l}/{z}/{x}/{y}.{ext}', timeout=30).read())).convert('RGB')


def xy(lat, lon, z):
    n = 2 ** z
    return (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n


def photos():
    z, R = 17, 2
    fx, fy = xy(CENTER[0], CENTER[1], z)
    x0, y0 = int(fx), int(fy)
    for name, l, ext in [('aerial_1936', 'ort_riku10', 'png'), ('aerial_1961', 'ort_old10', 'png'),
                         ('aerial_now', 'seamlessphoto', 'jpg')]:
        im = Image.new('RGB', (256 * (2 * R + 1),) * 2)
        for i in range(-R, R + 1):
            for j in range(-R, R + 1):
                im.paste(tile(l, z, x0 + i, y0 + j, ext), ((i + R) * 256, (j + R) * 256))
        im.save(OUT / f'{name}.png')
        print('photo', name, im.size)


# 銀座のまわり。砂州のうえ（銀座・京橋）と、その両側の低地を比べる
PTS = {'皇居・本丸': (35.6850, 139.7560), '日本橋': (35.6839, 139.7744),
       '京橋': (35.6760, 139.7696), '銀座四丁目': (35.6713, 139.7650),
       '築地本願寺': (35.6666, 139.7717), '汐留': (35.6648, 139.7596)}


def _crop_box(pts_px, size, w, h):
    cx = sum(p[0] for p in pts_px) / len(pts_px)
    cy = sum(p[1] for p in pts_px) / len(pts_px)
    x0 = int(min(max(cx - w / 2, 0), size - w))
    y0 = int(min(max(cy - h / 2, 0), size - h))
    return (x0, y0, x0 + w, y0 + h)


def grid(z=15, R=2):
    cx, cy = xy(CENTER[0], CENTER[1], z)
    return z, int(cx) - R, int(cy) - R, 256 * (2 * R + 1)


def dem(z=15, R=2):
    z, X0, Y0, N = grid(z, R)
    D = np.zeros((N, N))
    for i in range(2 * R + 1):
        for j in range(2 * R + 1):
            t = np.array(tile('dem5a_png', z, X0 + i, Y0 + j)).astype(np.int64)
            raw = t[..., 0] * 65536 + t[..., 1] * 256 + t[..., 2]
            v = np.where(raw >= 8388608, raw - 16777216, raw) * 0.01
            v[raw == 8388608] = np.nan
            D[j * 256:(j + 1) * 256, i * 256:(i + 1) * 256] = v
    m = np.isnan(D)
    if m.any():
        D = D[tuple(ndi.distance_transform_edt(m, return_distances=False, return_indices=True))]
    return D, X0, Y0, N


def relief():
    Z = 15
    D, X0, Y0, N = dem(Z)
    pts = {}
    for k, (la, lo) in PTS.items():
        fx, fy = xy(la, lo, Z)
        x, y = int((fx - X0) * 256), int((fy - Y0) * 256)
        pts[k] = (float(np.mean(D[y - 4:y + 5, x - 4:x + 5])), (x, y))
    gy, gx = np.gradient(D, 5.0)
    az, alt = math.radians(315), math.radians(40)
    slope, asp = np.arctan(2.0 * np.hypot(gx, gy)), np.arctan2(-gx, gy)
    hs = np.clip(np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - asp), 0, 1)
    t = np.clip((D - 1) / (25 - 1), 0, 1)
    stops = [(0, (46, 96, 150)), (.25, (70, 150, 150)), (.5, (150, 185, 110)),
             (.75, (225, 205, 120)), (1, (235, 235, 225))]
    out = np.zeros(t.shape + (3,))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        f = ((t - a) / (b - a))[..., None]
        out = np.where(((t >= a) & (t <= b))[..., None], np.array(ca) * (1 - f) + np.array(cb) * f, out)
    im = Image.fromarray(np.clip(out * (0.55 + 0.45 * hs[..., None]), 0, 255).astype('uint8'))
    box = _crop_box([p[1] for p in pts.values()], N, *FRAME)
    im.crop(box).save(OUT / 'relief_plain.png')
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype('C:/Windows/Fonts/NotoSansJP-VF.ttf', 34)
    f.set_variation_by_axes([700])
    for k, (v, (x, y)) in pts.items():
        X, Y = x, y
        d.ellipse((X - 8, Y - 8, X + 8, Y + 8), fill=(255, 90, 80), outline=(255, 255, 255), width=3)
        s = f'{k} {v:.1f}m'
        w = d.textlength(s, font=f)
        tx = min(max(X + 12, 6), im.width - w - 10)
        d.rectangle((tx - 6, Y - 24, tx + w + 6, Y + 24), fill=(7, 24, 36))
        d.text((tx, Y - 21), s, font=f, fill=(245, 243, 232))
    im.crop(box).save(OUT / 'relief.png')
    print({k: round(v[0], 2) for k, v in pts.items()})


# ---------------------------------------------------------------- 模式図：砂州の両側が埋まる
FILL_FRAME = (1160, 795)
FILL_CENTER = (35.6760, 139.7690)
SEA_COL, COAST_COL = (92, 156, 204), (46, 96, 148)
BAR_COL, BAR_EDGE = (244, 213, 132), (146, 112, 58)
RIVER_COL = (72, 136, 188)
FILL_EDGE = (128, 92, 52)
ROAD_COL = (168, 166, 160)

# 江戸前島の軸（＝中央通りの尾根筋）。日本橋 → 京橋 → 銀座 → 汐留
AXIS = [(35.6900, 139.7735), (35.6839, 139.7744), (35.6760, 139.7696),
        (35.6713, 139.7650), (35.6648, 139.7596)]
HALF = 0.0030          # 軸から東西への半幅（度）。約550m幅の模式化


def _offset(pts, dlon):
    return [(la, lo + dlon) for la, lo in pts]


# 江戸前島（砂州の半島）。西の縁を南下し、東の縁を北上して閉じる
BAR = _offset(AXIS, -HALF) + list(reversed(_offset(AXIS, HALF)))
# 西の日比谷入江（台地との間）
SEA_W = _offset(AXIS, -HALF) + [(35.6650, 139.7626), (35.6520, 139.7626), (35.6520, 139.7505),
                                (35.6930, 139.7505), (35.6930, 139.7705)]
# 東の江戸湾（東の縁から外側）
SEA_E = list(reversed(_offset(AXIS, HALF))) + [(35.6520, 139.7626), (35.6520, 139.7980),
                                               (35.6930, 139.7980), (35.6930, 139.7765)]
# 堀（1949〜64年に埋められて道路になった）。4本で銀座を囲んでいた
MOATS = {
    '三十間堀川': _offset(AXIS, 0.0016),
    '外堀': _offset(AXIS, -0.0022),
    '京橋川': [(35.6792, 139.7660), (35.6812, 139.7740), (35.6838, 139.7810)],
    '汐留川': [(35.6646, 139.7570), (35.6652, 139.7650), (35.6644, 139.7726)],
}
BAR_ANG = 52.0
STAGES = [dict(kind='west', col=(206, 182, 142), lab='① 1603年〜　西の入り江 → 台地',
               names=[('① 日本橋台地', 35.6790, 139.7662, 26)]),
          dict(kind='east', col=(222, 198, 158), lab='② 1657年〜　東の海 → 築地',
               names=[('② 築地', 35.6660, 139.7708, 26), ('佃島', 35.6680, 139.7838, 24)]),
          dict(kind='moat', col=ROAD_COL, lab='③ 1949〜64年　堀 → 道路',
               names=[('③ 外堀通り', 35.6712, 139.7600, 24), ('昭和通り', 35.6726, 139.7684, 24)])]


def _font(size, w=700):
    f = ImageFont.truetype('C:/Windows/Fonts/NotoSansJP-VF.ttf', size)
    f.set_variation_by_axes([w])
    return f


def _box(center, frame, z=15):
    z, X0, Y0, N = grid(z, 2)
    fx, fy = xy(center[0], center[1], z)
    x0 = min(max(int(round((fx - X0) * 256 - frame[0] / 2)), 0), N - frame[0])
    y0 = min(max(int(round((fy - Y0) * 256 - frame[1] / 2)), 0), N - frame[1])
    return (x0, y0, x0 + frame[0], y0 + frame[1])


def _ll2px(pts, box, z=15):
    _, X0, Y0, _ = grid(z, 2)
    out = []
    for la, lo in pts:
        fx, fy = xy(la, lo, z)
        out.append(((fx - X0) * 256 - box[0], (fy - Y0) * 256 - box[1]))
    return out


def _chip(d, x, y, text, size=30, fg=(255, 255, 255), bg=(34, 30, 54, 215), anchor='lt', pad=None):
    f = _font(size)
    pad = int(size * .45) if pad is None else pad
    w, h = d.textlength(text, font=f) + pad * 2, int(size * 1.36) + pad
    if anchor in ('mm', 'cm'):
        x, y = x - w / 2, y - h / 2
    elif anchor == 'rt':
        x = x - w
    elif anchor in ('lm', 'la'):
        y = y - h / 2 if anchor == 'lm' else y
    d.rounded_rectangle((x, y, x + w, y + h), min(16, h / 2), fill=bg)
    d.text((x + pad, y + h / 2 - 1), text, font=f, fill=fg, anchor='lm')
    return int(w), int(h)


def _rot_text(im, x, y, text, size, angle, fg=(255, 255, 255), stroke=(38, 34, 62), sw=5):
    f = _font(size)
    d0 = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    w, h = int(d0.textlength(text, font=f)) + sw * 2 + 6, size + sw * 2 + 8
    t = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(t).text((w / 2, h / 2), text, font=f, fill=fg, stroke_width=sw, stroke_fill=stroke, anchor='mm')
    t = t.rotate(angle, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(t, (int(x - t.width / 2), int(y - t.height / 2)))


def fillmap():
    """fillmap_0=砂州と両側の海。fillmap_1..3=西→東→堀の順に埋めた範囲（累積）。"""
    z, R = 15, 2
    D, X0, Y0, N = dem(z, R)
    box = _box(FILL_CENTER, FILL_FRAME, z)
    W, H = FILL_FRAME
    d = ndi.gaussian_filter(D[box[1]:box[3], box[0]:box[2]], 1.2)
    gy, gx = np.gradient(d, 5.0)
    az, alt = math.radians(315), math.radians(40)
    slope, asp = np.arctan(2.0 * np.hypot(gx, gy)), np.arctan2(-gx, gy)
    hs = np.clip(np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - asp), 0, 1)
    t = np.clip((d - 2) / 18.0, 0, 1)[..., None]
    arr = np.array([238., 232., 214.]) * (1 - t) + np.array([201., 211., 181.]) * t
    arr = arr * (0.87 + 0.16 * hs[..., None])

    SS = 3

    def amask(polys, width=0, closed=True):
        m = Image.new('L', (W * SS, H * SS), 0)
        g = ImageDraw.Draw(m)
        for p in polys:
            if width:
                seq = list(p) + ([p[0]] if closed else [])
                g.line([(x * SS, y * SS) for x, y in seq], fill=255, width=width * SS, joint='curve')
            else:
                g.polygon([(x * SS, y * SS) for x, y in p], fill=255)
        return np.asarray(m.resize((W, H), Image.LANCZOS)).astype(float) / 255.

    def paint(a, col):
        nonlocal arr
        k = a[..., None]
        arr = arr * (1 - k) + np.array(col, float) * k

    sea_w, sea_e = _ll2px(SEA_W, box), _ll2px(SEA_E, box)
    bar_px = _ll2px(BAR, box)
    moat_px = [_ll2px(p, box) for p in MOATS.values()]

    paint(amask([sea_w]), SEA_COL)
    paint(amask([sea_e]), SEA_COL)
    paint(amask([sea_w, sea_e], 3) * .5, COAST_COL)
    paint(amask([bar_px]), BAR_COL)
    paint(amask([bar_px], 3) * .65, BAR_EDGE)
    for mp in moat_px:
        paint(amask([mp], 7, closed=False), RIVER_COL)

    im = Image.fromarray(np.clip(arr, 0, 255).astype('uint8')).convert('RGBA')
    dr = ImageDraw.Draw(im)
    P = lambda la, lo: _ll2px([(la, lo)], box)[0]
    w, _ = _chip(dr, 18, 14, '江戸前島と銀座', 38)
    _chip(dr, 18 + w + 10, 24, '模式図', 23, fg=(58, 44, 24), bg=(238, 228, 192, 240))
    _chip(dr, *P(35.6830, 139.7476), '本丸台地', 28, anchor='mm')
    _rot_text(im, *P(35.6778, 139.7702), '江戸前島', 30, BAR_ANG)
    dr.text(P(35.6655, 139.7880), '江戸湾', font=_font(34), fill=(255, 255, 255), anchor='mm',
            stroke_width=6, stroke_fill=(40, 70, 110))
    _chip(dr, *P(35.6788, 139.7552), '日比谷入江', 27, anchor='mm')
    _chip(dr, *P(35.6846, 139.7748), '日本橋', 24, anchor='mm')
    _chip(dr, *P(35.6702, 139.7636), '銀座', 26, anchor='mm', bg=(120, 40, 30, 230))
    _chip(dr, *P(35.6652, 139.7582), '汐留', 24, anchor='mm')
    _chip(dr, *P(35.6812, 139.7792), '京橋川', 21, anchor='mm', bg=(30, 62, 96, 220))
    _chip(dr, *P(35.6724, 139.7680), '三十間堀川', 21, anchor='mm', bg=(30, 62, 96, 220))
    _chip(dr, *P(35.6716, 139.7586), '外堀', 21, anchor='mm', bg=(30, 62, 96, 220))
    _chip(dr, *P(35.6630, 139.7666), '汐留川', 21, anchor='mm', bg=(30, 62, 96, 220))
    dr.text((W - 14, H - 12), '国土地理院の標高データから作成・位置と形は模式化', font=_font(20, 500),
            fill=(255, 255, 255), anchor='rs', stroke_width=4, stroke_fill=(32, 52, 78))
    im.convert('RGB').save(OUT / 'fillmap_0.png')

    sea = (amask([sea_w]) > .5) | (amask([sea_e]) > .5)
    moat = np.zeros((H, W), bool)
    for mp in moat_px:
        moat |= amask([mp], 7, closed=False) > .5
    n = 2 ** z
    ys = (Y0 * 256 + box[1] + np.arange(H) + .5) / 256 / n
    lats = np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * ys))))[:, None]

    cum = np.zeros_like(sea)
    for i, st in enumerate(STAGES, 1):
        if st['kind'] == 'west':
            new = amask([sea_w]) > .5
        elif st['kind'] == 'east':
            new = (amask([sea_e]) > .5) & (lats < 35.6800)
        else:
            new = moat & ~cum
        cum = cum | new
        a = np.zeros((H, W, 4), float)
        a[..., :3] = st['col']
        a[..., 3] = new * 255.
        if st['kind'] == 'moat':
            a[ndi.binary_dilation(new, np.ones((2, 2), bool)) & ~new] = (70, 70, 70, 255.)
        else:
            edge = new & ndi.binary_dilation(~new & ~moat, np.ones((4, 4), bool))
            a[ndi.binary_dilation(edge, np.ones((2, 2), bool))] = FILL_EDGE + (255.,)
        s = Image.fromarray(np.clip(a, 0, 255).astype('uint8'))
        ds = ImageDraw.Draw(s)
        for txt, la, lo_, sz in st['names']:
            _chip(ds, *P(la, lo_), txt, sz, anchor='mm', bg=(40, 34, 26, 220))
        _chip(ds, W - 16, 556 + (i - 1) * 52, st['lab'], 28, fg=(255, 255, 255), bg=(40, 34, 26, 225), anchor='rt')
        s.save(OUT / f'fillmap_{i}.png')
    print('fillmap', FILL_FRAME, 'box', box)


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('photos', 'all'):
        photos()
    if what in ('relief', 'all'):
        relief()
    if what in ('fillmap', 'all'):
        fillmap()
