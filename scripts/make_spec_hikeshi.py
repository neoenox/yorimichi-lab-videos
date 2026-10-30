"""Writes data/hikeshi_spec.json（江戸の火消しは、水をかけず、家を壊して火を止めた？）。台本：docs/themes/20270203_hikeshi/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
spec = dict(slug='hikeshi', theme_dir='20270203_hikeshi', pack='60_hikeshi', header_sub='東京消防庁などの解説で、江戸の火消しを確かめる',
 images={},
 bgm=[['intro', 'kowasu', 'piano36'], ['mizu', 'soshiki', 'piano12'], ['matoi', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='江戸の火消しは、家を壊して火を止めた？', chapter_title='導入：江戸の火消しは、家を壊して火を止めた？', opener='江戸の火消しは、家を壊して火を止めた？', opener_until=1, scene=[
   dict(t='big', text='江戸の火消しは、家を壊して火を止めた？', y=270, at=0, size=46, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='水をかけて消した、とは限らないらしい', at=1, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：東京消防庁などの解説', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：中心は壊す消し方。水の道具もあった', at=4, size=36, col='gold')]),
 dict(key='kowasu', title='壊して止める', chapter_title='壊して止める', scene=[
   dict(t='panel', box=TOP, text='まず、消し方の中心を見る', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='東京消防庁：火元のまわりの家を取り壊し、広がるのを防いだ', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='道具は、「とび口」や「大のこ」など', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='燃えた家より、壊された家のほうが多い火事もあった（ある解説）', at=3, until=4, size=32),
   dict(t='panel', box=TOP, text='消すというより、燃えるものを先になくして止める', at=4, size=38, col='gold')]),
 dict(key='mizu', title='水の道具', chapter_title='水の道具', scene=[
   dict(t='panel', box=TOP, text='では、水は使わなかったのか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='龍吐水：手で押すポンプがあった', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='東京消防庁：放水の力は、今の消防ホースほどではなかった', at=2, until=3, size=34),
   dict(t='panel', box=TOP, text='刺子半纏：厚い布。水をかぶって、火の粉を防いだ', at=3, until=4, size=36),
   dict(t='panel', box=TOP, text='水は、補助や身を守るために使われた面が大きいようだ', at=4, size=36, col='gold')]),
 dict(key='soshiki', title='火消しの種類', chapter_title='火消しの種類', scene=[
   dict(t='panel', box=TOP, text='火消しにも、種類があった', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='大名火消：1643年、16の大名家を指名。江戸城と武家屋敷を守る', at=1, until=2, size=32, hi=True),
   dict(t='panel', box=TOP, text='定火消：1657年、明暦の大火のあと、4人の旗本に命じて創設', at=2, until=3, size=32),
   dict(t='panel', box=TOP, text='町火消：1718年、南町奉行の大岡忠相が始めた', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='いろは48組＋本所・深川の16組＝64組', at=4, size=40, col='gold'),
   dict(t='table', box=[60, 300, 1860, 640], cols=['火消し（東京消防庁）', 'はじまり'], colw=[1200, 600], size=32, rows=[
     dict(at=1, cells=['大名火消', '1643年']),
     dict(at=2, cells=['定火消', '1657年']),
     dict(at=3, cells=['町火消', '1718年'], col='gold')])]),
 dict(key='matoi', title='纏と火事場', chapter_title='纏と火事場', scene=[
   dict(t='panel', box=TOP, text='町火消の中心は、とび職の人たち', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='纏持ち：火事場に近い屋根で纏を立て、振って目印にした', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='纏は、組ごとにデザインが違った', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='はしご乗りは、のちの出初式の芸として知られる', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='壊す人、纏を持つ人。役割を分けたチームの仕事', at=4, size=38, col='gold')]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=1, items=[
      dict(at=1, text='消し方の中心は、周りの家を壊して燃え広がるのを止めること'),
      dict(at=2, text='龍吐水など水の道具もあったが、放水の力は今ほどではない'),
      dict(at=3, text='町火消は1718年に始まり、64組（東京消防庁の説明）')]),
     right=dict(title='分からないこと・言い方', title_at=4, items=[
      dict(at=4, text='組数は資料で47・48の違いがある。壊した家の割合'),
      dict(at=4, text='「水より、壊して止めるのが中心だった」と言うのが近い')]))]),
 ],
 desc=dict(title_main='江戸の火消しは家を壊して火を止めたのか', title_no=1,
  titles=['江戸の火消しは、家を壊して火を止めた？ 東京消防庁の解説で確かめる', '江戸の火消し、水より「壊す」が中心？ 龍吐水と町火消64組', '江戸の消火はなぜ家を壊した？ 纏・龍吐水・いろは四十八組を整理'],
  intro='「江戸の火消しは、水をかけず、家を壊して火を止めた」と聞いたことはありませんか。この動画では、東京消防庁などの解説を比べて、江戸の消し方と火消しの仕組みを確かめます。',
  points=['東京消防庁の解説によると、火が広がらないよう、火元のまわりの家を取り壊す消し方が中心でした。「とび口」や「大のこ」が使われました。', '「龍吐水」という手押しのポンプもありましたが、放水の力は今の消防ホースほどではなかった、とされます。', '町火消は1718年に南町奉行の大岡忠相が始め、いろは48組に本所・深川の16組を加えて64組になった、と東京消防庁は説明しています。'],
  refs=['東京消防庁「消防の歴史(江戸の消防)」:https://www.tfd.metro.tokyo.lg.jp/learning/elib/times/times01.html', 'コトバンク「火消」(組数を「いろは四十七組」とする説明あり):https://kotobank.jp/word/%E7%81%AB%E6%B6%88'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['町火消の組数は、東京消防庁は「いろは48組と本所・深川16組」、別の辞典は「いろは47組」とし、資料で違いがあります。この動画は東京消防庁の説明に従いました。', '「燃えた家より壊された家のほうが多い火事もあった」は、検索で見つかった解説の記述で、原典は確認できていません。', '「水は補助や身を守るために使われた面が大きい」は、解説をもとにした自作のまとめです。'],
  tags='江戸時代, 火消し, 町火消, 破壊消防, 龍吐水, 纏, 江戸の暮らし, 検証',
  checks=['町火消の組数の違い(47・48)の出どころを確認する', '壊された家の数の記録を確認する', '龍吐水の性能に関する資料を確認する']),
 thumb=dict(bg='assets/hikeshi/thumb_art.png', lines=[['江戸の火消し', 90, 'white'], ['水より壊す？', 110, 'gold']], sub='東京消防庁の解説で、確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {'intro': 'intro', 'kowasu': 'fire', 'mizu': 'fire', 'soshiki': 'town', 'matoi': 'town', 'end': 'intro'})
