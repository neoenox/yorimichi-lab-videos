"""Writes data/literacy_spec.json（江戸時代の日本は、識字率が世界一だった？）。台本：docs/themes/20270306_literacy/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
spec = dict(slug='literacy', theme_dir='20270306_literacy', pack='51_literacy', header_sub='寺子屋の解説と解説記事で、江戸の識字率を確かめる',
 images={},
 bgm=[['intro', 'tera', 'piano36'], ['yomi', 'sekai', 'piano12'], ['end', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='江戸の日本は、識字率が世界一だった？', chapter_title='導入：江戸時代の日本は、識字率が世界一だった？', opener='江戸の日本は、識字率が世界一だった？', opener_until=1, scene=[
   dict(t='big', text='江戸の日本は、識字率が世界一だった？', y=270, at=0, size=48, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='庶民も、読み書きができた、というイメージ', at=1, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：寺子屋の解説と、解説記事', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：「世界一」と言い切れる根拠は、今回の資料では確認できなかった', at=4, size=32, col='gold')]),
 dict(key='tera', title='寺子屋は、どれくらいあったか', chapter_title='寺子屋は、どれくらいあったか', scene=[
   dict(t='panel', box=TOP, text='庶民が学んだ場所、寺子屋の数を見る', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='1883年の文部省の全国調査：寺子屋は16,560軒あった、とされる', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='江戸：大きな寺子屋が400〜500軒、小さなものを含め1,000〜1,300軒ほどと推定', at=2, until=3, size=30),
   dict(t='panel', box=TOP, text='寺子屋で学んだこと：読み・書き・そろばん', at=3, until=4, size=40),
   dict(t='panel', box=TOP, text='ただし、これは寺子屋の数。読み書きできた人の割合ではない', at=4, size=36, col='gold'),
   dict(t='table', box=[60, 300, 1860, 560], cols=['寺子屋の数（寺子屋の解説）', '数'], colw=[1200, 600], size=34, rows=[
     dict(at=1, cells=['全国（1883年の文部省調査）', '16,560軒'], col='gold'),
     dict(at=2, cells=['江戸（推定）', '1,000〜1,300軒ほど'])])]),
 dict(key='yomi', title='読み書きできた人は、どれくらいか', chapter_title='読み書きできた人は、どれくらいか', scene=[
   dict(t='panel', box=TOP, text='読み書きできた人は、どれくらいだったのか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='ある学校の資料：幕末の識字率は50〜60％、江戸は70％超ではないか', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='同じ資料：地域差が大きく、正確な統計は取れていない', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='つまり、この数字は推定。調査で出た数字ではない', at=3, until=4, size=38, col='gold'),
   dict(t='panel', box=TOP, text='実際の調査：1877年（明治10年）、滋賀県', at=4, until=5, size=40),
   dict(t='panel', box=TOP, text='6歳以上で自分の名前を書ける人：男子89％、女子39％', at=5, until=6, size=40, hi=True),
   dict(t='panel', box=TOP, text='男女で大きな差。江戸時代ではなく、明治初めの1つの県の数字', at=6, size=34, col='gold'),
   dict(t='table', box=[60, 300, 1860, 640], cols=['数字の種類', '内容'], colw=[600, 1200], size=32, rows=[
     dict(at=1, cells=['推定（学校の資料）', '幕末：全国50〜60％、江戸70％超']),
     dict(at=5, cells=['調査（1877年・滋賀県）', '自分の名前を書ける人：男子89％、女子39％'], col='gold')])]),
 dict(key='sekai', title='「世界一」と言えるのか', chapter_title='「世界一」と言えるのか', scene=[
   dict(t='panel', box=TOP, text='「世界一」と言うには、ほかの国との比較が必要', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='1831年のイングランド：読書人口は男性66％、女性50％（寺子屋の解説）', at=1, until=2, size=32, hi=True),
   dict(t='panel', box=TOP, text='ただし、集計の方法や、読み書きの基準が同じとは限らない', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='ある評論家：日本語は漢字の読み書きで測るべき。寺子屋の水準は仮名が中心', at=3, until=4, size=30),
   dict(t='panel', box=TOP, text='仮名中心の数字を、そのまま世界と比べるのは公平でない、という意見', at=4, until=5, size=34),
   dict(t='panel', box=TOP, text='同じ基準で国どうしを比べた資料は、今回の調査では見つからなかった', at=5, size=32, col='gold')]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=1, items=[
      dict(at=1, text='寺子屋は全国に16,000軒以上。庶民が読み書きを学ぶ場は広くあった'),
      dict(at=2, text='識字率70％などの数字は推定で、地域差が大きい'),
      dict(at=3, text='1877年の滋賀県：名前を書ける人は男子約9割、女子約4割')]),
     right=dict(title='分からないこと・言い方', title_at=4, items=[
      dict(at=4, text='「世界一」を、同じ基準で比べた根拠'),
      dict(at=5, text='「読み書きできる人が多かった。ただし世界一かは、はっきりしない」が近い')]))]),
 ],
 desc=dict(title_main='江戸時代の日本は識字率が世界一だったのか', title_no=1,
  titles=['江戸時代の日本は、識字率が世界一だった？ 寺子屋の資料で確かめる', '江戸の識字率「世界一」は本当か：寺子屋16,560軒と、70％の根拠', '江戸時代の識字率はどれくらい？ 寺子屋・滋賀県の調査・世界との比較'],
  intro='「江戸時代の日本は、識字率が世界一だった」と聞いたことはありませんか。この動画では、寺子屋の解説と解説記事で、その根拠を確かめます。',
  points=['寺子屋の解説によると、1883年の文部省の全国調査で、寺子屋は16,560軒あったとされます。江戸には1,000〜1,300軒ほどあったと推定されています。', '幕末の識字率を、全国50〜60％、江戸70％超とする説明がありますが、推定で、地域差が大きく、正確な統計はないとされています。', '1877年(明治10年)の滋賀県の調査では、6歳以上で自分の名前を書ける人は、男子89％、女子39％でした。', '「世界一」を、同じ基準で比べた資料は、今回の調査では確認できませんでした。'],
  refs=['Wikipedia「寺子屋」(文部省『日本教育史資料』などを紹介・二次情報):https://ja.wikipedia.org/wiki/寺子屋', '兵庫県立県立高校の生徒指導部だより「識字率世界NO1の国とは？」(二次情報):https://www2.hyogo-c.ed.jp/weblog2/kenita-hs/', '和楽web(Into Japan Waraku)・江戸の識字率の解説(二次情報):https://intojapanwaraku.com/rock/culture-rock/182791/'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['識字率の数字(50〜60％、70％超)や、ドーアなどの研究、「世界一」という評価の原典は、確認できていません。', '1877年の滋賀県の調査と、1883年の寺子屋の全国調査は、寺子屋の解説(Wikipedia)に載っている数字で、原典の資料は確認していません。', '外国との比較(1831年のイングランド)は、集計の方法や基準が日本の数字と同じとは限りません。'],
  tags='江戸時代, 識字率, 寺子屋, 世界一, 読み書き, 江戸の暮らし, 教育, 検証',
  checks=['ドーア『江戸時代の教育』など、識字率・就学率の原典を確認する', '『日本教育史資料』の寺子屋数の原典を確認する', '同じ基準で比べた国際比較の研究を確認する']),
 thumb=dict(bg='assets/literacy/thumb_art.png', lines=[['江戸の識字率', 90, 'white'], ['世界一？', 130, 'gold']], sub='寺子屋の資料で確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {'intro': 'intro', 'tera': 'desk', 'yomi': 'books', 'sekai': 'shop', 'end': 'intro'})
