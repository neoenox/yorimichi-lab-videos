"""日比谷入江の動画（hibiya）の素材を作る。国土地理院のタイルから、空中写真3年代と、標高の色別図（5mメッシュ）を作る。
出典：国土地理院（ort_riku10=1936〜42年頃、ort_old10=1961〜69年、seamlessphoto=全国最新写真、dem5a_png）。加工して作成。
usage: python scripts/make_hibiya_assets.py [photos|relief|all]

見せ場：本丸台地（約20m）と、埋め立てた低地（約3m）の段差。日比谷入江はその低い側にあった。
土地条件図（lcmfc2）は、タイルの配信範囲と位置合わせがこちらの座標計算と合わなかったため、この動画では使っていない。
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


def relief():
    z, R = 15, 2          # 5x5タイル = 1280px（約6km四方）
    cx, cy = xy(CENTER[0], CENTER[1], z)
    X0, Y0 = int(cx) - R, int(cy) - R
    N = 256 * (2 * R + 1)
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
    pts = {}
    for k, (la, lo) in PTS.items():
        fx, fy = xy(la, lo, z)
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


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('photos', 'all'):
        photos()
    if what in ('relief', 'all'):
        relief()
