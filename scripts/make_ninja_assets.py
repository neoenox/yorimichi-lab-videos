"""忍者の動画の素材：『正忍記』の服の色（茶・柿・黒・紺）の色見本。assets/ninja/colors.png。usage: python scripts/make_ninja_assets.py"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
FD = 'C:/Windows/Fonts/'
OUT = Path(__file__).resolve().parents[1] / 'assets' / 'ninja'
OUT.mkdir(parents=True, exist_ok=True)


def font(size, w=800):
    f = ImageFont.truetype(FD + 'NotoSansJP-VF.ttf', size); f.set_variation_by_axes([w]); return f


W, H = 1600, 600
im = Image.new('RGB', (W, H), (255, 252, 244)); d = ImageDraw.Draw(im)
d.text((W // 2, 56), '『正忍記』に挙げられた服の色（国立国会図書館の解説）', font=font(48), fill=(40, 40, 60), anchor='mm')
cols = [('茶色', (122, 82, 48)), ('柿色', (219, 112, 52)), ('黒色', (30, 30, 34)), ('紺色', (28, 48, 100))]
cw = 330; gap = 40; x0 = (W - (cw * 4 + gap * 3)) // 2
for i, (n, c) in enumerate(cols):
    x = x0 + i * (cw + gap)
    d.rounded_rectangle((x, 130, x + cw, 480), 28, fill=c, outline=(40, 40, 60), width=5)
    d.text((x + cw // 2, 540), n, font=font(64), fill=(40, 40, 60), anchor='mm')
im.save(OUT / 'colors.png'); print('colors.png')
