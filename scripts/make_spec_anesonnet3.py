"""Writes data/anesonnet3_spec.json（姉川の戦い 三部構成。モデル比較検証・Sonnet 5.5）。台本：docs/themes/20261104_anegawa3/09_script_v2.md（固定）"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]

ODA = (235, 90, 80); TOK = (70, 150, 255); ASAI = (90, 200, 120); ASAK = (190, 140, 255); RIV = (90, 160, 245)
BOX = [30, 100, 1230, 836]
RX0, RX1 = 1290, 1890   # 地図の右の列

# 地図（assets/anegawa/map_area.png）の正規化座標。地図は現代の地形で、位置は模式的（数百メートル〜数キロの目安）
KODANI = (0.41, 0.24); TORA = (0.33, 0.37); YOKO = (0.64, 0.76); RYU = (0.57, 0.69)
OOYORI = (0.60, 0.31); NOMURA = (0.57, 0.55); MITA = (0.41, 0.55); OTANI = (0.47, 0.37)
RIVER = [(0.78, 0.69), (0.68, 0.63), (0.60, 0.59), (0.52, 0.62), (0.44, 0.59), (0.35, 0.60), (0.27, 0.64), (0.20, 0.72)]


def bgi(img, alts):
    return dict(t='anim', name='pop_bgimg', img=img, at=0, dim=0.55, blur=4, alts=alts, seg=22)


def tel(text, at, until=None, x=960, y=330, size=100, plate=None, rot=-1.5, maxw=1560):
    d = dict(t='anim', name='pop_telop', text=text, x=x, y=y, size=size, at=at, plate=plate, rot=rot, maxw=maxw)
    if until is not None:
        d['until'] = until
    return d


def rows(items, y0=370, size=40, x0=RX0, x1=RX1, gap=14, ymax=None):
    d = dict(t='anim', name='pop_rows', items=items, x0=x0, x1=x1, y0=y0, size=size, gap=gap)
    if ymax is None and x0 == RX0 and y0 < 700:
        ymax = 755   # 右の列は、注記（y770）の手前で止める（文字は自動で縮む）
    if ymax:
        d['ymax'] = ymax
    return d


def rtel(text, at, until=None, plate='yellow', y=250, size=58):
    return tel(text, at, until, x=(RX0 + RX1) // 2, y=y, size=size, plate=plate, maxw=580)


def note():
    return rows([dict(at=0, text='現代の地形。位置は目安です', col='cyan')], y0=770, size=28, gap=0)


def place(xy, label, kind, col, side='r', at=0, lsize=34):
    return dict(xy=list(xy), label=label, kind=kind, col=list(col), side=side, at=at, lsize=lsize)


def river(at=0, lab=(0.72, 0.655)):
    return dict(pts=[list(p) for p in RIVER], label='姉川', col=list(RIV), at=at, lab=list(lab), lsize=34)


def unit(label, col, pts, at=0, legs=None, portrait=None, sub=None, until=None, dashed=False, head=34, lab_off=None, lsize=34, trail=True):
    u = dict(label=label, col=list(col), pts=[list(p) for p in pts], at=at, head=head, lsize=lsize, trail=trail)
    if legs:
        u['legs'] = legs
    if portrait:
        u['portrait'] = portrait
    if sub:
        u['sub'] = sub
    if until is not None:
        u['until'] = until
    if dashed:
        u['dashed'] = True
    if lab_off:
        u['lab_off'] = list(lab_off)
    return u


# 詳細な地図が、map_area（広域）のどの範囲にあたるか（左,上,右,下。画像の位置合わせで求めた）
EXT = dict(area=(0, 0, 1, 1), mid=(0.204, 0.127, 0.773, 0.863), core=(0.318, 0.318, 0.818, 0.909), main=(0.418, 0.318, 0.736, 0.791))


def conv(img, q):
    x0, y0, x1, y1 = EXT[img]
    return [round((q[0] - x0) / (x1 - x0), 4), round((q[1] - y0) / (y1 - y0), 4)]


def bmap(img='area', places=(), lines=(), units=(), marks=(), at=0, until=None):
    """座標は、すべて map_area の正規化座標で書く。img に合わせて自動で換算する。"""
    P = []
    for o in places:
        o = dict(o); o['xy'] = conv(img, o['xy']); P.append(o)
    L = []
    for o in lines:
        o = dict(o); o['pts'] = [conv(img, q) for q in o['pts']]
        if 'lab' in o:
            o['lab'] = conv(img, o['lab'])
        L.append(o)
    U = []
    for o in units:
        o = dict(o); o['pts'] = [conv(img, q) for q in o['pts']]; U.append(o)
    M = []
    for o in marks:
        o = dict(o); o['xy'] = conv(img, o['xy']); M.append(o)
    d = dict(t='anim', name='battle_map', img=img, box=BOX, at=at, places=P, lines=L, units=U, marks=M)
    if until is not None:
        d['until'] = until
    return d


OFF = (0.97, 0.97)   # 岐阜の方向（地図の外）
WH = (245, 243, 232)

spec = dict(slug='anesonnet3', theme_dir='20261104_anegawa3s', pack='cmp3_anesonnet3', header_sub='姉川の戦いを、地図と史料で確かめる', style='pop',
 images=dict(area=dict(file='assets/anegawa/map_area.png'), mid=dict(file='assets/anegawa/map_mid.png'), core=dict(file='assets/anegawa/map_core.png'), main=dict(file='assets/anegawa/map_main.png'), wide=dict(file='assets/anegawa/map_wide.png'),
             castle=dict(file='assets/anegawa/art_castle.png'), dawn=dict(file='assets/anegawa/art_dawn.png'),
             docs=dict(file='assets/anegawa/art_docs.png'), river=dict(file='assets/anegawa/art_river.png'),
             p_nobunaga=dict(file='assets/portraits/nobunaga.jpg', crop=[0.28, 0.12, 0.62, 0.40]),
             p_ieyasu=dict(file='assets/portraits/ieyasu.jpg', crop=[0.34, 0.36, 0.57, 0.545]),
             p_nagamasa=dict(file='assets/portraits/nagamasa.jpg', crop=[0.33, 0.445, 0.63, 0.545]),
             p_honda=dict(file='assets/portraits/honda_t.jpg', crop=[0.12, 0.25, 0.88, 0.85]),
             p_hideyoshi=dict(file='assets/portraits/hideyoshi.jpg', crop=[0.32, 0.36, 0.60, 0.46])),
 bgm=[['kanegasaki', 'cast', 'piano33'], ['terrain', 'dawn', 'ethnic26'], ['west', 'decide', 'orchestra24'], ['kubi', 'after', 'piano40']],
 chapters=[
 # ---------- 第1部：経緯 ----------
 dict(key='kanegasaki', title='金ヶ崎の退き口', chapter_title='第1部　金ヶ崎の退き口', scene=[
   bgi('castle', ['river', 'dawn']),
   tel('[[1570年]]　4月', 0, 1, y=300, size=120, plate='yellow'),
   tel('信長、[[朝倉]]を攻める', 0, 1, y=570, size=100, plate='red'),
   dict(t='anim', name='pop_card', inner='img', img='p_nobunaga', box=[110, 170, 560, 640], rot=-3, at=1, until=4, cap='織田信長'),
   dict(t='anim', name='pop_card', inner='img', img='p_nagamasa', box=[1360, 170, 1810, 640], rot=3, at=1, until=4, cap='浅井長政'),
   tel('妹の夫・[[浅井]]が、朝倉に味方', 1, 2, y=775, size=64, plate='green', maxw=1500),
   tel('前は[[朝倉]]、後ろは[[浅井]]', 2, 4, y=775, size=64, plate='purple', maxw=1500),
   tel('[[挟み撃ち]]！', 3, 4, y=450, size=130, plate='red'),
   tel('金ヶ崎の[[退き口]]', 4, 6, y=400, size=130, plate='orange'),
   rows([dict(at=6, tag='と伝わる', text='殿（しんがり）は木下藤吉郎らが務めた', col='orange', until=7)], y0=300, size=52, x0=110, x1=1810),
   rows([dict(at=7, tag='5月', text='千草越えで、岐阜へ戻る', col='orange')], y0=300, size=60, x0=110, x1=1810)]),
 dict(key='june', title='虎御前山と、竜ヶ鼻', chapter_title='第1部　虎御前山と、竜ヶ鼻', scene=[
   bgi('river', ['castle']),
   bmap(places=[place(KODANI, '小谷城', 'castle', ASAI, 'r', 0), place(TORA, '虎御前山', 'camp', ODA, 'l', 2), place(YOKO, '横山城', 'castle', ASAI, 'r', 4), place(RYU, '竜ヶ鼻', 'camp', ODA, 'l', 4)],
        lines=[river()],
        units=[unit('織田信長', ODA, [OFF, TORA, (0.50, 0.60), RYU], legs=[[0, 2], [3, 4], [4, 5]], portrait='p_nobunaga', head=38, lab_off=(-80, 40)),
               unit('徳川家康', TOK, [(0.62, 0.72)], at=5, portrait='p_ieyasu', head=36, lab_off=(70, 30))]),
   rtel('六月', 0, 2, 'yellow'),
   rows([dict(at=1, tag='6/19', text='岐阜を出た、といわれる', col='orange', until=2)], y0=360, size=40),
   rows([dict(at=2, tag='6/21', text='虎御前山に陣取り、小谷の城下に火（公記）', col='orange', until=3)], y0=360, size=40),
   rows([dict(at=3, tag='6/22', text='いったん兵を引く（公記）', col='orange', until=4)], y0=360, size=40),
   rows([dict(at=4, tag='6/24', text='横山城を囲み、竜ヶ鼻に陣取る（公記）', col='orange'), dict(at=5, tag='6/24', text='家康も出陣し、同じ竜ヶ鼻へ（公記）', col='cyan')], y0=360, size=38),
   note()]),
 dict(key='cast', title='両軍の顔ぶれと、数', chapter_title='第1部　両軍の顔ぶれと、数', scene=[
   bgi('docs', ['river']),
   bmap(places=[place(KODANI, '小谷城', 'castle', ASAI, 'r', 0), place(OOYORI, '大依山', 'spot', ASAK, 'r', 3), place(RYU, '竜ヶ鼻', 'camp', ODA, 'l', 0)],
        lines=[river()],
        units=[unit('朝倉景健', ASAK, [(0.93, 0.08), OOYORI], legs=[[0, 3]], head=30, lab_off=(60, -30)),
               unit('浅井長政', ASAI, [KODANI], at=4, portrait='p_nagamasa', head=34, lab_off=(-70, -30)),
               unit('織田信長', ODA, [(0.50, 0.77)], at=5, portrait='p_nobunaga', head=34, lab_off=(-80, 30)),
               unit('徳川家康', TOK, [(0.66, 0.66)], at=6, portrait='p_ieyasu', head=34, lab_off=(70, 30))]),
   rtel('両軍の数', 1, 3, 'yellow'),
   rows([dict(at=1, tag='公記', text='朝倉 八千ほど', col='purple', until=4), dict(at=1, tag='公記', text='浅井 五千ほど', col='green', until=4), dict(at=2, tag='合計', text='一万三千', col='orange', until=4)], y0=360, size=44),
   rows([dict(at=4, tag='浅井方', text='長政・磯野員昌・遠藤直経ほか', col='green', until=7), dict(at=5, tag='織田方', text='柴田勝家・木下秀吉・稲葉良通・氏家卜全・安藤守就ほか', col='orange', until=7),
         dict(at=6, tag='徳川方', text='酒井忠次・榊原康政・本多忠勝ほか', col='cyan', until=7)], y0=300, size=32),
   rows([dict(at=7, tag='注意', text='顔ぶれも数も、書物で違う。織田・徳川の数は公記に無い', col='red')], y0=360, size=38),
   note()]),
 # ---------- 第2部：開戦時の動き（地図） ----------
 dict(key='terrain', title='戦場の地形', chapter_title='第2部　戦場の地形', scene=[
   bgi('river', ['dawn']),
   bmap(places=[place(KODANI, '小谷城', 'castle', ASAI, 'r', 2), place(YOKO, '横山城', 'castle', ASAI, 'r', 5), place(RYU, '竜ヶ鼻', 'camp', ODA, 'l', 6), place(NOMURA, '野村', 'spot', WH, 'r', 7), place(MITA, '三田村', 'spot', WH, 'l', 7)],
        lines=[river(at=4)]),
   rtel('ここから[[地図]]', 0, 2, 'yellow'),
   rows([dict(at=1, tag='戦場', text='近江の北・姉川の周り', col='orange', until=2)], y0=360),
   rows([dict(at=2, tag='北', text='浅井の本拠・小谷城（山の上の城）', col='green', until=4)], y0=360),
   rows([dict(at=4, tag='姉川', text='小谷城の南を西へ流れ、琵琶湖へ', col='cyan'), dict(at=5, tag='南', text='浅井方の横山城', col='green'),
         dict(at=6, tag='陣', text='竜ヶ鼻に織田・徳川', col='orange'), dict(at=7, tag='北岸', text='野村の郷・三田村の郷', col='pink')], y0=360, size=34),
   note()]),
 dict(key='dawn', title='陣払い、そして、未明', chapter_title='第2部　陣払い、そして、未明', scene=[
   bgi('dawn', ['river']),
   bmap(img='mid', places=[place(KODANI, '小谷城', 'castle', ASAI, 'r', 0), place(OOYORI, '大依山', 'spot', ASAK, 'r', 0), place(RYU, '竜ヶ鼻', 'camp', ODA, 'l', 0), place(NOMURA, '野村', 'spot', WH, 'r', 3), place(MITA, '三田村', 'spot', WH, 'l', 3)],
        lines=[river()],
        units=[unit('浅井', ASAI, [(0.45, 0.30), NOMURA], legs=[[1, 3]], portrait='p_nagamasa', head=34, lab_off=(70, -10)),
               unit('朝倉', ASAK, [(0.58, 0.33), MITA], legs=[[1, 3]], head=30, lab_off=(-60, -34)),
               unit('織田・徳川', ODA, [RYU], at=0, head=28, lab_off=(60, 34))]),
   rtel('六月[[二十七日]]', 0, 1, 'yellow'),
   rows([dict(at=0, tag='6/27 暁', text='浅井・朝倉は陣払いして帰ったと思われた（公記）', col='orange', until=1)], y0=360),
   rows([dict(at=1, tag='6/28 未明', text='三十町（三キロ余り）をかかって来る（公記）', col='orange', until=3)], y0=360),
   rows([dict(at=3, tag='二手に備え', text='姉川を前に、野村・三田村へ移る（公記）', col='orange', until=4)], y0=360),
   rows([dict(at=4, tag='ある研究者', text='浅井・朝倉の奇襲だった、と見る', col='pink', until=5), dict(at=5, tag='ただし', text='公記は「奇襲」とは書いていない', col='cyan')], y0=360),
   note()]),
 dict(key='west', title='西の戦場：徳川と朝倉', chapter_title='第2部　西の戦場：徳川と朝倉', scene=[
   bgi('dawn', ['river', 'castle']),
   bmap(img='core', places=[place(RYU, '竜ヶ鼻', 'camp', ODA, 'l', 0), place(MITA, '三田村', 'spot', WH, 'l', 1), place(NOMURA, '野村', 'spot', WH, 'r', 0)],
        lines=[river(lab=(0.74, 0.665)), dict(pts=[list(RYU), [0.57, 0.50]], label='当初の予定？', col=list(TOK), at=3, dash=True, lab=[0.60, 0.56], lsize=28)],
        units=[unit('朝倉', ASAK, [(0.37, 0.43)], at=0, head=30, lab_off=(-70, -40)),
               unit('徳川家康', TOK, [RYU, (0.47, 0.62)], at=1, legs=[[1, 2]], portrait='p_ieyasu', head=36, lab_off=(-85, 45)),
               unit('本多忠勝（伝承）', TOK, [(0.47, 0.60), (0.41, 0.48)], at=6, legs=[[6, 7]], portrait='p_honda', head=30, dashed=True, lab_off=(-60, 50), lsize=28),
               unit('榊原康政（通説）', TOK, [(0.56, 0.62), (0.48, 0.49)], at=8, legs=[[8, 9]], head=26, dashed=True, lab_off=(60, -34), lsize=28)]),
   rtel('西：[[徳川]]vs[[朝倉]]', 0, 2, 'blue', size=52),
   rows([dict(at=1, tag='公記', text='西は三田村口。一番合戦に家康', col='orange', until=2)], y0=360, size=38),
   rows([dict(at=2, tag='実紀', text='もとは信長→朝倉、家康→浅井の予定', col='pink', until=4)], y0=360, size=38),
   rows([dict(at=4, tag='実紀', text='暁、朝倉の大軍を見て陣を替えたと書く', col='pink', until=6)], y0=360, size=38),
   rows([dict(at=6, tag='伝承', text='本多忠勝が敵の大軍へ突っ込んだ（相手は実紀＝浅井、三代記＝朝倉）', col='pink', until=8)], y0=360, size=36),
   rows([dict(at=8, tag='通説', text='榊原康政が敵の横を突いた', col='pink', until=9)], y0=360, size=38),
   rows([dict(at=9, tag='ただし', text='公記にも実紀の姉川の条にも見えない', col='cyan')], y0=360, size=38),
   note()]),
 dict(key='east', title='東の戦場：織田と浅井', chapter_title='第2部　東の戦場：織田と浅井', scene=[
   bgi('river', ['dawn', 'castle']),
   bmap(img='main', places=[place(NOMURA, '野村', 'spot', WH, 'r', 0), place(RYU, '竜ヶ鼻', 'camp', ODA, 'l', 0)],
        lines=[river(lab=(0.47, 0.66))],
        units=[unit('浅井', ASAI, [(0.57, 0.47)], at=2, portrait='p_nagamasa', head=36, lab_off=(-80, -20)),
               unit('織田馬廻', ODA, [RYU, (0.56, 0.62)], at=0, legs=[[0, 1]], portrait='p_nobunaga', head=36, lab_off=(-85, 55)),
               unit('美濃三人衆', ODA, [(0.69, 0.68)], at=1, head=28, lab_off=(-70, 45)),
               unit('磯野員昌（伝承）', ASAI, [(0.57, 0.47), (0.56, 0.63)], at=3, legs=[[3, 5]], head=26, dashed=True, lab_off=(60, -55), lsize=28),
               unit('美濃三人衆（通説）', ODA, [(0.69, 0.68), (0.64, 0.50)], at=6, legs=[[6, 7]], head=26, dashed=True, lab_off=(-60, -45), lsize=28)]),
   rtel('東：[[織田]]vs[[浅井]]', 0, 1, 'red', size=52),
   rows([dict(at=0, tag='公記', text='東は野村の郷。信長の馬廻', col='orange', until=3), dict(at=1, tag='公記', text='さらに東は美濃三人衆（稲葉・氏家・安藤）', col='orange', until=3)], y0=360, size=36),
   rows([dict(at=3, tag='伝承', text='磯野員昌が織田の先陣を突き崩す＝「十一段崩し」', col='pink', until=6), dict(at=5, tag='三代記', text='織田の旗本まで騒ぎに', col='pink', until=6)], y0=360, size=34),
   rows([dict(at=6, tag='通説', text='美濃三人衆が浅井の横から攻め、持ち直したともいわれる', col='pink', until=7)], y0=360, size=36),
   rows([dict(at=7, tag='ただし', text='十一段崩しは後世の創作という見方が強く、公記には無い', col='cyan')], y0=360, size=36),
   note()]),
 dict(key='decide', title='決着', chapter_title='第2部　決着', scene=[
   bgi('dawn', ['river']),
   bmap(img='mid', places=[place(KODANI, '小谷城', 'castle', ASAI, 'r', 0), place(OOYORI, '大依山', 'spot', ASAK, 'r', 0), place(NOMURA, '野村', 'spot', WH, 'r', 0), place(MITA, '三田村', 'spot', WH, 'l', 0)],
        lines=[river()],
        units=[unit('織田・徳川', ODA, [RYU], at=0, head=28, lab_off=(60, 34)),
               unit('浅井', ASAI, [NOMURA, (0.45, 0.30)], at=0, legs=[[5, 6]], portrait='p_nagamasa', head=34, lab_off=(70, -10)),
               unit('朝倉', ASAK, [MITA, (0.58, 0.33)], at=0, legs=[[5, 6]], head=30, lab_off=(-60, -34))],
        marks=[dict(xy=[0.50, 0.57], at=1, label='', col=[255, 90, 80])]),
   rtel('元亀元年[[六月二十八日]]', 0, 1, 'yellow', size=50),
   rows([dict(at=0, tag='暦', text='ユリウス暦で7/30、グレゴリオ暦では8/9', col='cyan', until=1)], y0=420, size=36),
   rows([dict(at=1, tag='午前6時ごろ', text='戦いが始まる（公記）', col='orange', until=3)], y0=420, size=36),
   rows([dict(at=3, tag='公記', text='「推しつ返しつ、散々に入り乱れ」', col='orange', until=4)], y0=420, size=36),
   rows([dict(at=4, tag='公記', text='「黒煙を立て…ついに追い崩した」', col='orange', until=5)], y0=420, size=36),
   rows([dict(at=5, tag='結果', text='浅井・朝倉は崩れ、退く', col='pink', until=6)], y0=420, size=36),
   rows([dict(at=6, tag='ただし', text='戦いの描写は、公記ではこの数行', col='cyan')], y0=420, size=36),
   note()]),
 # ---------- 第3部：戦後 ----------
 dict(key='kubi', title='首注文と、追い討ち', chapter_title='第3部　首注文と、追い討ち', scene=[
   bgi('docs', ['river', 'castle']),
   bmap(img='core', places=[place(YOKO, '横山城', 'castle', ASAI, 'r', 6), place(OTANI, '大谷', 'spot', ASAK, 'l', 5), place(NOMURA, '野村', 'spot', WH, 'r', 0)],
        lines=[river()],
        units=[unit('織田信長', ODA, [(0.56, 0.58), OTANI, (0.62, 0.74)], at=5, legs=[[5, 6], [6, 7]], portrait='p_nobunaga', head=36, lab_off=(70, 40))]),
   rtel('首注文', 0, 1, 'yellow'),
   rows([dict(at=0, tag='公記', text='討ち取った首の一覧（首注文）を載せる', col='orange', until=1)], y0=360, size=36),
   rows([dict(at=1, tag='朝倉方', text='真柄十郎左衛門 ←青木所左衛門', col='purple', until=3), dict(at=2, tag='浅井方', text='遠藤喜右衛門 ←竹中久作', col='green', until=3)], y0=360, size=36),
   rows([dict(at=3, tag='千百余', text='主だった者を討ち捕った（公記）', col='orange', until=5), dict(at=4, tag='注意', text='討った側の書き方。死者の総数ではない', col='cyan', until=5)], y0=360, size=36),
   rows([dict(at=5, tag='追い討ち', text='大谷まで五十町。麓に火を放つ', col='orange', until=6)], y0=360, size=36),
   rows([dict(at=6, tag='引き返す', text='大谷は高山。攻め上るのは難しいと見て横山へ', col='orange')], y0=360, size=36),
   note()]),
 dict(key='after', title='その後', chapter_title='第3部　その後', scene=[
   bgi('river', ['castle', 'dawn']),
   bmap(places=[place(YOKO, '横山城', 'castle', ODA, 'r', 0)], lines=[river()],
        units=[unit('木下藤吉郎', ODA, [(0.55, 0.80), YOKO], at=0, legs=[[0, 1]], portrait='p_hideyoshi', head=34, lab_off=(-80, 40)),
               unit('織田信長', ODA, [YOKO, (0.40, 0.99)], at=1, legs=[[1, 2]], portrait='p_nobunaga', head=36, lab_off=(70, 40))], until=2),
   rows([dict(at=0, tag='降参', text='横山城は降参。木下藤吉郎が、城を守る定番に入る（公記）', col='orange', until=1), dict(at=1, tag='7/1', text='信長は佐和山城へ（公記）', col='orange', until=2)], y0=360, size=40),
   tel('浅井・朝倉は、[[敗れた]]', 2, 3, y=300, size=100, plate='red'),
   tel('けれども、[[滅びては]]いない', 3, 4, y=300, size=100, plate='blue'),
   tel('秋、[[志賀の陣]]', 4, 5, y=300, size=120, plate='orange'),
   tel('倒れるのは[[三年後]]', 5, 6, y=300, size=110, plate='purple'),
   tel('姉川は、勝ちでも[[決着ではなかった]]', 6, y=520, size=86, plate='yellow')]),
 ],
 desc=dict(title_main='姉川の戦い', title_no=1, titles=['姉川の戦い 経緯・地図・戦後'], intro='姉川の戦いを、経緯、開戦時の動き（地図）、戦後の三部に分けて、史料に帰属して確かめます。',
  points=['『信長公記』が書くこと、後世の軍記が書くことを、分けて見ます。'], refs=['『信長公記』巻三「あね川合戦之事」（Wikisource）'], credit_lines=['・地図:国土地理院タイル（陰影起伏図・標準地図）を加工して作成。現代の地形で、位置は目安です'],
  notes=['美濃三人衆の側面攻撃などは、通説として語られる話で、一次資料は未確認です。'], tags='姉川の戦い, 織田信長, 徳川家康, 浅井長政, 戦国', checks=['通説・軍記の項目は、公開前に原文で確認する']),
 thumb=dict(bg='assets/anegawa/art_river.png', lines=[['姉川の戦い', 120, 'white']], sub='経緯・地図・戦後'))
(R / 'data' / 'anesonnet3_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8')
print('spec written')
