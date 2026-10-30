"""Writes data/nukemairi_spec.json（抜け参り）。台本：docs/themes/20270407_nukemairi/09_script_v2.md
at / until は『章内の行番号（0始まり）』。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
spec = dict(slug='nukemairi', theme_dir='20270407_nukemairi', pack='69_nukemairi', header_sub='各地の資料で、抜け参りの旅を確かめる',
 images={},
 bgm=[['intro', 'nuke', 'piano36'], ['dogu', 'kodomo', 'piano12'], ['wakaranai', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='子どもが黙って伊勢参りに出かけても、許された？', chapter_title='導入：子どもが黙って伊勢参りに出かけても、許された？', opener='江戸時代、子どもが黙って伊勢参りに出かけても、許された？', opener_until=1, scene=[
   dict(t='big', text='黙って伊勢参りに出ても、許された？', y=270, at=0, size=44, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='「抜け参り」と呼ばれた旅の話', at=1, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：各地の資料の説明', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：道中は施しで旅ができたが、お咎めの有無は確認できず', at=4, size=30, col='gold')]),
 dict(key='nuke', title='抜け参り', chapter_title='抜け参り', scene=[
   dict(t='panel', box=TOP, text='まず、抜け参りとは', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='奈良市の資料：許可も旅行手形もなく出た参宮者がいた', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='大流行：1650・1705・1771・1830年が特に大きい', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='百科事典：1771年は200万人を超えた', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='ただし、その数字の原典は未確認', at=4, size=40, col='gold')]),
 dict(key='dogu', title='旅の道具', chapter_title='旅の道具', scene=[
   dict(t='panel', box=TOP, text='手形も許可もない旅は、どうしたか', at=0, until=1, size=38),
   dict(t='panel', box=TOP, text='柄杓を差し出して、食べ物などの施しを求めた', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='道中の町々が、食事や宿の世話をした（施行）', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='生駒市：1830年に俵口村の文七が持った柄杓', at=3, until=4, size=36),
   dict(t='panel', box=TOP, text='底に「閏三月二日」と書かれている', at=4, size=40, col='gold')]),
 dict(key='kodomo', title='子どもたち', chapter_title='子どもたち', scene=[
   dict(t='panel', box=TOP, text='子どもも、出かけたのか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='静岡県の資料：『文政神異記』の記述を紹介', at=1, until=2, size=36, hi=True),
   dict(t='panel', box=TOP, text='1830年、徳島の手習屋の子ども20〜30人が、3月20日に出発', at=2, until=3, size=32),
   dict(t='panel', box=TOP, text='親や主人の許しなく出かけられた点も、記されている', at=3, until=4, size=34),
   dict(t='panel', box=TOP, text='ただし、帰ってから叱られたかは、分からなかった', at=4, size=36, col='gold'),
   dict(t='table', box=[60, 300, 1860, 640], cols=['1830年の子どもたち（資料の紹介）', '内容'], colw=[1000, 800], size=30, rows=[
     dict(at=2, cells=['出発した人数', '20〜30人（徳島の手習屋）']),
     dict(at=2, cells=['出発の日', '3月20日']),
     dict(at=4, cells=['帰ってからの扱い', '確認できず'], col='gold')])]),
 dict(key='wakaranai', title='分からないこと', chapter_title='分からないこと', scene=[
   dict(t='panel', box=TOP, text='分からないことも、整理する', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='1830年の参宮者の総数は、確認できなかった', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='「黙って出られた」と「咎められなかった」は、別の話', at=2, until=3, size=34),
   dict(t='panel', box=TOP, text='資料は、道中で施しを受けられた様子を伝える', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='帰ってからの扱いは、別の資料を見る必要がある', at=4, size=36, col='gold')]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=1, items=[
      dict(at=1, text='許可や手形がなくても出かけ、柄杓で施しを受けた'),
      dict(at=2, text='1830年に、徳島の子ども20〜30人が一緒に出発したという紹介'),
      dict(at=3, text='道中の町々が、食事や宿の世話をした')]),
     right=dict(title='分からないこと・言い方', title_at=4, items=[
      dict(at=4, text='帰ってから咎められたか。1830年の総人数'),
      dict(at=4, text='「道中は施しで旅ができたが、お咎めの有無は確認できない」と言うのが近い')]))]),
 ],
 desc=dict(title_main='江戸時代、子どもが黙って伊勢参りに出かけても許されたのか', title_no=1,
  titles=['子どもが黙って伊勢参り？ 抜け参りは許された？ 各地の資料で確かめる', '抜け参りの柄杓と施行 江戸の伊勢参りの不思議', '1830年、徳島の子ども20〜30人が伊勢へ 抜け参りを確かめる'],
  intro='「江戸時代、子どもが黙って伊勢参りに出かけても、許された」と聞いたことはありませんか。この動画では、各地の資料の説明で、抜け参りの旅の様子を確かめます。',
  points=['奈良市の資料によると、許可を得ず、旅行手形も持たずに出た参宮者は、柄杓を差し出して食べ物などの施しを求め、道中の町々は食事や宿の世話をしました。', '静岡県の資料は、『文政神異記』の記述として、1830年に徳島の手習屋にいた子ども20〜30人が3月20日に一緒に出発したことを紹介しています。親や主人の許しなく出かけられた点も記されているとのことです。', '帰ってから咎められたか、1830年の総数は、今回の資料では確認できていません。'],
  refs=['奈良市の資料(PDF・二次情報):https://www.city.nara.lg.jp/uploaded/attachment/120904.pdf', '静岡県立図書館の資料(PDF・二次情報):https://www.tosyokan.pref.shizuoka.jp/data/open/cnt/3/50/1/ssr3-41.pdf', 'Encyclopedia of Shinto「お蔭参り」(二次情報):https://d-museum.kokugakuin.ac.jp/eos/detail/?id=8686'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['検索結果の要約をもとにしており、資料の全文は確認していません。奈良市のPDFは本文を読み取れませんでした。', '1771年に200万人を超えた、という数字は百科事典の記述で、原典は未確認です。', '帰ってから咎められたか、1830年の総数は確認できていません。「咎められなかった」とも「咎められた」とも断定していません。'],
  tags='江戸時代, 抜け参り, 伊勢参り, おかげ参り, 江戸の暮らし, 検証',
  checks=['奈良市の資料の本文を確認する', '『文政神異記』の原文を確認する', '抜け参りの帰郷後の扱いを確認する']),
 thumb=dict(bg='assets/nukemairi/thumb_art.png', lines=[['黙って伊勢参り', 84, 'white'], ['許された？', 110, 'gold']], sub='各地の資料で、確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {'intro': 'intro', 'nuke': 'road', 'dogu': 'ladle', 'kodomo': 'road', 'wakaranai': 'ladle', 'end': 'intro'})
