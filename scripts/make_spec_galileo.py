"""Writes data/galileo_spec.json（ガリレオは「それでも地球は動く」と言った？）。台本：docs/themes/20270213_galileo/09_script_v2.md
at / until は『章内の行番号（0始まり）』。末尾で文の番号に直す。イラスト（specart.inject）は、画像ができてから足す。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
R = Path(__file__).resolve().parents[1]
from specart import inject
TOP = [60, 170, 1860, 235]
spec = dict(slug='galileo', theme_dir='20270213_galileo', pack='44_galileo', header_sub='有名な言葉の、最古の記録を確かめる',
 images={},
 bgm=[['intro', 'first', 'piano36'], ['painting', 'why', 'piano12'], ['clear', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='ガリレオは「それでも地球は動く」と言った？', chapter_title='導入：ガリレオは「それでも地球は動く」と言った？', opener='「それでも地球は動く」', opener_until=1, scene=[
   dict(t='big', text='「それでも地球は動く」', y=270, at=0, size=64, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='裁判のあとの、ガリレオのつぶやき？', at=1, size=44, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる：本当に、そう言ったのか', at=2, size=40),
   dict(t='panel', box=[120, 750, 1800, 830], text='同時代の証拠は見つかっていない。印刷物の最古の例は、死後100年以上あと', at=3, size=32, col='gold')]),
 dict(key='trial', title='伝承は、どんな話か', chapter_title='伝承は、どんな話か', scene=[
   dict(t='panel', box=TOP, text='伝承：1633年、ローマの異端審問にかけられたガリレオ', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='地動説を撤回させられた後、「それでも地球は動く」とつぶやいた、とされる', at=1, until=2, size=32),
   dict(t='panel', box=TOP, text='裁判にかけられ、地動説を撤回させられたことは、歴史の解説で述べられている', at=2, until=3, size=32),
   dict(t='panel', box=TOP, text='著作『天文対話』は、禁書目録に載った', at=3, until=4, size=40),
   dict(t='panel', box=TOP, text='ガリレオが、地球は動くと考え続けていたことも、確かだとされる', at=4, until=5, size=34),
   dict(t='panel', box=TOP, text='問題：そのつぶやきを裏づける記録は、あるのか', at=5, size=40, col='gold')]),
 dict(key='first', title='最初の記録は、いつか', chapter_title='最初の記録は、いつか', scene=[
   dict(t='panel', box=TOP, text='印刷物で確認されている最も古い例：1757年', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='バレッティ『イタリアン・ライブラリー』（ロンドン、英語の本）', at=1, until=2, size=36),
   dict(t='panel', box=TOP, text='解放された直後に、空を見上げ、足で地面を踏みながら言った、と書いた（とされる）', at=2, until=3, size=30),
   dict(t='panel', box=TOP, text='ガリレオの死（1642年）から、100年以上あと', at=3, until=4, size=40, col='gold'),
   dict(t='panel', box=TOP, text='この記述には「歴史に基づかない飾り」が含まれる、とも言われる', at=4, until=5, size=34),
   dict(t='panel', box=TOP, text='1761年：フランスで出た本にも載り、広まっていった', at=5, until=6, size=38),
   dict(t='panel', box=TOP, text='ヴィヴィアーニ（弟子）の最初の伝記にも、裁判の記録にも、この言葉はない（とされる）', at=6, until=7, size=30, hi=True),
   dict(t='panel', box=TOP, text='ガリレオの時代の記録として、この言葉を示すものは、見つかっていない', at=7, size=34),
   dict(t='timeline', y=330, x0=160, x1=1760, w=520, size=34, ymax=660, nodes=[dict(at=3, x=330, label='1642年', sub='ガリレオが亡くなる', col='gold'), dict(at=0, x=960, label='1757年', sub='印刷物での最古の例（バレッティ）', col='org'), dict(at=5, x=1590, label='1761年', sub='フランスの本にも載り、広まる', col='blue')])]),
 dict(key='painting', title='絵に、書いてあった？', chapter_title='絵に、書いてあった？', scene=[
   dict(t='panel', box=TOP, text='1911年：ベルギーの収集家が、ある絵画を手に入れた', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='絵には「それでも地球は動く」と書き込まれていた', at=1, until=2, size=38),
   dict(t='panel', box=TOP, text='制作年は1643年か1645年、作者はムリーリョとされた', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='本物なら、死の直後にこの話が広まっていた証拠になる', at=3, until=4, size=38, col='gold'),
   dict(t='panel', box=TOP, text='専門家4人は、写真を見て、ムリーリョ作とは考えにくいと言った。うち一人は19世紀の作品では、と', at=4, until=5, size=28),
   dict(t='panel', box=TOP, text='1837年に描かれた『獄中のガリレオ』が、ほぼ同じ構図', at=5, until=6, size=36, hi=True),
   dict(t='panel', box=TOP, text='2007年：オークション会社は19世紀の作品と判断。署名・日付は見つからず', at=6, until=7, size=32),
   dict(t='panel', box=TOP, text='この絵をガリレオの時代の証拠と考えるのは、難しい', at=7, size=40, col='gold'),
   dict(t='table', box=[60, 300, 1860, 700], cols=['いつ', 'できごと'], colw=[300, 1460], size=34, rows=[
     dict(at=0, cells=['1911年', 'ベルギーの収集家が、絵画を入手（制作年は1643年か1645年とされた）']),
     dict(at=4, cells=['専門家4人', '写真を見て、ムリーリョ作とは考えにくいと判断（うち一人は19世紀の作品ではと）'], col='gold'),
     dict(at=5, cells=['1837年', 'ヴァン・マルデヘムが、ほぼ同じ構図の『獄中のガリレオ』を描いていた']),
     dict(at=6, cells=['2007年', 'オークション会社は19世紀の作品と判断。署名・日付は見つからなかった'], col='gold')])]),
 dict(key='say', title='言わなかった、と言えるのか', chapter_title='言わなかった、と言えるのか', scene=[
   dict(t='panel', box=TOP, text='では、言わなかったと言い切れるのか', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='天文学者リビオ：異端審問官の前で言うのは、極めて危険だった', at=1, until=2, size=36),
   dict(t='panel', box=TOP, text='後の時代の作り話の可能性が高い。ただし、確実ではない、とも述べる', at=2, until=3, size=34),
   dict(t='panel', box=TOP, text='「言った証拠がない」≠「言わなかった証拠がある」', at=3, until=4, size=40, col='gold'),
   dict(t='panel', box=TOP, text='心の中や、その場のつぶやきは、記録に残りにくい', at=4, until=5, size=40),
   dict(t='panel', box=TOP, text='確かに言えるのは：同時代の記録には見つかっていない。印刷物の最古の例は、100年以上あと', at=5, size=30, hi=True)]),
 dict(key='why', title='なぜ、広まったのか', chapter_title='なぜ、広まったのか', scene=[
   dict(t='panel', box=TOP, text='それでも、とても有名になった。なぜか', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='考えられる理由①：話として、とても分かりやすい', at=1, until=2, size=40),
   dict(t='panel', box=TOP, text='権力に言葉では従っても、真実は心の中で曲げなかった、という筋書き', at=2, until=3, size=34),
   dict(t='panel', box=TOP, text='考えられる理由②：ガリレオが地動説を考え続けていたのは確かで、本当らしく聞こえた', at=3, until=4, size=30),
   dict(t='panel', box=TOP, text='これは私の推測。広まった理由を示す記録は、確認していない', at=4, size=38, col='gold')]),
 dict(key='clear', title='分かることと、分からないこと', chapter_title='分かることと、分からないこと', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かっていること', title_at=0, items=[
      dict(at=1, text='ガリレオは、異端の疑いで裁判にかけられ、地動説を撤回させられた'),
      dict(at=2, text='地球は動くと、考え続けていた'),
      dict(at=3, text='印刷物での最古の例は、1757年の本（死後100年以上あと）'),
      dict(at=4, text='この絵を、ガリレオの時代の証拠と見ることは難しい')]),
     right=dict(title='分からないこと', title_at=5, items=[
      dict(at=5, text='実際に、つぶやいたのかどうか。直接確かめる記録は見つかっていない')]))]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='panel', box=TOP, text='同時代の証拠は、見つかっていない', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='印刷物で確認できる最古の例は、死後100年以上あとの1757年', at=1, until=2, size=36),
   dict(t='panel', box=TOP, text='「言った証拠がない」と「言わなかった証拠がある」は別', at=2, until=3, size=38, col='gold'),
   dict(t='panel', box=TOP, text='言えるのは、地動説を信じ続けたこと。有名な言葉は、後の時代に広まった話として伝わっている', at=3, until=4, size=28),
   dict(t='panel', box=TOP, text='有名な言葉は、いつ、誰が最初に記録したかをたどると、見えてくる', at=4, size=36)]),
 ],
 desc=dict(title_main='ガリレオは「それでも地球は動く」と言ったのか', title_no=1,
  titles=['ガリレオは「それでも地球は動く」と言った？ 最古の記録を確かめる', '「それでも地球は動く」の最古の記録は、ガリレオの死の115年後だった', '有名な絵に書いてあった？ ガリレオの言葉と、19世紀の絵の謎'],
  intro='「それでも地球は動く」。ガリレオが裁判のあとにつぶやいた、とされる有名な言葉です。この動画では、天文学者マリオ・リビオの調査などを手がかりに、本当に言ったのか、最古の記録はいつか、確かめます。',
  points=['ガリレオが、1633年に異端の疑いで裁判にかけられ、地動説を撤回させられたことは、歴史の解説で述べられています。', '「それでも地球は動く」が、印刷物で確認されている最も古い例は、1757年のバレッティ『The Italian Library』です。ガリレオの死(1642年)から100年以上あとです。', '弟子ヴィヴィアーニの最初の伝記や、裁判の記録には、この言葉はないとされます。', '1911年に見つかった、この言葉が書き込まれた絵画は、1643年か1645年の作とされましたが、専門家は疑い、1837年の似た構図の絵もあります。', 'リビオは、後の時代の作り話の可能性が高いとしつつ、実際に言ったかどうかは確実ではない、と述べています。'],
  refs=['Mario Livio, "Did Galileo Truly Say, \'And Yet It Moves\'? A Modern Detective Story", Scientific American (2020):https://www.scientificamerican.com/blog/observations/did-galileo-truly-say-and-yet-it-moves-a-modern-detective-story/', 'Wikipedia「And yet it moves」(脚注:Hayton 2012、Baretti 1757 ほか):https://en.wikipedia.org/wiki/And_yet_it_moves', 'Darin Hayton, "Toward a history of \'eppur si muove\'" (2012):https://dhayton.haverford.edu/blog/2012/06/03/toward-a-history-of-eppur-si-muove/'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['バレッティ『The Italian Library』(1757)の本文、ヴィヴィアーニの伝記の本文、1633年の裁判記録は、直接確認していません。二次資料(Scientific American、Wikipedia、ヘイトン)による紹介です。', '「印刷物で確認されている最も古い例」は、未発見の手稿や私的な記録まで含めて、1757年が初出と証明されたという意味ではありません。', '絵画の専門家の判断は、写真による判断を含みます。制作年が科学的検査で最終確定したわけではありません。', '「なぜ広まったか」は、私の推測です。'],
  tags='ガリレオ, それでも地球は動く, 地動説, 科学史, 俗説, 検証, 歴史, リビオ',
  checks=['バレッティ『The Italian Library』(1757)の本文で、言い回しを確認する（諦めた:古書）', 'ヴィヴィアーニの伝記の本文を確認する（諦めた:原典）', '1633年の裁判・撤回の一次記録を確認する（諦めた:原典）']),
 thumb=dict(bg='assets/galileo/thumb_art.png', lines=[['それでも', 110, 'white'], ['地球は動く', 110, 'white'], ['本当に言った？', 100, 'gold']], sub='ガリレオの有名な言葉を確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


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
    """台本の番号つきの行（1行に複数の文がある）→ 各行の最初の文の番号（vp.py の sentences と同じく「。」で区切る）。"""
    import re
    t = (R / 'docs' / 'themes' / '20270213_galileo' / '09_script_v2.md').read_text(encoding='utf8')
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
_ART = {'intro': 'intro', 'trial': 'hall', 'first': 'books', 'painting': 'gallery', 'say': 'sky', 'why': 'intro', 'clear': 'hall', 'end': 'sky'}
if all((R / 'assets' / 'galileo' / f'art_{v}.png').exists() for v in set(_ART.values())):
    inject(spec, _ART)
(R / 'data' / 'galileo_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
