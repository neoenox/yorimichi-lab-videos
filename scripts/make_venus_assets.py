"""金星の動画（venus）の素材。NASAの表の周期（日数に換算）から、棒グラフを自作する。
出力：assets/venus/chart_days.png。usage: python scripts/make_venus_assets.py"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FD = 'C:/Windows/Fonts/'
OUT = Path(__file__).resolve().parents[1] / 'assets' / 'venus'


def font(size, w=800):
    f = ImageFont.truetype(FD + 'NotoSansJP-VF.ttf', size); f.set_variation_by_axes([w]); return f


def chart(name, title, rows, note=None, vmax=260.0):
    W, H = 1600, 700
    im = Image.new('RGB', (W, H), (255, 252, 244)); d = ImageDraw.Draw(im)
    d.text((W // 2, 56), title, font=font(54), fill=(40, 40, 60), anchor='mm')
    y = 120; bh = 150; x0 = 60; xmax = W - 60
    for lab, val, vlab, col in rows:
        d.text((x0, y), lab, font=font(44), fill=(40, 40, 60), anchor='lt')
        by = y + 58
        d.rounded_rectangle((x0, by, xmax, by + 90), 16, fill=(228, 224, 214))
        wbar = int((xmax - x0) * val / vmax)
        d.rounded_rectangle((x0, by, x0 + wbar, by + 90), 16, fill=col)
        d.text((x0 + wbar - 24, by + 45), vlab, font=font(70), fill=(255, 255, 255), anchor='rm')
        y += bh + 36
    if note:
        d.text((W // 2, H - 36), note, font=font(34, 600), fill=(90, 90, 110), anchor='mm')
    im.save(OUT / f'{name}.png'); print(name)


ORG = (232, 120, 40); BLU = (40, 110, 200); GLD = (214, 150, 10)
chart('chart_days', '金星の周期（NASAの表を、日数に換算）', [
    ('自転周期（遠くの星を基準）', 243.0, '約243日', BLU),
    ('公転周期', 224.7, '224.7日', ORG),
    ('太陽の動きで決める一日', 116.75, '116.75日', GLD)],
    '24時間＝1日で換算（自作の計算）')
