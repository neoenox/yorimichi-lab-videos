"""深川・木場（fukagawa）の素材を作る。国土地理院のタイルから、空中写真3年代と、標高の色別図（5mメッシュ）、
埋め立ての段階を示す模式図（fillmap_0..3）を作る。

出典：国土地理院（ort_riku10=1936〜42年頃、ort_old10=1961〜69年、seamlessphoto=全国最新写真、dem5a_png）。加工して作成。
usage: python scripts/make_fukagawa_assets.py [photos|relief|fillmap|all]

見せ場：深川地域（門前仲町・清澄白河・木場・東陽・豊洲）は海抜0〜3mの超低地。
銀座（約4m）よりさらに低い＝東京湾最奥の入り江の最深部だった。
fillmap は標高だけを土台に、干潟・自然河川・運河網・木場・埋め立ての範囲を手で描いた模式図。位置と形は模式化してある。
"""
import io, math, sys, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'assets' / 'fukagawa'
OUT.mkdir(parents=True, exist_ok=True)
CENTER = (35.6720, 139.8000)   # 門前仲町〜木場〜豊洲
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


# 深川のまわり。超低地（0-3m）と、隅田川・運河網を比べる
PTS = {'門前仲町': (35.6748, 139.7985), '清澄白河': (35.6837, 139.7960),
       '木場三丁目': (35.6713, 139.8074), '東陽四丁目': (35.6652, 139.8220),
       '豊洲四丁目': (35.6570, 139.7880), '隅田川・佃': (35.6680, 139.7830)}


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
    # 深川は 0〜5m に収まるので、色の幅を低地側へ極端に寄せる
    t = np.clip((D - 0) / (5 - 0), 0, 1)
    stops = [(0, (30, 80, 140)), (.2, (50, 130, 150)), (.4, (90, 170, 130)),
             (.6, (160, 200, 110)), (.8, (220, 220, 130)), (1, (235, 235, 225))]
    out = np.zeros(t.shape + (3,))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        f = ((t - a) / (b - a))[..., None]
        out = np.where(((t >= a) & (t <= b))[..., None], np.array(ca) * (1 - f) + np.array(cb) * f, out)
    im = Image.fromarray(np.clip(out * (0.5 + 0.5 * hs[..., None]), 0, 255).astype('uint8'))
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


# ---------------------------------------------------------------- 模式図：入り江の奥が埋まる
FILL_FRAME = (1160, 795)
FILL_CENTER = (35.6720, 139.8050)
SEA_COL, COAST_COL = (70, 130, 180), (30, 70, 120)
BAR_COL, BAR_EDGE = (244, 213, 132), (146, 112, 58)
RIVER_COL = (72, 136, 188)
FILL_EDGE = (128, 92, 52)
CANAL_COL = (100, 160, 200)

# 自然の入り江（隅田川河口から北へ広がる干潟・湿地）
SEA = [(35.6900, 139.7900), (35.6820, 139.7850), (35.6750, 139.7800), (35.6680, 139.7780),
       (35.6620, 139.7750), (35.6580, 139.7780), (35.6550, 139.7950), (35.6550, 139.8300),
       (35.6920, 139.8300), (35.6920, 139.8000), (35.6880, 139.7950)]

# 自然河川（隅田川・大横川・北十間川の古い流れ）
NATURAL_RIVERS = {
    '隅田川': [(35.6900, 139.7920), (35.6820, 139.7880), (35.6740, 139.7840), (35.6680, 139.7800)],
    '大横川': [(35.6820, 139.7880), (35.6800, 139.8000), (35.6750, 139.8100), (35.6700, 139.8180)],
    '北十間川': [(35.6780, 139.8000), (35.6760, 139.8120), (35.6720, 139.8200)],
}

# 運河網（人工的に掘削された格子状の川）
CANALS = {
    '横十間川': [(35.6760, 139.7980), (35.6760, 139.8250)],
    '仙台堀川': [(35.6700, 139.8000), (35.6700, 139.8300)],
    '大横川': [(35.6720, 139.8020), (35.6720, 139.8250)],
    '北十間川': [(35.6750, 139.8050), (35.6750, 139.8220)],
    '小名木川': [(35.6800, 139.7850), (35.6780, 139.8000), (35.6750, 139.8120)],
    '北十間川支流': [(35.6730, 139.8100), (35.6730, 139.8180)],
}

# 木場（貯木場）の広がり
KIBA_STAGES = [
    dict(name='① 1657年〜 木場誕生', col=(200, 160, 100),
         poly=[(35.6700, 139.8000), (35.6700, 139.8100), (35.6650, 139.8100), (35.6650, 139.8000)],
         labels=[('木場', 35.6675, 139.8050, 26)]),
    dict(name='② 1700年〜 運河網整備', col=(120, 180, 220),
         poly=[],  # 運河は線で描く
         labels=[('横十間川', 35.6760, 139.8115, 22),
                 ('仙台堀川', 35.6700, 139.8150, 22)]),
    dict(name='③ 1872年〜 生糸輸出・埋め立て', col=(220, 200, 140),
         poly=[(35.6600, 139.8200), (35.6600, 139.8300), (35.6550, 139.8300), (35.6550, 139.8200)],
         labels=[('豊洲埋立', 35.6575, 139.8250, 24),
                 ('東陽', 35.6650, 139.8220, 22)]),
]

BAR_ANG = 45.0


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
    """fillmap_0=入り江と自然河川。fillmap_1..3=木場→運河網→埋め立ての順に累積。"""
    z, R = 15, 2
    D, X0, Y0, N = dem(z, R)
    box = _box(FILL_CENTER, FILL_FRAME, z)
    W, H = FILL_FRAME
    d = ndi.gaussian_filter(D[box[1]:box[3], box[0]:box[2]], 1.2)
    gy, gx = np.gradient(d, 5.0)
    az, alt = math.radians(315), math.radians(40)
    slope, asp = np.arctan(2.0 * np.hypot(gx, gy)), np.arctan2(-gx, gy)
    hs = np.clip(np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - asp), 0, 1)
    t = np.clip((d - 0) / 5.0, 0, 1)[..., None]
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

    sea_px = _ll2px(SEA, box)
    river_px = {k: _ll2px(v, box) for k, v in NATURAL_RIVERS.items()}
    canal_px = {k: _ll2px(v, box) for k, v in CANALS.items()}

    # 海（入り江）
    paint(amask([sea_px]), SEA_COL)
    paint(amask([sea_px], 3) * .5, COAST_COL)
    # 自然河川
    for rp in river_px.values():
        paint(amask([rp], 8), RIVER_COL)
    # 運河（最初は海の一部として青く、後で水色に）
    for cp in canal_px.values():
        paint(amask([cp], 7), RIVER_COL)

    im = Image.fromarray(np.clip(arr, 0, 255).astype('uint8')).convert('RGBA')
    dr = ImageDraw.Draw(im)
    P = lambda la, lo: _ll2px([(la, lo)], box)[0]
    w, _ = _chip(dr, 18, 14, '深川・木場', 38)
    _chip(dr, 18 + w + 10, 24, '模式図', 23, fg=(58, 44, 24), bg=(238, 228, 192, 240))
    _chip(dr, *P(35.6880, 139.7800), '隅田川', 24, anchor='mm', bg=(30, 62, 96, 220))
    _chip(dr, *P(35.6740, 139.8050), '門前仲町', 26, anchor='mm', bg=(120, 40, 30, 230))
    _chip(dr, *P(35.6713, 139.8074), '木場', 26, anchor='mm', bg=(160, 100, 40, 230))
    _chip(dr, *P(35.6570, 139.7880), '豊洲', 24, anchor='mm')
    _chip(dr, *P(35.6652, 139.8220), '東陽', 24, anchor='mm')
    _chip(dr, *P(35.6920, 139.7880), '両国橋', 22, anchor='mm')
    _rot_text(im, *P(35.6730, 139.8030), '小名木川', 24, BAR_ANG)
    for cp in canal_px.values():
        if len(cp) >= 2:
            mid = ((cp[0][0] + cp[-1][0]) / 2, (cp[0][1] + cp[-1][1]) / 2)
            dx = cp[-1][0] - cp[0][0]
            dy = cp[-1][1] - cp[0][1]
            ang = math.degrees(math.atan2(dy, dx))
            _rot_text(im, mid[0], mid[1], '運河', 20, ang)
    dr.text((W - 14, H - 12), '国土地理院の標高データから作成・位置と形は模式化', font=_font(20, 500),
            fill=(255, 255, 255), anchor='rs', stroke_width=4, stroke_fill=(32, 52, 78))
    im.convert('RGB').save(OUT / 'fillmap_0.png')

    # 累積マスク
    sea = amask([sea_px]) > .5
    cum = np.zeros_like(sea)

    for i, st in enumerate(KIBA_STAGES, 1):
        if st['poly']:
            new = amask([_ll2px(st['poly'], box)]) > .5
        else:
            new = np.zeros_like(sea)
        cum = cum | new
        a = np.zeros((H, W, 4), float)
        a[..., :3] = st['col']
        a[..., 3] = new * 255.
        edge = new & ndi.binary_dilation(~new & ~sea, np.ones((4, 4), bool))
        a[ndi.binary_dilation(edge, np.ones((2, 2), bool))] = FILL_EDGE + (255.,)
        s = Image.fromarray(np.clip(a, 0, 255).astype('uint8'))
        ds = ImageDraw.Draw(s)
        for txt, la, lo_, sz in st['labels']:
            _chip(ds, *P(la, lo_), txt, sz, anchor='mm', bg=(40, 34, 26, 220))
        _chip(ds, W - 16, 556 + (i - 1) * 52, st['name'], 28, fg=(255, 255, 255), bg=(40, 34, 26, 225), anchor='rt')
        # 運河も毎回重ね描き（水色で）
        for cp in canal_px.values():
            if len(cp) >= 2:
                paint(amask([cp], 7), CANAL_COL)
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