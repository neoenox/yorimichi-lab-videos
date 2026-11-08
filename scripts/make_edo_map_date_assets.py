"""edo_map_date の背景を作る。実資料（NDL・PDM）を使い、シーンごとに見せ場を変える。

原本: 国立国会図書館デジタルコレクション「武州豊嶋郡江戸〔庄〕図」（PID 1286168, PDM）
      assets/edo_map_date/src_map.jpg に IIIF 画像を取得済み（git 管理外）

usage: python scripts/make_edo_map_date_assets.py
出力: assets/edo_map_date/bg_{full,text,names,title}.png（1080x1920）
      資料であることを画面に明記し、原図の一部を暗く加工した旨も書く。
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'assets' / 'edo_map_date' / 'src_map.jpg'
OUT = ROOT / 'assets' / 'edo_map_date'
W, H = 1080, 1920
FONT = 'C:/Windows/Fonts/NotoSansJP-VF.ttf'
GOLD = (239, 201, 118)
DIM = (190, 205, 208)

# 原図のどこを見せるか（元画像の比率で指定）。デジタル化の色票・物差しは除く。
CROPS = {
    'full': (0.070, 0.082, 0.978, 0.872),   # 全体
    'text': (0.058, 0.585, 0.372, 0.870),   # 左下の詞書（文字ブロック）
    'names': (0.415, 0.300, 0.720, 0.610),  # 短冊状の屋敷名が並ぶ領域
    'wide': (0.115, 0.120, 0.940, 0.815),  # やや引き（全体より少し寄る）
}
LABEL = {
    'full': '原図（全体）',
    'text': '部分拡大：詞書',
    'names': '部分拡大：屋敷名',
    'wide': 'やや引き',
}
# 横長の帯は全体を見せる（cover だと中央だけを拡大してしまう）
CONTAIN = set()


def font(size, weight=500):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def backdrop():
    im = Image.new('RGB', (W, H), (7, 24, 36))
    d = ImageDraw.Draw(im, 'RGBA')
    for y in range(H):
        k = y / H
        d.line([(0, y), (W, y)], fill=(int(7 + 9 * (1 - k)), int(24 + 13 * (1 - k)), int(36 + 18 * (1 - k))))
    return im


def place_map(im, src, box, contain=False):
    """原図を box に入れる。contain=True は横幅に合わせて全体を見せ、上下を余白にする。"""
    panel = im.crop(box)
    bw, bh = box[2] - box[0], box[3] - box[1]
    if contain:
        s = bw / src.width
        r = src.resize((bw, max(1, round(src.height * s))), Image.LANCZOS)
        panel.paste(r, (0, (bh - r.height) // 2))
        return panel
    s = max(bw / src.width, bh / src.height)
    r = src.resize((max(1, round(src.width * s)), max(1, round(src.height * s))), Image.LANCZOS)
    x = (r.width - bw) // 2
    y = (r.height - bh) // 2
    panel.paste(r.crop((x, y, x + bw, y + bh)), (0, 0))
    return panel


def build(key, src):
    im = backdrop().convert('RGB')
    d = ImageDraw.Draw(im, 'RGBA')

    # 見出し（資料であること・部分拡大の別）
    suffix = '' if key == 'full' else '／部分拡大：%s' % LABEL[key].replace('部分拡大：', '')
    d.text((W // 2, 452), '資料：国立国会図書館デジタルコレクション（PDM）' + suffix,
           font=font(25, 500), fill=DIM + (225,), anchor='mm')

    box = (52, 500, W - 52, 1470)
    x0, y0, x1, y1 = CROPS[key]
    crop = src.crop((int(src.width * x0), int(src.height * y0),
                     int(src.width * x1), int(src.height * y1)))
    panel = place_map(im, crop, box, contain=(key in CONTAIN))
    # 文字が乗るので少し沈める（原図の色は残す）
    panel = ImageEnhance.Brightness(panel).enhance(0.74)
    im.paste(panel, (box[0], box[1]))
    d.rectangle(box, outline=GOLD + (150,), width=4)

    # 加工の明示（下端。字幕パネルより下に置く）
    d.text((W // 2, 1556), '原図の一部を暗く加工しています。史実の再現図ではありません。',
           font=font(25, 500), fill=DIM + (200,), anchor='mm')
    d.text((W // 2, 1608), '出典：https://dl.ndl.go.jp/pid/1286168（PDM）',
           font=font(23, 500), fill=DIM + (170,), anchor='mm')

    path = OUT / f'bg_{key}.png'
    im.save(path, optimize=True)
    print('wrote', path.name, path.stat().st_size, 'bytes')


def ensure_src():
    """原本が無ければ NDL の IIIF から取得する（PDM）。"""
    if SRC.exists():
        return
    import requests
    url = 'https://dl.ndl.go.jp/api/iiif/1286168/R0000001/full/1600,/0/default.jpg'
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    SRC.parent.mkdir(parents=True, exist_ok=True)
    SRC.write_bytes(r.content)
    print('downloaded', SRC, SRC.stat().st_size, 'bytes')


def main():
    ensure_src()
    src = Image.open(SRC).convert('RGB')
    print('src', src.size)
    for key in CROPS:
        build(key, src)


if __name__ == '__main__':
    main()
