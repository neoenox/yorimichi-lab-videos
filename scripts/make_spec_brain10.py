"""Writes data/brain10_spec.json（人は、脳の十パーセントしか使っていない？）。台本：docs/themes/20270123_brain10/09_script_v2.md
at / until は『章内の行番号（0始まり）』。末尾で文の番号に直す。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
R = Path(__file__).resolve().parents[1]
from specart import inject
TOP = [60, 170, 1860, 235]
L = [60, 300, 930, 520]; Rt = [990, 300, 1860, 520]
spec = dict(slug='brain10', theme_dir='20270123_brain10', pack='41_brain10', header_sub='「10%」の出どころと、脳の実際を確かめる',
 images={},
 bgm=[['intro', 'origin', 'piano36'], ['damage', 'imaging', 'piano12'], ['energy', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='人は、脳の10%しか使っていない？', chapter_title='導入：人は、脳の10%しか使っていない？', opener='人は、脳の10%しか使っていない？', opener_until=1, scene=[
   dict(t='big', text='脳は、10%しか使われていない？', y=270, at=0, size=58, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='残りの90%を使えたら、天才になれる？', at=1, size=42, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：原文、脳損傷、脳画像、エネルギー', at=2, size=38),
   dict(t='panel', box=[120, 750, 1800, 830], text='答えは、神話とされる。数字の出どころにも、面白い話がある', at=3, size=38, col='gold')]),
 dict(key='origin', title='この話は、どこから来たのか', chapter_title='この話は、どこから来たのか', scene=[
   dict(t='panel', box=TOP, text='きっかけとされる人物：ウィリアム・ジェームズ（心理学者）', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='1907年の論文「人間のエネルギー」', at=1, until=2, size=40),
   dict(t='panel', box=TOP, text='原文：精神的・肉体的な力の「ごく一部」しか使っていない', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='原文に「10%」という数字は、出てこない', at=3, until=4, size=40, col='gold'),
   dict(t='panel', box=TOP, text='書かれているのは、能力の話。脳のどこが使われているか、ではない', at=4, until=5, size=34),
   dict(t='panel', box=TOP, text='数字は、のちの自己啓発の書き手たちが、付けていった（ベイヤースタインの解説）', at=5, until=6, size=32),
   dict(t='panel', box=TOP, text='1936年：カーネギーの本の序文で、トーマスが、この考えをジェームズのものとして紹介（とされる）', at=6, until=7, size=30),
   dict(t='panel', box=TOP, text='序文は「能力の10%」とされる。「脳の10%」は、その後の言い方だと説明される', at=7, until=8, size=36, hi=True),
   dict(t='panel', box=TOP, text='アインシュタインの発言の記録は、アーカイブに確認されていない', at=8, size=36),
   dict(t='timeline', y=330, x0=160, x1=1760, w=520, size=34, ymax=660, nodes=[dict(at=1, x=330, label='1907年', sub='ジェームズ：「ごく一部」（数字なし）', col='gold'), dict(at=6, x=960, label='1936年', sub='序文：「能力の10%」とされる', col='org'), dict(at=7, x=1590, label='その後', sub='「脳の10%」という言い方が広まる', col='blue')])]),
 dict(key='damage', title='脳をけがすると、何が起きるのか', chapter_title='脳をけがすると、何が起きるのか', scene=[
   dict(t='panel', box=TOP, text='確かめる方法①：脳の損傷', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='90%が使われていないなら、傷ついても影響は出ないはず', at=1, until=2, size=38),
   dict(t='panel', box=TOP, text='実際は：10%よりずっと小さい範囲の損傷でも、重い影響が出ることがある', at=2, until=3, size=34, hi=True),
   dict(t='panel', box=TOP, text='例：脳の一部で血の流れが止まると、小さな範囲でも、言葉や手足の動きに影響が出ることがある', at=3, until=4, size=34),
   dict(t='panel', box=TOP, text='「何も担当していない場所」は、見つかっていない', at=4, until=5, size=38, col='gold'),
   dict(t='panel', box=TOP, text='影響の大きさは、場所・大きさで違う。回復や、他の部分が補う場合も', at=5, size=34),
   dict(t='anim', name='grid100', box=[60, 290, 1860, 850], at=1, at2=2)]),
 dict(key='imaging', title='脳の中を、のぞいてみると', chapter_title='脳の中を、のぞいてみると', scene=[
   dict(t='panel', box=TOP, text='確かめる方法②：脳の活動を画像で見る（PET・fMRI・脳波・電極）', at=0, until=1, size=34, hi=True),
   dict(t='panel', box=TOP, text='心の働きが、脳の特定の場所と結びつけられてきた', at=1, until=2, size=38),
   dict(t='panel', box=TOP, text='「新しい役割を待つ、静かな領域」は、見つかっていない', at=2, until=3, size=38, col='gold'),
   dict(t='panel', box=TOP, text='疑問：課題の間、一部しか光らないのは、なぜ？', at=3, until=4, size=38, hi=True),
   dict(t='panel', box=TOP, text='画像で見えるのは、基準の状態と比べた「差」。暗い部分が止まっているわけではない', at=4, until=5, size=32),
   dict(t='panel', box=TOP, text='PETで測った局所の血流の変化は、多くの課題で5%以下（Raichle & Gusnard 2002）', at=5, until=6, size=32),
   dict(t='panel', box=TOP, text='この5%は、血流が増えた割合。「脳の5%しか使っていない」という意味ではない', at=6, until=7, size=32, col='gold'),
   dict(t='panel', box=TOP, text='安静にしていても、脳は、ふだんから全体で動いている', at=7, until=8, size=38),
   dict(t='panel', box=TOP, text='fMRIは、神経の活動を直接撮るのではなく、血流の変化などから推定する', at=8, size=34),
   dict(t='bars', box=[60, 300, 1860, 540], title='局所の血流の目安（安静時を100とした、自作の模式図）', unit='', max=150, lab_w=560, data=[dict(at=5, label='安静時', value=100, vlabel='100', col='blue', until=8), dict(at=5, label='課題中（多くの課題）', value=105, vlabel='105以下（5%以下の増加）', col='gold', until=8)])]),
 dict(key='energy', title='エネルギーから、考える', chapter_title='エネルギーから、考える', scene=[
   dict(t='panel', box=TOP, text='確かめる方法③：エネルギー', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='体重の約2%。酸素とカロリーの約20%を使う（Raichle & Gusnard 2002）', at=1, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='燃費の悪い、高性能な機械のようなもの', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='90%が無駄なら、維持費も無駄。進化の中で残りにくい', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='ベイヤースタイン：自然選択が、使われない大きな器官を維持するとは考えにくい', at=4, until=5, size=32),
   dict(t='panel', box=TOP, text='ただし、直接の実験ではなく、進化の考え方からの反論', at=5, size=38, col='gold'),
   dict(t='bars', box=[60, 300, 1860, 540], title='脳が占める割合（Raichle & Gusnard 2002）', unit='%', max=25, lab_w=620, data=[dict(at=1, label='体重に占める割合', value=2, vlabel='約2%', col='blue'), dict(at=1, label='酸素・カロリーに占める割合', value=20, vlabel='約20%', col='gold')])]),
 dict(key='meaning', title='「使っている」とは、どういう意味か', chapter_title='「使っている」とは、どういう意味か', scene=[
   dict(t='panel', box=TOP, text='全部のニューロンが、いつも最大で動いている、という意味ではない', at=0, until=1, size=34, hi=True),
   dict(t='panel', box=TOP, text='場所ごとに、働きの強さは、時々刻々と変わる。一部が永遠に眠っている証拠は、ない', at=1, until=2, size=32),
   dict(t='panel', box=TOP, text='「脳には、まだ分からないことが多い」は本当。でも、「90%が未使用」とは別の話', at=2, size=32, col='gold')]),
 dict(key='why', title='なぜ、信じられてきたのか', chapter_title='なぜ、信じられてきたのか', scene=[
   dict(t='panel', box=TOP, text='広まった理由①：初期の脳研究の「沈黙の皮質」', at=0, until=1, size=36, hi=True),
   dict(t='panel', box=TOP, text='働きが分かりにくく、「何もしていない」と誤解された可能性がある（とされる）', at=1, until=2, size=32),
   dict(t='panel', box=TOP, text='2002年のブラジルの調査：大学教育を受けた人にも、信じる人が多かった', at=2, until=3, size=34),
   dict(t='panel', box=TOP, text='広まった理由②：「まだ大きな可能性がある」と言ってくれる、魅力的な話', at=3, until=4, size=34, col='gold'),
   dict(t='panel', box=TOP, text='ベイヤースタインも、意欲を高めてきた面は認める。ただし、事実かどうかとは別', at=4, size=32)]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=1, text='損傷の研究でも、画像でも、静かに眠る領域は見つかっていない'),
      dict(at=2, text='脳は体重の約2%で、エネルギーの約20%を使う'),
      dict(at=3, text='「10%」は、ジェームズの原文にない'),
      dict(at=4, text='能力の話が、いつのまにか、脳の話になった、と説明されている')]),
     right=dict(title='言えないこと', title_at=5, items=[
      dict(at=5, text='人の力が、これ以上伸びない、ということ（練習と経験の話は別）')]))]),
 ],
 desc=dict(title_main='人は、脳の10%しか使っていないのか', title_no=1,
  titles=['人は、脳の10%しか使っていない？ 原文と脳の研究で確かめる', '「脳は10%しか使っていない」は本当か：ジェームズの原文に数字はあるか', '脳の10%神話：どこから来て、なぜ否定されるのか'],
  intro='「人は、脳の10%しか使っていない」という話を、聞いたことはないでしょうか。この動画では、この話の出どころとされる、ウィリアム・ジェームズの論文(1907年)と、脳損傷・脳画像・エネルギー消費の研究から、事実かどうかを確かめます。',
  points=['ジェームズ『人間のエネルギー』(1907年)の原文に、「10%」という数字は出てきません。書かれているのは、人の力や能力の話です。', '1936年のカーネギーの本の序文が、広まるきっかけの一つだったとされます。序文の原文は、この動画では確認していません。', '脳の損傷では、10%よりずっと小さい範囲でも、重い影響が出ることがあります。', '脳画像でも、新しい役割を待つ静かな領域は見つかっていません。局所の血流の変化が5%以下というのは、使用割合ではありません。', '脳は体重の約2%で、体の酸素とカロリーの約20%を使います(Raichle & Gusnard, 2002)。'],
  refs=['William James「The Energies of Men」(1911年版の翻刻、Wikisource):https://en.wikisource.org/wiki/The_Energies_of_Men', 'Raichle & Gusnard (2002) PNAS 99(16):10237–10239:https://pmc.ncbi.nlm.nih.gov/articles/PMC124895', 'Barry L. Beyerstein (2004) Do we really use only 10 percent of our brains? Scientific American:https://www.scientificamerican.com/article/do-we-really-use-only-10/', 'Beyerstein (1999) Whence cometh the myth that we only use ten percent of our brains? In Della Sala (ed.) Mind Myths, Wiley, pp.1-24(この動画では、Scientific American の記事を通して確認しました)'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['1936年のカーネギー本の序文の原文は、確認していません。解説(ベイヤースタイン)による紹介です。', '2002年のブラジルの調査は、原論文の割合を確認できていないため、数字を言っていません。', '血流が止まったときの影響の例は、一般的な医学知識にもとづく説明です。', 'ベイヤースタインの1999年の章そのものは読んでおらず、2004年の記事で確認しました。'],
  tags='脳, 10%神話, 脳科学, 都市伝説, ウィリアム・ジェームズ, 俗説, 検証, 心理学',
  checks=['1936年カーネギー『人を動かす』序文の原文で、10%の記述を確認する', 'ブラジル調査(Herculano-Houzel 2002)の本文で、割合を確認する', 'ベイヤースタイン1999の章(Mind Myths)を確認する', '1907年 Philosophical Review 初出版の文言を確認する']),
 thumb=dict(bg='assets/brain10/thumb_art.png', lines=[['脳の10%しか', 100, 'white'], ['使ってない', 100, 'white'], ['は本当？', 130, 'gold']], sub='原文と脳の研究で確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and o.get('title'):
            h = o['box'][3] - o['box'][1]
            if h < 112:
                tx = o['title'] + '：' + o['text']; sz = min(o.get('size', 40), 40, int((o['box'][2] - o['box'][0] - 70) / len(tx)))
                if sz >= 26: o['title'] = None; o['text'] = tx; o['size'] = sz
                else: o['size'] = min(o.get('size', 40), 30)
            else: o['size'] = min(o.get('size', 40), 40 if h < 125 else 46)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


def _line_to_sentence_starts():
    """台本の番号つきの行（1行に複数の文がある）→ 各行の最初の文の番号（vp.py の sentences と同じく「。」で区切る）。
    この spec の at / until / title_at は『行の番号（0始まり）』で書き、ここで文の番号に直す。"""
    import re
    t = (R / 'docs' / 'themes' / '20270123_brain10' / '09_script_v2.md').read_text(encoding='utf8')
    out = []
    for c in re.split('\n## ', t)[1:]:
        if not re.match('章(\\d+)　', c.split('\n')[0]): continue
        starts, n = [], 0
        for l in c.split('\n'):
            if re.match('^\\d+\\. ', l):
                body = re.sub('〔[^〕]*〕', '', re.sub('^\\d+\\. ', '', l)).strip()
                starts.append(n); n += len([x for x in body.split('。') if x.strip()])
        starts.append(n)
        out.append(starts)
    return out


def _remap(o, st):
    f = lambda i: None if i is None else st[min(i, len(st) - 1)]
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if k in ('at', 'until', 'title_at', 'at2') and isinstance(v, int): o[k] = f(v)
            else: _remap(v, st)
    elif isinstance(o, list):
        for v in o: _remap(v, st)


_S = _line_to_sentence_starts()
assert len(_S) == len(spec['chapters']), (len(_S), len(spec['chapters']))
for _ch, _st in zip(spec['chapters'], _S):
    _remap(_ch['scene'], _st)
    if 'opener_until' in _ch: _ch['opener_until'] = _st[min(_ch['opener_until'], len(_st) - 1)]

_fit(spec)
inject(spec, {'intro': 'intro', 'origin': 'study', 'damage': 'clinic', 'imaging': 'scan', 'energy': 'lamp', 'meaning': 'city', 'why': 'crowd', 'end': 'intro'})
(R / 'data' / 'brain10_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
