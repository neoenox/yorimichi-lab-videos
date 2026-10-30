"""Writes data/frequency_spec.json（日本の電気は、なぜ東と西で周波数が違う？）。台本：docs/themes/20270116_frequency/09_script_v2.md
at / until は『章内の行番号（0始まり）』。末尾で文の番号に直す。"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
R = Path(__file__).resolve().parents[1]
from specart import inject
TOP = [60, 170, 1860, 235]
spec = dict(slug='frequency', theme_dir='20270116_frequency', pack='49_frequency', header_sub='電力会社の資料で、東西の周波数の違いを確かめる',
 images={},
 bgm=[['intro', 'meiji', 'piano36'], ['nen', 'border', 'piano12'], ['kaden', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='日本の電気は、なぜ東と西で違う？', chapter_title='導入：日本の電気は、なぜ東と西で周波数が違う？', opener='電気の周波数は、なぜ東と西で違う？', opener_until=1, scene=[
   dict(t='big', text='電気の周波数は、なぜ東と西で違う？', y=270, at=0, size=50, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='東日本は50ヘルツ、西日本は60ヘルツ（北海道電力NW）', at=1, size=38, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：電力会社・送配電事業者の資料', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 860], text='答え：明治時代に、輸入した発電機が、東京と大阪で違ったから', at=4, size=34, col='gold')]),
 dict(key='define', title='周波数とは、何か', chapter_title='周波数とは、何か', scene=[
   dict(t='panel', box=TOP, text='まず、「周波数」という言葉を確かめる', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='コンセントから来る電気は「交流」と呼ばれる（関西電力）', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='交流：電気の向きと強さが、波のように周期的に変わる', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='周波数＝1秒間に、その波が繰り返される回数。単位はヘルツ（Hz）', at=3, until=4, size=34, col='gold'),
   dict(t='panel', box=TOP, text='50ヘルツなら1秒間に50回、60ヘルツなら60回', at=4, until=5, size=38),
   dict(t='panel', box=TOP, text='世界のほとんどの国は、50か60のどちらか。2つが同じ国にあるのは、世界でもめずらしい', at=5, size=30),
   dict(t='table', box=[60, 300, 1860, 560], cols=['周波数（自作のまとめ）', '1秒間に波が繰り返される回数'], colw=[760, 1040], size=34, rows=[
     dict(at=4, cells=['50ヘルツ', '50回']),
     dict(at=4, cells=['60ヘルツ', '60回'], col='gold')])]),
 dict(key='meiji', title='明治時代の発電機', chapter_title='明治時代の発電機', scene=[
   dict(t='panel', box=TOP, text='日本で電気が使われ始めたのは、明治時代', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='そのころの日本は、発電機を外国から輸入していた', at=1, until=2, size=40),
   dict(t='panel', box=TOP, text='東京：ドイツ製の発電機 → 50ヘルツの電気', at=2, until=3, size=40, col='gold'),
   dict(t='panel', box=TOP, text='大阪：アメリカ製の発電機 → 60ヘルツの電気', at=3, until=4, size=40, col='gold'),
   dict(t='panel', box=TOP, text='東京・大阪を中心に、それぞれが全国に広がった（関西電力）', at=4, size=36),
   dict(t='table', box=[60, 300, 1860, 560], cols=['明治に輸入された発電機（関西電力）', '電気の周波数'], colw=[1100, 700], size=36, rows=[
     dict(at=2, cells=['東京：ドイツ製', '50ヘルツ'], col='gold'),
     dict(at=3, cells=['大阪：アメリカ製', '60ヘルツ'], col='gold')])]),
 dict(key='nen', title='年やメーカーは、どう言われているか', chapter_title='年やメーカーは、どう言われているか', scene=[
   dict(t='panel', box=TOP, text='解説記事には、もう少し細かい話もある（二次情報）', at=0, until=1, size=38),
   dict(t='panel', box=TOP, text='東京電灯はドイツのメーカー、大阪電灯はアメリカのメーカーの発電機、とされる', at=1, until=2, size=32, hi=True),
   dict(t='panel', box=TOP, text='導入した年は、明治20年代〜30年ごろまで、資料で違う。最初の導入か、あとの設備かでも違うようだ', at=2, until=3, size=28),
   dict(t='panel', box=TOP, text='一次の資料では未確認。確かな範囲は「東京はドイツ製、大阪はアメリカ製」まで', at=3, size=32, col='gold')]),
 dict(key='tougou', title='なぜ、統一されなかったのか', chapter_title='なぜ、統一されなかったのか', scene=[
   dict(t='panel', box=TOP, text='周波数が違うと、使えない・故障する電気製品がある（関西電力）', at=0, until=1, size=34, hi=True),
   dict(t='panel', box=TOP, text='約100年前から、周波数を1つに決めようと、何度も話し合われた', at=1, until=2, size=36),
   dict(t='panel', box=TOP, text='しかし、うまくいかなかった', at=2, until=3, size=40, col='gold'),
   dict(t='panel', box=TOP, text='詳しい理由は、今回確認した資料では確かめられなかった', at=3, until=4, size=36),
   dict(t='panel', box=TOP, text='背景として、設備や製品がすでに広く使われていたことが考えられる（自作の推測）', at=4, size=30)]),
 dict(key='border', title='境目は、どこか', chapter_title='境目は、どこか', scene=[
   dict(t='panel', box=TOP, text='今の境目：新潟県の糸魚川と、静岡県の富士川を結ぶ線（関西電力）', at=0, until=1, size=34, hi=True),
   dict(t='panel', box=TOP, text='この線の西側は60ヘルツ、東側は50ヘルツ', at=1, until=2, size=40, col='gold'),
   dict(t='panel', box=TOP, text='北海道電力NW：一般に、静岡県の富士川を境に、東日本50、西日本60', at=2, until=3, size=32),
   dict(t='panel', box=TOP, text='境目付近の、細かい地域の分かれ方は、この動画では未確認', at=3, size=38),
   dict(t='table', box=[60, 300, 1860, 560], cols=['境目（関西電力・北海道電力NW）', '周波数'], colw=[1100, 700], size=34, rows=[
     dict(at=0, cells=['新潟県の糸魚川と静岡県の富士川を結ぶ線', '境目'], col='gold'),
     dict(at=1, cells=['西側', '60ヘルツ']),
     dict(at=1, cells=['東側', '50ヘルツ'])])]),
 dict(key='kaden', title='家電は、どうなるのか', chapter_title='家電は、どうなるのか', scene=[
   dict(t='panel', box=TOP, text='周波数が違う地域に引っ越すと、電気製品はどうなる？', at=0, until=1, size=36),
   dict(t='panel', box=TOP, text='「50/60ヘルツ」の表示なら、どこでも使える（関西電力）', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='50または60だけの製品は、その地域でしか使えない。故障や火災のおそれ', at=2, until=3, size=34),
   dict(t='panel', box=TOP, text='今までどおり使える例：電気こたつ・電気ポット・トースター・テレビ・パソコン', at=3, until=4, size=32, col='gold'),
   dict(t='panel', box=TOP, text='性能が変わる：扇風機・ヘアドライヤー・掃除機。そのままでは使えない：洗濯機・電気時計・電子レンジ', at=4, until=5, size=28),
   dict(t='panel', box=TOP, text='2016年の資料の例。機種で異なる。今の製品は、本体の表示を確かめる', at=5, size=34, col='gold'),
   dict(t='table', box=[60, 300, 1860, 640], cols=['周波数が違う地域で（関西電力・2016年の例）', '例'], colw=[1000, 800], size=32, rows=[
     dict(at=3, cells=['今までどおり使える', 'こたつ・ポット・トースター・テレビ・パソコン'], col='gold'),
     dict(at=4, cells=['性能が変わる', '扇風機・ヘアドライヤー・掃除機']),
     dict(at=4, cells=['そのままでは使えない', '洗濯機・電気時計・電子レンジ'])])]),
 dict(key='fc', title='東と西を、つなぐ設備', chapter_title='東と西を、つなぐ設備', scene=[
   dict(t='panel', box=TOP, text='東と西の電気は、完全に分かれている？', at=0, until=1, size=40),
   dict(t='panel', box=TOP, text='周波数の違う電気をやり取りする設備：周波数変換設備（FC）', at=1, until=2, size=36, hi=True),
   dict(t='panel', box=TOP, text='東日本大震災で供給力が大幅に不足したことが、増強のきっかけ', at=2, until=3, size=34),
   dict(t='panel', box=TOP, text='2021年3月31日、飛騨信濃FCが運用開始。計画の確定から約8年', at=3, until=4, size=36),
   dict(t='panel', box=TOP, text='FCの合計容量：120万kW → 210万kW（キロワット＝一度に送れる電気の大きさ）', at=4, until=5, size=30, col='gold'),
   dict(t='panel', box=TOP, text='今後300万kWまで増強決定。2027年度の運用開始を目指す（2021年の発表）', at=5, until=6, size=30),
   dict(t='panel', box=TOP, text='その後、時期が変わる見通しも示されているようだ。最新は未確認', at=6, size=34),
   dict(t='table', box=[60, 300, 1860, 640], cols=['周波数変換設備の合計容量（送配電事業者9社の発表）', ''], colw=[1300, 500], size=32, rows=[
     dict(at=4, cells=['2021年3月31日より前', '120万kW']),
     dict(at=4, cells=['飛騨信濃FC運用開始後', '210万kW'], col='gold'),
     dict(at=5, cells=['今後の増強（2021年の発表では2027年度を目指す）', '300万kW'])])]),
 dict(key='know', title='わかることと、わからないこと', chapter_title='わかることと、わからないこと', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='わかること', title_at=0, items=[
      dict(at=0, text='明治に、東京はドイツ製の50Hz、大阪はアメリカ製の60Hzの発電機が輸入された'),
      dict(at=1, text='統一は何度も話し合われたが、うまくいかなかった。変換設備で東西をつないでいる')]),
     right=dict(title='わからないこと', title_at=2, items=[
      dict(at=2, text='導入した年・メーカーの確かな情報。統一が進まなかった詳しい理由'),
      dict(at=3, text='周波数変換設備の最新の増強状況')]))]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=0, items=[
      dict(at=1, text='明治に輸入した発電機が、東京（ドイツ製・50Hz）と大阪（アメリカ製・60Hz）で違った'),
      dict(at=2, text='統一はうまくいかず、今は周波数変換設備で東西をつないでいる')]),
     right=dict(title='言い方の注意', title_at=3, items=[
      dict(at=3, text='引っ越しのときは、電気製品の周波数の表示を確かめる')]))]),
 ],
 desc=dict(title_main='日本の電気はなぜ東と西で周波数が違うのか', title_no=1,
  titles=['日本の電気は、なぜ東と西で周波数が違う？ 電力会社の資料で確かめる', '東日本50ヘルツ・西日本60ヘルツの理由：明治のドイツ製とアメリカ製の発電機', '電気の周波数が東西で違うのはなぜ？ 統一できなかった理由と周波数変換設備'],
  intro='日本の電気には、50ヘルツと60ヘルツの2種類があります。なぜ東と西で違うのでしょうか。この動画では、関西電力・北海道電力ネットワーク・送配電事業者9社の資料で確かめます。',
  points=['東日本は50ヘルツ、西日本は60ヘルツです。境目は、新潟県の糸魚川と静岡県の富士川を結ぶ線とされます(関西電力・北海道電力ネットワーク)。', '明治時代に、東京にはドイツ製(50ヘルツ)、大阪にはアメリカ製(60ヘルツ)の発電機が輸入され、それぞれが全国に広がりました(関西電力)。', '約100年前から統一が何度も話し合われましたが、うまくいきませんでした(関西電力)。詳しい理由は確認できていません。', '周波数変換設備の合計容量は、2021年3月31日の飛騨信濃FCの運用開始で、120万kWから210万kWに拡大しました(送配電事業者9社の発表)。', '導入年やメーカー名は、解説記事の二次情報で、一次資料は確認できていません。'],
  refs=['関西電力「教えて！かんでん なぜちがう周波数ができてしまったの？」(2016年2月時点):https://www.kepco.co.jp/brand/for_kids/teach/2016_03/detail1.html', '北海道電力ネットワーク「日本の周波数」:https://www.hepco.co.jp/network/renewable_energy/efforts/problem/japan_hz.html', '送配電事業者9社・送配電網協議会「飛騨信濃周波数変換設備の運用開始について」(2021年4月1日):https://www.tepco.co.jp/pg/company/press-information/press/2021/1591426_8616.html', 'Benesse「なぜ電気の周波数は東日本50ヘルツで西日本60ヘルツなの？」(二次情報):https://benesse.jp/kyouiku/202103/20210326-2.html', 'Nichicon「日本の電気の不思議。なぜ、東西で周波数が違うのか」(二次情報):https://owners.nichicon.co.jp/column/2024_11'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['東京電灯・大阪電灯、ドイツ・アメリカのメーカー、導入年(1895・1896年など)は、解説記事による二次情報で、一次資料は確認できていません。', '家電の例は関西電力の2016年2月時点の資料の例で、機種によって異なります。今の製品は本体の表示を確認してください。', '300万kWへの増強と2027年度の運用開始は、2021年4月の発表の記述です。その後、時期が見直される見通しも示されているようですが、最新の状況は確認していません。'],
  tags='周波数, 50ヘルツ, 60ヘルツ, 東日本, 西日本, 電気, 発電機, 検証',
  checks=['電気事業連合会・資源エネルギー庁の資料で、導入年・メーカー名の一次情報を確認する', '電力広域的運営推進機関の最新資料で、周波数変換設備の増強状況(運用開始時期)を確認する', '統一が進まなかった詳しい理由(歴史資料)を確認する']),
 thumb=dict(bg='assets/frequency/thumb_art.png', lines=[['東日本50Hz', 95, 'white'], ['西日本60Hz', 95, 'white'], ['なぜ違う？', 115, 'gold']], sub='電力会社の資料で確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


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
    t = (R / 'docs' / 'themes' / '20270116_frequency' / '09_script_v2.md').read_text(encoding='utf8')
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
_ART = {'intro': 'intro', 'define': 'pylon', 'meiji': 'plant', 'nen': 'plant', 'tougou': 'plant', 'border': 'pylon', 'kaden': 'home', 'fc': 'sub', 'know': 'pylon', 'end': 'intro'}
if all((R / 'assets' / 'frequency' / f'art_{v}.png').exists() for v in set(_ART.values())):
    inject(spec, _ART)
(R / 'data' / 'frequency_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
