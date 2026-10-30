"""自作アニメーション部品：脳の10%神話（brain10）。たとえの図で、脳の実際の形・位置を示すものではない。
vp_anim.py の末尾から読み込まれる（DRAW に登録）。"""
from PIL import Image, ImageDraw
import vp_anim as A
from vp_anim import layer, commit, vs, text, ease, T, S, WHITE, GOLD, DIM

RED = (235, 90, 80)
LIT = (239, 201, 118)
OFF = (60, 78, 100)


def grid100(im, d0, cx, it, a):
    """100マスを脳に見立てたたとえ。at：格子が出る。10マス＝『使われている』、90マス＝『使われていない（とされる）』。at2：10%より小さい範囲（4マス）が傷つく。"""
    box = it['box']; L, d = layer(box, 1.0); W, H = vs(box, 1.0)
    t0 = T(cx, it.get('at', 0)); t1 = T(cx, it.get('at2')) if it.get('at2') is not None else -1.0
    if t0 < 0:
        return
    cell = min(52, (H - 90) / 10); gx0 = 70; gy0 = 60
    hit = {(5, 4), (5, 5), (6, 4), (6, 5)}
    text(d, (gx0 - 10, 26), '脳を100マスにたとえた図（実際の脳の形ではありません）', 30, GOLD, 'lm')
    for r in range(10):
        for c in range(10):
            k = r * 10 + c
            kk = ease((t0 - k * 0.006) / 0.3)
            if kk <= 0:
                continue
            on = r < 1 and c < 10
            col = LIT if on else OFF
            if (r, c) in hit and t1 >= 0:
                k2 = ease(t1 / 0.5)
                col = tuple(int(OFF[i] + (RED[i] - OFF[i]) * k2) for i in range(3))
            x = gx0 + c * cell; y = gy0 + r * cell; m = cell * 0.08
            d.rounded_rectangle(((x + m) * S, (y + m) * S, (x + cell - m) * S, (y + cell - m) * S), 8 * S, fill=col + (int(255 * kk),))
    xr = gx0 + cell * 10 + 60
    d.rounded_rectangle((xr * S, (gy0 + 4) * S, (xr + 28) * S, (gy0 + 32) * S), 6 * S, fill=LIT + (255,))
    text(d, (xr + 44, gy0 + 18), '使われているとされる10%', 32, WHITE, 'lm')
    d.rounded_rectangle((xr * S, (gy0 + 64) * S, (xr + 28) * S, (gy0 + 92) * S), 6 * S, fill=OFF + (255,))
    text(d, (xr + 44, gy0 + 78), '使われていないとされる90%', 32, WHITE, 'lm')
    if t1 >= 0:
        k2 = ease(t1 / 0.5)
        d.rounded_rectangle((xr * S, (gy0 + 170) * S, (xr + 28) * S, (gy0 + 198) * S), 6 * S, fill=RED + (int(255 * k2),))
        text(d, (xr + 44, gy0 + 184), '10%よりずっと小さい範囲（4%）の損傷', 32, WHITE, 'lm', alpha=int(255 * k2))
        text(d, (xr, gy0 + 250), '90%が未使用なら、影響は出ないはず。', 34, WHITE, 'lm', alpha=int(255 * k2))
        text(d, (xr, gy0 + 300), '実際は、重い影響が出ることがある。', 34, GOLD, 'lm', alpha=int(255 * k2))
    commit(im, L, box, a)


DRAW_BRAIN = dict(grid100=grid100)
