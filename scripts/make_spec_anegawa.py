"""Writes data/anegawa_spec.json（姉川の戦い。戦況解説シリーズ7本目）。台本：docs/themes/20261205_anegawa/09_script_v2.md
文の番号（at・legs）は章内の0始まりの『行の番号』で書き、下で文の番号に直す。地図の座標は anegawa_maps.norm()。
位置は、国土地理院住所検索（野村町・三田町・大依町・虎御前山・堀部町）とWikipedia座標（小谷城・横山城・佐和山城）、案内をもとにした概略の推定（竜ヶ鼻など。画面に『推定』と明記）。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import anegawa_maps as MM
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]
BOX = [60, 250, 1860, 850]
BLUE = (90, 150, 255); RED = (238, 96, 84); GRN = (110, 214, 140); GOLD = (239, 201, 118); WATER = (130, 195, 255)
NC = json.loads((R / 'data' / 'nagashino_crops.json').read_text(encoding='utf8'))
SC = json.loads((R / 'data' / 'sekigahara_crops.json').read_text(encoding='utf8'))


def A(lon, lat): return list(MM.norm(lon, lat, 'area'))
def C(lon, lat): return list(MM.norm(lon, lat, 'core'))
def W(lon, lat): return list(MM.norm(lon, lat, 'wide'))
def D(lon, lat): return list(MM.norm(lon, lat, 'mid'))
def N(lon, lat): return list(MM.norm(lon, lat, 'main'))


ODANI = (136.277, 35.459); YOKOYAMA = (136.325, 35.394); TORA = (136.263, 35.445); OYORI = (136.311, 35.435)
NOMURA = (136.323, 35.419); MITA = (136.313, 35.420); GIFU = (136.7606, 35.4232); KANAGASAKI = (136.0775, 35.6757); SAWAYAMA = (136.2689, 35.2795)
# 以下は、案内をもとにした概略の推定位置（正確な地点ではない）
RYUGA = (136.318, 35.402)       # 竜ヶ鼻（推定）
_CORE_PX = [(0, 265), (60, 275), (120, 297), (190, 290), (260, 300), (330, 305), (400, 290), (470, 270), (520, 285), (555, 320), (590, 372), (650, 395), (720, 405), (790, 420), (828, 428)]
_AREA_PX_W = [(125, 490), (165, 445), (215, 400), (240, 375), (285, 355), (350, 358)]
ANE_PTS = [(136.19 + x / 978 * 0.22, 35.48 - y / 600 * 0.11) for x, y in _AREA_PX_W] + [(136.26 + x / 828 * 0.11, 35.445 - y / 600 * 0.065) for x, y in _CORE_PX[1:]]



def pn(text, at, until=None, size=40, hi=True, col=None):
    """旧パネルの代わり：右側の白いカード（ポップ）。"""
    it = dict(at=at, text=text, col='orange')
    if until is not None: it['until'] = until
    return dict(t='anim', name='pop_rows', items=[it], x0=1010, x1=1880, y0=170, size=44, gap=0)


def tel(text, x, y, size, **kw): return dict(t='anim', name='pop_telop', text=text, x=x, y=y, size=size, **kw)
def rows(items, **kw): return dict(t='anim', name='pop_rows', items=items, **kw)
def bgimg(img, **kw): return dict(t='anim', name='pop_bgimg', img=img, **kw)


def unit(**k): return k
def NOTE_POS(at=0, txt='※位置は概略の推定'): return dict(xy=[0.02, 0.04], label='※推定', kind='spot', at=at, side='r', col=GOLD, lsize=28, _note=True)


MAPBOX = [30, 120, 1000, 880]


def _big(k):
    for pl in k.get('places', []):
        if not pl.get('_note'): pl['lsize'] = int(pl.get('lsize', 24) * 1.5)
        pl.pop('_note', None)
    for u in k.get('units', []):
        u['lsize'] = int(u.get('lsize', 26) * 1.5); u['head'] = int(u.get('head', 26) * 1.3)
        if 'lab_off' in u: u['lab_off'] = (int(u['lab_off'][0] * 1.6), int(u['lab_off'][1] * 1.6))
    for ln in k.get('lines', []): ln['lsize'] = int(ln.get('lsize', 26) * 1.5)
    for mk in k.get('marks', []): mk['lsize'] = int(mk.get('lsize', 24) * 1.5)


def amap(img='area', **k):
    _big(k)
    return dict(t='anim', name='battle_map', img=img, box=MAPBOX, at=0, **k)


NOTE_IMG = 'イメージ（生成画像）。実際の場面の再現ではありません'
NOTE_GUNKI = '※軍記による描写。実際の経路・順序は確定しない'
EST = '※位置・経路は概略の推定'
def _clip(pts):
    """0〜1の枠で折れ線を切る（枠の外の点は、交点に置き換える）。"""
    out = []
    def inside(p): return 0 <= p[0] <= 1 and 0 <= p[1] <= 1
    def cross(p, q):
        t0, t1 = 0.0, 1.0
        dx, dy = q[0] - p[0], q[1] - p[1]
        for pp, qq in ((-dx, p[0]), (dx, 1 - p[0]), (-dy, p[1]), (dy, 1 - p[1])):
            if pp == 0:
                if qq < 0: return None
            else:
                r = qq / pp
                if pp < 0: t0 = max(t0, r)
                else: t1 = min(t1, r)
        if t0 > t1: return None
        return [p[0] + t0 * dx, p[1] + t0 * dy], [p[0] + t1 * dx, p[1] + t1 * dy]
    for p, q in zip(pts, pts[1:]):
        c = cross(p, q)
        if c is None: continue
        if not out or out[-1] != c[0]: out.append(c[0])
        out.append(c[1])
    return out
def RIVER(f, at=0, lab=(0.04, 0.38)):
    pts = _clip([f(*p) for p in ANE_PTS])
    return dict(pts=pts, label='姉川（現代の川筋の概略）', at=at, col=WATER, dash=False, lab=list(lab))

_MAPCH = {'terrain', 'next', 'dawn', 'after', 'battle', 'gunki', 'lines', 'road'}
_MAPCH_ORDER = ['intro', 'road', 'forces', 'terrain', 'dawn', 'lines', 'battle', 'gunki', 'after', 'next', 'source', 'summary']
DROP = {}

chapters = [
 dict(key='intro', title='姉川の戦い', chapter_title='導入：姉川の戦い', scene=[
   bgimg('river', at=0, dim=.5, blur=4),
   tel('姉川の戦い\n有名な話は\n[[記録にある]]？', 960, 470, 120, at=0, until=1, rot=-3),
   tel('[[康政の側面攻撃]]・[[十一段崩し]]\n『信長公記』には[[書かれていない]]', 960, 470, 88, at=1, until=2, plate='red', rot=-2),
   tel('元亀元年6/28（1570年）\n織田・徳川 対 浅井・朝倉', 960, 470, 96, at=2, until=3, plate='blue', rot=2),
   tel('通説：織田・徳川の勝ち', 960, 470, 120, at=3, until=4, plate='yellow', rot=-1.5),
   tel('地図で追って、確かめる！', 960, 470, 120, at=4, plate='pink', rot=2)]),
 dict(key='road', title='金ヶ崎から、虎御前山へ', chapter_title='金ヶ崎から、虎御前山へ', scene=[
   pn('元亀元年4月　信長が越前の朝倉を攻める。浅井長政が朝倉に味方（説）', 0, 1, 40),
   pn('挟み撃ちを避けて、信長は退く＝金ヶ崎の退き口（説）', 1, 2, 38),
   pn('6/21　信長は虎御前山に陣取り、小谷の城下を放火（『信長公記』）', 2, 3, 34, col='gold'),
   pn('6/24　横山城を囲み、信長は竜ヶ鼻に陣取る。家康も同じ竜ヶ鼻へ（『信長公記』）', 3, None, 34, col='gold'),
   amap('mid', places=[NOTE_POS(0, EST),
                dict(xy=D(*ODANI), label='小谷城', kind='castle', at=0, side='r', col=RED, lsize=24),
                dict(xy=D(*TORA), label='虎御前山', kind='spot', at=2, side='l', col=BLUE, lsize=22),
                dict(xy=D(*YOKOYAMA), label='横山城', kind='castle', at=3, side='r', col=RED, lsize=22),
                dict(xy=D(*RYUGA), label='竜ヶ鼻（推定）', kind='spot', at=3, side='l', col=BLUE, lsize=22)], lines=[RIVER(D, 0)],
        units=[unit(label='織田信長', sub='岐阜方面から', col=BLUE, portrait='p_nobunaga', pts=[D(136.352, 35.425), D(*TORA), D(*RYUGA)], legs=[[2, 3], [3, 4]], at=2, head=26, lab_off=(-36, 10), lsize=22, dashed=True),
               unit(label='徳川家康', col=BLUE, portrait='p_ieyasu', pts=[D(RYUGA[0] + 0.006, RYUGA[1] + 0.004)], at=3, head=24, lab_off=(36, 20), lsize=20)])]),
 dict(key='forces', title='両軍の顔ぶれと、数', chapter_title='両軍の顔ぶれと、数', scene=[
   bgimg('docs', at=0, dim=.55, blur=6),
   rows([dict(at=0, tag='浅井・朝倉', text='浅井長政・磯野員昌・遠藤直経ほか。朝倉は景健が大将', col='red', until=2),
         dict(at=1, tag='織田・徳川', text='信長・柴田勝家・木下秀吉・美濃三人衆／家康・酒井・榊原・本多ほか', col='blue', until=2)], x0=110, x1=1810, y0=250, size=52, gap=40),
   tel('顔ぶれは、書物で[[違う]]', 960, 470, 120, at=2, until=3, plate='yellow', rot=-1.5),
   rows([dict(at=3, tag='『信長公記』', text='朝倉8千ほど＋浅井5千ほど＝1万3千', col='green', until=6),
         dict(at=4, tag='『東照宮御実紀』', text='朝倉1万5千余／浅井8千余（軍記）', col='orange', until=6),
         dict(at=5, tag='不明', text='織田・徳川の数は書かれていない。実際の数は分からない', col='red')], x0=110, x1=1810, y0=250, size=52, gap=40)]),
 dict(key='terrain', title='地形と、城', chapter_title='地形と、城', scene=[
   pn('小谷城（山城）の南を、姉川が西へ流れ、琵琶湖へ向かう', 0, 1, 40),
   pn('姉川の南に、横山城（浅井方）。近くの竜ヶ鼻に、織田・徳川が陣取る（『信長公記』）', 1, 2, 34, col='gold'),
   pn('朝倉の軍は、小谷の東の大依山に陣取った（『信長公記』）', 2, 3, 36, col='gold'),
   pn('姉川の北に、野村の郷と、三田村の郷', 3, None, 40),
   amap('mid', places=[NOTE_POS(0, '※現代の地形。城・陣の位置は概略の推定'),
                dict(xy=D(*ODANI), label='小谷城', kind='castle', at=0, side='r', col=RED, lsize=26),
                dict(xy=D(*YOKOYAMA), label='横山城', kind='castle', at=1, side='r', col=RED, lsize=24),
                dict(xy=D(*RYUGA), label='竜ヶ鼻（推定）', kind='spot', at=1, side='l', col=BLUE, lsize=22),
                dict(xy=D(*OYORI), label='大依山（推定）', kind='spot', at=2, side='r', col=RED, lsize=22),
                dict(xy=D(NOMURA[0] + 0.004, NOMURA[1] + 0.002), label='野村', kind='spot', at=3, side='r', col=GOLD, lsize=22),
                dict(xy=D(MITA[0] - 0.004, MITA[1] + 0.002), label='三田村', kind='spot', at=3, side='l', col=GOLD, lsize=22)],
        lines=[RIVER(D, 0)])]),
 dict(key='dawn', title='陣払い、そして、未明', chapter_title='陣払い、そして、未明', scene=[
   pn('『信長公記』：6/27の暁、浅井・朝倉は陣払いして、帰ったと思われた', 0, 1, 36, col='gold'),
   pn('ところが、6/28の未明、30町（3キロ余り）ほど、かかって来た', 1, 2, 38, col='gold'),
   pn('姉川を前にして、野村の郷と三田村の郷へ移り、二手に備えた', 2, 3, 38, col='gold'),
   pn('この文などから、浅井・朝倉の奇襲だった、とみる研究者も（説）', 3, 4, 36),
   pn('ただし、公記は「奇襲」とは書いていない。読み方の問題', 4, None, 38, col='gold'),
   amap('mid', places=[NOTE_POS(0, EST),
                dict(xy=D(*OYORI), label='大依山（推定）', kind='spot', at=0, side='r', col=RED, lsize=22),
                dict(xy=D(NOMURA[0] + 0.004, NOMURA[1] + 0.002), label='野村', kind='spot', at=2, side='r', col=GOLD, lsize=22),
                dict(xy=D(MITA[0] - 0.004, MITA[1] + 0.002), label='三田村', kind='spot', at=2, side='l', col=GOLD, lsize=22),
                dict(xy=D(*RYUGA), label='竜ヶ鼻（推定）', kind='spot', at=0, side='l', col=BLUE, lsize=22)], lines=[RIVER(D, 2)],
        units=[unit(label='朝倉軍', sub='大依山から', col=RED, pts=[D(OYORI[0] + 0.004, OYORI[1] + 0.004), D(MITA[0] - 0.002, MITA[1] + 0.003)], legs=[[1, 3]], at=0, head=24, lab_off=(-36, -20), lsize=20, dashed=True),
               unit(label='浅井軍', sub='小谷方面から', col=RED, portrait='p_nagamasa', pts=[D(OYORI[0] + 0.012, OYORI[1] + 0.012), D(NOMURA[0] + 0.004, NOMURA[1] + 0.003)], legs=[[1, 3]], at=0, head=24, lab_off=(36, -20), lsize=20, dashed=True)])]),
 dict(key='lines', title='布陣', chapter_title='布陣', scene=[
   pn('『信長公記』の布陣：西は三田村口。一番合戦に、家康が向かった', 0, 1, 36, col='gold'),
   pn('東は野村の郷に、信長の馬廻。さらに東は美濃三人衆。両軍全体の配置は書かれていない', 1, 2, 34, col='gold'),
   pn('『東照宮御実紀』は違う話：信長は朝倉に、家康は浅井に向かう予定だった（軍記）', 2, 3, 34),
   pn('暁に、信長は朝倉の大軍を見て、陣を替えた（軍記）', 3, None, 38),
   amap('main', places=[NOTE_POS(0, EST),
                        dict(xy=N(MITA[0] - 0.004, MITA[1] + 0.002), label='三田村口', kind='spot', at=0, side='l', col=GOLD, lsize=22),
                        dict(xy=N(NOMURA[0] + 0.004, NOMURA[1] + 0.002), label='野村の郷', kind='spot', at=1, side='r', col=GOLD, lsize=22),
                        dict(xy=N(*RYUGA), label='竜ヶ鼻（推定）', kind='spot', at=0, side='l', col=BLUE, lsize=20)], lines=[RIVER(N, 0)],
        units=[unit(label='徳川家康', sub='三田村口へ', col=BLUE, portrait='p_ieyasu', pts=[N(RYUGA[0] - 0.01, RYUGA[1] - 0.001), N(MITA[0], MITA[1] - 0.012)], legs=[[0, 1]], at=0, head=24, lab_off=(-36, 10), lsize=20, dashed=True),
               unit(label='信長の馬廻', sub='野村の郷へ', col=BLUE, portrait='p_nobunaga', pts=[N(RYUGA[0] + 0.004, RYUGA[1] + 0.001), N(NOMURA[0] - 0.002, NOMURA[1] - 0.012)], legs=[[1, 2]], at=1, head=24, lab_off=(36, 10), lsize=20, dashed=True),
               unit(label='美濃三人衆', sub='さらに東へ', col=BLUE, pts=[N(RYUGA[0] + 0.02, RYUGA[1] + 0.002), N(NOMURA[0] + 0.014, NOMURA[1] - 0.012)], legs=[[1, 2]], at=1, head=20, lab_off=(36, 10), lsize=18, dashed=True),
               unit(label='朝倉軍', col=RED, pts=[N(MITA[0] - 0.003, MITA[1] + 0.004)], at=0, head=22, lab_off=(-36, -20), lsize=20),
               unit(label='浅井軍', col=RED, portrait='p_nagamasa', pts=[N(NOMURA[0] + 0.003, NOMURA[1] + 0.005)], at=1, head=22, lab_off=(36, -20), lsize=20)])]),
 dict(key='battle', title='姉川　戦闘', chapter_title='姉川　戦闘', scene=[
   pn('6/28　卯の刻（午前6時ごろ）', 0, 1, 42),
   pn('『信長公記』：敵も姉川へかかり合い、推しつ返しつ、散々に入り乱れ', 1, 2, 34, col='gold'),
   pn('黒煙を立て、しのぎを削り、鍔を割り、ついに追い崩した（『信長公記』）', 2, 3, 34, col='gold'),
   pn('戦いの描写は、公記では、この数行だけ', 3, 4, 38),
   pn('有名な、榊原康政の側面攻撃（通説）', 4, 5, 40, col='gold'),
   pn('公記にも、『東照宮御実紀』の姉川の条にも、見えない', 5, None, 38, col='gold'),
   amap('main', places=[NOTE_POS(0, '※位置は概略の推定。軍記による描写')], lines=[RIVER(N, 0)],
        units=[unit(label='徳川勢', col=BLUE, portrait='p_ieyasu', pts=[N(MITA[0], MITA[1] - 0.012), N(MITA[0] - 0.002, MITA[1] + 0.002)], legs=[[1, 3]], at=0, head=24, lab_off=(-36, 10), lsize=20, dashed=True),
               unit(label='織田勢', col=BLUE, portrait='p_nobunaga', pts=[N(NOMURA[0] - 0.002, NOMURA[1] - 0.012), N(NOMURA[0], NOMURA[1] + 0.001)], legs=[[1, 3]], at=0, head=24, lab_off=(36, 10), lsize=20, dashed=True),
               unit(label='朝倉軍', col=RED, pts=[N(MITA[0] - 0.003, MITA[1] + 0.004), N(MITA[0] - 0.012, MITA[1] + 0.02)], legs=[[2, 3]], at=1, head=22, lab_off=(-36, -20), lsize=20),
               unit(label='浅井軍', col=RED, portrait='p_nagamasa', pts=[N(NOMURA[0] + 0.003, NOMURA[1] + 0.005), N(NOMURA[0] + 0.008, NOMURA[1] + 0.02)], legs=[[2, 3]], at=1, head=22, lab_off=(36, -20), lsize=20)])]),
 dict(key='gunki', title='「十一段崩し」と、家康の働き', chapter_title='「十一段崩し」と、家康の働き', scene=[
   pn('『東照宮御実紀』：浅井方の磯野員昌が、織田の先陣を、十一段まで切り崩した（軍記）', 0, 1, 34),
   pn('家康は、織田の旗色が乱れるのを見て、旗本の備えを崩してかかれと命じた（軍記）', 1, 2, 32),
   pn('本多忠勝らが浅井の大軍へ突入。浅井勢は横を討たれて、小谷城へ逃げ入った（軍記）', 2, 3, 32),
   pn('『浅井三代記』にも、十一段崩しの話。17世紀後半の書物で、同時代の記録では確かめられない', 3, 4, 32, col='gold'),
   pn('『信長公記』には、十一段崩しも、書かれていない', 4, 5, 38, col='gold'),
   pn('実紀は、徳川の功を、大きく書く本。割り引いて読む', 5, None, 38),
   amap('main', places=[NOTE_POS(0, '※位置は概略の推定。軍記による描写'), dict(xy=N(*RYUGA), label='織田の本陣（竜ヶ鼻・推定）', kind='spot', at=0, side='l', col=BLUE, lsize=20)], lines=[RIVER(N, 0)],
        units=[unit(label='磯野員昌', sub='十一段崩し（軍記）', col=RED, pts=[N(NOMURA[0], NOMURA[1] - 0.004), N(RYUGA[0] + 0.004, RYUGA[1] + 0.006)], legs=[[0, 1]], at=0, head=22, lab_off=(36, -20), lsize=20, dashed=True),
               unit(label='本多忠勝ら', sub='突入（軍記）', col=BLUE, portrait='p_honda', pts=[N(MITA[0] - 0.002, MITA[1] - 0.012), N(NOMURA[0] - 0.01, NOMURA[1] - 0.003)], legs=[[1, 3]], at=1, head=22, lab_off=(-36, 10), lsize=20, dashed=True)])]),
 dict(key='after', title='討ち取りと、その後', chapter_title='討ち取りと、その後', scene=[
   pn('『信長公記』の「首の注文」＝討ち取った首の一覧。前波新八・弓削六郎左衛門ら', 0, 1, 34, col='gold'),
   pn('朝倉方の真柄十郎左衛門は青木所左衛門が、浅井方の遠藤喜右衛門は竹中久作が討った', 1, 2, 32),
   pn('このほか、主だった者、千百余を討ち捕った（『信長公記』）', 2, 3, 36, col='gold'),
   pn('討ち取った側の書き方。両軍の死者の総数ではない', 3, 4, 38),
   pn('信長は、小谷（大谷）まで50町を追い討ちし、麓を放火', 4, 5, 38),
   pn('大谷は高山で、攻め上るのは難しいと考え、横山へ戻った', 5, 6, 36),
   pn('横山城は降参。木下藤吉郎が定番として入る（『信長公記』）', 6, 7, 36, col='gold'),
   pn('7/1　佐和山城を囲む　7/6　上洛し将軍に報告　7/8　岐阜へ戻る', 7, None, 36),
   amap('wide', places=[NOTE_POS(0, EST), dict(xy=W(*ODANI), label='小谷城（大谷）', kind='castle', at=4, side='l', col=RED, lsize=22),
                dict(xy=W(*YOKOYAMA), label='横山城', kind='castle', at=5, side='r', col=BLUE, lsize=22),
                dict(xy=W(*SAWAYAMA), label='佐和山城', kind='castle', at=6, side='r', col=RED, lsize=22),
                dict(xy=W(*GIFU), label='岐阜', kind='castle', at=7, side='l', col=BLUE, lsize=22)],
        units=[unit(label='織田・徳川軍', sub='追い討ち→横山城', col=BLUE, portrait='p_nobunaga', pts=[W(NOMURA[0], NOMURA[1]), W(ODANI[0] + 0.01, ODANI[1] - 0.012), W(*YOKOYAMA), W(*SAWAYAMA), W(*GIFU)], legs=[[4, 5], [5, 6], [6, 7], [7, 8]], at=4, head=24, lab_off=(-36, 10), lsize=20, dashed=True),
               unit(label='木下藤吉郎', sub='横山城の定番', col=BLUE, portrait='p_hideyoshi', pts=[W(YOKOYAMA[0] - 0.02, YOKOYAMA[1] + 0.02)], at=6, head=20, lab_off=(-36, 20), lsize=20)])]),
 dict(key='next', title='その後', chapter_title='その後', scene=[
   pn('浅井・朝倉は、この戦いに敗れた。しかし、滅びてはいない（説）', 0, 1, 36),
   pn('秋に、志賀の陣が始まる。森可成や織田信治が討死（説）', 1, 2, 38),
   pn('浅井・朝倉が倒れるのは、天正元年。3年後。姉川の勝ちは、決定的ではなかった（説）', 2, None, 34, col='gold'),
   amap('wide', places=[NOTE_POS(0, '※位置は概略'), dict(xy=W(*ODANI), label='小谷城', kind='castle', at=0, side='l', col=RED, lsize=24),
                        dict(xy=W(*SAWAYAMA), label='佐和山城', kind='castle', at=2, side='r', col=RED, lsize=24), dict(xy=W(*YOKOYAMA), label='横山城', kind='castle', at=0, side='r', col=BLUE, lsize=22)])]),
 dict(key='source', title='呼び名と、資料', chapter_title='呼び名と、資料', scene=[
   bgimg('docs', at=0, dim=.55, blur=6),
   tel('「姉川の戦い」は\n[[徳川方]]の呼び方（説）', 960, 400, 110, at=0, until=1, rot=-2),
   tel('織田・浅井＝野村合戦／朝倉＝三田村合戦（説）', 960, 700, 52, at=0, until=1, plate='yellow', rot=1),
   rows([dict(at=1, tag='『信長公記』', text='同時代に近い、織田の側の記録。家康の働きを詳しく書くのは目的ではない', col='blue', until=3),
         dict(at=2, tag='『東照宮御実紀』', text='江戸幕府が、徳川家の事績をまとめた記録', col='orange', until=3)], x0=110, x1=1810, y0=250, size=54, gap=40),
   tel('どちらも[[視点]]がある。\n分けて見るのが、確かめる第一歩', 960, 470, 100, at=3, plate='yellow', rot=-1.5)]),
 dict(key='summary', title='分かること、決められないこと', chapter_title='分かること、決められないこと', scene=[
   bgimg('castle', at=0, dim=.55, blur=6),
   rows([dict(at=0, tag='分かる', text='1570年6/28、姉川で、織田・徳川が浅井・朝倉に勝った。公記は千百余を討ち捕ったと書く', col='green'),
         dict(at=1, tag='不明', text='両軍の、実際の兵力', col='red'),
         dict(at=1, tag='不明', text='浅井・朝倉の、奇襲だったのか', col='red'),
         dict(at=2, tag='不明', text='康政の側面攻撃・十一段崩しは、実際にあったのか', col='red'),
         dict(at=2, tag='不明', text='主戦場の、正確な場所', col='red')], x0=110, x1=1810, y0=170, size=50, gap=26),
   tel('通説・軍記・同時代の記録。\n分けて見ると、[[見え方が変わる]]', 960, 850, 56, at=3, plate='yellow', rot=-1.2)]),
]

images = dict(
    mid=dict(file='assets/anegawa/map_mid.png'), main=dict(file='assets/anegawa/map_main.png'),
    area=dict(file='assets/anegawa/map_area.png'), core=dict(file='assets/anegawa/map_core.png'), wide=dict(file='assets/anegawa/map_wide.png'),
    p_nobunaga=dict(file='assets/portraits/nobunaga.jpg', crop=NC['nobunaga']), p_ieyasu=dict(file='assets/portraits/ieyasu.jpg', crop=SC['ieyasu']),
    p_nagamasa=dict(file='assets/portraits/nagamasa.jpg', crop=[0.36, 0.425, 0.64, 0.545]), p_honda=dict(file='assets/portraits/honda_t.jpg', crop=[0.18, 0.34, 0.62, 0.72]),
    p_hideyoshi=dict(file='assets/portraits/hideyoshi.jpg', crop=[0.28, 0.385, 0.54, 0.525]),
    river=dict(file='assets/anegawa/art_river.png'), docs=dict(file='assets/anegawa/art_docs.png'),
    dawn=dict(file='assets/anegawa/art_dawn.png'), castle=dict(file='assets/anegawa/art_castle.png'))


def _line_to_sentence_starts():
    import re
    t = (R / 'docs' / 'themes' / '20261205_anegawa' / '09_script_v2.md').read_text(encoding='utf8')
    out = []
    for c in re.split(r'\n## ', t)[1:]:
        if not re.match(r'章(\d+)　', c.split('\n')[0]): continue
        starts, n = [], 0
        for l in c.split('\n'):
            if re.match(r'^\d+\. ', l):
                body = re.sub(r'〔[^〕]*〕', '', re.sub(r'^\d+\. ', '', l)).strip()
                starts.append(n); n += len([x for x in body.split('。') if x.strip()])
        starts.append(n)
        out.append(starts)
    return out


def _remap(o, st, drop=()):
    sh = lambda i: i - sum(1 for d in drop if d < i)
    f = lambda i: None if i is None else st[min(sh(i), len(st) - 1)]
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if k in ('at', 'until', 'title_at') and isinstance(v, int): o[k] = f(v)
            elif k == 'legs': o[k] = [[f(a), f(b)] for a, b in v]
            else: _remap(v, st, drop)
    elif isinstance(o, list):
        for v in o: _remap(v, st, drop)


_S = _line_to_sentence_starts()
assert len(_S) == len(chapters), (len(_S), len(chapters))
for _ch, _st in zip(chapters, _S):
    _remap(_ch['scene'], _st, DROP.get(_ch['key'], ()))
    if _ch['key'] in ('check', 'summary'):
        _tels = [e for e in _ch['scene'] if e.get('name') == 'pop_telop' and e.get('y', 0) >= 800]
        if _tels:
            _t0 = _tels[0]
            for _e in _ch['scene']:
                if _e.get('name') == 'pop_rows':
                    _e['size'] = 44; _e['y0'] = 150; _e['gap'] = 18
                    for _it in _e['items']: _it.setdefault('until', _t0['at'])
            _t0['y'] = 470; _t0['size'] = int(_t0['size'] * 1.5)
    _wide = False
    if _ch['key'] in _MAPCH:
        _ART = ['river', 'dawn', 'castle', 'docs']
        _ch['scene'].insert(0, bgimg(_ART[_MAPCH_ORDER.index(_ch['key']) % len(_ART)], at=0, dim=.6, blur=9))
        _bm = next((e for e in _ch['scene'] if e.get('name') == 'battle_map'), None)
        if _bm is not None:
            from PIL import Image as _Im
            _w, _h = _Im.open(Path(__file__).resolve().parents[1] / images[_bm['img']]['file']).size
            if _w / _h > 1.7:
                _wide = True
                _bm['box'] = [30, 110, 1890, 690]
                for _e in _ch['scene']:
                    if _e.get('name') == 'pop_rows': _e['x0'] = 60; _e['x1'] = 1860; _e['y0'] = 705; _e['size'] = 46
        _ch['scene'].append(tel('※位置・経路は概略の推定（資料の推定図と軍記による）', 1500 if _wide else 1440, 140 if _wide else 835, 28, at=0))
    if 'opener_until' in _ch: _ch['opener_until'] = _st[min(_ch['opener_until'], len(_st) - 1)]

T1 = '【姉川は圧勝だった？】姉川の戦い 家康の活躍と十一段崩しは本当か｜地図と『信長公記』で検証'
spec = dict(slug='anegawa', theme_dir='20261205_anegawa', pack='34_anegawa', header_sub='姉川の戦いを、地図の上で、『信長公記』と後世の逸話に分けて確かめる',
 images=images,
 bgm=[['intro', 'terrain', 'piano36'], ['dawn', 'gunki', 'piano12'], ['after', 'summary', 'piano40']],
 style='pop',
 chapters=chapters,
 desc=dict(title_main=T1, title_no=1,
  titles=[T1, '姉川の戦いを地図で解説 榊原康政の側面攻撃・磯野員昌の十一段崩しは同時代の記録にある？', '姉川の戦い 織田・徳川の勝ちと有名な逸話を、『信長公記』と軍記で分けて確かめる'],
  intro='元亀元年6月28日（ユリウス暦1570年7月30日、グレゴリオ暦では8月9日）、近江の姉川で、織田信長・徳川家康の軍と、浅井長政・朝倉景健の軍がぶつかりました。姉川の戦いです。この動画では、地図の上で軍勢を動かしながら、戦いの流れを追います。そして、「浅井・朝倉の奇襲だったのか」「榊原康政の側面攻撃」「磯野員昌の十一段崩し」「家康の活躍」という有名な話を、『信長公記』と、江戸時代の軍記・編纂物（『東照宮御実紀』など）、研究者の見方に分けて確かめます。分かることと決められないことを分けて、最後にまとめます。',
  points=['『信長公記』が書くこと：6/21に信長は虎御前山に陣取って小谷の城下を放火、6/22に退き、6/24に横山城を囲んで竜ヶ鼻に陣取り、家康も同じ竜ヶ鼻に陣取った。朝倉孫三郎の後巻が八千ほど、浅井備前の五千ほどが加わり、あわせて一万三千。6/27の暁に陣払いして帰ったと思われたが、6/28の未明に三十町ほどかかって来て、姉川を前にして野村の郷・三田村の郷へ移り、二手に備えた。西の三田村口の一番合戦に家康、東の野村の郷に信長の馬廻、さらに東に美濃三人衆が向かった。卯の刻に一戦となり、「推つ返しつ散々に入りみだれ」ついに追い崩し、真柄十郎左衛門・前波新八・遠藤喜右衛門ら首の注文のほか、宗徒の者千百余を討ち捕った。横山城は降参し、木下藤吉郎が定番として入った。(Wikisourceの翻刻で原文を確認)',
          '『信長公記』に書かれていないこと：榊原康政の側面攻撃、磯野員昌の十一段崩し、織田・徳川の兵数。『東照宮御実紀』（江戸時代後期に幕府が編纂した記録）は、朝倉一万五千余騎・浅井八千余騎とし、当初は信長が朝倉・家康が浅井に向かう手はずだったが暁に信長が陣を替えた、磯野員昌が織田の先陣を十一段まで切り崩した、本多忠勝らが浅井の大軍へ突入した、と書いています(Wikisourceの翻刻で原文を確認)。ただし榊原康政の側面攻撃は、『信長公記』にも『東照宮御実紀』の姉川の条にも見えません。',
          '奇襲だったのかは、読み方の問題です。『信長公記』は「奇襲」とは書いていません。ある研究者は浅井・朝倉の奇襲だったと見ており、日時を取り決めた合戦だったという見方、信長と足利義昭の軍事計画の一環だったと見る研究もあります(日本語版Wikipediaなどを通した紹介。原典は未確認で、研究者名は出していません)。',
          '数字：浅井・朝倉の兵数（『信長公記』は一万三千、『東照宮御実紀』は朝倉一万五千余・浅井八千余）、織田・徳川の兵数（書かれていない）、討ち取りの数（『信長公記』の千百余は、討ち取った側の書き方で、両軍の死者の総数ではありません）は、確かな数を決められません。',
          '『浅井三代記』（17世紀後半の書物。巻十五で原文を確認しました）にも十一段崩しの話がありますが、同時代の記録では確かめられません。「姉川の戦い」という呼び方は、もともと徳川方のものとされ、織田・浅井は「野村合戦」、朝倉は「三田村合戦」と呼んだ、と紹介されます。地図上の軍勢の動きは、記録にもとづく大まかな図で、実際の経路・順序ではありません。'],
  refs=['太田牛一『信長公記』巻三「あね川合戦之事」（Wikisource）:https://ja.wikisource.org/wiki/信長公記/我自刊我書', '『東照宮御実紀』巻二（Wikisource）:https://ja.wikisource.org/wiki/東照宮御実紀/卷二',
        'Wikipedia「姉川の戦い」(研究者の説と出典の整理)', '国立天文台 暦計算室「日本の暦日データベース」', '国土地理院 地理院タイル:https://maps.gsi.go.jp/development/ichiran.html'],
  credit_lines=['・図：自作（国土地理院タイル(陰影起伏図・標準地図)を加工して作成。現代の地形で、当時の川筋・湖岸・道ではありません。城・陣・経路の位置は、案内をもとにした概略の推定です）',
                '・肖像：織田信長・徳川家康・浅井長政・本多忠勝・豊臣秀吉：古い肖像画。Wikimedia Commonsで公開されているパブリックドメインの画像です。',
                '・イラスト：ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['地図上の軍勢の動きは、記録の描写と推定にもとづく概略の図で、実際の経路・時刻ではありません。', '『信長公記』は、Wikisourceの翻刻（旧字版）で該当部分を確認しました。『東照宮御実紀』も翻刻で確認しました。『浅井三代記』巻十五（Wikisource）も確認し、磯野員昌が織田の「十三段」の備えを「十一段」まで切り崩した記述、徳川勢の本多平八郎が朝倉勢へ突入する記述があることを確かめました（榊原康政の名は、この巻には見えません）。『三河物語』『信長記』、研究者の説、奇襲説・軍事計画説、呼び名、織田信治らの討死、その後の経過は、日本語版Wikipediaなど二次資料を通して確認したもので、原典は直接確認していません。'],
  tags='姉川の戦い, 織田信長, 徳川家康, 浅井長政, 朝倉景健, 信長公記, 戦国時代, 戦況解説, 検証, 十一段崩し',
  checks=['『信長記』『三河物語』の原文', '『大日本史料』元亀元年6月28日条', '奇襲説・信長と足利義昭の軍事計画説の原論文', '榊原康政の側面攻撃の出典', '国立天文台の換算ツールで、1570年7月30日（ユリウス暦）＝8月9日（グレゴリオ暦）の再確認']),
 thumb=dict(bg='assets/anegawa/thumb_art.png', lines=[['姉川の戦い', 112, 'white'], ['織田・徳川の', 96, 'white'], ['圧勝だった？', 112, 'gold']], sub='『信長公記』と後世の逸話を分けて確かめる', shade_col=[10, 14, 28], accent=[238, 96, 84], bar_col=[238, 96, 84], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and not o.get('title') and o['box'][3] - o['box'][1] <= 70: o['size'] = min(o.get('size', 40), 40)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


_fit(spec)
(R / 'data' / 'anegawa_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
