"""Writes data/nagashino_spec.json（長篠の戦い。戦況解説シリーズ1本目）。台本：docs/themes/20261127_nagashino/09_script_v2.md
文の番号（at・legs）は `python scripts/vp.py nagashino sents` の番号。地図の座標は nagashino_maps.norm()（位置の不明なものは概略の推定値で、画面に「推定」と明記）。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from specart import inject
import nagashino_maps as NM
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]
BOX = [60, 250, 1860, 850]
BLUE = (90, 150, 255); RED = (238, 96, 84); GRN = (110, 214, 140); GOLD = (239, 201, 118); WATER = (130, 195, 255)
CROPS = json.loads((R / 'data' / 'nagashino_crops.json').read_text(encoding='utf8'))


def A(lon, lat): return list(NM.norm(lon, lat, 'area'))
def Wd(lon, lat): return list(NM.norm(lon, lat, 'wide'))


CASTLE = A(137.55985, 34.92282)          # 長篠城跡（Wikipedia座標）
IOJI = A(137.55787, 34.93034)            # 医王寺（勝頼本陣と伝わる）
# 以下は、史料・案内の記述をもとにした概略の推定位置（正確な地点ではない）
GOKURAKU = [0.17, 0.40]                  # 信長の本陣（極楽寺山）
TAKAMATSU = [0.24, 0.62]                 # 家康の陣（高松山／弾正山）
TAKEDA_BASE = [0.40, 0.58]               # 武田軍（連吾川の東の台地）
FENCE = [[0.268, 0.42], [0.262, 0.60], [0.256, 0.80]]     # 馬防柵（連吾川沿い）
RENGO = [[0.292, 0.30], [0.286, 0.50], [0.281, 0.68], [0.276, 0.96]]
TOBI = A(137.5695, 34.9165)                      # 鳶ノ巣山砦（長篠城の東。位置は推定）


def pn(text, at, until=None, size=40, hi=True, col=None):
    d = dict(t='panel', box=TOP, text=text, at=at, size=size, hi=hi)
    if until is not None: d['until'] = until
    if col: d['col'] = col
    return d


def unit(**k): return k


def amap(img='area', **k):
    return dict(t='anim', name='battle_map', img=img, box=BOX, at=0, **k)


chapters = [
 dict(key='intro', title='長篠の戦い', chapter_title='導入：長篠の戦い', opener='長篠の戦い', opener_until=3, scene=[
   pn('天正3年（1575）旧暦5月21日', 0, 1, 44), pn('今の暦では、7月9日にあたる（新城市）', 1, 2, 42),
   pn('愛知県・設楽原：織田・徳川の連合軍 対 武田勝頼の軍', 2, 4, 40), pn('「武田の騎馬隊が、鉄砲で全滅した」？', 4, 6, 44, col='gold'),
   pn('戦いは、二か所で、同時に進んだ', 6, 8, 44), pn('地図で追い、『信長公記』などの記録で、通説を確かめる', 8, None, 40),
   amap('wide', places=[dict(xy=Wd(137.55985, 34.92282), label='長篠城', kind='castle', at=7, side='b', col=BLUE),
                        dict(xy=Wd(137.5215, 34.9225), label='設楽原', kind='spot', at=7, side='t', col=RED)])]),
 dict(key='siege', title='長篠城の包囲', chapter_title='長篠城の包囲', scene=[
   pn('発端：三河の長篠城', 0, 1, 44), pn('武田勝頼：約1万5千で長篠城を囲む（新城市）', 1, 2, 40, col='gold'),
   pn('城主 奥平貞昌（のちの信昌）', 2, 3, 44), pn('守る兵：約500（新城市）', 3, 4, 44),
   pn('5/14 鳥居強右衛門ら、援軍を求めて岡崎へ', 4, 5, 42), pn('強右衛門は、帰りに捕らえられ、磔にされたと伝わる', 5, 6, 40),
   pn('信長は、その前の5/13に、すでに出陣していた（信長公記）', 6, None, 38, col='gold'),
   amap(places=[dict(xy=CASTLE, label='', kind='castle', at=0, side='b', col=BLUE)],
        lines=[dict(pts=[CASTLE, [0.04, 0.78]], label='岡崎の方へ（経路は推定）', at=4, col=GOLD, dash=True, lab=[0.20, 0.64])],
        units=[unit(label='武田勝頼', sub='約1万5千（新城市）', col=RED, portrait='p_katsuyori', pts=[IOJI], at=1, head=28, lab_off=(40, -10)),
               unit(label='奥平貞昌', sub='城兵 約500', col=BLUE, portrait='p_okudaira', pts=[CASTLE], at=2, head=24, lab_off=(-24, 52))])]),
 dict(key='march', title='信長の進軍', chapter_title='信長の進軍', scene=[
   pn('5/13 信長・信忠、出陣（信長公記）', 0, 1, 42), pn('5/14 岡崎に着陣', 1, 2, 44), pn('5/16 牛窪の城に泊まる', 2, 3, 44),
   pn('5/17 野田原で野陣', 3, 4, 44), pn('5/18 設楽の郷・極楽寺山に陣を置く', 4, 5, 42), pn('信忠は、新御堂山に陣取る', 5, None, 44),
   amap('wide', places=[dict(xy=Wd(137.55985, 34.92282), label='長篠城', kind='castle', at=0, side='b', col=BLUE),
                        dict(xy=Wd(137.15994, 34.95581), label='岡崎', kind='spot', at=1, side='t', col=GOLD),
                        dict(xy=Wd(137.38294, 34.80906), label='牛窪', kind='spot', at=2, side='b', col=GOLD),
                        dict(xy=Wd(137.4772, 34.8905), label='野田原', kind='spot', at=3, side='b', col=GOLD),
                        dict(xy=Wd(137.5215, 34.9225), label='極楽寺山', kind='camp', at=4, side='t', col=RED)],
        units=[unit(label='織田信長', col=BLUE, portrait='p_nobunaga', pts=[Wd(137.15994, 34.95581), Wd(137.38294, 34.80906), Wd(137.4772, 34.8905), Wd(137.5215, 34.9225)],
                    legs=[[1, 2], [2, 3], [3, 4]], at=1, head=28, lab_off=(36, -6)),
               unit(label='織田信忠', col=BLUE, portrait='p_nobutada', pts=[Wd(137.5155, 34.9215)], at=5, head=22, lab_off=(-26, 46))])]),
 dict(key='forces', title='両軍の兵力と指揮官', chapter_title='両軍の兵力と指揮官', scene=[
   pn('信長方：「三万ばかり」（信長公記）', 0, 1, 42), pn('家康：「高松山」に陣を取る（信長公記）', 1, 2, 42),
   pn('武田方：「一万五千ばかり」（信長公記）', 2, 3, 42), pn('甲斐・信濃・西上野などの兵が、十三か所に分かれ、西向きに構えた', 3, 4, 36),
   pn('通説：連合軍 約3万8千／武田軍 約1万5千', 4, 6, 42, col='gold'), pn('史料や説明で数字に違いがあり、数える範囲も検討が必要', 6, 7, 38),
   pn('山県昌景・馬場信春：信玄の時代から仕えた重臣', 7, None, 40),
   amap(places=[dict(xy=[0.05, 0.93], label='※陣の位置は、すべて概略の推定', kind='spot', at=0, side='r', col=GOLD, lsize=28)],
        units=[unit(label='信長方', sub='約3万（信長公記）', col=BLUE, portrait='p_nobunaga', pts=[GOKURAKU], at=0, head=28, lab_off=(40, -10)),
               unit(label='家康（高松山）', col=BLUE, portrait='p_ieyasu', pts=TAKAMATSU and [TAKAMATSU], at=1, head=26, lab_off=(36, 6)),
               unit(label='武田勝頼', sub='約1万5千（13か所）', col=RED, portrait='p_katsuyori', pts=[TAKEDA_BASE], at=2, head=28, lab_off=(36, -10)),
               unit(label='山県昌景', sub='浮世絵（想像図）', col=RED, portrait='p_yamagata', pts=[[0.47, 0.44]], at=7, head=22, lab_off=(34, -4), lsize=30),
               unit(label='馬場信春', sub='肖像（制作年代は不確か）', col=RED, portrait='p_baba', pts=[[0.47, 0.72]], at=7, head=22, lab_off=(34, -4), lsize=30)])]),
 dict(key='terrain', title='設楽原の地形と馬防柵', chapter_title='設楽原の地形と馬防柵', scene=[
   pn('設楽原：台地の間を、連吾川が流れる谷あい', 0, 2, 42), pn('「一段と地形がくぼんだ所」。人数を、段々に置く（信長公記）', 2, 4, 36),
   pn('家康・滝川一益らの陣の前に、馬を防ぐ柵（信長公記）', 4, 5, 38, col='gold'), pn('柵は、連吾川に沿って築かれた（新城市）', 5, 6, 40),
   pn('武田軍は、川の東の台地に陣を取る（新城市）', 6, 7, 40), pn('両軍の間：二十町、約2.2km（信長公記）', 7, None, 44),
   amap(places=[dict(xy=[0.05, 0.93], label='※位置は概略の推定', kind='spot', at=0, side='r', col=GOLD, lsize=28), dict(xy=[0.281, 0.68], label='連吾川（付近）', kind='spot', at=0, side='b', col=WATER, lsize=28)],
        lines=[dict(pts=FENCE, label='馬防柵（位置は推定）', at=4, col=GOLD, dash=True, lab=[0.256, 0.80]),
               dict(pts=[[0.21, 0.90], [0.395, 0.90]], label='約2.2km（二十町）', at=7, col=(245, 243, 232), lab=[0.30, 0.90])],
        units=[unit(label='織田・徳川', col=BLUE, portrait='p_nobunaga', pts=[[0.19, 0.55]], at=2, head=26, lab_off=(-20, -44)),
               unit(label='武田軍', col=RED, portrait='p_katsuyori', pts=[TAKEDA_BASE], at=6, head=26, lab_off=(34, -4))])]),
 dict(key='flank', title='酒井忠次の別働隊', chapter_title='酒井忠次の別働隊', scene=[
   pn('5/20 信長、酒井忠次を大将に命じる', 0, 2, 42), pn('徳川方の弓・鉄砲の者 約2千人＋信長方の鉄砲500挺など：総勢 約4千', 2, 4, 34),
   pn('5/20夜、戌の刻　乗本川を渡り、南の深い山を回る', 4, 6, 40), pn('道すじは推定', 6, 7, 44, col='gold'),
   pn('5/21朝、辰の刻　鳶ノ巣山を攻め取る', 7, 9, 42), pn('数百挺の鉄砲を撃ちかけ、武田軍を追い払う', 9, 10, 40),
   pn('長篠城の兵と合流。敵の陣の小屋を焼き上げ、包囲は崩れた', 10, None, 38),
   amap(places=[dict(xy=CASTLE, label='長篠城', kind='castle', at=0, side='b', col=BLUE),
                dict(xy=TOBI, label='鳶ノ巣山砦（位置は推定）', kind='camp', at=7, side='b', col=RED)],
                units=[unit(label='酒井忠次の別働隊', sub='約4千（信長公記）', col=GRN, portrait='p_sakai', pts=[TAKAMATSU, [0.30, 0.86], [0.56, 0.84], TOBI, CASTLE],
                    legs=[[5, 6], [6, 7], [7, 8], [10, 11]], at=4, head=28, lab_off=(36, -6))],
        marks=[dict(xy=TOBI, label='', at=8, col=GRN)])]),
 dict(key='battle', title='設楽原の戦い：五つの攻撃', chapter_title='設楽原の戦い：五つの攻撃', scene=[
   pn('5/21 日の出のころ　設楽原でも戦いが始まる', 0, 1, 42), pn('鉄砲 千挺ばかり：五人の奉行が指揮（信長公記）', 1, 2, 40),
   pn('武田方の攻撃は五つ。『信長公記』の叙述の順で見る。実際の時刻は不明', 2, 5, 34, col='gold'),
   pn('①山県昌景：押太鼓で攻めかかるが、鉄砲で撃たれ、引き退く', 5, 7, 38), pn('②正用軒：信玄の弟・武田信廉とされる', 7, 9, 42),
   pn('③西上野の小幡一党', 9, 10, 44), pn('④典厩：信玄の甥・武田信豊とされる', 10, 12, 42), pn('⑤馬場信春', 12, 13, 44),
   pn('どの攻撃も、鉄砲で大半を打ち倒され、引いた（信長公記）', 13, 14, 38, col='gold'), pn('日の出から、午後の未の刻（午後2時ごろ）まで', 14, None, 40),
   amap(places=[dict(xy=[0.05, 0.93], label='※位置は概略の推定。一つずつ往復したわけではない', kind='spot', at=2, side='r', col=GOLD, lsize=28), dict(xy=[0.281, 0.68], label='連吾川（付近）', kind='spot', at=0, side='b', col=WATER, lsize=28)],
        lines=[dict(pts=FENCE, label='馬防柵（位置は推定）', at=0, col=GOLD, dash=True, lab=[0.256, 0.80])],
        units=[unit(label='織田・徳川', sub='鉄砲 千挺ばかり', col=BLUE, portrait='p_nobunaga', pts=[[0.20, 0.58]], at=1, head=26, lab_off=(-22, -48)),
               unit(label='①山県昌景', col=RED, portrait='p_yamagata', pts=[[0.44, 0.38], [0.30, 0.38], [0.44, 0.38]], legs=[[5, 6], [6, 7]], at=5, head=22, lab_off=(34, -4), lsize=30),
               unit(label='②正用軒', col=RED, pts=[[0.44, 0.48], [0.30, 0.48], [0.44, 0.48]], legs=[[7, 8], [8, 9]], at=7, head=20, lab_off=(34, -4), lsize=30),
               unit(label='③小幡一党', col=RED, pts=[[0.44, 0.58], [0.30, 0.58], [0.44, 0.58]], legs=[[9, 10], [10, 11]], at=9, head=20, lab_off=(34, -4), lsize=30),
               unit(label='④典厩', col=RED, pts=[[0.44, 0.68], [0.30, 0.68], [0.44, 0.68]], legs=[[10, 11], [11, 12]], at=10, head=20, lab_off=(34, -4), lsize=30),
               unit(label='⑤馬場信春', col=RED, portrait='p_baba', pts=[[0.44, 0.78], [0.30, 0.78], [0.44, 0.78]], legs=[[12, 13], [13, 14]], at=12, head=22, lab_off=(34, -4), lsize=30)])]),
 dict(key='collapse', title='崩れる武田軍', chapter_title='崩れる武田軍', scene=[
   pn('攻撃を続けた武田軍は、次第に人数が少なくなる', 0, 1, 40), pn('勝頼の旗元へ駆け集まるが、持ちこたえられず、鳳来寺の方へ退く', 1, 2, 38),
   pn('討ち取った首：山県昌景・馬場信春・真田源太左衛門ら（信長公記）', 2, 3, 36), pn('侍や雑兵の討死：約1万と記す。実数は確定できない', 3, 5, 38, col='gold'),
   pn('馬場信春の働きは、比べるものがないと記される', 5, 6, 40), pn('信長は、5/25、岐阜へ戻る', 6, None, 44),
   amap(places=[dict(xy=[0.05, 0.93], label='※位置・経路は概略の推定', kind='spot', at=0, side='r', col=GOLD, lsize=28)],
        lines=[dict(pts=FENCE, label='馬防柵', at=0, col=GOLD, dash=True, lab=[0.256, 0.80])],
        units=[unit(label='織田・徳川', col=BLUE, portrait='p_nobunaga', pts=[[0.20, 0.58]], at=0, head=26, lab_off=(-22, -48)),
               unit(label='武田勝頼の軍', col=RED, portrait='p_katsuyori', pts=[TAKEDA_BASE, [0.62, 0.32], [0.84, 0.14]], legs=[[1, 2], [2, 3]], at=0, head=28, lab_off=(36, 10), dashed=True)],
        marks=[dict(xy=[0.36, 0.40], label='山県昌景ら 討死', at=3, col=RED, lsize=28)])]),
 dict(key='after', title='その後', chapter_title='その後', scene=[
   dict(t='cols2', size=36, xm=940, xm2=980, left=dict(title='『信長公記』が記すこと', title_at=0, items=[dict(at=0, text='長篠城は救われた'), dict(at=1, text='家康は駿河へ攻め入った')]),
        right=dict(title='その後と、分かれる評価', title_at=2, items=[dict(at=2, text='武田氏の滅亡：1582年'), dict(at=3, text='長篠の敗北だけが理由とは限らない')]))]),
 dict(key='check', title='通説を確かめる', chapter_title='通説を確かめる', scene=[
   dict(t='cols2', size=38, xm=940, xm2=980, left=dict(title='『信長公記』にある', title_at=1, items=[dict(at=4, text='鉄砲は五人の奉行のもとで、足軽に懸けさせた'), dict(at=9, text='この場面の鉄砲：写本で「千挺」と「三千挺」の違いがあるとされる'), dict(at=12, text='兵力：「三万ばかり」')]),
        right=dict(title='ない／後世の話', title_at=2, items=[dict(at=3, text='三列に入れ替えて撃つ説明（公開翻刻）'), dict(at=5, text='千挺ずつ交代で撃つ描写：後の軍記物語（甫庵『信長記』など）'), dict(at=6, text='ただし、何らかの交代射撃がなかったとまでは言い切れない')]))]),
 dict(key='end', title='分かること、決められないこと', chapter_title='結論：分かること、決められないこと', scene=[
   dict(t='cols2', size=38, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=1, text='『信長公記』：連合軍は馬防柵を設け、鉄砲を使って、武田軍の五つの攻撃を退けた'),
      dict(at=2, text='酒井忠次の別働隊が鳶ノ巣山を攻め、長篠城の包囲を崩した'),
      dict(at=3, text='武田軍が鉄砲で大きな損害を受けたこと')]),
     right=dict(title='決められないこと', title_at=4, items=[
      dict(at=4, text='「全滅」だったのか、騎馬隊だけの話か'),
      dict(at=6, text='三段撃ちがあったのか'), dict(at=7, text='鉄砲の数'), dict(at=8, text='柵の詳しい作り'),
      dict(at=9, text='兵力（史料や研究で幅がある）'), dict(at=10, text='陣や部隊の動きの細かい位置')]))]),
]

images = dict(
    area=dict(file='assets/nagashino/map_area.png'), wide=dict(file='assets/nagashino/map_wide.png'),
    p_katsuyori=dict(file='assets/portraits/katsuyori.jpg', crop=CROPS['katsuyori']), p_sakai=dict(file='assets/portraits/sakai_t.jpg', crop=CROPS['sakai_t']),
    p_baba=dict(file='assets/portraits/baba.jpg', crop=CROPS['baba']), p_yamagata=dict(file='assets/portraits/yamagata.jpg', crop=CROPS['yamagata']),
    p_okudaira=dict(file='assets/portraits/okudaira.jpg', crop=CROPS['okudaira']), p_nobunaga=dict(file='assets/portraits/nobunaga.jpg', crop=CROPS['nobunaga']),
    p_ieyasu=dict(file='assets/portraits/ieyasu.jpg', crop=CROPS['ieyasu']), p_nobutada=dict(file='assets/portraits/nobutada.jpg', crop=[0.25, 0.1, 0.7, 0.5]))

spec = dict(slug='nagashino', theme_dir='20261127_nagashino', pack='26_nagashino', header_sub='長篠の戦いを、地図の上で、『信長公記』で確かめる',
 images=images,
 bgm=[['intro', 'forces', 'piano36'], ['terrain', 'battle', 'piano12'], ['collapse', 'end', 'piano40']],
 chapters=chapters,
 desc=dict(title_main='長篠の戦いは、鉄砲の三段撃ちで決まったのか', title_no=1,
  titles=['長篠の戦い「三段撃ち」は本当か｜1575年、鉄砲1000挺と馬防柵で武田軍1万5000はなぜ崩れたか', '長篠の戦いを地図で解説 三段撃ちは本当？『信長公記』で確かめる', '長篠の戦い 武田軍はなぜ敗れた？ 地図で動きを追って史料で確かめる'],
  intro='天正3年（1575）旧暦5月21日、愛知県の設楽原で、織田信長・徳川家康の連合軍と、武田勝頼の軍がぶつかりました。長篠の戦いです。この動画では、地図の上で軍勢を動かしながら、戦いの流れを追います。そして、『信長公記』などの記録で、「武田の騎馬隊が鉄砲で全滅した」という通説を確かめます。分かることと決められないことを分けて、史料に帰属して述べます。',
  points=['『信長公記』巻八「三州長篠御合戦之事」によれば、信長は5月13日に出陣し、18日に設楽の郷の極楽寺山に陣を置きました。信長方の人数は「三万ばかり」、武田方は「一万五千ばかり」と書かれています(通説は連合軍約3万8千・武田約1万5千で、諸説があります)。', '家康・滝川一益らの陣の前には、馬を防ぐための柵が設けられました。5月20日の夜、酒井忠次を大将とする約4千(鉄砲500挺を含む)の別働隊が、乗本川を越えて鳶ノ巣山へ向かい、21日に攻め取って長篠城の兵と合流しました(『信長公記』)。', '設楽原では、鉄砲千挺ばかりが五人の奉行のもとで用いられ、武田方は五つに分かれて攻めましたが、鉄砲で大半を打ち倒されて引きました。戦いは日の出から未の刻(午後2時ごろ)まで続き、武田軍は鳳来寺の方へ退きました。討死は「一萬ばかり」と記されますが、実数は確定できません。', '『信長公記』の公開されている翻刻に、鉄砲を三列に入れ替えて撃つ説明はありません。千挺ずつ交代して撃つ描写は、後の軍記物語などに現れます。鉄砲の数は写本によって違いがあるとされます。三段撃ちの有無、鉄砲の数、兵力、柵の詳しい作り、陣の細かい位置は、史料だけでは断定できません。'],
  refs=['『信長公記』巻八(Wikisource・我自刊我書本の翻刻):https://ja.wikisource.org/wiki/信長公記/我自刊我書', '新城市「長篠・設楽原の戦い」:https://www.city.shinshiro.lg.jp/kanko/meisyo/nagashino-shitaragah.html', '国土地理院 地理院タイル(陰影起伏図・標準地図):https://maps.gsi.go.jp/development/ichiran.html'],
  credit_lines=['・図：自作（国土地理院タイル(陰影起伏図・標準地図)を加工して作成。現代の地形で、当時の川筋や道ではありません。陣・柵・別働隊の位置と経路は、史料と現地の案内をもとにした概略の推定です）', '・肖像：武田勝頼(高野山持明院蔵)、酒井忠次(先求院蔵)、馬場信春(恵林寺蔵)、奥平信昌(久昌院蔵)、織田信長・信忠・徳川家康：いずれも古い肖像画で、Wikimedia Commonsで公開されているパブリックドメインの画像です。山県昌景は、江戸時代後期の浮世絵(想像図)です。顔は後世の描写で、本人の実像とは限りません。', '・イラスト：ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面の再現ではありません)'],
  notes=['地図上の軍勢の動きは、『信長公記』の記述をもとにした概略の図で、実際の経路・時刻ではありません。武田方の五つの攻撃は、『信長公記』の叙述の順に紹介したもので、一隊ずつ往復したわけではありません。', '「正用軒＝武田信廉」「典厩＝武田信豊」は、一般的な同定に基づく説明です。', '旧暦5月21日を今の暦で7月9日とするのは、新城市の説明です(ユリウス暦では6月29日にあたります)。', '『信長公記』巻八の本文(Wikisource)で、鉄砲千挺ほど・五人の奉行・兵力三万・五つの攻撃・討死した武将の名を確認しました。信忠の陣の山名「新御堂山」は『信長公記』の表記ですが、読みを確認できなかったため、ナレーションでは読み上げていません。'],
  tags='長篠の戦い, 設楽原, 織田信長, 徳川家康, 武田勝頼, 三段撃ち, 信長公記, 戦国時代, 戦況解説, 検証',
  checks=['『信長公記』巻八の影印・別の翻刻で、数字・人名・時刻を確認する(Wikisourceの翻刻は確認済み。docs/themes/20261127_nagashino/08_fact_check.md)', '設楽原歴史資料館「設楽原布陣図」、新城市「酒井忠次の大作戦」の原ページを確認する', '正用軒＝武田信廉、典厩＝武田信豊、馬場信春・山県昌景が信玄以来の重臣であることを確認する', '鳶ノ巣山砦・信長/家康の陣・馬防柵の位置を、現地の案内・国土地理院の史跡情報で確認する']),
 thumb=dict(bg='assets/nagashino/map_area.png', lines=[['長篠の戦い', 120, 'white'], ['三段撃ちは', 96, 'white'], ['本当？', 130, 'gold']], sub='地図と『信長公記』で確かめる', shade_col=[10, 14, 28], accent=[238, 96, 84], bar_col=[238, 96, 84], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and not o.get('title') and o['box'][3] - o['box'][1] <= 70: o['size'] = min(o.get('size', 40), 40)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


_fit(spec)
(R / 'data' / 'nagashino_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
