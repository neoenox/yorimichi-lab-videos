"""渋谷川の動画（shibuya）の素材を作る。国土地理院のタイルから、空中写真3年代と、標高の色別図（5mメッシュ）を作る。
出典：国土地理院（ort_riku10=1936〜42年頃、ort_old10=1961〜69年、seamlessphoto=全国最新写真、dem5a_png）。加工して作成。
usage: python scripts/make_shibuya_assets.py [photos|relief]"""
import io, math, sys, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
from pathlib import Path
OUT = Path(__file__).resolve().parents[1] / 'assets' / 'shibuya'
OUT.mkdir(parents=True, exist_ok=True)


def tile(l, z, x, y, ext='png'):
    return Image.open(io.BytesIO(urllib.request.urlopen(f'https://cyberjapandata.gsi.go.jp/xyz/{l}/{z}/{x}/{y}.{ext}', timeout=30).read())).convert('RGB')


def xy(lat, lon, z):
    n = 2 ** z
    return (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n


def photos():
    z, R = 17, 2
    fx, fy = xy(35.6585, 139.7010, z)
    x0, y0 = int(fx), int(fy)
    for name, l, ext in [('aerial_1936', 'ort_riku10', 'png'), ('aerial_1961', 'ort_old10', 'png'), ('aerial_now', 'seamlessphoto', 'jpg')]:
        im = Image.new('RGB', (256 * (2 * R + 1),) * 2)
        for i in range(-R, R + 1):
            for j in range(-R, R + 1):
                im.paste(tile(l, z, x0 + i, y0 + j, ext), ((i + R) * 256, (j + R) * 256))
        im.save(OUT / f'{name}.png')


PTS = {'渋谷駅前': (35.6590, 139.7005), '道玄坂の上': (35.6560, 139.6965), '松濤': (35.6620, 139.6900), '代々木公園の南': (35.6640, 139.6960)}


def relief():
    z = 15
    cx, cy = xy(35.6600, 139.6990, z)
    X0, Y0 = int(cx) - 1, int(cy) - 1
    D = np.zeros((768, 768))
    for i in range(3):
        for j in range(3):
            t = np.array(tile('dem5a_png', z, X0 + i, Y0 + j)).astype(np.int64)
            raw = t[..., 0] * 65536 + t[..., 1] * 256 + t[..., 2]
            v = np.where(raw >= 8388608, raw - 16777216, raw) * 0.01
            v[raw == 8388608] = np.nan
            D[j * 256:(j + 1) * 256, i * 256:(i + 1) * 256] = v
    m = np.isnan(D)
    if m.any():
        D = D[tuple(ndi.distance_transform_edt(m, return_distances=False, return_indices=True))]
    res = {}
    for k, (la, lo) in PTS.items():
        fx, fy = xy(la, lo, z)
        x, y = int((fx - X0) * 256), int((fy - Y0) * 256)
        res[k] = (float(np.mean(D[y - 4:y + 5, x - 4:x + 5])), (x, y))
    S = 2
    Z = ndi.zoom(D, S, order=3)
    gy, gx = np.gradient(Z, 5 / S)
    az, alt = math.radians(315), math.radians(40)
    slope, asp = np.arctan(2.0 * np.hypot(gx, gy)), np.arctan2(-gx, gy)
    hs = np.clip(np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - asp), 0, 1)
    t = np.clip((Z - 8) / (40 - 8), 0, 1)
    stops = [(0, (46, 96, 150)), (.25, (70, 150, 150)), (.5, (150, 185, 110)), (.75, (225, 205, 120)), (1, (235, 235, 225))]
    out = np.zeros(t.shape + (3,))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        f = ((t - a) / (b - a))[..., None]
        out = np.where(((t >= a) & (t <= b))[..., None], np.array(ca) * (1 - f) + np.array(cb) * f, out)
    im = Image.fromarray(np.clip(out * (0.55 + 0.45 * hs[..., None]), 0, 255).astype('uint8'))
    plain = im.crop((300, 540, 1360, 1260))
    plain.save(OUT / 'relief_plain.png')
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype('C:/Windows/Fonts/NotoSansJP-VF.ttf', 40)
    f.set_variation_by_axes([700])
    for k, (v, (x, y)) in res.items():
        X, Y = x * S, y * S
        d.ellipse((X - 9, Y - 9, X + 9, Y + 9), fill=(255, 90, 80), outline=(255, 255, 255), width=3)
        s = f'{k} {v:.0f}m'
        w = d.textlength(s, font=f)
        tx = min(max(X + 14, 6), im.width - w - 10)
        d.rectangle((tx - 6, Y - 28, tx + w + 6, Y + 28), fill=(7, 24, 36))
        d.text((tx, Y - 25), s, font=f, fill=(245, 243, 232))
    im = im.crop((300, 540, 1360, 1260))
    im.save(OUT / 'relief.png')
    print({k: round(v[0], 2) for k, v in res.items()})


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('photos', 'all'): photos()
    if what in ('relief', 'all'): relief()
