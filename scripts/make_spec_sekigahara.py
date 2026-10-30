"""Writes data/sekigahara_spec.json（関ヶ原の戦い。戦況解説シリーズ2本目）。台本：docs/themes/20261205_sekigahara/09_script_v2.md（最終版＝v3）
文の番号（at・legs）は章内の0始まりの文番号（`python scripts/vp.py sekigahara sents` の番号）。地図の座標は sekigahara_maps.norm()。
位置は、OpenStreetMap（開戦地・決戦地・島津陣・福島陣跡・笹尾山・桃配山・小早川陣跡）、Wikipedia（松尾山城・南宮山）の座標と、史料・案内をもとにした概略の推定（画面に「推定」と明記）。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import sekigahara_maps as SM
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]
BOX = [60, 250, 1860, 850]
BLUE = (90, 150, 255); RED = (238, 96, 84); GRN = (110, 214, 140); GOLD = (239, 201, 118); WATER = (130, 195, 255)
CROPS = json.loads((R / 'data' / 'sekigahara_crops.json').read_text(encoding='utf8'))


def A(lon, lat): return list(SM.norm(lon, lat, 'area'))
def Wd(lon, lat): return list(SM.norm(lon, lat, 'wide'))
def K(lon, lat): return list(SM.norm(lon, lat, 'core'))


# 実在の地点（OSM・Wikipedia座標）
SASAO = A(136.458666, 35.371807)         # 笹尾山（石田三成の陣と伝わる）
KAISEN = A(136.45839, 35.365541)         # 「開戦地」の碑
KESSEN = A(136.4616, 35.37048)           # 「決戦地」の碑
SHIMAZU_P = A(136.45925, 35.36707)       # 島津義弘陣跡
FUKUSHIMA_P = A(136.46033, 35.35966)     # 福島正則陣跡
MATSUO = A(136.45425, 35.34739)          # 松尾山城
MOMO = A(136.48788, 35.36543)            # 桃配山（家康の最初の陣）
NANGU = A(136.5098, 35.3468)             # 南宮山
# 以下は、史料・案内をもとにした概略の推定位置（正確な地点ではない）
UKITA_P = A(136.4548, 35.3638); KONISHI_P = A(136.4562, 35.3685); OTANI_P = A(136.4440, 35.3622)
IEYASU_L = A(136.4668, 35.3662)           # 家康の最後の陣（推定）
KIKKAWA_P = A(136.5036, 35.3530); CHOSO_P = A(136.5290, 35.3525)

# 戦場の拡大図（core）用の座標
SASAO_K = K(136.458666, 35.371807); KAISEN_K = K(136.45839, 35.365541); FUKUSHIMA_K = K(136.46033, 35.35966); MATSUO_K = K(136.45425, 35.34739)
UKITA_K = K(136.4548, 35.3638); KONISHI_K = K(136.4562, 35.3685); OTANI_K = K(136.4440, 35.3622)
EAST_EDGE = [0.995, 0.16]; EAST_EDGE2 = [0.995, 0.34]


def pn(text, at, until=None, size=40, hi=True, col=None):
    d = dict(t='panel', box=TOP, text=text, at=at, size=size, hi=hi)
    if until is not None: d['until'] = until
    if col: d['col'] = col
    return d


def unit(**k): return k
def NOTE_POS(at=0, txt='※位置は概略の推定（通説的な配置）'): return dict(xy=[0.02, 0.95], label=txt, kind='spot', at=at, side='r', col=GOLD, lsize=28)


def NOTE_TOP(at=0, txt=''): return dict(xy=[0.02, 0.04], label=txt, kind='spot', at=at, side='r', col=GOLD, lsize=26)


def amap(img='area', **k):
    return dict(t='anim', name='battle_map', img=img, box=BOX, at=0, **k)


NOTE_IMG = 'イメージ（生成画像）。実際の場面の再現ではありません'
ART_BOX = [60, 170, 1860, 850]

chapters = [
 dict(key='intro', title='関ヶ原の戦い', chapter_title='導入：関ヶ原の戦い', opener='関ヶ原の戦い', opener_until=2, scene=[
   dict(t='art', name='fog', box=ART_BOX, at=0, dim=0.8, dir=1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.5),
   pn('慶長5年9月15日（1600年10月21日）', 0, 1, 44), pn('美濃・関ヶ原：徳川家康の東軍 対 石田三成らの西軍', 1, 2, 40),
   pn('「小早川秀秋は、家康の鉄砲に脅されて寝返った」？', 2, 3, 42, col='gold'), pn('戦いは、朝に始まり、短時間で決まったと言われる', 3, 4, 40),
   pn('始まった時刻も、寝返りの時刻も、史料によって違う', 4, 5, 40, col='gold'), pn('地図の上で動きを追い、史料ごとの違いを確かめる', 5, None, 40)]),
 dict(key='before', title='戦いの前', chapter_title='戦いの前', scene=[
   pn('慶長3年（1598）豊臣秀吉が亡くなる。跡継ぎの秀頼は幼い', 0, 1, 38), pn('慶長5年　家康、上杉景勝を討つため会津へ', 1, 2, 42),
   pn('7/17　豊臣政権の三奉行が、家康の行いを非難する書状を諸大名に送る', 2, 3, 36, col='gold'), pn('西軍の中心：毛利輝元（大坂城に残る）', 3, 4, 42),
   pn('家康は軍を西へ戻し、東軍は美濃へ。西軍の拠点は大垣城', 4, None, 40),
   amap('wide', places=[dict(xy=Wd(136.6161, 35.362), label='大垣城', kind='castle', at=4, side='b', col=RED),
                        dict(xy=Wd(136.465, 35.3685), label='関ヶ原', kind='spot', at=0, side='t', col=GOLD),
                        dict(xy=Wd(136.5806, 35.3938), label='赤坂', kind='camp', at=4, side='t', col=BLUE),
                        dict(xy=Wd(136.2743, 35.2805), label='佐和山城', kind='castle', at=0, side='b', col=RED)])]),
 dict(key='forces', title='両軍の兵力と布陣', chapter_title='両軍の兵力と布陣', scene=[
   pn('兵力は、史料でも研究でも、数字が定まらない', 0, 1, 42), pn('東軍：7万〜10万ほど／西軍：8万前後（推計）', 1, 2, 42, col='gold'),
   pn('明治の『日本戦史 関原役』：石高100石につき3人で算出。実数は不明と断る', 2, 3, 36),
   pn('9/14　家康、赤坂に着く。石田三成・宇喜多秀家らも、この夜、大垣城を出て関ヶ原へ（連署状）', 3, 4, 34),
   pn('これから示す布陣は、明治の『日本戦史』の図にもとづく、通説的な配置', 4, 5, 38, col='gold'), pn('西軍：笹尾山の石田、小西、宇喜多、大谷、島津', 5, 6, 40),
   pn('南：松尾山の小早川秀秋、南宮山の毛利秀元・吉川広家ら', 6, 7, 40), pn('同時代の史料から、別の配置を考える研究もある', 7, None, 42, col='gold'),
   amap(places=[NOTE_POS(0, '※位置は概略の推定（通説的な配置。別の配置を考える研究もある）')],
        units=[unit(label='徳川家康', sub='東軍（桃配山）', col=BLUE, portrait='p_ieyasu', pts=[EAST_EDGE, MOMO], legs=[[3, 4]], at=3, head=28, lab_off=(36, -6)),
               unit(label='石田三成', sub='笹尾山', col=RED, portrait='p_ishida', pts=[EAST_EDGE2, [0.62, 0.20], SASAO], legs=[[3, 4], [4, 5]], at=3, head=28, lab_off=(36, -10), dashed=True),
               unit(label='小西行長', sub='浮世絵（想像図）', col=RED, portrait='p_konishi', pts=[KONISHI_P], at=5, head=22, lab_off=(-28, -36), lsize=22),
               unit(label='宇喜多秀家', col=RED, portrait='p_ukita', pts=[UKITA_P], at=5, head=22, lab_off=(-30, 42), lsize=22),
               unit(label='大谷吉継', sub='浮世絵（想像図）', col=RED, portrait='p_otani', pts=[OTANI_P], at=5, head=22, lab_off=(-20, 44), lsize=22),
               unit(label='島津義弘', col=RED, portrait='p_shimazu', pts=[SHIMAZU_P], at=5, head=22, lab_off=(30, 6), lsize=22),
               unit(label='小早川秀秋', sub='松尾山', col=RED, portrait='p_kobaya', pts=[MATSUO], at=6, head=24, lab_off=(32, 4), lsize=22),
               unit(label='毛利秀元・吉川広家ら', sub='南宮山', col=RED, portrait='p_mori', pts=[NANGU], at=6, head=24, lab_off=(30, 6), lsize=22)])]),
 dict(key='mouri', title='南宮山の毛利', chapter_title='南宮山の毛利', scene=[
   pn('西軍の有力な軍勢の一つ：毛利の一族', 0, 1, 40), pn('南宮山：毛利秀元・吉川広家ら。毛利関係の兵は、およそ1万6千とする記録', 1, 2, 36),
   pn('吉川広家は、東軍と通じていた', 2, 3, 42, col='gold'), pn('9/14　本多忠勝・井伊直政の起請文：忠節を尽くせば、毛利家を粗略にせず、領地も現状のまま', 3, 4, 34),
   pn('南宮山の毛利勢は、主戦場の戦いに加わらなかった', 4, None, 40, col='gold'),
   amap(places=[NOTE_POS()],
        units=[unit(label='毛利秀元', sub='約1万6千（毛利関係の記録）', col=RED, portrait='p_mori', pts=[NANGU], at=0, head=26, lab_off=(30, -10)),
               unit(label='吉川広家', sub='山麓（位置は推定）', col=RED, portrait='p_kikkawa', pts=[KIKKAWA_P], at=2, head=24, lab_off=(30, 14), lsize=22),
               unit(label='長宗我部盛親ら', sub='位置は推定', col=RED, pts=[CHOSO_P], at=1, head=20, lab_off=(30, -34), lsize=20)],
        lines=[dict(pts=[NANGU, A(136.4845, 35.3560), SASAO], label='戦場へは出ない', at=4, col=GOLD, dash=True, lab=[0.50, 0.55])])]),
 dict(key='start', title='戦いの始まり', chapter_title='戦いの始まり', scene=[
   pn('9/15　朝。戦場には、霧が立ちこめていたと、後世の記録は伝える', 0, 1, 38), pn('開戦の時刻は確定していない。9/17の連署書状：巳の刻（午前10時ごろ）', 1, 2, 38, col='gold'),
   pn('白峰旬：開戦は午前10時ごろ／笠谷和比古：午前8時ごろ。10時は霧が晴れて本格化', 2, 3, 34),
   pn('『黒田家譜』（後世）：井伊直政が松平忠吉を連れ、物見と称して福島隊より先へ', 3, 4, 36), pn('先陣を誰が務めたかは、史料の記述も解釈も分かれる', 4, None, 40, col='gold'),
   amap('core', places=[NOTE_TOP(0, '※位置・経路は概略の推定。実際の時刻・順序は確定しない'), dict(xy=KAISEN_K, label='開戦地（碑）', kind='spot', at=1, side='t', col=GOLD, lsize=22)],
        units=[unit(label='福島正則', col=BLUE, portrait='p_fukushima', pts=[FUKUSHIMA_K], at=3, head=24, lab_off=(32, 4), lsize=22),
               unit(label='宇喜多秀家', col=RED, portrait='p_ukita', pts=[UKITA_K], at=3, head=22, lab_off=(-30, 42), lsize=22),
               unit(label='井伊直政', sub='松平忠吉とともに（『黒田家譜』）', col=BLUE, portrait='p_ii', pts=[K(136.4690, 35.3580), FUKUSHIMA_K, UKITA_K], legs=[[3, 4], [4, 5]], at=3, head=26, lab_off=(34, -4), lsize=22, dashed=True)])]),
 dict(key='west', title='西軍の戦い', chapter_title='西軍の戦い', scene=[
   pn('西軍の中心：笹尾山の石田三成', 0, 1, 42), pn('石田隊には島左近ら。黒田長政・細川忠興の隊と戦う', 1, 2, 38),
   pn('福島正則の隊は、宇喜多秀家の隊（後世の推計で約1万7千）と戦う', 2, 3, 38), pn('北天満山の小西行長陣：のろしを上げた、という伝承', 3, 4, 38),
   pn('一進一退。ただし、実際の推移をどこまで再現できるかは、慎重に', 4, None, 38, col='gold'),
   amap('core', places=[NOTE_TOP(0, '※位置・経路は概略の推定')],
        units=[unit(label='石田三成', col=RED, portrait='p_ishida', pts=[SASAO_K], at=0, head=28, lab_off=(34, -4)),
               unit(label='黒田長政・細川忠興', col=BLUE, pts=[K(136.4760, 35.3690), K(136.4680, 35.3712)], legs=[[1, 2]], at=1, head=22, lab_off=(30, -26), lsize=22),
               unit(label='福島正則', col=BLUE, portrait='p_fukushima', pts=[FUKUSHIMA_K, K(136.4605, 35.3655)], legs=[[2, 3]], at=2, head=24, lab_off=(34, 16), lsize=22),
               unit(label='宇喜多秀家', sub='約1万7千（推計）', col=RED, portrait='p_ukita', pts=[UKITA_K], at=2, head=24, lab_off=(-60, -64), lsize=22)],
        marks=[dict(xy=KONISHI_K, label='小西行長陣：のろし（伝承）', at=3, col=GOLD, lsize=20)])]),
 dict(key='kobayakawa', title='小早川秀秋の寝返り', chapter_title='小早川秀秋の寝返り', scene=[
   pn('松尾山：小早川秀秋（伝統的な布陣図で約1万5千）', 0, 1, 40), pn('働きかけは、戦いの前から。黒田長政が重臣・平岡頼勝に接触したと伝わる', 1, 2, 36),
   pn('通説：家康が松尾山へ鉄砲を撃たせ、迷う秀秋を動かした（問鉄砲）', 2, 3, 38, col='gold'),
   pn('戦いの60年以上あとの『慶長軍記』など、江戸時代の軍記に見える。同時代の史料では確かめられていない', 3, 4, 34),
   pn('藤本正行・白峰旬：後世の創作／笠谷和比古：射撃はあった（誤射の釈明、『備前老人物語』）', 4, 6, 34, col='gold'),
   pn('寝返りの時刻：白峰＝開戦の直後（連署書状・吉川広家書状「即時に」）', 6, 7, 36),
   pn('笠谷＝昼ごろ。「即時に」は決まり文句で、島津義弘の自伝は数刻の戦いと記す', 7, 8, 36, col='gold'),
   pn('9/17の書状：小早川・脇坂安治・小川祐忠父子が裏切り（一次）。朽木・赤座は軍記', 8, 9, 34),
   pn('大谷吉継は戦死。平塚為広・戸田勝成も戦死と伝わる', 9, None, 38),
   amap('core', places=[NOTE_TOP(0, '※位置・経路は概略の推定。動き出した時刻は確定しない')],
        units=[unit(label='小早川秀秋', sub='松尾山', col=RED, portrait='p_kobaya', pts=[MATSUO_K, OTANI_K], legs=[[8, 9]], at=0, head=30, lab_off=(32, 6)),
               unit(label='大谷吉継', sub='浮世絵（想像図）', col=RED, portrait='p_otani', pts=[OTANI_K], at=0, head=26, lab_off=(-20, 44), lsize=22),
               unit(label='脇坂安治・小川祐忠ら', sub='位置は推定', col=BLUE, pts=[K(136.4472, 35.3562), K(136.4452, 35.3600)], legs=[[8, 9]], at=8, head=20, lab_off=(30, 6), lsize=20, dashed=True)],
        marks=[dict(xy=OTANI_K, label='大谷吉継 戦死', at=9, col=RED, lsize=22)])]),
 dict(key='collapse', title='崩れる西軍', chapter_title='崩れる西軍', scene=[
   pn('小早川らの攻撃が、西軍の崩壊を早めたと考えられている', 0, 1, 38), pn('宇喜多・小西の隊も敗走。各隊が崩れた順序には、不明な点がある', 1, 2, 38),
   pn('9/15付の家康書状（伊達政宗宛）：午の刻（正午ごろ）の記述。終わった時刻とは断定できない', 2, 3, 34, col='gold'),
   pn('『関ヶ原軍記大成』（1713年序）：午後2時ごろ（未の刻）', 3, 4, 38), pn('南宮山の毛利・長宗我部・長束・安国寺らは、戦わず、東軍の勝利のあとに退いた', 4, None, 36),
   amap(places=[NOTE_POS(0, '※方向は概略。各隊が崩れた順序は確定しない')],
        lines=[dict(pts=[UKITA_P, A(136.4400, 35.3790)], label='', at=1, col=RED, dash=True), dict(pts=[SASAO, A(136.4570, 35.3955)], label='敗走（方向は概略）', at=1, col=RED, dash=True, lab=[0.30, 0.04])],
        units=[unit(label='東軍', col=BLUE, portrait='p_ieyasu', pts=[MOMO, IEYASU_L], legs=[[2, 3]], at=0, head=26, lab_off=(36, -6)),
               unit(label='毛利ら', sub='戦わず', col=RED, portrait='p_mori', pts=[NANGU], at=4, head=24, lab_off=(30, 6), lsize=22)])]),
 dict(key='shimazu', title='島津義弘の退却', chapter_title='島津義弘の退却', scene=[
   pn('島津義弘：千数百人ほど（推定）', 0, 1, 42), pn('西軍が崩れると、島津隊は敵に囲まれた', 1, 2, 42),
   pn('味方の退く向きとは違う、敵軍の正面を突破する道を選んだ（軍記）', 2, 3, 38, col='gold'), pn('大きな犠牲。最後まで従ったのは、数十人という伝承', 3, 4, 38),
   pn('追った井伊直政は、銃撃で負傷したとされる', 4, 5, 40),
   pn('前夜の夜襲案：『落穂集』（1727）などの逸話。桐野作人氏らは史実に疑問', 5, None, 36, col='gold'),
   amap(places=[NOTE_POS(0, '※経路は概略の推定。戦場から南東へ抜けたと伝わる')],
        units=[unit(label='島津義弘', sub='千数百（推定）', col=RED, portrait='p_shimazu', pts=[SHIMAZU_P, A(136.4690, 35.3652), A(136.4790, 35.3545), A(136.4880, 35.3410)], legs=[[2, 3], [3, 4], [4, 5]], at=0, head=28, lab_off=(34, -6), dashed=True),
               unit(label='井伊直政', col=BLUE, portrait='p_ii', pts=[A(136.4655, 35.3660)], at=4, head=22, lab_off=(-30, -40), lsize=22)],
        marks=[dict(xy=A(136.4790, 35.3545), label='負傷（伝承）', at=4, col=GOLD, lsize=20)])]),
 dict(key='after', title='その後', chapter_title='その後', scene=[
   dict(t='art', name='aftermath', box=ART_BOX, at=0, dim=0.8, dir=1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.62),
   dict(t='cols2', size=36, xm=940, xm2=980, left=dict(title='人の処分', title_at=0, items=[dict(at=0, text='9/21　石田三成、近江の山中で捕らえられる'), dict(at=1, text='10/1　三成・小西行長・安国寺恵瓊、京都の六条河原で処刑')]),
        right=dict(title='領地の変動（約）', title_at=2, items=[dict(at=3, text='豊臣家の直轄地：220万石 → 65万石'), dict(at=3, text='毛利：120万石 → 36万石（周防・長門）'), dict(at=3, text='上杉：120万石 → 30万石'), dict(at=4, text='島津：領地を守った'), dict(at=5, text='数字は、比べる条件で変わる')]))]),
 dict(key='check', title='通説と史料', chapter_title='通説と史料', scene=[
   dict(t='art', name='old_docs', box=ART_BOX, at=0, dim=0.8, dir=-1, note='イメージ（生成画像）。実際の資料の再現ではありません'), dict(t='shade', box=ART_BOX, at=0, alpha=0.66),
   dict(t='cols2', size=32, xm=940, xm2=980, until=2, left=dict(title='同時代の書状が伝えること', title_at=0, items=[dict(at=0, text='9/15　東軍が勝った'), dict(at=0, text='小早川・脇坂・小川が裏切った'), dict(at=0, text='巳の刻・午の刻という時刻の記述')]),
        right=dict(title='後世の軍記が描いたこと', title_at=1, items=[dict(at=1, text='霧の朝'), dict(at=1, text='問鉄砲と、迷う秀秋'), dict(at=1, text='島津の敵中突破'), dict(at=1, text='先陣を争う井伊と福島')])),
   dict(t='cols2', size=32, xm=940, xm2=980, at=2, left=dict(title='現代の研究でも確定できないこと', title_at=2, items=[dict(at=2, text='開戦は8時か、10時か'), dict(at=2, text='秀秋が動いたのは、開戦の直後か、昼ごろか'), dict(at=2, text='鉄砲の射撃があったのかどうか'), dict(at=2, text='各隊が崩れた順序と、布陣図そのもの')]),
        right=dict(title='見方', title_at=3, items=[dict(at=3, text='分かることと、物語として作られたことを、分けて見る')]))]),
]

images = dict(
    area=dict(file='assets/sekigahara/map_area.png'), core=dict(file='assets/sekigahara/map_core.png'), wide=dict(file='assets/sekigahara/map_wide.png'),
    p_ieyasu=dict(file='assets/portraits/ieyasu.jpg', crop=CROPS['ieyasu']), p_ishida=dict(file='assets/portraits/ishida.jpg', crop=CROPS['ishida']),
    p_kobaya=dict(file='assets/portraits/kobaya.jpg', crop=CROPS['kobaya']), p_otani=dict(file='assets/portraits/otani.jpg', crop=CROPS['otani']),
    p_ukita=dict(file='assets/portraits/ukita.jpg', crop=CROPS['ukita']), p_shimazu=dict(file='assets/portraits/shimazu.jpg', crop=CROPS['shimazu']),
    p_konishi=dict(file='assets/portraits/konishi.jpg', crop=CROPS['konishi']), p_fukushima=dict(file='assets/portraits/fukushima.jpg', crop=CROPS['fukushima']),
    p_ii=dict(file='assets/portraits/ii.jpg', crop=CROPS['ii']), p_mori=dict(file='assets/portraits/mori_h.jpg', crop=CROPS['mori_h']), p_kikkawa=dict(file='assets/portraits/kikkawa.jpg', crop=CROPS['kikkawa']),
    fog=dict(file='assets/sekigahara/art_fog.png'), council=dict(file='assets/sekigahara/art_council.png'),
    aftermath=dict(file='assets/sekigahara/art_aftermath.png'), old_docs=dict(file='assets/sekigahara/art_old_docs.png'))

def _line_to_sentence_starts():
    """台本の番号つきの行（1行に複数の文があることがある）→ 各行の最初の文の番号（vp.py の sentences と同じく「。」で区切る）。
    この spec の at / until / legs / title_at は『行の番号（0始まり）』で書き、ここで文の番号に直す。"""
    import re
    t = (R / 'docs' / 'themes' / '20261205_sekigahara' / '09_script_v2.md').read_text(encoding='utf8')
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

spec = dict(slug='sekigahara', theme_dir='20261205_sekigahara', pack='27_sekigahara', header_sub='関ヶ原の戦いを、地図の上で、書状と軍記を分けて確かめる',
 images=images,
 bgm=[['intro', 'forces', 'piano36'], ['mouri', 'kobayakawa', 'piano12'], ['collapse', 'check', 'piano40']],
 chapters=chapters,
 desc=dict(title_main='関ヶ原の戦いは、小早川秀秋の「問鉄砲」で決まったのか', title_no=2,
  titles=['関ヶ原の戦いを地図で解説 問鉄砲は本当？ 書状と軍記で確かめる', '関ヶ原の戦い 開戦は何時？ 小早川秀秋はいつ寝返った？ 史料で確かめる', '関ヶ原の戦いの流れ 南宮山の毛利・小早川の寝返り・島津の退却'],
  intro='慶長5年9月15日（1600年10月21日）、美濃の関ヶ原で、徳川家康の東軍と、石田三成らの西軍がぶつかりました。関ヶ原の戦いです。この動画では、地図の上で軍勢を動かしながら、戦いの流れを追います。そして、同時代の書状と、後世の軍記を分けて、「小早川秀秋は家康の鉄砲に脅されて寝返った」という通説を確かめます。分かることと決められないことを分けて、史料に帰属して述べます。',
  points=['戦いの二日後（9/17）の石川康通・彦坂元正連署書状には、巳の刻（午前10時ごろ）に石田三成らが関ヶ原へ移動し、東軍が攻め込んで戦いが始まった時、小早川秀秋・脇坂安治・小川祐忠父子が味方して裏切り、西軍が敗れた、とあります(研究者の要約による)。開戦時刻は、白峰旬氏は午前10時ごろ、笠谷和比古氏は午前8時ごろ(島津家臣の覚書に「夜明」から戦ったとある)とみます。',
          '小早川秀秋の寝返りは、白峰氏は開戦の直後、笠谷氏は昼ごろとみます。問鉄砲(家康が松尾山へ鉄砲を撃たせたという話)は、戦いの60年以上あとの『慶長軍記』など江戸時代の軍記に見えます。藤本正行氏・白峰氏は後世の創作とし、笠谷氏は、『備前老人物語』にある誤射の釈明の話などから、射撃はあったとみます。',
          '南宮山の毛利秀元らは、吉川広家が東軍と通じていたこともあり、主戦場の戦いに加わりませんでした(9/14の本多忠勝・井伊直政の起請文)。島津義弘は、西軍が崩れたあと、敵軍の正面を突破して退いたと伝わります。戦後、豊臣家の直轄地は約220万石から約65万石へ、毛利は約120万石から約36万石へ、上杉は約120万石から30万石へ減りました(概数)。',
          '布陣図の多くは、明治の『日本戦史 関原役』の図にもとづく通説的な配置で、同時代の史料から別の配置を考える研究もあります。兵力、開戦・終結の時刻、秀秋が動いた時刻、鉄砲射撃の有無は、史料だけでは断定できません。'],
  refs=['Wikipedia「関ヶ原の戦い」「小早川秀秋」(研究者の説と出典の整理)', '呉座勇一「家康は｢早く裏切れ｣と小早川秀秋に催促したわけではない…」PRESIDENT Online 2023-11-12:https://president.jp/articles/-/75298', '日経BizGate「家康はいつ小早川を裏切らせたか 関ケ原大論争が勃発」2022-09-15:https://bizgate.nikkei.com/article/DGXZQOLM07257007092022000000', '国土地理院 地理院タイル(陰影起伏図・標準地図):https://maps.gsi.go.jp/development/ichiran.html', 'OpenStreetMap contributors (ODbL):https://www.openstreetmap.org/copyright'],
  credit_lines=['・図：自作（国土地理院タイル(陰影起伏図・標準地図)を加工して作成。現代の地形で、当時の川筋や道ではありません。陣の位置と経路は、史料と現地の案内、OpenStreetMapの史跡座標をもとにした概略の推定です）',
                '・肖像：徳川家康・石田三成・小早川秀秋・宇喜多秀家・島津義弘・福島正則・井伊直政：古い肖像画。大谷吉継・小西行長：歌川芳幾の浮世絵（想像図）。いずれもWikimedia Commonsで公開されているパブリックドメインの画像です。顔は後世の描写で、本人の実像とは限りません。',
                '・イラスト：ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['地図上の軍勢の動きは、史料と研究をもとにした概略の図で、実際の経路・時刻ではありません。', '開戦・終結・寝返りの時刻は、史料と研究者で異なります。この動画は、一つの説を選ばず、並べて示しています。', '書状の内容は、研究者による要約・引用で確認したもので、原本・翻刻そのものは未照合です。'],
  tags='関ヶ原の戦い, 小早川秀秋, 問鉄砲, 徳川家康, 石田三成, 島津義弘, 戦国時代, 戦況解説, 検証, 白峰旬, 笠谷和比古',
  checks=['9/15付家康書状(伊達政宗宛)の原文と、午の刻の文脈を確認する(docs/themes/20261205_sekigahara/11_source_check.md)', '9/17付石川康通・彦坂元正連署書状(堀文書)の原文を確認する', '島津義弘の自伝(『惟新公御日記』『惟新公御自記』)の名称と、数刻の戦いの記述を確認する', '神戸五兵衛覚書、『備前老人物語』の該当箇所を確認する', '「問鉄砲」の元になった逸話(『慶長軍記』)と、陣・布陣の位置を確認する']),
 thumb=dict(bg='assets/sekigahara/thumb_art.png', lines=[['関ヶ原の戦い', 118, 'white'], ['問鉄砲は', 100, 'white'], ['本当？', 130, 'gold']], sub='書状と軍記を分けて確かめる', shade_col=[10, 14, 28], accent=[238, 96, 84], bar_col=[238, 96, 84], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and not o.get('title') and o['box'][3] - o['box'][1] <= 70: o['size'] = min(o.get('size', 40), 40)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


_fit(spec)
(R / 'data' / 'sekigahara_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
