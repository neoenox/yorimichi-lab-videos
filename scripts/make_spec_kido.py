"""Writes data/kido_spec.json（江戸の町は、夜になると閉鎖された？）。台本：docs/themes/20261223_kido/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
spec = dict(slug='kido', theme_dir='20261223_kido', pack='54_kido', header_sub='木戸番の解説と国会図書館の事例で、江戸の夜の木戸を確かめる',
 images={},
 bgm=[['intro', 'mokuteki', 'piano36'], ['jikoku', 'tooreru', 'piano12'], ['kyubyo', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='江戸の町は、夜になると閉鎖された？', chapter_title='導入：江戸の町は、夜になると閉鎖された？', opener='江戸の町は、夜になると閉鎖された？', opener_until=1, scene=[
   dict(t='big', text='江戸の町は、夜になると閉鎖された？', y=270, at=0, size=48, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='木戸が閉まって、通れなくなった、という話', at=0, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：木戸番の解説と、国会図書館の事例', at=2, size=38),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：夜の10時ごろに閉まったが、決まりに従えば、通れた', at=3, size=36, col='gold')]),
 dict(key='mokuteki', title='木戸は、何のためにあったのか', chapter_title='木戸は、何のためにあったのか', scene=[
   dict(t='panel', box=TOP, text='まず、木戸とは何かを見る', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='国会図書館の事例：町の境ごとに木戸があり、夜は原則通行禁止', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='目的：盗賊や怪しい人が、町の中を自由に動けないようにする', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='木戸を開け閉めし、夜の見回りもする人：木戸番', at=3, size=38, col='gold')]),
 dict(key='jikoku', title='何時に閉まったのか', chapter_title='何時に閉まったのか', scene=[
   dict(t='panel', box=TOP, text='何時に閉まったのか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='Wikipedia「木戸番」：夜の四ツ時（午後10時ごろ）に閉めた', at=1, until=2, size=36, hi=True),
   dict(t='panel', box=TOP, text='時刻は季節で変わる不定時法。いつも同じ時刻とは限らない', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='長屋の路地木戸は、もっと早く閉まることもあった', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='「夜の10時ごろ」は、目安として考える', at=4, size=40, col='gold'),
   dict(t='table', box=[60, 300, 1860, 560], cols=['木戸の閉まる時刻（Wikipedia「木戸番」）', '目安'], colw=[1200, 600], size=34, rows=[
     dict(at=1, cells=['夜の四ツ時', '午後10時ごろ'], col='gold'),
     dict(at=3, cells=['長屋の路地木戸', 'もっと早いことも'])])]),
 dict(key='tooreru', title='閉まったあとは、通れなかったのか', chapter_title='閉まったあとは、通れなかったのか', scene=[
   dict(t='panel', box=TOP, text='閉まったあとは、本当に通れなかったのか', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='木戸番に確かめてもらい、左右の潜り戸から通った', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='人数の分だけ拍子木を打つ。次の木戸番への合図（送り拍子木）', at=2, until=3, size=34),
   dict(t='panel', box=TOP, text='拍子木が鳴っても人が来なければ、町内を調べた', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='閉まった木戸は、壁ではなく、検問のようなもの', at=4, size=40, col='gold')]),
 dict(key='kyubyo', title='急病人は、どうしたのか', chapter_title='急病人は、どうしたのか', scene=[
   dict(t='panel', box=TOP, text='気になるのは、夜の急病人', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='Wikipedia：医師や産婆など、命にかかわる急用の人は、そのまま通れた', at=1, until=2, size=32, hi=True),
   dict(t='panel', box=TOP, text='ただし、この例外を定めた法令や史料は、確認できなかった', at=2, until=3, size=36, col='gold'),
   dict(t='panel', box=TOP, text='盗賊が出たときは、時刻に関係なく木戸を閉めた', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='木戸番：火事の半鐘も担当。給金は少なく、焼き芋などを売った', at=4, size=34)]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=1, items=[
      dict(at=1, text='木戸は夜の四ツ時（午後10時ごろ）に閉まったとされる'),
      dict(at=2, text='木戸番に確かめてもらえば、潜り戸から通れた'),
      dict(at=3, text='医師・産婆はそのまま通れたとされる')]),
     right=dict(title='分からないこと・言い方', title_at=4, items=[
      dict(at=4, text='医師・産婆の例外を定めた原典の史料'),
      dict(at=5, text='「夜に閉まったが、決まりに従えば通れた」と言うのが近い')]))]),
 ],
 desc=dict(title_main='江戸の町は夜になると閉鎖されたのか', title_no=1,
  titles=['江戸の町は、夜になると閉鎖された？ 木戸番の解説と国会図書館の事例で確かめる', '江戸の木戸は夜10時に閉まった？ 潜り戸・拍子木・医者の例外', '江戸の夜、木戸が閉まったら通れない？ 急病人はどうした？'],
  intro='「江戸の町は、夜になると木戸が閉まって通れなくなった」と聞いたことはありませんか。この動画では、木戸番の解説と国立国会図書館のレファレンス事例で、夜の木戸の決まりを確かめます。',
  points=['Wikipedia「木戸番」によると、木戸は夜の四ツ時(午後10時ごろ)に閉められました。', '夜四ツ時を過ぎて用事のある人は、木戸番に確かめてもらったうえで、木戸の左右の潜り戸から通りました。通るたびに拍子木を打ち、次の木戸番に知らせました(送り拍子木)。', '医師や産婆など、命にかかわる急用の人は、そのまま通れたと説明されています。この例外を定めた原典は確認できていません。'],
  refs=['Wikipedia「木戸番」(二次情報):https://ja.wikipedia.org/wiki/木戸番', '国立国会図書館 レファレンス協同データベース「江戸においても町の境界毎に木戸が設置されていて…」:https://crd.ndl.go.jp/reference/entry/index.php?page=ref_view&id=1000082495', '「江戸時代の研究ノート 木戸番と番所」(個人の研究ノート・二次情報):https://ncode.syosetu.com/n3190eu/8/'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['木戸の閉まる時刻、潜り戸と拍子木の決まり、医師・産婆の例外は、Wikipediaなどの二次情報で、原典の史料(『守貞漫稿』など)は確認できていません。', '医師・産婆の例外を、はっきり定めた法令や史料は、確認できませんでした。', '木戸の閉まる時刻は、地域・季節・町によって違った可能性があります。'],
  tags='江戸時代, 木戸, 木戸番, 夜, 拍子木, 江戸の暮らし, 潜り戸, 検証',
  checks=['『守貞漫稿』など、木戸の閉鎖時刻と通行の決まりの原典を確認する', '医師・産婆の例外を定めた町触などを確認する']),
 thumb=dict(bg='assets/kido/thumb_art.png', lines=[['江戸の町は', 90, 'white'], ['夜に閉鎖？', 120, 'gold']], sub='木戸の決まりを、資料で確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {'intro': 'intro', 'mokuteki': 'gate', 'jikoku': 'gate', 'tooreru': 'night', 'kyubyo': 'night', 'end': 'intro'})
