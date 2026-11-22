"""雷と金属Short用の自作嵐イラストを生成する（AI生成・外部素材なし）。
使い方: python scripts/draw_thunder_bg.py
"""
import math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

def main():
    random.seed(1582)
    W, H = 1080, 1920
    out = Path(__file__).resolve().parents[1] / 'assets' / 'thunder_metal' / 'bg_storm.png'
    out.parent.mkdir(parents=True, exist_ok=True)
    im = Image.new('RGB', (W, H)); px = im.load()
    for y in range(H):
        t = y / H
        for x in range(W):
            v = int(14 + 16 * (1 - t) + 6 * math.sin(x / 180 + y / 90))
            px[x, y] = (max(0, v - 2), max(0, v), min(255, v + 14))
    cloud = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cloud, 'RGBA')
    for _ in range(90):
        x = random.randrange(-100, W + 100); y = random.randrange(-80, 950); r = random.randrange(90, 300)
        cd.ellipse((x - r, y - r // 2, x + r, y + r // 2), fill=(70, 86, 110, random.randrange(25, 70)))
    cloud = cloud.filter(ImageFilter.GaussianBlur(45))
    im = Image.alpha_composite(im.convert('RGBA'), cloud)
    d = ImageDraw.Draw(im, 'RGBA')
    def bolt(points, width, color):
        d.line(points, fill=color, width=width, joint='curve')
    pts = [(620, -20), (570, 210), (640, 360), (545, 560), (600, 700), (500, 930), (560, 1090)]
    for w, col in [(36, (150, 190, 255, 34)), (20, (210, 230, 255, 80)),
                   (9, (255, 252, 220, 230)), (3, (255, 255, 255, 255))]:
        bolt(pts, w, col)
    for br in [[(640, 360), (745, 450), (800, 590)], [(545, 560), (440, 650), (390, 790)]]:
        for w, col in [(12, (190, 215, 255, 60)), (4, (255, 250, 220, 180))]:
            bolt(br, w, col)
    for _ in range(420):
        x = random.randrange(W); y = random.randrange(300, H - 80); L = random.randrange(28, 90)
        d.line((x, y, x - 8, y + L), fill=(150, 180, 210, random.randrange(20, 55)), width=2)
    d.polygon([(0, 1780), (180, 1710), (390, 1760), (610, 1680), (830, 1750), (1080, 1690),
               (1080, 1920), (0, 1920)], fill=(4, 9, 16, 255))
    im.convert('RGB').save(out)
    print('wrote', out)

if __name__ == '__main__':
    main()
