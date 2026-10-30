"""Writes data/napoleon_spec.json（ナポレオンは、背が低かった？）。台本：docs/themes/20270313_napoleon/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
spec = dict(slug='napoleon', theme_dir='20270313_napoleon', pack='52_napoleon', header_sub='英語版Wikipediaと解説記事で、ナポレオンの身長を確かめる',
 images={},
 bgm=[['intro', 'hyoki', 'piano36'], ['tani', 'fuushi', 'piano12'], ['end', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='ナポレオンは、背が低かった？', chapter_title='導入：ナポレオンは、背が低かった？', opener='ナポレオンは、背が低かった？', opener_until=1, scene=[
   dict(t='big', text='ナポレオンは、背が低かった？', y=270, at=0, size=50, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='身長は157センチ、とも言われる', at=1, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：英語版Wikipediaと、解説記事', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 850], text='答え：低くなかった。当時の成人男性の平均くらい、と説明されている', at=4, size=32, col='gold')]),
 dict(key='hyoki', title='身長は、どう記録されているか', chapter_title='身長は、どう記録されているか', scene=[
   dict(t='panel', box=TOP, text='まず、記録された身長を見る', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='英語版Wikipedia：メートル法の前のフランスの単位で、5ピエ2プースと推定', at=1, until=2, size=32, hi=True),
   dict(t='panel', box=TOP, text='メートルに直すと、約1.67メートル', at=2, until=3, size=40, col='gold'),
   dict(t='panel', box=TOP, text='一部の歴史家は、1.70メートルとしている', at=3, until=4, size=40),
   dict(t='panel', box=TOP, text='同じ記事：1.67メートルは、当時の成人男性の平均身長（資料によって違う）', at=4, size=32),
   dict(t='table', box=[60, 300, 1860, 560], cols=['ナポレオンの身長（英語版Wikipedia）', '数字'], colw=[1200, 600], size=34, rows=[
     dict(at=2, cells=['フランスの昔の単位', '5ピエ2プース']),
     dict(at=2, cells=['メートルに直すと', '約1.67メートル'], col='gold'),
     dict(at=3, cells=['一部の歴史家', '1.70メートル'])])]),
 dict(key='tani', title='単位の違い', chapter_title='単位の違い', scene=[
   dict(t='panel', box=TOP, text='なぜ、157センチという数字が広まったのか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='解説記事：フランスと英国の単位は、同じ名前でも長さが違う（二次情報）', at=1, until=2, size=32, hi=True),
   dict(t='panel', box=TOP, text='自作の計算：フランスの1ピエ＝約32.5cm、1プース＝約2.7cm', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='5ピエ2プース ＝ 32.5×5 ＋ 2.7×2 ＝ 約168cm', at=3, until=4, size=40, col='gold'),
   dict(t='panel', box=TOP, text='英国の5フィート2インチなら、30.5×5 ＋ 2.5×2 ＝ 約157cm', at=4, until=5, size=36),
   dict(t='panel', box=TOP, text='単位を取り違えると、約11センチ、小さくなる', at=5, size=40, col='gold'),
   dict(t='table', box=[60, 300, 1860, 560], cols=['同じ「5と2」でも（自作の計算）', '長さ'], colw=[1200, 600], size=34, rows=[
     dict(at=3, cells=['フランスの5ピエ2プース', '約168cm'], col='gold'),
     dict(at=4, cells=['英国の5フィート2インチ', '約157cm'])])]),
 dict(key='fuushi', title='なぜ、小さいと思われたのか', chapter_title='なぜ、小さいと思われたのか', scene=[
   dict(t='panel', box=TOP, text='英国の風刺画家が、繰り返しナポレオンを小柄に描いた（英語版Wikipedia）', at=0, until=1, size=32, hi=True),
   dict(t='panel', box=TOP, text='目的：ナポレオンと、その領土拡大をからかうため', at=1, until=2, size=38),
   dict(t='panel', box=TOP, text='ジェームズ・ギルレイが、1803年の風刺画などで、小柄なイメージを広めたとされる', at=2, until=3, size=30),
   dict(t='panel', box=TOP, text='別の解説記事：背の高い護衛を周りに置いたため、小さく見えた、という説明も', at=3, until=4, size=32),
   dict(t='panel', box=TOP, text='ただし、護衛の話を裏付ける記録は、今回確認できなかった', at=4, size=36, col='gold')]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=1, items=[
      dict(at=1, text='約1.67メートルで、当時の成人男性の平均くらい（英語版Wikipedia）'),
      dict(at=2, text='157センチは、単位の違いによる読み違いと説明されている。自分の計算では約168cmと約157cm'),
      dict(at=3, text='小柄なイメージは、英国の風刺画で広まったとされる')]),
     right=dict(title='分からないこと・言い方', title_at=4, items=[
      dict(at=4, text='死亡時の記録の原典。護衛の話の根拠'),
      dict(at=5, text='「低かったのではなく、当時の平均くらいだった」と言うのが近い')]))]),
 ],
 desc=dict(title_main='ナポレオンは背が低かったのか', title_no=1,
  titles=['ナポレオンは、背が低かった？ 英語版Wikipediaと単位の計算で確かめる', 'ナポレオンの身長157cmの誤解：フランスの単位と英国の単位の違い', 'ナポレオンは本当に小柄だった？ 5ピエ2プースを計算してみた'],
  intro='「ナポレオンは背が低かった」「身長は157センチ」と聞いたことはありませんか。この動画では、英語版Wikipediaと解説記事、そして自分の計算で、確かめます。',
  points=['英語版Wikipediaによると、ナポレオンの身長はメートル法の前のフランスの単位で5ピエ2プースと推定され、約1.67メートル。一部の歴史家は1.70メートルとしています。同記事は、これを当時の成人男性の平均身長と述べています。', '157センチという数字は、フランスと英国の単位の違いによる読み違いだと説明されています。自作の計算では、5ピエ2プースは約168センチ、英国の5フィート2インチは約157センチです。', '小柄なイメージは、英国の風刺画家(ジェームズ・ギルレイなど)が広めたとされています(英語版Wikipedia)。'],
  refs=['Wikipedia(英語版)「Napoleon complex」:https://en.wikipedia.org/wiki/Napoleon_complex', 'Wikipedia(英語版)「Napoleon」:https://en.wikipedia.org/wiki/Napoleon', 'HowStuffWorks「How Tall Was Napoleon Bonaparte?」(二次情報):https://history.howstuffworks.com/history-vs-myth/napoleon-short.htm'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['身長の記録(5ピエ2プース)の原典や、死亡時の計測の記録は、確認できていません。', '「ピエ・プースの長さ」は、1ピエ約32.5cm、1プース約2.7cmという一般的な換算で、自作の計算です。', '背の高い護衛を周りに置いたため小さく見えた、という説明は、解説記事の二次情報で、裏付けとなる記録は確認できませんでした。'],
  tags='ナポレオン, 身長, 157cm, フランス, 風刺画, ギルレイ, 単位, 検証',
  checks=['ナポレオンの死亡時の身長の記録(原典)を確認する', '当時のフランス人男性の平均身長の根拠を確認する', '護衛の話の出どころを確認する']),
 thumb=dict(bg='assets/napoleon/thumb_art.png', lines=[['ナポレオンは', 90, 'white'], ['背が低い？', 125, 'gold']], sub='身長と単位を、計算で確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {'intro': 'intro', 'hyoki': 'ruler', 'tani': 'ruler', 'fuushi': 'print', 'end': 'island'}, art2={'fuushi': ('guard', 3)})
