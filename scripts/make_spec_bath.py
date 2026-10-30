"""Writes data/bath_spec.json（江戸の銭湯は、そば一杯の半分の値段だった？）。台本：docs/themes/20270106_bath/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
spec = dict(slug='bath', theme_dir='20270106_bath', pack='56_bath', header_sub='解説記事の説明を比べて、江戸の銭湯の値段を確かめる',
 images={},
 bgm=[['intro', 'nedan', 'piano36'], ['soba', 'hagaki', 'piano12'], ['yen', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='江戸の銭湯は、そば一杯の半分の値段だった？', chapter_title='導入：江戸の銭湯は、そば一杯の半分の値段だった？', opener='江戸の銭湯は、そば一杯の半分の値段だった？', opener_until=1, scene=[
   dict(t='big', text='江戸の銭湯は、そば一杯の半分の値段だった？', y=270, at=0, size=44, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='今のお風呂代とは、感覚が違いそう', at=1, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：解説記事の説明', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：大人6文ほど。そばの約4割。時期や資料で幅がある', at=4, size=34, col='gold')]),
 dict(key='nedan', title='入浴料は、いくらだったのか', chapter_title='入浴料は、いくらだったのか', scene=[
   dict(t='panel', box=TOP, text='まず、銭湯の入浴料を見る', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='解説記事：江戸時代の初めの入浴料は、永楽銭1文', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='終わりごろ『洗湯手引草』の「湯屋万歳暦」：6文ほど', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='別の解説：大人6文、子供4文。寛永のころから約150年、ほぼ同じ', at=3, until=4, size=34),
   dict(t='panel', box=TOP, text='一方、1794年に大人10文とする説明もあり、資料で幅がある', at=4, size=36, col='gold'),
   dict(t='table', box=[60, 300, 1860, 640], cols=['入浴料（解説記事）', '値段'], colw=[1200, 600], size=32, rows=[
     dict(at=1, cells=['江戸時代の初め', '永楽銭1文']),
     dict(at=2, cells=['終わりごろ（湯屋万歳暦）', '6文ほど'], col='gold'),
     dict(at=3, cells=['別の解説（大人／子供）', '6文／4文']),
     dict(at=4, cells=['1794年（別の解説）', '大人10文'])])]),
 dict(key='soba', title='そばと比べる', chapter_title='そばと比べる', scene=[
   dict(t='panel', box=TOP, text='では、そばと比べてみる', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='ある解説：かけそば1杯は、16文', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='6 ÷ 16 ＝ 約0.4。そばの約4割（自作の計算）', at=2, until=3, size=38, col='gold'),
   dict(t='panel', box=TOP, text='「半分」というより、半分より少し安い、が近い', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='ただし、そばの16文は、元の史料を確認できていない', at=4, size=38),
   dict(t='table', box=[60, 300, 1860, 560], cols=['比べる（解説記事）', '値段'], colw=[1200, 600], size=34, rows=[
     dict(at=1, cells=['かけそば1杯', '16文']),
     dict(at=2, cells=['銭湯・大人', '6文（そばの約4割）'], col='gold')])]),
 dict(key='hagaki', title='月ぎめの「羽書」', chapter_title='月ぎめの「羽書」', scene=[
   dict(t='panel', box=TOP, text='もう一つ、面白い仕組みがある', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='「羽書」：1か月のフリーパス。『守貞謾稿』では148文前後', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='1回6文なら、25回入ると約150文（自作の計算）', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='月に25回以上入る人には、羽書のほうが得', at=3, until=4, size=40, col='gold'),
   dict(t='panel', box=TOP, text='毎日のように通う人が、多かったことを思わせる', at=4, size=38)]),
 dict(key='yen', title='円に直すと、いくらか', chapter_title='円に直すと、いくらか', scene=[
   dict(t='panel', box=TOP, text='気になるのは、今のお金でいくらか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='解説記事：1文を約30円とするもの、6文を約150円とするものなど、ばらばら', at=1, until=2, size=30, hi=True),
   dict(t='panel', box=TOP, text='時代で物価が違い、円換算はあくまで目安', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='この動画では、円に直さず、「そばの何割か」で比べる', at=3, size=38, col='gold')]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=1, items=[
      dict(at=1, text='入浴料は、大人6文ほどとする説明が多い。時期や資料で幅がある'),
      dict(at=2, text='そば1杯を16文とすると、6文は約4割'),
      dict(at=3, text='月ぎめの羽書は148文前後。25回以上入る人に得')]),
     right=dict(title='分からないこと・言い方', title_at=4, items=[
      dict(at=4, text='そばの値段の元の史料。時期ごとの正確な値段'),
      dict(at=4, text='「半分より少し安かったとされる」と言うのが近い')]))]),
 ],
 desc=dict(title_main='江戸の銭湯はそば一杯の半分の値段だったのか', title_no=1,
  titles=['江戸の銭湯は、そば一杯の半分の値段だった？ 解説記事の数字を比べて確かめる', '江戸の銭湯は何文？ そばとの比較と、月ぎめ「羽書」の損得を計算', '江戸時代のお風呂代はいくら？ 6文・16文・148文を調べてみた'],
  intro='「江戸の銭湯は、そば一杯の半分ほどの値段だった」と聞いたことはありませんか。この動画では、解説記事の説明を比べて、入浴料とそばの値段、月ぎめの「羽書」を確かめます。',
  points=['解説記事によると、江戸時代の初めの入浴料は永楽銭1文、終わりごろは『洗湯手引草』の「湯屋万歳暦」で6文ほどです。別の解説は、大人6文・子供4文が寛永のころから約150年ほぼ変わらなかったとしています。', 'ある解説は、かけそば1杯を16文としています。6文は16文の約4割です(自作の計算)。', '『守貞謾稿』によると、月ぎめの「羽書」は148文前後です。1回6文なら25回入ると約150文で、月に25回以上入る人には得、という計算です(自作)。'],
  refs=['住まいの情報「銭湯の歴史を調べてみた」(LIFULL HOME\'S・二次情報):https://www.homes.co.jp/cont/press/reform/reform_01245/', '歌舞伎美人「湯屋は庶民の大事な社交場」(二次情報):https://www.kabuki-bito.jp/special/knowledge/tepco-life/post-life-22/2/', '「江戸時代の銭湯はどれくらい通った？」(個人サイト・出典の記載なし):https://history.wild-g.com/edo-bath-culture-frequency-price/'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['入浴料の数字(1文、6文、10文)、かけそば16文、羽書148文は、解説記事の二次情報で、『守貞謾稿』『洗湯手引草』などの原典は確認できていません。', '「かけそば1杯16文」は、出典の史料を確認できていません。', '1794年に大人10文とする説明は、検索で見つかった解説の記述で、出典は未確認です。', '円換算は資料によって大きく違うため、扱っていません。'],
  tags='江戸時代, 銭湯, 湯屋, 入浴料, そば, 羽書, 守貞謾稿, 江戸の暮らし, 検証',
  checks=['『守貞謾稿』の入浴料と羽書の記述を確認する', 'かけそば1杯の値段の出典を確認する', '時期ごとの入浴料の変化を、史料で確認する']),
 thumb=dict(bg='assets/bath/thumb_art.png', lines=[['江戸の銭湯は', 90, 'white'], ['そばの半額？', 115, 'gold']], sub='6文と16文を、計算で確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {'intro': 'intro', 'nedan': 'bath', 'soba': 'soba', 'hagaki': 'coins', 'yen': 'coins', 'end': 'intro'})
