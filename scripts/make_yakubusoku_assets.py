"""役不足の動画（yakubusoku）の素材。文化庁の調査結果の数字から、棒グラフを自作する。
出力：assets/yakubusoku/chart_h14.png / chart_h18.png / chart_diff.png。usage: python scripts/make_yakubusoku_assets.py"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FD = 'C:/Windows/Fonts/'
OUT = Path(__file__).resolve().parents[1] / 'assets' / 'yakubusoku'


def font(size, w=800):
    f = ImageFont.truetype(FD + 'NotoSansJP-VF.ttf', size); f.set_variation_by_axes([w]); return f


def chart(name, title, rows, note=None):
    W, H = 1600, 700
    im = Image.new('RGB', (W, H), (255, 252, 244)); d = ImageDraw.Draw(im)
    d.text((W // 2, 62), title, font=font(60), fill=(40, 40, 60), anchor='mm')
    y = 150; bh = 190; x0 = 60; xmax = W - 60
    for lab, val, col in rows:
        d.text((x0, y), lab, font=font(48), fill=(40, 40, 60), anchor='lt')
        by = y + 70
        d.rounded_rectangle((x0, by, xmax, by + 100), 16, fill=(228, 224, 214))
        wbar = int((xmax - x0) * val / 70.0)
        d.rounded_rectangle((x0, by, x0 + wbar, by + 100), 16, fill=col)
        d.text((x0 + wbar - 24 if wbar > 420 else x0 + wbar + 24, by + 50), f'{val}％', font=font(78), fill=(255, 255, 255) if wbar > 420 else col, anchor='rm' if wbar > 420 else 'lm', stroke_width=0)
        y += bh + 40
    if note:
        d.text((W // 2, H - 52), note, font=font(40, 600), fill=(90, 90, 110), anchor='mm')
    im.save(OUT / f'{name}.png'); print(name)


ORG = (232, 120, 40); BLU = (40, 110, 200)
chart('chart_h14', '平成14年度の調査（文化庁）', [('(ア) 役目が重すぎる', 62.8, ORG), ('(イ) 役目が軽すぎる（本来の意味）', 27.6, BLU)], '例文：「彼には役不足の仕事だ。」')
chart('chart_h18', '平成18年度の調査（文化庁）', [('(ア) 役目が重すぎる', 50.3, ORG), ('(イ) 役目が軽すぎる（本来の意味）', 40.3, BLU)], '例文：「彼には役不足の仕事だ。」')
