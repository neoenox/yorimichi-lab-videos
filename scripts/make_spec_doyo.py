"""Writes data/doyo_spec.json（土用の丑の日と平賀源内）。台本：docs/themes/20270331_doyo/09_script_v2.md
at / until は『章内の行番号（0始まり）』。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
spec = dict(slug='doyo', theme_dir='20270331_doyo', pack='68_doyo', header_sub='解説記事で、土用の丑の日の由来を確かめる',
 images={},
 bgm=[['intro', 'gen', 'piano36'], ['hoka', 'tabe', 'piano12'], ['tabe', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='うなぎの丑の日は、平賀源内が広めた？', chapter_title='導入：うなぎの丑の日は、平賀源内が広めた？', opener='土用の丑の日にうなぎを食べるのは、平賀源内が広めたからだ？', opener_until=1, scene=[
   dict(t='big', text='丑の日のうなぎは、源内が広めた？', y=270, at=0, size=44, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='江戸の学者・平賀源内の知恵の話', at=1, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：解説記事の説明', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：有名な説だが、史料は示されていない', at=4, size=36, col='gold')]),
 dict(key='gen', title='源内説', chapter_title='源内説', scene=[
   dict(t='panel', box=TOP, text='まず、源内説の中身', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='解説記事：夏のうなぎは旬ではなく、人気がなかった', at=1, until=2, size=36, hi=True),
   dict(t='panel', box=TOP, text='困ったうなぎ屋が、平賀源内に相談した、とされる', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='源内：丑の日に「う」のつくものを食べると縁起がいい', at=3, until=4, size=34),
   dict(t='panel', box=TOP, text='店先に「本日土用丑の日」と貼ると、大繁盛した', at=4, size=36, col='gold')]),
 dict(key='hoka', title='ほかの説', chapter_title='ほかの説', scene=[
   dict(t='panel', box=TOP, text='由来の説は、これだけではない', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='別の解説：春木屋善兵衛という鰻屋の話', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='蒲焼を子・丑・寅の3日に分けて作ると、丑の日の分だけ傷まなかった', at=2, until=3, size=30),
   dict(t='panel', box=TOP, text='「う」のつく食べ物：うどん・瓜・梅干しも', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='説が複数あるのは、決め手の史料がないからかもしれない', at=4, size=32, col='gold'),
   dict(t='table', box=[60, 300, 1860, 640], cols=['由来の説', '内容'], colw=[600, 1200], size=32, rows=[
     dict(at=1, cells=['源内説', 'うなぎ屋に「丑の日」の張り紙を勧めた']),
     dict(at=2, cells=['春木屋説', '丑の日に作った分だけ傷まなかった']),
     dict(at=4, cells=['史料での確認', '今回の記事では示されず'], col='gold')])]),
 dict(key='shiryo', title='裏付け', chapter_title='裏付け', scene=[
   dict(t='panel', box=TOP, text='気になるのは、裏付け', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='読んだ解説記事は、源内説の史料・出典を示していない', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='一方、記事は万葉集の歌を挙げる。大伴家持の夏痩せの歌', at=2, until=3, size=34),
   dict(t='panel', box=TOP, text='夏にうなぎ、という考えは、奈良時代から知られていた', at=3, until=4, size=36),
   dict(t='panel', box=TOP, text='ただし、丑の日に食べる風習の始まりは、確認できず', at=4, size=36, col='gold')]),
 dict(key='tabe', title='丑の日の風習', chapter_title='丑の日の風習', scene=[
   dict(t='panel', box=TOP, text='丑の日の風習は、うなぎだけではない', at=0, until=1, size=38),
   dict(t='panel', box=TOP, text='解説記事：かば焼きを食べ、お灸を据える習わし', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='寒中の丑の日には、口荒れを防ぐという「丑紅」', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='夏の丑の日に、黒い食べ物を食べる習慣も', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='丑の日は、いろいろな験担ぎの日だったようだ', at=4, size=38, col='gold')]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=1, items=[
      dict(at=1, text='源内説は、売れないうなぎ屋を助けた話として広く紹介'),
      dict(at=2, text='記事は史料を示さず、春木屋説などほかの説もある'),
      dict(at=3, text='夏にうなぎ、という考えは奈良時代から')]),
     right=dict(title='分からないこと・言い方', title_at=4, items=[
      dict(at=4, text='丑の日に食べる風習の始まり。源内説の史料'),
      dict(at=4, text='「源内が広めた説が有名だが、史料は確認できない」と言うのが近い')]))]),
 ],
 desc=dict(title_main='土用の丑の日のうなぎは平賀源内が広めたのか', title_no=1,
  titles=['うなぎの丑の日は、平賀源内が広めた？ 解説記事で由来を確かめる', '土用の丑の日の由来 源内説と春木屋説、史料は？', '丑の日にうなぎを食べるのはいつから？ 万葉集の歌と源内説'],
  intro='「土用の丑の日にうなぎを食べるのは、平賀源内が広めたからだ」と聞いたことはありませんか。この動画では、解説記事の説明で、源内説の中身と、ほかの説、裏付けを確かめます。',
  points=['解説記事によると、夏のうなぎは旬ではなく人気がなかったため、うなぎ屋が平賀源内に相談し、源内が「丑の日に『う』のつくものを食べると縁起がいい」という語呂合わせを勧めた、とされます。', '別の解説には、春木屋善兵衛という鰻屋が、蒲焼の大量の注文を子・丑・寅の3日に分けて作ったところ、丑の日の分だけ傷まなかった、という話も紹介されています。', '読んだ記事は、源内説に具体的な史料や出典を示していません。夏にうなぎ、という考えそのものは、万葉集の大伴家持の歌から奈良時代にはあったと記事は述べます。'],
  refs=['Into JAPAN WARAKU 土用の丑の日の解説記事(二次情報):https://intojapanwaraku.com/gourmet/11623/', 'precious.jp 土用の丑の日の解説記事(二次情報。春木屋説・黒い食べ物の習慣):https://precious.jp/articles/-/20508'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['源内説・春木屋説は、解説記事の紹介で、江戸時代の史料は確認できていません。', '丑の日にうなぎを食べる風習がいつ始まったかは、確認できていません。「源内が広めなかった」と断定するものではありません。', '春木屋説と黒い食べ物の習慣は、検索結果の解説の紹介で、記事の全文と原典は未確認です。'],
  tags='江戸時代, 土用の丑の日, うなぎ, 平賀源内, 江戸の暮らし, 検証',
  checks=['源内説の最古の文献を確認する', '春木屋説の出典を確認する', '丑の日にうなぎを食べる風習の初出を確認する']),
 thumb=dict(bg='assets/doyo/thumb_art.png', lines=[['源内が広めた？', 84, 'white'], ['土用の丑の日', 100, 'gold']], sub='解説記事で、由来を確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {'intro': 'intro', 'gen': 'stall', 'hoka': 'board', 'shiryo': 'desk', 'tabe': 'stall', 'end': 'intro'})
