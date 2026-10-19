"""Okehazama battle maps: GSI hillshade mosaics + place markers + army routes.

Base layer: 国土地理院 陰影起伏図 (https://cyberjapandata.gsi.go.jp/xyz/hillshademap/{z}/{x}/{y}.png).
The base shows the MODERN terrain; it is not a reconstruction of 1560, and the arrows are a schematic of
the relative positions, not the historical roads.

Places come from cache/oke_places.json (GSI address search, 大字 representative points -> +/- a few hundred m).

Writes assets/okehazama/map_*.png (rendered 1:1 at display size).
Run:  .venv\\Scripts\\python.exe scripts\\oke_maps.py
"""
import io, json, math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
TILES = ROOT / 'cache' / 'oke_tiles'
ASSETS = ROOT / 'assets' / 'okehazama'
FD = 'C:/Windows/Fonts/'
ATTR = '地理院タイル（陰影起伏図）を加工'
WATER = (24, 50, 72)
INK = (4, 10, 18)

PLACES = json.loads((ROOT / 'cache' / 'oke_places.json').read_text(encoding='utf8'))
PT = {k: (v['lon'], v['lat']) for k, v in PLACES.items()}
# candidate area for 桶狭間山 (location disputed): a circle, not a point
HILL = (136.9690, 35.0470, 470)     # lon, lat, radius in metres


def txy(lon, lat, z):
    return ((lon + 180) / 360 * 2 ** z,
            (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * 2 ** z)


def fetch(args):
    z, x, y = args
    p = TILES / f'hs_{z}_{x}_{y}.png'
    if p.exists():
        return args, p.read_bytes()
    for _ in range(4):
        try:
            r = requests.get(f'https://cyberjapandata.gsi.go.jp/xyz/hillshademap/{z}/{x}/{y}.png', timeout=60)
        except Exception:  # noqa: BLE001
            continue
        if r.status_code == 404:
            return args, None
        if r.ok:
            p.write_bytes(r.content)
            return args, r.content
    return args, None


def build(name, z, lon0, lon1, lat0, lat1, out_w, out_h, draw_fn):
    """Mosaic the tiles for the window, crop, style, then draw_fn(im, d, at)."""
    xa, ya = txy(lon0, lat1, z)
    xb, yb = txy(lon1, lat0, z)
    x0, y0 = int(math.floor(xa)), int(math.floor(ya))
    x1, y1 = int(math.floor(xb)), int(math.floor(yb))
    jobs = [(z, x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]
    base = Image.new('RGBA', ((x1 - x0 + 1) * 256, (y1 - y0 + 1) * 256), (0, 0, 0, 0))
    got = 0
    with ThreadPoolExecutor(8) as ex:
        for (zz, x, y), data in ex.map(fetch, jobs):
            if data:
                base.alpha_composite(Image.open(io.BytesIO(data)).convert('RGBA'), ((x - x0) * 256, (y - y0) * 256))
                got += 1
    print(f'  {name}: z{z} {len(jobs)} tiles, got {got}')
    assert got == len(jobs), 'missing tiles - refusing to draw a partial base map'

    box = (int(xa * 256 - x0 * 256), int(ya * 256 - y0 * 256), int(xb * 256 - x0 * 256), int(yb * 256 - y0 * 256))

    # land mask (hillshade alpha) and the hillshade itself, composited over water at SOURCE resolution so the
    # resize never drags transparent black pixels into the coastline.
    alpha_src = base.getchannel('A').crop(box).resize((out_w, out_h), Image.LANCZOS)
    over = Image.new('RGBA', base.size, WATER + (255,))
    over.alpha_composite(base)
    im = over.convert('RGB').crop(box).resize((out_w, out_h), Image.LANCZOS)

    arr = np.asarray(im, dtype=float) / 255.
    g = arr.mean(-1, keepdims=True)
    shade = np.clip(g * np.array([.62, .74, .86]) * 1.34 + 0.035, 0, 1)
    a = np.asarray(alpha_src, dtype=float)[..., None] / 255.
    water = np.array(WATER, dtype=float) / 255.
    rgb = shade * a + water * (1 - a)

    # coastline: land pixels touching water get a light rim, so the sea reads as sea and not as a hole
    land = a[..., 0] > 0.35
    er = land.copy()
    er[1:, :] &= land[:-1, :]
    er[:-1, :] &= land[1:, :]
    er[:, 1:] &= land[:, :-1]
    er[:, :-1] &= land[:, 1:]
    edge = np.repeat((land & ~er)[..., None], 3, axis=2)
    rgb = np.where(edge, rgb * .45 + np.array([.58, .70, .80]) * .55, rgb)

    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype('uint8'), 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im, 'RGBA')

    def at(k):
        lon, lat = PT[k] if isinstance(k, str) else k[:2]
        mx, my = txy(lon, lat, z)
        px = (mx * 256 - x0 * 256 - box[0]) / (box[2] - box[0]) * out_w
        py = (my * 256 - y0 * 256 - box[1]) / (box[3] - box[1]) * out_h
        return (px, py)

    draw_fn(im, d, at)
    attribution(im, d)
    ASSETS.mkdir(parents=True, exist_ok=True)
    im.convert('RGB').save(ASSETS / f'{name}.png', quality=95)
    print(f'  -> assets/okehazama/{name}.png {im.size}')


FONTS = {}


def font(size, weight=700, serif=False):
    k = (size, weight, serif)
    if k not in FONTS:
        f = ImageFont.truetype(FD + ('NotoSerifJP-VF.ttf' if serif else 'NotoSansJP-VF.ttf'), size)
        f.set_variation_by_axes([weight])
        FONTS[k] = f
    return FONTS[k]


def marker(d, xy, kind, col=(245, 243, 232)):
    x, y = xy
    if kind == 'castle':
        r = 12
        d.rectangle((x - r, y - r, x + r, y + r), fill=(16, 22, 30), outline=col, width=4)
        d.rectangle((x - r + 4, y - r + 4, x + r - 4, y + r - 4), fill=col)
    elif kind == 'fort':
        r = 10
        d.ellipse((x - r, y - r, x + r, y + r), fill=WATER, outline=(150, 205, 250), width=4)
    elif kind == 'battle':
        r = 15
        d.polygon([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], fill=(222, 72, 56), outline=(255, 240, 230))
    elif kind == 'spot':
        r = 13
        d.ellipse((x - r, y - r, x + r, y + r), fill=(214, 62, 52), outline=(255, 235, 225), width=4)


def label(d, xy, text, off, size=30, sub=None, col=(245, 243, 232), sub_col=(198, 212, 220),
          align='left', leader=True):
    """Place a label near `xy` (marker) at xy+off, with a thin leader line back to the marker."""
    x, y = xy
    f = font(size, 800)
    w = d.textlength(text, font=f)
    tx, ty = x + off[0], y + off[1]
    if align == 'center':
        tx -= w / 2
    elif align == 'right':
        tx -= w
    if leader:
        ey = ty + size * .60
        ex = min(max(x, tx - 6), tx + w + 6)
        dx, dy = ex - x, ey - y
        L = math.hypot(dx, dy) or 1
        d.line((x + dx / L * 17, y + dy / L * 17, ex, ey), fill=(240, 233, 206), width=3)
    d.text((tx, ty), text, font=f, fill=col, stroke_width=6, stroke_fill=INK)
    if sub:
        fs = font(int(size * .72))
        sw = d.textlength(sub, font=fs)
        sx = tx if align == 'left' else (tx + w - sw if align == 'right' else tx + (w - sw) / 2)
        d.text((sx, ty + int(size * 1.16)), sub, font=fs, fill=sub_col, stroke_width=5, stroke_fill=INK)


def route(d, pts, col, label_text=None, lab_at=0.5, width=8, dash=30, lab_off=0):
    segs = []
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(L // dash))
        for i in range(n):
            s, e = i / n, min(1.0, (i + .55) / n)
            segs.append((a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s,
                         a[0] + (b[0] - a[0]) * e, a[1] + (b[1] - a[1]) * e))
    for x0, y0, x1, y1 in segs:
        d.line((x0, y0, x1, y1), fill=col, width=width)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ang = math.atan2(y1 - y0, x1 - x0)
    hl = 26
    d.polygon([(x1, y1),
               (x1 - hl * math.cos(ang - .42), y1 - hl * math.sin(ang - .42)),
               (x1 - hl * math.cos(ang + .42), y1 - hl * math.sin(ang + .42))], fill=col)
    if label_text:
        i = max(1, int((len(pts) - 1) * lab_at))
        a, b = pts[i - 1], pts[i]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        f = font(28, 800)
        w = d.textlength(label_text, font=f)
        d.rounded_rectangle((mx - w / 2 - 12, my - 22 + lab_off, mx + w / 2 + 12, my + 22 + lab_off),
                            8, fill=(6, 16, 26), outline=col, width=3)
        d.text((mx - w / 2, my - 18 + lab_off), label_text, font=f, fill=(242, 242, 236))


def caption(d, text, size=30):
    f = font(size, 800, serif=True)
    d.text((26, 20), text, font=f, fill=(248, 246, 236), stroke_width=7, stroke_fill=INK)


def note(d, text, xy, size=24, col=(214, 222, 226)):
    f = font(size, 700)
    d.text(xy, text, font=f, fill=col, stroke_width=5, stroke_fill=INK)


def water_label(d, text, xy, size=26):
    f = font(size, 600)
    d.text(xy, text, font=f, fill=(146, 182, 210), stroke_width=4, stroke_fill=INK)


def attribution(im, d):
    f = font(21, 700)
    w = d.textlength(ATTR, font=f)
    d.rectangle((im.width - w - 34, im.height - 38, im.width - 10, im.height - 8), fill=(6, 16, 26, 228))
    d.text((im.width - w - 22, im.height - 34), ATTR, font=f, fill=(200, 212, 218))


# ---------------------------------------------------------------- 1. castle / fort layout
def draw_situ(im, d, at):
    caption(d, '城と砦の配置（模式図）')
    for k, lab, kind, off, sub, sub_col in [
            ('narumi', '鳴海城', 'castle', (30, -54), '今川方', (255, 172, 120)),
            ('nakajima', '中嶋砦', 'fort', (-196, -50), '織田方', (126, 194, 255)),
            ('zenshoji', '善照寺砦', 'fort', (78, -36), '織田方', (126, 194, 255)),
            ('washizu', '鷲津砦', 'fort', (-170, -4), '織田方', (126, 194, 255)),
            ('marune', '丸根砦', 'fort', (-178, 12), '織田方', (126, 194, 255)),
            ('odaka', '大高城', 'castle', (24, 26), '今川方', (255, 172, 120)),
            ('okehazama_den', '桶狭間', 'battle', (26, -78), '古戦場伝説地', (250, 226, 160))]:
        marker(d, at(k), kind)
        label(d, at(k), lab, off, 30, sub, sub_col=sub_col)
    note(d, '※この図の範囲外は省略', (26, im.height - 44))


# ---------------------------------------------------------------- 2. the march
def draw_march(im, d, at):
    caption(d, '両軍の動き（模式図）')
    org, blu = (255, 150, 90), (120, 190, 255)
    route(d, [at('kutsukake'), at('odaka'), at('okehazama_den')], org, '今川軍', .5, 8, 30, -50)
    route(d, [at('kiyosu'), at('atsuta'), at('zenshoji'), at('nakajima'), at('okehazama_den')],
          blu, '織田軍', .45, 8, 30, 34)
    for k, lab, kind, off, sub, sub_col, *al in [
            ('kiyosu', '清洲城', 'castle', (-148, -30), '5/19 4時ごろ', (206, 218, 226)),
            ('atsuta', '熱田神宮', 'fort', (24, -44), '8時ごろ', (206, 218, 226)),
            ('kutsukake', '沓掛城', 'castle', (24, -78), '今川方', (255, 172, 120)),
            ('zenshoji', '善照寺砦', 'fort', (-40, -46), None, None, 'right'),
            ('okehazama_den', '桶狭間', 'battle', (-26, -40), None, None, 'right')]:
        marker(d, at(k), kind)
        label(d, at(k), lab, off, 30, sub, sub_col=sub_col, align=al[0] if al else 'left')
    note(d, '矢印は位置関係の模式図です。', (26, im.height - 74))
    water_label(d, '伊勢湾', (26, im.height - 132))


# ---------------------------------------------------------------- 3. battlefield
def draw_field(im, d, at):
    caption(d, '桶狭間の周辺（模式図）')
    for k, lab, kind, off, sub, sub_col in [
            ('odaka', '大高城', 'castle', (-107, 10), '今川方', (255, 172, 120)),
            ('okehazama_park', '古戦場公園', 'spot', (36, -64), '名古屋市緑区', (206, 218, 226)),
            ('okehazama_den', '古戦場伝説地', 'battle', (44, 20), '豊明市', (206, 218, 226)),
            ('taragakubo', '田楽ケ窪', 'spot', (30, -8), '義元戦死の地とされる', (206, 218, 226)),
            ('kutsukake', '沓掛城', 'castle', (-104, -52), '今川方', (255, 172, 120))]:
        marker(d, at(k), kind)
        label(d, at(k), lab, off, 29, sub, sub_col=sub_col)
    # the disputed 桶狭間山 area: a dashed ring, not a point
    cx, cy = at(HILL)
    rx, ry = 62, 46
    for k in range(0, 48, 2):
        d.arc((cx - rx, cy - ry, cx + rx, cy + ry), k / 48 * 360, (k + 1) / 48 * 360,
              fill=(240, 210, 130), width=6)
    label(d, (cx, cy), '桶狭間山の候補地', (0, ry + 16), 27, '位置は諸説あり',
          col=(250, 226, 160), sub_col=(250, 226, 160), align='center', leader=False)


# ---------------------------------------------------------------- 4. thumbnail background
def draw_thumb(im, d, at):
    org, blu = (255, 150, 90), (120, 190, 255)
    route(d, [at('kutsukake'), at('odaka'), at('okehazama_den')], org, None, .5, 11, 36)
    route(d, [at('kiyosu'), at('atsuta'), at('zenshoji'), at('nakajima'), at('okehazama_den')],
          blu, None, .5, 11, 36)
    marker(d, at('okehazama_den'), 'battle')


# ---------------------------------------------------------------- 5. windows
# 切り出しの条件を表にしておく。地図の上で軍勢を動かす（vp_anim.oke_march）ときに、
# 場所の画素位置が要るので、build() と同じ式を map_at() からも使えるようにしている。
MAPS = {
    'map_situ': (15, 136.925, 137.000, 35.038, 35.100, 900, 680, draw_situ),
    'map_march': (14, 136.775, 137.075, 35.035, 35.260, 900, 676, draw_march),
    'map_field': (15, 136.942, 137.032, 35.034, 35.086, 900, 672, draw_field),
    'thumb_art': (14, 136.596, 137.084, 35.035, 35.260, 1280, 720, draw_thumb),
}


def map_at(name):
    """地図画像の中の座標を返す関数をつくる（左上=(0,0)、右下=(out_w,out_h)）。"""
    z, lon0, lon1, lat0, lat1, out_w, out_h = MAPS[name][:7]
    xa, ya = txy(lon0, lat1, z)
    xb, yb = txy(lon1, lat0, z)
    x0, y0 = int(math.floor(xa)), int(math.floor(ya))
    box = (int(xa * 256 - x0 * 256), int(ya * 256 - y0 * 256),
           int(xb * 256 - x0 * 256), int(yb * 256 - y0 * 256))

    def at(k):
        lon, lat = PT[k] if isinstance(k, str) else k[:2]
        mx, my = txy(lon, lat, z)
        return ((mx * 256 - x0 * 256 - box[0]) / (box[2] - box[0]) * out_w,
                (my * 256 - y0 * 256 - box[1]) / (box[3] - box[1]) * out_h)

    return at


if __name__ == '__main__':
    TILES.mkdir(parents=True, exist_ok=True)
    for _n, (_z, _lo0, _lo1, _la0, _la1, _w, _h, _fn) in MAPS.items():
        build(_n, _z, _lo0, _lo1, _la0, _la1, _w, _h, _fn)
    print('done')
