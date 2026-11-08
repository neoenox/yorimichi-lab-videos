"""アララ不正アクセスShort用の自作背景（1080x1920）。封筒・ネットワーク・疑問符の抽象図。assets/arara/bg_*.png"""
import random, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
R = Path(__file__).resolve().parents[1]
W, H = 1080, 1920
GOLD = (214, 164, 70); RED = (232, 86, 74); TEAL = (70, 150, 190)

def base(c1=(5, 14, 24), c2=(14, 36, 58)):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)))
    for x in range(0, W, 90): d.line([(x, 0), (x, H)], fill=(255, 255, 255, 0) if False else (22, 44, 64), width=1)
    for y in range(0, H, 90): d.line([(0, y), (W, y)], fill=(22, 44, 64), width=1)
    return im

def envelope(d, x, y, w, col, a=255, fill=None):
    h = int(w * 0.68)
    d.rounded_rectangle((x, y, x + w, y + h), 8, outline=col + (a,), width=4, fill=(fill or (8, 24, 38)) + (a,))
    d.line([(x, y), (x + w / 2, y + h * 0.58), (x + w, y)], fill=col + (a,), width=4)

def glow(im, blur=14):
    return Image.blend(im, im.filter(ImageFilter.GaussianBlur(blur)), 0.0)

def bg_mail(seed, n, col, spread=1.0, name='mail'):
    random.seed(seed); im = base().convert('RGBA'); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for _ in range(n):
        w = random.randint(70, 230); x = random.randint(-30, W - w + 30); y = random.randint(340, H - 300)
        envelope(d, x, y, w, col, a=random.randint(60, 170))
    g = lay.filter(ImageFilter.GaussianBlur(10)); im = Image.alpha_composite(im, g); im = Image.alpha_composite(im, lay)
    im.convert('RGB').save(R / 'assets' / 'arara' / f'bg_{name}.png')

def bg_net(seed, hub_col, name='net'):
    random.seed(seed); im = base().convert('RGBA'); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    hub = (540, 800); pts = [(random.randint(60, W - 60), random.randint(420, H - 380)) for _ in range(34)]
    for p in pts:
        d.line([hub, p], fill=hub_col + (70,), width=2)
    for i, p in enumerate(pts):
        for q in pts[i + 1:i + 3]:
            d.line([p, q], fill=TEAL + (60,), width=2)
    for p in pts:
        r = random.randint(8, 20); d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=TEAL + (150,), outline=(190, 220, 240, 200), width=2)
    for r, a in ((120, 40), (80, 70), (46, 200)):
        d.ellipse((hub[0] - r, hub[1] - r, hub[0] + r, hub[1] + r), fill=hub_col + (a,))
    g = lay.filter(ImageFilter.GaussianBlur(12)); im = Image.alpha_composite(im, g); im = Image.alpha_composite(im, lay)
    im.convert('RGB').save(R / 'assets' / 'arara' / f'bg_{name}.png')

def bg_q(seed, name='q'):
    random.seed(seed); im = base().convert('RGBA'); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    from PIL import ImageFont
    f = ImageFont.truetype('C:/Windows/Fonts/YuGothB.ttc', 300) if Path('C:/Windows/Fonts/YuGothB.ttc').exists() else ImageFont.load_default()
    for _ in range(9):
        x = random.randint(40, W - 200); y = random.randint(380, H - 500)
        d.text((x, y), '?', font=ImageFont.truetype(f.path, random.randint(160, 380)) if hasattr(f, 'path') else f, fill=GOLD + (random.randint(40, 90),))
    for _ in range(5):
        envelope(d, random.randint(40, W - 240), random.randint(500, H - 500), random.randint(120, 200), TEAL, a=70)
    g = lay.filter(ImageFilter.GaussianBlur(6)); im = Image.alpha_composite(im, g); im = Image.alpha_composite(im, lay)
    im.convert('RGB').save(R / 'assets' / 'arara' / f'bg_{name}.png')

bg_mail(1, 22, GOLD, name='mail')
bg_mail(2, 70, RED, name='mail_many')
bg_net(3, RED, name='net')
bg_q(4)
print('ok')
