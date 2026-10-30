"""Writes data/lightning_spec.json（雷）。台本：docs/themes/20261119_forest/09_script_v2.md
文の番号（at）は `python scripts/vp.py forest sents` の番号。図は棒グラフ（自作）のみ。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]


def pn(text, at, until=None, size=40, hi=True, col=None, box=TOP):
    d = dict(t='panel', box=box, text=text, at=at, size=size, hi=hi)
    if until is not None: d['until'] = until
    if col: d['col'] = col
    return d


spec = dict(slug='lightning', theme_dir='20261123_lightning', pack='29_lightning', header_sub='雷の俗説を、米国立気象局の説明で確かめる',
 images={},
 bgm=[['intro', 'empire', 'piano36'], ['cause', 'safety', 'piano12'], ['end', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='雷は、同じ場所に二度落ちない？', chapter_title='導入：雷は、同じ場所に二度落ちない？', opener='雷は、同じ場所に二度落ちない？', opener_until=2, scene=[
   dict(t='big', text='雷は、同じ場所に二度落ちない？', y=270, at=0, size=58, col='gold'),
   pn('「雷は、同じ場所に二度落ちない」と聞いたことは？', 0, 2, 44, box=[120, 640, 1800, 720]),
   pn('結論：これは、俗説とされている', 2, 3, 44, box=[120, 730, 1800, 810], col='gold'),
   pn('アメリカの国立気象局の説明で確かめる', 3, None, 44, box=[120, 730, 1800, 810])]),
 dict(key='nws', title='国立気象局の説明', chapter_title='国立気象局の説明', scene=[
   dict(t='cols2', size=34, xm=940, xm2=980,
        left=dict(title='よくある思い込み', title_at=1, items=[dict(at=1, text='「雷は、同じ場所に二度落ちない」')]),
        right=dict(title='国立気象局の説明', title_at=2, items=[dict(at=2, text='これは俗説とされている'), dict(at=3, text='特に、高く・とがった・孤立したものに、繰り返し落ちることがよくある')])),
   pn('資料：米国立気象局（NWS）「Lightning Myths」', 0, None, 34, box=[60, 740, 1860, 810])]),
 dict(key='empire', title='エンパイア・ステート・ビル', chapter_title='エンパイア・ステート・ビル', scene=[
   pn('米国立気象局：ニューヨークのエンパイア・ステート・ビルの例', 0, 1, 40),
   dict(t='bars', box=[60, 260, 1860, 520], title='このビルへの落雷（平均・1年あたり）', unit='回', max=30, lab_w=520, data=[
     dict(at=1, label='エンパイア・ステート・ビル', value=23, vlabel='平均で年に23回', col='org')]),
   pn('資料：米国立気象局（NWS）「Lightning Myths」', 0, None, 34, box=[60, 560, 1860, 630])]),
 dict(key='cause', title='どこに落ちるのか', chapter_title='どこに落ちるのか', scene=[
   dict(t='cols2', size=34, xm=940, xm2=980,
        left=dict(title='落ちる場所を決める、おもな要因', title_at=0, items=[dict(at=0, text='高さ'), dict(at=0, text='とがった形'), dict(at=0, text='周りから孤立していること')]),
        right=dict(title='関係しないもの', title_at=1, items=[dict(at=1, text='金属があるかどうか（まったく関係しない）')])),
   pn('詳しい物理の仕組みは、この動画では扱わない', 2, None, 40, box=[60, 740, 1860, 810], col='gold')]),
 dict(key='safety', title='安全のために', chapter_title='安全のために', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980,
        left=dict(title='避難する場所', title_at=0, items=[dict(at=0, text='頑丈な建物、屋根が硬い車へ（雷の音が聞こえたらすぐ）'), dict(at=2, text='家の中：電気を通すものを避ければ、安全な場所')]),
        right=dict(title='避けるもの', title_at=1, items=[dict(at=1, text='木の下：死傷の原因の第2位。濡れるほうがまし'), dict(at=3, text='有線の電話、電気製品、配線、水道の配管')])),
   pn('「一度落ちた場所なら安全」とは言えない', 4, None, 42, box=[60, 740, 1860, 810], col='gold')]),
 dict(key='end', title='分かること、決められないこと', chapter_title='結論：分かること、決められないこと', scene=[
   dict(t='cols2', size=34, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=1, text='「同じ場所に二度落ちない」は、国立気象局が俗説としている'),
      dict(at=2, text='高く・とがった・孤立したものには、繰り返し落ちることがある'),
      dict(at=3, text='エンパイア・ステート・ビルは、平均で年に23回'),
      dict(at=6, text='雷の音が聞こえたら、頑丈な建物か屋根が硬い車へ避難')]),
     right=dict(title='決められないこと', title_at=4, items=[
      dict(at=5, text='詳しい物理の仕組み（この動画では確かめていない）')]))])
 ],
 desc=dict(title_main='雷は同じ場所に二度落ちないのか', title_no=1,
  titles=['雷は、同じ場所に二度落ちない？ 米国立気象局の説明で確かめる', '「雷は同じ場所に落ちない」は本当？ エンパイア・ステート・ビルは年に23回', '雷の俗説を確かめる 落ちやすい場所と、避難の考え方'],
  intro='「雷は、同じ場所に二度落ちない」。そう聞いたことはありませんか。この動画では、アメリカの国立気象局(NWS)が公開している「Lightning Myths」の説明で、この俗説を確かめます。',
  points=['国立気象局は、「雷は同じ場所に二度落ちない」を俗説としています。雷は、特に高く、とがった、孤立したものに繰り返し落ちることがよくあると説明しています。', '例として、エンパイア・ステート・ビルには、平均で年に23回、雷が落ちるとされています(国立気象局)。', '国立気象局は、雷が落ちる場所を決めるおもな要因を、高さ、とがった形、周りから孤立していることとし、金属があるかどうかは関係しないとしています。', '国立気象局は、雷の音が聞こえたら頑丈な建物か屋根が硬い車に避難するよう勧め、木の下は避けるよう書いています。家の中は、電気を通すものを避ければ安全な場所だとされています。'],
  refs=['米国立気象局(NWS)「Lightning Myths」:https://www.weather.gov/safety/lightning-myths'],
  credit_lines=['・図:自作(米国立気象局の記述をもとにした表・グラフです)'],
  notes=['動画は、雷の安全を保証するものではありません。雷の音が聞こえたら、頑丈な建物か屋根が硬い車に避難してください。', '「約25回」「百回近く」などの別の数字を紹介する資料もありますが、動画では国立気象局のページに書かれた「平均で年に23回」だけを用いています。', '詳しい物理の仕組みは、動画では扱っていません。'],
  tags='雷, 落雷, 俗説, エンパイア・ステート・ビル, 米国立気象局, 雷の安全, 雑学, 検証',
  checks=['米国立気象局「Lightning Myths」の原文(23回、避難、家の中、木の下)を、公開前にもう一度確認する', '日本の気象庁の雷の安全の解説と、矛盾がないか確認する(動画はNWSの記述に限定)', '`docs/themes/20261123_lightning/08_fact_check.md`']),
 thumb=dict(bg='assets/lightning/thumb_bg.png', lines=[['雷は同じ場所に', 90, 'white'], ['落ちない？', 110, 'gold']], sub='米国立気象局の説明で確かめる', shade_col=[14, 16, 40], accent=[255, 230, 120], bar_col=[255, 230, 120], y0=14, bar_y=470, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and not o.get('title') and o['box'][3] - o['box'][1] <= 70: o['size'] = min(o.get('size', 40), 40)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


_fit(spec)
(R / 'data' / 'lightning_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
