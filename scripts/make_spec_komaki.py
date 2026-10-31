"""Writes data/komaki_spec.json（小牧・長久手の戦い。戦況解説シリーズ5本目）。台本：docs/themes/20261226_komaki_nagakute/09_script_v2.md
文の番号（at・legs）は章内の0始まりの『行の番号』で書き、下で文の番号に直す。地図の座標は komaki_maps.norm()。
位置は、国土地理院住所検索（小牧山・犬山城・羽黒・小幡城・龍泉寺・岩崎城・長久手古戦場・色金山・御旗山・清洲城・岡崎城・蟹江城・長島城）の座標と、
長久手市・小牧市の資料の推定図をもとにした概略の推定（画面に『推定』と明記）。軍記・資料による動きは『資料の推定図と軍記による。実際の経路・順序は確定しない』と明記。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import komaki_maps as KM
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]
BOX = [60, 250, 1860, 850]
BLUE = (90, 150, 255); RED = (238, 96, 84); GRN = (110, 214, 140); GOLD = (239, 201, 118); WATER = (130, 195, 255)
CY = json.loads((R / 'data' / 'yamazaki_crops.json').read_text(encoding='utf8'))
SC = json.loads((R / 'data' / 'sekigahara_crops.json').read_text(encoding='utf8'))
CK = json.loads((R / 'data' / 'komaki_crops.json').read_text(encoding='utf8'))


def T(lon, lat): return list(KM.norm(lon, lat, 'theatre'))
def C(lon, lat): return list(KM.norm(lon, lat, 'core'))
def W(lon, lat): return list(KM.norm(lon, lat, 'wide'))


# 実在の地点（国土地理院住所検索）
KOMAKI = (136.9122, 35.2921); INUYAMA = (136.9373, 35.3863); HAGURO = (136.9734, 35.3525)
OBATA = (136.9913, 35.2166); RYUSEN = (136.9839, 35.2237); IROGANE = (137.0537, 35.1866); IWASAKI = (137.0332, 35.1462)
NAGAKUTE = (137.0465, 35.1727); OHATA_Y = (137.0434, 35.1791); KIYOSU = (136.8404, 35.2100); OKAZAKI = (137.1599, 34.9558)
KANIE = (136.7940, 35.1387); NAGASHIMA = (136.6900, 35.0939)
# 以下は、資料の推定図・案内をもとにした概略の推定位置（正確な地点ではない）
RAKUDEN = (136.9450, 35.3350)
KAMIJO = (137.0050, 35.2600)       # 上条（中入り隊の宿営地。推定）
SHIRAYAMA = (137.0145, 35.2131)    # 白山林（推定）
HINOKI = (137.0360, 35.1700)       # 桧ヶ根（推定）
FUJIGANE = (137.0480, 35.1830)     # 富士ヶ根（推定）
MID1 = (136.9780, 35.3120); MID2 = (136.9950, 35.2850)   # 中入り隊の経路（模式）



NOTE_IMG = 'イメージ（生成画像）。実際の場面の再現ではありません'
NOTE_GUNKI = '※資料の推定図と軍記による。実際の経路・順序は確定しない'

def pn(text, at, until=None, size=40, hi=True, col=None):
    """旧パネルの代わり：右側の白いカード（ポップ）。"""
    it = dict(at=at, text=text, col='orange')
    if until is not None: it['until'] = until
    return dict(t='anim', name='pop_rows', items=[it], x0=1010, x1=1880, y0=230, size=62, gap=0)


def tel(text, x, y, size, **kw): return dict(t='anim', name='pop_telop', text=text, x=x, y=y, size=size, **kw)
def rows(items, **kw): return dict(t='anim', name='pop_rows', items=items, **kw)
def bgimg(img, **kw): return dict(t='anim', name='pop_bgimg', img=img, **kw)


def unit(**k): return k
def NOTE_POS(at=0, txt='※位置は概略の推定'): return dict(xy=[0.02, 0.04], label='※推定', kind='spot', at=at, side='r', col=GOLD, lsize=28, _note=True)


MAPBOX = [30, 120, 1000, 880]


def _big(k):
    for pl in k.get('places', []):
        if not pl.get('_note'): pl['lsize'] = int(pl.get('lsize', 24) * 2.0)
        pl.pop('_note', None)
    for u in k.get('units', []):
        u['lsize'] = int(u.get('lsize', 26) * 2.0); u['head'] = int(u.get('head', 26) * 1.5)
        if 'lab_off' in u: u['lab_off'] = (int(u['lab_off'][0] * 2.0), int(u['lab_off'][1] * 2.0))
    for ln in k.get('lines', []): ln['lsize'] = int(ln.get('lsize', 26) * 2.0)
    for mk in k.get('marks', []): mk['lsize'] = int(mk.get('lsize', 24) * 1.5)


def amap(img='theatre', **k):
    _big(k)
    return dict(t='anim', name='battle_map', img=img, box=MAPBOX, at=0, **k)

_MAPCH = {'before', 'standoff', 'nakairi', 'chase', 'apr9', 'after9'}
_MAPCH_ORDER = ['before', 'standoff', 'nakairi', 'chase', 'apr9', 'after9']
DROP = {'before': {0, 1, 2, 4}, 'standoff': {2, 4, 6}, 'nakairi': {3, 4, 5, 6, 7, 9, 12, 13, 14}, 'chase': {1, 2, 4, 6, 7}, 'apr9': {2, 3, 5, 8, 9, 11, 13}, 'after9': {3, 6, 8, 10, 11, 12, 13}}

chapters = [
 dict(key='intro', title='小牧・長久手の戦い', chapter_title='導入：家康は、本当に勝ったのか', scene=[
   bgimg('docs', at=0, dim=.5, blur=4),
   tel('家康は\n本当に[[勝った]]？', 960, 470, 160, at=0, until=1, rot=-3),
   tel('2026年\n[[秀吉の朱印状]]\n2通 発見！', 960, 470, 130, at=1, until=2, rot=2),
   tel('秀吉は[[動揺していなかった]]', 960, 400, 92, at=2, until=3, plate='green', rot=-2),
   tel('池田・森が討ち死にしても…', 960, 640, 60, at=2, until=3, plate='blue', rot=1.5),
   tel('和議を申し入れたのは\n[[家康の側]]？（説）', 960, 470, 110, at=3, until=4, plate='yellow', rot=-2),
   tel('ただし、味方への手紙。\n[[有利に書いた]]可能性も', 960, 470, 100, at=4, until=5, plate='red', rot=2),
   tel('地図で追って、確かめる！', 960, 470, 120, at=5, plate='pink', rot=-2)]),

 dict(key='letters', title='新しく見つかった朱印状', chapter_title='新しく見つかった朱印状', scene=[
   bgimg('docs', at=0, dim=.55, blur=6),
   tel('朱印状\n[[2通]]発見！', 960, 470, 170, at=0, until=1, rot=-3),
   rows([dict(at=1, tag='発表', text='たつの市・龍野歴史文化資料館。8月発表、10/24から公開', col='blue', until=3),
         dict(at=2, tag='注意', text='以下は報道の要約。朱印状の原文ではない', col='red', until=3)], x0=110, x1=1810, y0=250, size=54, gap=34),
   rows([dict(at=3, tag='①4/21付', text='一通目：池田恒興・森長可の討死に触れる', col='orange', until=7),
         dict(at=5, tag='内容', text='陣地の普請を固めているので、心配するな', col='blue', until=7),
         dict(at=6, tag='専門家', text='局地戦では負けたが、秀吉側は動揺していなかった（村井准教授・説）', col='green', until=7)], x0=110, x1=1810, y0=210, size=50, gap=30),
   rows([dict(at=7, tag='②9/6付', text='二通目', col='orange', until=11),
         dict(at=8, tag='内容', text='西へ回り込み、火を放ち、砦を築いた。さらに戦うつもりだった', col='blue', until=11),
         dict(at=9, tag='和議', text='そこへ、信雄と家康から、人質を出すので和議を、と申し入れ', col='red', until=11),
         dict(at=10, tag='専門家', text='申し入れたのは家康の側だと、はっきりした（説）', col='green', until=11)], x0=110, x1=1810, y0=210, size=50, gap=30),
   tel('秀吉が[[家臣に宛てた]]手紙\n自分に有利に書いた可能性も', 960, 470, 96, at=11, until=12, plate='yellow', rot=-2),
   tel('以上は、報道で紹介された内容', 960, 470, 90, at=12, plate='blue', rot=1.5)]),
 dict(key='before', title='賤ヶ岳のあと', chapter_title='賤ヶ岳のあと', scene=[
   pn('天正11年　賤ヶ岳の戦い：羽柴秀吉が柴田勝家を倒す', 0, 1, 40), pn('織田信雄（信長の次男）は、このとき秀吉と協力していた', 1, 2, 40),
   pn('しかし、信雄と秀吉の関係は悪化していく（説）', 2, 3, 40, col='gold'), pn('天正12年3/6　信雄が、秀吉と通じたとして三人の家老（津川・岡田・浅井）を殺す', 3, 4, 36),
   pn('『太閤記』：秀吉の出兵は、三人の死への怒りから（軍記）', 4, 5, 38, col='gold'), pn('信雄は、徳川家康と手を結んでいた', 5, 6, 42),
   pn('秀吉は信雄を討つと決め、家康も信雄を助けて立ち上がる', 6, 7, 38), pn('3/13　家康が信雄の居城・清洲城に入る（小牧市の年表）', 7, None, 38),
   amap('wide', places=[NOTE_POS(0, '※位置は概略の推定'),
                        dict(xy=W(*NAGASHIMA), label='長島城（信雄）', kind='castle', at=3, side='b', col=RED, lsize=24),
                        dict(xy=W(*KIYOSU), label='清洲城', kind='castle', at=7, side='l', col=RED, lsize=24),
                        dict(xy=W(*OKAZAKI), label='岡崎城（家康の本国・三河）', kind='castle', at=5, side='r', col=RED, lsize=22),
                        dict(xy=W(*KOMAKI), label='小牧山', kind='spot', at=7, side='r', col=GOLD, lsize=22)],
        units=[unit(label='織田信雄', col=RED, portrait='p_nobukatsu', pts=[W(*NAGASHIMA)], at=1, head=24, lab_off=(36, -4), lsize=22),
               unit(label='徳川家康', sub='→ 清洲へ', col=RED, portrait='p_ieyasu', pts=[W(*OKAZAKI), W(*KIYOSU)], legs=[[6, 7]], at=5, head=26, lab_off=(36, 10), lsize=22, dashed=True)])]),
 dict(key='standoff', title='小牧山と楽田', chapter_title='小牧山と楽田', scene=[
   pn('3/13　池田恒興が秀吉方に寝返り、犬山城を奪う（小牧市の年表）', 0, 1, 38), pn('3/17　羽黒の戦い：徳川軍が森長可の隊を破る（小牧市の年表）', 1, 2, 38),
   pn('3/18　家康が小牧山城の改修を命じる。数日で防御工事が整う（小牧市の年表）', 2, 3, 36), pn('3月末　秀吉が楽田城に入る（小牧市の年表）', 3, 4, 40),
   pn('二重堀や、いくつもの砦を築かせる（小牧市の年表）', 4, 5, 40), pn('両軍は土塁を築き合い、にらみ合う。大きな戦いは起きない', 5, 6, 40),
   pn('4月に入っても、小競り合いが続く（小牧市の年表）', 6, 7, 40), pn('動かない戦いを動かしたのが「中入り」', 7, None, 42, col='gold'),
   amap(places=[NOTE_POS(0, '※位置は概略の推定'),
                dict(xy=T(*INUYAMA), label='犬山城', kind='castle', at=0, side='r', col=BLUE, lsize=24),
                dict(xy=T(*HAGURO), label='羽黒', kind='spot', at=1, side='r', col=RED, lsize=24),
                dict(xy=T(*KOMAKI), label='小牧山城', kind='castle', at=2, side='l', col=RED, lsize=24),
                dict(xy=T(*RAKUDEN), label='楽田城（推定）', kind='castle', at=3, side='r', col=BLUE, lsize=24)],
        lines=[dict(pts=[T(*KOMAKI), T(*RAKUDEN)], label='対陣（にらみ合い）', at=5, col=GOLD, dash=True, lab=[0.55, 0.40])],
        units=[unit(label='池田恒興', sub='犬山城を奪う', col=BLUE, portrait='p_ikeda', pts=[T(*INUYAMA)], at=0, head=22, lab_off=(36, -20), lsize=22),
               unit(label='森長可', sub='羽黒で敗れる', col=BLUE, portrait='p_mori', pts=[T(HAGURO[0], HAGURO[1] + 0.004), T(*INUYAMA)], legs=[[1, 2]], at=1, head=22, lab_off=(36, -4), lsize=22, dashed=True),
               unit(label='徳川家康', sub='小牧山へ', col=RED, portrait='p_ieyasu', pts=[T(*KIYOSU), T(*KOMAKI)], legs=[[2, 3]], at=2, head=26, lab_off=(-36, -4), lsize=22, dashed=True),
               unit(label='羽柴秀吉', sub='楽田へ', col=BLUE, portrait='p_hideyoshi', pts=[T(*INUYAMA), T(*RAKUDEN)], legs=[[3, 4]], at=3, head=26, lab_off=(36, 10), lsize=22, dashed=True)])]),
 dict(key='nakairi', title='三河中入り　誰の案か', chapter_title='三河中入り　誰の案か', scene=[
   pn('中入り：敵の守りを避けて、奥へ軍を入れる作戦', 0, 1, 40), pn('小牧山を避け、東の丘を回って、家康の本国・三河の岡崎を突こうとした（通説）', 1, 2, 34),
   pn('『太閤記』：この作戦は、池田恒興が願い出た（軍記）', 2, 3, 40, col='gold'), pn('4/4の夜　恒興が犬山の本陣に秀吉を訪ね、中入りを望む（軍記）', 3, 4, 38),
   pn('秀吉：「明日、返事をする」（軍記）', 4, 5, 42), pn('4/5の朝　恒興が再び訪ねる。篠木・柏井の人々を味方につける見通しも述べた（軍記）', 5, 6, 34),
   pn('秀吉は同意し、「敵を侮るな」といさめた（『太閤記』）', 6, 7, 38), pn('許されたのは、東三河に少し火を放ち、すぐに引き返す作戦と書かれる（軍記）', 7, 8, 34),
   pn('4/6の夜　池田・森・堀の三隊と、総大将・羽柴秀次の隊が、楽田を出発（長久手市の資料）', 8, 9, 34), pn('合わせて、およそ2万といわれる（説）', 9, 10, 42),
   pn('近年の研究には、別の説がある（日本語版Wikipediaが紹介。原典は未確認）', 10, 11, 36, col='gold'), pn('秀吉があらかじめ考えていた作戦を、恒興が意をくんで願い出た、という説', 11, 12, 36),
   pn('根拠の一つ：秀吉が丹羽長秀に宛てた、4/8付の書状と紹介される（説）', 12, 13, 36), pn('水軍の九鬼嘉隆も加えた、水陸の作戦だったという説も（説）', 13, 14, 36),
   pn('『太閤記』は、江戸時代の初めに書かれた秀吉の伝記', 14, 15, 40), pn('発案者は、確かめられた範囲では、同時代の記録から決められない', 15, None, 36, col='gold'),
   amap(places=[NOTE_POS(0, '※位置・経路は概略の推定。' + NOTE_GUNKI[1:]),
                dict(xy=T(*KOMAKI), label='小牧山', kind='castle', at=0, side='l', col=RED, lsize=22),
                dict(xy=T(*RAKUDEN), label='楽田', kind='castle', at=0, side='r', col=BLUE, lsize=22),
                dict(xy=T(*INUYAMA), label='犬山（秀吉の本陣）', kind='castle', at=3, side='r', col=BLUE, lsize=22),
                dict(xy=T(*KAMIJO), label='上条（宿営）', kind='camp', at=8, side='r', col=BLUE, lsize=22)],
        units=[unit(label='池田恒興', sub='4/4夜、秀吉を訪ねる', col=BLUE, portrait='p_ikeda', pts=[T(*RAKUDEN), T(*INUYAMA), T(*RAKUDEN)], legs=[[3, 4], [5, 6]], at=2, until=8, head=24, lab_off=(-36, -30), lsize=20, dashed=True),
               unit(label='中入り隊（約2万）', sub='池田・森・堀・秀次', col=BLUE, portrait='p_hidetsugu', pts=[T(*RAKUDEN), T(*MID1), T(*MID2), T(*KAMIJO)], legs=[[8, 9]], at=8, head=22, lab_off=(36, -4), lsize=20, dashed=True)])]),
 dict(key='chase', title='家康の追尾', chapter_title='家康の追尾', scene=[
   pn('4/7　羽柴軍の中入り隊が上条村に入り、砦を築いて宿営（小牧市の年表）', 0, 1, 36), pn('動きを家康に知らせたのは、篠木の住民（小牧市の年表）', 1, 2, 38),
   pn('『太閤記』『東照宮御実紀』も、篠木の人の知らせがきっかけと書く（軍記）', 2, 3, 34, col='gold'), pn('4/7　徳川の先遣隊が小牧を出て、小幡城へ（小牧市の年表）', 3, 4, 38),
   pn('『東照宮御実紀』：榊原康政・水野忠重らが先遣隊（軍記）', 4, 5, 38), pn('4/8の夜　家康と信雄の主力が小牧山を出る（長久手市の資料）', 5, 6, 38),
   pn('出た時刻は書物で違う：『東照宮御実紀』は夜8時ごろ、『太閤記』は昼2時ごろ（軍記）', 6, 7, 34, col='gold'), pn('小牧山には、本多忠勝らが残った（『東照宮御実紀』）', 7, 8, 38),
   pn('家康は、小幡城から色金山へ向かい、羽柴軍を追った（長久手市の資料）', 8, None, 36),
   amap(places=[NOTE_POS(0, '※位置・経路は概略の推定。' + NOTE_GUNKI[1:]),
                dict(xy=T(*KOMAKI), label='小牧山', kind='castle', at=0, side='l', col=RED, lsize=22),
                dict(xy=T(*KAMIJO), label='上条', kind='camp', at=0, side='r', col=BLUE, lsize=22),
                dict(xy=T(*OBATA), label='小幡城', kind='castle', at=3, side='l', col=RED, lsize=24),
                dict(xy=T(*IROGANE), label='色金山', kind='spot', at=8, side='r', col=RED, lsize=22)],
        units=[unit(label='中入り隊', sub='上条に宿営', col=BLUE, portrait='p_hidetsugu', pts=[T(*KAMIJO)], at=0, head=22, lab_off=(36, -4), lsize=20),
               unit(label='徳川先遣隊', sub='榊原・水野ら', col=RED, pts=[T(*KOMAKI), T(*OBATA)], legs=[[3, 4]], at=3, head=18, lab_off=(-36, 10), lsize=20, dashed=True),
               unit(label='徳川家康・織田信雄', sub='主力', col=RED, portrait='p_ieyasu', pts=[T(*KOMAKI), T(*OBATA), T(IROGANE[0] - 0.02, IROGANE[1] + 0.02), T(*IROGANE)], legs=[[5, 6], [8, 9]], at=5, head=26, lab_off=(-36, -30), lsize=20, dashed=True),
               unit(label='本多忠勝ら', sub='小牧山に残る', col=RED, portrait='p_honda', pts=[T(KOMAKI[0] + 0.006, KOMAKI[1] - 0.004)], at=7, head=22, lab_off=(-36, 10), lsize=20)])]),
 dict(key='apr9', title='四月九日', chapter_title='4月9日　長久手', scene=[
   pn('4/9の未明　池田恒興・元助の隊が、岩崎城（守将・丹羽氏重）を攻める', 0, 1, 36), pn('岩崎城は攻め落とされた（小牧市の年表）', 1, 2, 40),
   pn('そのころ後方の白山林では、羽柴秀次の隊が休んでいた（『東照宮御実紀』）', 2, 3, 34), pn('霧が深く、徳川軍が後ろから攻めかかった（『東照宮御実紀』）', 3, 4, 38),
   pn('秀次の隊は崩れる：白山林の戦い', 4, 5, 42), pn('堀秀政の隊が、桧ヶ根で徳川軍を迎え撃った（通説）', 5, 6, 38),
   pn('長久手市の資料：午前10時ごろ、長久手で池田・森の隊と家康の本隊が戦った', 6, 7, 34), pn('家康は、色金山の丘から戦場を見下ろしたと伝わる（長久手市の資料）', 7, 8, 36),
   pn('御旗山には、家康が牙旗を立てたと伝わる（長久手市の資料）', 8, 9, 38),
   pn('犬山城白帝文庫の屏風絵：井伊直政が鉄砲隊を率いて応戦。ただし17世紀なかばの作品', 9, 10, 32, col='gold'),
   pn('森長可は、眉間を鉄砲で撃たれて討死（『太閤記』）', 10, 11, 38), pn('『当代記』：長可は、羽黒のあと、討死を覚悟し、遺書を硯箱に残していた（軍記）', 11, 12, 34),
   pn('池田恒興と元助も討ち取られた（軍記）', 12, 13, 40), pn('恒興を討った者の名は、書物によって違う（軍記）', 13, 14, 38, col='gold'), pn('池田と森の討死は、のちの秀吉自身の書状にも記される', 14, None, 38, col='gold'),
   amap('core', places=[NOTE_POS(0, '※位置・経路は概略の推定。' + NOTE_GUNKI[1:]),
                        dict(xy=C(*IWASAKI), label='岩崎城', kind='castle', at=0, side='r', col=BLUE, lsize=24),
                        dict(xy=C(*SHIRAYAMA), label='白山林（推定）', kind='spot', at=2, until=6, side='r', col=BLUE, lsize=22),
                        dict(xy=C(*HINOKI), label='桧ヶ根（推定）', kind='spot', at=5, until=7, side='l', col=BLUE, lsize=22),
                        dict(xy=C(*NAGAKUTE), label='長久手古戦場', kind='spot', at=6, side='r', col=GOLD, lsize=22),
                        dict(xy=C(*IROGANE), label='色金山', kind='spot', at=7, side='r', col=RED, lsize=22),
                        dict(xy=C(*OHATA_Y), label='御旗山', kind='spot', at=8, side='r', col=RED, lsize=22)],
        units=[unit(label='池田恒興・元助', col=BLUE, portrait='p_ikeda', pts=[C(IWASAKI[0] + 0.003, IWASAKI[1] + 0.010), C(*IWASAKI), C(*NAGAKUTE)], legs=[[0, 1], [6, 7]], at=0, head=24, lab_off=(-36, 10), lsize=20, dashed=True),
               unit(label='羽柴秀次', sub='白山林', col=BLUE, portrait='p_hidetsugu', pts=[C(*SHIRAYAMA)], at=2, until=6, head=22, lab_off=(36, -4), lsize=20),
               unit(label='堀秀政', sub='桧ヶ根', col=BLUE, portrait='p_hori', pts=[C(*HINOKI)], at=5, until=7, head=22, lab_off=(-36, -4), lsize=20),
               unit(label='森長可', sub='討死', col=BLUE, portrait='p_mori', pts=[C(NAGAKUTE[0] - 0.004, NAGAKUTE[1] - 0.004)], at=10, head=20, lab_off=(-36, 10), lsize=20),
               unit(label='徳川家康', sub='色金山 → 富士ヶ根', col=RED, portrait='p_ieyasu', pts=[C(*IROGANE), C(*FUJIGANE)], legs=[[6, 7]], at=6, head=26, lab_off=(36, -12), lsize=20, dashed=True),
               unit(label='井伊直政', sub='鉄砲隊', col=RED, portrait='p_ii', pts=[C(FUJIGANE[0] - 0.004, FUJIGANE[1] - 0.006)], at=9, head=20, lab_off=(36, 10), lsize=20)])]),
 dict(key='after9', title='長久手のあと', chapter_title='長久手のあと', scene=[
   pn('秀吉は、午後1時ごろ、楽田を出陣（長久手市の資料）', 0, 1, 40), pn('龍泉寺まで進んだが、家康と信雄はすでに小幡城へ引いていた（長久手市の資料）', 1, 2, 34),
   pn('夜、家康は小牧山に戻る。午後8時ごろ（長久手市の資料）', 2, 3, 38), pn('4/10　秀吉も楽田へ戻る（長久手市の資料）', 3, 4, 40),
   pn('家康は深追いしなかった。「長追いするな」と制した（『太閤記』『東照宮御実紀』）', 4, 5, 34), pn('『東照宮御実紀』：本多忠勝が、わずかな手勢で秀吉の前に立ちはだかった', 5, 6, 36, col='gold'),
   pn('秀吉は感心し、味方に矢を射るなと命じた（軍記）', 6, 7, 40), pn('ただし、この出来事は旧暦の5/1ごろとみる指摘（日本語版Wikipedia）', 7, 8, 36, col='gold'),
   pn('旧暦5/1は、グレゴリオ暦では6/9。長久手の戦いの3週間ほどあと', 8, 9, 38),
   pn('死者の数は、記録によって、大きく違う', 9, 10, 40, col='gold'), pn('徳川方・松平家忠の日記：池田父子・森長可ほか、5千余を討ち捕った（同時代の日記）', 10, 11, 32, col='gold'),
   pn('『当代記』：2万余を討ち取った（軍記）', 11, 12, 40), pn('『東照宮御実紀』：羽柴方の首を1万3千余級と記す（軍記）', 12, 13, 36), pn('多くの解説は、羽柴方2500余と紹介（出典の書物は未確認）', 13, 14, 36), pn('5千余から、2万余まで。実際の数は分かっていない', 14, None, 38, col='gold'),
   amap(places=[NOTE_POS(0, '※位置・経路は概略の推定。' + NOTE_GUNKI[1:]),
                dict(xy=T(*RAKUDEN), label='楽田', kind='castle', at=0, side='r', col=BLUE, lsize=22),
                dict(xy=T(*RYUSEN), label='龍泉寺', kind='spot', at=1, side='l', col=GOLD, lsize=22),
                dict(xy=T(*OBATA), label='小幡城', kind='castle', at=1, side='r', col=RED, lsize=22),
                dict(xy=T(*KOMAKI), label='小牧山', kind='castle', at=2, side='l', col=RED, lsize=22)],
        units=[unit(label='羽柴秀吉', sub='楽田 → 龍泉寺 → 楽田', col=BLUE, portrait='p_hideyoshi', pts=[T(*RAKUDEN), T(*RYUSEN), T(*RAKUDEN)], legs=[[0, 1], [3, 4]], at=0, head=26, lab_off=(36, -20), lsize=20, dashed=True),
               unit(label='徳川家康', sub='小幡城 → 小牧山', col=RED, portrait='p_ieyasu', pts=[T(*OBATA), T(*KOMAKI)], legs=[[2, 3]], at=1, head=26, lab_off=(-36, 6), lsize=20, dashed=True),
               unit(label='本多忠勝', sub='『東照宮御実紀』では秀吉の前に', col=RED, portrait='p_honda', pts=[T(RYUSEN[0] - 0.012, RYUSEN[1] + 0.008)], at=5, head=20, lab_off=(-36, -4), lsize=18)])]),
 dict(key='views', title='評価は、分かれる', chapter_title='評価は、分かれる', scene=[
   bgimg('dusk', at=0, dim=.55, blur=6),
   tel('結局、[[誰の勝ち]]？', 960, 470, 150, at=0, until=1, rot=-3),
   rows([dict(at=1, tag='長久手', text='長久手だけ見れば、徳川方の勝ち（通説）', col='green', until=4),
         dict(at=2, tag='戦争全体', text='信雄が秀吉と和睦。家康は戦う大義を失った（通説）', col='red', until=4),
         dict(at=3, tag='研究者', text='見方は、いくつかに分かれる（説）', col='purple', until=4)], x0=110, x1=1810, y0=250, size=54, gap=36),
   rows([dict(at=4, tag='①', text='1584年の講和は形式的。1586年の上洛で、やっと服従', col='orange', until=9),
         dict(at=5, tag='②', text='1584年に人質を出した時点で、すでに服従の姿勢', col='blue', until=9),
         dict(at=6, tag='③', text='1586年の天正地震のあと、家康が臣従を表明', col='green', until=9),
         dict(at=7, tag='④', text='完全な服従は、1590年の小田原征伐の時', col='purple', until=9)], x0=110, x1=1810, y0=170, size=46, gap=24),
   tel('何を[[服従]]と見るかで、答えが変わる', 960, 840, 62, at=8, until=9, plate='yellow', rot=-1.5),
   tel('朱印状は、秀吉側を優勢とする\n最近の研究を[[補強]]（専門家・説）', 960, 470, 84, at=9, until=10, plate='blue', rot=2),
   tel('局地戦と、戦争全体を\n[[分けて]]考える材料', 960, 470, 110, at=10, plate='green', rot=-2)]),
 dict(key='check', title='分かること、決められないこと', chapter_title='分かること、決められないこと', scene=[
   bgimg('dusk', at=0, dim=.55, blur=6),
   rows([dict(at=0, tag='分かる', text='1584年4/9、長久手で、池田恒興と森長可が討死', col='green'),
         dict(at=1, tag='分かる', text='11月に信雄と秀吉が和睦。のちに家康も秀吉に従った', col='green'),
         dict(at=2, tag='不明', text='中入りを言い出したのは誰か', col='red'),
         dict(at=3, tag='不明', text='長久手の死者の数（5千余〜2万余）', col='red'),
         dict(at=4, tag='不明', text='本多忠勝が秀吉の前に立った日付', col='red'),
         dict(at=5, tag='不明', text='誰が勝ったと言うべきか（基準で変わる）', col='red')], x0=110, x1=1810, y0=170, size=50, gap=26),
   tel('通説・軍記・公的資料・同時代の書状。\n分けて見ると、[[見え方が変わる]]', 960, 850, 56, at=6, plate='yellow', rot=-1.2)]),
]

images = dict(
    theatre=dict(file='assets/komaki/map_theatre.png'), core=dict(file='assets/komaki/map_core.png'), wide=dict(file='assets/komaki/map_wide.png'),
    p_hideyoshi=dict(file='assets/portraits/hideyoshi.jpg', crop=CY['hideyoshi']), p_ieyasu=dict(file='assets/portraits/ieyasu.jpg', crop=SC['ieyasu']),
    p_ikeda=dict(file='assets/portraits/ikeda.jpg', crop=CY['ikeda']), p_hori=dict(file='assets/portraits/hori.jpg', crop=CY['hori']),
    p_ii=dict(file='assets/portraits/ii.jpg', crop=SC['ii']),
    p_nobukatsu=dict(file='assets/portraits/nobukatsu.jpg', crop=CK['nobukatsu']), p_mori=dict(file='assets/portraits/mori_n.jpg', crop=CK['mori_n']),
    p_hidetsugu=dict(file='assets/portraits/hidetsugu.jpg', crop=CK['hidetsugu']), p_honda=dict(file='assets/portraits/honda_t.jpg', crop=CK['honda_t']),
    hill=dict(file='assets/komaki/art_hill.png'), docs=dict(file='assets/komaki/art_docs.png'), dusk=dict(file='assets/komaki/art_dusk.png'))


def _line_to_sentence_starts():
    """台本の番号つきの行（1行に複数の文があることがある）→ 各行の最初の文の番号（vp.py の sentences と同じく「。」で区切る）。
    この spec の at / until / legs / title_at は『行の番号（0始まり）』で書き、ここで文の番号に直す。"""
    import re
    t = (R / 'docs' / 'themes' / '20261226_komaki_nagakute' / '09_script_v2.md').read_text(encoding='utf8')
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
        _ART = ['hill', 'docs', 'dusk']
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

spec = dict(slug='komaki', theme_dir='20261226_komaki_nagakute', pack='32_komaki', header_sub='小牧・長久手の戦いを、地図の上で、通説・軍記・新しく見つかった朱印状に分けて確かめる',
 images=images,
 bgm=[['intro', 'standoff', 'piano36'], ['nakairi', 'after9', 'piano12'], ['views', 'check', 'piano40']],
 style='pop',
 chapters=chapters,
 desc=dict(title_main='小牧・長久手の戦い「家康の勝ち」は本当か？ 新しく見つかった秀吉の朱印状と、記録で確かめる', title_no=1,
  titles=['小牧・長久手の戦いを地図で解説 池田恒興の中入り・長久手の戦い・新発見の秀吉朱印状', '小牧・長久手の戦い 本当に家康の勝ち？ 新発見の秀吉朱印状から読み直す', '小牧・長久手の戦いの流れ 三河中入りから和睦まで、軍記と記録を分けて確かめる'],
  intro='天正12年4月9日（グレゴリオ暦1584年5月18日）、尾張の長久手で、羽柴秀吉の軍の一部と徳川家康の軍がぶつかりました。小牧・長久手の戦いの山場です。この動画では、地図の上で軍勢を動かしながら、戦いの流れを追います。そして、「家康が勝った」「中入りは池田恒興の案」「本多忠勝が秀吉の前に立った」という有名な話を、江戸時代の軍記、長久手市・小牧市の資料、研究者の見方、そして2026年に見つかったと報じられた秀吉の朱印状2通に分けて確かめます。分かることと決められないことを分けて、最後にまとめます。',
  points=['中入りの発案：江戸時代初めの『太閤記』(小瀬甫庵)は、池田恒興が願い出て、秀吉が許したと書きます(4/4夜・4/5朝)。一方、近年の研究には、秀吉があらかじめ考えていた作戦を恒興が意をくんで願い出た、水軍の九鬼嘉隆も加えた水陸の作戦だった、という説があります(日本語版Wikipediaが紹介する説。原典は未確認で、研究者名は出していません)。この動画で確かめられた範囲では、同時代の記録からは決められません。',
          '長久手の戦い：長久手市の資料の推定図によると、羽柴方の中入り隊は池田恒興・元助、森長可、堀秀政、総大将の羽柴秀次。家康と信雄の主力は4/8の夜に小牧山を出て小幡城へ向かい、4/9に戦いました。森長可・池田恒興・元助は討死しました。屏風絵(犬山城白帝文庫蔵)は17世紀なかばの作品です。恒興を討った者の名は書物で違います。',
          '本多忠勝の逸話：『東照宮御実紀』は、4/9に忠勝がわずかな手勢で秀吉の前に立ちはだかり、秀吉が感心した、と書きます。日本語版Wikipediaは、書状の写しから、この出来事は旧暦5月1日ごろ(グレゴリオ暦6月9日)とみられる、という指摘を載せています(書状の写しは未確認)。死者の数は、記録によって大きく違います。松平家忠の日記(同時代の日記。国立国会図書館デジタルコレクションの『家忠日記』第3の画像で確認)は、4/9に池田父子・森長可ほか「五千余」を討ち捕った、『当代記』(史籍雑纂 第2。同、原文で確認)は「二万余」、『東照宮御実紀』は「羽柴方の首1万3千余級」、多くの解説は「2500余」と紹介します(この数字の出典の書物は未確認)。',
          '新しく見つかった朱印状：2026年5月に兵庫県たつの市の旧家で見つかり、8月に市立龍野歴史文化資料館が発表した、秀吉の朱印状2通です(たつの市は脇坂安治に宛てた書状と案内)。報道によれば、4月21日付は池田恒興・森長可の討死に触れ、陣地の普請を固めているので心配するな、という趣旨、9月6日付は、信雄・家康から人質を出すので和議を、と申し入れがあった、という内容です。東京大学史料編纂所の村井祐樹准教授は、秀吉側は局地戦では負けたが動揺していなかったこと、和議を申し入れたのは家康の側だったことが、はっきりした、と話しています。ただし、書状の全文は確認しておらず、報道の要約の範囲です。秀吉が自分の家臣に宛てた書状で、自分に有利に書いた可能性もあります。',
          '評価は分かれます：「いつ臣従したか」(1584年の講和／1586年の上洛／天正地震のあと／1590年の小田原征伐)と、「軍事的にどちらが優勢だったか」は、別の問いです。地図上の軍勢の動きは、資料の推定図と軍記にもとづく概略で、実際の経路・順序ではありません。'],
  refs=['松平家忠『家忠日記』第3(坪井九馬三・日下寛校、吉川半七、1897。国立国会図書館デジタルコレクション):https://dl.ndl.go.jp/pid/772515', '『当代記』(『史籍雑纂』第2。国立国会図書館デジタルコレクション):https://dl.ndl.go.jp/pid/769631', '長久手市「史跡の指定に至る経緯」(国指定史跡 長久手古戦場):https://www.city.nagakute.lg.jp/material/files/group/14/shiryo7.pdf', '長久手市「資料3　長久手合戦の様相」:https://www.city.nagakute.lg.jp/material/files/group/14/shiryou3_59757551.pdf',
        '小牧市「小牧・長久手の合戦」関連年表:https://www.city.komaki.aichi.jp/admin/soshiki/kyoiku/bunkazai/1_1/2/bunkazai/9161.html',
        '小瀬甫庵『太閤記』巻九(『史籍集覧』所収。Wikisource):https://ja.wikisource.org/wiki/太閤記/巻九', '『東照宮御実紀』巻三(Wikisource):https://ja.wikisource.org/wiki/東照宮御実紀/卷三',
        '読売新聞「小牧・長久手の戦い「家康が優位」の通説見直し？…秀吉から家臣への書状に「家康から和議申し込み」」2026-08-07:https://www.yomiuri.co.jp/culture/20260807-GYT1T00142/',
        'Japaaan「定説が覆る可能性…和睦は家康から？「小牧・長久手の戦い」で秀吉が発した朱印状2通が発見」2026-09-01:https://mag.japaaan.com/archives/285743',
        'たつの市 龍野歴史文化資料館 秋季企画展「龍野で出会う名品」:https://www.city.tatsuno.lg.jp/soshiki/1041/gyomu/4/1/11017.html',
        'Wikipedia「小牧・長久手の戦い」(研究者の説と出典の整理)', '国立天文台 暦計算室「日本の暦日データベース」', '国土地理院 地理院タイル:https://maps.gsi.go.jp/development/ichiran.html'],
  credit_lines=['・図：自作（国土地理院タイル(陰影起伏図・標準地図)を加工して作成。現代の地形で、当時の川筋・道ではありません。陣・城・経路の位置は、長久手市・小牧市の資料と案内をもとにした概略の推定です）',
                '・肖像：羽柴秀吉・池田恒興・堀秀政・徳川家康・井伊直政・織田信雄・森長可・豊臣秀次・本多忠勝：古い肖像画・近代の版画。いずれもWikimedia Commonsで公開されているパブリックドメインの画像です。後世の描写で、本人の姿とは限りません。',
                '・イラスト：ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['地図上の軍勢の動きは、資料の推定図と軍記にもとづく概略の図で、実際の経路・時刻ではありません。', '『太閤記』『東照宮御実紀』は、翻刻(Wikisource)で、『家忠日記』(天正12年3〜4月の条)と『当代記』(巻二の羽黒・長久手・和睦の条)は、国立国会図書館デジタルコレクションの画像・本文で、該当部分を確認しました。長久手市・小牧市の資料は、公開PDF・ページを確認しました(PDFは画像化して読みました)。2026年の朱印状は、新聞・ウェブ記事の報道で確認した範囲で、書状の全文は確認していません。岩澤・谷口などの研究者の説、秀吉の丹羽長秀宛4/8付書状、本多忠勝と秀吉の戦闘を5/1とする書状の写し、2500余・590余という数字の出典は、解説記事・Wikipediaなど二次資料を通して確認したもので、原典は直接確認していません。'],
  tags='小牧・長久手の戦い, 長久手の戦い, 徳川家康, 羽柴秀吉, 池田恒興, 森長可, 三河中入り, 朱印状, 戦国時代, 戦況解説, 検証',
  checks=['『家忠日記』の3/17の条(「三百余」)を、翻刻の画像で、読みを確かめ直す', '4/8付丹羽長秀宛の秀吉書状の原文と、岩澤・谷口の論考を確認する', '本多忠勝と秀吉の戦闘を5/1とする書状の写しの原文と、成立・対応関係を確認する', '龍野歴史文化資料館の展示・図録で、朱印状の翻刻を確認する', '『日本戦史 小牧役』の死者数の記述と、小牧市の説明の数字を確認する', '国立天文台の換算ツールで、4/8・4/9・4/21・5/1の日付を再確認する']),
 thumb=dict(bg='assets/komaki/thumb_art.png', lines=[['小牧・長久手の戦い', 100, 'white'], ['家康の勝ち', 118, 'white'], ['本当？', 126, 'gold']], sub='新しく見つかった朱印状と、記録で確かめる', shade_col=[10, 14, 28], accent=[238, 96, 84], bar_col=[238, 96, 84], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and not o.get('title') and o['box'][3] - o['box'][1] <= 70: o['size'] = min(o.get('size', 40), 40)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


_fit(spec)
(R / 'data' / 'komaki_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
