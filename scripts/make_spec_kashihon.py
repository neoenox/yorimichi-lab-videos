"""Writes data/kashihon_spec.json（貸本屋）。台本：docs/themes/20270414_kashihon/09_script_v2.md
at / until は『章内の行番号（0始まり）』。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
spec = dict(slug='kashihon', theme_dir='20270414_kashihon', pack='70_kashihon', header_sub='辞書と解説記事で、貸本屋の実態を確かめる',
 images={},
 bgm=[['intro', 'toha', 'piano36'], ['kazu', 'nedan', 'piano12'], ['naka', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='庶民は、本を買わず貸本屋で借りていた？', chapter_title='導入：庶民は、本を買わず貸本屋で借りていた？', opener='江戸の庶民は、本を買わず、貸本屋で借りて読んでいた？', opener_until=1, scene=[
   dict(t='big', text='江戸の庶民は、本を借りて読んでいた？', y=270, at=0, size=44, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='背中に本を背負って、家々を回る商売', at=1, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：辞書と解説記事', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：広く行われたが、庶民のどれほどかは未確認', at=4, size=34, col='gold')]),
 dict(key='toha', title='貸本屋とは', chapter_title='貸本屋とは', scene=[
   dict(t='panel', box=TOP, text='まず、貸本屋とは', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='辞書：料金を取って本を貸す職業', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='読本や草双紙を大風呂敷に包み、得意先を貸し歩いた', at=2, until=3, size=34),
   dict(t='panel', box=TOP, text='寛永年間以降、行商の本屋が兼ねて始めたとみられる', at=3, until=4, size=34),
   dict(t='panel', box=TOP, text='店を構える貸本屋も、街頭の行商もいた', at=4, size=38, col='gold')]),
 dict(key='kazu', title='数', chapter_title='数', scene=[
   dict(t='panel', box=TOP, text='気になるのは、数', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='解説：1808年の江戸に、少なくとも656軒', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='天保のころ『江戸繁昌記』では、800軒とされる', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='一軒あたりの得意先は、170〜180軒ほど', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='江戸全体で、10万軒ほどの読者という推定', at=4, size=38, col='gold'),
   dict(t='table', box=[60, 300, 1860, 640], cols=['江戸の貸本屋（解説の紹介）', '数'], colw=[1200, 600], size=32, rows=[
     dict(at=1, cells=['1808年（文化5年）', '少なくとも656軒']),
     dict(at=2, cells=['天保のころ（江戸繁昌記）', '800軒']),
     dict(at=3, cells=['一軒の得意先', '170〜180軒ほど'], col='gold')])]),
 dict(key='nedan', title='値段', chapter_title='値段', scene=[
   dict(t='panel', box=TOP, text='借りるのは、安かったのか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='研究者の池上英子さん：貸す料金は、買う値段の約6分の1', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='薄い黄表紙は、1冊16文より安かったとも紹介', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='貸本料の具体的な金額は、確認できず', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='値段は、地域や貸本屋で大きく違ったとされる', at=4, size=36, col='gold')]),
 dict(key='naka', title='本の中身', chapter_title='本の中身', scene=[
   dict(t='panel', box=TOP, text='どんな本が、貸されたのか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='辞書：読本や草双紙', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='解説：薄手の黄表紙', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='本の見返しなどに、貸本屋の印が押されていた', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='「本が高価だったから重宝された」と直接示す記述は、見つからず', at=4, size=30, col='gold')]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=1, items=[
      dict(at=1, text='本を背負って得意先を回り、江戸に800軒ほどあったとされる'),
      dict(at=2, text='貸す料金は、買う値段の約6分の1という紹介'),
      dict(at=3, text='読本・草双紙・黄表紙などが貸された')]),
     right=dict(title='分からないこと・言い方', title_at=4, items=[
      dict(at=4, text='庶民のどれほどが借りたか。貸本料の金額'),
      dict(at=4, text='「借りて読むことが、広く行われていた」と言うのが近い')]))]),
 ],
 desc=dict(title_main='江戸の庶民は本を買わず貸本屋で借りて読んでいたのか', title_no=1,
  titles=['江戸の庶民は、本を借りて読んでいた？ 貸本屋800軒を確かめる', '貸本屋は買う値段の6分の1？ 江戸の本の借り方', '背中に本を背負う貸本屋 江戸の読書を確かめる'],
  intro='「江戸の庶民は、本を買わず、貸本屋で借りて読んでいた」と聞いたことはありませんか。この動画では、辞書や解説記事の説明で、貸本屋の仕組みと数、値段を確かめます。',
  points=['辞書によると、貸本屋は料金を取って本を貸す職業で、江戸時代から明治初期には、読本や草双紙を大風呂敷に包んで得意先を回りました。', '解説によると、1808年の江戸には少なくとも656軒、天保のころの『江戸繁昌記』では800軒とされます。1軒あたりの得意先は170〜180軒ほどと紹介されています。', '研究者の池上英子さんによると、貸す料金は買う値段のおよそ6分の1ほどだそうです。ただし、貸本料の具体的な金額や、庶民のどれほどが借りたかは、確認できていません。'],
  refs=['コトバンク「貸本屋」(辞書・二次情報):https://kotobank.jp/word/%E8%B2%B8%E6%9C%AC%E5%B1%8B', 'Edo Flourishing「kashihonya lending books」(個人ブログ・二次情報。池上英子氏の説を紹介):https://edoflourishing.blogspot.com/2015/06/kashihonya-lending-books.html'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['軒数・得意先・値段の数字は、個人ブログによる紹介で、原典(『江戸繁昌記』や専門書)は確認できていません。', '貸す料金が買う値段の約6分の1という数字は、研究者の説として紹介されたもので、原文は未確認です。', '「本が高価だったから貸本が重宝された」ことを直接示す記述は、今回見つかっていません。'],
  tags='江戸時代, 貸本屋, 黄表紙, 江戸の暮らし, 読書, 検証',
  checks=['『江戸繁昌記』の貸本屋の記述を確認する', '長友千代治『近世貸本屋の研究』を確認する', '貸本料の金額の記録を確認する']),
 thumb=dict(bg='assets/kashihon/thumb_art.png', lines=[['本は借りて読む？', 80, 'white'], ['貸本屋800軒', 100, 'gold']], sub='辞書と解説記事で、確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {'intro': 'intro', 'toha': 'bundle', 'kazu': 'shelf', 'nedan': 'shelf', 'naka': 'bundle', 'end': 'intro'})
