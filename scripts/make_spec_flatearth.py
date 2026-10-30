"""Writes data/flatearth_spec.json（中世の人は、地球が平らだと信じていた？）。台本：docs/themes/20261227_flatearth/09_script_v2.md"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from specart import inject, inject2
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]
L = [60, 300, 930, 520]; Rt = [990, 300, 1860, 520]
spec = dict(slug='flatearth', theme_dir='20261227_flatearth', pack='31_flatearth', header_sub='中世の学者の本で、「平らな地球」の話を確かめる',
 images={},
 bgm=[['intro', 'irving', 'piano36'], ['textbook', 'spread', 'piano12'], ['columbus', 'outro', 'piano40']],
 chapters=[
 dict(key='intro', title='中世の人は、地球が平らだと信じていた？', chapter_title='導入：中世の人は、地球が平らだと信じていた？', opener='中世の人は、地球が平らだと信じていた？', opener_until=1, scene=[
   dict(t='big', text='地球は、平らだと信じられていた？', y=270, at=0, size=58, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='コロンブスは、平らだと信じる人たちと戦った？', at=1, size=42, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：中世の学者が書いた本', at=2, size=38),
   dict(t='panel', box=[120, 750, 1800, 830], text='答えは、学者の本の中では、ほぼ逆', at=3, size=40, col='gold')]),
 dict(key='irving', title='この話は、どこから来たのか', chapter_title='この話は、どこから来たのか', scene=[
   dict(t='panel', box=TOP, text='この話の出どころは？', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='1828年：アーヴィングが、コロンブスの伝記を書いた', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='スペインのサラマンカで、学者たちが、コロンブスに反対する場面', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='聖書の比喩を根拠に、地球は平らだと主張する学者がいた（アーヴィングの記述）', at=3, until=4, size=32, col='gold'),
   dict(t='panel', box=TOP, text='この議論の出典は、この動画で確認した本文では見つからなかった', at=4, size=38)]),
 dict(key='textbook', title='中世の教科書を読む', chapter_title='中世の教科書を読む', scene=[
   dict(t='panel', box=TOP, text='中世の学者は、何を教えていたのか', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='サクロボスコ『天球論』（1230年ごろ・天文学の入門書）', at=1, until=2, size=38),
   dict(t='panel', box=TOP, text='節の題：Quod terra sit rotunda ＝ 地球が丸いこと', at=2, until=3, size=38, hi=True),
   dict(t='panel', box=TOP, text='理由1：星の昇り沈みは、東の人ほど早い', at=3, until=4, size=40),
   dict(t='panel', box=TOP, text='理由2：同じ月食でも、東では日が先に沈み、夜の時刻が先に進む', at=4, until=5, size=36),
   dict(t='panel', box=TOP, text='船の上：低い位置では見えない港の目印も、マストの上では見える', at=5, until=6, size=36),
   dict(t='panel', box=TOP, text='平らに見えるのは、地球があまりに大きいから', at=6, size=40, col='gold'),
   dict(t='chips', y=330, w=520, h=150, gap=60, size=40, items=[dict(at=3, text='星の昇り沈み'), dict(at=4, text='月食'), dict(at=5, text='遠ざかる船')])]),
 dict(key='aquinas', title='神学者も、丸いと書いていた', chapter_title='神学者も、丸いと書いていた', scene=[
   dict(t='panel', box=TOP, text='13世紀：トマス・アクィナス『神学大全』', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='学問の違いを説明する一節', at=1, until=2, size=40),
   dict(t='panel', box=TOP, text='例：地球が丸いこと（天文学者は数学で、自然学者は物の性質で、証明できる）', at=2, until=3, size=32, hi=True),
   dict(t='panel', box=TOP, text='地球が丸いことが、前提のように使われている', at=3, size=40, col='gold')]),
 dict(key='oppose', title='反対した人は、いなかったのか', chapter_title='反対した人は、いなかったのか', scene=[
   dict(t='panel', box=TOP, text='地球の形に、反対した人はいなかったのか', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='5世紀：アウグスティヌスは、反対側に人が住むことに反対', at=1, until=2, size=38),
   dict(t='panel', box=TOP, text='丸いことは、仮に認めた上での議論（『神の国』第16巻第9章）', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='古代の終わりごろ：ラクタンティウスは、はっきり反対', at=3, until=4, size=38, hi=True),
   dict(t='panel', box=TOP, text='天が丸い→地球も丸い、という推論そのものを誤りだと言う（『神的教え』第3巻第24章）', at=4, until=5, size=30),
   dict(t='panel', box=TOP, text='この動画で読んだ中で、はっきり反対したのは、この一人', at=5, size=38, col='gold'),
   dict(t='panel', box=L, title='アウグスティヌス（5世紀）', text='反対側に人が住むことに反対。丸さは、仮に認めた上での議論', at=2, size=34, hi=True),
   dict(t='panel', box=Rt, title='ラクタンティウス（古代の終わりごろ）', text='球形説そのものに反対した', at=4, size=34, col='gold')]),
 dict(key='spread', title='なぜ、平らな地球の話が広まったのか', chapter_title='なぜ、「平ら」の話が広まったのか', scene=[
   dict(t='panel', box=TOP, text='それでも、平らな地球の話は、広まった', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='百科事典が紹介するラッセルの整理：この歴史像は19世紀に広まった', at=1, until=2, size=36),
   dict(t='panel', box=TOP, text='アーヴィングの本（1828年）も、その一つ', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='1834年 ルトロンヌ：古い教会の著作家は、平らな地球を信じたと主張', at=3, until=4, size=34),
   dict(t='panel', box=TOP, text='ドレイパーとホワイト：科学と宗教は戦ってきた、という見方で広めた', at=4, size=36, col='gold'),
   dict(t='chips', y=330, w=400, h=150, gap=50, size=36, items=[dict(at=2, text='1828 アーヴィング'), dict(at=3, text='1834 ルトロンヌ'), dict(at=4, text='1874 ドレイパー'), dict(at=4, text='1896 ホワイト')])]),
 dict(key='columbus', title='コロンブスの時代の、本当の論点', chapter_title='コロンブスの時代の、本当の論点', scene=[
   dict(t='panel', box=TOP, text='コロンブスと学者は、何でもめたのか', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='論点は、地球の形ではなく、大きさと距離', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='コロンブス：地球の大きさを、実際より小さく見積もった', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='アジアが東に広がる距離も、大きく見積もった', at=3, until=4, size=40),
   dict(t='panel', box=TOP, text='地球の大きさは、紀元前3世紀に、エラトステネスが計算（学者には知られていた）', at=4, until=5, size=30),
   dict(t='panel', box=TOP, text='西へ向かう距離を短く見積もったので、計画は実現しにくいと判断された', at=5, until=6, size=34),
   dict(t='panel', box=TOP, text='結果：コロンブスの見積もりは、間違いだった', at=6, size=40, col='gold'),
   dict(t='panel', box=L, title='学者が知っていたこと', text='地球は丸い。大きさも、計算されていた', at=4, size=36, hi=True),
   dict(t='panel', box=Rt, title='コロンブスの見積もり', text='地球を小さく、アジアの東の広がりを大きく見積もり、西への距離を短く見た', at=5, size=30, col='gold')]),
 dict(key='end', title='分かること、決められないこと', chapter_title='結論：分かること、決められないこと', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=0, text='中世の学者の教科書は、地球が丸いと説明していた'),
      dict(at=1, text='反対側に人が住むことに反対した人も、丸さは仮に認めて論じた'),
      dict(at=2, text='球形説にはっきり反対した人もいた'),
      dict(at=3, text='この整理では、「中世は平らな地球を信じた」という歴史像は、19世紀の本で広まった')]),
     right=dict(title='決められないこと', title_at=4, items=[
      dict(at=4, text='当時の一般の人々が、実際に何を信じていたか'),
      dict(at=5, text='サラマンカの会議で平らな地球が論じられたという話は、アーヴィングの本のほかに確かめられていない')]))]),
 dict(key='outro', title='おわりに', chapter_title='おわりに', scene=[
   dict(t='big', text='中世の人は、地球が平らだと信じていた？', y=250, at=0, size=50, col='gold'),
   dict(t='panel', box=[120, 400, 1800, 520], text='学者の教科書では、地球は、丸いものとして説明されていた', at=1, size=40, hi=True),
   dict(t='panel', box=[120, 580, 1800, 700], text='この整理では、「平らな地球」の話のほうが、19世紀に広まった話だった', at=2, size=40, col='gold')])
 ],
 desc=dict(title_main='中世の人は、地球が平らだと信じていたのか', title_no=1,
  titles=['中世の人は、地球が平らだと信じていた？ 学者の本で確かめる', '平らな地球は、中世の常識？ サクロボスコ・アクィナスの原典を読む', 'コロンブスと「平らな地球」の誤解：中世の教科書には何と書いてあったか'],
  intro='「中世の人は、地球が平らだと信じていた」「コロンブスは、それと戦った」。そんな話を、聞いたことはないでしょうか。この動画では、中世の学者が書いた本(サクロボスコ『天球論』、トマス・アクィナス『神学大全』など)を読んで、実際に何と書いてあったかを確かめます。',
  points=['サクロボスコ『天球論』(1230年ごろ)には、「地球が丸いこと」という節があり、星の昇り沈み・月食・船の見え方で、地球が丸いことを説明しています(この動画では、1478年ヴェネツィア版のラテン語・ポルトガル語対訳を読みました)。', 'トマス・アクィナス『神学大全』(第1部第1問第1項)は、地球が丸いことを、学問の違いを説明する例として使っています。', 'アウグスティヌス『神の国』第16巻第9章は、反対側に人が住むことに反対しましたが、世界が丸いとしても、という条件つきの議論です。', 'ラクタンティウス『神的教え』第3巻第24章は、球形説そのものを批判しました。この動画で読んだ中で、はっきり反対したのはこの一人です。', '「中世の人は平らな地球を信じていた」という歴史像は、アーヴィングの『コロンブス伝』(1828年)など、19世紀の本で広まったとされます(歴史家ラッセルの整理)。', 'コロンブスと学者の論点は、地球の形ではなく、大きさと距離だったと考えられています。'],
  refs=['Johannes de Sacrobosco『Tractatus de sphaera』(1478年ヴェネツィア版・ラテン語/ポルトガル語対訳、カンピーナス大学):https://www.ghtc.usp.br/server/pdf/Sacrobosco-1478-trad.pdf', 'Thomas Aquinas『Summa Theologiae』第1部第1問(英訳、New Advent):https://www.newadvent.org/summa/1001.htm', 'Augustine『The City of God』第16巻(英訳、New Advent):https://www.newadvent.org/fathers/120116.htm', 'Lactantius『The Divine Institutes』第3巻(英訳、New Advent):https://www.newadvent.org/fathers/07013.htm', 'Washington Irving『The Life and Voyages of Christopher Columbus』(1893年版の全文、Internet Archive):https://archive.org/details/lifevoyagesofchr00ir', 'Jeffrey Burton Russell『Inventing the Flat Earth: Columbus and Modern Historians』(Praeger, 1991)。この動画では、この本そのものではなく、次の記事の要約を通して確認しました:https://en.wikipedia.org/wiki/Myth_of_the_flat_Earth'],
  credit_lines=['・図:自作(原典の記述をまとめた図です)', '・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実際の人物・場面・資料の再現ではありません)'],
  notes=['この動画で確かめたのは、中世の学者が書いた本の記述です。当時の一般の人々が何を信じていたかは、この資料からは分かりません。', 'アーヴィングの本は、1893年版の本文で読みました。1828年の初版との違いは確認していません。', 'ラッセル、ルトロンヌ、ドレイパー、ホワイトについては、原典ではなく、百科事典の要約を通して確認しました。', 'コロンブスの地球の大きさの見積もりは、資料によって数字が異なるため、割合は言っていません。', 'アクィナス・アウグスティヌス・ラクタンティウスは、英訳(New Advent)で読みました。ラテン語の原文との照合はしていません。', 'ベーダなど、本文を確認できなかった著作は、取り上げていません。'],
  tags='中世, 地球, 平らな地球, コロンブス, サクロボスコ, アクィナス, 歴史, 科学史, 俗説, 検証',
  checks=['ラッセル『平らな地球の発明』の本文で、台本の整理(19世紀に広まった等)を確認する(docs/themes/20261227_flatearth/08_fact_check.md)', 'アーヴィング初版(1828年)のサラマンカの場面と、1893年版の違いを確認する', 'サクロボスコ『天球論』の1230年ごろの写本・校訂本(Thorndike 1949)で、月食の記述を確認する']),
 thumb=dict(bg='assets/flatearth/thumb_art.png', lines=[['中世の人は', 100, 'white'], ['地球が平ら', 100, 'white'], ['と信じた？', 130, 'gold']], sub='学者の本で確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


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
    t = (R / 'docs' / 'themes' / '20261227_flatearth' / '09_script_v2.md').read_text(encoding='utf8')
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
            if k in ('at', 'until', 'title_at') and isinstance(v, int): o[k] = f(v)
            else: _remap(v, st)
    elif isinstance(o, list):
        for v in o: _remap(v, st)


_S = _line_to_sentence_starts()
assert len(_S) == len(spec['chapters']), (len(_S), len(spec['chapters']))
for _ch, _st in zip(spec['chapters'], _S):
    _remap(_ch['scene'], _st)
    if 'opener_until' in _ch: _ch['opener_until'] = _st[min(_ch['opener_until'], len(_st) - 1)]

_fit(spec)
inject(spec, {'intro': 'intro', 'irving': 'press', 'textbook': 'book', 'aquinas': 'book', 'oppose': 'intro', 'spread': 'press', 'columbus': 'map', 'end': 'intro', 'outro': 'intro'})
_tb = _S[2]
inject2(spec, {'textbook': ('ship', _tb[5])})
(R / 'data' / 'flatearth_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
