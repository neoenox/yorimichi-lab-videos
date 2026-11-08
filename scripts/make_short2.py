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


_VID = {}


def vid_frame(path, dim, fi_key, dur):
    """動画背景（AI生成クリップ）。ループも逆再生もせず、クリップ全体を場面の長さ dur 秒に合わせて再生速度を落とす（スロー）。
    動きの間は minterpolate で補間して滑らかにする。cover で 1080x1920 に切り出し、dim で暗くして、場面ごとに1フレームずつ読む。
    場面の開始から終了まで順に呼ばれる前提（render が時刻順に回すため）。"""
    key = (path, fi_key)
    if key not in _VID:
        src = ROOT / path
        L = float(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=duration', '-of', 'csv=p=0', str(src)]).decode().split()[0])
        f = max(1.0, (dur + 0.1) / L)   # 少し長めに伸ばし、最後の1フレームは tpad で保持（足りなくならないように）
        vf = (f'setpts={f:.4f}*PTS,minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1,tpad=stop_mode=clone:stop_duration=2,'
              f'scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},lutrgb=r=val*{dim}:g=val*{dim}:b=val*{dim}')
        _VID[key] = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(src), '-an', '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'], stdout=subprocess.PIPE)
    buf = _VID[key].stdout.read(W * H * 3)
    return Image.frombytes('RGB', (W, H), buf)


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
    d.text((540, 190), spec.get('head') or spec['title'], font=font(56, True), fill=WHITE + (255,), anchor='mm')
    d.line([(120, 258), (960, 258)], fill=GOLD + (255,), width=4)
    if sc.get('src_small'):
        d.text((60, 300), sc['src_small'], font=font(26), fill=DIM + (A,))
    col = COLS.get(sc.get('col', 'gold'), GOLD)
    if sc.get('end'):
        if spec.get('platform') == 'tiktok':
            draw_tiktok_end(d, spec, A)
            return
        if spec.get('nolong'):   # 本編に触れない版（2026-11-04）：本編が公開前でもリンク切れにならない。結論→出典は概要欄→登録
            y1 = panel(d, (60, 470, 1020, 470), '結論', spec.get('answer') or spec['title'], 52, hi=True, alpha=A)
            top = y1 + 50
            d.rounded_rectangle((90, top, 990, top + 330), 18, fill=(7, 24, 36, int(215 * A / 255)))
            d.text((540, top + 55), '出典は、説明欄に', font=font(46), fill=WHITE + (A,), anchor='mm')
            d.text((540, top + 165), 'チャンネル登録', font=font(92, True), fill=GOLD + (A,), anchor='mm')
            d.text((540, top + 265), '寄り道ラボ', font=font(36), fill=DIM + (A,), anchor='mm')
            return
        panel(d, (60, 480, 1020, 860), '本編の動画', spec['long_title'], 50, hi=True, alpha=A)
        d.rounded_rectangle((90, 905, 990, 1215), 18, fill=(7, 24, 36, int(215 * a)))
        if spec.get('cta', True):   # 登録の呼びかけ版（2026-10-26から）。cta:false で従来の終わり方
            d.text((540, 955), '続きは、本編の動画で', font=font(48), fill=WHITE + (A,), anchor='mm')
            d.text((540, 1060), 'チャンネル登録', font=font(96, True), fill=GOLD + (A,), anchor='mm')
            d.text((540, 1150), '寄り道ラボ', font=font(38), fill=DIM + (A,), anchor='mm')
        else:
            d.text((540, 960), '概要欄のリンクから', font=font(52), fill=WHITE + (A,), anchor='mm')
            d.text((540, 1090), '寄り道ラボ', font=font(84, True), fill=GOLD + (A,), anchor='mm')
            d.text((540, 1170), 'ふと気になったことを、資料で調べる', font=font(36), fill=DIM + (A,), anchor='mm')
        return
    if sc.get('big'):
        y = sc.get('big_y', 430 if sc.get('viz') else 520)
        sz = 92
        big = display(sc['big'])
        while sz > 60 and d.textlength(big, font=font(sz, True)) > 840 and d.textlength(big, font=font(sz, True)) < 1300:
            sz -= 4   # 1行に収まる範囲なら縮めて語の途中で折り返さない
        for ln in wrap(d, big, font(sz, True), 840):
            d.text((540, y), ln, font=font(sz, True), fill=col + (A,), anchor='mm', stroke_width=5, stroke_fill=(5, 14, 24, A)); y += int(sz * 1.3)
    if sc.get('sub') and not sc.get('viz'):
        panel(d, (60, 800, 960, 960), sc.get('src'), display(sc['sub']), 44, alpha=A)



def _ease(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


RED = (232, 86, 74)


def draw_viz(im, sc, A, tt):
    """場面に重ねる、動く自作の図（2026-11-05）。viz: {type: timeline|bars|flow|count|compare, ...}。tt=場面開始からの秒。"""
    v = sc.get('viz')
    if not v:
        return
    d = ImageDraw.Draw(im, 'RGBA')
    typ = v['type']
    def box(xy, fill=(7, 24, 36, 215), outline=None, w=3, a=1.0):
        d.rounded_rectangle(xy, 18, fill=(fill[0], fill[1], fill[2], int(fill[3] * a * A / 255)),
                            outline=(outline + (int(255 * a * A / 255),)) if outline else None, width=w)
    if typ == 'timeline':
        ev = v['events']; n = len(ev); y0 = 640; step = min(200, 560 // max(1, n))
        d.line([(150, y0), (150, y0 + step * (n - 1) + 10)], fill=GOLD + (int(120 * A / 255),), width=6)
        for i, (dt, tx) in enumerate(ev):
            a = _ease((tt - 0.4 - i * float(v.get('gap', 1.6))) / 0.5)
            if a <= 0:
                continue
            y = y0 + i * step
            d.ellipse((132, y - 18, 168, y + 18), fill=(RED if v.get('red') == i else GOLD) + (int(255 * a * A / 255),))
            box((200 + int((1 - a) * 60), y - 62, 1010, y + 62), a=a, outline=GOLD)
            d.text((226 + int((1 - a) * 60), y - 30), dt, font=font(34, True), fill=GOLD + (int(255 * a * A / 255),), anchor='lm')
            d.text((226 + int((1 - a) * 60), y + 20), tx, font=font(42, True), fill=WHITE + (int(255 * a * A / 255),), anchor='lm')
    elif typ == 'bars':
        it = v['items']; y = 660; mx = max(i['value'] for i in it); stp = v.get('step', 250)
        for i, b in enumerate(it):
            a = _ease((tt - 0.3 - i * 1.4) / 0.9)
            if a <= 0:
                y += stp; continue
            d.text((90, y), b['label'], font=font(38, True), fill=GOLD + (int(255 * A / 255),), anchor='lm')
            d.rounded_rectangle((90, y + 40, 990, y + 130), 14, fill=(7, 24, 36, int(200 * A / 255)))
            wbar = max(40, int(900 * b['value'] / mx * a))
            d.rounded_rectangle((90, y + 40, 90 + wbar, y + 130), 14, fill=tuple(b.get('color', GOLD)) + (int(255 * A / 255),))
            d.text((90 + min(wbar, 900) - 16 if wbar > 360 else 90 + wbar + 16, y + 85), b['text'], font=font(46, True),
                   fill=(WHITE if wbar > 360 else WHITE) + (int(255 * A / 255),), anchor='rm' if wbar > 360 else 'lm')
            if b.get('note'):
                d.text((90, y + 160), b['note'], font=font(32), fill=DIM + (int(255 * a * A / 255),), anchor='lm')
            y += stp
    elif typ == 'flow':
        hub = v['hub']; mids = v['mid']; hot = _ease((tt - 0.3) / 0.6)
        box((270, 640, 810, 770), outline=RED, a=hot or 0.0)
        box((270, 640, 810, 770), outline=GOLD, a=1 - hot)
        d.text((540, 705), hub, font=font(44, True), fill=WHITE + (A,), anchor='mm')
        xs = [180, 540, 900]
        for i, m in enumerate(mids[:3]):
            a = _ease((tt - 1.2 - i * 0.7) / 0.5)
            if a <= 0:
                continue
            x = xs[i]
            d.line([(540, 770), (x, 930)], fill=RED + (int(255 * a * A / 255),), width=6)
            box((x - 150, 930, x + 150, 1070), outline=RED, a=a)
            for k, ln in enumerate(m.split('|')):
                d.text((x, 975 + k * 52), ln, font=font(36, True), fill=WHITE + (int(255 * a * A / 255),), anchor='mm')
        a = _ease((tt - 3.2) / 0.6)
        if a > 0:
            box((60, 1100, 1020, 1170), fill=(120, 30, 26, 235), outline=RED, a=a)
            d.text((540, 1135), v['leaf'], font=font(38, True), fill=WHITE + (int(255 * a * A / 255),), anchor='mm')
    elif typ == 'count':
        p = _ease(tt / 1.4)
        box((80, 660, 1000, 1080))
        d.text((540, 730), v['label'], font=font(42, True), fill=GOLD + (A,), anchor='mm')
        d.text((540, 890), v.get('fmt', '{:,.0f}').format(v['value'] * p) + v.get('unit', ''), font=font(190, True), fill=WHITE + (A,), anchor='mm')
        if v.get('note'):
            d.text((540, 1020), v['note'], font=font(34), fill=DIM + (A,), anchor='mm')
    elif typ == 'compare':
        a2 = _ease((tt - 0.8) / 0.6)
        box((70, 660, 500, 1020), outline=GOLD)
        d.text((285, 730), v['l_label'], font=font(36, True), fill=GOLD + (A,), anchor='mm')
        def fitf(txt, base=130, maxw=380):   # 枠(幅430)に収まるまで文字を小さくする（「1080円」など長い値が枠をはみ出さないように）
            sz = base
            while sz > 60 and d.textlength(txt, font=font(sz, True)) > maxw:
                sz -= 6
            return font(sz, True)
        d.text((285, 870), v['l_val'], font=fitf(v['l_val']), fill=WHITE + (A,), anchor='mm')
        d.text((540, 840), '→', font=font(70, True), fill=GOLD + (int(255 * a2 * A / 255),), anchor='mm')
        box((580, 660, 1010, 1020), outline=RED, a=a2)
        d.text((795, 730), v['r_label'], font=font(36, True), fill=GOLD + (int(255 * a2 * A / 255),), anchor='mm')
        d.text((795, 870), v['r_val'], font=fitf(v['r_val']), fill=WHITE + (int(255 * a2 * A / 255),), anchor='mm')
    if sc.get('src') or sc.get('sub'):
        cap = ' / '.join(x for x in [display(sc.get('sub', '')) if sc.get('sub') else '', sc.get('src', '')] if x)
        cs = 36   # 出典の行：明るい背景でも読めるよう、暗い帯の上に白字。幅に収まるまで縮める
        while cs > 26 and d.textlength(cap, font=font(cs)) > 940: cs -= 2
        cw = d.textlength(cap, font=font(cs)) / 2 + 24
        d.rounded_rectangle((540 - cw, 1200 - cs * 0.8, 540 + cw, 1200 + cs * 0.8), 12, fill=(5, 14, 24, int(170 * A / 255)))
        d.text((540, 1200), cap, font=font(cs), fill=(235, 238, 242, A), anchor='mm')


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
    fs = 84
    lns = wrap(d, display(ans), font(fs, True), 820)
    while len(lns) > 2 and fs > 56:   # 長い結論は、箱に収まるまで字を小さくする(2行まで)
        fs -= 4; lns = wrap(d, display(ans), font(fs, True), 820)
    h = 340 if len(lns) == 1 else 430
    d.rounded_rectangle((60, 470, 1020, 470 + h), 20, fill=(7, 24, 36, int(255 * a)),
                        outline=GOLD + (A,), width=4)
    d.text((540, 545), '結論', font=font(44, True), fill=GOLD + (A,), anchor='mm')
    y = 650 if len(lns) == 1 else 618
    for ln in lns:
        d.text((540, y), ln, font=font(fs, True), fill=WHITE + (A,), anchor='mm')
        y += 108


def sub_clean(c):
    """字幕から句読点を除く(読点は、ナレーションの間のために多めに打つので、画面では邪魔)。文末の。、は消し、途中の、。は改行にする(空白にはしない)。"""
    import re
    c = re.sub(r'[、。]+$', '', c)
    return re.sub(r'[、。]+', '\n', c).strip()


def render(spec, segs, total, out_mp4, slug):
    n = round(total * FPS)
    cks = []
    for s in segs:
        cs = chunks(display(s['text'])); ws = [len(c) for c in cs]; tot = sum(ws); t0 = s['start']; dur = s['end'] - s['start']
        for c, w in zip(cs, ws):
            cks.append((t0, t0 + dur * w / tot, sub_clean(c))); t0 += dur * w / tot
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
        if sc.get('vid'):   # AI生成の動画背景（場面ごと）。無ければ従来の静止画
            im = vid_frame(sc['vid'], sc.get('dim', 0.55), seg['i'], seg['end'] - seg['start'] + 0.55).convert('RGBA')
        else:
            im = bg(sc.get('art') or spec['art'], ratio, sc.get('dim', 0.55), spec.get('bg_fit', 1.12)).convert('RGBA')
        hook_on = bool(spec.get('hook_card', True) and spec.get('answer') and t < 2.25)
        if hook_on:   # 結論カードの間は、後ろの見出し・図を出さない(重なり防止)。カードが消えてから出す
            a = max(0.0, min(1.0, (t - 1.9) / 0.35))
        if hook_on:   # PILは透明度0でも文字を描いてしまうので、見出し・図そのものを描かない(ヘッダーだけ)
            draw_scene(im, {k: v for k, v in sc.items() if k not in ('big', 'sub', 'viz', 'src')}, spec, 1.0)
        else:
            draw_scene(im, sc, spec, a)
            draw_viz(im, sc, int(255 * a), max(0.0, t - seg['start']))
        if spec.get('hook_card', True):
            draw_hook(im, spec, t)
        ck = next((c for c in cks if c[0] <= t < c[1]), None)
        if ck and not (spec.get('hook_card', True) and spec.get('answer') and t < 1.75):   # 結論カードと字幕が同じことを二重に言わないようにする
            d = ImageDraw.Draw(im, 'RGBA')
            fs = 60
            lns = [w for part in ck[2].split('\n') for w in wrap(d, part, font(fs), 880)]
            while len(lns) * int(fs * 1.4) + 46 > 300 and fs > 40:   # 字幕の枠を y=1240 より下に収め、出典の帯(y=1200±29)に被らないようにする
                fs -= 4; lns = [w for part in ck[2].split('\n') for w in wrap(d, part, font(fs), 880)]
            lh = int(fs * 1.4)
            nh = len(lns) * lh
            h = nh + 46
            y0 = 1540 - h
            d.rounded_rectangle((50, y0, 960, 1540), 16, fill=(7, 24, 36, 225))
            y = y0 + (h - nh) // 2 + lh // 2
            for ln in lns:
                rich.draw_center(d, 505, y - lh // 2, ln, font(fs), (255, 252, 239, 255), (255, 208, 122)); y += lh
        proc.stdin.write(im.convert('RGB').tobytes())
    proc.stdin.close(); proc.wait()


def description(spec):
    # 概要欄も画面と同じ規則で算用数字にそろえる（展示用の表記）
    # long_id（対応する長尺動画）が無い単独Shortsでは、その案内行を出さない
    link = ''
    if spec.get('nolink'):
        link = ''   # 時事ネタなど、本編が存在しない単独Short
    elif spec.get('nolong'):
        link = '▶ このテーマの本編動画は、チャンネルで順に公開しています。\n\n'
    elif spec.get('long_id'):
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
    elif spec.get('nolong'):
        texts[-1] = '出典は、説明欄にまとめています。チャンネル登録も、お願いします。'
    elif spec.get('cta', True) and not is_tt:   # 最後の場面の読み上げに、登録の呼びかけを足す
        texts[-1] = texts[-1] + '続きが気になったら、チャンネル登録も、お願いします。'
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
