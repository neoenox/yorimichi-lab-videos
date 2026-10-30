"""Writes data/twomeals_spec.json（江戸時代の人は、1日2食だった？）。台本：docs/themes/20270227_twomeals/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
spec = dict(slug='twomeals', theme_dir='20270227_twomeals', pack='50_twomeals', header_sub='農林水産省の説明と解説記事で、江戸の食事の回数を確かめる',
 images={},
 bgm=[['intro', 'nouhou', 'piano36'], ['genroku', 'chiiki', 'piano12'], ['taika', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='江戸時代の人は、1日2食だった？', chapter_title='導入：江戸時代の人は、1日2食だった？', opener='江戸時代の人は、1日2食だった？', opener_until=1, scene=[
   dict(t='big', text='江戸時代の人は、1日2食だった？', y=270, at=0, size=50, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='今は、朝・昼・夕の3食が当たり前', at=0, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：農林水産省の説明と、解説記事', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：江戸の中ごろから3食に広がった、とされる。それ以前は2食が中心という説明が多い', at=4, size=30, col='gold')]),
 dict(key='nouhou', title='農林水産省は、どう説明しているか', chapter_title='農林水産省は、どう説明しているか', scene=[
   dict(t='panel', box=TOP, text='まず、公的な機関の説明を見る', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='農林水産省：江戸時代の中ごろから、朝・昼・夕の1日3食になった、といわれている', at=1, until=2, size=32, hi=True),
   dict(t='panel', box=TOP, text='理由：あんどん（あかり）が使われ、夜の活動時間が長くなり、おなかがすくようになったから', at=2, until=3, size=30),
   dict(t='panel', box=TOP, text='「江戸時代の中ごろから」。江戸時代の全体が2食だった、とは言っていない', at=3, until=4, size=34, col='gold'),
   dict(t='panel', box=TOP, text='「といわれている」。はっきりした年を示した説明ではない', at=4, size=38)]),
 dict(key='genroku', title='「元禄」という説明', chapter_title='「元禄」という説明', scene=[
   dict(t='panel', box=TOP, text='解説記事には、もう少し具体的な説明がある（二次情報）', at=0, until=1, size=38),
   dict(t='panel', box=TOP, text='3食が定着したのは、元禄期（1688〜1704年）以降（ある記事）', at=1, until=2, size=36, hi=True),
   dict(t='panel', box=TOP, text='元禄の前は、産業の生産性が低く、流通も盛んでなかったため、1日2食が普通だった', at=2, until=3, size=30),
   dict(t='panel', box=TOP, text='別の記事：元禄〜享保のころは2食が中心。その後、照明器具の普及などで3食に', at=3, until=4, size=30),
   dict(t='panel', box=TOP, text='農林水産省は「中ごろ」、記事は「元禄以降」。説明には幅がある', at=4, until=5, size=34, col='gold'),
   dict(t='panel', box=TOP, text='いずれも解説記事。原典の史料は、この動画では未確認', at=5, size=38),
   dict(t='table', box=[60, 300, 1860, 560], cols=['説明の出どころ', '3食になった時期'], colw=[1000, 800], size=34, rows=[
     dict(at=1, cells=['農林水産省', '江戸時代の中ごろから']),
     dict(at=1, cells=['解説記事（ある記事）', '元禄期（1688〜1704年）以降'], col='gold'),
     dict(at=3, cells=['別の記事', '元禄〜享保のあと'])])]),
 dict(key='chiiki', title='地域で、違った', chapter_title='地域で、違った', scene=[
   dict(t='panel', box=TOP, text='同じ江戸時代でも、地域で食事の習慣は違ったようだ', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='江戸：朝に1日分のご飯をまとめて炊き、昼は冷めたご飯で済ませるのが一般的（記事）', at=1, until=2, size=30, hi=True),
   dict(t='panel', box=TOP, text='京阪神：昼食が重視されていた、とされる（記事）', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='「江戸は2食」「江戸は3食」と、1つに言い切るのは難しい', at=3, size=38, col='gold'),
   dict(t='table', box=[60, 300, 1860, 560], cols=['地域（記事の説明）', '食事の習慣'], colw=[600, 1200], size=34, rows=[
     dict(at=1, cells=['江戸', '朝にまとめて炊き、昼は冷めたご飯'], col='gold'),
     dict(at=2, cells=['京阪神', '昼食が重視された'])])]),
 dict(key='taika', title='大火の復興が理由？', chapter_title='大火の復興が理由？', scene=[
   dict(t='panel', box=TOP, text='食事の回数が増えた理由として、「大火からの復興」を挙げる記事もある', at=0, until=1, size=32, hi=True),
   dict(t='panel', box=TOP, text='復興で働く職人に昼ご飯を出したのが、広まるきっかけ、という話', at=1, until=2, size=36),
   dict(t='panel', box=TOP, text='ただし、どの大火か、裏付ける記録は、今回の資料では見つからなかった', at=2, until=3, size=32, col='gold'),
   dict(t='panel', box=TOP, text='この動画では、「そういう説明もある」という紹介にとどめる', at=3, size=38)]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=1, items=[
      dict(at=1, text='農林水産省：江戸時代の中ごろから、朝・昼・夕の3食になったといわれている'),
      dict(at=2, text='記事の多くは、元禄期以降に定着。それより前は2食が中心'),
      dict(at=3, text='時期には幅があり、江戸と京阪神など、地域でも違った')]),
     right=dict(title='分からないこと・言い方', title_at=4, items=[
      dict(at=4, text='はっきりした年。大火と食事の回数の関係'),
      dict(at=5, text='「江戸時代の前半は、2食が中心だったとされる」と言うのが近い')]))]),
 ],
 desc=dict(title_main='江戸時代の人は1日2食だったのか', title_no=1,
  titles=['江戸時代の人は、1日2食だった？ 農林水産省の説明と解説記事で確かめる', '江戸時代は1日2食？ 3食になった時期と理由：元禄・あんどん・地域差', '1日3食はいつから？ 江戸時代の食事の回数を調べてみた'],
  intro='「江戸時代の人は、1日2食だった」と聞いたことはありませんか。この動画では、農林水産省の説明と解説記事で、3食になった時期と理由を確かめます。',
  points=['農林水産省の子ども向けページは、江戸時代の中ごろから、朝・昼・夕の1日3食になったといわれている、と説明しています。理由は、あんどんが使われて夜の活動時間が長くなったためとされています。', '解説記事の多くは、3食の定着を元禄期(1688〜1704年)以降としています。時期には説明の幅があります。', '江戸では朝に1日分を炊いて昼は冷めたご飯、京阪神では昼食が重視された、と記事は説明しています。', '「大火の復興が理由」という説明もありますが、裏付ける記録は確認できませんでした。'],
  refs=['農林水産省「食育 子ども向けページ(1日の食事クイズ)」:https://www.maff.go.jp/j/syokuiku/kodomo_navi/oneday/quiz_a1.html', '車浮代「江戸の食事の回数」解説記事(serai.jp・二次情報):https://serai.jp/hobby/1047048', '和楽web(Into Japan Waraku)・江戸の食の解説(二次情報):https://intojapanwaraku.com/rock/culture-rock/35878/2/'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['元禄期以降という説明、江戸と京阪神の違い、大火の話は、解説記事の二次情報で、原典の史料は確認できていません。', '「大火からの復興」と食事の回数の関係は、裏付けとなる記録を確認できませんでした。'],
  tags='江戸時代, 1日3食, 1日2食, 食事, 元禄, あんどん, 江戸の暮らし, 検証',
  checks=['江戸時代の食事の回数について、食文化史の専門書で原典と年代を確認する', '「大火からの復興」説の出どころ(どの大火か)を確認する']),
 thumb=dict(bg='assets/twomeals/thumb_art.png', lines=[['江戸の人は', 95, 'white'], ['1日2食？', 125, 'gold']], sub='農水省の説明と解説記事で確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {'intro': 'intro', 'nouhou': 'lamp', 'genroku': 'lamp', 'chiiki': 'kitchen', 'taika': 'craft', 'end': 'intro'})
