"""ラッコShort用の自作背景（1080x1920）。水面と、仰向けに浮かぶラッコのシルエット（模式図）。assets/otter/bg_*.png"""
import random
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
R = Path(__file__).resolve().parents[1]
OUT = R / 'assets' / 'otter'
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1080, 1920


def sea(c1=(8, 30, 52), c2=(14, 70, 96), seed=1):
    random.seed(seed)
    im = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)))
    im = im.convert('RGBA')
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for k in range(26):  # 水面のゆらぎ（横に流れる波線）
        y = random.randint(300, H - 200)
        x0 = random.randint(-200, 600)
        pts = [(x0 + i * 40, y + math.sin(i * 0.9 + k) * 9) for i in range(int(random.randint(8, 18)))]
        ld.line(pts, fill=(150, 210, 230, random.randint(18, 46)), width=3)
    lay = lay.filter(ImageFilter.GaussianBlur(2))
    return Image.alpha_composite(im, lay)


def otter(lay, cx, cy, s, col=(226, 196, 150), a=255):
    """仰向けに浮かぶラッコ（模式図）。s=倍率。"""
    d = ImageDraw.Draw(lay)
    c = col + (a,)
    dark = tuple(int(v * 0.55) for v in col) + (a,)
    d.ellipse((cx - 150 * s, cy - 52 * s, cx + 110 * s, cy + 52 * s), fill=c)  # 胴
    d.ellipse((cx + 70 * s, cy - 46 * s, cx + 160 * s, cy + 40 * s), fill=c)  # 頭
    d.ellipse((cx + 92 * s, cy - 56 * s, cx + 112 * s, cy - 36 * s), fill=c)  # 耳
    d.ellipse((cx + 132 * s, cy - 54 * s, cx + 152 * s, cy - 34 * s), fill=c)
    d.ellipse((cx + 112 * s, cy - 18 * s, cx + 124 * s, cy - 6 * s), fill=dark)  # 目
    d.ellipse((cx + 136 * s, cy - 18 * s, cx + 148 * s, cy - 6 * s), fill=dark)
    d.ellipse((cx + 122 * s, cy - 2 * s, cx + 142 * s, cy + 14 * s), fill=dark)  # 鼻
    d.ellipse((cx + 20 * s, cy - 40 * s, cx + 74 * s, cy - 6 * s), fill=c)  # 前足（胸の上）
    d.ellipse((cx - 190 * s, cy - 22 * s, cx - 110 * s, cy + 26 * s), fill=c)  # 後ろ足
    d.ellipse((cx - 232 * s, cy - 4 * s, cx - 160 * s, cy + 22 * s), fill=c)  # 尾


def finish(im, lay, name, blur=3):
    g = lay.filter(ImageFilter.GaussianBlur(blur))
    im = Image.alpha_composite(im, g)
    im.convert('RGB').save(OUT / f'bg_{name}.png')


def bg_one(name, col=(226, 196, 150), seed=1):
    im = sea(seed=seed)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    otter(lay, 540, 1020, 1.9, col)
    finish(im, lay, name, 2)


def bg_two(name, seed=2):
    im = sea(seed=seed)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    otter(lay, 430, 960, 1.35, (226, 196, 150), 70)  # 昨日までいた1頭（うすく）
    otter(lay, 640, 1280, 1.5, (226, 196, 150), 255)
    finish(im, lay, name, 2)


def bg_many(name, seed=3):
    im = sea((6, 22, 40), (12, 56, 80), seed)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    random.seed(seed)
    for i in range(9):
        x = random.randint(160, 920)
        y = 1380 + i * 52
        otter(lay, x, y, random.uniform(0.5, 0.75), (226, 196, 150), max(30, 200 - i * 16))
    finish(im, lay, name, 2)


def bg_bubbles(name, q=False, seed=4):
    im = sea((6, 20, 36), (10, 48, 70), seed)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    random.seed(seed)
    for _ in range(70):
        r = random.randint(6, 34)
        x = random.randint(20, W - 20)
        y = random.randint(340, H - 240)
        ld.ellipse((x - r, y - r, x + r, y + r), outline=(190, 225, 240, random.randint(50, 130)), width=3)
    if q:
        f = 'C:/Windows/Fonts/YuGothB.ttc'
        for _ in range(7):
            ft = ImageFont.truetype(f, random.randint(170, 360))
            ld.text((random.randint(40, W - 220), random.randint(380, H - 520)), '?', font=ft, fill=(214, 164, 70, random.randint(34, 80)))
    finish(im, lay, name, 5)


bg_one('one', seed=1)
bg_two('two')
bg_many('many')
bg_bubbles('reason')
bg_bubbles('q', q=True, seed=5)
print('ok')
