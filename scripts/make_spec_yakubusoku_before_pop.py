"""Writes data/yakubusoku_spec.json（「役不足」は、自分の能力が足りないという意味？）。台本：docs/themes/20261103_yakubusoku/09_script_v2.md"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from specart import inject
R = Path(__file__).resolve().parents[1]
spec = dict(slug='yakubusoku', theme_dir='20261103_yakubusoku', pack='18_yakubusoku_meaning', header_sub='「役不足」の意味を文化庁の調査で確かめる',
 images={},
 bgm=[['intro', 'ask', 'piano36'], ['result', 'meaning', 'piano12'], ['end', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='「役不足」の意味は？', chapter_title='導入：「役不足」の意味は？', scene=[
   dict(t='big', text='「彼には役不足の仕事だ」', y=330, at=0, size=76, col='gold'),
   dict(t='chips', y=470, w=700, h=130, gap=160, size=46, items=[dict(at=1, text='仕事が重すぎる？')]),
   dict(t='panel', box=[120, 640, 1800, 730], text='文化庁の「国語に関する世論調査」の結果で、意味を確かめる', at=1, size=42, hi=True),
   dict(t='panel', box=[120, 760, 1800, 830], text='資料：文化庁（平成14年度・平成18年度の調査）', at=2, size=32)]),
 dict(key='ask', title='文化庁の調査は、何を尋ねたのか', chapter_title='文化庁の調査は、何を尋ねたのか', scene=[
   dict(t='panel', box=[60, 190, 1860, 300], text='例文：「彼には役不足の仕事だ。」この言葉の意味は？', at=0, size=44, hi=True),
   dict(t='panel', box=[60, 340, 1860, 450], text='(ア)　本人の力量に対して、役目が重すぎること', at=1, size=42),
   dict(t='panel', box=[60, 480, 1860, 590], text='(イ)　本人の力量に対して、役目が軽すぎること', at=2, size=42),
   dict(t='panel', box=[60, 620, 1860, 720], text='文化庁：(イ)が、本来の意味', at=4, size=46, hi=True, col='gold'),
   dict(t='panel', box=[60, 750, 1860, 830], text='(ア)の「役目が重すぎる」は、本来の意味ではない、と整理されている', at=5, size=36)]),
 dict(key='result', title='調査の結果は、どうだったのか', chapter_title='調査の結果は、どうだったのか', scene=[
   dict(t='bars', box=[60, 190, 1860, 470], title='平成14年度の調査（文化庁）', unit='％', max=70, lab_w=560, data=[
     dict(at=0, label='(ア)役目が重すぎる', value=62.8, vlabel='62.8％', col='org'),
     dict(at=1, label='(イ)役目が軽すぎる（本来の意味）', value=27.6, vlabel='27.6％', col='blue')]),
   dict(t='bars', box=[60, 490, 1860, 770], title='平成18年度の調査（文化庁）', unit='％', max=70, lab_w=560, data=[
     dict(at=2, label='(ア)役目が重すぎる', value=50.3, vlabel='50.3％', col='org'),
     dict(at=2, label='(イ)役目が軽すぎる（本来の意味）', value=40.3, vlabel='40.3％', col='blue')]),
   dict(t='panel', box=[60, 790, 1860, 850], text='差：35ポイント（平成14年度）→ 10ポイント（平成18年度）', at=4, size=38, hi=True, col='gold')]),
 dict(key='meaning', title='この数字は、何を表しているのか', chapter_title='この数字は、何を表しているのか', scene=[
   dict(t='panel', box=[60, 200, 1860, 320], text='この数字は、調査に答えた人が、選んだ意味の割合', at=0, size=46, hi=True),
   dict(t='panel', box=[60, 360, 1860, 480], text='「いま、何割の人が、本来と違う意味で使っている」とは、言えない', at=1, size=42),
   dict(t='panel', box=[60, 520, 1860, 640], text='この動画で見たのは、平成14年度と平成18年度の調査', at=2, size=42),
   dict(t='panel', box=[60, 680, 1860, 800], text='その後の調査の結果は、この動画の資料だけでは、分からない', at=3, size=42, col='gold')]),
 dict(key='end', title='分かること、決められないこと', chapter_title='結論：分かること、決められないこと', scene=[
   dict(t='cols2', size=36, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=1, text='文化庁は、「役不足」の本来の意味を、「本人の力量に対して、役目が軽すぎること」としている'),
      dict(at=2, text='平成14年度・平成18年度の調査では、本来の意味ではない(ア)を選んだ人のほうが多かった')]),
     right=dict(title='決められないこと', title_at=3, items=[
      dict(at=4, text='いまの、本来の意味とそうでない意味の割合（この動画の資料だけでは分からない）')]))])
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
inject(spec, dict(intro='intro', ask='ask', result='result', meaning='meaning', end='end'))
(R / 'data' / 'yakubusoku_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
