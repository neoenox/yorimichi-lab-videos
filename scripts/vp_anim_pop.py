"""「ポップ」スタイル（spec の style='pop'）。紺の背景に枠付きの文字を並べる従来の見た目をやめ、
バラエティ番組のテロップに寄せる：
  ・背景：章ごとに色が変わるグラデーション＋流れる斜めの帯。または写真いっぱいのぼかし背景（pop_bgimg）
  ・文字：太字・白抜き・黒ふち（テロップ）。強調語は黄色。ぽんっと弾んで出る（pop_telop）
  ・箇条書き：白いカードに色タグ（pop_rows）。横から弾んで入る
  ・写真・図：白縁の写真／暗いカードにのせて少し傾け、影をつける（pop_card）
  ・字幕：帯なし。太い黒ふちの白文字。数字は黄色
vp.py の _base_frame / header / _subs_layer が style を見て、このモジュールを呼ぶ。
spec の部品は t='anim', name='pop_*'。at/until は他の部品と同じ『文の番号』。"""
import math
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

G = {}
FD = 'C:/Windows/Fonts/'
YELLOW = (255, 230, 40); WHITE = (255, 255, 255); BLACK = (18, 14, 28); INK = (28, 24, 58)
COLS = dict(white=(255, 255, 255), yellow=YELLOW, pink=(255, 110, 170), cyan=(90, 225, 255), green=(120, 240, 150), red=(255, 80, 80), orange=(255, 170, 60))
PLATES = dict(yellow=(255, 226, 40), red=(235, 60, 70), blue=(40, 130, 240), green=(40, 190, 110), pink=(240, 80, 150), orange=(255, 140, 30), white=(255, 255, 255), purple=(130, 80, 230))
# 章ごとの背景色（上→下）。章の番号で巡回する
PAL = [((226, 58, 110), (255, 140, 50)), ((20, 130, 220), (110, 90, 235)), ((20, 170, 130), (30, 130, 190)), ((235, 130, 20), (225, 60, 70)),
       ((130, 80, 230), (225, 70, 140)), ((10, 150, 190), (50, 100, 220)), ((235, 100, 30), (220, 160, 20)), ((90, 90, 235), (225, 70, 140))]


def bind(g):
    global G
    G = g   # vp.py の globals そのもの（SPEC が差し替わっても追従する）


@lru_cache(maxsize=64)
def heavy(size):
    f = ImageFont.truetype(FD + 'NotoSansJP-VF.ttf', size)
    f.set_variation_by_axes([900])
    return f


@lru_cache(maxsize=64)
def semi(size):
    f = ImageFont.truetype(FD + 'NotoSansJP-VF.ttf', size)
    f.set_variation_by_axes([700])
    return f


def ease(x):
    x = min(1, max(0, x))
    return x * x * (3 - 2 * x)


def bounce(x):
    """0→1 で、少し行きすぎて戻る（ぽんっと出る）"""
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    c1, c3 = 1.9, 2.9
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def pop_k(cx, i, dur=.38):
    """文 i が始まってからの出方（0〜1）"""
    if i is None: return 1.0
    if not cx.on(i): return 0.0
    return (cx.t - cx.st[i]) / dur


# ---------------------------------------------------------------- 背景・見出し・字幕（vp.py から呼ばれる）
@lru_cache(maxsize=16)
def _grad(ci):
    c1, c2 = PAL[ci % len(PAL)]
    h, w = 270, 480
    y = np.linspace(0, 1, h)[:, None, None]
    x = np.linspace(0, 1, w)[None, :, None]
    k = np.clip(0.75 * y + 0.25 * x, 0, 1)
    return np.array(c1)[None, None, :] * (1 - k) + np.array(c2)[None, None, :] * k, x, y


def background(ci, t):
    base, x, y = _grad(ci)
    s = 0.5 + 0.5 * np.sin((x * 480 + y * 270 * 1.7) * 0.075 - t * 0.8)
    dots = 0.5 + 0.5 * np.sin(x * 480 * 0.55) * np.sin(y * 270 * 0.55)
    v = base * (1 - 0.0) + 255 * (0.07 * s + 0.05 * (dots > 0.82))
    r = np.sqrt(((x - 0.5) * 1.1) ** 2 + (y - 0.5) ** 2)
    v = v * (1 - 0.55 * np.clip(r - 0.35, 0, 1))
    im = Image.fromarray(np.clip(v, 0, 255).astype('uint8')).resize((1920, 1080), Image.BILINEAR).convert('RGBA')
    return im


def header(d, ci):
    title = G['SPEC']['chapters'][ci].get('title', '')
    f = heavy(54)
    w = d.textlength(title, font=f)
    x0, y0 = 40, 26
    d.rounded_rectangle((x0 + 7, y0 + 9, x0 + w + 61, y0 + 90), 20, fill=(0, 0, 0, 110))
    d.rounded_rectangle((x0, y0, x0 + w + 54, y0 + 81), 20, fill=YELLOW + (255,), outline=BLACK + (255,), width=5)
    d.text((x0 + 27, y0 + 9), title, font=f, fill=BLACK + (255,))


def subs(d, lines, f, rich):
    """字幕。帯なし・太い黒ふち。rich は rich_text。下に薄い影を敷く（呼び出し側）"""
    for j, txt in enumerate(lines):
        rich.draw_center(d, 960, 862 + j * 86, txt, f, '#ffffff', YELLOW, stroke_width=10, stroke_fill=BLACK)


def subs_shade(lay):
    g = Image.new('L', (1, 1080), 0)
    px = g.load()
    for yy in range(1080):
        px[0, yy] = int(170 * max(0, min(1, (yy - 780) / 260)))
    sh = Image.new('RGBA', (1920, 1080), (8, 6, 20, 255))
    sh.putalpha(g.resize((1920, 1080)))
    lay.alpha_composite(sh)


# ---------------------------------------------------------------- 部品
_BG = {}


def _bg_big(name, blur):
    key = (name, blur)
    if key not in _BG:
        src = Image.open(G['P'](G['SPEC']['images'][name]['file'])).convert('RGB')
        sc = max(1920 / src.width, 1080 / src.height) * 1.25
        big = src.resize((int(src.width * sc) + 1, int(src.height * sc) + 1), Image.LANCZOS)
        if blur: big = big.filter(ImageFilter.GaussianBlur(blur))
        _BG[key] = ImageEnhance.Color(big).enhance(1.35)
    return _BG[key]


def _chap_prog(cx):
    """章の進み具合 0〜1（カードのゆっくりしたズームに使う）"""
    tl = G.get('TL') or []
    if cx.ci < len(tl):
        s, e = tl[cx.ci]['start'], tl[cx.ci]['end']
        return max(0.0, min(1.0, (cx.t - s) / max(0.1, e - s)))
    return 0.0


def _bg_crop(big, prog, zoom, rev=False):
    z = 1 - zoom * (1 - prog if rev else prog)
    q = (1 - prog) if rev else prog
    w, h = 1920 * z, 1080 * z
    ox = (big.width - w) * (0.3 + 0.4 * q); oy = (big.height - h) * 0.5
    # 整数pxで切ると同じコマが続いて「静止」に見えるので、小数のまま拡大縮小する
    return big.transform((1920, 1080), Image.AFFINE,
                         (w / 1920, 0, ox, 0, h / 1080, oy),
                         resample=Image.BILINEAR).convert('RGBA')


def pop_bgimg(im, d0, cx, it, a):
    """写真いっぱいの背景。ゆっくり拡大。spec: dict(t='anim', name='pop_bgimg', img='aerial_1936', at=0, until=N, dim=.5, blur=4, zoom=.12,
    alts=['別の背景', ...], seg=22)  alts があれば seg 秒ごとに別の写真へ、ゆっくり溶けて切り替わる（同じ背景が続く単調さを避ける）"""
    blur = it.get('blur', 4); zoom = it.get('zoom', .12)
    names = [it['img']] + list(it.get('alts') or [])
    if len(names) == 1:
        prog = min(1.0, 0.02 + 0.98 * _chap_prog(cx))   # 章の間ずっと動かす（以前は開始40秒で止まっていた）
        crop = _bg_crop(_bg_big(names[0], blur), prog, zoom)
    else:
        seg = float(it.get('seg', 22)); fade = 1.6
        t0 = cx.st[it['at']] if it.get('at') is not None and cx.on(it['at']) else 0.0
        tt = max(0.0, cx.t - t0)
        n = int(tt // seg); local = tt - n * seg
        cur = names[n % len(names)]
        crop = _bg_crop(_bg_big(cur, blur), min(1.0, local / seg), zoom, rev=(n % 2 == 1))
        if n > 0 and local < fade:
            prev = names[(n - 1) % len(names)]
            pc = _bg_crop(_bg_big(prev, blur), 1.0, zoom, rev=((n - 1) % 2 == 1))
            crop = Image.blend(pc, crop, ease(local / fade))
    dim = it.get('dim', .5)
    crop = Image.blend(crop, Image.new('RGBA', crop.size, (10, 8, 30, 255)), dim)
    if a < 1: crop.putalpha(crop.getchannel('A').point(lambda v: int(v * a)))
    im.alpha_composite(crop)


def _runs(text):
    """[[強調]] を黄色にする。[(断片, 強調か)]"""
    out, i = [], 0
    while True:
        s = text.find('[[', i)
        if s < 0:
            out.append((text[i:], False)); break
        e = text.find(']]', s)
        out.append((text[i:s], False)); out.append((text[s + 2:e], True)); i = e + 2
    return [(t, h) for t, h in out if t]


def _text_img(text, size, col, plate=None, maxw=1500, pad=None, stroke=None):
    """テロップ1枚（透明画像）。改行は \\n。plate があれば色つきの角丸の板の上に黒文字"""
    d0 = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    f = heavy(size)
    lines = []
    for ln in text.split('\n'):
        lines += G['wrapn'](d0, ln.replace('[[', '').replace(']]', ''), f, maxw) if '[[' not in ln else [ln]
    if len(lines) > 1 and all('[[' not in l for l in lines):
        # 最終行が短すぎる（1〜2文字だけ次の行に落ちる）ときは、同じ行数で幅を詰めて均等にする
        plain = ''.join(lines); n = len(lines)
        if len(lines[-1]) < 0.4 * len(lines[0]):
            lo, hi = 200, maxw
            while hi - lo > 8:
                mid = (lo + hi) // 2
                tl = G['wrapn'](d0, plain, f, mid)
                if len(tl) <= n: hi = mid
                else: lo = mid
            lines = G['wrapn'](d0, plain, f, hi)
    lh = int(size * 1.22)
    ws = [d0.textlength(l.replace('[[', '').replace(']]', ''), font=f) for l in lines]
    stroke = stroke if stroke is not None else max(6, int(size * .13))
    pad = pad if pad is not None else (int(size * .45) if plate else stroke + 6)
    W, H = int(max(ws)) + pad * 2 + 8, lh * len(lines) + pad * 2 - (int(size * .1) if not plate else 0) + 8
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if plate:
        pc = PLATES.get(plate, plate)
        d.rounded_rectangle((6, 10, W - 2, H - 2), int(size * .5), fill=(0, 0, 0, 120))
        d.rounded_rectangle((2, 4, W - 8, H - 8), int(size * .5), fill=pc + (255,), outline=BLACK + (255,), width=max(4, int(size * .07)))
    y = pad
    for ln, w in zip(lines, ws):
        x = (W - w) / 2
        for seg, hi in _runs(ln):
            c = YELLOW if hi and not plate else (255, 255, 255) if plate == 'red' else col
            if plate:
                c = BLACK if plate in ('yellow', 'white', 'orange') else (255, 255, 255)
                if hi: c = (200, 20, 40) if plate in ('yellow', 'white', 'orange') else YELLOW
                d.text((x, y), seg, font=f, fill=c + (255,))
            else:
                d.text((x, y), seg, font=f, fill=c + (255,), stroke_width=stroke, stroke_fill=BLACK + (255,))
            x += d0.textlength(seg, font=f)
        y += lh
    return im


SUB_TOP = 836   # 字幕の枠は y=850 から


def _place(im, pic, cx_, cy_, k, rot=0.0, settle=True, zoom=1.0):
    """pic を中心 (cx_, cy_) に、k(0〜1の出方)で弾ませて置く。zoom でゆっくり拡大（静止画の単調さ対策）"""
    if k <= 0: return
    s = (max(0.01, bounce(k)) if k < 1 else 1.0) * zoom
    r = rot * (1 + (1 - ease(k)) * 1.5 if settle and k < 1 else 1)
    w, h = max(1, int(pic.width * s)), max(1, int(pic.height * s))
    p = pic.resize((w, h), Image.LANCZOS) if s != 1 else pic
    if r: p = p.rotate(r, resample=Image.BICUBIC, expand=True)
    if cy_ + p.height / 2 > SUB_TOP: cy_ = SUB_TOP - p.height / 2
    if k < .3: p.putalpha(p.getchannel('A').point(lambda v: int(v * k / .3)))
    im.alpha_composite(p, (int(cx_ - p.width / 2), int(cy_ - p.height / 2)))


def pop_telop(im, d0, cx, it, a):
    """大きな文字のテロップ。spec: dict(t='anim', name='pop_telop', text='渋谷は[[坂だらけ]]！', x=960, y=400, size=110,
    col='white', plate=None|'yellow'|'red'..., rot=-2, at=N, until=M, maxw=1500)"""
    k = pop_k(cx, it.get('at'))
    key = ('tp', it['text'], it.get('size', 100), it.get('col', 'white'), str(it.get('plate')), it.get('maxw', 1500))
    if key not in _BG:
        _BG[key] = _text_img(it['text'], it.get('size', 100), COLS.get(it.get('col', 'white'), WHITE), it.get('plate'), it.get('maxw', 1500))
    pic = _BG[key]
    # ふわっと上下に揺れる
    bob = 5 * math.sin(cx.t * 2.2 + len(it['text']))
    _place(im, pic, it.get('x', 960), it.get('y', 500) + bob, k, it.get('rot', 0))


def pop_rows(im, d0, cx, it, a):
    """箇条書き。白いカードに色タグ。spec: dict(t='anim', name='pop_rows', x0=100, x1=1820, y0=190, size=40, gap=18,
    items=[dict(at=N, tag='1898年', text='淀橋浄水場が完成', col='orange', until=M)])"""
    x0, x1, y = it.get('x0', 100), it.get('x1', 1820), it.get('y0', 190)
    size, gap = it.get('size', 40), it.get('gap', 18)
    d = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    ymax = it.get('ymax', SUB_TOP)
    while True:
        f = semi(size); ft = heavy(int(size * .86)); yy_ = y
        for e in it['items']:
            tg = e.get('tag'); tw0 = int(d.textlength(tg, font=ft)) + 44 if tg else 0
            ln = G['wrapn'](d, e['text'], f, x1 - x0 - tw0 - 60)
            yy_ += max(len(ln) * int(size * 1.3), int(size * 1.2)) + 30 + gap
        if yy_ - gap <= ymax or size <= 24: break
        size = int(size * .92); gap = max(8, int(gap * .9))
    for n, e in enumerate(it['items']):
        un = e.get('until')
        tag = e.get('tag')
        tw_ = int(d.textlength(tag, font=ft)) + 44 if tag else 0
        lines = G['wrapn'](d, e['text'], f, x1 - x0 - tw_ - 60)
        h = max(len(lines) * int(size * 1.3), int(size * 1.2)) + 30
        top = y
        y += h + gap
        if not cx.on(e.get('at')) or (un is not None and cx.on(un)): continue
        k = pop_k(cx, e.get('at'), .45)
        W = x1 - x0
        card = Image.new('RGBA', (W + 20, h + 20), (0, 0, 0, 0)); c = ImageDraw.Draw(card)
        c.rounded_rectangle((8, 12, W + 12, h + 14), 22, fill=(0, 0, 0, 110))
        c.rounded_rectangle((4, 4, W + 4, h + 4), 22, fill=(255, 255, 255, 250), outline=BLACK + (255,), width=4)
        tx = 26
        if tag:
            pc = PLATES.get(e.get('col', 'orange'), PLATES['orange'])
            c.rounded_rectangle((4, 4, 4 + tw_, h + 4), 22, fill=pc + (255,), outline=BLACK + (255,), width=4)
            col = (255, 255, 255) if e.get('col', 'orange') in ('red', 'blue', 'green', 'pink', 'purple') else BLACK
            c.text((4 + tw_ / 2, 4 + h / 2), tag, font=ft, fill=col + (255,), anchor='mm')
            tx = tw_ + 28
        yy = 4 + (h - len(lines) * int(size * 1.3)) / 2
        for l in lines:
            for seg, hi in _runs(l):
                pass
            c.text((tx, yy), l, font=f, fill=INK + (255,))
            yy += int(size * 1.3)
        fade_in = e.get('fade_in', True)
        travel = 80 if not fade_in else 140
        off = (1 - ease(k)) * travel * (1 if n % 2 == 0 else -1)
        if k < 1 and fade_in:
            p = card.copy(); p.putalpha(p.getchannel('A').point(lambda v: int(v * min(1, k / .4))))
        else:
            p = card
        xpos = int(x0 - 10 + off * (0 if k >= 1 else 1))
        if not fade_in:
            xpos = max(0, min(im.width - p.width, xpos))
        im.alpha_composite(p, (xpos, int(top - 6)))


def _frame_photo(pic, cap=None, size=30):
    """白縁の写真（ポラロイド風）"""
    b = 16; capH = (size + 30) if cap else 0
    W, H = pic.width + b * 2, pic.height + b * 2 + capH
    im = Image.new('RGBA', (W + 24, H + 24), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((14, 18, W + 12, H + 14), 12, fill=(0, 0, 0, 120))
    d.rounded_rectangle((6, 6, W + 6, H + 6), 12, fill=(255, 255, 255, 255))
    im.alpha_composite(pic.convert('RGBA'), (6 + b, 6 + b))
    if cap:
        d.text((6 + W / 2, 6 + b * 2 + pic.height + capH / 2 - 8), cap, font=semi(size), fill=INK + (255,), anchor='mm')
    return im


def pop_card(im, d0, cx, it, a):
    """写真・図を、傾けて置く。spec: dict(t='anim', name='pop_card', inner='photos'|'flow'|'edo'|'img', box=[...], rot=-1.5, at=N, until=M, ...inner用のキー)
    inner='img' は img= の画像を box に収め、cap= を白縁の下に出す。それ以外は vp_anim_shibuya の同名の図を、暗いカードにのせる。"""
    k = pop_k(cx, it.get('at'), .5)
    if k <= 0: return
    x0, y0, x1, y1 = it['box']; W, H = x1 - x0, y1 - y0
    inner = it['inner']
    if inner == 'img':
        cap = it.get('cap')
        pic = G['get_img'](it['img'], W - 44, H - 44 - (60 if cap else 0))
        card = _frame_photo(pic.convert('RGBA'), cap)
    else:
        import vp_anim_shibuya as S
        tmp = Image.new('RGBA', im.size, (0, 0, 0, 0))
        fn = dict(photos=S.sb_photos, flow=S.sb_flow, edo=S.sb_edo)[inner]
        fn(tmp, ImageDraw.Draw(tmp), cx, dict(it, box=[x0, y0, x1, y1]), 1.0)
        piece = tmp.crop((x0, y0, x1, y1))
        if inner == 'photos':
            card = _frame_photo(piece, None)
        else:
            card = Image.new('RGBA', (W + 24, H + 24), (0, 0, 0, 0)); c = ImageDraw.Draw(card)
            c.rounded_rectangle((14, 18, W + 12, H + 14), 26, fill=(0, 0, 0, 120))
            c.rounded_rectangle((6, 6, W + 6, H + 6), 26, fill=(14, 20, 48, 238), outline=(255, 255, 255, 255), width=6)
            card.alpha_composite(piece, (12, 12))
    _place(im, card, (x0 + x1) / 2, (y0 + y1) / 2, k, it.get('rot', 0),
           zoom=1 + it.get('zoom', .04) * _chap_prog(cx))


def _fill_img(name):
    """模式図は透過を持つので、RGB に落とす get_img ではなく RGBA のまま読む。"""
    key = ('fill', name)
    if key not in _BG:
        _BG[key] = Image.open(G['P'](G['SPEC']['images'][name]['file'])).convert('RGBA')
    return _BG[key]


def pop_fill(im, d0, cx, it, a):
    """段階を追って陸地が広がる図。spec: dict(t='anim', name='pop_fill', base='fillmap_0',
    steps=[dict(img='fillmap_1', at=0), dict(img='fillmap_2', at=2)], box=[...], rot=-2, at=0, cap='...')
    steps の各画像は base と同じ大きさの透過PNG。at の文が始まると、ふわっと重なる。"""
    k = pop_k(cx, it.get('at'), .5)
    if k <= 0: return
    x0, y0, x1, y1 = it['box']; W, H = x1 - x0, y1 - y0
    cap = it.get('cap')
    tw, th = W - 44, H - 44 - (60 if cap else 0)
    base = _fill_img(it['base'])
    sc = min(tw / base.width, th / base.height)
    size = (max(1, int(base.width * sc)), max(1, int(base.height * sc)))
    key = ('fillc', it['base'], size)
    if key not in _BG:
        _BG[key] = base.resize(size, Image.LANCZOS)
    pic = _BG[key].copy()
    for st in it['steps']:
        ka = ease(cx.a(st.get('at'), .45))
        if ka <= 0: continue
        sk = ('fillc', st['img'], size)
        if sk not in _BG:
            _BG[sk] = _fill_img(st['img']).resize(size, Image.LANCZOS)
        lay = _BG[sk]
        if ka < 1:
            lay = lay.copy()
            lay.putalpha(lay.getchannel('A').point(lambda v: int(v * ka)))
        pic.alpha_composite(lay)
    cr = it.get('credit')
    if cr:
        f2 = semi(max(14, int(pic.width * .022)))
        d2 = ImageDraw.Draw(pic)
        d2.text((pic.width - 12, pic.height - 10), cr, font=f2, fill=(255, 255, 255, 255),
                anchor='rs', stroke_width=4, stroke_fill=(32, 52, 78, 255))
    _place(im, _frame_photo(pic, cap), (x0 + x1) / 2, (y0 + y1) / 2, k, it.get('rot', 0),
           zoom=1 + it.get('zoom', .05) * _chap_prog(cx))


DRAW_POP = dict(pop_bgimg=pop_bgimg, pop_telop=pop_telop, pop_rows=pop_rows, pop_card=pop_card, pop_fill=pop_fill)
