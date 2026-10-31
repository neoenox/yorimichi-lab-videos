"""Writes data/yakubusoku_spec.json（「役不足」は、自分の能力が足りないという意味？）。台本：docs/themes/20261103_yakubusoku/09_script_v2.md"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize
R = Path(__file__).resolve().parents[1]
def pop(name, **kw):
    return dict(t='anim', name=name, **kw)


def tel(text, x, y, size, **kw):
    return dict(t='anim', name='pop_telop', text=text, x=x, y=y, size=size, **kw)


def rows(items, **kw):
    return dict(t='anim', name='pop_rows', items=items, **kw)


def card(inner, box, **kw):
    kw.setdefault('at', 0)
    return dict(t='anim', name='pop_card', inner=inner, box=box, **kw)


spec = dict(slug='yakubusoku', theme_dir='20261103_yakubusoku', pack='18_yakubusoku_meaning', header_sub='「役不足」の意味を文化庁の調査で確かめる',
 style='pop',
 images={n: dict(file=f'assets/yakubusoku/{n}.png') for n in ('art_intro', 'art_ask', 'art_result', 'art_meaning', 'art_end', 'chart_h14', 'chart_h18')},
 bgm=[['intro', 'ask', 'piano36'], ['result', 'meaning', 'piano12'], ['end', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='「役不足」の意味は？', chapter_title='導入：「役不足」の意味は？', scene=[
   pop('pop_bgimg', img='art_intro', at=0, dim=.5, blur=3),
   tel('「彼には\n[[役不足]]の仕事だ」', 960, 440, 130, at=0, until=1, rot=-2),
   tel('答え：本来は\n[[役目が軽すぎる]]', 960, 440, 120, at=1, until=2, plate='green', rot=2),
   tel('でも、選んだ人が多かったのは[[逆]]！', 960, 440, 96, at=2, plate='red', rot=-1.5),
   tel('文化庁の調査で確かめる', 960, 760, 54, at=1, plate='blue', rot=1)]),
 dict(key='ask', title='文化庁の調査は、何を尋ねたのか', chapter_title='文化庁の調査は、何を尋ねたのか', scene=[
   pop('pop_bgimg', img='art_ask', at=0, dim=.55, blur=4),
   tel('「彼には役不足の仕事だ」\nこの言葉の意味は？', 960, 240, 72, at=0, plate='yellow', rot=-1),
   rows([dict(at=1, tag='(ア)', text='役目が重すぎる', col='orange'),
         dict(at=2, tag='(イ)', text='役目が軽すぎる', col='blue')], x0=170, x1=1750, y0=400, size=64, gap=34),
   tel('ほかに「両方」「別の意味」「分からない」', 960, 800, 40, at=3, until=4, plate='blue', rot=1),
   tel('文化庁：本来の意味は[[(イ)]]', 960, 770, 76, at=4, plate='green', rot=-1.5)]),
 dict(key='result', title='調査の結果は、どうだったのか', chapter_title='調査の結果は、どうだったのか', scene=[
   pop('pop_bgimg', img='art_result', at=0, dim=.5, blur=8),
   card('img', [170, 110, 1750, 790], img='chart_h14', at=0, until=2, rot=-1),
   card('img', [170, 110, 1750, 790], img='chart_h18', at=2, until=4, rot=1),
   rows([dict(at=4, tag='H14', text='差　35ポイント', col='orange'),
         dict(at=4, tag='H18', text='差　10ポイント　（縮まった）', col='blue')], x0=170, x1=1750, y0=300, size=70, gap=40),
   tel('どちらの年度も、[[(ア)の方が多い]]', 960, 190, 84, at=3, until=4, plate='red', rot=-1.5),
   tel('差は縮まっている', 960, 800, 80, at=5, plate='yellow', rot=1.5)]),
 dict(key='meaning', title='この数字は、何を表しているのか', chapter_title='この数字は、何を表しているのか', scene=[
   pop('pop_bgimg', img='art_meaning', at=0, dim=.55, blur=6),
   rows([dict(at=0, tag='数字は', text='選んだ意味の割合', col='blue'),
         dict(at=1, tag='言えない', text='「いま何割が、本来と違う意味で使う」', col='red'),
         dict(at=2, tag='見たのは', text='平成14年度と平成18年度の調査', col='orange'),
         dict(at=3, tag='その後は', text='この資料だけでは、分からない', col='purple')], x0=130, x1=1790, y0=210, size=60, gap=34)]),
 dict(key='end', title='分かること、決められないこと', chapter_title='結論：分かること、決められないこと', scene=[
   rows([dict(at=0, tag='分かる', text='文化庁は、本来の意味を「役目が軽すぎる」としている', col='green'),
         dict(at=1, tag='分かる', text='H14・H18の調査では、逆の意味を選んだ人の方が多かった', col='green'),
         dict(at=2, tag='不明', text='いまの使われ方までは、この結果だけでは決められない', col='red')], x0=110, x1=1810, y0=190, size=52, gap=30),
   tel('「役不足」は[[軽すぎる役目]]の意味。\nただし、いまの割合は不明', 960, 700, 64, at=3, plate='yellow', rot=-1)])
 ],
 desc=dict(title_main='「役不足」は、自分の能力が足りないという意味なのか', title_no=1,
  titles=['「役不足」は、能力が足りない意味？ 文化庁の調査で確かめる', '「役不足」の本来の意味は？ 文化庁の世論調査の結果を確かめる', '「役不足」を、役目が重すぎる意味で選んだ人は？ 文化庁の調査'],
  intro='「彼には役不足の仕事だ」。この「役不足」は、自分の能力が足りない、という意味でしょうか。この動画では、文化庁の「国語に関する世論調査」の結果から、「役不足」の意味を確かめます。調査は何を尋ねたのか、結果はどうだったのか、その数字は何を表しているのか、を分けて見ていきます。調査の年度を限定して、文化庁の調査に帰属して述べます。',
  points=['文化庁の調査では、「彼には役不足の仕事だ。」という例文で意味を尋ねています。選択肢は、(ア)本人の力量に対して役目が重すぎること、(イ)本人の力量に対して役目が軽すぎること、で、文化庁は(イ)を本来の意味としています(文化庁「国語に関する世論調査」平成14年度・平成18年度)。', '平成14年度は(ア)62.8％、(イ)27.6％。平成18年度は(ア)50.3％、(イ)40.3％でした。差は35ポイントから10ポイントに縮まりました(同)。', 'この数字は、調査に答えた人が選んだ意味の割合です。「いま何割の人が本来と違う意味で使っている」と言えるものではありません。'],
  refs=['文化庁「平成18年度『国語に関する世論調査』の結果について」:https://www.bunka.go.jp/tokei_hakusho_shuppan/tokeichosa/kokugo_yoronchosa/h18/', '文化庁「平成14年度『国語に関する世論調査』の結果について」:https://www.bunka.go.jp/tokei_hakusho_shuppan/tokeichosa/kokugo_yoronchosa/h14/'],
  credit_lines=['・グラフ:自作(文化庁の調査結果の数字をもとにしています)', '・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実際の場面の再現ではありません)'],
  notes=['数字は、平成14年度・平成18年度の調査のものです。いまの割合を示すものではありません。', '令和6年度の調査結果、「役不足」の言葉の由来、「力不足」との使い分けは、この動画では確認していません。'],
  tags='役不足, 力不足, 言葉, 日本語, 誤用, 文化庁, 国語に関する世論調査, 雑学, 検証',
  checks=['文化庁の平成14・18年度の原文を、公開前にもう一度開いて確認する(`docs/themes/20261103_yakubusoku/08_fact_check.md`)', '令和年度の調査に「役不足」が含まれるか、文化庁の報告書で確認する(確認できれば最新の数字を足す)']),
 thumb=dict(bg='assets/yakubusoku/thumb_art.png', lines=[['役不足', 150, 'white'], ['逆の意味？', 105, 'gold']], sub='文化庁の調査で確かめる', shade_col=[58,10,16], accent=[255,205,90], bar_col=[255,255,255], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))

finalize(spec, {})
