"""Writes data/carpenter_spec.json（江戸の大工は、一日四時間しか働かなかった？）。台本：docs/themes/20261216_carpenter/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
spec = dict(slug='carpenter', theme_dir='20261216_carpenter', pack='53_carpenter', header_sub='解説記事の説明を比べて、江戸の大工の働く時間を確かめる',
 images={},
 bgm=[['intro', 'yon', 'piano36'], ['genba', 'kazu', 'piano12'], ['shugyo', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='江戸の大工は、一日四時間しか働かなかった？', chapter_title='導入：江戸の大工は、一日4時間しか働かなかった？', opener='江戸の大工は、一日4時間しか働かなかった？', opener_until=1, scene=[
   dict(t='big', text='江戸の大工は、一日4時間しか働かなかった？', y=270, at=0, size=46, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='今から見ると、とても短く感じる', at=1, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：解説記事の説明', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：休憩が多く、実働は短め。ただし数字に幅があり、出典も不明', at=4, size=32, col='gold')]),
 dict(key='yon', title='「4時間」という説明', chapter_title='「4時間」という説明', scene=[
   dict(t='panel', box=TOP, text='まず、一日4時間という話の出どころを見る', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='歴史家の解説記事：大工は昼食を含め、一日3回の休憩があった', at=1, until=2, size=36, hi=True),
   dict(t='panel', box=TOP, text='休憩を引くと、働くのは4時間ほど、という話', at=1, until=2, size=40),
   dict(t='panel', box=TOP, text='ただし「という」と伝聞の形。元の史料は示されていない', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='話としては面白いが、そのまま事実とは言いにくい', at=3, size=38, col='gold')]),
 dict(key='genba', title='現場にいた時間は、長かった', chapter_title='現場にいた時間は、長かった', scene=[
   dict(t='panel', box=TOP, text='別の解説では、働いた時間がもっと長く書かれている', at=0, until=1, size=38),
   dict(t='panel', box=TOP, text='朝の六ツ半（今の午前7時ごろ）から、夕の七ツ半（午後5時ごろ）まで', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='現場にいた時間だけなら、約10時間（自作の計算）', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='休憩を引くと、実働は6〜7時間ほど、という計算', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='時刻は不定時法。同じ六ツ半でも、季節で実際の時刻は変わる', at=4, size=34, col='gold'),
   dict(t='table', box=[60, 300, 1860, 560], cols=['説明の出どころ', '実働の目安'], colw=[1100, 700], size=34, rows=[
     dict(at=1, cells=['歴史家の解説記事', '約4時間']),
     dict(at=3, cells=['別の解説（現場に約10時間）', '6〜7時間ほど'], col='gold')])]),
 dict(key='kazu', title='数字に幅がある理由', chapter_title='数字に幅がある理由', scene=[
   dict(t='panel', box=TOP, text='4時間から7時間。同じ大工でも、数字がだいぶ違う', at=0, until=1, size=38),
   dict(t='panel', box=TOP, text='理由1：休憩を何回、どれだけ数えるか（自作の整理）', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='理由2：季節や仕事の種類。夏は昼が長く、冬は短い', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='理由3：どの解説も、元になった史料を示していない', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='結論：4〜7時間と言われるが、確かな数字は分からない', at=4, size=38, col='gold')]),
 dict(key='shugyo', title='大工になるまでが、大変だった', chapter_title='大工になるまでが、大変だった', scene=[
   dict(t='panel', box=TOP, text='もう一つ、見落としたくない話：大工になるまで', at=0, until=1, size=38),
   dict(t='panel', box=TOP, text='一人前になるまで、数年間は、給金のない弟子修行（解説記事）', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='独立後も、しばらくは下働きが続いた（解説記事）', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='腕のよい大工は高給とあるが、金額は確認できなかった', at=3, until=4, size=36),
   dict(t='panel', box=TOP, text='時間が短くても、「楽な仕事」とは言い切れない', at=4, size=38, col='gold')]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=1, items=[
      dict(at=1, text='「一日4時間」は、昼食を含む3回の休憩を引いた数字として紹介されている'),
      dict(at=2, text='別の解説：現場に約10時間いて、実働は6〜7時間ほど'),
      dict(at=3, text='どちらも、元になった史料は示されていない')]),
     right=dict(title='分からないこと・言い方', title_at=4, items=[
      dict(at=4, text='確かな実働時間。季節・仕事による違い'),
      dict(at=5, text='「休憩が多く、実働は4〜7時間ほどと説明されることが多い」と言うのが近い')]))]),
 ],
 desc=dict(title_main='江戸の大工は一日四時間しか働かなかったのか', title_no=1,
  titles=['江戸の大工は、一日4時間しか働かなかった？ 解説記事の説明を比べて確かめる', '江戸の大工の働く時間：4時間説と6〜7時間説、どちらが近い？', '江戸の職人は楽だった？ 大工の休憩・実働・修行を調べてみた'],
  intro='「江戸時代の大工は、一日に4時間しか働かなかった」と聞いたことはありませんか。この動画では、解説記事の説明を比べて、働く時間を確かめます。',
  points=['歴史家の解説記事は、大工は昼食を含めて一日3回の休憩があり、それを引くと働くのは4時間ほどで済んだ、と紹介しています。ただし伝聞の形で、元の史料は示されていません。', '別の解説では、大工は朝の六ツ半(午前7時ごろ)から夕の七ツ半(午後5時ごろ)まで現場にいる習慣で、休憩を引くと実働は6〜7時間ほど、と説明されています。', '一人前になるまで数年間は給金のない弟子修行があった、とも紹介されています。'],
  refs=['河合敦「江戸時代、庶民の労働はこんなにブラックだった」(現代ビジネス・二次情報):https://gendai.media/articles/-/52810', '「江戸時代の人々はどう働いていたか」(note・二次情報):https://note.com/o_eight/n/n72be2378b651'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['労働時間の数字(4時間、6〜7時間)は、いずれも解説記事の二次情報で、元になった史料は確認できていません。', '手間賃(給金)の金額は、出典を確認できなかったため、扱っていません。', '「約10時間」は、午前7時ごろから午後5時ごろまでの差による、自作の計算です。'],
  tags='江戸時代, 大工, 職人, 労働時間, 江戸の暮らし, 不定時法, 弟子修行, 検証',
  checks=['江戸の職人の労働時間について、史料に基づく研究を確認する', '大工の手間賃(日当)の出典を確認する']),
 thumb=dict(bg='assets/carpenter/thumb_art.png', lines=[['江戸の大工は', 90, 'white'], ['一日4時間？', 120, 'gold']], sub='休憩と実働を、記事で確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {'intro': 'intro', 'yon': 'tools', 'genba': 'site', 'kazu': 'site', 'shugyo': 'deshi', 'end': 'intro'})
