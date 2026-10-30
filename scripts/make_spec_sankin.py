"""Writes data/sankin_spec.json（参勤交代は、大名を貧乏にさせるための制度だった？）。台本：docs/themes/20270217_sankin/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
spec = dict(slug='sankin', theme_dir='20270217_sankin', pack='62_sankin', header_sub='解説記事の数字で、参勤交代の費用と負担を確かめる',
 images={},
 bgm=[['intro', 'gyoretsu', 'piano36'], ['tabi', 'edo', 'piano12'], ['moto', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='参勤交代は、大名を貧乏にする制度だった？', chapter_title='導入：参勤交代は、大名を貧乏にする制度だった？', opener='参勤交代は、大名を貧乏にする制度だった？', opener_until=1, scene=[
   dict(t='big', text='参勤交代は、大名を貧乏にする制度だった？', y=270, at=0, size=44, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='長い行列で江戸へ。お金がかかりそう', at=1, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：解説記事の数字', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：負担は大きい。ただし中心は江戸での暮らしの費用', at=4, size=32, col='gold')]),
 dict(key='gyoretsu', title='行列の大きさ', chapter_title='行列の大きさ', scene=[
   dict(t='panel', box=TOP, text='まず、行列の大きさ', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='解説記事：加賀藩前田家の行列は、約2000人', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='『加賀藩大名行列図屏風』：人物473人・馬14頭・駕籠4丁', at=2, until=3, size=32),
   dict(t='panel', box=TOP, text='2000人と473人は数が違う。屏風が全員を描いたかは未確認', at=3, until=4, size=32, col='gold'),
   dict(t='panel', box=TOP, text='加賀藩は、江戸まで約2週間かけて旅したとされる', at=4, size=36),
   dict(t='table', box=[60, 300, 1860, 640], cols=['加賀藩の行列（解説記事）', '数字'], colw=[1200, 600], size=32, rows=[
     dict(at=1, cells=['行列の人数（時代による）', '約2000人']),
     dict(at=2, cells=['屏風に描かれた人物', '473人'], col='gold'),
     dict(at=4, cells=['江戸までの日数', '約2週間'])])]),
 dict(key='tabi', title='旅費は、いくらか', chapter_title='旅費は、いくらか', scene=[
   dict(t='panel', box=TOP, text='では、旅費はどれくらいか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='加賀藩・1808年（文化5年）の帰国費用：約5500両', at=1, until=2, size=36, hi=True),
   dict(t='panel', box=TOP, text='往路も同程度。往復で、約1万1000両', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='内訳：旅籠代、川を渡る費用、他藩領を通るときの贈りもの', at=3, until=4, size=34),
   dict(t='panel', box=TOP, text='庄内藩：福島まで来て、旅費が尽きて足止めされた話も', at=4, size=34, col='gold'),
   dict(t='table', box=[60, 300, 1860, 640], cols=['加賀藩の旅費（解説記事）', '金額'], colw=[1200, 600], size=32, rows=[
     dict(at=1, cells=['帰国の費用（1808年）', '約5500両']),
     dict(at=2, cells=['往復（往路も同程度）', '約1万1000両'], col='gold')])]),
 dict(key='edo', title='江戸での暮らし', chapter_title='江戸での暮らし', scene=[
   dict(t='panel', box=TOP, text='いちばん大きな出費は、別にあった', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='解説記事：江戸での支出は、年間経費の約43〜78%', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='加賀藩・1747年（延享4年）：約61%が江戸での支出', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='往復の旅費は、江戸での支出の約10分の1', at=3, until=4, size=40),
   dict(t='panel', box=TOP, text='負担の中心は、江戸藩邸の暮らしと、藩士の給金', at=4, size=38, col='gold'),
   dict(t='table', box=[60, 300, 1860, 640], cols=['藩の支出（解説記事）', '割合'], colw=[1200, 600], size=32, rows=[
     dict(at=1, cells=['江戸での支出（各藩・年間経費の中）', '約43〜78%']),
     dict(at=2, cells=['加賀藩（1747年）', '約61%'], col='gold'),
     dict(at=3, cells=['往復の旅費（江戸での支出に対し）', '約10分の1'])])]),
 dict(key='moto', title='目的と、確認できないこと', chapter_title='目的と、確認できないこと', scene=[
   dict(t='panel', box=TOP, text='「貧乏にさせる制度」だったのか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='制度の目的を直接示す史料は、今回、確認できず', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='別の解説：街道や宿場、海上交通が整った面もある', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='費用の数字は、藩や時期、換算によって違う', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='「収入の何割」という比率も、確認できず', at=4, size=38, col='gold')]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=1, items=[
      dict(at=1, text='参勤交代は、藩の財政に大きな負担だったとされる'),
      dict(at=2, text='負担の中心は旅費より、江戸での暮らしの費用'),
      dict(at=3, text='江戸での支出は、年間経費の約4〜8割')]),
     right=dict(title='分からないこと・言い方', title_at=4, items=[
      dict(at=4, text='制度の目的。収入に対する比率。原典の史料'),
      dict(at=4, text='「負担は大きいが、中心は江戸での暮らし」と言うのが近い')]))]),
 ],
 desc=dict(title_main='参勤交代は大名を貧乏にさせる制度だったのか', title_no=1,
  titles=['参勤交代は、大名を貧乏にする制度だった？ 解説記事の数字で確かめる', '参勤交代でいちばんお金がかかったのは旅費じゃない？ 江戸での支出の割合', '加賀藩の行列2000人と旅費5500両 参勤交代の費用の中身'],
  intro='「参勤交代は、大名を貧乏にさせるための制度だった」と聞いたことはありませんか。この動画では、解説記事の数字を使って、参勤交代の費用と藩の負担を確かめます。',
  points=['nippon.comの解説記事によると、加賀藩の1808年(文化5年)の帰国の費用は銀332貫466匁余、約5500両(往路も同程度で、往復約1万1000両)です。行列は時代によりますが約2000人でした。', '同じ記事によると、各藩の年間経費のうち江戸での支出は約43〜78%を占めました。加賀藩の1747年(延享4年)の例では約61%です。往復の旅費は、江戸での支出の約10分の1程度とされています。', '負担の中心は、旅そのものより、江戸藩邸での暮らしと藩士の給金でした。'],
  refs=['nippon.com「参勤交代の費用」の解説記事(二次情報):https://www.nippon.com/ja/japan-topics/c08609/', '記事が挙げる資料:『御道中日記』、『荘内藩主 酒井忠徳の施政資料』(國分剛二著)、『加賀藩大名行列図屏風』(石川県立歴史博物館所蔵)。いずれも原文は未確認'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['費用と割合の数字は、解説記事の紹介で、『御道中日記』などの原文は確認できていません。', '「貧乏にさせるための制度」という目的を直接示す史料は、確認できていません。', '約2000人の行列と、屏風に描かれた473人の関係は、確認できていません。', '円換算は資料によって大きく違うため、扱っていません。'],
  tags='江戸時代, 参勤交代, 大名行列, 加賀藩, 藩財政, 江戸の暮らし, 検証',
  checks=['『御道中日記』の費用の記述を確認する', '各藩の江戸での支出の割合の出典を確認する', '参勤交代の制度の目的に関する研究を確認する']),
 thumb=dict(bg='assets/sankin/thumb_art.png', lines=[['参勤交代の出費', 84, 'white'], ['旅費ではない？', 105, 'gold']], sub='解説記事の数字で、確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {'intro': 'intro', 'gyoretsu': 'river', 'tabi': 'river', 'edo': 'mansion', 'moto': 'mansion', 'end': 'intro'})
