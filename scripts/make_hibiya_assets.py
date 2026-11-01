"""日比谷入江の動画（hibiya）の素材を作る。国土地理院のタイルから、空中写真3年代と、標高の色別図（5mメッシュ）、
埋め立ての段階を示す模式図（fillmap_0..3）を作る。
出典：国土地理院（ort_riku10=1936〜42年頃、ort_old10=1961〜69年、seamlessphoto=全国最新写真、dem5a_png）。加工して作成。
usage: python scripts/make_hibiya_assets.py [photos|relief|fillmap|all]

見せ場：本丸台地（約20m）と、埋め立てた低地（約3m）の段差。日比谷入江はその低い側にあった。
土地条件図（lcmfc2）は、タイルの配信範囲と位置合わせがこちらの座標計算と合わなかったため、この動画では使っていない。
fillmap は標高だけを土台に、水・砂州・埋め立ての範囲を手で描いた模式図。位置と形は模式化してある。
"""
import io, math, sys, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
from pathlib import Path
OUT = Path(__file__).resolve().parents[1] / 'assets' / 'hibiya'
OUT.mkdir(parents=True, exist_ok=True)
CENTER = (35.6760, 139.7600)   # 日比谷〜丸の内
FRAME = (1060, 720)


def tile(l, z, x, y, ext='png'):
    return Image.open(io.BytesIO(urllib.request.urlopen(
        f'https://cyberjapandata.gsi.go.jp/xyz/{l}/{z}/{x}/{y}.{ext}', timeout=30).read())).convert('RGB')


def tile_rgba(l, z, x, y):
    return Image.open(io.BytesIO(urllib.request.urlopen(
        f'https://cyberjapandata.gsi.go.jp/xyz/{l}/{z}/{x}/{y}.png', timeout=30).read())).convert('RGBA')


def xy(lat, lon, z):
    n = 2 ** z
    return (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n


def photos():
    z, R = 17, 2
    fx, fy = xy(CENTER[0], CENTER[1], z)
    x0, y0 = int(fx), int(fy)
    for name, l, ext in [('aerial_1936', 'ort_riku10', 'png'), ('aerial_1961', 'ort_old10', 'png'), ('aerial_now', 'seamlessphoto', 'jpg')]:
        im = Image.new('RGB', (256 * (2 * R + 1),) * 2)
        for i in range(-R, R + 1):
            for j in range(-R, R + 1):
                im.paste(tile(l, z, x0 + i, y0 + j, ext), ((i + R) * 256, (j + R) * 256))
        im.save(OUT / f'{name}.png')
        print('photo', name, im.size)


PTS = {'皇居・本丸': (35.6850, 139.7560), '日比谷公園': (35.6735, 139.7565),
       '有楽町駅': (35.6755, 139.7635), '新橋駅': (35.6665, 139.7585)}


def _crop_box(pts_px, size, w, h):
    """点の重心を中心に w x h の枠を作り、画像内に収める。"""
    cx = sum(p[0] for p in pts_px) / len(pts_px)
    cy = sum(p[1] for p in pts_px) / len(pts_px)
    x0 = int(min(max(cx - w / 2, 0), size - w))
    y0 = int(min(max(cy - h / 2, 0), size - h))
    return (x0, y0, x0 + w, y0 + h)


def grid(z=15, R=2):
    """z=15・R=2 なら 5x5タイル = 1280px（約5km四方）。左上のタイル番号と一辺の画素数を返す。"""
    cx, cy = xy(CENTER[0], CENTER[1], z)
    return z, int(cx) - R, int(cy) - R, 256 * (2 * R + 1)


def dem(z=15, R=2):
    """5mメッシュ標高を (2R+1)^2 タイルぶん読み、標高(m)の配列とタイル原点を返す。欠測は最近傍で埋める。"""
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
    D, X0, Y0, N = dem(Z)          # 5x5タイル = 1280px（約6km四方）
    pts = {}
    for k, (la, lo) in PTS.items():
        fx, fy = xy(la, lo, Z)
        x, y = int((fx - X0) * 256), int((fy - Y0) * 256)
        pts[k] = (float(np.mean(D[y - 4:y + 5, x - 4:x + 5])), (x, y))
    gy, gx = np.gradient(D, 5.0)
    az, alt = math.radians(315), math.radians(40)
    slope, asp = np.arctan(2.0 * np.hypot(gx, gy)), np.arctan2(-gx, gy)
    hs = np.clip(np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - asp), 0, 1)
    # 日比谷は 0〜25m に収まるので、色の幅を低地側へ寄せる（渋谷の回は 8〜40m）
    t = np.clip((D - 1) / (25 - 1), 0, 1)
    stops = [(0, (46, 96, 150)), (.25, (70, 150, 150)), (.5, (150, 185, 110)), (.75, (225, 205, 120)), (1, (235, 235, 225))]
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


# ---------------------------------------------------------------- 模式図：入り江が段階的に埋まる
FILL_FRAME = (1160, 795)          # 1060x720 より縦を広く取り、大手町〜新橋までを入れる
FILL_CENTER = (35.6785, 139.7620)
SEA_COL, COAST_COL = (92, 156, 204), (46, 96, 148)
BAR_COL, BAR_EDGE = (244, 213, 132), (146, 112, 58)
RIVER_COL = (72, 136, 188)
FRONT_COL = (128, 92, 52)
# 日比谷入江と江戸湾（奥から西岸を南下し、湾として枠外へ抜ける）lat, lon
SEA = [(35.6888, 139.7650), (35.6862, 139.7612), (35.6830, 139.7590), (35.6790, 139.7598),
       (35.6755, 139.7582), (35.6720, 139.7558), (35.6680, 139.7540), (35.6640, 139.7555),
       (35.6585, 139.7590), (35.6585, 139.7950), (35.6920, 139.7950), (35.6920, 139.7755),
       (35.6896, 139.7720), (35.6893, 139.7688), (35.6890, 139.7662)]
# 江戸前島（砂州の半島）。北で台地につながる
BAR = [(35.6940, 139.7716), (35.6860, 139.7706), (35.6822, 139.7688), (35.6782, 139.7664),
       (35.6742, 139.7638), (35.6702, 139.7612), (35.6666, 139.7584), (35.6648, 139.7610),
       (35.6680, 139.7640), (35.6720, 139.7670), (35.6760, 139.7696), (35.6800, 139.7722),
       (35.6840, 139.7746), (35.6870, 139.7762), (35.6940, 139.7772)]
# 埋め立ては入り江の内側だけ。砂州の西がわ（この折れ線より西）を切り取り線にする
CUT = [(35.7000, 139.7718), (35.6860, 139.7706), (35.6822, 139.7688), (35.6782, 139.7664),
       (35.6742, 139.7638), (35.6702, 139.7612), (35.6666, 139.7584), (35.6648, 139.7610),
       (35.6610, 139.7588), (35.6550, 139.7588), (35.6550, 139.7000), (35.7000, 139.7000)]
RIVER = [(35.6916, 139.7594), (35.6902, 139.7610), (35.6892, 139.7630), (35.6887, 139.7646)]
BAR_ANG = 54.0                    # 「江戸前島」を砂州に沿って回す角度
# 段階（北→南）。lat=(南端, 北端) は None で枠外まで
STAGES = [dict(lat=(35.6835, None), col=(200, 176, 138),
               lab='① 1592年　北側から', names=[('① 大手町', 35.6878, 139.7658, 27)]),
          dict(lat=(35.6742, 35.6835), col=(216, 192, 152),
               lab='② 1603年〜　本丸東から有楽町',
               names=[('② 丸の内', 35.6822, 139.7643, 27), ('有楽町', 35.6762, 139.7636, 25)]),
          dict(lat=(None, 35.6742), col=(232, 208, 168),
               lab='③ 江戸時代初頭　南側',
               names=[('③ 日比谷', 35.6730, 139.7598, 27), ('銀座', 35.6698, 139.7637, 25)])]


def _font(size, w=700):
    f = ImageFont.truetype('C:/Windows/Fonts/NotoSansJP-VF.ttf', size)
    f.set_variation_by_axes([w])
    return f


def _box(center, frame, z=15):
    """中心の緯度経度から、frame の大きさの切り出し枠を作る（地図の範囲がぶれないように）。"""
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
    """地図の上に、傾けた文字をのせる（半島の向きに合わせる）。"""
    f = _font(size)
    d0 = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    w, h = int(d0.textlength(text, font=f)) + sw * 2 + 6, size + sw * 2 + 8
    t = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(t).text((w / 2, h / 2), text, font=f, fill=fg, stroke_width=sw, stroke_fill=stroke, anchor='mm')
    t = t.rotate(angle, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(t, (int(x - t.width / 2), int(y - t.height / 2)))


def fillmap():
    """fillmap_0=入り江と江戸前島。fillmap_1..3=北から順に埋め立てた範囲（累積）。"""
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

    def amask(polys, width=0):
        m = Image.new('L', (W * SS, H * SS), 0)
        g = ImageDraw.Draw(m)
        for p in polys:
            if width:
                g.line([(x * SS, y * SS) for x, y in list(p) + [p[0]]], fill=255, width=width * SS, joint='curve')
            else:
                g.polygon([(x * SS, y * SS) for x, y in p], fill=255)
        return np.asarray(m.resize((W, H), Image.LANCZOS)).astype(float) / 255.

    def paint(a, col):
        nonlocal arr
        k = a[..., None]
        arr = arr * (1 - k) + np.array(col, float) * k

    sea_px, bar_px = _ll2px(SEA, box), _ll2px(BAR, box)
    paint(amask([sea_px]), SEA_COL)
    paint(amask([sea_px], 3) * .5, COAST_COL)
    paint(amask([bar_px]), BAR_COL)
    paint(amask([bar_px], 3) * .65, BAR_EDGE)
    paint(amask([_ll2px(RIVER, box)], 8), RIVER_COL)

    im = Image.fromarray(np.clip(arr, 0, 255).astype('uint8')).convert('RGBA')
    dr = ImageDraw.Draw(im)
    P = lambda la, lo: _ll2px([(la, lo)], box)[0]
    w, _ = _chip(dr, 18, 14, '日比谷入江', 40)
    _chip(dr, 18 + w + 10, 24, '模式図', 23, fg=(58, 44, 24), bg=(238, 228, 192, 240))
    _chip(dr, *P(35.6852, 139.7524), '本丸台地', 30, anchor='mm')
    _chip(dr, *P(35.6903, 139.7572), '平川', 25, anchor='mm')
    dr.text(P(35.6768, 139.7768), '江戸湾', font=_font(34), fill=(255, 255, 255), anchor='mm',
            stroke_width=6, stroke_fill=(40, 70, 110))
    _rot_text(im, *P(35.6816, 139.7702), '江戸前島', 29, BAR_ANG)
    dr.text((W - 14, H - 12), '国土地理院の標高データから作成・位置と形は模式化', font=_font(20, 500),
            fill=(255, 255, 255), anchor='rs', stroke_width=4, stroke_fill=(32, 52, 78))
    im.convert('RGB').save(OUT / 'fillmap_0.png')

    # 緯度の帯で、北→南の3段階に切る
    n = 2 ** z
    ys = (Y0 * 256 + box[1] + np.arange(H) + .5) / 256 / n
    lats = np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * ys))))[:, None]
    sea = amask([sea_px]) > .5
    cut_m = amask([_ll2px(CUT, box)]) > .5
    cum = np.zeros_like(sea)
    for i, st in enumerate(STAGES, 1):
        lo, hi = st['lat']
        band = np.ones((H, 1), bool)
        if lo is not None: band &= lats >= lo
        if hi is not None: band &= lats < hi
        new = sea & cut_m & band
        cum = cum | new
        front = new & ~ndi.binary_erosion(new, np.ones((3, 3), bool), border_value=1) \
            & ~ndi.binary_dilation(~sea, np.ones((3, 3), bool))
        a = np.zeros((H, W, 4), float)
        a[..., :3] = st['col']
        a[..., 3] = new * 255.
        coast = new & ndi.binary_dilation(~sea, np.ones((3, 3), bool))
        a[ndi.binary_dilation(coast, np.ones((2, 2), bool))] = COAST_COL + (255.,)
        a[ndi.binary_dilation(front, np.ones((5, 5), bool))] = FRONT_COL + (255.,)
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

