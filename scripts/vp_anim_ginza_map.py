"""銀座本編用の、現在地図を土台にした累積形成アニメーション。"""
import math
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

G = {}
W, H = 1920, 1080
R = 6378137.0
MAP_CENTER = (35.6745, 139.7690)
GINZA = (35.6716, 139.7658)
WIDE = (35.6780, 139.7730)
AXIS = [(35.6900, 139.7735), (35.6839, 139.7744), (35.6760, 139.7696),
        (35.6713, 139.7650), (35.6648, 139.7596)]
HALF = 0.0030

def offset(points, delta):
    return [(lat, lon + delta) for lat, lon in points]

BAR = offset(AXIS, -HALF) + list(reversed(offset(AXIS, HALF)))
SEA_W = offset(AXIS, -HALF) + [(35.6650,139.7626),(35.6520,139.7626),
        (35.6520,139.7505),(35.6930,139.7505),(35.6930,139.7705)]
SEA_E = list(reversed(offset(AXIS, HALF))) + [(35.6520,139.7626),
        (35.6520,139.7980),(35.6930,139.7980),(35.6930,139.7765)]
MOATS = [offset(AXIS, 0.0016), offset(AXIS, -0.0022),
         [(35.6792,139.7660),(35.6812,139.7740),(35.6838,139.7810)],
         [(35.6646,139.7570),(35.6652,139.7650),(35.6644,139.7726)]]
MOAT_NAMES = ['三十間堀川', '外堀', '京橋川', '汐留川']
WATER = (42, 92, 108)
WATER_LINE = (70, 132, 145)
SAND = (211, 170, 94)
FILL = (221, 169, 83)
LAND_LINE = (184, 129, 48)
OFFWHITE = (255, 252, 242, 246)
_FONT_PATH = Path('C:/Windows/Fonts/NotoSansJP-VF.ttf')
_RAW = {}
_STATIC_BASE = None


def bind(g):
    global G
    G = g


def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def ease(v):
    v = clamp(v)
    return v * v * (3 - 2 * v)


def mix(a, b, p):
    return a + (b - a) * p


def geo(lat, lon):
    phi = math.radians(lat)
    return R * math.radians(lon + 180), R * math.asinh(math.tan(phi))


def tile_xy(lat, lon, z):
    n = 2 ** z
    return ((lon + 180) / 360 * n,
            (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n)


def _raw(name):
    if name not in _RAW:
        path = G['P'](G['SPEC']['images'][name]['file'])
        _RAW[name] = Image.open(path).convert('RGB')
    return _RAW[name]


def _map_frame(src, z, radius, cam):
    cx_tile, cy_tile = tile_xy(*MAP_CENTER, z)
    origin_x = math.floor(cx_tile) - radius
    origin_y = math.floor(cy_tile) - radius
    ppm = (2 ** z) * 256 / (2 * math.pi * R)
    x0_world = origin_x * 256 / ppm
    y_top_world = math.pi * R - (origin_y * 256) / ppm
    cx, cy, scale = cam
    a = ppm / scale
    c = (cx - x0_world) * ppm - (W / 2) * a
    f = (y_top_world - cy) * ppm - (H / 2) * a
    return src.transform((W, H), Image.Transform.AFFINE, (a, 0, c, 0, a, f),
                         resample=Image.Resampling.BICUBIC, fillcolor=(247, 247, 243))


def _map_base(cam):
    global _STATIC_BASE
    final = (geo(*MAP_CENTER)[0], geo(*MAP_CENTER)[1], 0.42)
    if all(abs(cam[i] - final[i]) < 1e-8 for i in range(3)) and _STATIC_BASE is not None:
        return _STATIC_BASE.copy()
    broad = _map_frame(_raw('pale_map_z15'), 15, 3, cam)
    detail = _map_frame(_raw('pale_map_z17'), 17, 6, cam)
    detail_mix = ease((cam[2] - 0.35) / 0.27)
    frame = Image.blend(broad, detail, detail_mix)
    frame = ImageEnhance.Color(frame).enhance(0.42)
    frame = Image.blend(frame, Image.new('RGB', (W, H), (250, 249, 245)), 0.32)
    result = frame.convert('RGBA')
    if all(abs(cam[i] - final[i]) < 1e-8 for i in range(3)):
        _STATIC_BASE = result.copy()
    return result


def screen(point, cam):
    x, y = geo(*point)
    return W / 2 + (x - cam[0]) * cam[2], H / 2 - (y - cam[1]) * cam[2]


def poly_points(points, cam):
    return [screen(p, cam) for p in points]


def _line(base, points, color, width):
    layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer, 'RGBA').line(points, fill=color, width=width, joint='curve')
    base.alpha_composite(layer)


def _polygon(base, points, color, alpha, outline=None, width=2):
    if alpha <= 0.001:
        return
    layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, 'RGBA')
    draw.polygon(points, fill=(*color, int(255 * clamp(alpha))))
    if outline:
        draw.line(points + [points[0]], fill=(*outline, int(255 * clamp(alpha))),
                  width=width, joint='curve')
    base.alpha_composite(layer)


def _font(size, weight=700):
    font = ImageFont.truetype(str(_FONT_PATH), size)
    try:
        font.set_variation_by_axes([weight])
    except Exception:
        pass
    return font


@lru_cache(maxsize=48)
def _cached_font(size, weight):
    return _font(size, weight)


def _label(base, point, text, size=30, color=(31, 48, 52), opacity=1.0,
           anchor='mm', weight=700, sw=5):
    opacity = clamp(opacity)
    if opacity <= 0.01:
        return
    xy = screen(point, _CURRENT_CAM[0])
    layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer, 'RGBA').text(
        xy, text, font=_cached_font(size, weight),
        fill=(*color[:3], int(255 * opacity)), anchor=anchor,
        stroke_width=sw, stroke_fill=(*OFFWHITE[:3], int(OFFWHITE[3] * opacity)))
    base.alpha_composite(layer)


def _map_callout(base, point, text, center, cam):
    """Keep the active moat name readable without covering the sandbar label."""
    sx, sy = screen(point, cam)
    draw = ImageDraw.Draw(base, 'RGBA')
    font = _cached_font(27, 700)
    width = int(draw.textlength(text, font=font)) + 34
    height = 50
    cx, cy = center
    x0, y0 = int(cx - width / 2), int(cy - height / 2)
    x1, y1 = x0 + width, y0 + height
    direction = 1 if cx > sx else -1
    edge_x = x0 if direction > 0 else x1
    elbow_x = sx + direction * 72
    tip_x = edge_x - direction * 8
    draw.line(((sx, sy), (elbow_x, sy), (tip_x, cy)),
              fill=(38, 109, 129, 225), width=4, joint='curve')
    draw.ellipse((sx - 6, sy - 6, sx + 6, sy + 6),
                 fill=(250, 249, 242, 245), outline=(38, 109, 129, 235), width=3)
    draw.rounded_rectangle((x0, y0, x1, y1), radius=13,
                           fill=(250, 249, 242, 238),
                           outline=(38, 109, 129, 220), width=2)
    draw.text((cx, cy), text, font=font, fill=(37, 83, 91, 255), anchor='mm')


_CURRENT_CAM = [None]


def _sentence_progress(cx, chapter_index, sentence_index, duration=1.8, delay=0.0):
    if cx.ci < chapter_index:
        return 0.0
    if cx.ci > chapter_index:
        return 1.0
    if sentence_index >= len(cx.st):
        return 0.0
    return ease((cx.t - cx.st[sentence_index] - delay) / duration)


def _chapter_index(key):
    return next(i for i, ch in enumerate(G['SPEC']['chapters']) if ch['key'] == key)


def _status(key, idx, moat_substage, multi_step=False):
    if key == 'maejima':
        if idx >= 3:
            return '中央通り｜砂州の軸をたどる'
        if idx >= 1:
            return '江戸前島｜砂州の半島（海岸線は推定）'
        return '江戸前島の砂州と、周囲の海・入り江'
    if key == 'west':
        return ('1603年〜｜日比谷入江を埋め立て' if idx >= 1
                else '西側｜日比谷入江（推定）')
    if key == 'east':
        return ('1657年以降｜築地側に土地を造成' if idx >= 1
                else '東側｜江戸初期はまだ海')
    if key == 'moat':
        if multi_step:
            if idx < 1:
                return '4本の堀｜銀座を囲む水路'
            if idx < 2:
                return '1949年〜｜三十間堀川の埋め立て'
            if idx < 3:
                return '外堀の埋め立て'
            if idx < 4:
                return '南側｜汐留川の埋め立て'
            if idx < 5:
                return '北側｜京橋川の埋め立て'
            if idx < 6:
                return '1964年｜東京高速道路が完成'
            return '掘割は道路に変わり、銀座は地続きに'
        if idx < 1:
            return '4本の堀｜銀座を囲む水路'
        if idx < 2:
            return '1949年〜｜三十間堀川の埋め立て'
        if idx < 3:
            return f'{MOAT_NAMES[moat_substage]}を、順に埋め立て'
        if idx < 4:
            return '掘割は道路に変わり、銀座は地続きに'
        return '砂州と埋立地が、現在の銀座の土地へ'
    return ''


def _pill(base, text):
    draw = ImageDraw.Draw(base, 'RGBA')
    box = (510, 126, 1410, 194)
    draw.rounded_rectangle(box, radius=20, fill=(250, 249, 242, 226),
                            outline=(116, 124, 113, 145), width=2)
    draw.text(((box[0] + box[2]) / 2, box[1] + 10), text,
              font=_cached_font(37, 700), fill=(30, 48, 53, 255), anchor='mt')


def _legend(base):
    draw = ImageDraw.Draw(base, 'RGBA')
    draw.rounded_rectangle((1212, 25, 1860, 120), radius=14,
                           fill=(250, 249, 242, 221), outline=(116, 124, 113, 125), width=2)
    draw.rounded_rectangle((1234, 42, 1266, 65), radius=5, fill=(60, 134, 157, 76),
                           outline=(56, 122, 143, 220), width=2)
    draw.text((1278, 37), '青：江戸初期の海・堀', font=_cached_font(25, 600),
              fill=(42, 66, 68, 255), anchor='lt')
    draw.rounded_rectangle((1234, 75, 1266, 98), radius=5, fill=(221, 169, 83, 94),
                           outline=(184, 129, 48, 220), width=2)
    draw.text((1278, 70), '黄：砂州・埋立地｜国土地理院の現在地図',
              font=_cached_font(24, 600), fill=(42, 66, 68, 255), anchor='lt')


def _camera(cx):
    ti = _chapter_index('maejima')
    start = G['TL'][ti]['start']
    if cx.ci > ti or cx.t >= start + 6.0:
        return (*geo(*MAP_CENTER), 0.42)
    p = ease((cx.t - start) / 6.0)
    x0, y0 = geo(*WIDE)
    x1, y1 = geo(*MAP_CENTER)
    return mix(x0, x1, p), mix(y0, y1, p), mix(0.315, 0.42, p)


def ginza_formation_map(im, d, cx, it, a):
    """Current GSI pale map with cumulative, narration-synchronized formation layers."""
    global _CURRENT_CAM
    key = G['SPEC']['chapters'][cx.ci]['key']
    if key not in ('maejima', 'west', 'east', 'moat'):
        return
    cam = _camera(cx)
    _CURRENT_CAM[0] = cam
    base = _map_base(cam)

    west_ch = _chapter_index('west')
    east_ch = _chapter_index('east')
    moat_ch = _chapter_index('moat')
    west_p = _sentence_progress(cx, west_ch, 1, 2.4)
    east_index = 2 if len(cx.st) >= 5 else 1
    east_p = _sentence_progress(cx, east_ch, east_index, 2.4)
    stage_idx = cx.idx()
    axis_p = _sentence_progress(cx, _chapter_index('maejima'), 3, 2.0)

    west = poly_points(SEA_W, cam)
    east = poly_points(SEA_E, cam)
    bar = poly_points(BAR, cam)
    _polygon(base, west, WATER, 0.12, WATER_LINE, 2)
    _polygon(base, east, WATER, 0.12, WATER_LINE, 2)
    _polygon(base, west, FILL, 0.28 * west_p, LAND_LINE, 3)
    south_east = [p for p in SEA_E if p[0] <= 35.6800]
    # Clip the eastern water boundary at the map's northern edge, retaining the south/Tsukiji half.
    def _clip_lat(poly, cut):
        out = []
        if not poly:
            return out
        prev = poly[-1]
        prev_in = prev[0] <= cut
        for cur in poly:
            cur_in = cur[0] <= cut
            if cur_in != prev_in:
                den = cur[0] - prev[0]
                if den:
                    q = (cut - prev[0]) / den
                    out.append((cut, prev[1] + q * (cur[1] - prev[1])))
            if cur_in:
                out.append(cur)
            prev, prev_in = cur, cur_in
        return out
    south_east = _clip_lat(SEA_E, 35.6800)
    if south_east:
        _polygon(base, poly_points(south_east, cam), FILL, 0.28 * east_p, LAND_LINE, 3)

    # The peninsula axis and its edges stay on the same geographic camera transform.
    _polygon(base, bar, SAND, 0.18, (156, 112, 48), max(2, int(2 * cam[2])))
    axis = poly_points(AXIS, cam)
    _line(base, axis, (150, 103, 43, int(105 + 130 * axis_p)), max(3, int(4 * cam[2])))
    for edge in (offset(AXIS, -HALF), offset(AXIS, HALF)):
        pts = poly_points(edge, cam)
        layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer, 'RGBA')
        length_on = True
        at = 0.0
        while at < len(pts) - 1:
            x0, y0 = pts[int(at)]
            x1, y1 = pts[min(len(pts)-1, int(at)+1)]
            length = math.hypot(x1-x0, y1-y0)
            if length < 1:
                at += 1
                continue
            ux, uy = (x1-x0)/length, (y1-y0)/length
            t = 0.0
            while t < length:
                end = min(length, t + 16)
                if length_on:
                    draw.line((x0+ux*t, y0+uy*t, x0+ux*end, y0+uy*end),
                              fill=(255, 248, 219, 190), width=max(2, int(3*cam[2])))
                length_on = not length_on
                t = end + 11
            at += 1
        base.alpha_composite(layer)

    # The four channels begin as water; each turns into a muted land/road trace in order.
    active_moat = 0
    multi_step_moat = len(cx.st) >= 7
    if cx.ci >= moat_ch:
        if cx.ci > moat_ch:
            moat_p = [1.0] * 4
            active_moat = 3
        elif multi_step_moat:
            # Narration names each waterway separately. Reveal and retain each route in that order.
            moat_p = [0.0] * 4
            route_order = [0, 1, 3, 2]
            step_starts = [1, 2, 3, 4]
            for route, sentence_index in zip(route_order, step_starts):
                if sentence_index < len(cx.st):
                    moat_p[route] = ease((cx.t - cx.st[sentence_index]) / 2.4)
            if stage_idx >= 1:
                active_moat = route_order[min(3, stage_idx - 1)]
        else:
            first = cx.st[1] if len(cx.st) > 1 else cx.t
            second = cx.st[2] if len(cx.st) > 2 else first
            starts = [first, second, second + 2.5, second + 5.0]
            moat_p = [ease((cx.t - s) / 1.8) for s in starts]
            active_moat = min(3, max(0, int(max(0, cx.t - second) // 2.5) + 1)) if stage_idx >= 2 else 0
            if stage_idx >= 1 and stage_idx < 2:
                active_moat = 0
            elif stage_idx >= 2:
                active_moat = min(3, int(max(0, cx.t - second) // 2.5) + 1)
        for j, path in enumerate(MOATS):
            p = moat_p[j]
            start_col = (38, 109, 129)
            end_col = (164, 130, 79)
            col = tuple(int(mix(start_col[k], end_col[k], p)) for k in range(3))
            _line(base, poly_points(path, cam), (*col, 205), max(6, int(21 * cam[2])))

    # Geographic labels are kept sparse and follow the map, not the video frame.
    pulse = 0.5 + 0.5 * math.sin(cx.t * 1.35)
    gx, gy = screen(GINZA, cam)
    radius = int(16 + 5 * pulse)
    mark = ImageDraw.Draw(base, 'RGBA')
    mark.ellipse((gx-radius, gy-radius, gx+radius, gy+radius),
                 outline=(234, 187, 91, 255), width=4)
    mark.ellipse((gx-6, gy-6, gx+6, gy+6), fill=(216, 92, 61, 255),
                 outline=(255, 248, 222, 255), width=3)
    _label(base, GINZA, '現在の銀座', 28, (31, 48, 52), anchor='lm', sw=5)
    _label(base, (35.6772, 139.7687), '砂州（推定）', 29, (103, 69, 26), sw=5)
    _label(base, (35.6805, 139.7565), '日比谷入江（推定）', 28, (28, 75, 91), sw=5,
           opacity=max(0.58, 1 - 0.42 * west_p))
    if west_p > 0.5:
        _label(base, (35.6815, 139.7540), '西側の埋立地', 27, (128, 85, 34), sw=5,
               opacity=ease((west_p - 0.5) / 0.5))
    east_point = (35.6662, 139.7780)
    _label(base, east_point, '築地側（推定）', 28,
           (128, 85, 34) if east_p > 0.5 else (28, 75, 91), sw=5,
           opacity=0.55 + 0.45 * east_p)
    if axis_p > 0.15:
        _label(base, (35.6800, 139.7720), '中央通り｜砂州の軸', 27,
               (103, 69, 26), sw=5, opacity=axis_p)

    if cx.ci >= moat_ch:
        path = MOATS[active_moat]
        mid = path[len(path)//2]
        if active_moat == 0:
            _map_callout(base, mid, MOAT_NAMES[active_moat], (1440, 520), cam)
        else:
            _label(base, mid, MOAT_NAMES[active_moat], 26, (37, 83, 91), sw=5)

    # Screen-fixed event tag and legend stay clear of the narration subtitle band.
    status = _status(key, stage_idx, active_moat, multi_step=multi_step_moat)
    _pill(base, status)
    _legend(base)
    scale_px = 500 * cam[2]
    xb, yb = W - 125 - scale_px, 746
    mark = ImageDraw.Draw(base, 'RGBA')
    mark.line((xb, yb, xb + scale_px, yb), fill=(33, 52, 56, 230), width=4)
    mark.line((xb, yb-9, xb, yb+9), fill=(33, 52, 56, 230), width=3)
    mark.line((xb+scale_px, yb-9, xb+scale_px, yb+9), fill=(33, 52, 56, 230), width=3)
    mark.text((xb + scale_px/2, yb - 15), '500 m', font=_cached_font(24, 600),
              fill=(33, 52, 56, 245), anchor='ms', stroke_width=3, stroke_fill=OFFWHITE)

    if a < 1:
        alpha = base.getchannel('A').point(lambda v: int(v * clamp(a)))
        base.putalpha(alpha)
    im.alpha_composite(base)
    # The base map replaces the pop background, so restore the normal chapter title and opener above it.
    if G.get('header'):
        G['header'](ImageDraw.Draw(im, 'RGBA'), cx.ci)
    if G.get('opener'):
        G['opener'](im, ImageDraw.Draw(im, 'RGBA'), cx)


DRAW_GINZA_MAP = {'ginza_formation_map': ginza_formation_map}
