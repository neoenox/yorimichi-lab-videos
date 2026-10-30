"""Writes data/shomi_spec.json（賞味期限）。台本：docs/themes/20261119_forest/09_script_v2.md
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


spec = dict(slug='shomi', theme_dir='20261121_shomi', pack='28_shomi', header_sub='賞味期限を、消費者庁のガイドラインで確かめる',
 images={},
 bgm=[['intro', 'how', 'piano36'], ['coef', 'after', 'piano12'], ['end', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='賞味期限は、過ぎたらもう食べられない？', chapter_title='導入：賞味期限は、過ぎたらもう食べられない？', opener='賞味期限は、過ぎたらもう食べられない？', opener_until=2, scene=[
   dict(t='big', text='賞味期限は、過ぎたらもう食べられない？', y=270, at=0, size=58, col='gold'),
   pn('賞味期限を、1日過ぎた食品。もう食べられない？', 0, 2, 44, box=[120, 640, 1800, 720]),
   pn('未開封・表示どおりの保存なら：「過ぎたら食べられない」期限ではない', 2, 3, 40, box=[120, 730, 1800, 810], col='gold'),
   pn('ただし、「いつまででも食べられる」とも言えない', 3, 4, 42, box=[120, 730, 1800, 810]),
   pn('消費者庁のガイドライン（令和7年3月）で確かめる', 4, None, 42, box=[120, 730, 1800, 810])]),
 dict(key='two', title='二つの期限', chapter_title='二つの期限', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980,
        left=dict(title='消費期限', title_at=1, items=[dict(at=1, text='定められた方法で保存した場合に、安全性を欠くおそれがないと認められる期限')]),
        right=dict(title='賞味期限', title_at=2, items=[dict(at=2, text='定められた方法で保存した場合に、期待される品質が十分に保てると認められる期限'), dict(at=3, text='期限を超えても、品質が保たれていることがある')])),
   pn('どちらも「開封する前の状態」で、表示された保存方法で保存した場合の期限', 4, None, 38, col='gold', box=[60, 720, 1860, 800])]),
 dict(key='how', title='どう決めるのか', chapter_title='どう決めるのか', scene=[
   dict(t='cols2', size=34, xm=940, xm2=980,
        left=dict(title='消費期限', title_at=0, items=[dict(at=0, text='微生物の試験など、安全性の検査の結果を優先して決める')]),
        right=dict(title='賞味期限', title_at=1, items=[dict(at=1, text='味や風味など、品質の検査の結果を優先して決める')])),
   pn('かつての「5日」で区別する考え方：平成20年に解消。消費者庁も推奨しない', 2, None, 38, box=[60, 720, 1860, 800])]),
 dict(key='coef', title='安全係数', chapter_title='安全係数', scene=[
   pn('検査で得られた期限に、1より小さい係数（安全係数）を掛けて決めることがある', 0, 2, 38),
   dict(t='bars', box=[60, 260, 1860, 520], title='自作の計算例（日数）', unit='日', max=12, lab_w=520, data=[
     dict(at=2, label='検査で得られた期限', value=10, vlabel='10日', col='blue'),
     dict(at=2, label='安全係数0.8を掛けた期限', value=8, vlabel='8日', col='org')]),
   pn('期限の決め方を示す計算例。期限のあと何日安全に食べられるかを示す数字ではない', 3, 4, 38, col='gold', box=[60, 560, 1860, 640]),
   pn('令和7年3月のガイドライン：係数は1に近づけることが望ましい', 4, 5, 40, hi=True),
   pn('加圧加熱殺菌のレトルト食品・缶詰など、安全性が十分に担保されている食品は、係数を考えなくてよい', 5, None, 36)]),
 dict(key='after', title='期限を過ぎたら', chapter_title='期限を過ぎたら', scene=[
   pn('賞味期限を表示した食品は、期限を過ぎても、必ずしもすぐに食べられなくなるわけではない（定められた方法で保存された場合）', 0, 2, 34, box=[60, 170, 1860, 300]),
   pn('消費者庁が示す表示の例', 2, 3, 42),
   pn('消費期限：「期限を過ぎたら食べないようにしてください」', 3, 4, 42, hi=True),
   pn('賞味期限：「おいしく食べることのできる期限です」', 4, 5, 42, hi=True),
   pn('消費期限を過ぎた食品は、食べないようにするのが基本', 5, 6, 42, col='gold'),
   pn('開封した食品は、期限内でも安全に食べられるとは限らない。なるべく早く食べる', 6, None, 40, col='gold')]),
 dict(key='end', title='分かること、決められないこと', chapter_title='結論：分かること、決められないこと', scene=[
   dict(t='cols2', size=34, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=1, text='未開封・表示どおりの保存なら、賞味期限は「おいしく食べられる期限」。過ぎても必ずしもすぐに食べられなくなるわけではない'),
      dict(at=2, text='消費期限は、過ぎたら食べないようにする期限')]),
     right=dict(title='決められないこと', title_at=3, items=[
      dict(at=4, text='期限を過ぎた食品を、今食べてよいか：食品の種類・保存・開封で変わる'),
      dict(at=6, text='まず、保存方法を守っていたか確かめる')]))])
 ],
 desc=dict(title_main='賞味期限は過ぎたら食べられないのか', title_no=1,
  titles=['賞味期限は、過ぎたらもう食べられない？ 消費者庁のガイドラインで確かめる', '消費期限と賞味期限の違いは？ 安全係数と「期限を過ぎたら」を確かめる', '賞味期限切れはすぐ食べられなくなる？ ガイドラインの原文で確かめる'],
  intro='賞味期限を1日過ぎた食品は、もう食べられないのでしょうか。この動画では、消費者庁の「食品期限表示の設定のためのガイドライン」(令和7年3月)の本文で、消費期限と賞味期限の定義、期限の決め方、安全係数、期限を過ぎたときの考え方を確かめます。食べてよいかどうかの個別の判断は、動画では断定しません。',
  points=['食品表示基準の定義では、消費期限は「安全性を欠くおそれがないと認められる期限」、賞味期限は「期待される全ての品質の保持が十分に可能であると認められる期限」です。ただし賞味期限を超えても、品質が保たれていることがあるとされています。', '消費期限は微生物試験など安全性の検査を、賞味期限は理化学試験や官能検査など品質の検査を優先して設定します。「5日」で区別する考え方は平成20年に解消され、消費者庁も推奨していません。', '検査で得られた期限に1未満の係数(安全係数)を掛けて期限を決めることがあります。令和7年3月のガイドラインは、係数を1に近づけることが望ましいとしています。動画の「10日→8日」は期限の決め方を示す自作の計算例で、期限の後の安全日数を示すものではありません。', 'ガイドラインは、定められた方法で保存された場合、賞味期限を表示した食品は、期限を過ぎても必ずしもすぐに食べられなくなるわけではない、と書いています。ただし、期限は開封前の状態で表示どおりに保存した場合のものです。開封後は期限内でも安全に食べられるとは限らず、なるべく早く食べることが勧められています。'],
  refs=['消費者庁「食品期限表示の設定のためのガイドライン」(令和7年3月):https://www.caa.go.jp/policies/policy/food_labeling/food_labeling_act/assets/food_labeling_cms201_250328_1029.pdf', '消費者庁「食品期限表示の設定のためのガイドラインの見直し検討会 取りまとめ」(令和7年3月):https://www.caa.go.jp/policies/policy/food_labeling/food_sanitation/expiration_date/assets/food_labeling_cms201_250328_01.pdf'],
  credit_lines=['・図:自作(消費者庁のガイドラインの記述をもとにした表です)'],
  notes=['動画は、食品の安全を保証するものではありません。食べてよいかの判断は、食品の種類、保存の状態、開封の有無で変わります。表示された保存方法を確かめてください。', '「10日→8日」は期限の決め方を示す自作の計算例で、期限後の安全日数を示すものではありません。', '家庭で冷凍した場合の期限の扱いは、ガイドラインの公的な根拠を確認できなかったため、動画では取り上げていません。'],
  tags='賞味期限, 消費期限, 違い, 安全係数, 食品ロス, 消費者庁, ガイドライン, 雑学, 検証',
  checks=['ガイドライン本文(令和7年3月)の該当箇所(定義・2(3)・2(5)・Q&A 期限(消)-7)を、公開前にもう一度確認する', '安全係数の従来の目安「0.8以上」が、この版で削除されたかを、原文または見直し検討会とりまとめで確認する(動画では言っていない)', '`docs/themes/20261121_shomi/08_fact_check.md`']),
 thumb=dict(bg='assets/shomi/thumb_bg.png', lines=[['賞味期限は', 96, 'white'], ['過ぎたらNG？', 100, 'gold']], sub='消費者庁のガイドラインで確かめる', shade_col=[40, 24, 8], accent=[255, 200, 100], bar_col=[255, 200, 100], y0=14, bar_y=470, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and not o.get('title') and o['box'][3] - o['box'][1] <= 70: o['size'] = min(o.get('size', 40), 40)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


_fit(spec)
(R / 'data' / 'shomi_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
