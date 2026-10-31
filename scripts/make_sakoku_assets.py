"""鎖国の動画（sakoku）の素材。国土地理院のタイルから日本列島の陰影起伏図を作り、四つの窓口の印と矢印を重ねる。
出典：国土地理院（hillshademap・std）。加工して作成。
出力：assets/sakoku/map_s0〜s4.png（s0=印のみ、s1=長崎、s2=対馬、s3=薩摩、s4=松前を強調）。usage: python scripts/make_sakoku_assets.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import gmaps

VIEW = dict(lon0=122.0, lon1=145.5, lat0=26.0, lat1=45.8, z=6)
M = gmaps.Maps('sakoku', {'japan': VIEW})
FD = 'C:/Windows/Fonts/'
SCALE = 2          # 600px高の下地を2倍に拡大して、印や文字を重ねる
PTS = {  # 名前: (経度, 緯度, 相手の呼び名, 矢印の向き(度)・長さ)
    'nagasaki': ('長崎', 129.87, 32.75, 'オランダ・中国', 255, 230),
    'tsushima': ('対馬', 129.29, 34.20, '朝鮮', 320, 150),
    'satsuma': ('薩摩', 130.56, 31.60, '琉球', 175, 170),
    'matsumae': ('松前', 140.11, 41.43, '蝦夷地', 25, 150),
}
COL = (255, 196, 50)
DIM = (150, 160, 175)


def font(size):
    f = ImageFont.truetype(FD + 'NotoSansJP-VF.ttf', size); f.set_variation_by_axes([800]); return f


def base():
    w, h = M.size('japan')
    hs = M._mosaic(VIEW, 'hs', w).convert('RGB'); std = M._mosaic(VIEW, 'std', w).convert('RGB')
    g = np.asarray(hs, dtype=float).mean(-1, keepdims=True) / 255.
    shade = np.clip(g * np.array(gmaps.LAND) * 1.34 + 0.035, 0, 1)
    s = np.asarray(std, dtype=float)
    wmask = (s[..., 2] >= 245) & (s[..., 2] - s[..., 0] >= 60) & (s[..., 1] - s[..., 0] >= 8)
    miss = (np.asarray(hs)[..., 0] == 200) & (np.asarray(hs)[..., 1] == 200) & (np.asarray(hs)[..., 2] == 200)
    wmask = wmask | miss
    rgb = np.where(wmask[..., None], np.array([0.10, 0.27, 0.50]), shade)
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype('uint8'), 'RGB')
    return im.resize((w * SCALE, h * SCALE), Image.LANCZOS)


def arrow(d, x, y, ang, ln, col, wid=18):
    import math
    a = math.radians(ang)
    ex, ey = x + ln * math.sin(a), y - ln * math.cos(a)
    d.line((x, y, ex, ey), fill=col, width=wid)
    hd = 52
    for da in (150, -150):
        b = a + math.radians(da)
        d.line((ex, ey, ex + hd * math.sin(b), ey - hd * math.cos(b)), fill=col, width=wid)
    return ex, ey


def render(sel):
    im = base().convert('RGBA'); d = ImageDraw.Draw(im, 'RGBA'); W, H = im.size
    for key, (name, lon, lat, other, ang, ln) in PTS.items():
        nx, ny = M.norm(lon, lat, 'japan'); x, y = nx * W, ny * H
        on = (sel == 'all') or (sel == key)
        col = COL if on else DIM
        if sel != 's0' and not on:
            col = (110, 118, 132)
        r = 36 if on else 22
        d.ellipse((x - r - 6, y - r - 6, x + r + 6, y + r + 6), fill=(0, 0, 0, 170))
        d.ellipse((x - r, y - r, x + r, y + r), fill=col + (255,), outline=(255, 255, 255, 255), width=5)
        if sel == 's0':
            d.text((x + (-40 if key in ('nagasaki', 'tsushima', 'satsuma') else 40), y + (0 if key != 'matsumae' else 4)), name, font=font(74), fill=(255, 255, 255, 255), anchor='rm' if key in ('nagasaki', 'tsushima', 'satsuma') else 'lm', stroke_width=7, stroke_fill=(0, 0, 0, 255))
        if on:
            ex, ey = arrow(d, x, y, ang, ln, col)
            f = font(92); fo = font(80)
            lab = name
            tx, ty = x + (30 if ang < 180 else -30), y + (-30 if key == 'nagasaki' else 22)
            anchor = 'lm' if ang < 180 else 'rm'
            d.text((tx, ty), lab, font=f, fill=(255, 255, 255, 255), anchor=anchor, stroke_width=12, stroke_fill=(0, 0, 0, 255))
            ox, oy = ex + (0 if True else 0), ey + (-34 if ang < 90 or ang > 270 else 34)
            tw = d.textlength(other, font=fo)
            if ex - tw / 2 < 24:
                d.text((24, oy), other, font=fo, fill=col + (255,), anchor='lm', stroke_width=12, stroke_fill=(0, 0, 0, 255))
            else:
                d.text((ex, oy), other, font=fo, fill=col + (255,), anchor='mm', stroke_width=12, stroke_fill=(0, 0, 0, 255))
    fs = font(40)
    txt = '地理院タイル（陰影起伏図・標準地図）を加工して作成'
    d.text((W - 16, H - 14), txt, font=fs, fill=(225, 232, 236, 235), anchor='rd', stroke_width=4, stroke_fill=(0, 0, 0, 220))
    return im.convert('RGB')


if __name__ == '__main__':
    out = Path(__file__).resolve().parents[1] / 'assets' / 'sakoku'; out.mkdir(parents=True, exist_ok=True)
    for name, sel in [('map_s0', 's0'), ('map_s1', 'nagasaki'), ('map_s2', 'tsushima'), ('map_s3', 'satsuma'), ('map_s4', 'matsumae'), ('map_all', 'all')]:
        render(sel).save(out / f'{name}.png'); print(name)
    print(M.size('japan'))
