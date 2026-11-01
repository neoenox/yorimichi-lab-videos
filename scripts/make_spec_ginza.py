"""Writes data/ginza_spec.json（銀座は、昔は海に突き出た砂州だった？）。台本：docs/themes/20271101_ginza/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。
素材は scripts/make_ginza_assets.py で作る（国土地理院のタイル。加工して作成）。
見せ場：江戸前島（約4m）と、両側の埋め立て地（約3m）の段差。
fillmap は標高だけを土台に、砂州・西の入り江・東の海・4本の堀を手で描いた模式図。位置と形は模式化してある。
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize

R = Path(__file__).resolve().parents[1]
PLAYLIST_LOWLAND = 'PLV4MJdcpAGpM'   # 再生リスト「東京の低地」（日比谷・渋谷・銀座）
IMG = ('aerial_1936', 'aerial_1961', 'aerial_now', 'relief', 'relief_plain',
       'fillmap_0', 'fillmap_1', 'fillmap_2', 'fillmap_3')
IMAGES = {n: dict(file=f'assets/ginza/{n}.png') for n in IMG}
CAP_RELIEF = '色別標高図（国土地理院の5mメッシュ標高から作成）'
CAP_1936 = '国土地理院 空中写真（1936〜42年頃）'


# --- ポップスタイルの部品（vp_anim_pop）。at/until は章内の行番号
def pop(name, **kw):
    return dict(t='anim', name=name, **kw)


def tel(text, x, y, size, **kw):
    return dict(t='anim', name='pop_telop', text=text, x=x, y=y, size=size, **kw)


def rows(items, **kw):
    kw.setdefault('x0', 100)
    kw.setdefault('x1', 1820)
    kw.setdefault('y0', 180)
    kw.setdefault('size', 38)
    kw.setdefault('gap', 18)
    return dict(t='anim', name='pop_rows', items=items, **kw)


def card(box, **kw):
    kw.setdefault('at', 0)
    kw.setdefault('rot', -2)
    return dict(t='anim', name='pop_card', inner='img', box=box, **kw)


spec = dict(
    slug='ginza', theme_dir='20271101_ginza', pack='80_ginza',
    header_sub='江戸前島・銀座の埋立てで、地形の成り立ちを確かめる',
    images=IMAGES,
    bgm=[['intro', 'maejima', 'piano36'], ['maejima', 'end', 'piano12'], ['end', 'end', 'piano40']],
    style='pop',
    chapters=[
        {'key': 'intro', 'title': '銀座は、昔は海に突き出た砂州だった？',
         'chapter_title': '導入：銀座は昔は海に突き出た砂州だった？',
         'opener': '銀座は、昔は海に突き出た砂州だった？', 'opener_until': 1,
         'scene': [pop('pop_bgimg', img='aerial_1936', at=0, dim=.5, blur=3),
                   tel('銀座は、昔は\n[[海に突き出た砂州]]だった？', 960, 450, 130, at=0, until=2, rot=-3),
                   tel('正確には、[[砂が積もってできた半島]]の先端ちかく', 960, 700, 92, at=1, until=3, plate='green', rot=1.5),
                   tel('半島の西は入り江、東は海', 960, 470, 76, at=2, until=4, plate='yellow', rot=-1.5),
                   tel('両側が埋め立てられて、今の銀座になった', 960, 660, 78, at=3, until=4, plate='blue', rot=1),
                   tel('順を追って、地形の成り立ちを確かめる', 960, 560, 96, at=4, plate='pink', rot=-2)]},
        {'key': 'maejima', 'title': '江戸前島', 'chapter_title': '江戸前島：砂がつくった半島',
         'scene': [pop('pop_bgimg', img='relief_plain', at=0, dim=.65, blur=12),
                   card([60, 150, 960, 840], at=0, rot=-2, img='relief', cap=CAP_RELIEF),
                   rows([dict(at=0, tag='半島', text='東京湾の奥に、南へ突き出した半島があった', col='orange'),
                         dict(at=1, tag='名前', text='江戸前島とよばれる', col='blue'),
                         dict(at=2, tag='でき方', text='隅田川が運んだ砂が積もってできた、砂州の半島', col='green'),
                         dict(at=3, tag='はさみ', text='西が日比谷入江、東は海。細い土地に町ができた', col='purple'),
                         dict(at=4, tag='通り', text='真ん中の線が、今の中央通りにあたる', col='pink'),
                         dict(at=5, tag='町', text='日本橋・京橋・銀座の町は、この半島の上に広がった', col='red')],
                        x0=1000, x1=1860, y0=165, size=32, gap=10),
                   tel('「島」ではなく、\n[[砂州]]の半島', 1430, 730, 54, at=2, until=5, plate='yellow', rot=2)]},
        {'key': 'west', 'title': '西を埋める', 'chapter_title': '西を埋める：1603年〜',
         'scene': [pop('pop_bgimg', img='aerial_1961', at=0, dim=.6, blur=7),
                   pop('pop_fill', base='fillmap_0', at=0, box=[60, 150, 960, 840], rot=-2,
                       cap='砂州と両側の海・堀の模式図（位置・形は模式化）',
                       steps=[dict(img='fillmap_1', at=0)]),
                   rows([dict(at=0, tag='日比谷入江', text='半島の西側は、入り江だった', col='orange'),
                         dict(at=1, tag='1603年', text='江戸開府、天下普請で埋め立てが始まった', col='blue'),
                         dict(at=2, tag='1612年', text='駿府の銀座が移り、地名のもとになった', col='green'),
                         dict(at=3, tag='台地', text='入り江が埋まると、日本橋台地と呼ばれる微高地になった', col='purple'),
                         dict(at=4, tag='通り', text='中央通りは尾根筋に通された。水はけのためとされる', col='pink')],
                        x0=1000, x1=1860, y0=180, size=36, gap=16),
                   tel('西側が、陸になった', 1430, 780, 46, at=5, plate='yellow', rot=-1)]},
        {'key': 'east', 'title': '東を埋める', 'chapter_title': '東を埋める：1657年〜',
         'scene': [pop('pop_bgimg', img='aerial_now', at=0, dim=.55, blur=6),
                   pop('pop_fill', base='fillmap_0', at=0, box=[60, 150, 960, 840], rot=-2,
                       cap='砂州と両側の海・堀の模式図（位置・形は模式化）',
                       steps=[dict(img='fillmap_2', at=0)]),
                   rows([dict(at=0, tag='東側', text='東側は、まだ海だった', col='orange'),
                         dict(at=1, tag='1657年', text='明暦の大火で江戸の大半が焼けた', col='blue'),
                         dict(at=2, tag='西本願寺', text='焼けた寺の代わりに、佃島の住人が海を埋めて築地を造成', col='green'),
                         dict(at=3, tag='築地', text='「築地」は、もともと埋め立て地という意味', col='purple'),
                         dict(at=4, tag='銀座', text='銀座の東も、しだいに陸になっていった', col='red')],
                        y0=180, size=38, gap=18),
                   tel('東側も、陸になった', 1430, 780, 46, at=5, plate='yellow', rot=-1)]},
        {'key': 'moat', 'title': '島になり、また陸になる', 'chapter_title': '島になり、また陸になる',
         'scene': [pop('pop_bgimg', img='aerial_now', at=0, dim=.5, blur=8),
                   pop('pop_fill', base='fillmap_0', at=0, box=[60, 150, 960, 840], rot=-2,
                       cap='砂州と両側の海・堀の模式図（位置・形は模式化）',
                       steps=[dict(img='fillmap_3', at=0)]),
                   rows([dict(at=0, tag='島', text='東西南北を4本の堀に囲まれ、銀座は島になった', col='orange'),
                         dict(at=1, tag='1949年', text='三十間堀川の埋め立てが始まった', col='blue'),
                         dict(at=2, tag='外堀ほか', text='外堀・汐留川・京橋川も埋め立てられた', col='green'),
                         dict(at=3, tag='1964年', text='東京高速道路が完成。掘割は道路に変わった', col='purple')],
                        y0=180, size=40, gap=18),
                   tel('こうして、[[地続きの街]]に', 1430, 780, 46, at=4, plate='yellow', rot=-1)]},
        {'key': 'end', 'title': '名残りとまとめ', 'chapter_title': '名残りとまとめ',
         'scene': [pop('pop_bgimg', img='relief_plain', at=0, dim=.5, blur=8),
                   tel('まとめ！', 960, 400, 150, at=0, until=1, rot=-3),
                   rows([dict(at=0, tag='分かった', text='銀座は、海ではなく砂州の半島の先端ちかくだった', col='green'),
                         dict(at=1, tag='分かった', text='西（1603年〜）→東（1657年〜）→堀（1949年〜』で別々に埋め立てられた', col='green'),
                         dict(at=2, tag='高さ', text='標高を測ると、銀座はまわりの埋め立て地より少し高い', col='orange'),
                         dict(at=3, tag='柳', text='1874年に植えた木が根腐れし、柳に替えられたとされる', col='red'),
                         dict(at=4, tag='通り', text='中央通りの向きは、京橋・日本橋と少し違う。地形に沿ったためとされる', col='purple')],
                        y0=180, size=40, gap=18),
                   tel('次に銀座を歩くとき、\n[[砂州の先端]]を思い出してみて', 960, 740, 52, at=5, plate='yellow', rot=-1)]},
    ],
    desc={
        'title_main': '銀座は、昔は海に突き出た砂州だった？',
        'title_no': 1,
        'titles': ['銀座は、昔は海に突き出た砂州だった？ 江戸前島と埋め立ての歴史',
                   '江戸前島とは？ 銀座と築地の地形を地図と標高で確かめる',
                   '三十間堀川・外堀の埋め立てから辿る銀座の歴史'],
        'intro': '銀座には海の名残が残っています。実は海ではなく、江戸前島という砂州の半島の先端ちかくでした。'
                 '半島の西は日比谷入江、東は海で、それぞれ別の理由で埋め立てられ、今の街になりました。'
                 '順を追って、地図・標高・空中写真で確かめます。'
                 '\n\n■ シリーズ「東京の低地」\n'
                 '昔は水だった土地を、地図・標高・空中写真で確かめます。\n'
                 '再生リスト:https://www.youtube.com/playlist?list=' + PLAYLIST_LOWLAND,
        'points': ['江戸前島は、隅田川が運んだ砂が積もってできた砂州の半島です。'
                   '中央通り付近を尾根筋とし、汐留付近を先端としていました。'
                   '日本橋・京橋・銀座の町は、この半島の上に広がっていきました。',
                   '半島の西側は日比谷入江という入り江でした。1603年の江戸開府後、天下普請で埋め立てが始まり、'
                   '1612年に駿府の銀座が移って地名の由来になりました。埋め立て地は日本橋台地と呼ばれます。',
                   '東側は1657年の明暦の大火をきっかけに、西本願寺の代替地として佃島の住人が造成しました。そこが「築地（埋立地の意）」です。',
                   '銀座は東を三十間堀川、西を外堀、南を汐留川、北を京橋川に囲まれた島になりました。'
                   '1949年に三十間堀川の埋め立てが始まり、1964年に東京高速道路が完成するまで、堀は順に道路へ変わりました。',
                   '国土地理院の標高データでは、銀座四丁目が約4.1m、京橋が約4.0m、築地本願寺が約3.4m、汐留が約3.3mで、'
                   '日比谷入江側の埋め立て地（約3m）よりわずかに高く、砂州の微高地であることが分かります。',
                   '1874年に植えた桜・松・楓が根腐れし、湿地に強い柳に植え替えられたエピソードは、埋立地の性質を物語ります。',
                   '中央通りの軸線は、京橋・日本橋・神田の軸線と方向が異なります。地形の尾根筋に沿って通したためとされます。'],
        'refs': ['Wikipedia「銀座」:https://ja.wikipedia.org/wiki/銀座',
                 'Wikipedia「築地」:https://ja.wikipedia.org/wiki/築地',
                 'Wikipedia「江戸前島」:https://ja.wikipedia.org/wiki/江戸前島',
                 '国土地理院 地理院タイル一覧:https://maps.gsi.go.jp/development/ichiran.html',
                 '国土地理院コンテンツ利用規約:https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html'],
        'credit_lines': [
            '・空中写真:国土地理院撮影の空中写真(1936〜42年頃、1961〜69年頃)と全国最新写真を、地理院タイルから加工して作成',
            '・色別標高図:国土地理院の標高タイル(5mメッシュ)から作成',
            '・模式図:国土地理院の標高タイルを土台に、砂州・日比谷入江・江戸湾・4本の堀・埋め立ての範囲を描き足して作成(位置と形は模式化)',
            '・場面のイラスト:ChatGPT・Codex(OpenAI)による生成イラスト(イメージです。実際の場面・人物・資料の再現ではありません)',
        ],
        'notes': ['「海」ではなく「砂州の半島」。表現には注意する。',
                  '埋め立ては「西（日比谷入江）→東（築地）→堀」の3段階で、別々の理由・時期に進んだ。1つの事業として語らない。',
                  '「島」は比喩ではなく、4本の堀に囲まれた事実。行政的な島ではない。',
                  '築地の造成は「銀座のため」ではなく、西本願寺の代替地として造成された。',
                  '中央通りの向きが京橋・日本橋と違うのは、砂州の尾根筋に沿ったため。現地で確認できる。',
                  '標高は国土地理院の5mメッシュ標高から、地点の周り9×9画素の平均を取った概算です。',
                  '柳の根腐れの原因は「埋立地の水分」とされるが、確定した説ではない。',
                  '1262年の「前嶋村」、中央通り＝尾根筋、楓川・三十間堀川の掘削は、二次資料（Wikipedia等）のみで確認したため「〜とされる」「との説」と弱めています。',
                  '三井住友トラスト不動産「このまちアーカイブス」は 2026-11-01 時点で HTTP 503 で再取得できず、日比谷回の参照情報から補っています。'],
        'tags': '銀座, 江戸前島, 江戸, 埋め立て, 日比谷入江, 築地, 明暦の大火, 地形, 検証',
        'checks': ['中央区「銀座・銀座西地区 町名の由来」で1612年の記述を直接確認',
                   '築地の造成（1657年・佃島の住人）を中央区の資料で確認',
                   '標高の値を国土地理院の標高確認ページで1点照合',
                   '模式図の範囲（砂州の幅・堀の位置）を古地図または治水地形分類図と見比べて調整'],
    },
    thumb=dict(bg='assets/ginza/relief_plain.png',
               lines=[['銀座は', 76, 'white'], ['砂州の先端？', 130, 'gold']],
               sub='地図と標高で、確かめる', shade_col=[8, 20, 36], accent=[255, 178, 72],
               bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=640, sub_size=42,
               shade_x=700, shade_w=520))

finalize(spec, {})