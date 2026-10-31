"""Writes data/mikatagahara_spec.json（三方ヶ原の戦い。戦況解説シリーズ6本目）。台本：docs/themes/20261128_mikatagahara/09_script_v2.md
文の番号（at・legs）は章内の0始まりの『行の番号』で書き、下で文の番号に直す。地図の座標は mikatagahara_maps.norm()。
位置は、国土地理院住所検索（浜松城・堀江城・二俣城・一言坂・犀ヶ崖・甲府・伊那・三方原町・根洗）の座標と、案内をもとにした概略の推定（画面に『推定』と明記）。
軍記による動きは『軍記による描写。実際の経路・順序は確定しない』と明記。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mikatagahara_maps as MM
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]
BOX = [60, 250, 1860, 850]
BLUE = (90, 150, 255); RED = (238, 96, 84); GRN = (110, 214, 140); GOLD = (239, 201, 118); WATER = (130, 195, 255)
NC = json.loads((R / 'data' / 'nagashino_crops.json').read_text(encoding='utf8'))
SC = json.loads((R / 'data' / 'sekigahara_crops.json').read_text(encoding='utf8'))
CK = json.loads((R / 'data' / 'komaki_crops.json').read_text(encoding='utf8'))


def A(lon, lat): return list(MM.norm(lon, lat, 'area'))
def M(lon, lat): return list(MM.norm(lon, lat, 'mid'))
def W(lon, lat): return list(MM.norm(lon, lat, 'wide'))


KOFU = (138.5703, 35.665); INA = (137.9539, 35.8275); FUTAMATA = (137.8158, 34.8645); HAMAMATSU = (137.725, 34.7126)
HORIE = (137.6203, 34.7604); SAIGA = (137.7218, 34.7159); ICHIGON = (137.8358, 34.7234); NODA = (137.4671, 34.8791); MIKATA = (137.712, 34.7816)
NEARAI = (137.7042, 34.7968)
# 以下は、案内をもとにした概略の推定位置（正確な地点ではない）
IWAI = (137.672, 34.812)           # 祝田の坂（推定）
SHIRASUKA = (137.5054, 34.6958)    # 白須賀（織田の援軍の分散配置の西端）


def pn(text, at, until=None, size=40, hi=True, col=None):
    d = dict(t='panel', box=TOP, text=text, at=at, size=size, hi=hi)
    if until is not None: d['until'] = until
    if col: d['col'] = col
    return d


def unit(**k): return k
def NOTE_POS(at=0, txt='※位置は概略の推定'): return dict(xy=[0.02, 0.04], label=txt, kind='spot', at=at, side='r', col=GOLD, lsize=28)
def amap(img='area', **k): return dict(t='anim', name='battle_map', img=img, box=BOX, at=0, **k)


NOTE_IMG = 'イメージ（生成画像）。実際の場面の再現ではありません'
NOTE_GUNKI = '※軍記による描写。実際の経路・順序は確定しない'
ART_BOX = [60, 170, 1860, 850]

chapters = [
 dict(key='intro', title='三方ヶ原の戦い', chapter_title='導入：三方ヶ原の戦い', opener='三方ヶ原の戦い', opener_until=2, scene=[
   dict(t='art', name='plateau', box=ART_BOX, at=0, dim=0.8, dir=1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.5),
   pn('家康は、なぜ、浜松城から出て、信玄と戦ったのか', 0, 1, 40, col='gold'), pn('元亀3年12月22日（ユリウス暦1573年1月25日）', 1, 2, 40),
   pn('グレゴリオ暦では、2月4日', 2, 3, 42), pn('遠江・三方ヶ原：武田信玄の軍 対 徳川家康の軍', 3, 4, 40),
   pn('家康は大敗した（通説）', 4, 5, 42, col='gold'), pn('「犀ヶ崖の夜襲」「空城の計」は、有名な話（通説）', 5, 6, 38, col='gold'),
   pn('同時代の記録は、この戦いを、どう書いているのか', 6, 7, 38), pn('地図の上で追い、記録を確かめる', 7, None, 42)]),
 dict(key='saijo', title='信玄の西上', chapter_title='信玄の西上', scene=[
   pn('元亀3年10月　武田信玄が甲府を出陣', 0, 1, 40), pn('目指したのは遠江と三河。徳川領を攻めるため', 1, 2, 38),
   pn('信玄の本隊は、およそ2万2千とされる', 2, 3, 40), pn('『東照宮御実紀』は、「4万5千余」と書く（軍記）', 3, 4, 38, col='gold'),
   pn('数字は書物で大きく違い、確かな数は分かっていない', 4, 5, 38), pn('10/14　一言坂で徳川軍が武田軍と衝突し、敗れる', 5, 6, 38),
   pn('武田軍は、徳川の要の城・二俣城を囲む', 6, 7, 40), pn('二俣城の開城：12/19とする説と、11月末とする説（説）', 7, 8, 36, col='gold'),
   pn('信長は、家康のもとへ援軍を送っていた（『信長公記』）', 8, None, 38, col='gold'),
   amap('wide', places=[NOTE_POS(0, '※位置・経路は概略の推定（模式）'),
                        dict(xy=W(*KOFU), label='甲府', kind='castle', at=0, side='r', col=RED, lsize=24),
                        dict(xy=W(*FUTAMATA), label='二俣城', kind='castle', at=6, side='l', col=BLUE, lsize=24),
                        dict(xy=W(*HAMAMATSU), label='浜松城', kind='castle', at=1, side='l', col=BLUE, lsize=24),
                        dict(xy=W(*ICHIGON), label='一言坂', kind='spot', at=5, side='r', col=GOLD, lsize=22)],
        units=[unit(label='武田信玄', sub='甲府 → 遠江', col=RED, portrait='p_shingen', pts=[W(*KOFU), W(*INA), W(*FUTAMATA)], legs=[[0, 1], [5, 6]], at=0, head=26, lab_off=(36, -4), lsize=22, dashed=True),
               unit(label='徳川家康', sub='浜松城', col=BLUE, portrait='p_ieyasu', pts=[W(*HAMAMATSU)], at=1, head=24, lab_off=(-36, 10), lsize=22)])]),
 dict(key='forces', title='両軍の顔ぶれ', chapter_title='両軍の顔ぶれ', scene=[
   dict(t='art', name='docs', box=ART_BOX, at=0, dim=0.8, dir=-1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.66),
   dict(t='cols2', size=31, xm=940, xm2=980, until=2, left=dict(title='武田方', title_at=0, items=[
        dict(at=0, text='武田信玄（本隊）'), dict(at=0, text='山県昌景・馬場信春・内藤昌豊'), dict(at=0, text='四郎勝頼')]),
        right=dict(title='徳川方', title_at=1, items=[dict(at=1, text='徳川家康'), dict(at=1, text='酒井忠次・本多忠勝・大久保忠世・榊原康政ほか')])),
   dict(t='cols2', size=29, xm=940, xm2=980, at=2, left=dict(title='織田の援軍', title_at=2, items=[
        dict(at=2, text='『信長公記』：大将は、佐久間信盛・平手汎秀・水野信元')]),
        right=dict(title='書物で違う', title_at=3, items=[
        dict(at=4, text='『松平記』：平手・水野・林・佐久間（軍記）'), dict(at=4, text='『総見記』：佐久間・平手に、林・水野・毛利・美濃三人衆（軍記）'),
        dict(at=5, text='数：『総見記』3千／『明智軍記』5千'), dict(at=5, text='『佐久間軍記』約1万5千／『甲陽軍鑑』約1万9千／『前橋酒井家旧蔵聞書』2万（軍記）'), dict(at=6, text='2万とみる研究者も。ただし岡崎〜白須賀に分散（説）'),
        dict(at=7, text='実際に戦場にいた数は、分かっていない')]))]),
 dict(key='terrain', title='地形と、浜松城', chapter_title='地形と、浜松城', scene=[
   pn('徳川家康の本拠は、浜松城', 0, 1, 42), pn('北西に広がる台地が、三方ヶ原', 1, 2, 42),
   pn('台地には祝田へ下る坂。武田軍は、この坂を下ろうとしていた、といわれる', 2, 3, 34, col='gold'), pn('台地を西へ進めば、浜名湖近くの堀江城へ向かう', 3, 4, 38),
   pn('『信長公記』：信玄は堀江城へ向かった', 4, 5, 40, col='gold'), pn('画面の地形は現代のもの。城・坂の位置は概略の推定', 5, None, 40),
   amap(places=[NOTE_POS(0, '※現代の地形。城・坂の位置は概略の推定'),
                dict(xy=A(*HAMAMATSU), label='浜松城', kind='castle', at=0, side='r', col=BLUE, lsize=26),
                dict(xy=A(*MIKATA), label='三方ヶ原（台地）', kind='spot', at=1, side='r', col=GOLD, lsize=24),
                dict(xy=A(*IWAI), label='祝田の坂（推定）', kind='spot', at=2, side='l', col=RED, lsize=22),
                dict(xy=A(*HORIE), label='堀江城', kind='castle', at=3, side='b', col=RED, lsize=24)],
        lines=[dict(pts=[A(*MIKATA), A(*IWAI), A(*HORIE)], label='武田軍の進路（推定）', at=3, col=RED, dash=True, lab=[0.30, 0.62])],
        units=[unit(label='徳川家康', col=BLUE, portrait='p_ieyasu', pts=[A(*HAMAMATSU)], at=0, head=24, lab_off=(36, 10), lsize=22)])]),
 dict(key='why', title='家康は、なぜ出たのか', chapter_title='家康は、なぜ出たのか', scene=[
   pn('12/22　武田軍が二俣城を出発', 0, 1, 42), pn('西へ進み、浜松城を素通りするように見えた', 1, 2, 40),
   pn('家康は、籠城するつもりだった、といわれる（説）', 2, 3, 38), pn('それが、軍を出して、武田軍を追った（通説）', 3, 4, 40),
   pn('通説：信玄の挑発に、乗った', 4, 5, 42, col='gold'), pn('別説①『当代記』：物見の浜松衆の小競り合いから、思いがけず合戦になった（軍記）', 5, 6, 32),
   pn('別説②堀江城が落ちると、浜松城への補給路が脅かされる（説）', 6, 7, 34), pn('別説③家臣・国人の信頼をつなぎ止めるため（説）', 7, 8, 36),
   pn('どれも決め手はなく、出陣の理由は確かめられない', 8, 9, 38, col='gold'), pn('『信長公記』は、理由を書いていない', 9, None, 40),
   amap(places=[NOTE_POS(0, '※位置・経路は概略の推定。' + NOTE_GUNKI[1:]),
                dict(xy=A(*HAMAMATSU), label='浜松城', kind='castle', at=0, side='r', col=BLUE, lsize=24),
                dict(xy=A(*MIKATA), label='三方ヶ原', kind='spot', at=3, side='r', col=GOLD, lsize=22),
                dict(xy=A(*HORIE), label='堀江城', kind='castle', at=6, side='b', col=RED, lsize=22)],
        units=[unit(label='武田軍', sub='二俣城から西へ', col=RED, portrait='p_shingen', pts=[A(FUTAMATA[0] - 0.08, FUTAMATA[1] - 0.04), A(NEARAI[0] + 0.01, NEARAI[1] + 0.02), A(*IWAI)], legs=[[0, 1], [1, 3]], at=0, head=24, lab_off=(36, -20), lsize=20, dashed=True),
               unit(label='徳川家康', sub='籠城 → 出陣', col=BLUE, portrait='p_ieyasu', pts=[A(*HAMAMATSU), A(*MIKATA)], legs=[[3, 4]], at=2, head=24, lab_off=(-36, 10), lsize=20, dashed=True)])]),
 dict(key='battle', title='三方ヶ原　戦闘', chapter_title='三方ヶ原　戦闘', scene=[
   pn('家康は浜松城から出陣。織田の援軍も加わった（『信長公記』）', 0, 1, 36, col='gold'), pn('夕刻、三方ヶ原の台地に着いたといわれる', 1, 2, 40),
   pn('武田軍は、すでに陣を構えて待っていた', 2, 3, 40), pn('武田は魚鱗の陣、徳川は鶴翼の陣と伝わる（軍記）', 3, 4, 38, col='gold'),
   pn('戦いは、日没までの、短い時間で決まったといわれる', 4, 5, 38), pn('『信長公記』：信玄は「水股之者」と名づけた300人ほどを先頭に立て、礫を打たせた', 5, 6, 32, col='gold'),
   pn('太鼓を打ち鳴らして、攻めかかった（『信長公記』）', 6, 7, 38), pn('一番合戦で、平手甚左衛門と家臣、成瀬藤蔵らが討死（『信長公記』）', 7, 8, 34),
   pn('信長に勘当されていた元小姓4人も、家康を頼って遠江におり、討死（『信長公記』）', 8, 9, 32), pn('清洲の町人・具足屋の玉越三十郎（24歳か25歳）が、4人を見舞いに来ていた', 9, 10, 32),
   pn('帰るように言われても帰らず、4人と一緒に討死した（『信長公記』）', 10, 11, 34),
   pn('死傷者は、武田200・徳川2,000といわれる。ただし出典の書物は未確認（説）', 11, 12, 32, col='gold'), pn('『当代記』：信玄の軍2万、浜松衆8千ばかり。徳川方の討死は千余（軍記）', 12, 13, 32), pn('数字は書物で違い、確かな数は決められない', 13, None, 38),
   amap(places=[NOTE_POS(0, '※位置・経路は概略の推定。' + NOTE_GUNKI[1:]),
                dict(xy=A(*HAMAMATSU), label='浜松城', kind='castle', at=0, side='r', col=BLUE, lsize=24),
                dict(xy=A(*NEARAI), label='三方ヶ原（主戦場は不明）', kind='spot', at=1, side='l', col=GOLD, lsize=22)],
        units=[unit(label='徳川家康・織田の援軍', col=BLUE, portrait='p_ieyasu', pts=[A(*HAMAMATSU), A(MIKATA[0] + 0.01, MIKATA[1] - 0.02)], legs=[[0, 2]], at=0, head=24, lab_off=(36, 10), lsize=20, dashed=True),
               unit(label='武田軍（魚鱗）', col=RED, portrait='p_shingen', pts=[A(NEARAI[0] - 0.01, NEARAI[1] + 0.012)], at=2, head=26, lab_off=(-36, -20), lsize=20),
               unit(label='武田勝頼ほか', col=RED, portrait='p_katsuyori', pts=[A(NEARAI[0] - 0.035, NEARAI[1] + 0.02)], at=3, head=20, lab_off=(-36, -4), lsize=18)])]),
 dict(key='flee', title='家康の敗走', chapter_title='家康の敗走', scene=[
   pn('徳川軍は崩れた。家康も追い詰められる', 0, 1, 40), pn('『信長公記』は、家康の様子を、こう書く', 1, 2, 40, col='gold'),
   pn('乱戦の中、岸道を下がりながら、待ち受ける敵を、馬上から弓で射倒して駆け抜けた、と読める（解釈は分かれる）', 2, 3, 30, col='gold'),
   pn('浜松城は堅固に保たれた。信玄は勝利を得て、軍を納めた（『信長公記』）', 3, 4, 34), pn('『東照宮御実紀』：夏目吉信が家康を逃がし、身代わりに討死（軍記）', 4, 5, 34, col='gold'),
   pn('家康の馬の尻を槍の柄で叩き、浜松の方へ向かわせたという話（軍記）', 5, 6, 34), pn('夏目吉信の身代わりの話は、『信長公記』にはない', 6, 7, 38, col='gold'),
   pn('家康が浜松城へ逃げ込んだ後の話は、次の章で見る', 7, None, 38),
   amap(places=[NOTE_POS(0, '※位置・経路は概略の推定。' + NOTE_GUNKI[1:]),
                dict(xy=A(*HAMAMATSU), label='浜松城', kind='castle', at=0, side='r', col=BLUE, lsize=24),
                dict(xy=A(*MIKATA), label='三方ヶ原', kind='spot', at=0, side='l', col=GOLD, lsize=22)],
        units=[unit(label='徳川家康', sub='敗走', col=BLUE, portrait='p_ieyasu', pts=[A(MIKATA[0], MIKATA[1] - 0.01), A(*HAMAMATSU)], legs=[[2, 4]], at=0, head=26, lab_off=(36, 10), lsize=22, dashed=True),
               unit(label='夏目吉信', sub='身代わり（軍記）', col=BLUE, pts=[A(MIKATA[0] + 0.01, MIKATA[1] - 0.01)], at=4, head=18, lab_off=(-36, -24), lsize=20)])]),
 dict(key='night', title='夜の、二つの逸話', chapter_title='夜の、二つの逸話', scene=[
   pn('①「空城の計」（通説）', 0, 1, 42, col='gold'), pn('『東照宮御実紀』：家康は城門を閉めさせず、門の内外に大篝火を焚かせた（軍記）', 1, 2, 32),
   pn('湯漬けを三杯食べ、高いびきで寝た（軍記）', 2, 3, 38), pn('武田軍はためらい、そのすきに鳥居・植村・天野・渡辺らが出て追い払ったと書かれる（軍記）', 3, 4, 30),
   pn('②「犀ヶ崖の夜襲」（通説）', 4, 5, 42, col='gold'), pn('『東照宮御実紀』：その夜、大久保忠世らが武田軍の陣に鉄砲を撃ちかけた（軍記）', 5, 6, 32),
   pn('穴山梅雪の陣の人馬が、犀ヶ崖に落ちて、多くが死んだ（軍記）', 6, 7, 36), pn('『信長公記』には、この夜襲も、城門の話もない', 7, 8, 38, col='gold'),
   pn('犀ヶ崖は、江戸幕府の編纂史料が初出で、同時代の史料にはない、とする解説がある（説）', 8, None, 32, col='gold'),
   amap(places=[NOTE_POS(0, '※位置・経路は概略の推定。' + NOTE_GUNKI[1:]),
                dict(xy=A(*HAMAMATSU), label='浜松城', kind='castle', at=0, side='r', col=BLUE, lsize=24),
                dict(xy=A(SAIGA[0], SAIGA[1] + 0.012), label='犀ヶ崖（城の北）', kind='spot', at=4, side='l', col=GOLD, lsize=22)],
        units=[unit(label='大久保忠世ら', sub='夜襲（軍記）', col=BLUE, pts=[A(*HAMAMATSU), A(SAIGA[0], SAIGA[1] + 0.012)], legs=[[5, 7]], at=5, head=20, lab_off=(-36, 10), lsize=20, dashed=True),
               unit(label='武田軍', sub='陣', col=RED, portrait='p_baba', pts=[A(SAIGA[0] - 0.005, SAIGA[1] + 0.02)], at=4, head=20, lab_off=(-36, -20), lsize=20)])]),
 dict(key='check', title='有名な逸話を、確かめる', chapter_title='有名な逸話を、確かめる', scene=[
   dict(t='art', name='ravine', box=ART_BOX, at=0, dim=0.8, dir=1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.66),
   dict(t='cols2', size=29, xm=940, xm2=980, until=5, left=dict(title='「味噌」の話', title_at=0, items=[
        dict(at=0, text='家康が、恐怖で失禁し、「これは味噌だ」と言い張った（通説）'), dict(at=1, text='出典が判明していない（説）'),
        dict(at=2, text='類似の話は『三河後風土記』にあるが、一言坂の戦いの後の話（説）')]),
        right=dict(title='「酒井の太鼓」', title_at=3, items=[dict(at=4, text='酒井忠次が櫓で太鼓を打ち、武田軍に伏兵を疑わせた（通説）')])),
   dict(t='cols2', size=29, xm=940, xm2=980, at=5, left=dict(title='「酒井の太鼓」の出どころ', title_at=5, items=[
        dict(at=5, text='明治6年に初演された歌舞伎で広まった。『三河後風土記』にも記述はない、とされる（説）')]),
        right=dict(title='「小山田信茂の投石隊」', title_at=6, items=[
        dict(at=7, text='『信長公記』：投石隊は「水股之者」。信茂の名はない'), dict(at=8, text='『総見記』の書き方が誤読され、明治の参謀本部の本で信茂が率いたとされて広まった、とされる（説）')]))]),
 dict(key='after', title='その後', chapter_title='その後', scene=[
   pn('近年の説では、戦いの翌日から信玄は堀江城を攻めた（説）', 0, 1, 34, col='gold'), pn('しかし、4日ほどで引き返したといわれる（説）', 1, 2, 38),
   pn('続いて、東三河の野田城を攻める（説）', 2, 3, 40), pn('信玄は、元亀4年4/12、信濃の波合で亡くなった、と『東照宮御実紀』は書く（軍記）', 3, 4, 32, col='gold'),
   pn('『当代記』：信濃の駒場で亡くなった。場所は記録によって違う（軍記）', 4, 5, 36), pn('武田軍は兵を引き上げた。信玄の西上は、ここで止まった', 5, 6, 38), pn('信玄の死を聞いた家康は、惜しむべきことだと語った、と『東照宮御実紀』は書く（軍記）', 6, 7, 32),
   pn('天正3年　長篠の戦いで、武田勝頼は織田・徳川連合軍に敗れる', 7, None, 36),
   amap('mid', places=[NOTE_POS(0, '※位置は概略の推定'),
                       dict(xy=M(*HAMAMATSU), label='浜松城', kind='castle', at=0, side='b', col=BLUE, lsize=24),
                       dict(xy=M(*HORIE), label='堀江城', kind='castle', at=0, side='l', col=RED, lsize=24),
                       dict(xy=M(*NODA), label='野田城', kind='castle', at=2, side='r', col=RED, lsize=24)],
        units=[unit(label='武田軍', sub='堀江城 → 野田城', col=RED, portrait='p_shingen', pts=[M(*HORIE), M(*NODA)], legs=[[1, 3]], at=0, head=24, lab_off=(36, -20), lsize=20, dashed=True)])]),
 dict(key='source', title='史料を、分けて見る', chapter_title='史料を、分けて見る', scene=[
   dict(t='art', name='docs', box=ART_BOX, at=0, dim=0.8, dir=1, note='イメージ（生成画像）。実際の資料の再現ではありません'), dict(t='shade', box=ART_BOX, at=0, alpha=0.66),
   dict(t='cols2', size=30, xm=940, xm2=980, until=6, left=dict(title='『信長公記』に書かれていること', title_at=1, items=[
        dict(at=2, text='織田の援軍、武田の投石隊、討死した人々、家康の弓の働き')]),
        right=dict(title='書かれていないこと', title_at=3, items=[
        dict(at=3, text='犀ヶ崖の夜襲・城門を開けた話・夏目吉信の身代わり・味噌・酒井の太鼓'),
        dict(at=4, text='『当代記』の三方ヶ原の条にも、犀ヶ崖の夜襲は見えない（軍記）'),
        dict(at=5, text='犀ヶ崖は江戸幕府の編纂物、酒井の太鼓は明治の歌舞伎、味噌は出典不明（説）')])),
   dict(t='cols2', size=30, xm=940, xm2=980, at=6, left=dict(title='『信長公記』', title_at=6, items=[
        dict(at=6, text='信長の側の記録。家康の戦いの全体を書くことが目的ではない')]),
        right=dict(title='『東照宮御実紀』', title_at=7, items=[
        dict(at=7, text='江戸幕府が、徳川家の事績をまとめた記録'), dict(at=8, text='どちらにも視点がある。分けて見るのが、確かめる第一歩')]))]),
 dict(key='summary', title='分かること、決められないこと', chapter_title='分かること、決められないこと', scene=[
   dict(t='art', name='castle', box=ART_BOX, at=0, dim=0.8, dir=-1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.62),
   dict(t='cols2', size=32, xm=940, xm2=980, until=6, left=dict(title='分かること', title_at=0, items=[
        dict(at=0, text='元亀3年12/22、三方ヶ原で、武田軍が徳川・織田の軍に勝った'), dict(at=1, text='平手汎秀らが討死し、家康は浜松城へ逃げ帰った')]),
        right=dict(title='決められないこと', title_at=2, items=[
        dict(at=2, text='家康は、なぜ出陣したのか'), dict(at=3, text='織田の援軍の顔ぶれと数。両軍の兵力と死者の数'),
        dict(at=4, text='犀ヶ崖の夜襲や空城の計は、実際にあったのか'), dict(at=5, text='主戦場の正確な場所')])),
   dict(t='cols2', size=33, xm=940, xm2=980, at=6, left=dict(title='見方', title_at=6, items=[
        dict(at=6, text='通説・軍記・同時代の記録。分けて見ると、見え方が変わる')]), right=dict(title='', title_at=6, items=[]))]),
]

images = dict(
    area=dict(file='assets/mikatagahara/map_area.png'), mid=dict(file='assets/mikatagahara/map_mid.png'), wide=dict(file='assets/mikatagahara/map_wide.png'),
    p_shingen=dict(file='assets/portraits/shingen.jpg', crop=[0.28, 0.42, 0.62, 0.78]), p_ieyasu=dict(file='assets/portraits/ieyasu.jpg', crop=SC['ieyasu']),
    p_katsuyori=dict(file='assets/portraits/katsuyori.jpg', crop=NC['katsuyori']), p_baba=dict(file='assets/portraits/baba.jpg', crop=NC['baba']),
    plateau=dict(file='assets/mikatagahara/art_plateau.png'), docs=dict(file='assets/mikatagahara/art_docs.png'),
    ravine=dict(file='assets/mikatagahara/art_ravine.png'), castle=dict(file='assets/mikatagahara/art_castle.png'))


def _line_to_sentence_starts():
    import re
    t = (R / 'docs' / 'themes' / '20261128_mikatagahara' / '09_script_v2.md').read_text(encoding='utf8')
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

spec = dict(slug='mikatagahara', theme_dir='20261128_mikatagahara', pack='33_mikatagahara', header_sub='三方ヶ原の戦いを、地図の上で、『信長公記』と後世の逸話に分けて確かめる',
 images=images,
 bgm=[['intro', 'terrain', 'piano36'], ['why', 'night', 'piano12'], ['check', 'summary', 'piano40']],
 chapters=chapters,
 desc=dict(title_main='【家康はなぜ出陣した？】三方ヶ原の戦い 犀ヶ崖の夜襲は本当か｜地図と『信長公記』で検証', title_no=1,
  titles=['【家康はなぜ出陣した？】三方ヶ原の戦い 犀ヶ崖の夜襲は本当か｜地図と『信長公記』で検証', '三方ヶ原の戦いを地図で解説 空城の計・犀ヶ崖・味噌の話は同時代の記録にある？', '三方ヶ原の戦い 家康の大敗と有名な逸話を、『信長公記』と軍記で分けて確かめる'],
  intro='元亀3年12月22日（ユリウス暦1573年1月25日、グレゴリオ暦では2月4日）、遠江の三方ヶ原で、武田信玄の軍と徳川家康の軍がぶつかりました。三方ヶ原の戦いです。この動画では、地図の上で軍勢を動かしながら、戦いの流れを追います。そして、「家康はなぜ出陣したのか」「犀ヶ崖の夜襲」「空城の計」「味噌」「酒井の太鼓」「小山田信茂の投石隊」という有名な話を、『信長公記』と、江戸時代の軍記・編纂物（『東照宮御実紀』など）、研究者の見方に分けて確かめます。分かることと決められないことを分けて、最後にまとめます。',
  points=['『信長公記』が書くこと：織田の援軍の大将は佐久間信盛・平手甚左衛門・水野下野守。武田軍は「水股之者」と名づけた300人ほどを先頭に礫を打たせ、太鼓を打ち鳴らして攻めた。一番合戦で平手甚左衛門や家康の家臣の成瀬藤蔵らが討死し、信長に勘当されていた元小姓4人（長谷川橋介・佐脇藤八・山口飛弾・加藤弥三郎）と、清洲の町人・具足屋の玉越三十郎も討死した。家康については、岸道を下がりながら、馬上から弓で敵を射倒して駆け抜けた、と読める記述があります（文の解釈は分かれます）。(Wikisourceの翻刻で原文を確認)',
          '『信長公記』に書かれていないこと：犀ヶ崖の夜襲、城門を開けて湯漬けを食べた「空城の計」、夏目吉信の身代わり、味噌、酒井の太鼓。『東照宮御実紀』（江戸時代後期に幕府が編纂した記録）には、夏目吉信の身代わり、門の内外の大篝火、湯漬け三椀と高いびき、大久保忠世らの鉄砲と「犀が磯」に落ちた武田軍の話が書かれています(Wikisourceの翻刻で原文を確認)。ある解説は、犀ヶ崖の戦いは江戸幕府の編纂史料が初出で、同時代の史料にはないとしています。',
          '家康が出陣した理由は決め手がありません。通説は信玄の挑発。ほかに、物見の小競り合いからの巻き込まれ(『当代記』に、浜松衆の物見が十騎、二十騎ずつ駆けて来て小競り合いになり、これを引き取らせようと家康が出馬したところ、思いがけず合戦になった、とあります。国立国会図書館デジタルコレクションの原文で確認)、堀江城が落ちて浜松城への補給路が脅かされるのを恐れた、家臣・国人の信頼をつなぎ止めるため、という説があります(後ろ二つは日本語版Wikipediaが紹介する説。原典は未確認で、研究者名は出していません)。',
          '数字：武田軍の兵数（本隊およそ2万2千、『東照宮御実紀』は4万5千余、『当代記』は信玄の軍2万・浜松衆8千ばかり・徳川方の討死千余）、織田の援軍の数（3千〜約1万9千、2万）、死傷者（武田200・徳川2,000という紹介がありますが出典の書物は未確認）は、書物によって大きく違い、確かな数は分かっていません。二俣城の開城も、12月19日とする説と11月末とする説があります。',
          '味噌の話は出典が判明していません。酒井の太鼓は明治6年初演の歌舞伎で広まった話とされます。小山田信茂の投石隊は、『総見記』の書き方が誤読され、明治の参謀本部の『日本戦史』で信茂が率いたと書かれて広まったとされます（『信長公記』に信茂の名はありません）。地図上の軍勢の動きは、軍記の描写と推定にもとづく概略の図で、実際の経路・順序ではありません。'],
  refs=['『当代記』(『史籍雑纂』第2。国立国会図書館デジタルコレクション):https://dl.ndl.go.jp/pid/769631', '太田牛一『信長公記』巻五「味方か原合戦之事」（Wikisource）:https://ja.wikisource.org/wiki/信長公記/我自刊我書', '『東照宮御実紀』巻二（Wikisource）:https://ja.wikisource.org/wiki/東照宮御実紀/卷二',
        'Wikipedia「三方ヶ原の戦い」(研究者の説と出典の整理)', '国立天文台 暦計算室「日本の暦日データベース」', '国土地理院 地理院タイル:https://maps.gsi.go.jp/development/ichiran.html'],
  credit_lines=['・図：自作（国土地理院タイル(陰影起伏図・標準地図)を加工して作成。現代の地形で、当時の川筋・湖岸・道ではありません。城・坂・経路の位置は、案内をもとにした概略の推定です）',
                '・肖像：徳川家康・武田勝頼・馬場信春：古い肖像画。武田信玄：歌川国芳の浮世絵（想像図）。いずれもWikimedia Commonsで公開されているパブリックドメインの画像です。浮世絵は後世の描写で、本人の姿とは限りません。',
                '・イラスト：ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['地図上の軍勢の動きは、軍記の描写と推定にもとづく概略の図で、実際の経路・時刻ではありません。', '『信長公記』は、Wikisourceの翻刻（旧字版）で該当部分を確認しました。「水股之者」の部分は、諸本で「水役之者」と書かれる異同があります。『東照宮御実紀』も翻刻で確認しました。『当代記』(史籍雑纂 第2。巻二の三方ヶ原の条、信玄の死、国立国会図書館デジタルコレクションの原文)も確認しました(犀ヶ崖の夜襲は見えません)。『三河物語』『甲陽軍鑑』、研究者の説、死傷者200・2,000という数字、二俣城の開城日、犀ヶ崖が初出とされる点、味噌・酒井の太鼓・小山田信茂の話は、日本語版Wikipediaなど二次資料を通して確認したもので、原典は直接確認していません。'],
  tags='三方ヶ原の戦い, 武田信玄, 徳川家康, 犀ヶ崖, 信長公記, 戦国時代, 戦況解説, 検証, 空城の計, 浜松城',
  checks=['『信長公記』諸本の本文（「水股之者」と「水役之者」の異同）', '『三河物語』『甲陽軍鑑』の原文', '『大日本史料』元亀3年12月22日条', '武田信玄の書状（朝倉義景宛など）', '二俣城の開城日（12/19説と11月末説）の根拠', '国立天文台の換算ツールで、1573年1月25日（ユリウス暦）＝2月4日（グレゴリオ暦）の再確認']),
 thumb=dict(bg='assets/mikatagahara/thumb_art.png', lines=[['三方ヶ原の戦い', 112, 'white'], ['犀ヶ崖の夜襲は', 96, 'white'], ['本当にあった？', 112, 'gold']], sub='『信長公記』と後世の逸話を分けて確かめる', shade_col=[10, 14, 28], accent=[238, 96, 84], bar_col=[238, 96, 84], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and not o.get('title') and o['box'][3] - o['box'][1] <= 70: o['size'] = min(o.get('size', 40), 40)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


_fit(spec)
(R / 'data' / 'mikatagahara_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
