"""Writes data/magnitude_spec.json（マグニチュードが1増えると、地震は10倍強くなる？）。台本：docs/themes/20261101_magnitude/09_script_v2.md"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from specart import inject
R = Path(__file__).resolve().parents[1]
spec = dict(slug='magnitude', theme_dir='20261101_magnitude', pack='17_magnitude_energy', header_sub='マグニチュードと震度を気象庁の解説で確かめる',
 images={},
 bgm=[['intro', 'diff', 'piano36'], ['energy', 'dist', 'piano12'], ['end', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='マグニチュードが1増えると、10倍強？', chapter_title='導入：マグニチュードが1増えると、10倍強？', opener='マグニチュードが1増えると、10倍強？', opener_until=1, scene=[
   dict(t='chips', y=250, w=640, h=150, gap=160, size=52, items=[dict(at=0, text='マグニチュード＋1'), dict(at=0, text='エネルギー10倍強？')]),
   dict(t='big', text='マグニチュードは、何の数字？', y=470, at=1, size=60, col='gold'),
   dict(t='panel', box=[120, 610, 1800, 700], text='気象庁の解説で、マグニチュードと震度の違いを確かめる', at=2, size=42, hi=True),
   dict(t='panel', box=[120, 730, 1800, 800], text='資料：気象庁（震度・マグニチュード・地震情報について）', at=3, size=32)]),
 dict(key='diff', title='マグニチュードと震度は、どう違うのか', chapter_title='マグニチュードと震度は、どう違うのか', scene=[
   dict(t='panel', box=[60, 170, 1860, 235], text='気象庁：マグニチュード＝地震そのものの大きさ（規模）', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=[60, 170, 1860, 235], text='気象庁：震度＝ある場所での、地震による揺れの強さ', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=[60, 170, 1860, 235], text='電球にたとえると、マグニチュード＝電球の明るさ、震度＝離れた場所での明るさ', at=2, until=5, size=34),
   dict(t='panel', box=[60, 170, 1860, 235], text='日本の震度は、全部で10階級', at=5, size=40, col='gold'),
   dict(t='shade', box=[60, 250, 1860, 850], at=0, alpha=0.5),
   dict(t='anim', name='bulb', box=[60, 250, 1860, 850], at=2, until=5, s_a=2, s_b=3, s_c=4),
   dict(t='anim', name='shindo', box=[60, 250, 1860, 850], at=5, s_a=5, s_b=6)]),
 dict(key='energy', title='マグニチュードが一つ大きいと、エネルギーは何倍か', chapter_title='マグニチュードが一つ大きいと、エネルギーは何倍か', scene=[
   dict(t='panel', box=[60, 170, 1860, 235], text='気象庁：マグニチュードが1大きくなると、エネルギーは、約32倍', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=[60, 170, 1860, 235], text='気象庁：2大きくなると、エネルギーは、約1,000倍', at=1, until=4, size=38, hi=True),
   dict(t='panel', box=[60, 170, 1860, 235], text='約32倍を2回かけると、約1,000（自作の計算）', at=4, until=5, size=38),
   dict(t='panel', box=[60, 170, 1860, 235], text='「10倍強」ではなく、1大きくなるごとに、約32倍', at=5, size=42, col='gold'),
   dict(t='shade', box=[60, 250, 1860, 850], at=0, alpha=0.5),
   dict(t='bars', box=[160, 330, 1760, 700], title='マグニチュード5のエネルギーを1としたときの比較（自作）', unit='', max=1000, lab_w=420, data=[
     dict(at=2, label='マグニチュード5', value=1, vlabel='1', col='blue'),
     dict(at=3, label='マグニチュード6', value=32, vlabel='約32', col='org'),
     dict(at=3, label='マグニチュード7', value=1000, vlabel='約1,000', col='gold')])]),
 dict(key='dist', title='マグニチュードが大きいと、揺れも大きいのか', chapter_title='マグニチュードが大きいと、揺れも大きいのか', scene=[
   dict(t='panel', box=[60, 170, 1860, 235], text='電球のたとえ：同じ電球でも、離れた場所では、周りは暗くなる', at=0, until=1, size=38),
   dict(t='panel', box=[60, 170, 1860, 235], text='電球のたとえ：電球から離れるほど、その場所の明るさは、小さくなる', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=[60, 170, 1860, 235], text='地震でも、震度は、場所によって異なることがある', at=2, size=40, col='gold'),
   dict(t='shade', box=[60, 250, 1860, 850], at=0, alpha=0.5),
   dict(t='anim', name='bulb', box=[60, 250, 1860, 850], at=0, s_a=0, s_b=0, s_c=1)]),
 dict(key='end', title='分かること、決められないこと', chapter_title='結論：分かること、決められないこと', scene=[
   dict(t='cols2', size=36, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=1, text='マグニチュードは地震そのものの大きさ、震度はある場所での揺れの強さ'),
      dict(at=2, text='マグニチュードが1大きいと、エネルギーは約32倍。2大きいと約1,000倍')]),
     right=dict(title='決められないこと', title_at=4, items=[
      dict(at=5, text='マグニチュードの数字だけでは、あなたのいる場所の震度は決められない')])),
   dict(t='panel', box=[60, 770, 1860, 840], text='なお：マグニチュードとエネルギーの、詳しい計算上の関係は、今回は扱いません', at=6, size=32, col='dim')])
 ],
 desc=dict(title_main='マグニチュードが1増えると、地震は10倍強くなるのか', title_no=1,
  titles=['マグニチュードが1増えると地震は10倍強い？ 気象庁の解説で確かめる', 'マグニチュードと震度の違いは？ エネルギーは約32倍を確かめる', 'マグニチュードが大きいと揺れも大きい？ 気象庁の解説で確かめる'],
  intro='「マグニチュードが一つ大きくなると、地震のエネルギーは、十倍強になる」。そう思っていませんか。この動画では、気象庁の解説から、マグニチュードと震度の違い、そして、エネルギーの差を確かめます。マグニチュードと震度はどう違うのか、一つ大きくなるとエネルギーは何倍か、マグニチュードが大きいと揺れも大きいのか、を分けて見ていきます。分かることと決められないことを分けて、気象庁の説明に帰属して述べます。',
  points=['気象庁の解説によると、マグニチュードは地震そのものの大きさ(規模)を表し、震度は、ある場所での、地震による揺れの強さを表します。電球にたとえると、マグニチュードは電球の明るさ、震度は離れた場所での明るさです(気象庁「震度・マグニチュード・地震情報について」)。', '日本の震度は、0、1、2、3、4、5弱、5強、6弱、6強、7の10階級で表されます(同)。', 'マグニチュードの値が1大きくなると、エネルギーは約32倍に、2大きくなると約1,000倍になります(同)。「約32倍を2回かけると約1,000」は自作の計算です。', 'マグニチュードの数字だけでは、あなたのいる場所の震度を決めることはできません。'],
  refs=['気象庁「震度・マグニチュード・地震情報について」:https://www.jma.go.jp/jma/kishou/know/faq/faq27.html'],
  credit_lines=['・図・グラフ・計算:自作(気象庁の解説をもとにした模式図と比較です。実際の観測値ではありません)', '・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実際の風景・観測の再現ではありません)'],
  notes=['図は、気象庁の説明を理解するための自作の模式図・比較で、実際の観測値ではありません。', 'マグニチュードとエネルギーの詳しい計算上の関係、震度に影響する具体的な場所の条件は、この動画では扱っていません。'],
  tags='マグニチュード, 震度, 地震, エネルギー, 32倍, 気象庁, 防災, 科学, 雑学, 検証',
  checks=['気象庁の原文を、公開前にもう一度開いて確認する(`docs/themes/20261101_magnitude/08_fact_check.md`)', '「震源から離れた場所の震度は小さくなることがある」の根拠を、気象庁の資料で確認する(ChatGPTは同ページに記載ありと述べたが、こちらは未確認)']),
 thumb=dict(bg='assets/magnitude/thumb_art.png', lines=[['M+1で', 130, 'white'], ['10倍強？', 130, 'gold']], sub='気象庁の解説で確かめる', shade_col=[48,16,6], accent=[255,150,70], bar_col=[255,150,70], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


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
inject(spec, dict(intro='intro', diff='diff', energy='energy', dist='dist', end='end'))
(R / 'data' / 'magnitude_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
