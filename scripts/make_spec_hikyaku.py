"""Writes data/hikyaku_spec.json（江戸の手紙は、大坂まで何日で届いた？）。台本：docs/themes/20270127_hikyaku/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
spec = dict(slug='hikyaku', theme_dir='20270127_hikyaku', pack='59_hikyaku', header_sub='解説記事の説明を比べて、飛脚の日数と値段を確かめる',
 images={},
 bgm=[['intro', 'tsugi', 'piano36'], ['machi', 'ryokin', 'piano12'], ['moto', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='江戸の手紙は、大坂まで何日で届いた？', chapter_title='導入：江戸の手紙は、大坂まで何日で届いた？', opener='江戸の手紙は、大坂まで何日で届いた？', opener_until=1, scene=[
   dict(t='big', text='江戸の手紙は、大坂まで何日で届いた？', y=270, at=0, size=46, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='飛脚が走って運んだ、というイメージ', at=1, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：解説記事・百科事典の説明', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：公用で4〜5日。町の人の便は頼み方しだい、値段は大違い', at=4, size=32, col='gold')]),
 dict(key='tsugi', title='幕府の公用「継飛脚」', chapter_title='幕府の公用「継飛脚」', scene=[
   dict(t='panel', box=TOP, text='まず、幕府の公用の飛脚', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='継飛脚：幕府が、公用の書類を運ぶために使った', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='宿場ごとに人が代わり、引き継いで運んだ', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='百科事典：江戸〜大坂は、4日から5日', at=3, until=4, size=40, col='gold'),
   dict(t='panel', box=TOP, text='公用の制度。町の人が自由に使えるものではない', at=4, size=38)]),
 dict(key='machi', title='町の人の頼み方', chapter_title='町の人の頼み方', scene=[
   dict(t='panel', box=TOP, text='町の人が頼むのは、「町飛脚」', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='解説記事：頼み方は、いくつかあった', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='並便：出発日は不定。10日以内に届ける', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='幸便：出発日は決まっている。同じく10日以内', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='仕立便：5日、または最短2日で届けた', at=4, size=38, col='gold')]),
 dict(key='ryokin', title='値段は、どれだけ違うか', chapter_title='値段は、どれだけ違うか', scene=[
   dict(t='panel', box=TOP, text='気になるのは、値段', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='解説記事：並便は30文、幸便は60文', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='最短5日ほどの便は、1200文', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='1200 ÷ 30 ＝ 40倍（自作の計算）。5日ほどなら並便の40倍', at=3, until=4, size=34, col='gold'),
   dict(t='panel', box=TOP, text='仕立便：金3両。最短2日では14両という説明も', at=4, size=36),
   dict(t='table', box=[60, 300, 1860, 640], cols=['町飛脚（解説記事）', '値段'], colw=[1200, 600], size=32, rows=[
     dict(at=1, cells=['並便（10日以内）', '30文']),
     dict(at=1, cells=['幸便（10日以内）', '60文']),
     dict(at=2, cells=['最短5日ほどの便', '1200文（並便の40倍）'], col='gold'),
     dict(at=4, cells=['仕立便（5日／最短2日）', '金3両／14両'])])]),
 dict(key='moto', title='この数字の出どころ', chapter_title='この数字の出どころ', scene=[
   dict(t='panel', box=TOP, text='この数字は、どこから来ているのか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='料金の数字は、一般向けの解説記事（二次情報）', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='4〜5日は、百科事典の「公用の継飛脚」の説明', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='民間の便の、江戸〜大坂の実際の日数は、確認できず', at=3, until=4, size=36),
   dict(t='panel', box=TOP, text='時期や相手先で、値段も日数も違った可能性', at=4, size=38, col='gold')]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=1, items=[
      dict(at=1, text='公用の継飛脚は、江戸〜大坂が4〜5日とされる'),
      dict(at=2, text='町飛脚は並便で10日以内。5日ほどの便は並便の40倍'),
      dict(at=3, text='急ぐほど、値段が大きく上がった')]),
     right=dict(title='分からないこと・言い方', title_at=4, items=[
      dict(at=4, text='民間の実際の日数。原典の料金'),
      dict(at=4, text='「数日から10日ほどで届いたが、値段は大違い」と言うのが近い')]))]),
 ],
 desc=dict(title_main='江戸の手紙は大坂まで何日で届いたのか', title_no=1,
  titles=['江戸の手紙は、大坂まで何日で届いた？ 飛脚の日数と値段を確かめる', '江戸の飛脚、速い便は並便の40倍？ 継飛脚・町飛脚の違い', '江戸から大坂まで手紙は何日？ 並便30文と最短2日の仕立便'],
  intro='「江戸から大坂まで、手紙は何日で届いたのだろう」と思ったことはありませんか。この動画では、解説記事や百科事典の説明を比べて、飛脚の日数と値段を確かめます。',
  points=['百科事典の説明では、幕府の公用の「継飛脚」は、江戸と大坂のあいだが4〜5日とされています。', '解説記事によると、町飛脚の「並便」は出発日が不定で10日以内に届ける便、料金は30文。「幸便」は60文、最短5日ほどの便は1200文、「仕立便」は金3両(最短2日では14両)とされています。', '1200文は30文の40倍です(自作の計算)。急ぐほど、値段が大きく上がったことが分かります。'],
  refs=['財産ネット(Financial Field)「江戸時代の飛脚」の解説記事(二次情報):https://financial-field.com/income/entry-167307', '(百科事典)継飛脚の項。江戸〜大坂の所要日数4〜5日の記述(検索結果で確認した要約。原文は未確認)'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['料金の数字(30文、60文、1200文、金3両、14両)は、一般向けの解説記事の二次情報で、原典は確認できていません。', '4〜5日は公用の継飛脚の説明で、町飛脚の日数ではありません。', '民間の便が、江戸〜大坂を実際に何日で届けたかは、確認できていません。', '円換算は資料によって大きく違うため、扱っていません。'],
  tags='江戸時代, 飛脚, 継飛脚, 町飛脚, 手紙, 東海道, 江戸の暮らし, 検証',
  checks=['継飛脚の記述の原文を確認する', '町飛脚の日数・料金の出典(飛脚問屋の記録など)を確認する', '郵政博物館の飛脚の研究資料を確認する']),
 thumb=dict(bg='assets/hikyaku/thumb_art.png', lines=[['江戸の手紙は', 90, 'white'], ['何日で届く？', 115, 'gold']], sub='飛脚の日数と値段を、確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {'intro': 'intro', 'tsugi': 'road', 'machi': 'shop', 'ryokin': 'shop', 'moto': 'road', 'end': 'intro'})
