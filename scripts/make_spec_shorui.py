"""Writes data/shorui_spec.json（生類憐みの令では、犬を殺すと死刑だった？）。台本：docs/themes/20270303_shorui/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
spec = dict(slug='shorui', theme_dir='20270303_shorui', pack='64_shorui', header_sub='解説記事の説明で、生類憐みの令の処罰を確かめる',
 images={},
 bgm=[['intro', 'rei', 'piano36'], ['batsu', 'mokuteki', 'piano12'], ['moto', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='生類憐みの令では、犬を殺すと死刑だった？', chapter_title='導入：生類憐みの令では、犬を殺すと死刑だった？', opener='生類憐みの令では、犬を殺すと死刑だった？', opener_until=1, scene=[
   dict(t='big', text='生類憐みの令では、犬を殺すと死刑だった？', y=270, at=0, size=44, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='犬公方・徳川綱吉の法令', at=1, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：解説記事の説明', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：厳罰の例はあるが、犬殺しで死刑の事例は未確認', at=4, size=32, col='gold')]),
 dict(key='rei', title='令の中身', chapter_title='令の中身', scene=[
   dict(t='panel', box=TOP, text='まず、令の中身', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='解説記事：最初の発布は、1685年（貞享2年）', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='その後24年間で、100回以上のお触れ', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='対象は、犬・猫・鳥・魚・貝・虫など、多岐にわたった', at=3, until=4, size=36),
   dict(t='panel', box=TOP, text='捨て子や、捨てられた老人を禁じる内容も含まれた', at=4, size=36, col='gold')]),
 dict(key='batsu', title='処罰の例', chapter_title='処罰の例', scene=[
   dict(t='panel', box=TOP, text='気になるのは、処罰', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='解説記事：鶏を射殺した家来は、死罪', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='子犬を捨てた者は、市中引き回しのうえ獄門', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='厳しい処罰があったことは、確かなようだ', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='ただし、これらは犬を殺した例ではない', at=4, size=40, col='gold'),
   dict(t='table', box=[60, 300, 1860, 640], cols=['処罰の例（解説記事）', '処罰'], colw=[1200, 600], size=32, rows=[
     dict(at=1, cells=['鶏を射殺した家来', '死罪']),
     dict(at=2, cells=['子犬を捨てた者', '引き回しのうえ獄門']),
     dict(at=4, cells=['犬を殺した人', '事例は確認できず'], col='gold')])]),
 dict(key='mokuteki', title='なぜ、出されたのか', chapter_title='なぜ、出されたのか', scene=[
   dict(t='panel', box=TOP, text='なぜ、こんな令が出たのか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='説：世継ぎに恵まれないのは殺生の報い。綱吉は戌年生まれ', at=1, until=2, size=32, hi=True),
   dict(t='panel', box=TOP, text='ただし、この説は、信憑性が低いと記事は述べる', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='背景：人を生き物の最上位に置く、儒学の思想', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='生活のための漁師や猟師の仕事は、認められていた', at=4, size=36, col='gold')]),
 dict(key='moto', title='綱吉の死後と、確認できないこと', chapter_title='綱吉の死後と、確認できないこと', scene=[
   dict(t='panel', box=TOP, text='綱吉の死後は、どうなったか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='解説記事：法令は、ただちに撤回された', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='捨て子や捨て馬の禁止など、一部は受け継がれた', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='犬小屋の規模や費用の数字は、確認できず', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='犬を殺した人の処罰の記録も、確認できず', at=4, size=38, col='gold')]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=1, items=[
      dict(at=1, text='1685年から100回以上。動物と、捨て子などを守る内容'),
      dict(at=2, text='鶏の射殺は死罪、子犬の遺棄は獄門などの例'),
      dict(at=3, text='綱吉の死後、ただちに撤回。一部は継承')]),
     right=dict(title='分からないこと・言い方', title_at=4, items=[
      dict(at=4, text='犬を殺して死刑になった事例。犬小屋の規模と費用'),
      dict(at=4, text='「厳罰の例はあるが、犬殺しで死刑の事例は未確認」と言うのが近い')]))]),
 ],
 desc=dict(title_main='生類憐みの令では犬を殺すと死刑だったのか', title_no=1,
  titles=['生類憐みの令では、犬を殺すと死刑だった？ 解説記事の処罰の例で確かめる', '生類憐みの令の処罰 鶏の射殺は死罪、子犬を捨てると獄門', '生類憐みの令は何のため？ 24年間で100回以上のお触れ'],
  intro='「生類憐みの令では、犬を殺すと死刑になった」と聞いたことはありませんか。この動画では、解説記事の説明で、令の中身と処罰の例を確かめます。',
  points=['解説記事によると、生類憐みの令の最初の発布は1685年(貞享2年)で、以後24年間で100回以上のお触れが出ました。対象は犬だけでなく、猫、鳥、魚、貝、虫など、捨て子や捨てられた老人の禁止も含まれました。', '処罰の例として、鶏を射殺した家来が死罪になったこと、子犬を捨てた者が市中引き回しのうえ獄門になったことが挙げられています。ただし、犬を殺して死刑になった事例は、今回確認できていません。', '綱吉の死後、法令はただちに撤回されましたが、捨て子や捨て馬の禁止など一部は受け継がれた、とされます。'],
  refs=['解説記事「生類憐みの令」(Into JAPAN WARAKU・二次情報):https://intojapanwaraku.com/culture/107005/', '根崎光男『生類をめぐる政治』(講談社学術文庫。検索結果で参考文献として確認。原文は未確認)'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['処罰の例(鶏の射殺は死罪、子犬の遺棄は獄門)は、解説記事の紹介で、原典の記録は確認できていません。', '犬を殺した人が死刑になった事例は、今回の資料では確認できていません。「なかった」と断定するものではありません。', '犬小屋(中野など)の規模・費用の数字は、確認できていません。', '令が出た理由の「世継ぎ・戌年」説は、記事が信憑性が低いと述べる説として紹介しました。'],
  tags='江戸時代, 生類憐みの令, 徳川綱吉, 犬公方, 江戸の暮らし, 検証',
  checks=['犬を殺した者の処罰の記録を確認する', '中野の犬小屋の規模と費用を確認する', '根崎光男『生類をめぐる政治』を確認する']),
 thumb=dict(bg='assets/shorui/thumb_art.png', lines=[['犬を殺すと死刑？', 84, 'white'], ['生類憐みの令', 105, 'gold']], sub='解説記事の処罰の例で、確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {'intro': 'intro', 'rei': 'dogs', 'batsu': 'board', 'mokuteki': 'board', 'moto': 'dogs', 'end': 'intro'})
