"""Writes data/islands_spec.json（日本の島は、本当に2倍に増えた？）。台本：docs/themes/20261102_islands/09_script_v2.md"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from specart import inject
R = Path(__file__).resolve().parents[1]
spec = dict(slug='islands', theme_dir='20261102_islands', pack='16_islands_count', header_sub='島の数の変化を国土地理院の解説で確かめる',
 images={},
 bgm=[['intro', 'nums', 'piano36'], ['count', 'new', 'piano12'], ['land', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='日本の島は、2倍に増えた？', chapter_title='導入：日本の島は、2倍に増えた？', opener='日本の島は、2倍に増えた？', opener_until=1, scene=[
   dict(t='chips', y=250, w=640, h=150, gap=160, size=52, items=[dict(at=0, text='6,852島'), dict(at=0, text='14,125島')]),
   dict(t='big', text='日本の島は、本当に増えた？', y=470, at=2, size=60, col='gold'),
   dict(t='panel', box=[120, 610, 1800, 700], text='国土地理院の解説で、数字の意味を確かめる', at=3, size=42, hi=True),
   dict(t='panel', box=[120, 730, 1800, 800], text='資料：国土地理院（報道発表・よくある質問）', at=3, size=32)]),
 dict(key='nums', title='二つの数字は、何なのか', chapter_title='二つの数字は、何なのか', scene=[
   dict(t='bars', box=[60, 200, 1860, 560], title='公表された、日本の島の数', unit='島', max=15000, lab_w=520, data=[
     dict(at=0, label='海上保安庁（昭和62年）', value=6852, vlabel='6,852島', col='blue'),
     dict(at=1, label='国土地理院（2023年2月）', value=14125, vlabel='14,125島', col='org')]),
   dict(t='panel', box=[60, 590, 1860, 700], text='国土地理院：従来の数字と大きく異なるのは、測量技術の進歩による、地図表現の詳細化が、大きく影響していると考えられる', at=2, size=36, hi=True),
   dict(t='panel', box=[60, 730, 1860, 830], text='14,125 ÷ 6,852 ≒ 2.06（自作の計算）', at=4, size=44, col='gold')]),
 dict(key='count', title='島は、どう数えたのか', chapter_title='島は、どう数えたのか', scene=[
   dict(t='panel', box=[60, 170, 1860, 235], text='国土地理院：島の定義は、国連海洋法条約に基づく', at=0, until=2, size=38, hi=True),
   dict(t='panel', box=[60, 170, 1860, 235], text='島の数え方には、国際的な取り決めがない', at=2, until=3, size=38),
   dict(t='panel', box=[60, 170, 1860, 235], text='法令等に基づく島 ＋ 電子国土基本図の陸地のうち、自然に形成され、周囲長0.1km以上', at=3, until=6, size=34, hi=True),
   dict(t='panel', box=[60, 170, 1860, 235], text='周囲長0.1kmは、昭和62年の海上保安庁の調査と同じ基準', at=8, until=9, size=38),
   dict(t='panel', box=[60, 170, 1860, 235], text='0.1km未満の陸地も、定義に当てはまれば、島になる', at=9, size=38, col='gold'),
   dict(t='shade', box=[60, 250, 1860, 850], at=0, alpha=0.5),
   dict(t='anim', name='islemap', box=[60, 250, 1100, 850], at=5, s_a=5, s_b=5, s_c=5),
   dict(t='bars', box=[1120, 300, 1860, 620], title='電子国土基本図の陸地（令和4年1月）', unit='', max=125000, lab_w=190, data=[
     dict(at=7, label='全陸地', value=120729, vlabel='120,729', col='blue'),
     dict(at=7, label='0.1km以上', value=14125, vlabel='14,125', col='org')])]),
 dict(key='new', title='新しい島が、見つかったのか', chapter_title='新しい島が、見つかったのか', scene=[
   dict(t='panel', box=[60, 170, 1860, 235], text='国土地理院（よくある質問）：電子国土基本図に描かれた陸地を、一定の条件で数えた結果', at=1, until=2, size=36, hi=True),
   dict(t='panel', box=[60, 170, 1860, 235], text='新しい島が見つかったわけではない', at=2, size=42, col='gold'),
   dict(t='shade', box=[60, 250, 1860, 850], at=0, alpha=0.5),
   dict(t='anim', name='islemap', box=[60, 250, 1860, 850], at=1, s_a=1, s_b=3, s_c=99, mode='both')]),
 dict(key='land', title='領土や領海には、影響するのか', chapter_title='領土や領海には、影響するのか', scene=[
   dict(t='panel', box=[60, 190, 1860, 300], text='国土地理院：今回の結果が、領土・領海に、影響することはない', at=0, size=42, hi=True),
   dict(t='panel', box=[60, 330, 1860, 440], text='島の数は、国境離島（領海基線を有する島。内閣府が公表）の数と、整合性を確保', at=1, size=38),
   dict(t='panel', box=[60, 470, 1860, 580], text='今後も、島の数は、適時に見直される', at=2, size=42, col='gold')]),
 dict(key='end', title='分かること、決められないこと', chapter_title='結論：分かること、決められないこと', scene=[
   dict(t='cols2', size=36, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=1, text='公表された島の数は、6,852島から14,125島へ、約2倍'),
      dict(at=2, text='新しい島が見つかったわけではなく、電子国土基本図の陸地を、一定の条件で数えた結果'),
      dict(at=3, text='測量技術の進歩による、地図表現の詳細化が大きく影響していると考えられる')]),
     right=dict(title='決められないこと', title_at=4, items=[
      dict(at=4, text='昭和62年の調査の、くわしい数え方'),
      dict(at=5, text='都道府県ごとの島の数')]))])
 ],
 desc=dict(title_main='日本の島は、本当に2倍に増えたのか', title_no=1,
  titles=['日本の島は、本当に2倍に増えた？ 国土地理院の解説で確かめる', '日本の島の数は6,852島から14,125島に？ 数え方の違いを確かめる', '日本の島は新しく見つかった？ 14,125島の数え方を確かめる'],
  intro='日本の島の数として公表された数字が、6,852島から、14,125島に変わった。そう聞いたことはありませんか。この動画では、国土地理院の解説から、島の数が変わった理由を確かめます。二つの数字は何なのか、島はどう数えたのか、新しい島が見つかったのか、領土や領海に影響するのか、を分けて見ていきます。分かることと決められないことを分けて、国土地理院の説明に帰属して述べます。',
  points=['6,852島は海上保安庁が昭和62年に公表した数字、14,125島は国土地理院が2023年2月に公表した数字です。国土地理院は、大きく異なるのは測量技術の進歩による地図表現の詳細化が大きく影響していると考えられる、と説明しています(国土地理院「我が国の島を数えました」)。', '島の定義は国連海洋法条約に基づきますが、数え方に国際的な取り決めはありません。国土地理院は、法令等に基づく島に加え、電子国土基本図に描かれた陸地のうち、自然に形成されたと判断した周囲長0.1km以上の陸地を数えました(同)。', '国土地理院のよくある質問は、数が2倍以上になった理由を、電子国土基本図に描かれた陸地を一定の条件で数えた結果とし、新しい島が見つかったわけではない、と説明しています。周囲長0.1km未満の陸地も、定義に当てはまれば島になります(国土地理院「日本の島の数 FAQ」)。', '今回の結果が領土・領海に影響することはない、と説明されています(国土地理院)。'],
  refs=['国土地理院 報道発表「我が国の島を数えました」:https://www.gsi.go.jp/kihonjohochousa/pressrelease20230228.html', '国土地理院「日本の島の数 よくあるご質問」:https://www.gsi.go.jp/kihonjohochousa/islands_FAQ.html', '国土地理院「我が国の島の数の計数方法」(資料1):https://www.gsi.go.jp/common/000247632.pdf'],
  credit_lines=['・図:自作(国土地理院の解説をもとにした模式図です。実在の地図・島の位置ではありません)', '・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実際の風景の再現ではありません)'],
  notes=['図は、国土地理院の説明を理解するための自作の模式図で、実在の地図・島の位置・数ではありません。', '昭和62年の海上保安庁の調査の詳しい数え方、都道府県別の島の数は、この動画では確認していません。', '「14,125÷6,852≒2.06」は、公表された二つの数字の自作の計算です。'],
  tags='島の数, 日本の島, 国土地理院, 14125島, 6852島, 海上保安庁, 電子国土基本図, 地理, 雑学, 検証',
  checks=['国土地理院の報道発表・FAQの原文を、公開前にもう一度開いて確認する(`docs/themes/20261102_islands/08_fact_check.md`)', '計数方法の資料1(https://www.gsi.go.jp/common/000247632.pdf)の原文を確認する(検索の要旨のみ確認済み)']),
 thumb=dict(bg='assets/islands/thumb_art.png', lines=[['日本の島', 110, 'white'], ['2倍に', 120, 'white'], ['増えた？', 130, 'gold']], sub='国土地理院の解説で確かめる', shade_col=[8,44,30], accent=[255,230,120], bar_col=[255,230,120], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and o.get('title'):
            h = o['box'][3] - o['box'][1]
            if h < 112:
                tx = o['title'] + '：' + o['text']; sz = min(o.get('size', 40), 40, int((o['box'][2] - o['box'][0] - 70) / len(tx)))
                if sz >= 26: o['title'] = None; o['text'] = tx; o['size'] = sz
                else: o['size'] = min(o.get('size', 40), 30)
            else: o['size'] = min(o.get('size', 40), 40 if h < 125 else 46)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


_fit(spec)
inject(spec, dict(intro='intro', nums='nums', count='count', new='new', land='land', end='end'))
(R / 'data' / 'islands_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
