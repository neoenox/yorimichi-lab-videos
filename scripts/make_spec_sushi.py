"""Writes data/sushi_spec.json（江戸の握り寿司は、屋台のファストフードだった？）。台本：docs/themes/20270224_sushi/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
spec = dict(slug='sushi', theme_dir='20270224_sushi', pack='63_sushi', header_sub='『守貞謾稿』を紹介する解説記事で、握り寿司の始まりを確かめる',
 images={},
 bgm=[['intro', 'oshi', 'piano36'], ['yatai', 'nedan', 'piano12'], ['moto', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='江戸の握り寿司は、屋台のファストフードだった？', chapter_title='導入：江戸の握り寿司は、屋台のファストフードだった？', opener='江戸の握り寿司は、屋台のファストフードだった？', opener_until=1, scene=[
   dict(t='big', text='江戸の握り寿司は、屋台のファストフードだった？', y=270, at=0, size=40, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='今の高級なイメージとは、ずいぶん違う', at=1, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：『守貞謾稿』を紹介する解説記事', at=3, size=36),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：屋台で手軽に売られていた、とされる', at=4, size=38, col='gold')]),
 dict(key='oshi', title='押し寿司から握りへ', chapter_title='押し寿司から握りへ', scene=[
   dict(t='panel', box=TOP, text='まず、握り寿司の始まり', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='江戸・京都・大坂の三都では、もともと押し寿司が主流', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='『守貞謾稿』：江戸では箱鮓が廃れ、握り鮓だけになった', at=2, until=3, size=34),
   dict(t='panel', box=TOP, text='考案は与兵衛とされ、文政の初め（1819年ごろ）', at=3, until=4, size=36),
   dict(t='panel', box=TOP, text='守貞：名があるのは、東両国元町の与兵衛鮓', at=4, size=38, col='gold')]),
 dict(key='yatai', title='屋台と売り方', chapter_title='屋台と売り方', scene=[
   dict(t='panel', box=TOP, text='次に、売り方', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='守貞：屋台見世は、鮓と天麩羅を専らとする', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='夜の人通りが多い所では、町ごとに3、4軒', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='与兵衛：岡持ちで売り歩き→屋台→1824年に東両国で店', at=3, until=4, size=32),
   dict(t='panel', box=TOP, text='狭い町人地では、手軽な屋台が多かった', at=4, size=38, col='gold')]),
 dict(key='nedan', title='値段とネタ', chapter_title='値段とネタ', scene=[
   dict(t='panel', box=TOP, text='気になるのは、値段とネタ', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='解説記事：握り1貫は、8文', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='玉子焼は16文。卵が高価だったため', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='かけそば16文とする説明と比べると、握り2つでそば1杯ほど', at=3, until=4, size=32, col='gold'),
   dict(t='panel', box=TOP, text='ネタ：玉子焼・白魚・マグロの刺身・コハダ・アナゴ・海老', at=4, size=34),
   dict(t='table', box=[60, 300, 1860, 640], cols=['値段（解説記事）', '文'], colw=[1200, 600], size=32, rows=[
     dict(at=1, cells=['握り1貫', '8文']),
     dict(at=2, cells=['玉子焼', '16文']),
     dict(at=3, cells=['かけそば1杯（別の説明）', '16文'], col='gold')])]),
 dict(key='moto', title='ファストフードと言えるか', chapter_title='ファストフードと言えるか', scene=[
   dict(t='panel', box=TOP, text='「ファストフード」と言ってよいか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='屋台で手軽に買えて、すぐ食べられた点は、解説と合う', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='一個の大きさは、今回の記事に寸法の記載がない', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='8文・16文は、記事の紹介。原文は確認できず', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='円換算は、記事で違うため、扱わない', at=4, size=40, col='gold')]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=1, items=[
      dict(at=1, text='江戸では押し寿司が廃れ、握り寿司だけになった（守貞）'),
      dict(at=2, text='屋台でも売られ、握り1貫は8文とする説明'),
      dict(at=3, text='岡持ち→屋台→店、という広がり方の紹介')]),
     right=dict(title='分からないこと・言い方', title_at=4, items=[
      dict(at=4, text='一個の大きさ。原文の値段'),
      dict(at=4, text='「屋台の、手軽な食べ物だった」と言うのが近い')]))]),
 ],
 desc=dict(title_main='江戸の握り寿司は屋台のファストフードだったのか', title_no=1,
  titles=['江戸の握り寿司は、屋台のファストフードだった？ 『守貞謾稿』の紹介記事で確かめる', '握り寿司は一貫8文？ 江戸の屋台と与兵衛鮓', '江戸の寿司は押し寿司から握りへ 屋台での売られ方'],
  intro='「江戸の握り寿司は、屋台で食べる、ファストフードだった」と聞いたことはありませんか。この動画では、『守貞謾稿』を紹介する解説記事で、握り寿司の始まりと、売られ方を確かめます。',
  points=['nippon.comの解説記事によると、江戸では押し寿司(箱鮓)が廃れ、握り鮓だけになった、と『守貞謾稿』にあります。考案者は与兵衛とされ、文政の初め(1819年ごろ)です。', '『守貞謾稿』は、屋台見世は鮓と天麩羅を専らとする、と記しています。夜の人通りが多い所では、町ごとに3、4軒あったとされます。', '解説記事では、握り1貫が8文、玉子焼が16文です。かけそば1杯を16文とする説明と比べると、握り2つでそば1杯ほどです(自作の比較)。'],
  refs=['nippon.com「寿司は江戸の昔からお手軽ファストフードだった:『守貞漫稿』(その3)」(二次情報):https://www.nippon.com/ja/japan-topics/g00962/'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['握り1貫8文、玉子焼16文、考案の年などは、解説記事の紹介で、『守貞謾稿』の原文は確認できていません。', '握り寿司の一個の大きさは、今回の記事に寸法の記載がなく、確認できていません。', '考案者は、記事では「小泉与兵衛」「華屋与兵衛」などの表記があり、この動画では「与兵衛」としました。', 'かけそば16文は、別の解説の数字で、出典は未確認です。円換算は扱っていません。'],
  tags='江戸時代, 握り寿司, 寿司, 屋台, 守貞謾稿, 与兵衛, 江戸の暮らし, 検証',
  checks=['『守貞謾稿』の鮓の項の原文を確認する', '握り寿司の大きさの記録を確認する', '与兵衛の表記(華屋・小泉)の違いを確認する']),
 thumb=dict(bg='assets/sushi/thumb_art.png', lines=[['江戸の握り寿司', 84, 'white'], ['屋台の軽食？', 110, 'gold']], sub='守貞謾稿の紹介記事で、確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {'intro': 'intro', 'oshi': 'stall', 'yatai': 'stall', 'nedan': 'sushi', 'moto': 'sushi', 'end': 'intro'})
