"""国土地理院の地理院タイル(年代別の空中写真)から、「この場所は昔は〇〇だった」用の背景クリップ(7秒・縦動画・ゆっくり拡大)を作る。
  python scripts/gsi_clip.py <出力mp4> <レイヤー> <緯度> <経度> [--dx 0.0] [--dy 0.0] [--zoom 17]
    --dx/--dy : 中心を、画面の幅/高さの割合でずらす(例 --dx -0.1 で左へ)。
レイヤーと撮影期間(国土地理院の告知で確認済みのもの):
  ort            現在の写真 (jpg)           ort_USA10  1945〜50年 米軍撮影 (png)    ort_old10  1961〜64年 (png)
  gazo1 1974〜78年 / gazo2 1979〜83年 / gazo3 1984〜86年 / gazo4 1987〜90年 (jpg)
  ort_riku10  戦前の陸軍撮影(撮影年は未確認) (png)     std  現在の地図(淡色ではなく標準) (png)
  ※ 迅速測図・1928年の写真は、このタイルでは取れない(404)。
画面に出す出典は「<年代>の写真:国土地理院」(短く)。注意書きは説明欄へ。タイルは cache/gsi_tiles にためる。"""
import io, math, subprocess, sys, urllib.request
from pathlib import Path
from PIL import Image
R = Path(__file__).resolve().parents[1]
EXT = {'seamlessphoto': 'jpg', 'ort': 'jpg', 'gazo1': 'jpg', 'gazo2': 'jpg', 'gazo3': 'jpg', 'gazo4': 'jpg'}
UA = {'User-Agent': 'yorimichi-lab-research/1.0'}


def tile_xy(lat, lon, z):
    n = 2 ** z
    return (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n


def fetch(layer, z, x, y):
    ext = EXT.get(layer, 'png')
    c = R / 'cache' / 'gsi_tiles' / layer / str(z) / str(x); c.mkdir(parents=True, exist_ok=True)
    f = c / f'{y}.{ext}'
    if f.exists(): return Image.open(f).convert('RGB')
    b = urllib.request.urlopen(urllib.request.Request(f'https://cyberjapandata.gsi.go.jp/xyz/{layer}/{z}/{x}/{y}.{ext}', headers=UA), timeout=30).read()
    f.write_bytes(b); return Image.open(io.BytesIO(b)).convert('RGB')


def main():
    a = sys.argv[1:]
    out, layer, lat, lon = a[0], a[1], float(a[2]), float(a[3])
    opt = {a[i]: a[i + 1] for i in range(4, len(a) - 1, 2)}
    dx, dy, z = float(opt.get('--dx', 0)), float(opt.get('--dy', 0)), int(opt.get('--zoom', 17))
    # 縦(9:16)の窓: 高さ7タイル分を取り、中心の周りを切り出す
    cx, cy = tile_xy(lat, lon, z)
    cols, rows = 5, 7
    x0, y0 = int(cx) - cols // 2, int(cy) - rows // 2
    im = Image.new('RGB', (cols * 256, rows * 256), 'black'); ok = 0
    for i in range(cols):
        for j in range(rows):
            try: im.paste(fetch(layer, z, x0 + i, y0 + j), (i * 256, j * 256)); ok += 1
            except Exception: pass
    if ok < cols * rows * 0.6: sys.exit(f'タイルが足りない({ok}/{cols * rows})。この年代・場所は取れない可能性')
    H = rows * 256; W = int(H * 9 / 16)
    px, py = (cx - x0) * 256 + dx * W, (cy - y0) * 256 + dy * H
    left = int(min(max(px - W / 2, 0), cols * 256 - W)); tmp = R / 'cache' / 'gsi_tmp.png'; tmp.parent.mkdir(exist_ok=True)
    im.crop((left, 0, left + W, H)).save(tmp)
    vf = f"scale={W * 2}:{H * 2}:flags=lanczos,zoompan=z='1+0.18*on/168':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=168:s=544x960:fps=24,format=yuv420p"
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(tmp), '-vf', vf, '-c:v', 'libx264', '-crf', '18', '-an', out], check=True)
    print('作成:', out, f'(タイル {ok}/{cols * rows})')


if __name__ == '__main__':
    if len(sys.argv) < 5: print(__doc__)
    else: main()
