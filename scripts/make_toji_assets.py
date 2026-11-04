"""冬至の動画の背景と図を作る（ChatGPTを使わず、PILで自作）。
出力: assets/toji/*.png
usage: python scripts/make_toji_assets.py
"""
import math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

R = Path(__file__).resolve().parents[1]
OUT = R / 'assets' / 'toji'
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1920, 1080
FONT = 'C:/Windows/Fonts/NotoSansJP-VF.ttf'


def font(size, weight=900):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight])
    return f


def gradient(top, bottom, glow=None, glow_r=0.55, glow_k=1.0, bands=0.0):
    y = np.linspace(0, 1, H)[:, None]
    arr = np.array(top, float) * (1 - y) + np.array(bottom, float) * y
    arr = np.repeat(arr[:, None, :], W, axis=1)
    if glow:
        gx, gy = glow[0] * W, glow[1] * H
        yy, xx = np.mgrid[0:H, 0:W]
        d = np.sqrt(((xx - gx) / (W * glow_r)) ** 2 + ((yy - gy) / (H * glow_r)) ** 2)
        k = np.clip(1 - d, 0, 1) ** 2 * glow_k
        arr = arr + np.array(glow[2], float)[None, None, :] * k[:, :, None]
    if bands:
        yy, xx = np.mgrid[0:H, 0:W]
        s = (np.sin((xx * 0.8 + yy * 1.6) / 90.0) * 0.5 + 0.5) ** 3
        arr = arr + s[:, :, None] * bands
    return np.clip(arr, 0, 255)


def vignette(arr, k=0.35):
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    v = np.clip(1 - k * np.clip(d - 0.55, 0, None) ** 1.6, 0, 1)
    return arr * v[:, :, None]


def sun_disc(arr, cx, cy, r, col, halo=3.2, halo_k=0.9):
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt((xx - cx * W) ** 2 + (yy - cy * H) ** 2)
    glow = np.clip(1 - d / (r * halo), 0, 1) ** 2.2 * halo_k
    arr = arr + np.array(col, float)[None, None, :] * glow[:, :, None]
    disc = np.clip((r - d) / 3.0, 0, 1)[:, :, None]
    return arr * (1 - disc) + np.array(col, float)[None, None, :] * disc


def noise(arr, amt=3.0):
    rng = np.random.default_rng(7)
    return np.clip(arr + rng.normal(0, amt, (H, W, 1)), 0, 255)


def save(arr, name):
    Image.fromarray(arr.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.4)).save(OUT / name)
    print('wrote', name)


def scene_intro():
    a = gradient((14, 20, 54), (196, 74, 36), glow=(0.66, 0.70, (255, 170, 90)), glow_r=0.5, bands=6)
    a = sun_disc(a, 0.66, 0.715, 120, (255, 214, 150), halo=4.0, halo_k=0.8)
    # 地平線
    a[int(H * 0.735):] *= 0.82
    save(vignette(noise(a), .45), 'art_intro.png')


def scene_toji():
    a = gradient((10, 28, 66), (120, 176, 210), glow=(0.5, 0.85, (255, 230, 180)), glow_r=0.6, bands=4)
    a = sun_disc(a, 0.5, 0.60, 84, (255, 240, 205), halo=4.5, halo_k=0.55)
    a[int(H * 0.80):] *= 0.88
    save(vignette(noise(a), .4), 'art_toji.png')


def scene_sunalt():
    a = gradient((10, 16, 40), (34, 48, 96), glow=(0.5, 0.45, (120, 160, 255)), glow_r=0.7, bands=5)
    # 薄い高度線
    yy, xx = np.mgrid[0:H, 0:W]
    for k in range(1, 6):
        line = np.exp(-((yy - H * (0.85 - k * 0.12)) ** 2) / 200.0)
        a = a + line[:, :, None] * 26
    a = sun_disc(a, 0.74, 0.22, 46, (255, 236, 190), halo=5.0, halo_k=0.5)
    save(vignette(noise(a), .42), 'art_sunalt.png')


def scene_temp():
    a = gradient((18, 44, 92), (176, 208, 232), glow=(0.35, 0.8, (210, 235, 255)), glow_r=0.7, bands=3)
    yy, xx = np.mgrid[0:H, 0:W]
    frost = np.abs(np.sin(xx / 26.0) * np.sin(yy / 34.0)) ** 8
    a = a + frost[:, :, None] * 40
    save(vignette(noise(a), .38), 'art_temp.png')


def scene_why():
    a = gradient((8, 18, 40), (16, 64, 84), glow=(0.5, 0.55, (60, 210, 200)), glow_r=0.55, bands=5)
    yy, xx = np.mgrid[0:H, 0:W]
    for r in (260, 360, 470):
        ring = np.exp(-((np.sqrt((xx - W * .5) ** 2 + (yy - H * .55) ** 2) - r) ** 2) / 300.0)
        a = a + ring[:, :, None] * 22
    save(vignette(noise(a), .45), 'art_why.png')


def scene_sun():
    a = gradient((58, 70, 86), (150, 164, 176), glow=(0.5, 0.35, (220, 225, 230)), glow_r=0.7, bands=3)
    img = Image.fromarray(a.astype(np.uint8))
    dr = ImageDraw.Draw(img, 'RGBA')
    for i in range(-40, 60):
        x = i * 46
        dr.line([(x, -100), (x + 620, H + 100)], fill=(235, 242, 250, 26), width=3)
    save(vignette(noise(np.asarray(img, float)), .35), 'art_sun.png')


def scene_range():
    a = gradient((44, 16, 72), (150, 60, 130), glow=(0.5, 0.75, (255, 140, 200)), glow_r=0.6, bands=5)
    save(vignette(noise(a), .42), 'art_range.png')


def scene_end():
    a = gradient((22, 12, 44), (232, 120, 54), glow=(0.5, 0.78, (255, 200, 120)), glow_r=0.55, bands=6)
    a = sun_disc(a, 0.5, 0.70, 100, (255, 226, 170), halo=4.4, halo_k=0.75)
    a[int(H * 0.78):] *= 0.78
    save(vignette(noise(a), .4), 'art_end.png')


def fig_alt():
    w, h = 1400, 780
    img = Image.new('RGB', (w, h), (16, 20, 38))
    d = ImageDraw.Draw(img, 'RGBA')
    for i in range(h):
        t = i / h
        d.line([(0, i), (w, i)], fill=(int(16 + 18 * t), int(20 + 22 * t), int(38 + 46 * t)))
    panels = [(30, 690, '冬至', 30.9, (255, 190, 110)), (710, 1370, '夏至', 77.8, (255, 236, 160))]
    for x0, x1, name, alt, col in panels:
        ox = (x0 + x1) / 2
        ground = 640
        d.rounded_rectangle((x0, 70, x1, 730), 24, fill=(10, 14, 30, 160), outline=(255, 255, 255, 60), width=3)
        d.text((ox, 120), name, font=font(60), fill=(255, 255, 255), anchor='mm')
        d.line([(x0 + 40, ground), (x1 - 40, ground)], fill=(255, 255, 255, 210), width=5)
        r = 258
        th = math.radians(alt)
        sx, sy = ox + r * math.cos(th), ground - r * math.sin(th)
        # 角度の弧
        pts = [(ox + 150 * math.cos(math.radians(a)), ground - 150 * math.sin(math.radians(a)))
               for a in np.linspace(0, alt, 60)]
        d.line(pts, fill=col + (230,), width=6)
        # 視線
        for k in range(0, 20):
            t0, t1 = k / 20, (k + 0.55) / 20
            d.line([(ox + (sx - ox) * t0, ground + (sy - ground) * t0),
                    (ox + (sx - ox) * t1, ground + (sy - ground) * t1)], fill=(255, 255, 255, 120), width=4)
        # 太陽
        d.ellipse((sx - 46, sy - 46, sx + 46, sy + 46), fill=col + (255,), outline=(255, 255, 255, 255), width=4)
        d.text((sx, sy - 96), f'{alt}度', font=font(52), fill=col, anchor='mm',
               stroke_width=6, stroke_fill=(10, 12, 26))
        d.text((ox, 700), '南中の太陽の高さ', font=font(34), fill=(220, 226, 240), anchor='mm')
    d.text((40, 20), '模式図：角度は南中高度（数値は国立天文台の暦）', font=font(30), fill=(210, 216, 232))
    img.save(OUT / 'fig_alt.png')
    print('wrote fig_alt.png')


def thumb():
    w, h = 1280, 720
    img = Image.new('RGB', (w, h), (0, 0, 0))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=(int(18 + 200 * t ** 2), int(20 + 70 * t ** 2), int(56 + 20 * t)))
    # 低い太陽（外側ほど暗い輪で、にじませる）
    cx, cy, r = 900, 470, 130
    for k in range(18, 0, -1):
        rr = int(r * (1 + k * 0.13))
        c = (255 - k * 5, 170 - k * 4, 100 - k * 3)
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=c)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 226, 170))
    d.rectangle((0, 520, w, 530), fill=(20, 24, 40))
    img.save(OUT / 'thumb_art.png')
    print('wrote thumb_art.png')


if __name__ == '__main__':
    scene_intro(); scene_toji(); scene_sunalt(); scene_temp(); scene_why()
    scene_sun(); scene_range(); scene_end(); fig_alt(); thumb()
