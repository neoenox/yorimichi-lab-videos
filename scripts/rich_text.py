"""強調つき文字描画。

字幕の中の「数字（数量・年号・割合・単位つき）」だけ色を変えて描く。
日本語の文章は数字の前後で分断されるので、run ごとに描いて x を進める。
"""
import re

# 算用数字（全角含む）＋小数点/桁区切り＋よく使う単位。単位は数字に密着している時だけ拾う。
NUM = re.compile(
    r'[0-9０-９]+(?:[.,][0-9０-９]+)*'
    r'(?:%|％|倍|万|億|千|百|人|名|年|月|日|時間|分|秒|km|km²|m|cm|mm|度|回|個|つ|位|件|種|階|代|時|貫|石|両|島|隻)?'
)


def runs(text):
    """[(断片, 数字かどうか), ...] に分解する。"""
    out, i = [], 0
    for m in NUM.finditer(text):
        if m.start() > i:
            out.append((text[i:m.start()], False))
        out.append((m.group(0), True))
        i = m.end()
    if i < len(text):
        out.append((text[i:], False))
    return out


def draw_line(d, x, y, text, font, base, hi, stroke_width=0, stroke_fill=None):
    """左上 (x, y) 基準で、数字だけ hi 色にして1行描く。"""
    for seg, is_num in runs(text):
        d.text((x, y), seg, font=font, fill=hi if is_num else base,
               stroke_width=stroke_width, stroke_fill=stroke_fill)
        x += d.textlength(seg, font=font)


def draw_center(d, cx, y, text, font, base, hi, stroke_width=0, stroke_fill=None):
    """中心 cx・上端 y で、数字だけ hi 色にして1行描く。"""
    x = cx - d.textlength(text, font=font) / 2
    draw_line(d, x, y, text, font, base, hi, stroke_width, stroke_fill)
