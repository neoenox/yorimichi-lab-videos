"""Writes data/shizugatake_spec.json（賤ヶ岳の戦い。戦況解説シリーズ4本目）。台本：docs/themes/20261219_shizugatake/09_script_v2.md
文の番号（at・legs）は章内の0始まりの『行の番号』で書き、下で文の番号に直す。地図の座標は shizugatake_maps.norm()。
位置は、国土地理院住所検索（賤ヶ岳・木之本・柳ヶ瀬・玄蕃尾城・行市山・大垣城・長浜・福井）の座標と、案内をもとにした概略の推定（画面に『推定』と明記）。
軍記による動きは『軍記による描写。実際の経路・順序は確定しない』と明記。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import shizugatake_maps as SM
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]
BOX = [60, 250, 1860, 850]
BLUE = (90, 150, 255); RED = (238, 96, 84); GRN = (110, 214, 140); GOLD = (239, 201, 118); WATER = (130, 195, 255)
CY = json.loads((R / 'data' / 'yamazaki_crops.json').read_text(encoding='utf8'))
CS = json.loads((R / 'data' / 'shizugatake_crops.json').read_text(encoding='utf8'))
SC = json.loads((R / 'data' / 'sekigahara_crops.json').read_text(encoding='utf8'))


def A(lon, lat): return list(SM.norm(lon, lat, 'area'))
def O(lon, lat): return list(SM.norm(lon, lat, 'ogaki'))
def N(lon, lat): return list(SM.norm(lon, lat, 'north'))


# 実在の地点（国土地理院住所検索・Wikipedia）
SHIZU = A(136.1931, 35.5061)       # 賤ヶ岳
YOGO = A(136.1944, 35.5231)        # 余呉湖
KINOMOTO = A(136.2226, 35.5023)    # 木之本
YANAGASE = A(136.1883, 35.5966)    # 柳ヶ瀬
GENBAO = A(136.1766, 35.5984)      # 玄蕃尾城（内中尾山城）
GYOJI = A(136.1692, 35.5681)       # 行市山
# 以下は、案内・伝承をもとにした概略の推定位置（正確な地点ではない）
OIWA = A(136.2105, 35.5300)        # 大岩山砦（余呉湖の東の丘）
IWASAKI = A(136.2090, 35.5170)     # 岩崎山砦（同）
SHIGEYAMA = A(136.2040, 35.5560)   # 茂山（推定）
HIDENAGA_P = A(136.2226, 35.5090)  # 秀長の陣（木之本）
HIDEYOSHI_K = A(136.2226, 35.5023)
WEST_SHORE = A(136.1790, 35.5450)  # 余呉湖の西岸（盛政の道、推定）
OJIRO = A(136.1905, 35.5110)       # 余呉湖の南端〜尾ノ呂（推定）
KAIZU = A(136.0600, 35.4950)       # 海津方面（模式）
NAKA_S = A(136.2119, 35.5458)      # 中之郷（北国街道）
GONGEN = A(136.2010, 35.5600)      # 勝政の隊が動いた方面（推定）

# 広域
OGAKI = O(136.6161, 35.3618); NAGAHAMA = O(136.2616, 35.3787); KINO_O = O(136.2226, 35.5023); GIFU = O(136.7872, 35.4337)
KAIZU_O = O(136.0877, 35.4491)
KITANOSHO = N(136.2217, 36.0613); FUCHU = N(136.1683, 35.9033); KINO_N = N(136.2226, 35.5023); YANAGASE_N = N(136.1883, 35.5966)


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
 dict(key='intro', title='賤ヶ岳の戦い', chapter_title='導入：賤ヶ岳の戦い', opener='賤ヶ岳の戦い', opener_until=2, scene=[
   dict(t='art', name='lake', box=ART_BOX, at=0, dim=0.8, dir=1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.5),
   pn('天正11年4月21日（グレゴリオ暦1583年6月11日。ユリウス暦では6月1日）', 0, 1, 38), pn('琵琶湖の北・余呉湖のまわり：羽柴秀吉の軍 対 柴田勝家の軍', 1, 2, 38),
   pn('山崎の戦いから、10か月後', 2, 3, 42), pn('「秀吉は、大垣から木之本まで、52kmを5時間で戻った」（通説）', 3, 4, 38, col='gold'),
   pn('「前田利家は、戦いの最中に勝家を裏切って退いた」（通説）', 4, 5, 38, col='gold'), pn('「賤ヶ岳の七本槍」の活躍（通説）', 5, 6, 40, col='gold'),
   pn('勝敗を分けたものは何か。同時代の記録は、何を語り、何を語っていないのか', 6, None, 36)]),
 dict(key='split', title='清洲会議のあと', chapter_title='清洲会議のあと', scene=[
   pn('天正10年6/27　清洲会議（尾張・清洲城）', 0, 1, 40), pn('織田信孝を推す柴田勝家 対 三法師を推す羽柴秀吉', 1, 2, 40),
   pn('三法師が後継に（通説）。近年、勝家も三法師自体には賛成で、名代をめぐって対立したとする説も', 2, 3, 34, col='gold'),
   pn('両者は、周りの勢力を味方に。勝家は伊勢の滝川一益、秀吉は美濃の稲葉一鉄・越後の上杉景勝', 3, 4, 34),
   pn('11月　勝家が前田利家らを使者に和睦を持ちかける（雪で動けない冬の時間かせぎ）', 4, 5, 34), pn('12月　秀吉が長浜城を攻め、柴田勝豊が降伏（『柴田退治記』）', 5, 6, 36, col='gold'),
   pn('岐阜城の織田信孝も降伏（『柴田退治記』）', 6, 7, 40, col='gold'), pn('天正11年1月　滝川一益が伊勢で挙兵。秀吉は伊勢へ', 7, 8, 40),
   pn('2月末　雪解けを待った勝家が、北ノ庄を出陣', 8, None, 40),
   amap('north', places=[NOTE_POS(0, '※位置は概略の推定。経路は直線で結んだ模式'),
                         dict(xy=KITANOSHO, label='北ノ庄', kind='castle', at=8, side='r', col=RED, lsize=24),
                         dict(xy=KINO_N, label='木之本', kind='spot', at=0, side='r', col=GOLD, lsize=22),
                         dict(xy=N(136.2616, 35.3787), label='長浜城', kind='castle', at=5, side='r', col=BLUE, lsize=22),
                         dict(xy=N(136.6161, 35.5200), label='岐阜方面', kind='spot', at=6, side='l', col=BLUE, lsize=20)],
        units=[unit(label='柴田勝家', sub='北ノ庄 → 近江へ', col=RED, portrait='p_shibata', pts=[KITANOSHO, YANAGASE_N], legs=[[8, 9]], at=0, head=26, lab_off=(36, -4), lsize=22, dashed=True)])]),
 dict(key='forces', title='両軍の顔ぶれ', chapter_title='両軍の顔ぶれ', scene=[
   pn('兵力：柴田軍 約3万／羽柴軍 約5万といわれる。後世の数字で、実際の人数は分かっていない', 0, 1, 34),
   pn('柴田方：勝家、甥の佐久間盛政、弟の柴田勝政、前田利家', 1, 2, 38), pn('利家は、勝家の家臣ではなく、与力だったと説明される', 2, 3, 38),
   pn('羽柴方：秀吉、弟の羽柴秀長、黒田孝高、中川清秀、高山右近、丹羽長秀', 3, 4, 36), pn('秀吉の近習：のちの七本槍の若い武将たち（加藤清正・福島正則ら）', 4, None, 36),
   amap(places=[NOTE_POS(0, '※位置は概略の推定（軍記・伝承にもとづく）')],
        units=[unit(label='柴田勝家', sub='本陣＝玄蕃尾城', col=RED, portrait='p_shibata', pts=[GENBAO], at=1, head=26, lab_off=(36, -4), lsize=22),
               unit(label='佐久間盛政', sub='浮世絵（想像図）', col=RED, portrait='p_sakuma', pts=[GYOJI], at=1, head=24, lab_off=(36, 10), lsize=22),
               unit(label='前田利家', sub='茂山', col=RED, portrait='p_maeda', pts=[SHIGEYAMA], at=2, head=24, lab_off=(36, -4), lsize=22),
               unit(label='羽柴秀吉', sub='木之本', col=BLUE, portrait='p_hideyoshi', pts=[HIDEYOSHI_K], at=3, head=26, lab_off=(36, 10), lsize=22),
               unit(label='中川清秀', sub='大岩山', col=BLUE, portrait='p_nakagawa', pts=[OIWA], at=3, head=22, lab_off=(36, -20), lsize=22),
               unit(label='高山右近', sub='岩崎山', col=BLUE, portrait='p_takayama', pts=[IWASAKI], at=3, head=22, lab_off=(36, 6), lsize=22)])]),
 dict(key='terrain', title='戦場の地形', chapter_title='戦場の地形', scene=[
   pn('戦場は、琵琶湖の北、余呉湖を囲む山々', 0, 1, 42), pn('北から南へ、北国街道。南の木之本は羽柴軍の本拠', 1, 2, 40),
   pn('柴田方は湖の北：柳ヶ瀬に勝家が着陣、北西の玄蕃尾城に本陣。盛政は行市山', 2, 3, 36, col='gold'),
   pn('羽柴方の砦：湖の東の丘に大岩山・岩崎山、湖の南に賤ヶ岳', 3, 4, 38, col='gold'), pn('今も、これらの砦の遺構が残る', 4, 5, 42),
   pn('画面の地形は現代のもの。陣や砦の位置は概略の推定', 5, None, 40, col='gold'),
   amap(places=[NOTE_POS(0, '※現代の地形。砦・陣の位置は概略の推定'),
                dict(xy=YOGO, label='余呉湖', kind='spot', at=0, side='l', col=WATER, lsize=26),
                dict(xy=SHIZU, label='賤ヶ岳', kind='spot', at=3, side='l', col=BLUE, lsize=24),
                dict(xy=OIWA, label='大岩山（推定）', kind='spot', at=3, side='r', col=BLUE, lsize=22),
                dict(xy=IWASAKI, label='岩崎山（推定）', kind='spot', at=3, side='r', col=BLUE, lsize=22),
                dict(xy=KINOMOTO, label='木之本', kind='camp', at=1, side='r', col=GOLD, lsize=24),
                dict(xy=YANAGASE, label='柳ヶ瀬', kind='camp', at=2, side='r', col=RED, lsize=24),
                dict(xy=GENBAO, label='玄蕃尾城', kind='castle', at=2, side='l', col=RED, lsize=24),
                dict(xy=GYOJI, label='行市山', kind='spot', at=2, side='l', col=RED, lsize=22)],
        lines=[dict(pts=[KINOMOTO, A(136.2200, 35.5250), NAKA_S, YANAGASE], label='北国街道（概略）', at=1, col=GOLD, dash=True, lab=[0.78, 0.50])])]),
 dict(key='standoff', title='対峙', chapter_title='対峙', scene=[
   pn('3/12　勝家が柳ヶ瀬に着陣', 0, 1, 42), pn('3/19　秀吉が木之本に陣を構える', 1, 2, 42), pn('両軍はすぐには戦わず、砦や陣を盛んに築く', 2, 3, 40),
   pn('3/27　秀吉は長浜城へ戻る（伊勢と近江の二方面に備える）', 3, 4, 38), pn('4/16　降伏していた織田信孝が、滝川一益と結んで再び挙兵', 4, 5, 38, col='gold'),
   pn('秀吉は美濃の大垣城へ（『柴田退治記』は4/17、16日とする書物も）', 5, 6, 36, col='gold'), pn('大雨で川が増水し、秀吉は大垣にとどまった（『柴田退治記』）', 6, None, 38),
   amap('ogaki', places=[NOTE_POS(0, '※位置は概略の推定。経路は直線で結んだ模式'),
                         dict(xy=KINO_O, label='木之本', kind='camp', at=1, side='l', col=BLUE, lsize=24),
                         dict(xy=NAGAHAMA, label='長浜城', kind='castle', at=3, side='b', col=BLUE, lsize=24),
                         dict(xy=OGAKI, label='大垣城', kind='castle', at=5, side='l', col=BLUE, lsize=24),
                         dict(xy=GIFU, label='岐阜城', kind='castle', at=4, side='b', col=RED, lsize=22)],
        units=[unit(label='羽柴秀吉', sub='木之本 → 長浜 → 大垣', col=BLUE, portrait='p_hideyoshi', pts=[KINO_O, NAGAHAMA, OGAKI], legs=[[3, 4], [5, 6]], at=1, head=26, lab_off=(36, -30), lsize=22, dashed=True),
               unit(label='織田信孝', sub='4/16　再挙兵', col=RED, portrait='p_nobutaka', pts=[GIFU], at=4, head=22, lab_off=(-34, 34), lsize=22)])]),
 dict(key='oiwa', title='四月二十日　大岩山', chapter_title='4月20日　大岩山', scene=[
   pn('秀吉の軍の多くが近江を離れた。勝家は、好機と見た（軍記）', 0, 1, 38, col='gold'), pn('佐久間盛政が、攻撃を強く進言したとされる（軍記）', 1, 2, 38),
   pn('勝家方に寝返った山路正国が、案内役を務め、羽柴方の陣取りを探った（『柴田退治記』）', 2, 3, 36, col='gold'), pn('4/20　盛政が大岩山の砦を攻める（日付は『柴田退治記』にもある）', 3, 4, 38), pn('中川清秀は、千余騎で砦を出て数時間戦い、討死（『柴田退治記』）', 4, 5, 36, col='gold'),
   pn('羽柴方の防衛線の一角が破られた。盛政は、そのまま大岩山の陣に居続けた（『柴田退治記』）', 5, 6, 36), pn('「勝家の撤退命令に盛政が従わなかった」は、軍記に見える話。事実とみなすには注意が要る', 6, 7, 36, col='gold'),
   pn('高山右近は、岩崎山を退いて木之本の秀長の陣へ、と伝わる（軍記）', 7, 8, 36), pn('同じ日、賤ヶ岳砦を守る桑山重晴も撤退を始めた（軍記）', 8, 9, 38),
   pn('丹羽長秀が船で琵琶湖を渡り海津に上陸、桑山と合流して賤ヶ岳砦を確保（軍記。『柴田退治記』には見えない）', 9, None, 32, col='gold'),
   amap(places=[NOTE_POS(0, '※位置・経路は概略の推定。' + NOTE_GUNKI[1:]), dict(xy=OIWA, label='大岩山', kind='castle', at=3, side='r', col=BLUE, lsize=24),
                dict(xy=IWASAKI, label='岩崎山', kind='castle', at=7, side='r', col=BLUE, lsize=22), dict(xy=SHIZU, label='賤ヶ岳砦', kind='castle', at=8, side='l', col=BLUE, lsize=22)],
        units=[unit(label='佐久間盛政', sub='行市山 → 大岩山', col=RED, portrait='p_sakuma', pts=[GYOJI, WEST_SHORE, OJIRO, OIWA], legs=[[3, 4]], at=1, head=24, lab_off=(-34, -30), lsize=22, dashed=True),
               unit(label='中川清秀', sub='討死', col=BLUE, portrait='p_nakagawa', pts=[OIWA], at=3, head=22, lab_off=(36, -20), lsize=22),
               unit(label='高山右近', col=BLUE, portrait='p_takayama', pts=[IWASAKI, KINOMOTO], legs=[[7, 8]], at=7, head=22, lab_off=(36, 6), lsize=22, dashed=True),
               unit(label='丹羽長秀', sub='船で海津へ（軍記）', col=BLUE, pts=[KAIZU, SHIZU], legs=[[9, 10]], at=9, head=18, lab_off=(-34, 34), lsize=20, dashed=True)])]),
 dict(key='mino', title='美濃大返し', chapter_title='美濃大返し', scene=[
   pn('大垣の秀吉は、知らせを受け「天下の雌雄は、この時」と言った（『柴田退治記』）', 0, 1, 34, col='gold'), pn('軍を引き返す。これが「美濃大返し」', 1, 2, 42),
   pn('『柴田退治記』：申の刻に大垣を出て、戌の刻に木之本に着陣。十三里。二時半で着いたのは古今まれな働き', 2, 3, 32, col='gold'),
   pn('申→戌は約4時間、「二時半」は約5時間。ぴったりは合わない（どれもおよそ）', 3, 4, 36), pn('十三里＝約52km。この数字が、美濃大返しの元になっている', 4, 5, 38),
   pn('同じ記録：馬は死に、歩兵にも息絶えた者が多かった', 5, 6, 40, col='gold'), pn('沿道の村々に飛脚を出し、家1軒につき米1升を木之本へ運ばせた、ともある', 6, 7, 36),
   pn('ただし、秀吉に仕えた大村由己が、その年の11月にまとめた記録。秀吉をたたえる文章であることに注意', 7, 8, 32, col='gold'),
   pn('渡邊大門氏：約1万5千の軍勢が5時間で52kmは物理的に不可能。史実としては認めがたい（説）', 8, 9, 32), pn('ただし渡邊氏も、馬上の小部隊が先に着いた可能性を挙げる。史料の裏付けのない「自分の想像」と断っている', 9, None, 32),
   amap('ogaki', places=[NOTE_POS(0, '※位置は概略の推定。経路は直線で結んだ模式。実際の道筋ではない'),
                         dict(xy=OGAKI, label='大垣城', kind='castle', at=0, side='l', col=BLUE, lsize=24), dict(xy=KINO_O, label='木之本', kind='camp', at=2, side='l', col=BLUE, lsize=24),
                         dict(xy=NAGAHAMA, label='長浜城', kind='castle', at=9, side='b', col=GOLD, lsize=22)],
        lines=[dict(pts=[OGAKI, KINO_O], label='十三里（約52km）', at=4, col=GOLD, dash=True, lab=[0.50, 0.22])],
        units=[unit(label='羽柴秀吉', sub='大垣 → 木之本', col=BLUE, portrait='p_hideyoshi', pts=[OGAKI, KINO_O], legs=[[1, 3]], at=0, head=28, lab_off=(36, -4), lsize=22, dashed=True)])]),
 dict(key='kessen', title='四月二十一日　決戦', chapter_title='4月21日　決戦', scene=[
   pn('夜が明けた4/21。朝から昼過ぎまで、5度、7度と合戦を重ねた（『柴田退治記』）', 0, 1, 36, col='gold'), pn('秀吉が戻ったと知った盛政は、孤立を恐れ、夜のうちに大岩山を離れ始めた（軍記）', 1, 2, 34),
   pn('秀吉は追撃を命じ、盛政は弟の柴田勝政の隊に逃げ込んだ（軍記）', 2, 3, 36), pn('秀吉は賤ヶ岳に本陣を移し、勝政の隊に攻めかかる。勝政は討死といわれる（軍記）', 3, 4, 34),
   pn('秀吉が、近習の若い侍二、三百騎を先頭に、柴田方に切り込んだ（『柴田退治記』）', 4, 5, 34, col='gold'),
   pn('一番槍の近習たちに、感状と3千石〜5千石の領地を与えた（『柴田退治記』）', 5, 6, 36), pn('茂山の前田利家の隊が、戦場を離れ始めた（軍記）', 6, 7, 38, col='gold'), pn('ただし、利家の離脱だけが敗因とは言えない。盛政・勝政の隊は、すでに追撃を受けていた', 7, 8, 34),
   pn('柴田軍に動揺。不破勝光・金森長近の隊も退いたとされる（軍記）', 8, 9, 38), pn('総攻撃。勝家は近習百余騎で北ノ庄へ戻る（『柴田退治記』）', 9, None, 38),
   amap(places=[NOTE_POS(0, '※位置・経路は概略の推定。' + NOTE_GUNKI[1:]), dict(xy=SHIZU, label='賤ヶ岳', kind='castle', at=3, side='l', col=BLUE, lsize=24),
                dict(xy=SHIGEYAMA, label='茂山（推定）', kind='spot', at=6, side='r', col=RED, lsize=22)],
        units=[unit(label='佐久間盛政', sub='大岩山 → 退く（軍記）', col=RED, portrait='p_sakuma', pts=[OIWA, OJIRO, GONGEN], legs=[[1, 2], [2, 3]], at=0, head=24, lab_off=(-34, -30), lsize=22, dashed=True),
               unit(label='羽柴秀吉', sub='賤ヶ岳へ（軍記）', col=BLUE, portrait='p_hideyoshi', pts=[KINOMOTO, SHIZU, OJIRO], legs=[[3, 4], [4, 5]], at=3, head=26, lab_off=(36, 10), lsize=22, dashed=True),
               unit(label='前田利家', sub='戦場を離れる（軍記）', col=RED, portrait='p_maeda', pts=[SHIGEYAMA, YANAGASE], legs=[[6, 7]], at=0, head=24, lab_off=(36, -4), lsize=22, dashed=True),
               unit(label='柴田勝家', sub='北ノ庄へ', col=RED, portrait='p_shibata', pts=[GENBAO, YANAGASE], legs=[[9, 10]], at=0, head=26, lab_off=(-36, -10), lsize=22, dashed=True)])]),
 dict(key='after', title='その後', chapter_title='その後', scene=[
   pn('4/22　秀吉は越前府中へ。4/23　北ノ庄城を囲む（『柴田退治記』）', 0, 1, 38, col='gold'), pn('4/24　勝家は、妻のお市の方とともに自害（グレゴリオ暦6月14日）', 1, 2, 38),
   pn('佐久間盛政は捕らえられ、京の六条河原で処刑（『柴田退治記』）', 2, 3, 38), pn('織田信孝は岐阜城で降伏し、尾張で自害。日付は4/29とも5/2とも', 3, 4, 38),
   pn('滝川一益は約1か月持ちこたえ、開城して出家', 4, 5, 40), pn('秀吉は、大坂で築城を始める。『柴田退治記』も、大坂の様子を誇らしげに記して結ばれる', 5, 6, 34),
   pn('信長の次男・織田信雄は秀吉と協力したが、のちに対立。小牧・長久手の戦いへ', 6, 7, 36), pn('ここまでが、通説に近い流れ。ここから、同時代の記録で確かめる', 7, None, 40, col='gold'),
   amap('north', places=[NOTE_POS(0, '※位置は概略の推定'), dict(xy=KITANOSHO, label='北ノ庄', kind='castle', at=0, side='r', col=RED, lsize=24),
                         dict(xy=FUCHU, label='越前府中', kind='camp', at=0, side='r', col=BLUE, lsize=22), dict(xy=KINO_N, label='木之本', kind='spot', at=0, side='r', col=GOLD, lsize=22)],
        units=[unit(label='羽柴秀吉', sub='4/22 府中 → 4/23 北ノ庄', col=BLUE, portrait='p_hideyoshi', pts=[KINO_N, FUCHU, KITANOSHO], legs=[[0, 1], [1, 2]], at=0, head=26, lab_off=(-36, -10), lsize=22, dashed=True)])]),
 dict(key='source', title='同時代の記録は、何を語るのか', chapter_title='同時代の記録は、何を語るのか', scene=[
   dict(t='art', name='docs', box=ART_BOX, at=0, dim=0.8, dir=-1, note='イメージ（生成画像）。実際の資料の再現ではありません'), dict(t='shade', box=ART_BOX, at=0, alpha=0.66),
   dict(t='cols2', size=30, xm=940, xm2=980, until=3, left=dict(title='『柴田退治記』とは', title_at=0, items=[
        dict(at=0, text='大村由己の編。天正11年11月成立（続群書類従所収）'), dict(at=0, text='秀吉の側が、その年のうちにまとめた記録'), dict(at=0, text='秀吉をたたえる文章であることに注意')]),
        right=dict(title='①美濃大返し', title_at=1, items=[
        dict(at=1, text='数字の元は、ありました（申の刻→戌の刻、十三里、二時半）'), dict(at=2, text='ただし、馬が死に、兵が息絶えた、とも書かれる'),
        dict(at=2, text='この記述だけでは、全軍が同じ時間に着いたかは確かめられない。「五時間」を全軍の正確な記録とみなすのは慎重に（渡邊大門氏）'), dict(at=2, text='渡邊氏は、約1万5千の軍勢が5時間で52kmは不可能、とする（説）')])),
   dict(t='cols2', size=30, xm=940, xm2=980, at=3, until=8, left=dict(title='②前田利家の裏切り', title_at=3, items=[
        dict(at=3, text='『柴田退治記』は、戦場での離脱に触れない。4/22に利家らが越前府中で降参、とだけ記す'), dict(at=4, text='利家は、勝家の家臣ではなく与力だったと説明される（説）')]),
        right=dict(title='見方', title_at=5, items=[
        dict(at=5, text='事前の密約を裏付ける同時代史料は確認されていない、との指摘がある（説）'),
        dict(at=6, text='動機の説明の多くは、『甫庵太閤記』など後世の記述に由来するとの見方も（説）'), dict(at=7, text='殿を務めた横山長隆の討死の伝承。ただし殿軍の有無は内通の有無とは別で、解釈は分かれる（軍記）')])),
   dict(t='cols2', size=30, xm=940, xm2=980, at=8, left=dict(title='③七本槍', title_at=8, items=[
        dict(at=8, text='『柴田退治記』が挙げるのは、七人ではなく九人'), dict(at=9, text='福島正則・脇坂安治・加藤嘉明・加藤清正・平野長泰・片桐且元・糟屋武則・桜井家一・石川一光（石川は討死）'),
        dict(at=10, text='「七本槍」の呼び名は、江戸初期の『甫庵太閤記』が初見とされる（軍記）'), dict(at=11, text='『一柳家記』は、14人の先懸の衆を挙げる（石田三成・大谷吉継も）（軍記）')]),
        right=dict(title='④兵力', title_at=12, items=[
        dict(at=12, text='『柴田退治記』は、柴田方を「五、六万騎」と書く。大きすぎて、そのまま信じられない')]))]),
 dict(key='check', title='分かること、決められないこと', chapter_title='分かること、決められないこと', scene=[
   dict(t='art', name='dusk', box=ART_BOX, at=0, dim=0.8, dir=1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.62),
   dict(t='cols2', size=34, xm=940, xm2=980, until=2, left=dict(title='分かること', title_at=0, items=[
        dict(at=0, text='天正11年4月、羽柴軍が柴田軍に勝った'), dict(at=0, text='勝家は4/24に自害した')]),
        right=dict(title='決められないこと', title_at=1, items=[
        dict(at=1, text='秀吉の軍は、本当に5時間で戻ったのか'), dict(at=1, text='両軍の、実際の兵数'), dict(at=1, text='前田利家が、なぜ退いたのか')])),
   dict(t='cols2', size=34, xm=940, xm2=980, at=2, left=dict(title='その後と日付', title_at=2, items=[dict(at=2, text='この勝利で、秀吉は信長の旧臣の中で優位を固めていった'), dict(at=3, text='大岩山を攻めた日や信孝の自害の日など、書物によって異なるものがある')]),
        right=dict(title='見方', title_at=4, items=[dict(at=4, text='通説・軍記・同時代の記録を、分けて見ると、見え方が変わる')]))]),
]

images = dict(
    area=dict(file='assets/shizugatake/map_area.png'), ogaki=dict(file='assets/shizugatake/map_ogaki.png'), north=dict(file='assets/shizugatake/map_north.png'),
    p_hideyoshi=dict(file='assets/portraits/hideyoshi.jpg', crop=CY['hideyoshi']), p_shibata=dict(file='assets/portraits/shibata.jpg', crop=CS['shibata']),
    p_sakuma=dict(file='assets/portraits/sakuma_m.jpg', crop=CS['sakuma_m']), p_maeda=dict(file='assets/portraits/maeda.jpg', crop=CS['maeda']),
    p_nakagawa=dict(file='assets/portraits/nakagawa.jpg', crop=CY['nakagawa']), p_takayama=dict(file='assets/portraits/takayama.jpg', crop=CY['takayama']),
    p_nobutaka=dict(file='assets/portraits/nobutaka.jpg', crop=CY['nobutaka']),
    lake=dict(file='assets/shizugatake/art_lake.png'), march=dict(file='assets/shizugatake/art_march.png'),
    docs=dict(file='assets/shizugatake/art_docs.png'), dusk=dict(file='assets/shizugatake/art_dusk.png'))


def _line_to_sentence_starts():
    """台本の番号つきの行（1行に複数の文があることがある）→ 各行の最初の文の番号（vp.py の sentences と同じく「。」で区切る）。
    この spec の at / until / legs / title_at は『行の番号（0始まり）』で書き、ここで文の番号に直す。"""
    import re
    t = (R / 'docs' / 'themes' / '20261219_shizugatake' / '09_script_v2.md').read_text(encoding='utf8')
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

spec = dict(slug='shizugatake', theme_dir='20261219_shizugatake', pack='29_shizugatake', header_sub='賤ヶ岳の戦いを、地図の上で、同時代の記録と軍記を分けて確かめる',
 images=images,
 bgm=[['intro', 'forces', 'piano36'], ['terrain', 'kessen', 'piano12'], ['after', 'check', 'piano40']],
 chapters=chapters,
 desc=dict(title_main='賤ヶ岳の戦い「五時間で五十二キロ」「利家の裏切り」「七本槍」を、同時代の記録で確かめる', title_no=1,
  titles=['賤ヶ岳の戦いを地図で解説 美濃大返し・前田利家の裏切り・七本槍は本当？', '賤ヶ岳の戦い 秀吉の美濃大返しは5時間で52km？ 同時代の記録で確かめる', '賤ヶ岳の戦いの流れ 大岩山・美濃大返し・勝家の最期と通説の見直し'],
  intro='天正11年4月21日（グレゴリオ暦1583年6月11日、ユリウス暦6月1日）、琵琶湖の北・余呉湖のまわりで、羽柴秀吉の軍と柴田勝家の軍がぶつかりました。賤ヶ岳の戦いです。この動画では、地図の上で軍勢を動かしながら、戦いの流れを追います。そして、「美濃大返し」「前田利家の裏切り」「賤ヶ岳の七本槍」という有名な話を、同時代の記録『柴田退治記』（大村由己、天正11年11月成立）と、後世の軍記、研究者の見解に分けて確かめます。分かることと決められないことを分けて、最後にまとめます。',
  points=['美濃大返し：「大垣から木之本まで十三里（約52km）を、二時半（五時間ほど）で着いた」という数字の元は、『柴田退治記』にあります（申の刻に大垣を出て、戌の刻に木之本に着陣）。ただし、秀吉に仕えた大村由己が、その年の11月にまとめた、秀吉をたたえる記録です。同じ記録には、馬が死に、歩兵にも息絶えた者が多かったとも書かれます。渡邊大門氏は、約1万5千の軍勢が5時間で52kmを走るのは物理的に不可能で、史実としては認めがたいと述べます(騎馬の小部隊が先行した可能性は、本人が「史料の裏付けのない想像」と断っています)。',
          '前田利家の離脱：『柴田退治記』は、戦場での離脱には触れず、4月22日に利家らが越前府中で降参したと記すだけです。事前の密約を裏付ける同時代史料は確認されていないとの指摘や、動機の説明の多くが『甫庵太閤記』など後世の記述に由来するとの見方があります(解説記事で紹介された岩沢愿彦氏・大西泰正氏の見解。原典は未確認)。',
          '賤ヶ岳の七本槍：『柴田退治記』が挙げる、一番槍の功を認められた近習は九人です。「七本槍」という呼び名は、江戸時代初めの『甫庵太閤記』が初見とされます。',
          '地図上の軍勢の動きは、軍記の描写と推定にもとづく概略の図で、実際の経路・順序ではありません。日付や時刻は、書物によって違います。'],
  refs=['大村由己『柴田退治記』（続群書類従所収。Wikisource）:https://ja.wikisource.org/wiki/柴田退治記', '渡邊大門「豊臣秀吉は驚異的なスピードで美濃大垣から賤ヶ岳へ戻ったのか。美濃大返しの真相」Yahoo!ニュース エキスパート 2021-04-09:https://news.yahoo.co.jp/expert/articles/1506318ae6377aa16b2122cada13bd8322af21d9','渡邊大門「秀吉は52kmを5時間で駆けた？賤ヶ岳「美濃大返し」の真相」Yahoo!ニュース エキスパート:https://news.yahoo.co.jp/expert/articles/23a1b53c4e78b58ddd822549f681841fb8371af2',
        'Wikipedia「賤ヶ岳の戦い」「美濃大返し」「佐久間盛政」「前田利家」(研究者の説と出典の整理)',
        '国立天文台 暦計算室「日本の暦日データベース」', '国土地理院 地理院タイル:https://maps.gsi.go.jp/development/ichiran.html'],
  credit_lines=['・図：自作（国土地理院タイル(陰影起伏図・標準地図)を加工して作成。現代の地形で、当時の川筋・湖岸・道ではありません。陣・砦の位置と経路は、史料・案内をもとにした概略の推定です）',
                '・肖像：羽柴秀吉・柴田勝家・前田利家・中川清秀・高山右近：古い肖像画。佐久間盛政・織田信孝：浮世絵(想像図)。いずれもWikimedia Commonsで公開されているパブリックドメインの画像です。浮世絵は後世の描写で、本人の姿とは限りません。',
                '・イラスト：ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['地図上の軍勢の動きは、軍記の描写と推定にもとづく概略の図で、実際の経路・時刻ではありません。', '『柴田退治記』は、秀吉の側がまとめた記録で、誇張や、秀吉に都合のよい書き方を含む可能性があります。',
         '『柴田退治記』は翻刻(続群書類従、Wikisource)で確認しました。渡邊大門氏の見解は、氏のYahoo!ニュース エキスパートの記事2本で確認しました。『甫庵太閤記』巻六と『賤岳合戦記』(いずれも『史籍集覧』所収、Wikisource)も、翻刻で確認しました。「七本鑓」の呼び名と、七人への感状(天正11年7月1日付、各5000石)の記述があります。「初見」かどうかまでは、確認できていません。『柴田退治記』の盛政の記述(「其儘所居陣也」の前後)は、原文を読み、「引き取れば有利だったところを、そのまま居続けた」という趣旨と受け取れることを確認しました(異本の注記があり、訓読は研究者の校訂を確認していません)。岩沢愿彦氏・大西泰正氏の見解、『福井県史』『加賀藩史料』『一柳家記』などは、解説記事・Wikipediaなど二次資料を通して確認したもので、原典は直接確認していません。'],
  tags='賤ヶ岳の戦い, 羽柴秀吉, 柴田勝家, 美濃大返し, 前田利家, 七本槍, 佐久間盛政, 戦国時代, 戦況解説, 検証, 柴田退治記',
  checks=['『一柳家記』の該当部分の原文を確認する(『甫庵太閤記』巻六の七本鑓の記述は確認済み)', '大西泰正『前田利家・利長』、岩沢愿彦『前田利家』の原典で、密約・動機に関する見解の有無と文言を確認する(渡邊大門氏の記事は確認済み)', '『福井県史』通史編3「賤ケ嶽の戦い」の兵力・日付・柴田勝安(勝政)の名乗りを確認する',
          '大岩山・岩崎山・茂山・権現坂など、砦と陣の位置を、現地案内・測量図で確認する', '盛政の居座りの原文(「其儘所居陣也」前後)の読みを、訓読で確認する']),
 thumb=dict(bg='assets/shizugatake/thumb_art.png', lines=[['賤ヶ岳の戦い', 118, 'white'], ['五時間で', 100, 'white'], ['五十二キロ？', 122, 'gold']], sub='同時代の記録で確かめる', shade_col=[10, 14, 28], accent=[238, 96, 84], bar_col=[238, 96, 84], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and not o.get('title') and o['box'][3] - o['box'][1] <= 70: o['size'] = min(o.get('size', 40), 40)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


_fit(spec)
(R / 'data' / 'shizugatake_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
