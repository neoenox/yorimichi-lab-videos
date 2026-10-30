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


ODANI = (136.277, 35.459); YOKOYAMA = (136.325, 35.394); TORA = (136.263, 35.445); OYORI = (136.311, 35.435)
NOMURA = (136.323, 35.419); MITA = (136.313, 35.420); GIFU = (136.7606, 35.4232); KANAGASAKI = (136.0775, 35.6757); SAWAYAMA = (136.2689, 35.2795)
# 以下は、案内をもとにした概略の推定位置（正確な地点ではない）
RYUGA = (136.318, 35.402)       # 竜ヶ鼻（推定）
_CORE_PX = [(0, 265), (60, 275), (120, 297), (190, 290), (260, 300), (330, 305), (400, 290), (470, 270), (520, 285), (555, 320), (590, 372), (650, 395), (720, 405), (790, 420), (828, 428)]
_AREA_PX_W = [(125, 490), (165, 445), (215, 400), (240, 375), (285, 355), (350, 358)]
ANE_PTS = [(136.19 + x / 978 * 0.22, 35.48 - y / 600 * 0.11) for x, y in _AREA_PX_W] + [(136.26 + x / 828 * 0.11, 35.445 - y / 600 * 0.065) for x, y in _CORE_PX[1:]]


def pn(text, at, until=None, size=40, hi=True, col=None):
    d = dict(t='panel', box=TOP, text=text, at=at, size=size, hi=hi)
    if until is not None: d['until'] = until
    if col: d['col'] = col
    return d


def unit(**k): return k
def NOTE_POS(at=0, txt='※位置は概略の推定'): return dict(xy=[0.02, 0.04], label=txt, kind='spot', at=at, side='r', col=GOLD, lsize=28)
def amap(img='area', **k): return dict(t='anim', name='battle_map', img=img, box=BOX, at=0, **k)
def RIVER(f, at=0): return dict(pts=[f(*p) for p in ANE_PTS], label='姉川（現代の川筋の概略）', at=at, col=WATER, dash=False, lab=[0.04, 0.38])


NOTE_IMG = 'イメージ（生成画像）。実際の場面の再現ではありません'
ART_BOX = [60, 170, 1860, 850]
EST = '※位置・経路は概略の推定'

chapters = [
 dict(key='intro', title='姉川の戦い', chapter_title='導入：姉川の戦い', opener='姉川の戦い', opener_until=2, scene=[
   dict(t='art', name='river', box=ART_BOX, at=0, dim=0.8, dir=1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.5),
   pn('姉川の戦いは、織田・徳川の圧勝だったのか', 0, 1, 40, col='gold'), pn('元亀元年6/28（ユリウス暦1570年7月30日）', 1, 2, 40),
   pn('グレゴリオ暦では、8月9日', 2, 3, 42), pn('近江・姉川：織田信長・徳川家康の軍 対 浅井長政・朝倉景健の軍', 3, 4, 36),
   pn('織田・徳川が勝った（通説）', 4, 5, 42, col='gold'), pn('「家康の活躍」「磯野員昌の十一段崩し」は、有名な話（通説）', 5, 6, 38, col='gold'),
   pn('同時代の記録は、この戦いを、どう書いているのか', 6, 7, 38), pn('地図の上で追い、記録を確かめる', 7, None, 42)]),
 dict(key='road', title='金ヶ崎から、虎御前山へ', chapter_title='金ヶ崎から、虎御前山へ', scene=[
   pn('元亀元年4月　信長が、越前の朝倉を攻めに向かう', 0, 1, 40), pn('妹お市の方の夫、浅井長政が、朝倉に味方（説）', 1, 2, 38),
   pn('挟み撃ちを避けて、信長は退く＝金ヶ崎の退き口（説）', 2, 3, 38), pn('浅井は朝倉勢を呼び、長比・刈安尾に要害を構えた（『信長公記』）', 3, 4, 34, col='gold'),
   pn('信長は調略で、長比城の堀・樋口を味方につけた（『信長公記』）', 4, 5, 34), pn('6/19　信長が出馬。浅井方の兵は、取る物も取りあえず退散（『信長公記』）', 5, 6, 32, col='gold'),
   pn('6/21　信長は虎御前山に陣取り、小谷の城下を放火（『信長公記』）', 6, 7, 34), pn('6/22　いったん退く。しんがりに、鉄砲500挺・弓30ほど（『信長公記』）', 7, 8, 34),
   pn('橋の上などで、敵の足軽と小競り合い（『信長公記』）', 8, 9, 38), pn('6/24　横山城を四方から囲み、信長は竜ヶ鼻に陣取る（『信長公記』）', 9, 10, 34, col='gold'),
   pn('家康も出陣し、同じ竜ヶ鼻に陣取る（『信長公記』）', 10, None, 38, col='gold'),
   amap(places=[NOTE_POS(0, EST),
                dict(xy=A(*ODANI), label='小谷城', kind='castle', at=1, side='r', col=RED, lsize=24),
                dict(xy=A(*TORA), label='虎御前山', kind='spot', at=6, side='l', col=BLUE, lsize=22),
                dict(xy=A(*YOKOYAMA), label='横山城', kind='castle', at=9, side='r', col=RED, lsize=22),
                dict(xy=A(*RYUGA), label='竜ヶ鼻（推定）', kind='spot', at=9, side='l', col=BLUE, lsize=22)], lines=[RIVER(A, 0)],
        units=[unit(label='織田信長', sub='岐阜方面から', col=BLUE, portrait='p_nobunaga', pts=[A(136.385, 35.425), A(*TORA), A(*RYUGA)], legs=[[5, 7], [8, 9]], at=5, head=26, lab_off=(-36, 10), lsize=22, dashed=True),
               unit(label='徳川家康', col=BLUE, portrait='p_ieyasu', pts=[A(RYUGA[0] + 0.006, RYUGA[1] + 0.004)], at=10, head=24, lab_off=(36, 20), lsize=22)])]),
 dict(key='forces', title='両軍の顔ぶれと、数', chapter_title='両軍の顔ぶれと、数', scene=[
   dict(t='art', name='docs', box=ART_BOX, at=0, dim=0.8, dir=-1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.66),
   dict(t='cols2', size=31, xm=940, xm2=980, until=4, left=dict(title='浅井・朝倉方', title_at=0, items=[
        dict(at=0, text='浅井長政・磯野員昌・遠藤直経ほか'), dict(at=1, text='朝倉景健（大将）')]),
        right=dict(title='織田・徳川方', title_at=2, items=[dict(at=2, text='織田信長・柴田勝家・木下秀吉・稲葉良通・氏家卜全・安藤守就ほか'), dict(at=3, text='徳川家康・酒井忠次・榊原康政・本多忠勝ほか')])),
   dict(t='cols2', size=30, xm=940, xm2=980, at=4, until=7, left=dict(title='『信長公記』が6/28に名を挙げる人', title_at=5, items=[
        dict(at=5, text='家康／信長の馬廻／美濃三人衆（稲葉・氏家・安藤）')]),
        right=dict(title='顔ぶれは書物で違う', title_at=4, items=[dict(at=4, text='参戦した武将は、書物によって挙げ方が違う'), dict(at=6, text='柴田勝家らの名は、前後の小谷城下の放火などの条に出てくる')])),
   dict(t='cols2', size=30, xm=940, xm2=980, at=7, left=dict(title='『信長公記』', title_at=7, items=[
        dict(at=7, text='朝倉8千ほど＋浅井5千ほど＝1万3千'), dict(at=9, text='織田・徳川の数は書かれていない')]),
        right=dict(title='『東照宮御実紀』（軍記）', title_at=8, items=[dict(at=8, text='朝倉1万5千余騎／浅井8千余騎'), dict(at=10, text='実際の数は、分かっていない')]))]),
 dict(key='terrain', title='地形と、城', chapter_title='地形と、城', scene=[
   pn('北近江の浅井の本拠は、小谷城（山城）', 0, 1, 40), pn('小谷城の南を、姉川が西へ流れ、琵琶湖へ向かう', 1, 2, 38),
   pn('姉川の南に、横山城。浅井方が守っていた', 2, 3, 40), pn('朝倉の軍は、小谷の東の大依山に陣取った（『信長公記』）', 3, 4, 36, col='gold'),
   pn('織田・徳川の軍は、横山城を囲み、竜ヶ鼻に陣取った（『信長公記』）', 4, 5, 36, col='gold'), pn('竜ヶ鼻から姉川までは、数キロ', 5, 6, 40),
   pn('姉川の北に、野村の郷と、三田村の郷', 6, 7, 40), pn('画面の地形は現代のもの。川筋・陣の位置は概略の推定', 7, None, 38),
   amap(places=[NOTE_POS(0, '※現代の地形。城・陣の位置は概略の推定'),
                dict(xy=A(*ODANI), label='小谷城', kind='castle', at=0, side='r', col=RED, lsize=26),
                dict(xy=A(*YOKOYAMA), label='横山城', kind='castle', at=2, side='r', col=RED, lsize=24),
                dict(xy=A(*OYORI), label='大依山（推定）', kind='spot', at=3, side='r', col=RED, lsize=22),
                dict(xy=A(*RYUGA), label='竜ヶ鼻（推定）', kind='spot', at=4, side='l', col=BLUE, lsize=22),
                dict(xy=A(NOMURA[0] + 0.004, NOMURA[1] + 0.002), label='野村', kind='spot', at=6, side='r', col=GOLD, lsize=22),
                dict(xy=A(MITA[0] - 0.004, MITA[1] + 0.002), label='三田村', kind='spot', at=6, side='l', col=GOLD, lsize=22)],
        lines=[RIVER(A, 1)])]),
 dict(key='dawn', title='陣払い、そして、未明', chapter_title='陣払い、そして、未明', scene=[
   dict(t='art', name='dawn', box=ART_BOX, at=0, dim=0.8, dir=1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.5, until=1),
   pn('『信長公記』は、こう書く', 0, 1, 42, col='gold'), pn('6/27の暁、浅井・朝倉は陣払いして、帰ったと思われた', 1, 2, 38),
   pn('ところが、6/28の未明、30町ほど、かかって来た', 2, 3, 40, col='gold'), pn('30町は、3キロ余り。1町は約109メートル', 3, 4, 40),
   pn('姉川を前にして、野村の郷と三田村の郷へ移り、二手に備えた', 4, 5, 36, col='gold'), pn('この文などから、浅井・朝倉の奇襲だった、とみる研究者も（説）', 5, 6, 34),
   pn('日時を取り決めた合戦だった、という見方も（説）', 6, 7, 38), pn('信長と将軍足利義昭の、軍事計画の一環とみる研究も（説）', 7, 8, 36),
   pn('ただし、公記は「奇襲」とは書いていない。読み方の問題', 8, 9, 38, col='gold'), pn('取り決めがあっても、浅井・朝倉と合意した、という意味かは、確かめられない', 9, None, 34),
   amap(places=[NOTE_POS(0, EST),
                dict(xy=A(*OYORI), label='大依山（推定）', kind='spot', at=0, side='r', col=RED, lsize=22),
                dict(xy=A(NOMURA[0] + 0.004, NOMURA[1] + 0.002), label='野村', kind='spot', at=4, side='r', col=GOLD, lsize=22),
                dict(xy=A(MITA[0] - 0.004, MITA[1] + 0.002), label='三田村', kind='spot', at=4, side='l', col=GOLD, lsize=22),
                dict(xy=A(*RYUGA), label='竜ヶ鼻（推定）', kind='spot', at=0, side='l', col=BLUE, lsize=22)], lines=[RIVER(A, 4)],
        units=[unit(label='朝倉軍', sub='大依山から', col=RED, pts=[A(OYORI[0] + 0.004, OYORI[1] + 0.004), A(MITA[0] - 0.002, MITA[1] + 0.003)], legs=[[2, 4]], at=0, head=24, lab_off=(-36, -20), lsize=20, dashed=True),
               unit(label='浅井軍', sub='小谷方面から', col=RED, portrait='p_nagamasa', pts=[A(OYORI[0] + 0.012, OYORI[1] + 0.012), A(NOMURA[0] + 0.004, NOMURA[1] + 0.003)], legs=[[2, 4]], at=0, head=24, lab_off=(36, -20), lsize=20, dashed=True)])]),
 dict(key='lines', title='布陣', chapter_title='布陣', scene=[
   pn('『信長公記』の布陣', 0, 1, 42, col='gold'), pn('西は三田村口。一番合戦に、家康が向かった', 1, 2, 38, col='gold'),
   pn('東は野村の郷。信長の馬廻が向かい、さらに東は美濃三人衆', 2, 3, 36, col='gold'), pn('公記が書くのは、ここまで。両軍全体の配置は書かれていない', 3, 4, 36),
   pn('『東照宮御実紀』は、違う話を書く（軍記）', 4, 5, 38, col='gold'), pn('信長は朝倉に、家康は浅井に向かう予定だった（軍記）', 5, 6, 36),
   pn('暁に、信長は朝倉の大軍を見て、陣を替えた（軍記）', 6, 7, 38), pn('家康は「大軍に向かうのが、勇士の本意」と答えた（軍記）', 7, None, 36),
   amap('core', places=[NOTE_POS(0, EST),
                        dict(xy=C(MITA[0] - 0.004, MITA[1] + 0.002), label='三田村口', kind='spot', at=1, side='l', col=GOLD, lsize=22),
                        dict(xy=C(NOMURA[0] + 0.004, NOMURA[1] + 0.002), label='野村の郷', kind='spot', at=2, side='r', col=GOLD, lsize=22),
                        dict(xy=C(*RYUGA), label='竜ヶ鼻（推定）', kind='spot', at=0, side='l', col=BLUE, lsize=20)], lines=[RIVER(C, 0)],
        units=[unit(label='徳川家康', sub='三田村口へ', col=BLUE, portrait='p_ieyasu', pts=[C(RYUGA[0] - 0.01, RYUGA[1] - 0.001), C(MITA[0], MITA[1] - 0.012)], legs=[[1, 2]], at=0, head=24, lab_off=(-36, 10), lsize=20, dashed=True),
               unit(label='信長の馬廻', sub='野村の郷へ', col=BLUE, portrait='p_nobunaga', pts=[C(RYUGA[0] + 0.004, RYUGA[1] + 0.001), C(NOMURA[0] - 0.002, NOMURA[1] - 0.012)], legs=[[2, 3]], at=0, head=24, lab_off=(36, 10), lsize=20, dashed=True),
               unit(label='美濃三人衆', sub='さらに東へ', col=BLUE, pts=[C(RYUGA[0] + 0.02, RYUGA[1] + 0.002), C(NOMURA[0] + 0.014, NOMURA[1] - 0.012)], legs=[[2, 3]], at=0, head=20, lab_off=(36, 10), lsize=18, dashed=True),
               unit(label='朝倉軍', col=RED, pts=[C(MITA[0] - 0.003, MITA[1] + 0.004)], at=1, head=22, lab_off=(-36, -20), lsize=20),
               unit(label='浅井軍', col=RED, portrait='p_nagamasa', pts=[C(NOMURA[0] + 0.003, NOMURA[1] + 0.005)], at=2, head=22, lab_off=(36, -20), lsize=20)])]),
 dict(key='battle', title='姉川　戦闘', chapter_title='姉川　戦闘', scene=[
   pn('6/28　卯の刻（午前6時ごろ）', 0, 1, 42), pn('『信長公記』：敵も姉川へかかり合い、推しつ返しつ、散々に入り乱れ', 1, 2, 34, col='gold'),
   pn('黒煙を立て、しのぎを削り、鍔を割り、ついに追い崩した（『信長公記』）', 2, 3, 34, col='gold'), pn('戦いが、何時に終わったかは、公記にない', 3, 4, 38),
   pn('戦いの描写は、公記では、この数行だけ', 4, 5, 38), pn('有名な、榊原康政の側面攻撃（通説）', 5, 6, 40, col='gold'),
   pn('公記にも、『東照宮御実紀』の姉川の条にも、見えない', 6, 7, 38, col='gold'), pn('本多忠勝らの徳川勢の突入は、『東照宮御実紀』が書く（軍記）', 7, None, 34),
   amap('core', places=[NOTE_POS(0, '※位置は概略の推定。軍記による描写')], lines=[RIVER(C, 0)],
        units=[unit(label='徳川勢', col=BLUE, portrait='p_ieyasu', pts=[C(MITA[0], MITA[1] - 0.012), C(MITA[0] - 0.002, MITA[1] + 0.002)], legs=[[1, 3]], at=0, head=24, lab_off=(-36, 10), lsize=20, dashed=True),
               unit(label='織田勢', col=BLUE, portrait='p_nobunaga', pts=[C(NOMURA[0] - 0.002, NOMURA[1] - 0.012), C(NOMURA[0], NOMURA[1] + 0.001)], legs=[[1, 3]], at=0, head=24, lab_off=(36, 10), lsize=20, dashed=True),
               unit(label='朝倉軍', col=RED, pts=[C(MITA[0] - 0.003, MITA[1] + 0.004), C(MITA[0] - 0.012, MITA[1] + 0.02)], legs=[[2, 3]], at=1, head=22, lab_off=(-36, -20), lsize=20),
               unit(label='浅井軍', col=RED, portrait='p_nagamasa', pts=[C(NOMURA[0] + 0.003, NOMURA[1] + 0.005), C(NOMURA[0] + 0.008, NOMURA[1] + 0.02)], legs=[[2, 3]], at=1, head=22, lab_off=(36, -20), lsize=20)])]),
 dict(key='gunki', title='「十一段崩し」と、家康の働き', chapter_title='「十一段崩し」と、家康の働き', scene=[
   pn('『東照宮御実紀』は、さらに書く（軍記）', 0, 1, 40, col='gold'), pn('浅井方の磯野員昌が、織田の先陣を、十一段まで切り崩した（軍記）', 1, 2, 36),
   pn('長政も、馬廻を励まして、かかった（軍記）', 2, 3, 38), pn('家康は、織田の旗色が乱れるのを見て、旗本の備えを崩してかかれと命じた（軍記）', 3, 4, 32),
   pn('本多忠勝らが浅井の大軍へ突入。浅井勢は横を討たれて、小谷城へ逃げ入った（軍記）', 4, 5, 32), pn('『浅井三代記』にも、十一段崩しの話がある', 5, 6, 38),
   pn('17世紀後半の書物で、同時代の記録では、確かめられない（軍記）', 6, 7, 36, col='gold'), pn('『信長公記』には、十一段崩しも、書かれていない', 7, None, 38, col='gold'),
   amap('core', places=[NOTE_POS(0, '※位置は概略の推定。軍記による描写'), dict(xy=C(*RYUGA), label='織田の本陣（竜ヶ鼻・推定）', kind='spot', at=1, side='l', col=BLUE, lsize=20)], lines=[RIVER(C, 0)],
        units=[unit(label='磯野員昌', sub='十一段崩し（軍記）', col=RED, pts=[C(NOMURA[0], NOMURA[1] - 0.004), C(RYUGA[0] + 0.004, RYUGA[1] + 0.006)], legs=[[1, 2]], at=1, head=22, lab_off=(36, -20), lsize=20, dashed=True),
               unit(label='本多忠勝ら', sub='突入（軍記）', col=BLUE, portrait='p_honda', pts=[C(MITA[0] - 0.002, MITA[1] - 0.012), C(NOMURA[0] - 0.01, NOMURA[1] - 0.003)], legs=[[3, 5]], at=3, head=22, lab_off=(-36, 10), lsize=20, dashed=True)])]),
 dict(key='after', title='討ち取りと、その後', chapter_title='討ち取りと、その後', scene=[
   pn('『信長公記』の「首の注文」＝討ち取った首の一覧', 0, 2, 38, col='gold'), pn('前波新八・前波新太郎・弓削六郎左衛門・今村掃部助・浅井雅楽助ら', 1, 2, 34),
   pn('朝倉方の真柄十郎左衛門は、青木所左衛門が討った', 2, 3, 36), pn('浅井方の遠藤喜右衛門は、竹中久作が討った。かねて首を取ると高言していた', 3, 4, 32),
   pn('このほか、主だった者、千百余を討ち捕った（『信長公記』）', 4, 5, 36, col='gold'), pn('討ち取った側の書き方。両軍の死者の総数ではない', 5, 6, 38),
   pn('大谷（小谷）まで、五十町を追い討ちし、麓を放火', 6, 7, 38), pn('大谷は高山で、一気に攻め上るのは難しいと考え、横山へ戻った', 7, 8, 34),
   pn('横山城は降参。木下藤吉郎が定番（城を守る役）として入る', 8, 9, 36, col='gold'), pn('7/1　信長は佐和山城を囲む', 9, 10, 40),
   pn('7/6　信長は上洛し、将軍に状況を報告', 10, 11, 40), pn('7/8　信長は岐阜に戻る（『信長公記』）', 11, None, 40),
   amap('wide', places=[NOTE_POS(0, EST), dict(xy=W(*ODANI), label='小谷城（大谷）', kind='castle', at=6, side='l', col=RED, lsize=22),
                dict(xy=W(*YOKOYAMA), label='横山城', kind='castle', at=7, side='r', col=BLUE, lsize=22),
                dict(xy=W(*SAWAYAMA), label='佐和山城', kind='castle', at=9, side='r', col=RED, lsize=22),
                dict(xy=W(*GIFU), label='岐阜', kind='castle', at=11, side='l', col=BLUE, lsize=22)],
        units=[unit(label='織田・徳川軍', sub='追い討ち→横山城', col=BLUE, portrait='p_nobunaga', pts=[W(NOMURA[0], NOMURA[1]), W(ODANI[0] + 0.01, ODANI[1] - 0.012), W(*YOKOYAMA), W(*SAWAYAMA), W(*GIFU)], legs=[[6, 7], [7, 8], [9, 10], [10, 11]], at=6, head=24, lab_off=(-36, 10), lsize=20, dashed=True),
               unit(label='木下藤吉郎', sub='横山城の定番', col=BLUE, portrait='p_hideyoshi', pts=[W(YOKOYAMA[0] - 0.02, YOKOYAMA[1] + 0.02)], at=8, head=20, lab_off=(-36, 20), lsize=20)])]),
 dict(key='next', title='その後', chapter_title='その後', scene=[
   pn('浅井・朝倉は、この戦いに敗れた。しかし、滅びてはいない（説）', 0, 1, 36), pn('秋には、浅井・朝倉が琵琶湖の西へ出て、志賀の陣が始まる（説）', 1, 2, 34),
   pn('森可成や、信長の弟の織田信治が討死（説）', 2, 3, 38), pn('浅井・朝倉が倒れるのは、天正元年。3年後（説）', 3, 4, 38),
   pn('磯野員昌が守る佐和山城も、のちに織田方へ降る（説）', 4, 5, 36), pn('姉川の勝ちは、決定的ではなかった', 5, None, 42, col='gold'),
   amap('wide', places=[NOTE_POS(0, '※位置は概略'), dict(xy=W(*ODANI), label='小谷城', kind='castle', at=0, side='l', col=RED, lsize=24),
                        dict(xy=W(*SAWAYAMA), label='佐和山城', kind='castle', at=4, side='r', col=RED, lsize=24), dict(xy=W(*YOKOYAMA), label='横山城', kind='castle', at=0, side='r', col=BLUE, lsize=22)])]),
 dict(key='source', title='呼び名と、資料', chapter_title='呼び名と、資料', scene=[
   dict(t='art', name='docs', box=ART_BOX, at=0, dim=0.8, dir=1, note='イメージ（生成画像）。実際の資料の再現ではありません'), dict(t='shade', box=ART_BOX, at=0, alpha=0.66),
   dict(t='cols2', size=30, xm=940, xm2=980, until=3, left=dict(title='呼び名', title_at=0, items=[
        dict(at=0, text='「姉川の戦い」は、もともと徳川方の呼び方（説）')]),
        right=dict(title='ほかの呼び名', title_at=1, items=[dict(at=1, text='織田・浅井：野村合戦／朝倉：三田村合戦（説）'), dict(at=2, text='『信長公記』は「あね川」を地名として書く')])),
   dict(t='cols2', size=30, xm=940, xm2=980, at=3, left=dict(title='『信長公記』', title_at=3, items=[
        dict(at=3, text='同時代に近い記録。織田の側の記録'), dict(at=4, text='家康の働きを詳しく書くことは目的ではない')]),
        right=dict(title='『東照宮御実紀』', title_at=5, items=[
        dict(at=5, text='江戸幕府が、徳川家の事績をまとめた記録'), dict(at=6, text='どちらにも視点がある。分けて見るのが、確かめる第一歩')]))]),
 dict(key='summary', title='分かること、決められないこと', chapter_title='分かること、決められないこと', scene=[
   dict(t='art', name='castle', box=ART_BOX, at=0, dim=0.8, dir=-1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.62),
   dict(t='cols2', size=32, xm=940, xm2=980, until=6, left=dict(title='分かること', title_at=0, items=[
        dict(at=0, text='元亀元年6/28、姉川で、織田・徳川が浅井・朝倉に勝った'), dict(at=1, text='公記は千百余を討ち捕ったと書く。横山城は降参')]),
        right=dict(title='決められないこと', title_at=2, items=[
        dict(at=2, text='両軍の実際の兵力'), dict(at=3, text='浅井・朝倉の奇襲だったのか'),
        dict(at=4, text='榊原康政の側面攻撃・十一段崩しは、実際にあったのか'), dict(at=5, text='主戦場の正確な場所')])),
   dict(t='cols2', size=33, xm=940, xm2=980, at=6, left=dict(title='見方', title_at=6, items=[
        dict(at=6, text='通説・軍記・同時代の記録。分けて見ると、見え方が変わる')]), right=dict(title='', title_at=6, items=[]))]),
]

images = dict(
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


def _remap(o, st):
    f = lambda i: None if i is None else st[min(i, len(st) - 1)]
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if k in ('at', 'until', 'title_at') and isinstance(v, int): o[k] = f(v)
            elif k == 'legs': o[k] = [[f(a), f(b)] for a, b in v]
            else: _remap(v, st)
    elif isinstance(o, list):
        for v in o: _remap(v, st)


_S = _line_to_sentence_starts()
assert len(_S) == len(chapters), (len(_S), len(chapters))
for _ch, _st in zip(chapters, _S):
    _remap(_ch['scene'], _st)
    if 'opener_until' in _ch: _ch['opener_until'] = _st[min(_ch['opener_until'], len(_st) - 1)]

T1 = '【姉川は圧勝だった？】姉川の戦い 家康の活躍と十一段崩しは本当か｜地図と『信長公記』で検証'
spec = dict(slug='anegawa', theme_dir='20261205_anegawa', pack='34_anegawa', header_sub='姉川の戦いを、地図の上で、『信長公記』と後世の逸話に分けて確かめる',
 images=images,
 bgm=[['intro', 'terrain', 'piano36'], ['dawn', 'gunki', 'piano12'], ['after', 'summary', 'piano40']],
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
