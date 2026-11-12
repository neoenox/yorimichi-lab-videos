"""「伝源頼朝像」Shorts（shorts/yoritomo_zo）の背景画像を作る。

入力: assets/yoritomo_zo/src_portrait.jpg
      ＝ Wikimedia Commons File:Minamoto no Yoritomo.jpg（1584x1974、PD-Art / PD-old-100-expired）
        出典・撮影者は "Unknown source"（Commons のファイルページ表記）
出力: assets/yoritomo_zo/bg_0.png 〜 bg_6.png（1080x1920）

画面の安全領域（docs/SHORTS_PRODUCTION_NOTES.md の実測値）:
- タイトル y=190 ／ 大テロップ（big）は viz 無しで y=520 中心、viz 有りで y=430
- 字幕パネル y=1240〜1540 ／ 注記（クレジット）y>1556
したがって **肖像の顔は y≈1000〜1100** に置くと、大テロップと字幕の間に顔が来る。

場面の種類で2通り作る:
- face:  顔を見せる場面。肖像を 1.0〜1.2 倍で置き、地の色になじませる
- soft:  自作の図（viz）を重ねる場面。肖像をぼかして図の下地にする
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'assets' / 'yoritomo_zo' / 'src_portrait.jpg'
OUT = ROOT / 'assets' / 'yoritomo_zo'
W, H = 1080, 1920

FACE_SRC_Y = 700.0   # 元画像での顔の中心（_grid.png で実測）

TINTS = [(16, 28, 44), (22, 26, 34), (18, 30, 40), (26, 24, 38), (20, 26, 32), (30, 26, 30), (14, 24, 38)]


def font(size):
    for cand in (ROOT / 'assets' / 'fonts' / 'NotoSansJP-Regular.ttf',
                 Path('C:/Windows/Fonts/NotoSansJP-VF.ttf'),
                 Path('C:/Windows/Fonts/meiryo.ttc')):
        if cand.exists():
            return ImageFont.truetype(str(cand), size)
    return ImageFont.load_default()


def gradient(tint):
    im = Image.new('RGB', (W, H))
    px = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H
        c = tuple(int(v * (1.30 - 0.62 * k)) for v in tint)
        px.line([(0, y), (W, y)], fill=c)
    d = ImageDraw.Draw(im, 'RGBA')
    for x in range(-H, W, 96):
        d.line([(x, H), (x + H // 2, 0)], fill=(255, 255, 255, 6), width=2)
    return im


def portrait(height, face_y, bright=1.0, blur=0.0):
    """肖像を height の高さで置き、顔の中心が画面 y=face_y に来るようにする。"""
    src = Image.open(SRC).convert('RGB')
    if bright != 1.0:
        src = ImageEnhance.Brightness(src).enhance(bright)
    s = height / src.height
    pw = int(src.width * s)
    im = src.resize((pw, height), Image.LANCZOS)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    y_top = int(face_y - FACE_SRC_Y * s)
    return im, y_top, s


def compose(tint, height, face_y, bright=1.0, blur=0.0, feather=140, top_feather=340):
    """肖像の縁をぼかして地の色になじませる（硬い境界線を出さない）。
    上端は特に強くぼかす（絵の上部が横一直線に見えないように）。"""
    im = gradient(tint)
    p, y_top, scale = portrait(height, face_y, bright, blur)
    x = (W - p.width) // 2
    mask = Image.new('L', (p.width, p.height), 255)
    md = ImageDraw.Draw(mask)
    if feather:
        md.rectangle((0, 0, feather, p.height), fill=0)
        md.rectangle((p.width - feather, 0, p.width, p.height), fill=0)
    if top_feather:
        for y in range(min(top_feather, p.height)):
            v = int(255 * (y / top_feather) ** 1.5)
            md.line([(feather, y), (p.width - feather, y)], fill=v)
    md.rectangle((0, p.height - feather, p.width, p.height), fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(60))
    im.paste(p, (x, y_top), mask)
    return im, x, y_top, scale


def vignette(im, strength=0.55):
    g = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(g)
    for i in range(60):
        a = int(255 * (i / 60) ** 1.6 * strength)
        d.rectangle((i * 9, i * 16, W - i * 9, H - i * 16), outline=a)
    black = Image.new('RGB', (W, H), (4, 10, 18))
    return Image.composite(black, im, g.filter(ImageFilter.GaussianBlur(60)))


def shade(im, top=1180, strength=170):
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for y in range(top, H):
        a = int(strength * min(1.0, (y - top) / (H - top)))
        d.line([(0, y), (W, y)], fill=(5, 12, 20, a))
    return Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')


def credit(im, sub='画像：Wikimedia Commons（PD-Art）'):
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((0, 1610, W, H), fill=(4, 10, 18, 205))
    d.text((92, 1631), '資料：伝源頼朝像（神護寺蔵・国宝）', font=font(28), fill=(214, 222, 232))
    d.text((92, 1677), sub, font=font(28), fill=(160, 174, 190))
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # bg_0: 冒頭（図なし・大テロップ y=520）。顔は y=1060
    im = compose(TINTS[0], 1560, 1060, bright=0.98)[0]
    im = vignette(im, 0.42); im = shade(im, 1150, 175)
    credit(im).save(OUT / 'bg_0.png')

    # bg_1: 全体（図なし）。「源頼朝」→「伝源頼朝像」の場面。少し引いて服装まで
    im = compose(TINTS[1], 1420, 1030, bright=1.0)[0]
    im = vignette(im, 0.48); im = shade(im, 1130, 185)
    credit(im).save(OUT / 'bg_1.png')

    # bg_2: 図あり（timeline）。ぼかして下地に
    im = compose(TINTS[2], 1500, 900, bright=0.92, blur=7)[0]
    im = vignette(im, 0.45); im = shade(im, 1100, 190)
    credit(im).save(OUT / 'bg_2.png')

    # bg_3: 図あり（2択）。少しだけぼかす（新説の場面は顔を見せたい）
    im = compose(TINTS[3], 1450, 880, bright=0.88, blur=3)[0]
    im = vignette(im, 0.48); im = shade(im, 1100, 195)
    credit(im).save(OUT / 'bg_3.png')

    # bg_4: 図あり（根拠の3つの札を重ねる）。ぼかして下地に
    #   ※ 肖像への引き出し線は焼き込まない。字幕域（1240〜1540）と重なり、
    #     ラベルが笏・袍の上に落ちて読みにくかったため（2026-11-12 の試作で確認）
    im = compose(TINTS[4], 1440, 880, bright=0.86, blur=6)[0]
    im = vignette(im, 0.45); im = shade(im, 1090, 195)
    credit(im).save(OUT / 'bg_4.png')

    # bg_5: 図あり（反論の構図）。ぼかす
    im = compose(TINTS[5], 1480, 880, bright=0.88, blur=8)[0]
    im = vignette(im, 0.50); im = shade(im, 1090, 195)
    credit(im).save(OUT / 'bg_5.png')

    # bg_6: 結論（図なし・大テロップ）。顔を中くらいに
    im = compose(TINTS[6], 1520, 1050, bright=0.88)[0]
    im = vignette(im, 0.52); im = shade(im, 1120, 185)
    credit(im).save(OUT / 'bg_6.png')

    for i in range(7):
        p = OUT / f'bg_{i}.png'
        print(p.name, p.stat().st_size)


if __name__ == '__main__':
    main()
