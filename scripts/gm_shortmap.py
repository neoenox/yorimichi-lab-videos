"""Short 用の縦型世界地図（Natural Earth 110m、CC0）を作る。

長尺の図は 16:9 なので、縦型に切ると地図が切れてしまう。Short 専用に
メルカトル図法で 1080x1920 を作り直す（アフリカ＝橙、グリーンランド＝青）。

usage: python scripts/gm_shortmap.py
  -> assets/gm_short/map_portrait.png        （アフリカとグリーンランド）
  -> assets/gm_short/map_greenland_zoom.png  （高緯度の引き伸ばし）
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gm_geo
from make_short import font

R = Path(__file__).resolve().parents[1]
OUT = R / 'assets' / 'gm_short'
W, H = 1080, 1920
LON0, LON1 = -88.0, 52.0
LAT0 = -45.0
BG = (7, 19, 31)
LAND = (40, 60, 72)
EDGE = (66, 94, 108)
AFRICA = (226, 138, 56)
GREENLAND = (110, 178, 235)


def my(lat):
    lat = max(min(lat, 84.0), -84.0)
    return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))


def my_inv(m):
    return math.degrees(2 * math.atan(math.exp(math.radians(m))) - math.pi / 2)


SX = W / (LON1 - LON0)
Y0 = my(LAT0)
Y1 = Y0 + H / SX
LAT1 = my_inv(Y1)


def px(lon, lat):
    return ((lon - LON0) * SX, (Y1 - my(lat)) * SX)


def draw_base():
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    for lon in range(-80, 61, 20):
        x, _ = px(lon, 0)
        d.line([(x, 0), (x, H)], fill=(18, 38, 52), width=2)
    for lat in range(-40, 81, 20):
        _, y = px(0, lat)
        d.line([(0, y), (W, y)], fill=(18, 38, 52), width=2)
    for c in gm_geo.load():
        name = c['attr'].get('ADMIN', '')
        cont = c['attr'].get('CONTINENT', '')
        if name == 'Greenland':
            fill, edge = GREENLAND, (146, 196, 232)
        elif cont == 'Africa':
            fill, edge = AFRICA, (232, 168, 100)
        else:
            fill, edge = LAND, EDGE
        for ring in c['rings']:
            if len(ring) < 3:
                continue
            pts = [px(lon, lat) for lon, lat in ring]
            d.polygon(pts, fill=fill)
            d.line(pts, fill=edge, width=1)
    return im


def bands(im):
    im = im.copy()
    d = ImageDraw.Draw(im, 'RGBA')
    for lat in (60, 80):
        _, y = px(0, lat)
        d.line([(0, y), (W, y)], fill=(232, 196, 108, 150), width=3)
        d.text((24, y - 34), f'{lat}°', font=font(30, True), fill=(232, 196, 108, 235))
    _, y60 = px(0, 60)
    _, y80 = px(0, 80)
    d.rectangle((0, y80, W, y60), fill=(232, 196, 108, 26))
    return im


def render(lon0, lon1, lat0, highlight_bands=False):
    global LON0, LON1, LAT0, SX, Y0, Y1
    LON0, LON1, LAT0 = lon0, lon1, lat0
    SX = W / (LON1 - LON0)
    Y0 = my(LAT0)
    Y1 = Y0 + H / SX
    im = draw_base()
    return bands(im) if highlight_bands else im


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    render(-88.0, 52.0, -45.0).save(OUT / 'map_portrait.png')
    # 高緯度ほど引き伸ばされることを見せるため、グリーンランド付近を拡大した版
    render(-78.0, -11.0, 51.0).save(OUT / 'map_greenland_zoom.png')
    print('assets/gm_short/map_portrait.png, map_greenland_zoom.png')
