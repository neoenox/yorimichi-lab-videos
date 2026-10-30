"""Writes data/takarakuji_spec.json（宝くじは、買ったお金の何割が、当せん金になる？）。台本：docs/themes/20270220_takarakuji/09_script_v2.md
at / until は『章内の行番号（0始まり）』。末尾で文の番号に直す。"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
R = Path(__file__).resolve().parents[1]
from specart import inject
TOP = [60, 170, 1860, 235]
spec = dict(slug='takarakuji', theme_dir='20270220_takarakuji', pack='45_takarakuji', header_sub='宝くじ公式サイトの数字で、お金の行き先を確かめる',
 images={},
 bgm=[['intro', 'money', 'piano36'], ['per100', 'law', 'piano12'], ['use', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='宝くじは、何割が当せん金になる？', chapter_title='導入：宝くじは、買ったお金の何割が当せん金？', opener='宝くじ、買ったお金の何割が当せん金？', opener_until=1, scene=[
   dict(t='big', text='宝くじ、買ったお金の何割が戻る？', y=270, at=0, size=54, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='当せん金として、何割が払われている？', at=1, size=44, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：宝くじ公式サイトの数字（令和6年度）', at=2, size=36),
   dict(t='panel', box=[120, 750, 1800, 830], text='答え：全体の46.5％。百円につき、約46円', at=3, size=40, col='gold'),
   dict(t='panel', box=[120, 860, 1800, 940], text='買う・買わないを決める動画ではない', at=4, size=36)]),
 dict(key='money', title='お金の行き先', chapter_title='お金の行き先', scene=[
   dict(t='panel', box=TOP, text='令和6年度の販売実績額：7,598億円（宝くじ公式サイト）', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='当せん金：3,529億円（公式の表記で46.5％）', at=1, until=2, size=40),
   dict(t='panel', box=TOP, text='収益金：2,750億円（36.2％）', at=2, until=3, size=42),
   dict(t='panel', box=TOP, text='印刷・売りさばき手数料などの経費：1,218億円（16.0％）', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='社会貢献広報費：101億円（1.3％）', at=4, until=5, size=42),
   dict(t='panel', box=TOP, text='四つの合計＝7,598億円。販売実績額と一致', at=5, size=40, col='gold'),
   dict(t='bars', box=[60, 300, 1860, 640], title='販売実績額7,598億円の内訳（令和6年度）', unit='％', max=50, lab_w=560, data=[dict(at=1, label='当せん金（3,529億円）', value=46.5, vlabel='46.5％', col='gold'), dict(at=2, label='収益金（2,750億円）', value=36.2, vlabel='36.2％', col='blue'), dict(at=3, label='経費（1,218億円）', value=16.0, vlabel='16.0％', col='blue'), dict(at=4, label='社会貢献広報費（101億円）', value=1.3, vlabel='1.3％', col='blue')])]),
 dict(key='per100', title='百円あたりに、直すと', chapter_title='百円あたりに、直すと', scene=[
   dict(t='panel', box=TOP, text='大きな数字は、百円あたりに直すとわかりやすい', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='当せん金 約46円／収益金 約36円／経費 16円／広報費 約1円', at=1, until=2, size=36),
   dict(t='panel', box=TOP, text='この割合は、令和6年度の、宝くじ全体の数字', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='300円のくじにあてはめると、当せん金は約140円という「目安」', at=3, until=4, size=36, col='gold'),
   dict(t='panel', box=TOP, text='ジャンボ・ロト・ナンバーズなど商品ごとの割合は未確認。個々の期待値ではない', at=4, size=32),
   dict(t='bars', box=[60, 300, 1860, 640], title='百円あたりの行き先（令和6年度・全体。自作の換算）', unit='円', max=50, lab_w=520, data=[dict(at=1, label='当せん金', value=46.5, vlabel='約46円', col='gold'), dict(at=1, label='収益金', value=36.2, vlabel='約36円', col='blue'), dict(at=1, label='経費', value=16.0, vlabel='16円', col='blue'), dict(at=1, label='社会貢献広報費', value=1.3, vlabel='約1円', col='blue')])]),
 dict(key='diff', title='「割合」と「一人ひとりの結果」は、違う', chapter_title='「割合」と「一人ひとりの結果」は、違う', scene=[
   dict(t='panel', box=TOP, text='46.5％＝売り上げ全体に対する、当せん金全体の割合', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='買った人みんなが、百円につき46円ずつ戻る、という意味ではない', at=1, until=2, size=36),
   dict(t='panel', box=TOP, text='多くは当たらないか小さな金額。ごく少数に、大きな金額が当たる', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='例：ロト6（1口200円）。43個から6個を選ぶ', at=3, until=4, size=38, hi=True),
   dict(t='panel', box=TOP, text='確率が小さいぶん、当たったときの金額は大きい。結果の幅は広い', at=4, size=36, col='gold'),
   dict(t='table', box=[60, 300, 1860, 680], cols=['ロト6（自作の計算）', ''], colw=[760, 1040], size=34, rows=[
     dict(at=3, cells=['1口の値段', '200円']),
     dict(at=3, cells=['数字の選び方', '43個から6個']),
     dict(at=3, cells=['組み合わせ', '6,096,454通り']),
     dict(at=3, cells=['一等の確率', '1／6,096,454'], col='gold')])]),
 dict(key='law', title='法律と、公式の説明', chapter_title='法律と、公式の説明', scene=[
   dict(t='panel', box=TOP, text='当せん金付証票法：当せん金の総額は発売総額の5割を超えない（原則。二次情報）', at=0, until=1, size=30),
   dict(t='panel', box=TOP, text='令和6年度の46.5％は、5割より小さい数字', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='公式サイトの説明：売り上げの約40％が、公共事業などに使われる', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='実績の収益金は36.2％。「約40％」の説明とは少し違う。動画では実績の数字を使う', at=3, size=30, col='gold'),
   dict(t='table', box=[60, 300, 1860, 680], cols=['', '数字', '出どころ'], colw=[620, 360, 820], size=32, rows=[
     dict(at=0, cells=['当せん金の上限（原則）', '5割', '当せん金付証票法（二次情報）']),
     dict(at=1, cells=['令和6年度の当せん金', '46.5％', '公式サイト'], col='gold'),
     dict(at=2, cells=['公式の説明（収益金）', '約40％', '公式サイト']),
     dict(at=3, cells=['令和6年度の収益金（実績）', '36.2％', '公式サイト'], col='gold')])]),
 dict(key='use', title='収益金は、何に使われるか', chapter_title='収益金は、何に使われるか', scene=[
   dict(t='panel', box=TOP, text='収益金は、発売元の全国の都道府県と、20の指定都市に納められる', at=0, until=1, size=36, hi=True),
   dict(t='panel', box=TOP, text='公式サイトの使い道の例：高齢化・少子化対策、防災対策、公園整備', at=1, until=2, size=34),
   dict(t='panel', box=TOP, text='ほかに：教育施設・社会福祉施設の建設・改修、東日本大震災の復興支援', at=2, until=3, size=32),
   dict(t='panel', box=TOP, text='使い道の効果、金額の内訳は、この動画では未確認', at=3, size=38, col='gold'),
   dict(t='table', box=[60, 300, 1860, 700], cols=['公式サイトが挙げる使い道の例', ''], colw=[1500, 300], size=32, rows=[
     dict(at=1, cells=['高齢化・少子化対策', '']),
     dict(at=1, cells=['防災対策', '']),
     dict(at=1, cells=['公園整備', '']),
     dict(at=2, cells=['教育施設・社会福祉施設の建設・改修', '']),
     dict(at=2, cells=['東日本大震災の復興支援', ''])])]),
 dict(key='year', title='別の年と、比べると', chapter_title='別の年と、比べると', scene=[
   dict(t='panel', box=TOP, text='令和4年度：販売実績額8,324億円、当せん金3,904億円（還元率46.9％）', at=0, until=1, size=34, hi=True),
   dict(t='panel', box=TOP, text='自治体の資料と報道で確認。公式サイトの当時のページは未確認', at=1, until=2, size=36),
   dict(t='panel', box=TOP, text='令和6年度の46.5％と近い。年によって、少し動くと考えられる', at=2, until=3, size=36, col='gold'),
   dict(t='panel', box=TOP, text='平成から令和への長い推移は、未確認', at=3, size=40),
   dict(t='table', box=[60, 300, 1860, 640], cols=['年度', '販売実績額', '当せん金', '還元率'], colw=[560, 480, 480, 340], size=34, rows=[
     dict(at=0, cells=['令和4年度（二次情報）', '8,324億円', '3,904億円', '46.9％']),
     dict(at=2, cells=['令和6年度（公式）', '7,598億円', '3,529億円', '46.5％'], col='gold')])]),
 dict(key='know', title='数字からわかることと、わからないこと', chapter_title='数字からわかることと、わからないこと', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=0, text='令和6年度の全体で、売り上げの約半分が当せん金、約3割強が収益金')]),
     right=dict(title='分からないこと', title_at=1, items=[
      dict(at=1, text='商品ごとの割合。一人ひとりが、いくら戻るか（運で決まる）'),
      dict(at=2, text='収益金の使い道の効果')]))]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=0, items=[
      dict(at=0, text='令和6年度の全体：当せん金46.5％（百円につき約46円）'),
      dict(at=1, text='収益金36.2％、経費16.0％'),
      dict(at=2, text='これは全体の割合。一人ひとりの結果は大きく違う')]),
     right=dict(title='言い方の注意', title_at=3, items=[
      dict(at=3, text='買う・買わないは、数字を知ったうえで、それぞれが決める'),
      dict(at=4, text='やめられなくなったら、精神保健福祉センターなどに相談できる')]))]),
 ],
 desc=dict(title_main='宝くじは、買ったお金の何割が当せん金になるのか', title_no=1,
  titles=['宝くじは、買ったお金の何割が当せん金になる？ 公式サイトの数字で確かめる', '宝くじの売り上げの行き先：当せん金46.5％、収益金36.2％（令和6年度）', '宝くじ300円で、当せん金は約140円？ 「全体の割合」と「一人ひとりの結果」'],
  intro='宝くじを買うとき、買ったお金のうち、何割が当せん金として払われているのでしょうか。この動画では、宝くじ公式サイトの令和6年度の数字で、お金の行き先を確かめます。買うことをすすめる・止める動画ではありません。',
  points=['令和6年度の販売実績額は7,598億円。当せん金は3,529億円(46.5％)、収益金は2,750億円(36.2％)、経費は1,218億円(16.0％)、社会貢献広報費は101億円(1.3％)でした。', '百円あたりに直すと、当せん金は約46円です。300円のくじにあてはめた約140円は、全体の割合をあてはめた目安で、個々の商品の期待値ではありません。', '46.5％は、売り上げ全体に対する当せん金全体の割合で、一人ひとりに戻る額ではありません。', '収益金は、全国の都道府県と20の指定都市に納められ、公共事業などに使われます。使い道の効果までは確かめていません。', 'ロト6の一等の確率は、43個から6個を選ぶ6,096,454通りの1です(自作の計算)。'],
  refs=['宝くじ公式サイト「収益金」:https://www.takarakuji-official.jp/about/proceeds/top.html', '当せん金付証票法(e-Gov法令検索):https://laws.e-gov.go.jp/law/323AC0000000144', 'ギャンブル等依存症の相談窓口の探し方(厚生労働省リーフレット):https://izonsho.mhlw.go.jp/pdf/leaf_gbl.pdf'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['百円あたりの金額、300円への換算(約140円)、ロト6の組み合わせ数は、公表値からの自作の計算です。公式サイトの表示金額で割ると当せん金は46.4%台ですが、公式の表記は46.5％です。', '当せん金付証票法の上限(原則5割、例外あり)と、令和4年度の数字(和歌山県「2023宝くじのしおり」と2023年の報道)は二次情報です。公式サイトの過去ページ、商品別の還元率は確認できていません。', 'やめられなくなったときは、お住まいの都道府県・指定都市の精神保健福祉センターなどに相談できます(案内先は厚生労働省などで確認してください)。'],
  tags='宝くじ, ジャンボ, ロト6, 当せん金, 還元率, 収益金, 検証, お金',
  checks=['宝くじ公式サイトの過去年度のページで、令和4年度などの数字を確認する', '商品別(ジャンボ・ロト・ナンバーズ)の還元率が公式に出ていれば追記する']),
 thumb=dict(bg='assets/takarakuji/thumb_art.png', lines=[['宝くじ', 120, 'white'], ['何割が', 110, 'white'], ['当せん金？', 120, 'gold']], sub='公式の数字で確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


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
    t = (R / 'docs' / 'themes' / '20270220_takarakuji' / '09_script_v2.md').read_text(encoding='utf8')
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
_ART = {'intro': 'intro', 'money': 'counter', 'per100': 'coins', 'diff': 'coins', 'law': 'counter', 'use': 'city', 'year': 'counter', 'know': 'coins', 'end': 'intro'}
if all((R / 'assets' / 'takarakuji' / f'art_{v}.png').exists() for v in set(_ART.values())):
    inject(spec, _ART)
(R / 'data' / 'takarakuji_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
