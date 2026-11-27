"""builder9(task-19): 夕焼けShort v9 を描画する。

v8 の描画設定（話速0.95・end_text_plain・overlay の2枚・登録誘導カード削除）を維持し、
slug だけ solo_sunset_v9 に変える。共通パッケージ E:\\yt-shorts-kit\\ytcore\\make_short2.py は
書き換えず、inspect.getsource → exec でこの process 内だけ次を差し替える。

  1. draw_scene(): 採用したAI生成プレゼン画像2枚を cover で貼る。
  2. draw_scene(): nolong 末尾の「チャンネル登録」カード行を pass に置き換える。

BGM は spec の曲名からファイルを選ぶ。ytcore/make_short.py の mix() は channel.toml の
[bgm] file（既定 piano12）を使うため、この process 内だけ BGM['file'] と BGM['credit'] を
差し替える（channel.toml 自体は変更しない）。音量0.30・afade・サイドチェーン圧縮・
loudnorm I=-14/TP=-1.5/LRA=7 は ytcore の既定をそのまま使う。

既存の out/short_solo_sunset*.mp4 は上書きしない。
"""
import inspect
import json
import os
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
os.environ.setdefault('YT_PROJECT_ROOT', str(R))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import procedure_gate
procedure_gate.require()

import ytcore.make_short as base
base.SPEED = 0.95
import ytcore.make_short2 as ms2

SLUG = 'solo_sunset_v9'
BGM_NAMES = {'piano': 'ピアノ', 'acoustic': 'アコースティック', 'ethnic': '民族', 'orchestra': 'オーケストラ'}


def paste_overlay(im, sc, a):
    """sc['overlay'] の画像を 1080x1920 へ cover で貼る。端は中央から切る。"""
    rel = sc.get('overlay')
    if not rel:
        return
    p = ms2.ROOT / rel
    if not p.is_file():
        raise SystemExit(f'overlay 画像が見つかりません: {p}')
    src = Image.open(p).convert('RGBA')
    iw, ih = src.size
    sw, sh = im.size
    scale = max(sw / iw, sh / ih)          # cover（768x1376 → 上下15pxだけ切る）
    nw, nh = max(sw, round(iw * scale)), max(sh, round(ih * scale))
    if (nw, nh) != (iw, ih):
        src = src.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - sw) // 2, (nh - sh) // 2
    src = src.crop((left, top, left + sw, top + sh))
    alpha = int(255 * a)
    if alpha < 255:
        src = src.copy()
        src.putalpha(src.getchannel('A').point(lambda v: v * alpha // 255))
    im.paste(src, (0, 0), src)


import PIL.Image as _PILImage
Image = _PILImage


def patch_draw_scene():
    """この process 内だけで draw_scene を差し替える（共通ファイルは変更しない）。"""
    src = inspect.getsource(ms2.draw_scene)
    cta = "d.text((540, top + 165), 'チャンネル登録', font=font(92, True), fill=GOLD + (A,), anchor='mm')"
    if src.count(cta) != 1:
        raise SystemExit(f'想定した登録カード行が見つかりません (count={src.count(cta)})')
    lines = src.splitlines(keepends=True)
    defline = next(i for i, ln in enumerate(lines) if ln.startswith('def draw_scene('))
    patched = ''.join(lines[:defline + 1] + ['    _paste_overlay(im, sc, a)\n'] + lines[defline + 1:])
    patched = patched.replace(cta, 'pass  # builder9(v9): nolong 末尾の登録誘導カードを削除')

    ns = dict(ms2.__dict__)
    ns['_paste_overlay'] = paste_overlay
    ns['Image'] = Image
    exec(compile(patched, '<builder9(v9)_draw_scene>', 'exec'), ns)
    ms2.draw_scene = ns['draw_scene']


def apply_bgm(spec):
    """spec の曲名を mix() が読む BGM 設定へ、この process 内だけ反映する。"""
    name = spec.get('bgm')
    if not name or name == 'none':
        raise SystemExit('v9 では BGM 曲名が必要です')
    f = ms2.ROOT / 'assets' / 'bgm_maou' / f'maou_bgm_{name}.mp3'
    if not f.is_file():
        raise SystemExit(f'BGM が見つかりません: {f}')
    base.BGM['file'] = f.relative_to(ms2.ROOT).as_posix()
    prefix = ''.join(c for c in name if c.isalpha())
    jp = BGM_NAMES.get(prefix)
    num = name[len(prefix):]
    if not jp or not num:
        raise SystemExit(f'BGM 曲名の形式が想定外: {name}')
    base.BGM['credit'] = (
        f'・音楽：魔王魂（https://maou.audio/）{jp}{num}'
        '（作曲：森田交一。音量調整を行っています）'
    )
    print(f"bgm {base.BGM['file']} / {base.BGM['credit']}")


def main_v9(slug):
    spec_path = ms2.ROOT / 'data' / f'short_{slug}.json'
    spec = json.loads(spec_path.read_text(encoding='utf8'))
    plain = spec.get('end_text_plain')
    if not plain or 'チャンネル登録' in plain or 'お願いします' in plain:
        raise SystemExit('end_text_plain が無い、または登録誘導が残っています')
    if spec.get('hook_card') is not False:
        raise SystemExit('hook_card=false が維持されていません')
    for sc in spec['scenes']:
        if sc.get('sub') or sc.get('src'):
            raise SystemExit('v5 以降では sub/src を空にする必要があります')
        if sc.get('viz'):
            raise SystemExit('v8 では timeline viz を消す必要があります')
    overlays = [sc.get('overlay') for sc in spec['scenes']]
    if overlays != [None,
                    'assets/solo_sunset/diagram/diagram_presentation_day_v2.png',
                    'assets/solo_sunset/diagram/diagram_presentation_day_v2.png',
                    'assets/solo_sunset/diagram/diagram_presentation_day_v2.png',
                    'assets/solo_sunset/diagram/diagram_presentation_compare.png',
                    'assets/solo_sunset/diagram/diagram_presentation_compare.png',
                    None]:
        raise SystemExit('画像の重ね先が想定と違います')

    patch_draw_scene()
    apply_bgm(spec)

    work = ms2.ROOT / 'cache' / f'short_{slug}'
    work.mkdir(parents=True, exist_ok=True)
    texts = [s['text'] for s in spec['scenes']]
    texts[-1] = plain
    segs, total = ms2.synth(dict(pron=spec['pron'], scenes=[dict(text=t, kind='') for t in texts]), work)
    (ms2.ROOT / 'out' / f'short_{slug}_kana.txt').write_text(
        '\n'.join(f"{s['text']}\n    {s['kana']}" for s in segs), encoding='utf8')
    print('narration', round(total, 1), 's')
    if '--kana' in sys.argv:
        return
    raw = work / 'raw.mp4'
    ms2.render(spec, segs, total, raw, slug)
    ms2.mix(spec, work, total, raw, ms2.ROOT / 'out' / f'short_{slug}.mp4')
    spec['sec'] = round(total)
    text = ms2.description(spec)
    (ms2.ROOT / 'out' / f'short_{slug}_description.md').write_text(text, encoding='utf8')
    print('done -> out/short_%s.mp4' % slug)


if __name__ == '__main__':
    sys.argv = ['make_short2', SLUG] + sys.argv[1:]
    main_v9(sys.argv[1])
