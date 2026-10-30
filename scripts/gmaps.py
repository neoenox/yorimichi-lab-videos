"""汎用の戦場図（ベース地図）。使い方：
  import gmaps; M = gmaps.Maps('anegawa', {'area': dict(lon0=..., lon1=..., lat0=..., lat1=..., z=14)}); M.build(); M.norm(lon, lat, 'area')
出力：assets/<slug>/map_<view>.png（高さ600px、下地=国土地理院 陰影起伏図＋標準地図の水域。現代の地形）。
"""
import io, math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FD = 'C:/Windows/Fonts/'
INK = (4, 10, 18)
LAND = (0.62, 0.74, 0.86)
OUT_H = 600


def txy(lon, lat, z):
    return ((lon + 180) / 360 * 2 ** z, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * 2 ** z)


class Maps:
    def __init__(self, slug, views):
        self.slug, self.views = slug, views
        self.tiles = ROOT / 'cache' / f'{slug}_tiles'
        self.assets = ROOT / 'assets' / slug

    def _fetch(self, args):
        kind, z, x, y = args
        p = self.tiles / f'{kind}_{z}_{x}_{y}.png'
        if p.exists():
            return args, p.read_bytes()
        url = f'https://cyberjapandata.gsi.go.jp/xyz/{"hillshademap" if kind == "hs" else "std"}/{z}/{x}/{y}.png'
        for _ in range(4):
            try:
                r = requests.get(url, timeout=60, headers={'User-Agent': 'rekishikaisetu-research/1.0'})
            except Exception:
                continue
            if r.status_code == 404:
                return args, None
            if r.ok:
                self.tiles.mkdir(parents=True, exist_ok=True); p.write_bytes(r.content)
                return args, r.content
        return args, None

    def _mosaic(self, V, kind, out_w):
        z = V['z']
        xa, ya = txy(V['lon0'], V['lat1'], z); xb, yb = txy(V['lon1'], V['lat0'], z)
        x0, y0, x1, y1 = int(xa), int(ya), int(xb), int(yb)
        jobs = [(kind, z, x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]
        base = Image.new('RGBA', ((x1 - x0 + 1) * 256, (y1 - y0 + 1) * 256), (200, 200, 200, 255) if kind == 'hs' else (255, 255, 255, 255)); got = 0
        with ThreadPoolExecutor(6) as ex:
            for (k, zz, x, y), data in ex.map(self._fetch, jobs):
                if data:
                    base.alpha_composite(Image.open(io.BytesIO(data)).convert('RGBA'), ((x - x0) * 256, (y - y0) * 256)); got += 1
        if got < len(jobs): print(f'tiles missing {kind} {got}/{len(jobs)} (sea?)')
        box = (int(xa * 256 - x0 * 256), int(ya * 256 - y0 * 256), int(xb * 256 - x0 * 256), int(yb * 256 - y0 * 256))
        return base.crop(box).resize((out_w, OUT_H), Image.LANCZOS)

    def size(self, view):
        V = self.views[view]; z = V['z']
        xa, ya = txy(V['lon0'], V['lat1'], z); xb, yb = txy(V['lon1'], V['lat0'], z)
        return int(round(OUT_H * (xb - xa) / (yb - ya))), OUT_H

    def norm(self, lon, lat, view):
        V = self.views[view]; z = V['z']
        xa, ya = txy(V['lon0'], V['lat1'], z); xb, yb = txy(V['lon1'], V['lat0'], z); x, y = txy(lon, lat, z)
        return [(x - xa) / (xb - xa), (y - ya) / (yb - ya)]

    def build(self, only=None):
        for name, V in self.views.items():
            if only and name != only:
                continue
            w, h = self.size(name)
            hs = self._mosaic(V, 'hs', w).convert('RGBA'); std = self._mosaic(V, 'std', w).convert('RGB')
            g = np.asarray(hs.convert('RGB'), dtype=float).mean(-1, keepdims=True) / 255.
            shade = np.clip(g * np.array(LAND) * 1.34 + 0.035, 0, 1)
            s = np.asarray(std, dtype=float)
            wmask = (s[..., 2] >= 245) & (s[..., 2] - s[..., 0] >= 60) & (s[..., 1] - s[..., 0] >= 8)
            try:
                from scipy import ndimage as ndi
                lab, n = ndi.label(wmask, structure=np.ones((3, 3)))
                sizes = ndi.sum(wmask, lab, range(1, n + 1))
                keep = np.zeros(n + 1, bool); keep[1:] = sizes >= 40
                wmask = ndi.binary_dilation(keep[lab], iterations=1)
            except ImportError:
                pass
            rgb = np.where(wmask[..., None], np.array([0.20, 0.42, 0.68]), shade)
            im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype('uint8'), 'RGB').convert('RGBA')
            d = ImageDraw.Draw(im, 'RGBA')
            f = ImageFont.truetype(FD + 'NotoSansJP-VF.ttf', 20); f.set_variation_by_axes([500])
            txt = '地理院タイル（陰影起伏図・標準地図）を加工して作成　※現代の地形。当時の川筋・道ではありません'
            tw = d.textlength(txt, font=f)
            d.rounded_rectangle((w - tw - 28, h - 38, w - 8, h - 8), 8, fill=INK + (200,))
            d.text((w - tw - 18, h - 34), txt, font=f, fill=(215, 224, 226, 255))
            self.assets.mkdir(parents=True, exist_ok=True)
            im.convert('RGB').save(self.assets / f'map_{name}.png', quality=95)
            print('->', self.assets / f'map_{name}.png', im.size, flush=True)
