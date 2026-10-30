"""Writes data/shimabara_spec.json（島原・天草の乱。戦況解説シリーズ10本目）。台本：docs/themes/20270116_shimabara/09_script_v2.md
文の番号は章内の0始まりの『行の番号』で書き、下で文の番号に直す。地図の座標は shimabara_maps.norm()。
位置は、国土地理院住所検索（南有馬町・北有馬町・口之津町・深江町・千々石町・島原市・苓北町富岡・天草市本渡町）による。軍の動きは概略の推定（画面に『推定』と明記）。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import shimabara_maps as MM
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]
BOX = [60, 250, 1860, 850]
BLUE = (90, 150, 255); RED = (238, 96, 84); GOLD = (239, 201, 118)
NC = json.loads((R / 'data' / 'nagashino_crops.json').read_text(encoding='utf8'))


def A(lon, lat): return list(MM.norm(lon, lat, 'area'))
def W(lon, lat): return list(MM.norm(lon, lat, 'wide'))


HARA = (130.257, 32.630); SHIMABARA = (130.3702, 32.788); TOMIOKA = (130.0294, 32.5223); HONDO = (130.19, 32.47); ARIMA = (130.2107, 32.6796)
KUCHINOTSU = (130.18, 32.60); FUKAE = (130.325, 32.722); CHIJIWA = (130.20, 32.777); OYANO = (130.4158, 32.598); KUMAMOTO = (130.7081, 32.8033); FUKUOKA = (130.4017, 33.59); SAGA = (130.3, 33.25)


def pn(text, at, until=None, size=40, hi=True, col=None):
    d = dict(t='panel', box=TOP, text=text, at=at, size=size, hi=hi)
    if until is not None: d['until'] = until
    if col: d['col'] = col
    return d


def unit(**k): return k
def NOTE_POS(at=0, txt='※位置は概略の推定'): return dict(xy=[0.02, 0.04], label=txt, kind='spot', at=at, side='r', col=GOLD, lsize=28)
def amap(img='area', **k): return dict(t='anim', name='battle_map', img=img, box=BOX, at=0, **k)


NOTE_IMG = 'イメージ（生成画像）。実際の場面の再現ではありません'
ART_BOX = [60, 170, 1860, 850]
EST = '※位置・経路は概略の推定'

chapters = [
 dict(key='intro', title='島原・天草の乱', chapter_title='導入：島原・天草の乱', opener='島原・天草の乱', opener_until=2, scene=[
   dict(t='art', name='sea', box=ART_BOX, at=0, dim=0.8, dir=1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.5),
   pn('島原の乱は、キリシタンの宗教戦争だったのか', 0, 1, 40, col='gold'), pn('寛永14年10/25（1637年12月11日）', 1, 2, 42),
   pn('肥前・島原と肥後・天草で、百姓たちが蜂起', 2, 3, 40), pn('総大将は、16歳の天草四郎（説）', 3, 4, 40),
   pn('キリシタンが弾圧に抗した反乱（通説）', 4, 5, 40, col='gold'), pn('記録は、乱の原因を、どう書いているのか', 5, 6, 40),
   pn('この回で原文を読めたのは、『島原記』だけ（国立国会図書館のデジタル資料）', 6, 7, 32, col='gold'), pn('ほかの記録は、日本語版Wikipediaなどの紹介を整理して確かめる', 7, 8, 34),
   pn('地図の上で追い、記録を確かめる', 8, None, 38)]),
 dict(key='land', title='島原と、天草', chapter_title='島原と、天草', scene=[
   pn('島原は、もとはキリシタン大名・有馬氏の領地（説）', 0, 1, 38), pn('慶長19年　有馬氏が転封（説）', 1, 2, 42),
   pn('元和2年　かわって松倉重政が入る（説）', 2, 3, 40), pn('重政は、厳しいキリシタンの取締りを始めた（説）', 3, 4, 38),
   pn('次の松倉勝家も、重政の政治を受け継いだ（説）', 4, 5, 38), pn('天草は、もとは小西行長の領地。関ヶ原の後、寺沢広高が入る（説）', 5, 6, 34),
   pn('次の寺沢堅高の時代まで、島原と同じような圧政と取締り（説）', 6, 7, 34), pn('領民は、重い年貢と飢饉に苦しんだ（説）', 7, None, 38),
   amap(places=[NOTE_POS(0, '※位置は概略の推定'), dict(xy=A(*SHIMABARA), label='島原城', kind='castle', at=0, side='l', col=RED, lsize=24),
                dict(xy=A(*HARA), label='原城跡', kind='castle', at=0, side='r', col=GOLD, lsize=22),
                dict(xy=A(*TOMIOKA), label='富岡城（唐津藩・天草）', kind='castle', at=5, side='l', col=RED, lsize=22)])]),
 dict(key='tax', title='重い年貢の、わけ', chapter_title='重い年貢の、わけ', scene=[
   dict(t='art', name='docs', box=ART_BOX, at=0, dim=0.8, dir=-1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.66),
   dict(t='cols2', size=30, xm=940, xm2=980, until=7, left=dict(title='島原・松倉重政（説）', title_at=0, items=[
        dict(at=0, text='江戸城の普請の役を受けた'), dict(at=1, text='島原城を新築した'), dict(at=2, text='ルソン島遠征の計画を立てた（1630年に先遣隊を送った）'), dict(at=4, text='計画は、重政の死で頓挫した'), dict(at=5, text='1637年にも、再び検討された')]),
        right=dict(title='費用は、年貢に（説）', title_at=6, items=[dict(at=6, text='費用は、領民への年貢にのしかかった')])),
   dict(t='cols2', size=30, xm=940, xm2=980, at=7, left=dict(title='天草・寺沢広高（説）', title_at=7, items=[
        dict(at=7, text='石高を42,000石と決めた'), dict(at=8, text='実際は、その半分ほどだった')]),
        right=dict(title='石高とは', title_at=9, items=[dict(at=9, text='土地の生産力の評価。実際の2倍の見積もりが、年貢の基準になった')]))]),
 dict(key='uprising', title='蜂起', chapter_title='蜂起', scene=[
   pn('重い取立てに耐えかね、島原の領民は、密かに反乱を計画（説）', 0, 1, 34), pn('中心は、百姓になった旧有馬氏の家臣たち（説）', 1, 2, 38),
   pn('天草でも、小西氏の浪人たちが中心になった（説）', 2, 3, 38), pn('16歳の天草四郎が、総大将に立てられた（説）', 3, 4, 38),
   pn('四郎は、キリシタンの間で、カリスマ的な人気があった（説）', 4, 5, 36), pn('『島原記』は、発端を、こう書く', 5, 6, 40, col='gold'), pn('代官たちは、キリシタンに立ち帰った者を取り調べ、角内と三吉を、妻子ともに15人、捕らえた（『島原記』）', 6, 7, 28),
   pn('仲間の者たちは、無念に思い、一同に一揆を起こした（『島原記』）', 7, 8, 34), pn('10/25　巳の刻、代官の林兵左衛門を斬り殺した（『島原記』）', 8, 9, 34, col='gold'),
   pn('島原の乱が、始まった（説）', 9, 10, 42), pn('南目では、領民が組織された（説）', 10, 11, 40), pn('賛成する者も、反対する者も、強制的に組み込まれた（説）', 11, 12, 36), pn('北目では、組織化できなかった（説）', 12, None, 40),
   amap(places=[NOTE_POS(0, EST), dict(xy=A(*ARIMA), label='有馬村（推定）', kind='spot', at=5, side='l', col=RED, lsize=22),
                dict(xy=A(*KUCHINOTSU), label='南目（口之津など）', kind='spot', at=10, side='l', col=GOLD, lsize=22),
                dict(xy=A(*CHIJIWA), label='北目（千々石など）', kind='spot', at=12, side='l', col=GOLD, lsize=22),
                dict(xy=A(*SHIMABARA), label='島原城', kind='castle', at=5, side='r', col=BLUE, lsize=22)],
        units=[unit(label='一揆軍', sub='島原', col=RED, portrait='p_amakusa', pts=[A(*ARIMA), A(FUKAE[0] - 0.01, FUKAE[1] + 0.01)], legs=[[8, 10]], at=8, head=22, lab_off=(36, -10), lsize=20, dashed=True)])]),
 dict(key='amakusa', title='天草の一揆', chapter_title='天草の一揆', scene=[
   pn('数日後、天草でも一揆が起こった（説）', 0, 1, 40), pn('11/14　本渡の戦いで、富岡城代の三宅重利が敗れた（説）', 1, 2, 36),
   pn('一揆軍は、富岡城を攻めたが、落とせなかった（説）', 2, 3, 38), pn('九州の諸藩の討伐軍が、近づいていると知った（説）', 3, 4, 38),
   pn('有明海を渡り、島原半島の原城の跡に籠もった（説）', 4, 5, 38), pn('原城は、もとは有馬氏の城で、すでに廃城だった（説）', 5, 6, 38),
   pn('原城は、キリシタンによって祝別を受けた城だった、という記録も（説）', 6, None, 34),
   amap(places=[NOTE_POS(0, EST), dict(xy=A(*HONDO), label='本渡', kind='spot', at=1, side='l', col=RED, lsize=22),
                dict(xy=A(*TOMIOKA), label='富岡城', kind='castle', at=2, side='l', col=BLUE, lsize=22), dict(xy=A(*HARA), label='原城跡', kind='castle', at=4, side='r', col=RED, lsize=24)],
        units=[unit(label='天草の一揆軍', sub='四郎を戴く', col=RED, portrait='p_amakusa', pts=[A(*HONDO), A(*TOMIOKA), A(HARA[0] - 0.12, HARA[1] - 0.08), A(*HARA)], legs=[[1, 2], [2, 4], [4, 5]], at=0, head=24, lab_off=(36, -10), lsize=20, dashed=True)])]),
 dict(key='hara', title='原城', chapter_title='原城', scene=[
   dict(t='art', name='castle', box=ART_BOX, at=0, dim=0.8, dir=1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.7),
   pn('ここに、島原と天草の一揆勢が、合流した（説）', 0, 1, 38), pn('『島原記』：城に籠もった男女は、3万7千百余人', 1, 2, 38, col='gold'),
   pn('総大将は、益田四郎時貞、16歳（『島原記』）', 2, 3, 38), pn('同じ書物の別の箇所は、討たれた四郎を17歳とする（『島原記』）', 3, 4, 34),
   pn('ただし、確かな数ではなく、2万7千人とする異説もある（説）', 4, 5, 36), pn('内訳の推定：戦える者1万4千人以上、女性や子どもなど1万3千人以上（説）', 5, 6, 30),
   pn('これは下限の数字で、これだけでは総人数は決められない', 6, 7, 36, col='gold'), pn('一揆軍は、原城の跡を修復した（説）', 7, 8, 40),
   pn('藩の蔵から奪った武器弾薬と食料を運び込んだ（説）', 8, 9, 38), pn('発掘で、竪穴の建物の跡が見つかった（説）', 9, 10, 40),
   pn('家族ごとに使ったとみられる（説）', 10, 11, 40), pn('調べた建物には、暖房や煮炊きの跡がない。失火を防ぐ軍規か（説）', 11, None, 32)]),
 dict(key='army', title='討伐軍', chapter_title='討伐軍', scene=[
   pn('幕府は、上使として、板倉重昌を送った（説）', 0, 1, 40), pn('九州の諸藩の軍勢が、原城を囲んだ（説）', 1, 2, 40), pn('12月に二度、総攻撃をしたが、敗れた（説）', 2, 3, 40),
   pn('討伐軍は、諸藩の寄せ集めだった（説）', 3, 4, 40), pn('重昌は、大名としては禄が小さく、九州の大名は従わなかった（説）', 4, 5, 34),
   pn('幕府は、老中の松平信綱を送ることにした（説）', 5, 6, 40), pn('手柄を奪われるのを恐れた重昌は、寛永15年の元日に総攻撃（説）', 6, 7, 34),
   pn('今の暦で、1638年2月14日（説）', 7, 8, 42), pn('重昌は、鉄砲に撃たれて戦死した（説）', 8, 9, 40), pn('信綱らが着陣し、討伐軍は12万以上に（説）', 9, 10, 38),
   pn('全期間では、13万近くという数もある（説）', 10, 11, 40), pn('『常山紀談』（後世の書物）：重昌の派遣に、柳生宗矩が反対した、という話（説）', 11, None, 30),
   amap(places=[NOTE_POS(0, '※位置は概略の推定（模式）'), dict(xy=A(*HARA), label='原城', kind='castle', at=0, side='l', col=RED, lsize=26),
                dict(xy=A(*SHIMABARA), label='島原城', kind='castle', at=0, side='r', col=BLUE, lsize=22)],
        units=[unit(label='討伐軍（九州の諸藩）', sub='板倉重昌の軍', col=BLUE, portrait='p_itakura', pts=[A(130.55, 32.84), A(HARA[0] + 0.06, HARA[1] + 0.07), A(HARA[0] + 0.02, HARA[1] + 0.02)], legs=[[1, 2], [6, 8]], at=0, head=24, lab_off=(-36, -10), lsize=22, dashed=True)])]),
 dict(key='siege', title='兵糧攻め', chapter_title='兵糧攻め', scene=[
   pn('信綱は、兵糧攻めに切り替えた、といわれる（説）', 0, 1, 38), pn('同じ年の旧暦1月、オランダ商館長が、船の大砲を提供（説）', 1, 2, 34),
   pn('船からも、城内へ砲撃した（説）', 2, 3, 40), pn('効果は、小さかったとされる（説）', 3, 4, 40), pn('士気を削いだという見方もあるが、確かめられない', 4, 5, 36),
   pn('日本の諸将からは、外国人の助けを受けることへの批判も出た（説）', 5, 6, 34), pn('討伐軍は、矢文などで、投降を呼びかけた（説）', 6, 7, 38),
   pn('生け捕りにした天草四郎の母と姉妹に手紙を書かせたが、拒否された（説）', 7, 8, 32), pn('一揆軍は、断崖を降りて、海藻を食料の足しにした（説）', 8, 9, 34),
   pn('城外で討たれた一揆軍の胃の中が、海藻だけだったことから、信綱は、食料が尽きかけていると知った、といわれる（説）', 9, None, 28),
   amap(places=[NOTE_POS(0, EST), dict(xy=A(*HARA), label='原城', kind='castle', at=0, side='r', col=RED, lsize=24)],
        lines=[dict(pts=[A(HARA[0] - 0.03, HARA[1] - 0.025), A(HARA[0] + 0.01, HARA[1] - 0.035), A(HARA[0] + 0.04, HARA[1] - 0.005), A(HARA[0] + 0.02, HARA[1] + 0.03), A(HARA[0] - 0.02, HARA[1] + 0.035), A(HARA[0] - 0.045, HARA[1] + 0.005), A(HARA[0] - 0.03, HARA[1] - 0.025)], label='討伐軍の包囲（模式）', at=0, col=BLUE, dash=True, lab=[0.60, 0.25])],
        units=[unit(label='オランダ船', col=BLUE, pts=[A(HARA[0] - 0.12, HARA[1] + 0.07), A(HARA[0] - 0.05, HARA[1] + 0.03)], legs=[[1, 2]], at=1, head=20, lab_off=(-36, -10), lsize=20, dashed=True)])]),
 dict(key='fall', title='落城', chapter_title='落城', scene=[
   pn('旧暦2/24　信綱の陣で軍議が開かれた（説）', 0, 1, 38), pn('兵糧攻めの継続を主張する人と、総攻撃を主張する人がいた（説）', 1, 2, 34),
   pn('信綱は、総攻撃を決めた（説）', 2, 3, 42), pn('総攻撃は、28日の予定だった（説）', 3, 4, 40), pn('けれども、鍋島勝茂が抜け駆けして、前日に始まった（説）', 4, 5, 36),
   pn('原城は落ち、天草四郎は討ち取られた（説）', 5, 6, 40), pn('2/28　今の暦で、1638年4月12日（説）', 6, 7, 40, col='gold'),
   pn('本丸の一番乗りは、後世の書物では争いが語られ、記録ではっきりしない（説）', 7, 8, 32), pn('『島原記』：城中の男女3万7千余人が、死亡した', 8, 9, 38, col='gold'),
   pn('生け捕りにされた落人たちも、2/29、原城の焼け跡で斬られた（『島原記』）', 9, 10, 32), pn('助命されたのは、絵師の山田右衛門作ら、わずか（『島原記』）', 10, 11, 36),
   pn('総攻撃の前に、投降や脱出をした人もいた、という説も（説）', 11, 12, 34),
   pn('投降者は1万人以上と推測する説もあるが、記録がなく、実数は分からない（説）', 12, None, 30),
   amap(places=[NOTE_POS(0, '※位置は概略の推定。経路は確定しない'), dict(xy=A(*HARA), label='原城（本丸）', kind='castle', at=5, side='r', col=RED, lsize=24)],
        units=[unit(label='討伐軍', sub='総攻撃', col=BLUE, pts=[A(HARA[0] - 0.05, HARA[1] + 0.02), A(*HARA)], legs=[[4, 6]], at=4, head=22, lab_off=(-36, 10), lsize=20, dashed=True)])]),
 dict(key='numbers', title='数字と、処分', chapter_title='数字と、処分', scene=[
   dict(t='art', name='docs', box=ART_BOX, at=0, dim=0.8, dir=1, note='イメージ（生成画像）。実際の資料の再現ではありません'), dict(t='shade', box=ART_BOX, at=0, alpha=0.66),
   dict(t='cols2', size=29, xm=940, xm2=980, until=7, left=dict(title='討伐軍の死傷者', title_at=0, items=[
        dict(at=1, text='『島原記』（2/27・28の二日間）：討死1,136・手負6,950余・計8,086'), dict(at=3, text='紹介される数字：死者1,130・負傷者6,960'), dict(at=4, text='『有馬一件』：死者2,800・負傷者7,700（紹介）'), dict(at=5, text='『オランダ商館長日記』：8万のうち死者5,712（紹介）'), dict(at=6, text='後の二つは、原典で確かめられていない')]),
        right=dict(title='', title_at=0, items=[])),
   dict(t='cols2', size=29, xm=940, xm2=980, at=7, left=dict(title='処分（説）', title_at=7, items=[
        dict(at=7, text='松倉勝家：責任を問われ、領地を取り上げられ、のちに斬首'), dict(at=9, text='大名が切腹でなく斬首となったのは、この一件だけ')]),
        right=dict(title='ほかの処分（説）', title_at=10, items=[dict(at=10, text='寺沢堅高：天草の領地を没収'), dict(at=11, text='鍋島勝茂：抜け駆けの責任で、半年の閉門')]))]),
 dict(key='after', title='その後', chapter_title='その後', scene=[
   pn('幕府は、キリシタンが、乱の拡大に関わったと考えた（説）', 0, 1, 36), pn('寛永16年　ポルトガル船の来航を禁止（説）', 1, 2, 40),
   pn('寛永18年　オランダ商館を出島に移した（説）', 2, 3, 40), pn('禁教は強化された。寺請制度も、乱の後に整えられていった（説）', 3, 4, 36),
   pn('島原と天草は、人口が激減した（説）', 4, 5, 40), pn('幕府は、各藩に、農民の移住を命じた（説）', 5, 6, 40), pn('天草は、のちに幕府の直轄領になった（説）', 6, 7, 40),
   pn('わずかに残ったキリシタンは、潜伏し、隠れキリシタンに（説）', 7, 8, 36), pn('文化2年　天草で取り調べ。5,200人に疑い（説）', 8, 9, 38), pn('村人は否定し、踏み絵と誓約だけで赦免された（説）', 9, None, 38),
   amap(places=[NOTE_POS(0, '※位置は概略の推定'), dict(xy=A(*HONDO), label='天草', kind='spot', at=6, side='l', col=GOLD, lsize=24), dict(xy=A(*HARA), label='原城跡', kind='castle', at=0, side='r', col=GOLD, lsize=22)])]),
 dict(key='summary', title='宗教戦争だったのか', chapter_title='宗教戦争だったのか', scene=[
   dict(t='art', name='castle', box=ART_BOX, at=0, dim=0.8, dir=-1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.62),
   dict(t='cols2', size=29, xm=940, xm2=980, until=9, left=dict(title='記録は、原因を、どう書くか', title_at=0, items=[
        dict(at=0, text='『島原記』：発端は、キリシタンの復宗者の取り調べと、仲間の怒り'), dict(at=1, text='『細川家記』『天草島鏡』など：年貢の取りすぎ（紹介）'), dict(at=2, text='どれも、のちにまとめられた記録で、同時代の記録ではない')]),
        right=dict(title='宗教戦争という見方', title_at=3, items=[
        dict(at=3, text='松倉勝家は、キリシタンの暴動だと主張した'), dict(at=4, text='幕府も、禁教政策の口実にしたといわれる'), dict(at=6, text='信仰が、結束の核になった、という見方もある'), dict(at=8, text='「殉教」も「百姓一揆」も、乱の一面にすぎない')])),
   dict(t='cols2', size=30, xm=940, xm2=980, at=9, until=12, left=dict(title='分かること', title_at=9, items=[
        dict(at=9, text='重い年貢と飢饉の中で、島原・天草の人々が蜂起し、原城で鎮圧された')]),
        right=dict(title='決められないこと', title_at=10, items=[dict(at=10, text='籠城した人の実数と、亡くなった人の数'), dict(at=11, text='乱の原因を、どれか一つに決めること')])),
   dict(t='cols2', size=33, xm=940, xm2=980, at=12, left=dict(title='見方', title_at=12, items=[
        dict(at=12, text='記録と、後の見方を、分けて見ると、見え方が変わる')]), right=dict(title='', title_at=12, items=[]))]),
]

images = dict(
    area=dict(file='assets/shimabara/map_area.png'), wide=dict(file='assets/shimabara/map_wide.png'),
    p_amakusa=dict(file='assets/portraits/amakusa.jpg', crop=[0.25, 0.1, 0.75, 0.5]), p_itakura=dict(file='assets/portraits/itakura.jpg', crop=[0.33, 0.355, 0.57, 0.485]),
    sea=dict(file='assets/shimabara/art_sea.png'), docs=dict(file='assets/shimabara/art_docs.png'), castle=dict(file='assets/shimabara/art_castle.png'))


def _line_to_sentence_starts():
    import re
    t = (R / 'docs' / 'themes' / '20270116_shimabara' / '09_script_v2.md').read_text(encoding='utf8')
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

T1 = '【島原の乱は宗教戦争？】島原・天草の乱 原因と全滅の話を記録の紹介で確かめる｜地図で解説'
spec = dict(slug='shimabara', theme_dir='20270116_shimabara', pack='37_shimabara', header_sub='島原・天草の乱を、地図の上で、記録の紹介と後世の見方に分けて確かめる',
 images=images,
 bgm=[['intro', 'tax', 'piano36'], ['uprising', 'fall', 'piano12'], ['numbers', 'summary', 'piano40']],
 chapters=chapters,
 desc=dict(title_main=T1, title_no=1,
  titles=[T1, '島原・天草の乱を地図で解説 原因は宗教か年貢か？籠城した人は全員亡くなったのか', '島原の乱 原城の籠城と落城、宗教戦争という見方を、記録の紹介と研究で分けて確かめる'],
  intro='寛永14年10月25日（1637年12月11日）、肥前の島原と肥後の天草で、百姓たちが蜂起しました。島原・天草の乱です。キリシタンの宗教戦争だった、原城の三万七千人は全員が亡くなった、という話が知られます。この動画では、地図の上で乱の経過を追いながら、「乱の原因は何か」「籠城した人は全員が亡くなったのか」「討伐軍の被害はどれほどか」を、日本語版Wikipediaなどが紹介する記録（『細川家記』『天草島鏡』『島原記』『有馬一件』『オランダ商館長日記』など）と研究に分けて確かめます。この回で原文を確認できたのは『島原記』（史籍集覧所収。国立国会図書館デジタルコレクション）だけで、ほかは直接確認できていません。分かることと決められないことを分けて、最後にまとめます。',
  points=['経過（二次資料の紹介）：慶長19年に有馬氏が転封され、元和2年に松倉重政が島原に入り、過重な年貢とキリシタンの取締りが行われた。天草は寺沢広高が石高を実態の約2倍の4万2千石と算定した。寛永14年10/25、有馬村のキリシタンが代官の林兵左衛門を殺して蜂起し、天草でも一揆が起こって、11/14に本渡で富岡城代の三宅重利が敗れた。一揆軍は有明海を渡って原城跡に籠もった。幕府は板倉重昌を上使に送ったが、寛永15年元日（1638年2月14日）の総攻撃で重昌は戦死し、老中松平信綱が着陣して討伐軍は12万以上に。兵糧攻めののち、2/28（1638年4月12日）に原城が落ち、天草四郎は討たれた。',
          '原因：『島原記』（原文確認）は、発端を、キリシタンに立ち帰った者の取り調べ（角内・三吉ら15人の捕縛）と、その仲間の怒りに置き、10/25巳の刻に代官の林兵左衛門を斬り殺した、と書きます。一方、『細川家記』『天草島鏡』などが原因を年貢の取りすぎとする、と紹介されます。ただし、どちらものちにまとめられた記録で、同時代の記録ではありません（『天草島鏡』は19世紀の編纂物とされます）。松倉勝家は自らの失政を認めずキリシタンの暴動と主張し、幕府も禁教政策の口実にしたため、「宗教戦争」という見方が広まった、と紹介されます。一方、信仰が一揆の結束の核だったことも確かで、旧有馬・小西氏の浪人なども加わっており、「殉教」も「百姓一揆」も乱の一面にすぎない、とされます。',
          '数字：籠城した人数は約3万7千人（推定。2万7千人とする異説もあり、内訳の推定は下限の数字で、これだけでは総人数を決められません）。討伐軍は12万以上（全期間で13万近く）。討伐軍の死傷者は、『島原記』の本文が、2/27・28の二日間で討死1,136・手負6,950余（紹介される数字は死者1,130・負傷者6,960）、『有馬一件』が死者2,800・負傷者7,700、『オランダ商館長日記』が8万のうち死者5,712、と紹介されます（原典は未確認）。籠城した人は「ほとんどが殺された」とされますが、投降・脱出者がいた、という説もあり、1万人以上と推測する説も記録がなく実数は不明です。',
          '処分と影響：松倉勝家は領地を取り上げられ斬首（江戸時代の大名で切腹でなく斬首となったのは唯一とされる）。寺沢堅高は天草を没収。寛永16年にポルトガル船の来航を禁止、寛永18年にオランダ商館を出島へ。島原・天草は人口が激減し、各藩から移住が命じられました。',
          '地図上の軍勢の動きは、紹介されている記録にもとづく大まかな図で、実際の経路・順序ではありません。天草四郎の肖像（歌川芳年）は後世の想像図です。'],
  refs=['Wikipedia「島原の乱」(紹介される記録と研究の整理。この回の主な根拠)', '南島原市公式ホームページ（原城跡の発掘情報）', '国立天文台 暦計算室「日本の暦日データベース」', '国土地理院 地理院タイル:https://maps.gsi.go.jp/development/ichiran.html'],
  credit_lines=['・図：自作（国土地理院タイル(陰影起伏図・標準地図)を加工して作成。現代の地形です。城・軍の位置は、案内をもとにした概略の推定です）',
                '・肖像：天草四郎：歌川芳年の浮世絵（想像図）。板倉重昌：古い肖像画。Wikimedia Commonsで公開されているパブリックドメインの画像です。',
                '・イラスト：ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['『島原記』は、近藤瓶城編『史籍集覧』（新加別記第七十四）の本文を、国立国会図書館デジタルコレクションのOCRテキストで確認しました（発端、城中の人数、四郎の年齢、落城後の処置、2/27・28の死傷者）。『細川家記』『天草島鏡』『有馬一件』『オランダ商館長日記』などは直接確認していません。日本語版Wikipedia、南島原市などの公的な解説を通して確認した内容です。研究者名は出していません。', '地図上の軍勢の動きは、記録の紹介と推定にもとづく概略の図で、実際の経路・時刻ではありません。'],
  tags='島原の乱, 島原天草の乱, 天草四郎, 原城, 松倉勝家, 松平信綱, 戦況解説, 検証, 江戸時代, キリシタン',
  checks=['『細川家記』『天草島鏡』の該当部分（原因の記述）', '『島原記』『有馬一件』『オランダ商館長日記』の数字の原典確認', '籠城人数の根拠', '投降・脱出者の根拠', '寺請制度の成立時期の表現', '松倉勝家の斬首の日付']),
 thumb=dict(bg='assets/shimabara/thumb_art.png', lines=[['島原の乱は', 112, 'white'], ['宗教戦争', 112, 'white'], ['だったのか？', 112, 'gold']], sub='原因と全滅の話を、記録の紹介で確かめる', shade_col=[10, 14, 28], accent=[238, 96, 84], bar_col=[238, 96, 84], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and not o.get('title') and o['box'][3] - o['box'][1] <= 70: o['size'] = min(o.get('size', 40), 40)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


_fit(spec)
(R / 'data' / 'shimabara_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
