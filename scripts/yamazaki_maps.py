"""山崎の戦場図（ベース地図）を作る。assets/yamazaki/map_area.png。
下地：国土地理院 陰影起伏図（現代の地形）に、標準地図の水域（川・池）を重ねる。当時の地形・川筋・道を再現したものではない。
位置の正規化：`norm(lon, lat)` が、地図の左上=(0,0)、右下=(1,1) の座標を返す（spec の軍の経路で使う）。
実行： python scripts/sekigahara_maps.py
出典表示：「地理院タイル（陰影起伏図・標準地図）を加工して作成」"""
import io, math, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
TILES = ROOT / 'cache' / 'yamazaki_tiles'
ASSETS = ROOT / 'assets' / 'yamazaki'
FD = 'C:/Windows/Fonts/'
VIEWS = {   # 地図の範囲（西・東・南・北）、ズーム、出力名
    'area': dict(lon0=135.628, lon1=135.752, lat0=34.882, lat1=34.926, z=15, out='map_area.png'),
    'core': dict(lon0=135.662, lon1=135.722, lat0=34.884, lat1=34.926, z=16, out='map_core.png'),
    'east': dict(lon0=135.62, lon1=135.95, lat0=34.86, lat1=35.10, z=13, out='map_east.png'),
    'approach': dict(lon0=135.55, lon1=135.74, lat0=34.815, lat1=34.935, z=14, out='map_approach.png'),
    'wide': dict(lon0=133.70, lon1=135.95, lat0=34.58, lat1=35.19, z=10, out='map_wide.png'),
}
V = VIEWS['area']
LON0, LON1, LAT0, LAT1 = V['lon0'], V['lon1'], V['lat0'], V['lat1']
OUT_H = 600
OUT_W = 1800
Z = V['z']


def use(view):
    global V, LON0, LON1, LAT0, LAT1, Z, OUT_W
    V = VIEWS[view]; LON0, LON1, LAT0, LAT1, Z = V['lon0'], V['lon1'], V['lat0'], V['lat1'], V['z']
    xa, ya = txy(LON0, LAT1); xb, yb = txy(LON1, LAT0)
    OUT_W = int(round(OUT_H * (xb - xa) / (yb - ya)))
INK = (4, 10, 18)
LAND = (0.62, 0.74, 0.86)


def txy(lon, lat, z=None):
    z = Z if z is None else z
    return ((lon + 180) / 360 * 2 ** z, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * 2 ** z)


def norm(lon, lat, view='area'):
    use(view)
    """地図の左上=(0,0)、右下=(1,1)。経度・緯度を等間隔に取る（この範囲では、縦横の比はほぼ保たれる）"""
    xa, ya = txy(LON0, LAT1); xb, yb = txy(LON1, LAT0); x, y = txy(lon, lat)
    return ((x - xa) / (xb - xa), (y - ya) / (yb - ya))


def fetch(args):
    kind, z, x, y = args
    p = TILES / f'{kind}_{z}_{x}_{y}.png'
    if p.exists():
        return args, p.read_bytes()
    url = f'https://cyberjapandata.gsi.go.jp/xyz/{"hillshademap" if kind == "hs" else "std"}/{z}/{x}/{y}.png'
    for _ in range(4):
        try:
            r = requests.get(url, timeout=60, headers={'User-Agent': 'rekishikaisetu-research/1.0'})
        except Exception:  # noqa: BLE001
            continue
        if r.status_code == 404:
            return args, None
        if r.ok:
            TILES.mkdir(parents=True, exist_ok=True); p.write_bytes(r.content)
            return args, r.content
    return args, None


def mosaic(kind):
    xa, ya = txy(LON0, LAT1); xb, yb = txy(LON1, LAT0)
    x0, y0, x1, y1 = int(xa), int(ya), int(xb), int(yb)
    jobs = [(kind, Z, x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]
    base = Image.new('RGBA', ((x1 - x0 + 1) * 256, (y1 - y0 + 1) * 256), (0, 0, 0, 0)); got = 0
    with ThreadPoolExecutor(6) as ex:
        for (k, z, x, y), data in ex.map(fetch, jobs):
            if data:
                base.alpha_composite(Image.open(io.BytesIO(data)).convert('RGBA'), ((x - x0) * 256, (y - y0) * 256)); got += 1
    print(f'  {kind}: {got}/{len(jobs)} tiles')
    assert got == len(jobs), 'タイルが欠けている'
    box = (int(xa * 256 - x0 * 256), int(ya * 256 - y0 * 256), int(xb * 256 - x0 * 256), int(yb * 256 - y0 * 256))
    return base.crop(box).resize((OUT_W, OUT_H), Image.LANCZOS)


def build(view='area'):
    use(view)
    hs = mosaic('hs').convert('RGBA')
    std = mosaic('std').convert('RGB')
    g = np.asarray(hs.convert('RGB'), dtype=float).mean(-1, keepdims=True) / 255.
    shade = np.clip(g * np.array(LAND) * 1.34 + 0.035, 0, 1)
    s = np.asarray(std, dtype=float)
    # 標準地図の水域（薄い青）を拾う
    wmask = (np.abs(s[..., 0] - 190) <= 14) & (np.abs(s[..., 1] - 210) <= 12) & (s[..., 2] >= 240)
    try:                                   # 小さな点（記号・注記のにじみ）を除き、川や池の連なりだけ残す
        from scipy import ndimage as ndi
        lab, n = ndi.label(wmask, structure=np.ones((3, 3)))
        sizes = ndi.sum(wmask, lab, range(1, n + 1))
        keep = np.zeros(n + 1, bool); keep[1:] = sizes >= 30
        wmask = keep[lab]
        wmask = ndi.binary_dilation(wmask, iterations=1)
    except ImportError:
        pass
    water = np.array([0.20, 0.42, 0.68])
    rgb = np.where(wmask[..., None], water, shade)
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype('uint8'), 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im, 'RGBA')
    f = ImageFont.truetype(FD + 'NotoSansJP-VF.ttf', 20); f.set_variation_by_axes([500])
    txt = '地理院タイル（陰影起伏図・標準地図）を加工して作成　※現代の地形。当時の川筋・道ではありません'
    w = d.textlength(txt, font=f)
    d.rounded_rectangle((OUT_W - w - 28, OUT_H - 38, OUT_W - 8, OUT_H - 8), 8, fill=INK + (200,))
    d.text((OUT_W - w - 18, OUT_H - 34), txt, font=f, fill=(215, 224, 226, 255))
    ASSETS.mkdir(parents=True, exist_ok=True)
    im.convert('RGB').save(ASSETS / V['out'], quality=95)
    print('->', ASSETS / V['out'], im.size)


if __name__ == '__main__':
    build('area'); build('wide'); build('core'); build('east'); build('approach'); use('area')
    for k, (lo, la) in {'天王山': (135.67671, 34.9018), '宝積寺': (135.67868, 34.89580), '勝龍寺城': (135.70069, 34.91811), '淀城': (135.7177, 34.90505)}.items():
        print(k, [round(v, 3) for v in norm(lo, la)])
