"""Writes data/seijin_spec.json（成人の日は、なぜ1月15日ではなくなった？）。台本：docs/themes/20270109_seijin/09_script_v2.md
at / until は『章内の行番号（0始まり）』。末尾で文の番号に直す。"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
R = Path(__file__).resolve().parents[1]
from specart import inject
TOP = [60, 170, 1860, 235]
spec = dict(slug='seijin', theme_dir='20270109_seijin', pack='48_seijin', header_sub='内閣府の資料と、法律の改正の記録で確かめる',
 images={},
 bgm=[['intro', 'since', 'piano36'], ['range', 'pick', 'piano12'], ['who', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='成人の日は、なぜ1月15日ではなくなった？', chapter_title='導入：成人の日は、なぜ1月15日ではなくなった？', opener='成人の日は、なぜ1月15日ではなくなった？', opener_until=1, scene=[
   dict(t='big', text='成人の日は、なぜ1月15日ではなくなった？', y=270, at=0, size=48, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='2026年は1月12日、2027年は1月11日（内閣府）', at=0, size=38, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：内閣府の資料と、法律の改正の記録', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：1998年の法律の改正で日付が変わった。目的は、連休にして余暇活動を充実させること', at=4, size=32, col='gold')]),
 dict(key='rule', title='成人の日は、何と決められているか', chapter_title='成人の日は、何と決められているか', scene=[
   dict(t='panel', box=TOP, text='まず、今の決まりを確かめる', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='内閣府の資料：成人の日は、1月の第2月曜日', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='趣旨：おとなになったことを自覚し、みずから生きぬこうとする青年を祝いはげます', at=2, until=3, size=32),
   dict(t='panel', box=TOP, text='祝日は、国民の祝日に関する法律（祝日法・昭和23年）で決められている', at=3, until=4, size=34),
   dict(t='panel', box=TOP, text='ねらい：元服や裳着の精神を生かし、青年が社会のために尽くす自覚を持つこと', at=4, until=5, size=32),
   dict(t='panel', box=TOP, text='月曜の祝日：海の日（7月第3）・敬老の日（9月第3）・スポーツの日（10月第2）', at=5, size=32),
   dict(t='table', box=[60, 300, 1860, 640], cols=['月曜日に決められている祝日（内閣府）', 'いつ'], colw=[1100, 700], size=34, rows=[
     dict(at=1, cells=['成人の日', '1月の第2月曜日'], col='gold'),
     dict(at=5, cells=['海の日', '7月の第3月曜日']),
     dict(at=5, cells=['敬老の日', '9月の第3月曜日']),
     dict(at=5, cells=['スポーツの日', '10月の第2月曜日'])])]),
 dict(key='reform', title='1998年の改正', chapter_title='1998年の改正', scene=[
   dict(t='panel', box=TOP, text='日付が変わったのは、法律が改正されたから', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='国民の祝日に関する法律の一部を改正する法律（法律第141号）', at=1, until=2, size=36, hi=True),
   dict(t='panel', box=TOP, text='平成10年（1998年）10月21日に公布', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='成人の日：「1月15日」→「1月の第2月曜日」', at=3, until=4, size=40, col='gold'),
   dict(t='panel', box=TOP, text='同じ改正で、体育の日（今のスポーツの日）も「10月の第2月曜日」に', at=4, size=34),
   dict(t='table', box=[60, 300, 1860, 600], cols=['1998年の改正（法律第141号）', ''], colw=[1000, 800], size=34, rows=[
     dict(at=2, cells=['公布', '1998年10月21日']),
     dict(at=3, cells=['成人の日', '1月15日 → 1月の第2月曜日'], col='gold'),
     dict(at=4, cells=['体育の日', '10月10日 → 10月の第2月曜日'])])]),
 dict(key='since', title='いつから変わったのか', chapter_title='いつから変わったのか', scene=[
   dict(t='panel', box=TOP, text='附則：「平成十二年一月一日から施行する」', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='つまり、2000年1月1日から', at=1, until=2, size=38),
   dict(t='panel', box=TOP, text='2000年の成人の日は1月10日（体育の日は10月9日）', at=2, until=3, size=40, col='gold'),
   dict(t='panel', box=TOP, text='1月15日が成人の日だったのは、1949年から1999年まで', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='1948年に祝日法が公布され、翌年から1月15日が成人の日（二次情報）', at=4, size=34),
   dict(t='table', box=[60, 300, 1860, 600], cols=['成人の日の日付', '期間'], colw=[800, 1000], size=34, rows=[
     dict(at=3, cells=['1月15日', '1949年〜1999年']),
     dict(at=1, cells=['1月の第2月曜日', '2000年〜（施行：2000年1月1日）'], col='gold'),
     dict(at=2, cells=['2000年の成人の日', '1月10日（国立天文台）'])])]),
 dict(key='range', title='第二月曜日は、いつからいつまでか', chapter_title='第二月曜日は、いつからいつまでか', scene=[
   dict(t='panel', box=TOP, text='第2月曜日は、いつからいつまでの間になる？', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='1月1日が月曜日 → 第2月曜日は8日', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='1月1日が火曜日 → 第1月曜日は7日、第2月曜日は14日', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='今の決まりでは、成人の日は必ず1月8日〜14日の間（自作の計算）', at=3, until=4, size=38, col='gold'),
   dict(t='panel', box=TOP, text='今の決まりでは、1月15日になることはない', at=4, size=38),
   dict(t='table', box=[60, 300, 1860, 600], cols=['1月1日が…', '第2月曜日（成人の日）'], colw=[900, 900], size=36, rows=[
     dict(at=1, cells=['月曜日', '8日']),
     dict(at=2, cells=['火曜日', '14日']),
     dict(at=3, cells=['どの曜日でも', '8日〜14日のどれか'], col='gold')])]),
 dict(key='why', title='なぜ、変えたのか', chapter_title='なぜ、変えたのか', scene=[
   dict(t='panel', box=TOP, text='では、なぜ、日付を変えたのか', at=0, until=1, size=38),
   dict(t='panel', box=TOP, text='内閣府の資料：連休にして余暇活動を充実させ、ゆとりある国民生活を実現するため', at=1, until=2, size=32, hi=True),
   dict(t='panel', box=TOP, text='月曜日にすると、土・日・月の三連休になりやすい', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='体育の日（今のスポーツの日）も、同じ時期に、10月の第2月曜日に', at=3, until=4, size=36),
   dict(t='panel', box=TOP, text='海の日・敬老の日は、平成13年の改正で、平成15年から第3月曜日に', at=4, until=5, size=34),
   dict(t='panel', box=TOP, text='この制度は「ハッピーマンデー」と呼ばれることがある（二次情報）', at=5, size=36, col='gold'),
   dict(t='table', box=[60, 300, 1860, 640], cols=['月曜に移った祝日（内閣府）', 'いつから'], colw=[1100, 700], size=34, rows=[
     dict(at=3, cells=['成人の日・体育の日（スポーツの日）', '2000年（平成12年）から'], col='gold'),
     dict(at=4, cells=['海の日・敬老の日', '2003年（平成15年）から'])])]),
 dict(key='pick', title='1月15日は、なぜ選ばれたのか', chapter_title='1月15日は、なぜ選ばれたのか', scene=[
   dict(t='panel', box=TOP, text='もともとの1月15日は、なぜ選ばれた？', at=0, until=1, size=38),
   dict(t='panel', box=TOP, text='内閣府の資料：昭和23年の当時の報告書に、説明がある', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='元服は正月に多かった。公家は正月5日まで、武家は正月11日ごろ', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='草案は、「国民の日」の立場から、それらの日を避け、松の内の15日を選んだ', at=3, until=4, size=32, col='gold'),
   dict(t='panel', box=TOP, text='成人式のルーツ：1946年、埼玉県蕨町の青年祭が有力（二次情報）', at=4, size=34),
   dict(t='table', until=4, box=[60, 300, 1860, 640], cols=['元服の日取り（内閣府・昭和23年の報告書）', '日'], colw=[1200, 600], size=34, rows=[
     dict(at=2, cells=['公家', '正月5日まで']),
     dict(at=2, cells=['武家', '正月11日ごろ']),
     dict(at=3, cells=['草案が選んだ日（松の内）', '1月15日'], col='gold')])]),
 dict(key='who', title='成人式は、誰が決めているのか', chapter_title='成人式は、誰が決めているのか', scene=[
   dict(t='panel', box=TOP, text='成人式は、法律で決められている？', at=0, until=1, size=38),
   dict(t='panel', box=TOP, text='成人の日は祝日法。成人式の日取りや対象年齢は、法律では決まっていない', at=1, until=2, size=32, hi=True),
   dict(t='panel', box=TOP, text='各自治体が、それぞれ決めている（二次情報）', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='2022年4月1日に、成人年齢が18歳に引き下げられた', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='それでも、対象を20歳のままにしている自治体がある。「二十歳のつどい」などに改称した例も', at=4, until=5, size=32, col='gold'),
   dict(t='panel', box=TOP, text='18歳を対象に開いた自治体も、あったとされる。対象は自治体の案内で確かめられる', at=5, size=32),
   dict(t='table', box=[60, 300, 1860, 600], cols=['成人式（自治体の公表の例）', ''], colw=[1000, 800], size=34, rows=[
     dict(at=2, cells=['日取り・対象年齢', '各自治体が決める']),
     dict(at=4, cells=['成年年齢が18歳になった後', '20歳対象のままの自治体がある'], col='gold'),
     dict(at=5, cells=['18歳を対象にした自治体', 'あったとされる']
     )])]),
 dict(key='know', title='わかることと、わからないこと', chapter_title='わかることと、わからないこと', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='わかること', title_at=0, items=[
      dict(at=0, text='1998年の改正で、成人の日は1月の第2月曜日に'),
      dict(at=1, text='施行は2000年1月1日')]),
     right=dict(title='わからないこと', title_at=2, items=[
      dict(at=2, text='国会での審議の、細かい内容'),
      dict(at=3, text='自治体ごとの成人式の対象（一部の例だけ確認）')]))]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=0, items=[
      dict(at=1, text='1998年の祝日法の改正で「1月の第2月曜日」に。施行は2000年1月1日'),
      dict(at=2, text='目的：連休にして余暇を充実。1月15日は、元服の日取りを避けて、松の内から選ばれた')]),
     right=dict(title='言い方の注意', title_at=3, items=[
      dict(at=3, text='成人式の日取りや対象年齢は、法律ではなく、自治体が決める')]))]),
 ],
 desc=dict(title_main='成人の日はなぜ1月15日ではなくなったのか', title_no=1,
  titles=['成人の日は、なぜ1月15日ではなくなった？ 内閣府の資料と法改正で確かめる', '成人の日が1月第2月曜日になった理由：1998年の祝日法改正と2000年の施行', '成人の日の「1月15日」はなぜ選ばれ、なぜ変わった？ ハッピーマンデーの確かめ方'],
  intro='成人の日は、昔は1月15日でした。なぜ、1月15日ではなくなったのでしょうか。この動画では、内閣府の資料と、法律の改正の記録で確かめます。',
  points=['成人の日は、祝日法第2条で「1月の第2月曜日」と決められています(内閣府)。', '1998年(平成10年)10月21日公布の祝日法の改正(法律第141号)で、「1月15日」から「1月の第2月曜日」に変わりました。施行は2000年(平成12年)1月1日です。', '改正の理由は、連休にして余暇活動を充実させ、ゆとりある国民生活を実現するため(内閣府)。', '1948年に1月15日とされた理由は、元服は正月に多く、公家は5日まで、武家は11日ごろだったため、それらを避けて松の内の15日を選んだ、と内閣府の資料にあります(昭和23年の参議院文化委員会の報告書)。', '成人式の日取りや対象年齢は、法律では決められておらず、各自治体が決めています。'],
  refs=['内閣府「国民の祝日について」:https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html', '内閣府「各「国民の祝日」について」:https://www8.cao.go.jp/chosei/shukujitsu/gaiyou/kaku.html', '国民の祝日に関する法律の一部を改正する法律(法律第141号。名古屋大学 法令データベース):https://jahis.law.nagoya-u.ac.jp/lawdb/l/410a0141', '国立天文台暦計算室「国民の祝日」:https://eco.mtk.nao.ac.jp/koyomi/topics/html/topics2000.html', 'Wikipedia「成人式」(二次情報。蕨町の青年祭など):https://ja.wikipedia.org/wiki/%E6%88%90%E4%BA%BA%E5%BC%8F'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['「第2月曜日は必ず1月8日〜14日」、「1月15日だったのは1949年から1999年まで」は、法律の改正の記録からの自作の確認・計算です。', '蕨町の青年祭、1949年から1月15日、2022年の成年年齢の引き下げ後の自治体の対応は、Wikipediaや自治体の公表による二次情報です。', '国会での審議の細かい内容、自治体ごとの成人式の対象の全体は、確かめていません。'],
  tags='成人の日, 成人式, 祝日, ハッピーマンデー, 祝日法, 内閣府, 検証, 暦',
  checks=['祝日法第2条の条文を、e-Gov法令検索で直接確認する', '国会会議録(1998年10月7日の衆議院本会議)で、改正の趣旨説明を確認する', '自治体の成人式の対象年齢(2027年1月時点)を、最新の自治体の案内で確認する']),
 thumb=dict(bg='assets/seijin/thumb_art.png', lines=[['成人の日', 120, 'white'], ['なぜ1月15日', 90, 'white'], ['じゃない？', 120, 'gold']], sub='内閣府の資料で確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=38, shade_x=700, shade_w=520))


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
    t = (R / 'docs' / 'themes' / '20270109_seijin' / '09_script_v2.md').read_text(encoding='utf8')
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
_ART = {'intro': 'intro', 'rule': 'hall', 'reform': 'desk', 'since': 'desk', 'range': 'desk', 'why': 'hall', 'pick': 'shrine', 'who': 'hall', 'know': 'shrine', 'end': 'intro'}
if all((R / 'assets' / 'seijin' / f'art_{v}.png').exists() for v in set(_ART.values())):
    inject(spec, _ART)
(R / 'data' / 'seijin_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
