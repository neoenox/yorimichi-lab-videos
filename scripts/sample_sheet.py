"""変換した動画の見本：各 slug の 4か所の静止画を、1枚の一覧にする。usage: python scripts/sample_sheet.py out.png slug1 slug2 ..."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image
R = Path(__file__).resolve().parents[1]
out = sys.argv[1]; slugs = sys.argv[2:]
W, H = 400, 225
sheet = Image.new('RGB', (W * 4, H * len(slugs)))
for r, s in enumerate(slugs):
    tl = json.loads((R / 'data' / f'{s}_timeline.json').read_text(encoding='utf8'))
    total = tl[-1]['end']
    ts = [int(total * f) for f in (0.12, 0.35, 0.6, 0.85)]
    subprocess.run([sys.executable, str(R / 'scripts' / 'vp.py'), s, 'still', *map(str, ts)], cwd=R, capture_output=True)
    for c, t in enumerate(ts):
        p = R / 'out' / f'{s}_review' / f'still_{t}.png'
        if p.exists(): sheet.paste(Image.open(p).convert('RGB').resize((W, H)), (c * W, r * H))
sheet.save(out); print('saved', out)
