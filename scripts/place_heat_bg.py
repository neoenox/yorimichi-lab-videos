"""ChatGPT生成の高温画像(assets/heat/src)を、図(中段)・字幕(下段)と重ならないよう下へずらして1080x1920の背景にする。"""
from pathlib import Path
from PIL import Image, ImageOps
R = Path(__file__).resolve().parents[1]
SHIFT = 620
m = {'one': 'heat_1_one', 'two': 'heat_2_two', 'many': 'heat_3_many', 'reason': 'heat_4_reason', 'q': 'heat_5_q'}
for k, f in m.items():
    im = Image.open(R / 'assets' / 'heat' / 'src' / f'{f}.png').convert('RGB')
    w, h = im.size
    tw = int(h * 1080 / 1920)
    im = im.crop(((w - tw) // 2, 0, (w - tw) // 2 + tw, h)).resize((1080, 1920), Image.LANCZOS)
    out = Image.new('RGB', (1080, 1920))
    out.paste(im.crop((0, 0, 1080, 1920 - SHIFT)), (0, SHIFT))
    top = im.crop((0, 0, 1080, SHIFT))  # 上の暗い水面を反転して延ばす
    out.paste(ImageOps.flip(top), (0, 0))
    out.save(R / 'assets' / 'heat' / f'bg_{k}.png')
print('ok')
