"""edo_map_date の背景イラスト（模式図）を作る。画像は git 管理外（assets/ は .gitignore）。

usage: python scripts/make_edo_map_date_assets.py
出力: assets/edo_map_date/art.png（1600x2400, 9:16 に cover で切れる余白付き）
中央は字幕・テロップ用に空け、下端に「模式図」と出典を明記する。
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'edo_map_date'
W, H = 1600, 2400
FONT = 'C:/Windows/Fonts/NotoSansJP-VF.ttf'
GOLD = (239, 201, 118)
TEAL = (120, 190, 255)


def font(size, weight=500):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    im = Image.new('RGB', (W, H), (7, 24, 36))
    d = ImageDraw.Draw(im, 'RGBA')

    # 背景のグラデーション（上が少し明るい）
    for y in range(H):
        k = y / H
        c = (int(7 + 10 * (1 - k)), int(24 + 14 * (1 - k)), int(36 + 20 * (1 - k)))
        d.line([(0, y), (W, y)], fill=c)

    # 古地図風の薄い格子
    for x in range(0, W, 100):
        d.line([(x, 0), (x, H)], fill=GOLD + (14,), width=1)
    for y in range(0, H, 100):
        d.line([(0, y), (W, y)], fill=GOLD + (14,), width=1)

    # 海岸線のような曲線（模式的なので数本だけ）
    for n, (x0, amp, ph) in enumerate([(180, 70, 0.6), (980, 110, 1.9), (520, 45, 3.1)]):
        pts = [(x0 + 320 * math.sin(y / 260 + ph), y) for y in range(120, H - 260, 24)]
        d.line(pts, fill=TEAL + (38,), width=3)

    # 中央の余白を守るための薄い枠（地図の枠）
    d.rounded_rectangle((90, 300, W - 90, H - 420), 28, outline=GOLD + (90,), width=4)
    d.rounded_rectangle((120, 330, W - 120, H - 450), 22, outline=GOLD + (36,), width=2)

    # 方位記号（右下）
    cx, cy, r = W - 250, H - 560, 70
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=GOLD + (120,), width=3)
    d.line([(cx, cy - r), (cx, cy + r)], fill=GOLD + (120,), width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=GOLD + (120,), width=2)
    d.polygon([(cx, cy - r - 18), (cx - 14, cy - r + 8), (cx + 14, cy - r + 8)], fill=GOLD + (170,))

    # 下端の表示（模式図であることと出典）
    d.text((W // 2, H - 400), '模式図：江戸図の年代を考える', font=font(58, 640), fill=GOLD + (235,), anchor='mm')
    d.text((W // 2, H - 320), '出典：国立国会図書館デジタルコレクションの解説文をもとに作成',
           font=font(34, 500), fill=(190, 205, 208, 220), anchor='mm')
    d.text((W // 2, H - 248), '史実の再現ではなく、年表と手がかりの関係を示す図です',
           font=font(30, 500), fill=(190, 205, 208, 170), anchor='mm')

    path = OUT / 'art.png'
    im.save(path, optimize=True)
    print('wrote', path, path.stat().st_size, 'bytes')


if __name__ == '__main__':
    main()
