"""Writes data/travel_spec.json（江戸時代の旅人は、一日に40キロ歩いた？）。台本：docs/themes/20270113_travel/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
spec = dict(slug='travel', theme_dir='20270113_travel', pack='57_travel', header_sub='国立国会図書館のレファレンス事例で、江戸の旅の距離を確かめる',
 images={},
 bgm=[['intro', 'kotae', 'piano36'], ['chigau', 'tokaido', 'piano12'], ['iikata', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='江戸時代の旅人は、一日に40キロ歩いた？', chapter_title='導入：江戸時代の旅人は、一日に40キロ歩いた？', opener='江戸時代の旅人は、一日に40キロ歩いた？', opener_until=1, scene=[
   dict(t='big', text='江戸時代の旅人は、一日に40キロ歩いた？', y=270, at=0, size=46, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='今の私たちには、なかなか難しい距離', at=1, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：国立国会図書館のレファレンス事例', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：男性は35〜39km歩く例が多い。人や旅で幅がある', at=4, size=34, col='gold')]),
 dict(key='kotae', title='レファレンス事例の答え', chapter_title='レファレンス事例の答え', scene=[
   dict(t='panel', box=TOP, text='まず、図書館の回答を見る', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='レファレンス事例（愛知県図書館）：成人男性は平坦な道で一日9〜10里', at=1, until=2, size=32, hi=True),
   dict(t='panel', box=TOP, text='1里は約3.93km。9〜10里は約35〜39km（自作の計算）', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='女性は、6〜8里（約23〜31km）', at=3, until=4, size=40),
   dict(t='panel', box=TOP, text='根拠の本：金森敦子『江戸庶民の旅』など（原典は未確認）', at=4, size=34, col='gold'),
   dict(t='table', box=[60, 300, 1860, 560], cols=['旅人（レファレンス事例）', '一日の距離'], colw=[900, 900], size=34, rows=[
     dict(at=1, cells=['成人男性（平坦な道）', '9〜10里（約35〜39km）'], col='gold'),
     dict(at=3, cells=['女性', '6〜8里（約23〜31km）'])])]),
 dict(key='chigau', title='本によって、数字が違う', chapter_title='本によって、数字が違う', scene=[
   dict(t='panel', box=TOP, text='ただし、本によって数字は少しずつ違う', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='伊勢参りの本：ゆったり6〜7里、急ぎ旅や健脚は12〜13里', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='平均は、8里前後（約31km）', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='東海道の本：11泊12日の旅で、一日約10里半の例', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='道中記に「何里歩いた」と書いた例は少ない、との指摘も', at=4, size=34, col='gold')]),
 dict(key='tokaido', title='東海道を、計算してみる', chapter_title='東海道を、計算してみる', scene=[
   dict(t='panel', box=TOP, text='東海道を、計算で確かめてみる', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='10里半 × 12日 ＝ 126里（自作の計算）', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='126里 × 約3.93km ＝ 約495km（自作の計算）', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='日本橋〜京都の道のりに近い数字（資料で少し違う）', at=3, until=4, size=36),
   dict(t='panel', box=TOP, text='11泊12日で着くには、一日40km余り歩く計算', at=4, size=38, col='gold')]),
 dict(key='iikata', title='どう言えばよいのか', chapter_title='どう言えばよいのか', scene=[
   dict(t='panel', box=TOP, text='「一日40km」は、どう言えばよいか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='急ぐ男性の旅なら、あり得る数字', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='平均は8里前後（約31km）という見方もある', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='女性や、ゆったりした旅は、もっと短い', at=3, until=4, size=40),
   dict(t='panel', box=TOP, text='一つの数字で言い切るのは、難しい', at=4, size=40, col='gold')]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=1, items=[
      dict(at=1, text='成人男性は平坦な道で9〜10里（約35〜39km）が一般的とされる'),
      dict(at=2, text='女性は6〜8里（約23〜31km）'),
      dict(at=3, text='平均を8里前後とする本もあり、旅の目的で幅がある')]),
     right=dict(title='分からないこと・言い方', title_at=4, items=[
      dict(at=4, text='一日の平均の確かな数字。原典の道中記'),
      dict(at=4, text='「急ぐ男性なら40km近い例も。平均はもう少し短め」と言うのが近い')]))]),
 ],
 desc=dict(title_main='江戸時代の旅人は一日に四十キロ歩いたのか', title_no=1,
  titles=['江戸時代の旅人は、一日に40キロ歩いた？ 国会図書館のレファレンス事例で確かめる', '江戸の旅は一日何里？ 9〜10里・8里・10里半と、東海道12日の計算', '江戸時代の旅人の歩く距離：男性35〜39km、女性23〜31km、本当？'],
  intro='「江戸時代の旅人は、一日に40キロ歩いた」と聞いたことはありませんか。この動画では、国立国会図書館のレファレンス協同データベースの事例で、一日に歩いた距離を確かめます。',
  points=['愛知県図書館が答えたレファレンス事例によると、成人男性は平坦な道で一日9〜10里(約35〜39km)、女性は6〜8里(約23〜31km)が一般的とされています。', '本によって数字は違い、伊勢参りの本では平均8里前後(約31km)、東海道の本では11泊12日で一日約10里半の例が挙げられています。', '10里半を12日続けると126里、約495kmになります(1里を約3.93kmとした自作の計算)。'],
  refs=['国立国会図書館 レファレンス協同データベース「江戸時代に旅行した人は1日に何キロくらい歩いたのか」(愛知県図書館・登録番号1000139827):https://crd.ndl.go.jp/reference/entry/index.php?id=1000139827&page=ref_view', '国土交通省 横浜国道事務所「江戸時代の旅人は1日で何キロくらい歩いたの？」(東海道Q&A):https://www.ktr.mlit.go.jp/yokohama/tokaido/02_tokaido/04_qa/index4/answer1.htm'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['レファレンス事例が根拠として挙げる本(金森敦子『江戸庶民の旅』、鎌田道隆『お伊勢参り』、森川昭『東海道五十三次ハンドブック』、板坂耀子『江戸の旅を読む』など)の原典は確認できていません。', '1里は約3.93kmとして換算しました。東海道の道のりは資料によって少し違います。', '「一日40km余り」は、10里半×12日の自作の計算で、実際の旅の記録ではありません。'],
  tags='江戸時代, 旅, 東海道, 里, 歩く距離, 道中記, 江戸の暮らし, 検証',
  checks=['道中記など、一日の歩行距離の一次史料を確認する', '日本橋〜京都の道のりを、資料ごとに確認する']),
 thumb=dict(bg='assets/travel/thumb_art.png', lines=[['江戸の旅人は', 90, 'white'], ['一日40km？', 120, 'gold']], sub='里とキロを、計算で確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {'intro': 'intro', 'kotae': 'road', 'chigau': 'inn', 'tokaido': 'road', 'iikata': 'inn', 'end': 'intro'})
