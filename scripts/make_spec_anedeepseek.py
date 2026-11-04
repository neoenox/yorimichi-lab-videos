"""Writes data/anedeepseek_spec.json（姉川の戦い。三部構成・第2部は地図で）。
台本：docs/themes/20261104_anegawa3/09_script_v2.md（固定・変更しない）。
画面は style='pop'。地図は assets/anegawa/ の5枚、背景は art_*.png、肖像は assets/portraits/。
at・until・legs は「章の中の文の番号（0始まり）」。番号は vp.py sents で確認済み。
地図の位置は、地形を見た概略の推定（画面に「※位置は概略の推定」と出す）。"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BLUE = (90, 150, 255)
GREEN = (110, 214, 140)
RED = (238, 96, 84)
PURPLE = (180, 140, 255)
GOLD = (239, 201, 118)
PINK = (255, 120, 170)

TAG = dict(公記='blue', 軍記='purple', 通説='orange', 説='green', 諸書='white')

MAPBOX = [40, 120, 1120, 790]

# 地図上の位置（正規化 0-1。地形を見た概略の推定）
KODANI = (0.405, 0.365)
TORAO = (0.515, 0.315)
OYORI = (0.625, 0.245)
ANEGAWA = (0.325, 0.555)
YOKOYAMA = (0.465, 0.665)
RYUGANA = (0.425, 0.575)
NOMURA = (0.625, 0.625)
MITAMURA = (0.300, 0.640)
OTANI = (0.800, 0.160)


def bg(name):
    return dict(t='anim', name='pop_bgimg', img=name, at=0, dim=.55, blur=4)


def tel(text, x, y, size, at, until=None, plate=None, rot=0.0):
    o = dict(t='anim', name='pop_telop', text=text, x=x, y=y, size=size, at=at)
    if until is not None:
        o['until'] = until
    if plate:
        o['plate'] = plate
    if rot:
        o['rot'] = rot
    return o


def R(text, tag, at, until=None):
    o = dict(at=at, text=text)
    if tag:
        o['tag'] = tag
        o['col'] = TAG[tag]
    if until is not None:
        o['until'] = until
    return o


def grp(items, y0=180, size=42, x0=1160, x1=1880, gap=14):
    return dict(t='anim', name='pop_rows', items=items, x0=x0, x1=x1, y0=y0, size=size, gap=gap)


def card(img, box, at, until=None, cap=None, rot=-1.2):
    o = dict(t='anim', name='pop_card', inner='img', img=img, box=box, at=at, rot=rot)
    if until is not None:
        o['until'] = until
    if cap:
        o['cap'] = cap
    return o


def PL(label, xy, kind, at, side='r', lsize=30, col=None):
    return dict(xy=list(xy), label=label, kind=kind, at=at, side=side, lsize=lsize,
                col=col or GOLD)


def U(label, sub, col, portrait, pts, at, legs=None, head=26, lsize=30, lab=(34, -6), until=None,
      dashed=False):
    o = dict(label=label, col=col, pts=[list(p) for p in pts], at=at, head=head, lsize=lsize,
             lab_off=lab)
    if sub:
        o['sub'] = sub
    if portrait:
        o['portrait'] = portrait
    if legs:
        o['legs'] = legs
    if until is not None:
        o['until'] = until
    if dashed:
        o['dashed'] = True
    return o


def MK(xy, at, label, col=PINK, lsize=26):
    return dict(xy=list(xy), at=at, label=label, col=col, lsize=lsize)


def bmap(places=None, units=None, marks=None, lines=None, img='area'):
    return dict(t='anim', name='battle_map', img=img, box=MAPBOX, at=0,
                places=places or [], units=units or [], marks=marks or [], lines=lines or [])


def note(at=0):
    return PL('※位置は概略の推定', (0.015, 0.05), 'spot', at, side='r', lsize=24, col=GOLD)


chapters = [
    # ================================================== 第1部（章1〜3）
    dict(key='kanegasaki', title='金ヶ崎の退き口', chapter_title='第1部：金ヶ崎の退き口', scene=[
        bg('docs'),
        tel('1570年 4月', 620, 230, 108, at=0, until=3, plate='yellow', rot=-1.5),
        card('p_nobunaga', [1290, 200, 1800, 660], 0, until=3, cap='織田信長'),
        grp([R('信長、越前の朝倉義景を攻める', '説', 1, 5),
             R('浅井長政が、朝倉方に付く', '説', 2, 5),
             R('前は朝倉、後ろは浅井', '説', 3, 5)], 380, size=46, x0=140, x1=1200),
        card('p_nagamasa', [1290, 200, 1800, 660], 3, until=5, cap='浅井長政'),
        tel('金ヶ崎の退き口', 620, 250, 86, at=5, until=9, plate='yellow'),
        grp([R('殿は木下藤吉郎らが務めた（通説）', '通説', 7, None),
             R('5月、千草越えで岐阜へ戻る', '説', 8, None)], 400, size=46, x0=140, x1=1200),
    ]),
    dict(key='june', title='虎御前山と、竜ヶ鼻', chapter_title='第1部：虎御前山と、竜ヶ鼻', scene=[
        bg('river'),
        bmap(places=[note(), PL('小谷城', KODANI, 'castle', 2, 'l'),
                     PL('虎御前山', TORAO, 'camp', 2, 'r'),
                     PL('横山城', YOKOYAMA, 'castle', 4, 'b'),
                     PL('竜ヶ鼻', RYUGANA, 'spot', 4, 'l'),
                     PL('姉川', ANEGAWA, 'spot', 4, 'b')],
             units=[U('織田信長', '虎御前山', BLUE, 'p_nobunaga', [TORAO], at=2, lab=(-40, -22)),
                    U('徳川家康', '竜ヶ鼻', GREEN, 'p_ieyasu', [RYUGANA], at=5, lab=(-40, 16))]),
        grp([R('6月、再び近江へ。19日に岐阜を出る', '説', 0, 2)], 180, size=42),
        grp([R('21日、虎御前山に陣取り、城下に放火', '公記', 2, 4)], 180, size=40),
        grp([R('24日、横山城を囲み、竜ヶ鼻に陣', '公記', 4, 5)], 180, size=40),
        grp([R('家康も、同じ竜ヶ鼻に陣取る', '公記', 5, None)], 180, size=40),
    ]),
    dict(key='cast', title='両軍の顔ぶれと、数', chapter_title='第1部：両軍の顔ぶれと、数', scene=[
        bg('castle'),
        card('p_nobunaga', [150, 150, 570, 500], 0, until=7, cap='織田信長'),
        card('p_ieyasu', [750, 150, 1170, 500], 0, until=7, cap='徳川家康'),
        card('p_nagamasa', [1350, 150, 1770, 500], 0, until=7, cap='浅井長政'),
        grp([R('朝倉景健が率いる援軍が来る', '諸書', 0, 4),
             R('朝倉8000・浅井5000＝1万3000', '公記', 1, 4)], 545, size=46, x0=150, x1=1780),
        grp([R('浅井方：長政・磯野員昌・遠藤直経', '諸書', 4, 7),
             R('織田方：柴田・秀吉・稲葉・氏家・安藤', '諸書', 5, 7),
             R('徳川方：酒井・榊原・本多', '諸書', 6, 7)], 555, size=46, x0=150, x1=1780),
        grp([R('顔ぶれも数も書物で違う。織田・徳川の数は公記になし', '公記', 7, None)], 555,
            size=42, x0=150, x1=1780),
    ]),
    # ================================================== 第2部（章4〜8）
    dict(key='terrain', title='戦場の地形', chapter_title='第2部：戦場の地形', scene=[
        bg('river'),
        bmap(places=[note(), PL('小谷城', KODANI, 'castle', 2, 'l'),
                     PL('姉川', ANEGAWA, 'spot', 4, 'b'),
                     PL('横山城', YOKOYAMA, 'castle', 5, 'b'),
                     PL('竜ヶ鼻', RYUGANA, 'spot', 6, 'l'),
                     PL('野村', NOMURA, 'spot', 7, 'r'),
                     PL('三田村', MITAMURA, 'spot', 7, 'l')]),
        grp([R('戦場は、近江の北、姉川の周り', None, 1, None),
             R('小谷城は、山の上に築かれた城', None, 2, None),
             R('姉川は、西へ流れ、琵琶湖へ', None, 4, None),
             R('横山城の近く、竜ヶ鼻に陣取る', '公記', 6, None),
             R('姉川の北に、野村と三田村', None, 7, None)], 180, size=38, gap=10),
    ]),
    dict(key='dawn', title='陣払い、そして、未明', chapter_title='第2部：陣払い、そして、未明', scene=[
        bg('dawn'),
        bmap(places=[note(), PL('小谷城', KODANI, 'castle', 0, 'l'),
                     PL('大依山', OYORI, 'spot', 0, 'r'),
                     PL('姉川', ANEGAWA, 'spot', 0, 'b'),
                     PL('野村', NOMURA, 'spot', 0, 'r'),
                     PL('三田村', MITAMURA, 'spot', 0, 'l')],
             units=[U('浅井軍', '小谷 → 野村', RED, 'p_nagamasa', [KODANI, NOMURA],
                      at=2, legs=[[2, 4]], lab=(30, 18)),
                    U('朝倉軍', '大依山 → 三田村', PURPLE, None, [OYORI, MITAMURA],
                      at=2, legs=[[2, 4]], head=30, lab=(-40, -16))]),
        grp([R('27日の暁、陣払いしたと思われた', '公記', 0, 2)], 180, size=40),
        grp([R('28日の未明、30町（3km余）をかけて来る', '公記', 2, 5),
             R('野村と三田村へ移り、二手に備える', '公記', 4, 5)], 180, size=38),
        grp([R('奇襲だった、と見る研究者がいる', '説', 5, 6)], 180, size=40),
        grp([R('ただし公記は「奇襲」と書かない', '公記', 6, None)], 180, size=40),
    ]),
    dict(key='west', title='西の戦場：徳川と朝倉', chapter_title='第2部：西の戦場', scene=[
        bg('castle'),
        bmap(img='core', places=[note(), PL('三田村', (0.130, 0.650), 'spot', 0, 'l'),
                                 PL('姉川', (0.440, 0.550), 'spot', 0, 'b'),
                                 PL('拡大図', (0.970, 0.050), 'spot', 0, 'l', 24)],
             units=[U('徳川家康', '三田村口', GREEN, 'p_ieyasu', [(0.190, 0.700)], at=0,
                      head=24, lab=(-40, 16)),
                    U('朝倉軍', '8000', PURPLE, None, [(0.260, 0.620)], at=0, head=30,
                      lab=(26, -22))],
             marks=[MK((0.100, 0.600), 7, None)]),
        tel('駒の大きさ＝兵数の目安', 1520, 140, 28, at=0),
        grp([R('西は三田村口。一番合戦は家康', '公記', 1, 3)], 180, size=40),
        grp([R('実紀：信長は朝倉、家康は浅井の予定', '軍記', 4, 7),
             R('暁に陣を替え、家康が朝倉へ', '軍記', 5, 7)], 180, size=38),
        grp([R('忠勝の突入。相手は浅井（実紀）、朝倉（三代記）', '軍記', 7, 10),
             R('榊原の側面攻撃（通説）', '通説', 9, 10)], 180, size=36),
        grp([R('公記にも、実紀の姉川の条にも、見えない', '公記', 10, None)], 180, size=38),
    ]),
    dict(key='east', title='東の戦場：織田と浅井', chapter_title='第2部：東の戦場', scene=[
        bg('river'),
        bmap(img='core', places=[note(), PL('野村', (0.630, 0.640), 'spot', 0, 'b'),
                                 PL('姉川', (0.440, 0.550), 'spot', 0, 'b'),
                                 PL('拡大図', (0.970, 0.050), 'spot', 0, 'l', 24)],
             units=[U('織田馬廻', '信長', BLUE, 'p_nobunaga', [(0.585, 0.665)], at=0,
                      head=24, lab=(30, -24)),
                    U('美濃三人衆', '稲葉・氏家・安藤', BLUE, None, [(0.700, 0.700)], at=2,
                      head=24, lab=(-30, 26)),
                    U('浅井軍', '5000', RED, 'p_nagamasa', [(0.480, 0.600)], at=4,
                      head=26, lab=(-46, -20))],
             marks=[MK((0.530, 0.620), 5, None, PINK)]),
        grp([R('東は野村。信長の馬廻が向かう', '公記', 0, 5),
             R('さらに東、美濃三人衆', '公記', 2, 5),
             R('相手は、浅井の軍と語られる', '通説', 4, 5)], 180, size=38),
        grp([R('磯野員昌が先陣を次々に崩す＝十一段崩し', '軍記', 5, 9),
             R('織田の旗本まで騒ぎに（三代記）', '軍記', 7, 9),
             R('美濃三人衆が横から攻め、持ち直した（通説）', '通説', 8, 9)], 180, size=34),
        grp([R('十一段崩しは後世の創作という見方。公記になし', '説', 9, None)], 180, size=36),
    ]),
    dict(key='decide', title='決着', chapter_title='第2部：決着', scene=[
        bg('dawn'),
        bmap(img='core', places=[note(), PL('姉川', (0.440, 0.550), 'spot', 0, 'b'),
                                 PL('拡大図', (0.970, 0.050), 'spot', 0, 'l', 24)],
             units=[U('織田', '馬廻', BLUE, 'p_nobunaga', [(0.585, 0.665)], at=0, head=24,
                      lab=(30, -20)),
                    U('徳川', '三田村口', GREEN, 'p_ieyasu', [(0.190, 0.700)], at=0, head=24,
                      lab=(-40, 16)),
                    U('浅井', '長政', RED, 'p_nagamasa', [(0.480, 0.600)], at=0, head=26,
                      until=6, lab=(-44, -20)),
                    U('朝倉', '景健', PURPLE, None, [(0.260, 0.620)], at=0, head=30,
                      until=6, lab=(-30, 16)),
                    U('浅井・崩れ', '退却', RED, None,
                      [(0.480, 0.600), (0.400, 0.420)], at=6, head=13, legs=[[6, 7]],
                      dashed=True, lab=(16, 14), lsize=24),
                    U('朝倉・崩れ', '退却', PURPLE, None,
                      [(0.260, 0.620), (0.360, 0.340)], at=6, head=13, legs=[[6, 7]],
                      dashed=True, lab=(16, -14), lsize=24)]),
        grp([R('ユリウス暦7月30日／グレゴリオ暦8月9日', '公記', 1, 3),
             R('卯の刻（午前6時ごろ）に開戦', '公記', 2, 3)], 180, size=38),
        grp([R('「推しつ返しつ、散々に、入り乱れ」', '公記', 4, 6),
             R('「黒煙を立て…ついに、追い崩した」', '公記', 5, 6)], 180, size=36),
        grp([R('浅井・朝倉は崩れ、退いた（兵数は不明）', '公記', 6, 7)], 180, size=38),
        grp([R('公記の戦闘描写は、この数行', '公記', 7, None)], 180, size=40),
    ]),
    # ================================================== 第3部（章9〜10）
    dict(key='kubi', title='首注文と、追い討ち', chapter_title='第3部：首注文と、追い討ち', scene=[
        bg('docs'),
        bmap(places=[note(), PL('横山城', YOKOYAMA, 'castle', 0, 'b'),
                     PL('大谷', OTANI, 'spot', 5, 'r')],
             units=[U('織田信長', None, BLUE, 'p_nobunaga',
                      [YOKOYAMA, OTANI, YOKOYAMA], at=0, legs=[[5, 6], [6, 7]], lab=(-40, -20))]),
        grp([R('首注文', '公記', 0, 1)], 180, size=48),
        grp([R('真柄十郎左衛門は、青木所左衛門が討つ', '公記', 1, 3),
             R('遠藤喜右衛門は、竹中久作が討つ', '公記', 2, 3)], 180, size=38),
        grp([R('主だった者、1100余（討った側の数）', '公記', 3, 5)], 180, size=38),
        grp([R('大谷まで50町、追い討ちして放火', '公記', 5, 7),
             R('大谷は高山。横山へ戻る', '公記', 6, 7)], 180, size=36),
    ]),
    dict(key='after', title='その後', chapter_title='第3部：その後', scene=[
        bg('castle'),
        grp([R('横山城が降参。木下藤吉郎が定番に', '公記', 0, 3),
             R('7月1日、信長は佐和山城へ', '公記', 2, 3)], 250, size=48, x0=180, x1=1740),
        grp([R('浅井・朝倉は敗れたが、滅びてはいない', '説', 3, 6),
             R('秋には、志賀の陣が始まる', '説', 5, 6)], 250, size=46, x0=180, x1=1740),
        tel('勝ち。だが、決着ではない', 960, 300, 96, at=6, until=8, plate='yellow', rot=-1.5),
        grp([R('倒れるのは天正元年。3年後', '説', 6, 8)], 520, size=44, x0=180, x1=1740),
        grp([R('姉川は織田・徳川の勝ち。決着ではなかった', '説', 8, None)], 520,
            size=44, x0=180, x1=1740),
    ]),
]

images = dict(
    area=dict(file='assets/anegawa/map_area.png'),
    core=dict(file='assets/anegawa/map_core.png'),
    castle=dict(file='assets/anegawa/art_castle.png'),
    dawn=dict(file='assets/anegawa/art_dawn.png'),
    docs=dict(file='assets/anegawa/art_docs.png'),
    river=dict(file='assets/anegawa/art_river.png'),
    p_nobunaga=dict(file='assets/portraits/nobunaga.jpg'),
    p_nagamasa=dict(file='assets/portraits/nagamasa.jpg', crop=[0.20, 0.36, 0.80, 0.60]),
    p_ieyasu=dict(file='assets/portraits/ieyasu.jpg'),
)


def _counts():
    t = (ROOT / 'docs' / 'themes' / '20261104_anegawa3' / '09_script_v2.md').read_text(encoding='utf8')
    out = []
    for c in re.split(r'\n## ', t)[1:]:
        if not re.match(r'章(\d+)　', c.split('\n')[0]):
            continue
        n = 0
        for l in c.split('\n'):
            if re.match(r'^\d+\. ', l):
                body = re.sub(r'〔[^〕]*〕', '', re.sub(r'^\d+\. ', '', l)).strip()
                n += len([x for x in body.split('。') if x.strip()])
        out.append(n)
    return out


def _check(o, n, where):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('at', 'until', 'title_at') and isinstance(v, int):
                assert -1 < v <= n, (where, k, v, n)
            elif k == 'legs':
                for a, b in v:
                    assert -1 < a <= n and -1 < b <= n, (where, k, v, n)
            else:
                _check(v, n, where)
    elif isinstance(o, list):
        for v in o:
            _check(v, n, where)


_N = _counts()
assert len(_N) == len(chapters), (len(_N), len(chapters))
for _ch, _n in zip(chapters, _N):
    _check(_ch['scene'], _n, _ch['key'])

spec = dict(
    slug='anedeepseek', theme_dir='20261104_anegawa3', pack='cmp3_anedeepseek',
    header_sub='姉川の戦いを、経緯・地図・戦後に分けて追う',
    style='pop',
    images=images,
    bgm=[['kanegasaki', 'cast', 'piano36'], ['terrain', 'dawn', 'ethnic30'],
         ['west', 'decide', 'orchestra22'], ['kubi', 'after', 'piano38']],
    chapters=chapters,
    desc=dict(
        title_main='姉川の戦い：金ヶ崎の退き口から、地図で追う開戦と戦後',
        title_no=1,
        titles=['姉川の戦いを地図で解説 金ヶ崎の退き口から開戦・戦後まで',
                '姉川の戦い 浅井・朝倉はなぜ退いた？ 地図と『信長公記』で追う',
                '姉川の戦い 三部構成で通す 経緯・開戦時の動き・戦後'],
        intro='元亀元年（1570年）、近江の姉川で、織田・徳川の軍と、浅井・朝倉の軍がぶつかりました。この動画は三部構成です。第1部では、金ヶ崎の退き口から、虎御前山・竜ヶ鼻の陣取り、両軍の顔ぶれと数までを追います。第2部では、開戦時の各軍の動きを、地図の上で確かめます。第3部では、首注文と追い討ち、そして戦いの後をまとめます。『信長公記』に書かれていることと、後世の軍記・通説・研究者の説を、画面のタグで分けています。',
        points=[
            '金ヶ崎の退き口：元亀元年4月、信長は越前の朝倉義景を攻め、浅井長政の離反で挟み撃ちの危険に陥り、退きました。殿は木下藤吉郎らが務めたと伝わります（通説）。',
            '陣取り：6月21日、信長は虎御前山に陣取り城下に放火。24日、横山城を囲み、竜ヶ鼻に陣取りました。家康も同じ竜ヶ鼻に陣取りました（『信長公記』）。',
            '数：『信長公記』は朝倉8000ほど、浅井5000ほど、合わせて1万3000とします。織田・徳川の数は公記に書かれていません。顔ぶれも書物で違います。',
            '開戦：6月28日未明、浅井・朝倉は30町（3km余）をかけて来て、姉川を前に野村・三田村へ移り、二手に備えました。奇襲だったと見る研究者がいますが、公記は「奇襲」と書いていません（説）。',
            '西の戦場：公記は西は三田村口、一番合戦に家康とします。本多忠勝の突入と榊原康政の側面攻撃は軍記・通説で、公記にも実紀の姉川の条にも見えません。',
            '東の戦場：公記は東は野村に信長の馬廻、さらに東に美濃三人衆とします。磯野員昌の「十一段崩し」は軍記の話で、後世の創作という見方も強いものです。',
            '決着：卯の刻（午前6時ごろ）に始まり、公記は「推しつ返しつ、散々に、入り乱れ」「ついに追い崩した」と、数行で書きます。',
            '戦後：首注文、大谷までの追い討ち、横山城の降参と木下藤吉郎の定番、7月1日の佐和山行き。浅井・朝倉は敗れましたが滅びず、倒れるのは天正元年（3年後）です。',
        ],
        refs=[
            '太田牛一『信長公記』巻三「あね川合戦之事」（Wikisource の翻刻で確認）:https://ja.wikisource.org/wiki/信長公記/我自刊我書',
            '『東照宮御実紀』巻二（Wikisource の翻刻で確認）:https://ja.wikisource.org/wiki/東照宮御実紀/卷二',
            '『浅井三代記』第十五（Wikisource の翻刻で確認）:https://ja.wikisource.org/wiki/浅井三代記',
            '日本語版Wikipedia「姉川の戦い」（二次資料。研究者名は出さない）',
            '国立天文台 暦計算室（ユリウス暦・グレゴリオ暦の換算）',
        ],
        credit_lines=[
            '・地図：国土地理院タイル（陰影起伏図・標準地図）を加工して作成。現代の地形で、当時の川筋・道ではありません。城・郷・陣の位置は、地形を見た概略の推定です。',
            '・肖像：織田信長・徳川家康・浅井長政・本多忠勝。Wikimedia Commons で公開されているパブリックドメインの画像です（後世の肖像画・想像図を含みます）。',
            '・イラスト：ChatGPT(OpenAI)による生成イラスト（イメージです。実際の場面の再現ではありません）',
        ],
        notes=[
            '画面のタグは出典の区別です。公記＝『信長公記』（同時代に近い記録）、軍記＝後世の軍記・編纂物（『東照宮御実紀』『浅井三代記』）、通説＝広く語られる話、説＝研究者の説・二次資料、諸書＝諸本。',
            '地図は、経緯と戦場の広い範囲を「広域図」、戦いの場面（西・東・決着）を「拡大図」で示しています。',
            '駒の大きさは兵数の目安です。朝倉8000・浅井5000は『信長公記』の陣立てで、大きさでおおよそを示しています。織田・徳川の数は公記にないため、小さめの一定にしています。崩れた後は、残兵を小さな駒と破線の退却線で示しています。',
            '地図上の軍勢の位置・経路は、地形と軍記の描写をもとにした概略の推定で、実際の経路・時刻ではありません。',
            '本多忠勝の突入先（実紀は浅井、『浅井三代記』は朝倉）と、榊原康政の側面攻撃、磯野員昌の十一段崩しは、出典によって食い違うため、動きではなく印で示しています。',
            '織田・徳川の兵数、浅井・朝倉の将の配置の細部、合戦の正確な場所は、この動画の資料だけでは決められません。',
        ],
        tags='姉川の戦い, 浅井長政, 織田信長, 徳川家康, 朝倉義景, 金ヶ崎の退き口, 信長公記, 戦国時代, 戦況解説, 地図',
        checks=[
            '『信長公記』巻三の原文（Wikisource の翻刻）を、公開前にもう一度確認する。',
            '『東照宮御実紀』『浅井三代記』の該当箇所を、公開前にもう一度確認する。',
            '地図の位置（小谷城・横山城・竜ヶ鼻・野村・三田村・大依山・大谷）を、国土地理院の住所検索と案内で再確認する。',
            'ユリウス暦・グレゴリオ暦の換算を、国立天文台の計算で再確認する。',
        ],
    ),
)

(ROOT / 'data' / 'anedeepseek_spec.json').write_text(
    json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8')
print('spec written; sentences per chapter', _N)

