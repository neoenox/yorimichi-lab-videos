"""Short の冒頭だけを、音声合成も全編レンダもせずに描いて、スマホ縦画面の大きさで確認する。
usage: python scripts/first_frame_preview.py <slug> [秒 ...]    # 既定: 0.3 1.0 1.8 3.0
spec: data/short_<slug>.json（make_short2 と同じ）。背景(art、または動画背景 vid のクリップ)が先に出来ていること。
動画背景の場面は、クリップの先頭コマ(静止画)で代える(本番の動きや補間は見ない)。
出力: out/short_<slug>_first/first_sheet.png（360x640 に縮小して横に並べたもの）と first_<秒>.png（実寸）。
場面の長さは音声が無いので 1 文字 0.18 秒で概算する（本番の時刻とは少しずれる）。
見るもの: ①0.5秒で何の話か分かるか ②文字が端で切れていないか ③字幕帯・結論カードが重ならないか。"""
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_short2 as M2
from make_short import ROOT

PHONE = (360, 640)
CPS_EST = 0.18   # 秒/文字
LEAD = 0.1


def estimated_segs(spec):
    texts = [s['text'] for s in spec['scenes']]
    segs, t = [], LEAD
    for i, tx in enumerate(texts):
        d = max(1.5, len(tx) * CPS_EST)
        segs.append({'i': i, 'text': tx, 'start': t, 'end': t + d})
        t += d + 0.25
    return segs


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    slug = sys.argv[1]
    times = [float(x) for x in sys.argv[2:]] or [0.3, 1.0, 1.8, 3.0]
    p = ROOT / 'data' / f'short_{slug}.json'
    if not p.exists():
        print(f'spec が無い: {p}')
        return 1
    spec = json.loads(p.read_text(encoding='utf8'))
    segs = estimated_segs(spec)
    cks = M2.subtitle_chunks(segs)
    out = ROOT / 'out' / f'short_{slug}_first'
    out.mkdir(parents=True, exist_ok=True)
    pw, ph = PHONE
    sheet = Image.new('RGB', (pw * len(times), ph + 24), 'black')
    d = ImageDraw.Draw(sheet)
    for k, t in enumerate(times):
        try:
            # preview=True: 動画背景(vid)は先頭コマの静止画で代える(本番の vid_frame は時刻順にしか読めないため)
            im = M2.frame_at(spec, segs, cks, t, preview=True).convert('RGB')
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print(f'背景が無い・読めない（先に生成する）: {e}')
            return 1
        im.save(out / f'first_{t:g}.png')
        sheet.paste(im.resize(PHONE, Image.LANCZOS), (k * pw, 24))
        d.text((k * pw + 6, 6), f'{t:g}s', fill='yellow')
    sp = out / 'first_sheet.png'
    sheet.save(sp)
    print('written', sp.relative_to(ROOT).as_posix())
    return 0


if __name__ == '__main__':
    sys.exit(main())
