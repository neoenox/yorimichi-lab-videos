"""汎用の縦型Short（1080x1920）。長尺のイラストを背景に、見出し→要点→最後に本動画への誘導。
usage: python scripts/make_short2.py <slug>     # data/short_<slug>.json から out/short_<slug>.mp4, _subtitles.srt, _description.md
spec: title, long_id, long_title, pron(JSON), hook, notes, art, scenes[{text,big,sub,src,art,col}]。最後の場面は end:true（本動画のタイトルと誘導を出す）。
ナレーションの数字・限定は長尺の台本（docs/themes/*/09_script_v2.md）と一致させる。VOICEVOXが 127.0.0.1:50021 で動いていること。"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_short as M
from make_short import ROOT, W, H, FPS, GOLD, WHITE, DIM, font, wrap, panel, synth, display, chunks, mix
import rich_text as rich

COLS = M.COL
_BG = {}


def bg(path, zoom, dim=0.55, fit=1.12):
    """アートを 1080x1920 に cover で切り出し、暗くして、ゆっくり拡大（Ken Burns）。
    dim は場面ごとの明るさ、fit は余白の取り方（1.0で9:16の画像を切らない）。"""
    key = (path, round(dim, 2), fit)
    if key not in _BG:
        im = Image.open(ROOT / path).convert('RGB')
        s = H * fit / im.height
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        _BG[key] = ImageEnhance.Brightness(im).enhance(dim)
    im = _BG[key]
    z = 1 + 0.06 * zoom
    cw, ch = W / z, H / z
    cx, cy = im.width / 2, im.height / 2
    return im.crop((round(cx - cw / 2), round(cy - ch / 2), round(cx + cw / 2), round(cy + ch / 2))).resize((W, H), Image.BILINEAR)


def draw_tiktok_end(d, spec, A):
    """TikTok用の最終画面。結論をくり返し、出典の場所とチャンネル名だけを出す（外部誘導なし）。"""
    y1 = panel(d, (60, 470, 1020, 470), '結論', spec.get('answer') or spec['title'], 52, hi=True, alpha=A)
    top = y1 + 60
    d.rounded_rectangle((90, top, 990, top + 300), 18, fill=(7, 24, 36, int(215 * A / 255)))
    d.text((540, top + 55), '出典は、コメントに', font=font(46), fill=WHITE + (A,), anchor='mm')
    d.text((540, top + 155), '寄り道ラボ', font=font(76, True), fill=GOLD + (A,), anchor='mm')
    d.text((540, top + 235), '地図と史料で、通説を確かめる', font=font(32), fill=DIM + (A,), anchor='mm')


def draw_scene(im, sc, spec, a):
    d = ImageDraw.Draw(im, 'RGBA'); A = int(255 * a)
    d.rectangle((0, 0, W, 330), fill=(5, 14, 24, 150))
    d.text((540, 190), spec['title'], font=font(56, True), fill=WHITE + (255,), anchor='mm')
    d.line([(120, 258), (960, 258)], fill=GOLD + (255,), width=4)
    if sc.get('src_small'):
        d.text((60, 300), sc['src_small'], font=font(26), fill=DIM + (A,))
    col = COLS.get(sc.get('col', 'gold'), GOLD)
    if sc.get('end'):
        if spec.get('platform') == 'tiktok':
            draw_tiktok_end(d, spec, A)
            return
        panel(d, (60, 480, 1020, 860), '本編の動画', spec['long_title'], 50, hi=True, alpha=A)
        d.rounded_rectangle((90, 905, 990, 1215), 18, fill=(7, 24, 36, int(215 * a)))
        if spec.get('cta', True):   # 登録の呼びかけ版（2026-10-26から）。cta:false で従来の終わり方
            d.text((540, 955), '続きは、本編の動画で', font=font(48), fill=WHITE + (A,), anchor='mm')
            d.text((540, 1060), 'チャンネル登録', font=font(96, True), fill=GOLD + (A,), anchor='mm')
            d.text((540, 1150), '寄り道ラボ　資料で確かめます', font=font(38), fill=DIM + (A,), anchor='mm')
        else:
            d.text((540, 960), '概要欄のリンクから', font=font(52), fill=WHITE + (A,), anchor='mm')
            d.text((540, 1090), '寄り道ラボ', font=font(84, True), fill=GOLD + (A,), anchor='mm')
            d.text((540, 1170), 'ふと気になったことを、資料で調べる', font=font(36), fill=DIM + (A,), anchor='mm')
        return
    if sc.get('big'):
        y = sc.get('big_y', 520)
        sz = 92
        big = display(sc['big'])
        while sz > 60 and d.textlength(big, font=font(sz, True)) > 840 and d.textlength(big, font=font(sz, True)) < 1300:
            sz -= 4   # 1行に収まる範囲なら縮めて語の途中で折り返さない
        for ln in wrap(d, big, font(sz, True), 840):
            d.text((540, y), ln, font=font(sz, True), fill=col + (A,), anchor='mm', stroke_width=5, stroke_fill=(5, 14, 24, A)); y += int(sz * 1.3)
    if sc.get('sub'):
        panel(d, (60, 800, 960, 960), sc.get('src'), display(sc['sub']), 44, alpha=A)



def draw_hook(im, spec, t):
    """冒頭1.6秒に「結論」を1枚だけ出す。答えを先に見せて、離脱を減らす。"""
    ans = spec.get('answer')
    if not ans or t > 1.9:
        return
    a = min(1.0, t / 0.18)
    if t > 1.55:
        a = min(a, max(0.0, (1.9 - t) / 0.35))
    A = int(255 * a)
    d = ImageDraw.Draw(im, 'RGBA')
    lns = wrap(d, display(ans), font(84, True), 820)
    h = 340 if len(lns) == 1 else 430
    d.rounded_rectangle((60, 470, 1020, 470 + h), 20, fill=(7, 24, 36, int(232 * a)),
                        outline=GOLD + (A,), width=4)
    d.text((540, 545), '結論', font=font(44, True), fill=GOLD + (A,), anchor='mm')
    y = 650 if len(lns) == 1 else 618
    for ln in lns:
        d.text((540, y), ln, font=font(84, True), fill=WHITE + (A,), anchor='mm')
        y += 108


def render(spec, segs, total, out_mp4, slug):
    n = round(total * FPS)
    cks = []
    for s in segs:
        cs = chunks(display(s['text'])); ws = [len(c) for c in cs]; tot = sum(ws); t0 = s['start']; dur = s['end'] - s['start']
        for c, w in zip(cs, ws):
            cks.append((t0, t0 + dur * w / tot, c)); t0 += dur * w / tot
    st = lambda t: (lambda ms: f'{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}')(round(t * 1000))
    (ROOT / 'out' / f'short_{slug}_subtitles.srt').write_text('\n\n'.join(f'{i + 1}\n{st(a)} --> {st(b)}\n{c}' for i, (a, b, c) in enumerate(cks)) + '\n', encoding='utf8')
    proc = subprocess.Popen(['ffmpeg', '-y', '-v', 'warning', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0',
                             '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', str(out_mp4)], stdin=subprocess.PIPE)
    for fi in range(n):
        t = fi / FPS
        seg = next((s for s in segs if s['start'] - 0.2 <= t < s['end'] + 0.35), segs[-1] if t >= segs[-1]['end'] else segs[0])
        sc = spec['scenes'][seg['i']]
        k = t - (seg['start'] - 0.2); a = min(1.0, max(0.0, k / 0.35))
        ratio = min(1.0, k / max(1.0, seg['end'] - seg['start']))
        im = bg(sc.get('art') or spec['art'], ratio, sc.get('dim', 0.55), spec.get('bg_fit', 1.12)).convert('RGBA')
        draw_scene(im, sc, spec, a)
        if spec.get('hook_card', True):
            draw_hook(im, spec, t)
        ck = next((c for c in cks if c[0] <= t < c[1]), None)
        if ck and not (spec.get('hook_card', True) and spec.get('answer') and t < 1.75):   # 結論カードと字幕が同じことを二重に言わないようにする
            d = ImageDraw.Draw(im, 'RGBA')
            lns = wrap(d, ck[2], font(60), 880)
            nh = len(lns) * 84
            h = nh + 46
            y0 = 1540 - h
            d.rounded_rectangle((50, y0, 960, 1540), 16, fill=(7, 24, 36, 225))
            y = y0 + (h - nh) // 2 + 42
            for ln in lns:
                rich.draw_center(d, 505, y - 42, ln, font(60), (255, 252, 239, 255), (255, 208, 122)); y += 84
        proc.stdin.write(im.convert('RGB').tobytes())
    proc.stdin.close(); proc.wait()


def description(spec):
    # 概要欄も画面と同じ規則で算用数字にそろえる（展示用の表記）
    # long_id（対応する長尺動画）が無い単独Shortsでは、その案内行を出さない
    link = ''
    if spec.get('long_id'):
        link = f"▶ 詳しい根拠は、長い動画で：https://youtu.be/{spec['long_id']}\n　{spec.get('long_title', '')}\n\n"
    return display(f"""{spec['title']}　（約{spec.get('sec', 45)}秒）

{spec['hook']}

{link}{spec['notes']}

■ 出典・クレジット
{spec.get('credit') or '・イラスト：ChatGPT(OpenAI)による生成イラスト（イメージです。実在の資料の複製ではありません）'}
・音声：VOICEVOX:四国めたん
・音楽：魔王魂（https://maou.audio/）ピアノ12（作曲：森田交一。音量調整を行っています）

■ このチャンネルについて
寄り道ラボは、ふと気になったことを、資料やデータで調べる解説チャンネルです。

#Shorts #雑学
""")


def tiktok_caption(spec):
    """TikTok用のキャプション。外部リンクを置かず、確かめたこと・出典・クレジットを残す。"""
    refs = spec.get('refs') or []
    ref_block = ('■ 参考\n' + '\n'.join(f'・{r}' for r in refs) + '\n\n') if refs else ''
    return f"""{spec['title']}

{spec['hook']}

{spec.get('notes', '')}

{ref_block}■ クレジット
{spec.get('credit') or '・イラスト：ChatGPT(OpenAI)による生成イラスト（イメージです。実在の資料の複製ではありません）'}
・音声：VOICEVOX:四国めたん

{spec.get('hashtags') or '#歴史 #雑学'}
"""


def main():
    slug = sys.argv[1]
    spec = json.loads((ROOT / 'data' / f'short_{slug}.json').read_text(encoding='utf8'))
    work = ROOT / 'cache' / f'short_{slug}'; work.mkdir(parents=True, exist_ok=True)
    texts = [s['text'] for s in spec['scenes']]
    is_tt = spec.get('platform') == 'tiktok'
    if is_tt and spec.get('end_text'):
        texts[-1] = spec['end_text']
    elif spec.get('cta', True) and not is_tt:   # 最後の場面の読み上げに、登録の呼びかけを足す
        texts[-1] = texts[-1] + '資料で確かめています。続きが気になったら、チャンネル登録を。'
    segs, total = synth(dict(pron=spec['pron'], scenes=[dict(text=t, kind='') for t in texts]), work)
    (ROOT / 'out' / f'short_{slug}_kana.txt').write_text('\n'.join(f"{s['text']}\n    {s['kana']}" for s in segs), encoding='utf8')
    print('narration', round(total, 1), 's')
    raw = work / 'raw.mp4'; render(spec, segs, total, raw, slug)
    mix(spec, work, total, raw, ROOT / 'out' / f'short_{slug}.mp4')
    spec['sec'] = round(total)
    text = tiktok_caption(spec) if is_tt else description(spec)
    (ROOT / 'out' / f'short_{slug}_description.md').write_text(text, encoding='utf8')
    print('done -> out/short_%s.mp4' % slug)


if __name__ == '__main__':
    main()
