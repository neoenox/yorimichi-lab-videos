"""Writes data/yamazaki_spec.json（山崎の戦い。戦況解説シリーズ3本目）。台本：docs/themes/20261212_yamazaki/09_script_v2.md
文の番号（at・legs）は章内の0始まりの『行の番号』で書き、下で文の番号に直す。地図の座標は yamazaki_maps.norm()。
位置は、Wikipedia（宝積寺・山崎城(天王山)・勝竜寺城・淀城・恵解山古墳・坂本城）、国土地理院住所検索（富田・尼崎・姫路・小栗栖・打出浜）の座標と、
史料・案内をもとにした概略の推定（画面に『推定』と明記）。軍記による動きは『軍記による描写。実際の経路・順序は確定しない』と明記。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import yamazaki_maps as YM
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]
BOX = [60, 250, 1860, 850]
BLUE = (90, 150, 255); RED = (238, 96, 84); GRN = (110, 214, 140); GOLD = (239, 201, 118); WATER = (130, 195, 255)
CROPS = json.loads((R / 'data' / 'yamazaki_crops.json').read_text(encoding='utf8'))
SC = json.loads((R / 'data' / 'sekigahara_crops.json').read_text(encoding='utf8'))


def A(lon, lat): return list(YM.norm(lon, lat, 'area'))
def W(lon, lat): return list(YM.norm(lon, lat, 'wide'))
def E(lon, lat): return list(YM.norm(lon, lat, 'east'))
def X(lon, lat): return list(YM.norm(lon, lat, 'approach'))


# 実在の地点（Wikipedia・国土地理院）
TENNO = A(135.6763, 34.9019)      # 山崎城（天王山山頂）
HOSHAKU = A(135.6787, 34.8958)    # 宝積寺
SHORYU = A(135.7007, 34.9181)     # 勝竜寺城
YODO = A(135.7177, 34.9050)       # 淀城
EGE = A(135.6976, 34.9145)        # 恵解山古墳（御坊塚の有力候補地）
# 以下は、史料・案内をもとにした概略の推定位置（正確な地点ではない）
HIGASHI_KURO = A(135.6862, 34.9000)   # 東黒門付近（推定）
W_ENTRY = A(135.640, 34.8905)         # 西から街道を進む摂津の隊の入口（推定）
NAKAGAWA_P = A(135.6835, 34.9042)     # 天王山の山裾（推定）
TAKAYAMA_P = HIGASHI_KURO
IKEDA_P = A(135.6935, 34.8932)        # 淀川沿い（推定）
IKEDA_P2 = A(135.6975, 34.9085)       # 円明寺川を越えた先（推定）
SAITO_P = A(135.6955, 34.9112)        # 明智軍の前面（推定）
ISE_P = A(135.6905, 34.9135)          # 明智軍の右（天王山側）（推定）
KURODA_P = A(135.6800, 34.9075)       # 天王山の山裾（推定）
HIDENAGA_P = A(135.6770, 34.9100)
HORI_P = A(135.6805, 34.8975)         # 後詰（推定）
NIWA_P = A(135.6895, 34.8965)
NOBUTAKA_P = A(135.6885, 34.8950)
AKECHI_YODO = A(135.7040, 34.9030)    # 淀川沿いの明智方（推定）
EAST_EDGE = A(135.7515, 34.9100)



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


def amap(img='area', **k):
    _big(k)
    return dict(t='anim', name='battle_map', img=img, box=MAPBOX, at=0, **k)


NOTE_IMG = 'イメージ（生成画像）。実際の場面の再現ではありません'
NOTE_GUNKI = '※軍記による描写。実際の経路・順序は確定しない'

_MAPCH = {'start', 'tondoubt', 'day12', 'finish', 'terrain', 'after', 'return'}
_MAPCH_ORDER = ['tondoubt', 'return', 'terrain', 'day12', 'start', 'finish', 'after']
DROP = {'return': {1, 2, 3, 6, 8}, 'terrain': {3, 4, 5}, 'day12': {1, 3}, 'start': {9, 10, 4}, 'finish': {2, 3, 4}, 'after': {1, 2, 3, 4}, 'tondoubt': {8, 11, 12, 13}}

chapters = [
 dict(key='intro', title='山崎の戦い', chapter_title='導入：秀吉は、間に合ったのか', scene=[
   bgimg('rain', at=0, dim=.5, blur=4),
   tel('山崎の戦い\n天王山を押さえて\n[[秀吉が勝った]]？', 960, 470, 120, at=0, until=1, rot=-3),
   tel('通説：天王山を先に押さえた秀吉が\n全軍を指揮して勝った', 960, 470, 80, at=1, until=2, plate='blue', rot=2),
   tel('2026年の新説：\n秀吉は開戦に[[間に合わなかった]]？', 960, 470, 100, at=2, until=3, plate='red', rot=-2),
   tel('手がかり：新しく見つかった[[書状]]\nと、[[フロイス]]の記録', 960, 470, 90, at=3, until=4, plate='yellow', rot=1.5),
   tel('地図で追って、確かめる！', 960, 470, 120, at=4, plate='pink', rot=-2)]),
 dict(key='tondoubt', title='秀吉は、間に合ったのか', chapter_title='秀吉は、間に合ったのか', scene=[
   pn('ここまでは、通説に近い流れ。ここから史料を確かめる', 0, 1, 40), pn('通説：秀吉は宝積寺に本陣を置き、全軍を指揮した', 1, 2, 40, col='gold'),
   pn('2026年3月に報じられた説：秀吉は合戦に遅参したのではないか', 2, 3, 38), pn('中京大学・馬部隆弘氏の見方', 3, 4, 42),
   pn('新出書状が直接示すのは、13日の摂津の武将の動きと、14日の進軍予定', 4, 5, 36, col='gold'),
   pn('10/18付の秀吉書状（後に書かれた回顧）：13日午前、約12km後方の富田にいたと読める', 5, 6, 34),
   pn('馬部説：摂津の武将だけで開戦、秀吉は間に合わず。ただし推論に留まる部分あり', 6, 7, 34), pn('フロイスの記録：秀吉・信孝の軍は、疲れて到着できなかった（時刻は他の史料と合わず、解釈が必要）', 7, 8, 32),
   pn('従来は、高山右近を持ち上げる書き方として、重く見られなかった', 8, 9, 38),
   pn('異論：呉座勇一氏　秀吉本人は遅れても、秀長・黒田孝高の部隊は戦場にいた（10/18付書状の持ち場）', 9, 10, 32, col='gold'),
   pn('フロイスは、主に前哨戦を書いたのではないか（呉座氏）', 10, 11, 38), pn('福島克彦氏：書状を合戦の前と後で分けて読む視点は受け継ぐべき', 11, 12, 36),
   pn('池田恒興ら摂津の武将の戦功が、清洲会議にも影響した可能性（福島氏）', 12, 13, 36), pn('馬部氏：後の書状では、書き方が変わっている', 13, None, 38),
   amap('approach', places=[NOTE_POS(0, '※位置は概略の推定。直線距離は約12km'),
                            dict(xy=X(135.5914, 34.8353), label='富田（高槻市）', kind='camp', at=5, side='b', col=BLUE, lsize=24),
                            dict(xy=X(135.6800, 34.8960), label='山崎（大山崎）', kind='spot', at=4, side='t', col=GOLD, lsize=24),
                            dict(xy=X(135.6787, 34.8958), label='宝積寺（通説の本陣）', kind='spot', at=1, side='l', col=(245, 243, 232), lsize=22),
                            dict(xy=X(135.7007, 34.9181), label='勝龍寺城', kind='castle', at=4, side='r', col=RED, lsize=22)],
        lines=[dict(pts=[X(135.5914, 34.8353), X(135.6800, 34.8960)], label='約12km', at=5, col=GOLD, dash=True, lab=[0.34, 0.74])],
        units=[unit(label='摂津の武将', sub='13日に前線（大山崎）', col=BLUE, portrait='p_ikeda', pts=[X(135.6800, 34.8960)], at=4, head=24, lab_off=(30, 28), lsize=22),
               unit(label='羽柴秀吉', sub='13日午前：富田（10/18付書状）', col=BLUE, portrait='p_hideyoshi', pts=[X(135.5914, 34.8353)], at=1, head=28, lab_off=(34, -4), lsize=22),
               unit(label='羽柴秀長', sub='呉座説：部隊は戦場にいた', col=BLUE, pts=[X(135.6730, 34.9030)], at=9, head=18, lab_off=(-34, -30), lsize=20),
               unit(label='黒田孝高', sub='10/18付書状の持ち場', col=BLUE, portrait='p_kuroda', pts=[X(135.6760, 34.8990)], at=9, head=22, lab_off=(-34, 34), lsize=20)])]),
 dict(key='return', title='本能寺のあと', chapter_title='本能寺のあと', scene=[
   pn('6/2　織田信長、本能寺で明智光秀に討たれる', 0, 1, 40), pn('羽柴秀吉は、備中高松城で毛利方と対陣中', 1, 2, 40),
   pn('秀吉が変を知った日：6/3〜6/4（史料で1日の差）', 2, 3, 38, col='gold'), pn('毛利方と和議。6/4　清水宗治が自刃', 3, 4, 40),
   pn('中国大返し：沼城・姫路城を経て、6/11ごろ尼崎へ（姫路着は6/6〜6/8と書物で異なる）', 4, 5, 34, col='gold'),
   pn('6/12　摂津・富田に入る', 5, 6, 42), pn('摂津の中川清秀・高山右近が味方。織田信孝・丹羽長秀も合流', 6, 7, 38),
   pn('羽柴軍は2万を超えたとされる', 7, 8, 42), pn('光秀は、近江と京の地盤固めを優先。細川父子は味方につかなかった', 8, None, 38),
   amap('wide', places=[NOTE_POS(0, '※位置は概略の推定。経路は直線で結んだ模式'),
                        dict(xy=W(133.8235, 34.6907), label='備中高松城', kind='castle', at=1, side='b', col=BLUE),
                        dict(xy=W(134.6938, 34.8379), label='姫路', kind='spot', at=4, side='b', col=GOLD),
                        dict(xy=W(135.4064, 34.7333), label='尼崎', kind='spot', at=4, side='b', col=GOLD),
                        dict(xy=W(135.5914, 34.8353), label='富田', kind='spot', at=5, side='b', col=GOLD),
                        dict(xy=W(135.68, 34.89), label='山崎', kind='camp', at=0, side='t', col=GOLD),
                        dict(xy=W(135.768, 35.012), label='京', kind='castle', at=0, side='t', col=RED)],
        units=[unit(label='羽柴秀吉', sub='備中高松 → 富田', col=BLUE, portrait='p_hideyoshi', pts=[W(133.8235, 34.6907), W(134.6938, 34.8379), W(135.4064, 34.7333), W(135.5914, 34.8353)], legs=[[3, 4], [4, 5], [5, 6]], at=1, head=30, lab_off=(36, -10), dashed=True),
               unit(label='明智光秀', sub='京・近江', col=RED, portrait='p_mitsuhide', pts=[W(135.768, 35.012)], at=8, head=26, lab_off=(-30, 44), lsize=22)])]),
 dict(key='terrain', title='山崎の地形', chapter_title='山崎の地形', scene=[
   pn('山崎は、京都盆地の南西の端', 0, 1, 42), pn('北に天王山、南に淀川。その間は、狭い平地', 1, 2, 42),
   pn('当時は沼地が広がっていたと言われる。大軍が通れる所は限られた', 2, 3, 38), pn('この道が西国街道。山崎は、西国と京を結ぶ要所', 3, 4, 40),
   pn('大山崎は街道沿いの集落。東西に「黒門」と呼ばれる出入口があった', 4, 5, 38), pn('戦場は、円明寺川（現・小泉川）のあたりと説明される', 5, 6, 38, col='gold'),
   pn('画面の地形は現代のもの。陣の位置は推定', 6, None, 40, col='gold'),
   amap(places=[NOTE_POS(0, '※現代の地形。当時の川筋・沼地・道ではありません'),
                dict(xy=TENNO, label='天王山（山崎城跡）', kind='spot', at=1, side='l', col=GOLD, lsize=24),
                dict(xy=SHORYU, label='勝龍寺城', kind='castle', at=5, side='r', col=RED, lsize=24),
                dict(xy=HOSHAKU, label='宝積寺', kind='spot', at=0, side='b', col=(245, 243, 232), lsize=20),
                dict(xy=HIGASHI_KURO, label='東黒門付近（推定）', kind='spot', at=4, side='r', col=GOLD, lsize=22),
                dict(xy=YODO, label='淀城跡', kind='spot', at=0, side='r', col=(245, 243, 232), lsize=20)],
        lines=[dict(pts=[A(135.6330, 34.8800), A(135.6620, 34.8875), A(135.6860, 34.8985), A(135.7050, 34.9100)], label='西国街道（概略）', at=3, col=GOLD, dash=True, lab=[0.28, 0.80]),
               dict(pts=[A(135.6890, 34.9120), A(135.6910, 34.9040), A(135.6930, 34.8960)], label='円明寺川（概略）', at=5, col=WATER, dash=True, lab=[0.50, 0.42])])]),
 dict(key='day12', title='十二日の動き', chapter_title='十二日の動き', scene=[
   pn('6/12　羽柴軍の先発隊が山崎に入る', 0, 1, 42), pn('池田恒興・高山右近・中川清秀ら、摂津の武将', 1, 2, 42),
   pn('高山右近は、大山崎の東の出入口に陣取った（フロイスの記録。伝聞を含む）', 2, 3, 36, col='gold'),
   pn('勝龍寺城の西で、足軽どうしの小競り合いがあったと伝わる', 3, 4, 38), pn('秀吉は、この日、富田に着いている', 4, 5, 42),
   pn('光秀は、勝龍寺城の近くに本陣を置き、迎え撃つ構え', 5, None, 40),
   amap(places=[NOTE_POS(0, '※位置は概略の推定')],
        units=[unit(label='中川清秀', col=BLUE, portrait='p_nakagawa', pts=[W_ENTRY, NAKAGAWA_P], legs=[[0, 1]], at=0, head=22, lab_off=(-30, -36), lsize=22, dashed=True),
               unit(label='池田恒興', col=BLUE, portrait='p_ikeda', pts=[W_ENTRY, IKEDA_P], legs=[[0, 1]], at=0, head=22, lab_off=(-30, 44), lsize=22, dashed=True),
               unit(label='高山右近', sub='東黒門（フロイス）', col=BLUE, portrait='p_takayama', pts=[W_ENTRY, TAKAYAMA_P], legs=[[0, 2]], at=0, head=24, lab_off=(30, 6), lsize=22, dashed=True),
               unit(label='明智光秀', sub='勝龍寺城の近く', col=RED, portrait='p_mitsuhide', pts=[EGE], at=5, head=26, lab_off=(36, -4), lsize=22)],
        marks=[dict(xy=A(135.6960, 34.9140), label='小競り合い', at=3, col=GOLD, lsize=20)])]),
 dict(key='start', title='戦いの始まり', chapter_title='6月13日　戦いの始まり', scene=[
   pn('6/13　雨が降ったとされる', 0, 1, 40), pn('この日の午前、秀吉は、まだ富田にいたと見られる（説）', 1, 2, 38, col='gold'),
   pn('近年見つかった、6/13付の秀吉書状（中京大学が購入）', 2, 3, 38), pn('姫路城の留守居・小寺職隆らに宛て、「明日（14日）、西岡へ出陣して着陣する」', 3, 4, 34),
   pn('西岡：京の西の、このあたりの地域', 4, 5, 40), pn('書状：前日に勝龍寺城へ押し込み、当日は放火。こちらの人数は山崎の狭い所に陣取る', 5, 6, 34),
   pn('申の刻（午後4時ごろ）に戦いが始まったとされる。最初の一撃の時刻は確定しない', 6, 7, 36, col='gold'), pn(NOTE_GUNKI.replace('※', ''), 7, 8, 38, col='gold'),
   pn('明智方が、天王山の山裾の中川清秀の隊などに襲いかかった、と描かれる（書物で違う）', 8, 9, 34),
   pn('苦戦する摂津の隊を、堀秀政らが後ろから支えた、とも言われる', 9, 10, 36), pn('山裾では、黒田孝高・羽柴秀長の隊が前に出た、と描かれる', 10, None, 36),
   amap(places=[NOTE_POS(0, '※位置・経路は概略の推定。' + NOTE_GUNKI[1:]), dict(xy=A(135.6890, 34.9050), label='円明寺川のあたり', kind='spot', at=7, side='t', col=WATER, lsize=20)],
        units=[unit(label='高山右近', col=BLUE, portrait='p_takayama', pts=[TAKAYAMA_P], at=0, head=22, lab_off=(30, 6), lsize=22),
               unit(label='中川清秀', col=BLUE, portrait='p_nakagawa', pts=[NAKAGAWA_P], at=0, head=22, lab_off=(-30, -36), lsize=22),
               unit(label='池田恒興', col=BLUE, portrait='p_ikeda', pts=[IKEDA_P], at=0, head=22, lab_off=(30, 30), lsize=22),
               unit(label='明智方', sub='斎藤・伊勢ら（軍記）', col=RED, portrait='p_saito', pts=[SAITO_P, A(135.6880, 34.9035)], legs=[[8, 9]], at=7, head=24, lab_off=(34, -10), lsize=22, dashed=True),
               unit(label='堀秀政', sub='後詰（軍記）', col=BLUE, portrait='p_hori', pts=[HORI_P, A(135.6840, 34.9010)], legs=[[9, 10]], at=9, head=22, lab_off=(-34, 34), lsize=20, dashed=True),
               unit(label='黒田孝高', sub='山裾（軍記）', col=BLUE, portrait='p_kuroda', pts=[KURODA_P, A(135.6840, 34.9105)], legs=[[10, 11]], at=10, head=22, lab_off=(-34, -30), lsize=20, dashed=True),
               unit(label='羽柴秀長', sub='肖像なし', col=BLUE, pts=[HIDENAGA_P, A(135.6815, 34.9135)], legs=[[10, 11]], at=10, head=18, lab_off=(-34, 12), lsize=20, dashed=True)],
        marks=[dict(xy=[0.03, 0.80], label='← 富田方面（約12km後方）。秀吉はまだ到着していないと見られる（説）', at=1, col=GOLD, lsize=20),
               dict(xy=[0.42, 0.20], label='↑ 西岡：京の西の一帯（この地図の北）', at=4, col=GOLD, lsize=22)])]),
 dict(key='finish', title='決着', chapter_title='決着', scene=[
   pn('戦いが動いたのは、しばらくしてからと描かれる（軍記）', 0, 1, 38, col='gold'), pn('池田恒興らが、淀川沿いに北上し、円明寺川を渡り、明智方の部隊を攻めた（軍記）', 1, 2, 34),
   pn('明智方は混乱', 2, 3, 42), pn('後続の丹羽長秀・織田信孝らの隊も加わった、と軍記は描く', 3, 4, 38),
   pn('苦戦していた摂津の隊も押し返す', 4, 5, 42), pn('明智軍は、総崩れになったとされる', 5, 6, 42, col='gold'),
   pn('光秀は勝龍寺城へ。夜のうちに城を出て、坂本城を目指したと伝わる', 6, None, 38),
   amap(places=[NOTE_POS(0, '※位置・経路は概略の推定。' + NOTE_GUNKI[1:]), dict(xy=SHORYU, label='勝龍寺城', kind='castle', at=0, side='r', col=RED, lsize=24)],
        units=[unit(label='池田恒興ら', sub='淀川沿いから（軍記）', col=BLUE, portrait='p_ikeda', pts=[IKEDA_P, A(135.6960, 34.9020), IKEDA_P2], legs=[[0, 1], [1, 2]], at=0, head=26, lab_off=(-30, 44), lsize=22, dashed=True),
               unit(label='丹羽長秀・織田信孝ら', sub='後続（軍記）', col=BLUE, portrait='p_nobutaka', pts=[NIWA_P, A(135.6930, 34.9040)], legs=[[3, 4]], at=3, head=22, lab_off=(-30, 44), lsize=20, dashed=True),
               unit(label='明智方', sub='淀川沿い', col=RED, pts=[AKECHI_YODO], at=0, head=20, lab_off=(34, 6), lsize=20),
               unit(label='明智光秀', col=RED, portrait='p_mitsuhide', pts=[EGE, SHORYU, A(135.7455, 34.9255)], legs=[[5, 6], [6, 7]], at=0, head=26, lab_off=(36, -4), lsize=22, dashed=True)])]),
 dict(key='after', title='光秀の最期と、その後', chapter_title='光秀の最期と、その後', scene=[
   pn('光秀は、坂本城へ向かう途中、小栗栖で命を落とした。死にざまは、落ち武者狩り・自害など、軍記や伝承で違う', 0, 1, 34),
   pn('光秀の首は、のちに京都でさらされた（日記など）', 1, 2, 40), pn('14日ごろ　堀秀政が打出の浜で明智秀満の軍を破る。秀満は坂本城で自刃と伝わる', 2, 3, 34),
   pn('17日　斎藤利三が近江で捕らえられ、処刑', 3, 4, 40), pn('秀吉は、清洲会議で主導権を握る。信長の跡継ぎは、孫の三法師', 4, 5, 38),
   pn('光秀の天下は「三日天下」と、たとえられる。実際は10日あまり', 5, None, 40, col='gold'),
   amap('east', places=[NOTE_POS(0, '※位置は概略の推定'), dict(xy=E(135.8067, 34.9519), label='小栗栖', kind='spot', at=0, side='r', col=RED, lsize=24),
                       dict(xy=E(135.7007, 34.9181), label='勝龍寺城', kind='castle', at=0, side='l', col=RED, lsize=22),
                       dict(xy=E(135.8774, 35.0049), label='打出の浜', kind='camp', at=2, side='l', col=BLUE, lsize=22),
                       dict(xy=E(135.8772, 35.0598), label='坂本城', kind='castle', at=2, side='l', col=RED, lsize=22),
                       dict(xy=E(135.768, 35.012), label='京', kind='spot', at=2, side='l', col=GOLD, lsize=22)],
        units=[unit(label='明智光秀', col=RED, portrait='p_mitsuhide', pts=[E(135.7007, 34.9181), E(135.8067, 34.9519)], legs=[[0, 1]], at=0, head=26, lab_off=(36, -4), lsize=22, dashed=True),
               unit(label='堀秀政', col=BLUE, portrait='p_hori', pts=[E(135.768, 35.012), E(135.8774, 35.0049)], legs=[[2, 3]], at=2, head=22, lab_off=(-30, 44), lsize=20, dashed=True)])]),
 dict(key='tennozan', title='天王山と、成句', chapter_title='天王山と、成句', scene=[
   bgimg('docs', at=0, dim=.55, blur=6),
   tel('[[天王山]]の争奪戦で\n勝敗が決まった？', 960, 470, 120, at=0, until=1, rot=-2),
   rows([dict(at=1, tag='軍記', text='『太閤記』など江戸時代の軍記に見られる', col='orange', until=4),
         dict(at=2, tag='同時代', text='良質な史料では、争奪戦は確かめられない', col='red', until=4),
         dict(at=3, tag='注意', text='部隊がいたことと、勝敗を決めたことは別の話', col='purple', until=4)], x0=110, x1=1810, y0=250, size=54, gap=36),
   tel('「天王山」＝勝敗の分かれ目（成句）', 960, 400, 80, at=4, until=5, plate='yellow', rot=-1.5),
   rows([dict(at=5, tag='洞ヶ峠', text='筒井順慶が日和見をした逸話も、確かめられない', col='red')], x0=110, x1=1810, y0=560, size=54, gap=30)]),
 dict(key='check', title='分かること、決められないこと', chapter_title='分かること、決められないこと', scene=[
   bgimg('dusk', at=0, dim=.55, blur=6),
   rows([dict(at=0, tag='分かる', text='6/13、山崎で羽柴軍と明智軍が戦い、羽柴軍が勝った。光秀はそのあと命を落とした', col='green'),
         dict(at=1, tag='不明', text='秀吉がいつ戦場に着いたのか', col='red'),
         dict(at=1, tag='不明', text='天王山の争奪戦が、勝敗を決めたのか', col='red'),
         dict(at=1, tag='不明', text='両軍の実際の兵数', col='red'),
         dict(at=2, tag='今', text='新しい書状をきっかけに、通説の見直しが進む。研究者の間でも見方は分かれる', col='blue')], x0=110, x1=1810, y0=170, size=50, gap=26),
   tel('通説・軍記・同時代の書状。\n分けて見ると、[[見え方が変わる]]', 960, 850, 56, at=3, plate='yellow', rot=-1.2)]),
]

images = dict(
    area=dict(file='assets/yamazaki/map_area.png'), core=dict(file='assets/yamazaki/map_core.png'), wide=dict(file='assets/yamazaki/map_wide.png'),
    east=dict(file='assets/yamazaki/map_east.png'), approach=dict(file='assets/yamazaki/map_approach.png'),
    p_hideyoshi=dict(file='assets/portraits/hideyoshi.jpg', crop=CROPS['hideyoshi']), p_mitsuhide=dict(file='assets/portraits/mitsuhide.jpg', crop=CROPS['mitsuhide']),
    p_kuroda=dict(file='assets/portraits/kuroda_y.jpg', crop=CROPS['kuroda_y']), p_ikeda=dict(file='assets/portraits/ikeda.jpg', crop=CROPS['ikeda']),
    p_takayama=dict(file='assets/portraits/takayama.jpg', crop=CROPS['takayama']), p_nakagawa=dict(file='assets/portraits/nakagawa.jpg', crop=CROPS['nakagawa']),
    p_nobutaka=dict(file='assets/portraits/nobutaka.jpg', crop=CROPS['nobutaka']), p_niwa=dict(file='assets/portraits/niwa.jpg', crop=CROPS['niwa']),
    p_hori=dict(file='assets/portraits/hori.jpg', crop=CROPS['hori']), p_saito=dict(file='assets/portraits/saito_t.jpg', crop=CROPS['saito_t']),
    rain=dict(file='assets/yamazaki/art_rain.png'), march=dict(file='assets/yamazaki/art_march.png'),
    docs=dict(file='assets/yamazaki/art_docs.png'), dusk=dict(file='assets/yamazaki/art_dusk.png'))


def _line_to_sentence_starts():
    """台本の番号つきの行（1行に複数の文があることがある）→ 各行の最初の文の番号（vp.py の sentences と同じく「。」で区切る）。
    この spec の at / until / legs / title_at は『行の番号（0始まり）』で書き、ここで文の番号に直す。"""
    import re
    t = (R / 'docs' / 'themes' / '20261212_yamazaki' / '09_script_v2.md').read_text(encoding='utf8')
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
        _ART = ['rain', 'march', 'docs', 'dusk']
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

spec = dict(slug='yamazaki', theme_dir='20261212_yamazaki', pack='28_yamazaki', header_sub='山崎の戦いを、地図の上で、書状と軍記を分けて確かめる',
 images=images,
 bgm=[['intro', 'tondoubt', 'piano36'], ['return', 'finish', 'piano12'], ['after', 'check', 'piano40']],
 style='pop',
 chapters=chapters,
 desc=dict(title_main='山崎の戦いは、「天王山」と秀吉の指揮で決まったのか', title_no=2,
  titles=['山崎の戦いを地図で解説 秀吉は間に合った？ 天王山は本当？ 書状で確かめる', '山崎の戦い 秀吉は遅参した？ 2026年の新説と異論を比べる', '山崎の戦いの流れ 摂津衆の前線・光秀の最期・天王山と洞ヶ峠の真相'],
  intro='天正10年6月13日（ユリウス暦1582年7月2日、グレゴリオ暦7月12日）、京都の南・山崎で、羽柴秀吉の軍と明智光秀の軍がぶつかりました。山崎の戦いです。この動画では、地図の上で軍勢を動かしながら、戦いの流れを追います。そして、2026年3月に報じられた新出の秀吉書状と、馬部隆弘氏の「秀吉遅参説」、呉座勇一氏・福島克彦氏の見解、天王山・宝積寺・洞ヶ峠にまつわる通説を、史料の種類（同時代の書状・日記、後世の軍記）を分けて確かめます。分かることと決められないことを分けて、最後にまとめます。',
  points=['新しく見つかった6月13日付の秀吉書状(小寺職隆・生駒七郎右衛門尉宛)は、前日に勝龍寺城へ押し込み当日は放火したこと、味方が山崎の狭い所に陣取っていること、翌14日に西岡へ着陣する予定を伝えます(馬部氏の論文に載る翻刻と、福島克彦氏の紹介による)。馬部隆弘氏は、これと10月18日付の秀吉書状(『金井文書』)などから、秀吉は13日の午前に約12km後方の富田にいて、開戦に間に合わなかったと考えます(2026年3月報道。論文は『戦国史研究』91号・『中京大学文学部紀要』60-2)。',
          '異論もあります。呉座勇一氏は、秀吉本人は遅れたかもしれないが、10月18日付書状に持ち場が書かれた羽柴秀長・黒田孝高らの部隊は戦場にいたと考えます。福島克彦氏は、馬部氏の見方に異論はあるとしつつ、合戦前後の書状を分けて読む視点は受け継ぐべきだと述べます。研究者の間でも見方は分かれています。',
          '「天王山の争奪戦が勝敗を決めた」という話は、『太閤記』『川角太閤記』など江戸時代の軍記に見えるもので、同時代の良質な史料では確かめられないとされてきました。近年は『乙夜之書物』などから見直す動きもありますが、山のあたりに部隊がいたことと、争奪戦が勝敗を決めたことは別の話です。宝積寺に秀吉が本陣を置いたという記述も、同時代の史料には見当たらないとされます。',
          '開戦は、申の刻(午後4時ごろ)とされますが、最初の一撃の時刻は確定していません(根拠史料の原文は未確認)。その後の部隊の動きは、後世の軍記による描写で、書物によって違います。地図上の動きは、史料と研究をもとにした概略の図で、実際の経路・順序ではありません。'],
  refs=['福島克彦「［特別寄稿］山崎合戦像の行方」web中公新書 2026-05-25:https://www.chuko.co.jp/shinsho/portal/128511.html', '呉座勇一「秀吉は山崎の戦いに『遅参』していたか」アゴラ 2026-08-01:https://agora-web.jp/archives/260731064914.html',
        'Wikipedia「山崎の戦い」「中国大返し」「清洲会議」「洞ヶ峠」(研究者の説と出典の整理)', '国土地理院 地理院タイル:https://maps.gsi.go.jp/development/ichiran.html'],
  credit_lines=['・図：自作（国土地理院タイル(陰影起伏図・標準地図)を加工して作成。現代の地形で、当時の川筋・沼地・道ではありません。陣の位置と経路は、史料・研究者の説をもとにした概略の推定です）',
                '・肖像：羽柴秀吉・明智光秀・黒田孝高(如水)・池田恒興・中川清秀・堀秀政：古い肖像画。高山右近・織田信孝・斎藤利三：歌川芳幾・歌川国芳の浮世絵(想像図)。いずれもWikimedia Commonsで公開されているパブリックドメインの画像です。浮世絵は後世の描写で、本人の姿とは限りません。',
                '・イラスト：ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['地図上の軍勢の動きは、史料と研究をもとにした概略の図で、実際の経路・時刻ではありません。', '開戦の時刻、部隊の動き、秀吉の到着の時期は、史料と研究者で異なります。この動画は、一つの説を選ばず、並べています。',
         '馬部氏の説は、論文『山崎の合戦と池田恒興』(中京大学学術情報リポジトリで公開)の本文と、福島氏・呉座氏の論考で確認しました。『兼見卿記』6月12日条・13日条(正本・別本)は、翻刻を載せる資料で確認しました(13日条は「雨降、申刻に山崎表で鉄砲の音が数刻止まず、一戦に及んだか」という趣旨です)。ただし、『金井文書』・フロイスの書翰の原文、別稿『山崎の合戦に遅参した羽柴秀吉』は、投稿者は直接確認していません。10月18日付の秀吉書状には、ほかに滋賀県立安土城考古博物館蔵・宮内庁書陵部蔵の写しが伝わりますが、本文は確認できていません。'],
  tags='山崎の戦い, 羽柴秀吉, 明智光秀, 天王山, 中国大返し, 馬部隆弘, 戦国時代, 戦況解説, 検証, 本能寺の変, 洞ヶ峠',
  checks=['『兼見卿記』の正本・別本の原本(史料纂集)で、翻刻の誤りがないか確認する(6/12・6/13条の翻刻は確認済み)', '馬部隆弘「山崎の合戦に遅参した羽柴秀吉」(『戦国史研究』91号)本体を確認する(「山崎の合戦と池田恒興」は確認済み)',
          '秀吉書状(6/13付・10/18付『金井文書』)とフロイス『日本史』の該当箇所の原文を確認する', '御坊塚の比定地(恵解山古墳説・境野一号墳説)と、宝積寺本陣説の出所(『雍州府志』『京華要誌』)を確認する', '光秀の最期・首・打出の浜の日付を、日記類で確認する']),
 thumb=dict(bg='assets/yamazaki/thumb_art.png', lines=[['山崎の戦い', 118, 'white'], ['秀吉は', 100, 'white'], ['遅参？', 130, 'gold']], sub='新説と異論を並べて確かめる', shade_col=[10, 14, 28], accent=[238, 96, 84], bar_col=[238, 96, 84], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and not o.get('title') and o['box'][3] - o['box'][1] <= 70: o['size'] = min(o.get('size', 40), 40)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


_fit(spec)
(R / 'data' / 'yamazaki_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
