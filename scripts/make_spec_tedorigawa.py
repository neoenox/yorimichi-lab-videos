"""Writes data/tedorigawa_spec.json（手取川の戦い。戦況解説シリーズ9本目）。台本：docs/themes/20270109_tedorigawa/09_script_v2.md
文の番号は章内の0始まりの『行の番号』で書き、下で文の番号に直す。地図の座標は tedorigawa_maps.norm()。
位置は、国土地理院住所検索（七尾・松任・湊・津幡・小松・丸岡・安土）による。川筋・軍の動きは概略の推定（画面に『推定』と明記）。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import tedorigawa_maps as MM
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]
BOX = [60, 250, 1860, 850]
BLUE = (90, 150, 255); RED = (238, 96, 84); GOLD = (239, 201, 118); WATER = (130, 195, 255)
NC = json.loads((R / 'data' / 'nagashino_crops.json').read_text(encoding='utf8'))
ZC = json.loads((R / 'data' / 'shizugatake_crops.json').read_text(encoding='utf8'))


def A(lon, lat): return list(MM.norm(lon, lat, 'area'))
def W(lon, lat): return list(MM.norm(lon, lat, 'wide'))


NANAO = (136.9672, 37.0431); MATTO = (136.513, 36.5135); MINATO = (136.4756, 36.4753); KOMATSU = (136.448, 36.398); TSUBATA = (136.7288, 36.6688)
KASUGA = (138.2223, 37.1436); AZUCHI = (136.135, 35.155); SUENO = (136.80, 36.78)
_RIVER_PX = [(100, 388), (150, 404), (210, 410), (268, 412), (292, 428)]
RIVER_PTS = [(136.40 + x / 787 * 0.62, 36.72 - y / 600 * 0.38) for x, y in _RIVER_PX]


def pn(text, at, until=None, size=40, hi=True, col=None):
    d = dict(t='panel', box=TOP, text=text, at=at, size=size, hi=hi)
    if until is not None: d['until'] = until
    if col: d['col'] = col
    return d


def unit(**k): return k
def NOTE_POS(at=0, txt='※位置は概略の推定'): return dict(xy=[0.02, 0.04], label=txt, kind='spot', at=at, side='r', col=GOLD, lsize=28)
def amap(img='area', **k): return dict(t='anim', name='battle_map', img=img, box=BOX, at=0, **k)
def RIVER(at=0): return dict(pts=[A(*p) for p in RIVER_PTS], label='手取川（現代の川筋の概略）', at=at, col=WATER, dash=False, lab=[0.30, 0.78])


NOTE_IMG = 'イメージ（生成画像）。実際の場面の再現ではありません'
ART_BOX = [60, 170, 1860, 850]
EST = '※位置・経路は概略の推定'

chapters = [
 dict(key='intro', title='手取川の戦い', chapter_title='導入：手取川の戦い', opener='手取川の戦い', opener_until=2, scene=[
   dict(t='art', name='flood', box=ART_BOX, at=0, dim=0.8, dir=1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.5),
   pn('手取川の戦いは、織田軍の大敗だったのか', 0, 1, 40, col='gold'), pn('天正5年9/23（ユリウス暦1577年11月3日）', 1, 2, 40),
   pn('グレゴリオ暦では、11月13日', 2, 3, 42), pn('加賀・手取川：柴田勝家の織田軍 対 上杉謙信の軍（といわれる）', 3, 4, 34),
   pn('謙信に追撃され、川で多くが溺れた（通説）', 4, 5, 40, col='gold'), pn('同時代の記録は、この戦いを、どう書いているのか', 5, 6, 38), pn('地図の上で追い、記録を確かめる', 6, None, 42)]),
 dict(key='nanao', title='七尾城', chapter_title='七尾城', scene=[
   pn('能登の七尾城は、守護・畠山氏の城', 0, 1, 40), pn('天正4年　上杉謙信が、2万余の軍で能登に攻め込む（説）', 1, 2, 36),
   pn('七尾城は堅く、戦いは翌年に持ち越される（説）', 2, 3, 38), pn('重臣の長続連らが、実権を握っていた（説）', 3, 4, 38),
   pn('城内に、百姓や町人までが収容されていた（説）', 4, 5, 38), pn('疫病が広まり、幼い城主も病死した、という解説も（説）', 5, 6, 36),
   pn('天正5年閏7月　謙信が、再び能登へ（説）', 6, 7, 40), pn('長続連が、信長に救援を求めた（説）', 7, 8, 40), pn('信長も、謙信の勢力拡大を望まず、援軍を決めた（説）', 8, None, 36),
   amap('wide', places=[NOTE_POS(0, '※位置は概略の推定'), dict(xy=W(*NANAO), label='七尾城', kind='castle', at=0, side='l', col=RED, lsize=26),
                        ],
        units=[unit(label='上杉謙信', sub='能登へ', col=RED, portrait='p_kenshin', pts=[W(136.62, 36.60), W(*NANAO)], legs=[[1, 3]], at=1, head=24, lab_off=(-36, 10), lsize=22, dashed=True)])]),
 dict(key='forces', title='顔ぶれと、数', chapter_title='顔ぶれと、数', scene=[
   dict(t='art', name='docs', box=ART_BOX, at=0, dim=0.8, dir=-1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.66),
   dict(t='cols2', size=31, xm=940, xm2=980, until=4, left=dict(title='織田軍（『信長公記』）', title_at=0, items=[
        dict(at=0, text='大将：柴田勝家'), dict(at=1, text='滝川・羽柴・惟住・斎藤・氏家・伊賀・稲葉・不破・前田・佐々・原・金森・若狭衆'), dict(at=2, text='惟住＝のちの丹羽長秀。前田＝利家、佐々＝成政')]),
        right=dict(title='数', title_at=3, items=[dict(at=3, text='『信長公記』は、軍勢の数を書いていない')])),
   dict(t='cols2', size=30, xm=940, xm2=980, at=4, left=dict(title='解説にある数（出典未確認）', title_at=4, items=[
        dict(at=4, text='織田軍：四万（説）'), dict(at=6, text='追撃した上杉軍：八千（説）')]),
        right=dict(title='分からないこと', title_at=7, items=[dict(at=7, text='確かな数は、分かっていない')]))]),
 dict(key='terrain', title='地形', chapter_title='地形', scene=[
   pn('手取川は、白山から日本海へ流れ込む川', 0, 1, 40), pn('川の北に松任、南に小松', 1, 2, 42), pn('河口の近くに、湊', 2, 3, 42),
   pn('七尾城は、能登半島の付け根に近い山の上', 3, 4, 38), pn('加賀から能登へ向かうには、津幡を通る', 4, 5, 38),
   pn('秋の手取川は、増水すると、流れが速い', 5, 6, 38), pn('画面の地形は現代のもの。城や川筋の位置は概略の推定', 6, None, 36),
   amap(places=[NOTE_POS(0, '※現代の地形。川筋・位置は概略の推定'),
                dict(xy=A(*MATTO), label='松任', kind='spot', at=1, side='r', col=GOLD, lsize=24),
                dict(xy=A(*KOMATSU), label='小松', kind='spot', at=1, side='r', col=GOLD, lsize=24),
                dict(xy=A(*MINATO), label='湊（河口）', kind='spot', at=2, side='l', col=GOLD, lsize=22),
                dict(xy=A(*TSUBATA), label='津幡', kind='spot', at=4, side='r', col=GOLD, lsize=24)], lines=[RIVER(0)])]),
 dict(key='north', title='織田軍の北上', chapter_title='織田軍の北上', scene=[
   pn('『信長公記』は、こう書く', 0, 1, 42, col='gold'), pn('8/8　柴田勝家を大将として、北国へ軍勢が出された', 1, 2, 38, col='gold'),
   pn('加賀へ乱入し、添川と手取川を越えた', 2, 3, 40, col='gold'), pn('小松村・本折村・阿多賀・富樫など、所々を焼き払い、在陣した', 3, 4, 36, col='gold'),
   pn('9/11　前衛が津幡あたりまで進んだ、という解説（説）', 4, 5, 38), pn('謙信の別働隊が破った、という紹介もあるが、根拠は確認できない（説）', 5, None, 34),
   amap(places=[NOTE_POS(0, EST + '。記録による大まかな動き'), dict(xy=A(*KOMATSU), label='小松村・本折村', kind='spot', at=3, side='r', col=GOLD, lsize=22),
                dict(xy=A(*TSUBATA), label='津幡', kind='spot', at=4, side='r', col=GOLD, lsize=24)], lines=[RIVER(0)],
        units=[unit(label='柴田勝家', sub='織田軍', col=BLUE, portrait='p_shibata', pts=[A(KOMATSU[0] + 0.02, KOMATSU[1] - 0.05), A(MINATO[0] + 0.02, MINATO[1] - 0.01), A(MATTO[0] + 0.02, MATTO[1] + 0.01), A(*TSUBATA)], legs=[[1, 4], [4, 5]], at=0, head=26, lab_off=(36, 10), lsize=22, dashed=True)])]),
 dict(key='fall', title='七尾城の落城', chapter_title='七尾城の落城', scene=[
   pn('その間に、七尾城は、落ちていた', 0, 1, 40), pn('9/15　七尾城の中で、上杉に味方する家臣が、内応（説）', 1, 2, 36),
   pn('長続連ら、長一族のほとんどが殺された（説）', 2, 3, 38), pn('三男の長連龍は、生き延びた（説）', 3, 4, 40), pn('七尾城は、落ちた（説）', 4, 5, 42),
   pn('織田軍は、この落城を知らなかった、といわれる（説）', 5, 6, 38), pn('9/17　末森城も、上杉方に落ちたとされる（説）', 6, None, 38),
   amap('wide', places=[NOTE_POS(0, '※位置は概略の推定'), dict(xy=W(*NANAO), label='七尾城', kind='castle', at=0, side='l', col=RED, lsize=26), dict(xy=W(*TSUBATA), label='津幡', kind='spot', at=0, side='r', col=GOLD, lsize=22), dict(xy=W(*SUENO), label='末森城（推定）', kind='castle', at=6, side='r', col=RED, lsize=22)])]),
 dict(key='river', title='手取川', chapter_title='手取川', scene=[
   pn('織田軍は、手取川を渡った（『信長公記』）', 0, 1, 40, col='gold'), pn('謙信は、七尾城を出て、松任城に入った、といわれる（説）', 1, 2, 36),
   pn('勝家は、全軍が渡り終えて、はじめて七尾城の落城を知った、といわれる（説）', 2, 3, 32), pn('勝家は、すぐに撤退を命じた（説）', 3, 4, 40),
   pn('途中、9/23の夜、謙信の軍が追撃した、といわれる（説）', 4, 5, 36), pn('謙信の書状の写しには、こうある（『別本歴代古案』）', 5, 6, 36, col='gold'),
   pn('23日の夜、織田軍が引き、これを追って、千余人を討ち捕った', 6, 7, 36, col='gold'), pn('洪水で、人馬が流された、とも書かれると紹介される', 7, 8, 36),
   pn('『信長公記』には、この追撃の話はない', 8, None, 38, col='gold'),
   amap(places=[NOTE_POS(0, EST + '。軍記・書状による大まかな動き'), dict(xy=A(*MATTO), label='松任城', kind='castle', at=1, side='r', col=RED, lsize=24)], lines=[RIVER(0)],
        units=[unit(label='上杉謙信', col=RED, portrait='p_kenshin', pts=[A(MATTO[0] + 0.08, MATTO[1] + 0.12), A(*MATTO), A(MINATO[0] + 0.06, MINATO[1] + 0.0)], legs=[[1, 2], [4, 5]], at=1, head=24, lab_off=(36, -20), lsize=22, dashed=True),
               unit(label='織田軍', sub='撤退', col=BLUE, portrait='p_shibata', pts=[A(MATTO[0] + 0.05, MATTO[1] - 0.02), A(KOMATSU[0] + 0.05, KOMATSU[1] - 0.02)], legs=[[3, 5]], at=3, head=24, lab_off=(-36, 10), lsize=22, dashed=True)])]),
 dict(key='hideyoshi', title='秀吉の離脱', chapter_title='秀吉の離脱', scene=[
   dict(t='art', name='docs', box=ART_BOX, at=0, dim=0.8, dir=1, note='イメージ（生成画像）。実際の資料の再現ではありません'), dict(t='shade', box=ART_BOX, at=0, alpha=0.7),
   pn('『信長公記』が書いているのは、秀吉のこと', 0, 1, 40, col='gold'), pn('「羽柴筑前、御届をも申し上げず、帰陣仕り候」', 1, 2, 38, col='gold'),
   pn('秀吉は、断りなく陣を離れて、帰った', 2, 3, 40), pn('信長は、「曲事（けしからん）」と激怒した', 3, 4, 40),
   pn('秀吉は、迷惑をした（困った）と書かれる', 4, 5, 40), pn('離脱の理由は、『信長公記』にはない', 5, 6, 40, col='gold'),
   pn('『武功夜話』などは、勝家との不仲、松永久秀の動きを理由に挙げる（軍記）', 6, 7, 34), pn('ただし、その書物は信頼性に議論がある（説）', 7, None, 38)]),
 dict(key='records', title='記録が、分かれる', chapter_title='記録が、分かれる', scene=[
   dict(t='art', name='docs', box=ART_BOX, at=0, dim=0.8, dir=-1, note='イメージ（生成画像）。実際の資料の再現ではありません'), dict(t='shade', box=ART_BOX, at=0, alpha=0.66),
   dict(t='cols2', size=30, xm=940, xm2=980, until=6, left=dict(title='『信長公記』', title_at=0, items=[
        dict(at=1, text='出陣と秀吉の離脱を書くが、合戦は書かない')]),
        right=dict(title='謙信の書状の写し（9/29付とされる）', title_at=2, items=[dict(at=3, text='23日の夜の追撃と、千余人の討ち取りを報告'), dict(at=4, text='ただし、原本ではなく写し'), dict(at=5, text='日付の違う写本もある。本文と日付が合わないものも')])),
   dict(t='cols2', size=29, xm=940, xm2=980, at=6, left=dict(title='注意', title_at=6, items=[
        dict(at=6, text='書状は、勝った側の自己申告。数をそのまま事実とはいえない')]),
        right=dict(title='ほかの記録', title_at=7, items=[dict(at=7, text='『福井県史』：9/23の夜戦で、織田軍が大敗した'), dict(at=8, text='『長家家譜』：秀吉は、戦わずに帰陣した（と紹介される）'), dict(at=9, text='下間頼廉の書状：夜討ちの記述。年不詳の5/25付で、9月とみてよいか議論がある')]))]),
 dict(key='after', title='その後', chapter_title='その後', scene=[
   pn('9/26　謙信は、七尾城に戻った（説）', 0, 1, 40), pn('次いで、能登をほぼ平定した（説）', 1, 2, 40), pn('10/3　柴田勝家らは、加賀から帰還した（説）', 2, 3, 38),
   pn('「上杉に逢うては織田も手取川 はねる謙信 逃げるとぶ長」', 3, 4, 36, col='gold'), pn('落首が伝わる。ただし、当時の反応を示す同時代の記録は確認できない（説）', 4, 5, 32),
   pn('天正6年　謙信は、関東への出陣を準備した（説）', 5, 6, 38), pn('その春に、謙信は亡くなる（説）', 6, 7, 40), pn('大局では、織田方が、一度に崩れたわけではない', 7, None, 38),
   amap('wide', places=[NOTE_POS(0, '※位置は概略の推定'), dict(xy=W(*NANAO), label='七尾城', kind='castle', at=0, side='l', col=RED, lsize=26)],
        units=[unit(label='上杉謙信', sub='七尾城へ', col=RED, portrait='p_kenshin', pts=[W(MATTO[0], MATTO[1]), W(*NANAO)], legs=[[0, 1]], at=0, head=24, lab_off=(36, 10), lsize=22, dashed=True)])]),
 dict(key='source', title='史料を、分けて見る', chapter_title='史料を、分けて見る', scene=[
   dict(t='art', name='docs', box=ART_BOX, at=0, dim=0.8, dir=1, note='イメージ（生成画像）。実際の資料の再現ではありません'), dict(t='shade', box=ART_BOX, at=0, alpha=0.66),
   dict(t='cols2', size=30, xm=940, xm2=980, until=3, left=dict(title='同時代に近い記録', title_at=0, items=[
        dict(at=0, text='『信長公記』と、謙信の書状の写し')]),
        right=dict(title='『信長公記』', title_at=1, items=[dict(at=1, text='信長の側の記録。合戦を書いていない'), dict(at=2, text='負け戦を書かなかったのか。小さな戦いと見たのか。決められない')])),
   dict(t='cols2', size=30, xm=940, xm2=980, at=3, left=dict(title='謙信の書状', title_at=3, items=[
        dict(at=3, text='上杉の側の記録。戦果を大きく書くことがありうる')]),
        right=dict(title='後の書物・県史', title_at=4, items=[dict(at=4, text='「溺れた」「大敗」の話は、後の書物や県史にも見られる（説）'), dict(at=5, text='分けて見るのが、確かめる第一歩')]))]),
 dict(key='summary', title='分かること、決められないこと', chapter_title='分かること、決められないこと', scene=[
   dict(t='art', name='castle', box=ART_BOX, at=0, dim=0.8, dir=-1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.62),
   dict(t='cols2', size=32, xm=940, xm2=980, until=6, left=dict(title='分かること', title_at=0, items=[
        dict(at=0, text='天正5年、織田軍が加賀へ入り、手取川を越えた'), dict(at=1, text='秀吉が断りなく帰陣し、信長が激怒した'), dict(at=2, text='9/23の夜、織田軍の撤退を謙信が追撃した、と書状の写しは伝える')]),
        right=dict(title='決められないこと', title_at=3, items=[
        dict(at=3, text='織田軍が、どれほど大敗したのか'), dict(at=4, text='手取川で、多くが溺れたのか'), dict(at=5, text='両軍の実際の数と、死者の数')])),
   dict(t='cols2', size=33, xm=940, xm2=980, at=6, left=dict(title='見方', title_at=6, items=[
        dict(at=6, text='同時代の記録と、後の話を、分けて見ると、見え方が変わる')]), right=dict(title='', title_at=6, items=[]))]),
]

images = dict(
    area=dict(file='assets/tedorigawa/map_area.png'), wide=dict(file='assets/tedorigawa/map_wide.png'),
    p_kenshin=dict(file='assets/portraits/kenshin.jpg', crop=[0.36, 0.23, 0.62, 0.40]), p_shibata=dict(file='assets/portraits/shibata.jpg', crop=ZC['shibata']),
    flood=dict(file='assets/tedorigawa/art_flood.png'), docs=dict(file='assets/tedorigawa/art_docs.png'), castle=dict(file='assets/tedorigawa/art_castle.png'))


def _line_to_sentence_starts():
    import re
    t = (R / 'docs' / 'themes' / '20270109_tedorigawa' / '09_script_v2.md').read_text(encoding='utf8')
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

T1 = '【手取川は大敗だった？】手取川の戦い 謙信の書状と『信長公記』で検証｜地図で解説'
spec = dict(slug='tedorigawa', theme_dir='20270109_tedorigawa', pack='36_tedorigawa', header_sub='手取川の戦いを、地図の上で、『信長公記』と謙信の書状、後世の話に分けて確かめる',
 images=images,
 bgm=[['intro', 'terrain', 'piano36'], ['north', 'hideyoshi', 'piano12'], ['after', 'summary', 'piano40']],
 chapters=chapters,
 desc=dict(title_main=T1, title_no=1,
  titles=[T1, '手取川の戦いを地図で解説 織田軍は謙信に大敗し川で溺れた？同時代の記録を確かめる', '手取川の戦い 上杉謙信の書状の写しと『信長公記』、後世の話を分けて確かめる'],
  intro='天正5年9月23日（ユリウス暦1577年11月3日、グレゴリオ暦では11月13日）、加賀の手取川で、柴田勝家の織田軍と上杉謙信の軍がぶつかった、といわれます。手取川の戦いです。織田軍は大敗し、増水した川で多くが溺れた、という話が有名です。この動画では、地図の上で軍勢の動きを追いながら、『信長公記』は何を書いているのか、謙信の書状の写しには何があるのか、後の書物は何を足したのかを、分けて確かめます。分かることと決められないことを分けて、最後にまとめます。',
  points=['『信長公記』が書くこと（巻十）：8/8に柴田勝家を大将として北国へ軍勢が出され、滝川・羽柴・惟住・斎藤・氏家・伊賀・稲葉・不破・前田・佐々・原・金森・若狭衆の名が挙がる。加賀へ乱入し、添川・手取川を越え、小松村・本折村・阿多賀・富樫を焼き払って在陣した。羽柴筑前が届けも出さずに帰陣したことを信長は曲事として逆鱗に触れ、羽柴は迷惑した、とある。上杉謙信の名も、合戦も、敗北も書かれていません。(Wikisourceの翻刻で原文を確認)',
          '謙信の書状の写し：『別本歴代古案』巻五所収の9月29日付とされる書状写には、23日夜の織田軍の撤退・追撃、千余人の討ち取り、洪水による人馬の流失が書かれると紹介されています。ただし原本ではなく写しで、日付の違う写本もあり、勝った側の自己申告のため、数をそのまま事実とはいえません。『福井県史』は9/23の夜戦で織田軍が大敗したと書くと紹介されます(二次資料を通した紹介。原典は未確認)。',
          '『長家家譜』は、七尾城の落城の報に接した秀吉が戦わずに帰陣したと書くと紹介されます。下間頼廉の書状には夜討ちの記述がありますが、年不詳の5月25日付で、9月とみてよいかは議論があります。秀吉の離脱の理由を、勝家との不仲や松永久秀の動きとする『武功夜話』は、信頼性に議論がある書物です。',
          '数字：織田軍四万、追撃した上杉軍八千という解説がありますが、出典の書物は確かめられていません。『信長公記』は軍勢の数を書いていません。「上杉に逢うては織田も手取川 はねる謙信 逃げるとぶ長」という落首が伝わりますが、当時の反応を示す同時代の記録は確認できていません。',
          '地図上の軍勢の動きは、記録にもとづく大まかな図で、実際の経路・順序ではありません。当時の川筋は現代と違うとされます。'],
  refs=['太田牛一『信長公記』巻十「柴田北国相働之事」（Wikisource）:https://ja.wikisource.org/wiki/信長公記/我自刊我書', 'Wikipedia「手取川の戦い」(研究者の説と出典の整理)', '『福井県史』通史編3', '国立天文台 暦計算室「日本の暦日データベース」', '国土地理院 地理院タイル:https://maps.gsi.go.jp/development/ichiran.html'],
  credit_lines=['・図：自作（国土地理院タイル(陰影起伏図・標準地図)を加工して作成。現代の地形で、当時の川筋・海岸・道ではありません。城・川筋・経路の位置は、案内をもとにした概略の推定です）',
                '・肖像：上杉謙信・柴田勝家：古い肖像画。Wikimedia Commonsで公開されているパブリックドメインの画像です。',
                '・イラスト：ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['地図上の軍勢の動きは、記録の描写と推定にもとづく概略の図で、実際の経路・時刻ではありません。', '『信長公記』は、Wikisourceの翻刻（旧字版）で該当部分を確認しました。謙信の書状の写し、『福井県史』『長家家譜』『武功夜話』、下間頼廉の書状、研究者の説、七尾城の経過は、日本語版Wikipediaや研究者の解説記事など二次資料を通して確認したもので、原典は直接確認していません。'],
  tags='手取川の戦い, 上杉謙信, 柴田勝家, 織田信長, 信長公記, 戦国時代, 戦況解説, 検証, 七尾城, 羽柴秀吉',
  checks=['『別本歴代古案』『歴代古案』の謙信書状の原文・写本の異同', '『福井県史』の記述', '『大日本史料』『史料綜覧』の該当条', '『長家家譜』の記述', '下間頼廉書状の年次', '国立天文台の換算ツールで、1577年11月3日（ユリウス暦）＝11月13日（グレゴリオ暦）の再確認']),
 thumb=dict(bg='assets/tedorigawa/thumb_art.png', lines=[['手取川の戦い', 112, 'white'], ['織田軍は本当に', 96, 'white'], ['大敗した？', 112, 'gold']], sub='謙信の書状と『信長公記』で確かめる', shade_col=[10, 14, 28], accent=[238, 96, 84], bar_col=[238, 96, 84], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and not o.get('title') and o['box'][3] - o['box'][1] <= 70: o['size'] = min(o.get('size', 40), 40)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


_fit(spec)
(R / 'data' / 'tedorigawa_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
