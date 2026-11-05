"""shodo_heritage の背景（模式図）を作る。画像は git 管理外。

usage: python scripts/make_shodo_heritage_assets.py
出力: assets/shodo_heritage/bg_ink.png, bg_flow.png（1080x1920）
中央はテロップ用に空け、資料ではなく模式図であることを明記する。
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'shodo_heritage'
W, H = 1080, 1920
FONT = 'C:/Windows/Fonts/NotoSansJP-VF.ttf'
GOLD = (239, 201, 118)
DIM = (190, 205, 208)
INK = (12, 20, 30)


def font(size, weight=500):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def backdrop():
    im = Image.new('RGB', (W, H), (7, 24, 36))
    d = ImageDraw.Draw(im, 'RGBA')
    for y in range(H):
        k = y / H
        d.line([(0, y), (W, y)], fill=(int(7 + 9 * (1 - k)), int(24 + 13 * (1 - k)), int(36 + 18 * (1 - k))))
    return im, d


def brush_strokes(d, cx, cy, scale=1.0):
    """墨の筆致を思わせる、太さの変わる線（模式図）。"""
    import math

    def tapered(x0, y0, x1, y1, wmax, alpha, curve=0.0):
        n = 80
        left, right = [], []
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / length, dx / length
        for i in range(n + 1):
            t = i / n
            x = x0 + dx * t
            y = y0 + dy * t + curve * math.sin(math.pi * t)
            w = wmax * (math.sin(math.pi * t) ** 0.55)
            left.append((x + nx * w / 2, y + ny * w / 2))
            right.append((x - nx * w / 2, y - ny * w / 2))
        d.polygon(left + right[::-1], fill=(238, 235, 224, alpha))

    s = scale
    tapered(cx - 330 * s, cy - 130 * s, cx + 300 * s, cy - 170 * s, 46 * s, 225, 26 * s)
    tapered(cx - 250 * s, cy + 20 * s, cx + 250 * s, cy - 10 * s, 30 * s, 200, -18 * s)
    tapered(cx - 150 * s, cy + 150 * s, cx + 120 * s, cy + 120 * s, 14 * s, 170, 10 * s)
    d.ellipse((cx + 250 * s, cy + 90 * s, cx + 268 * s, cy + 108 * s), fill=(238, 235, 224, 190))
    d.ellipse((cx - 300 * s, cy + 120 * s, cx - 288 * s, cy + 132 * s), fill=(238, 235, 224, 160))


def build_ink():
    im, d = backdrop()
    brush_strokes(d, W / 2, 980, 1.0)
    d.text((W // 2, 452), '模式図：墨と筆のイメージ（資料の複製ではありません）',
           font=font(24, 500), fill=DIM + (210,), anchor='mm')
    d.rounded_rectangle((60, 560, W - 60, 1420), 24, outline=GOLD + (90,), width=3)
    d.text((W // 2, 1600), '出典：NHK NEWS WEB（2026-11-05）／文化庁の発表による',
           font=font(23, 500), fill=DIM + (180,), anchor='mm')
    im.save(OUT / 'bg_ink.png', optimize=True)
    print('wrote bg_ink.png')


def build_flow():
    im, d = backdrop()
    d.text((W // 2, 452), '模式図：無形文化遺産の登録手続き（一般的な流れ）',
           font=font(24, 500), fill=DIM + (210,), anchor='mm')

    boxes = [(700, '評価機関'), (940, '勧告'), (1180, '政府間委員会')]
    for i, (y, label) in enumerate(boxes):
        d.rounded_rectangle((150, y - 62, W - 150, y + 62), 18,
                            fill=(10, 30, 44, 235), outline=GOLD + (150,), width=3)
        d.text((W // 2, y), label, font=font(46, 640), fill=GOLD + (240,), anchor='mm')
        if i < len(boxes) - 1:
            y2 = y + 62
            d.line([(W // 2, y2 + 12), (W // 2, y2 + 176)], fill=DIM + (160,), width=5)
            d.polygon([(W // 2 - 16, y2 + 160), (W // 2 + 16, y2 + 160), (W // 2, y2 + 196)],
                      fill=DIM + (200,))
    d.text((W // 2, 1600), '出典：NHK NEWS WEB（2026-11-05）／文化庁の発表による',
           font=font(23, 500), fill=DIM + (180,), anchor='mm')
    im.save(OUT / 'bg_flow.png', optimize=True)
    print('wrote bg_flow.png')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    build_ink()
    build_flow()


if __name__ == '__main__':
    main()
