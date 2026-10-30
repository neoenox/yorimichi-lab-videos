"""Writes data/tottori_spec.json（鳥取城の戦い。戦況解説シリーズ8本目）。台本：docs/themes/20270102_tottori/09_script_v2.md
文の番号は章内の0始まりの『行の番号』で書き、下で文の番号に直す。地図の座標は tottori_maps.norm()。
位置は、国土地理院住所検索（久松山・太閤ヶ平・丸山町・賀露町・羽衣石城）による。陣・出城・川筋は概略の推定（画面に『推定』と明記）。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import tottori_maps as MM
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]
BOX = [60, 250, 1860, 850]
BLUE = (90, 150, 255); RED = (238, 96, 84); GOLD = (239, 201, 118); WATER = (130, 195, 255)
NC = json.loads((R / 'data' / 'nagashino_crops.json').read_text(encoding='utf8'))
YC = json.loads((R / 'data' / 'yamazaki_crops.json').read_text(encoding='utf8'))


def A(lon, lat): return list(MM.norm(lon, lat, 'area'))
def W(lon, lat): return list(MM.norm(lon, lat, 'wide'))


CASTLE = (134.2407, 35.5103); TAIKO = (134.2562, 35.5109); MARUYAMA = (134.2248, 35.518); KARO = (134.1669, 35.5312); HOUKI = (133.8952, 35.4374)


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
 dict(key='intro', title='鳥取城の戦い', chapter_title='導入：鳥取城の戦い', opener='鳥取城の戦い', opener_until=2, scene=[
   dict(t='art', name='mountain', box=ART_BOX, at=0, dim=0.8, dir=1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.5),
   pn('「鳥取の渇え殺し」は、秀吉の計画どおりだったのか', 0, 1, 38, col='gold'), pn('天正9年10/25（ユリウス暦1581年11月21日）', 1, 2, 40),
   pn('グレゴリオ暦では、12月1日。因幡の鳥取城が開城', 2, 3, 38), pn('攻めた羽柴秀吉 対 守った毛利方の吉川経家', 3, 4, 40),
   pn('秀吉は、先に米を買い占めて、城を飢えさせた（通説）', 4, 5, 38, col='gold'), pn('住民を、城に追い込んだ（通説）', 5, 6, 40, col='gold'),
   pn('同時代の記録は、この戦いを、どう書いているのか', 6, 7, 38), pn('地図の上で追い、記録を確かめる', 7, None, 42)]),
 dict(key='background', title='背景', chapter_title='背景', scene=[
   pn('鳥取城は、因幡の山名氏の城（説）', 0, 1, 40), pn('天正8年　城主の山名豊国は、秀吉に従った（説）', 1, 2, 38),
   pn('けれども、家臣たちは毛利方に傾く（説）', 2, 3, 40), pn('9月　豊国は、家臣に城を追われた（説）', 3, 4, 40),
   pn('家臣たちは、毛利一族の吉川経家を城に迎えた（説）', 4, 5, 38), pn('天正9年3月　経家が鳥取城に入城（説）', 5, 6, 40),
   pn('入城した時点で、すでに兵糧が足りない、と書き送った（説）', 6, 7, 36, col='gold'), pn('因幡・伯耆は、戦いが続き、米が乏しかった（説）', 7, 8, 38),
   pn('前年にも、秀吉は因幡と伯耆の境まで攻め入った（『信長公記』）', 8, 9, 36), pn('国の端の城主たちは、人質を出して降参（『信長公記』）', 9, 10, 36),
   pn('信長は、秀吉の働きを褒めた（『信長公記』）', 10, None, 38),
   amap('wide', places=[NOTE_POS(0, '※位置は概略の推定'), dict(xy=W(*CASTLE), label='鳥取城', kind='castle', at=0, side='r', col=RED, lsize=26),
                        dict(xy=W(*HOUKI), label='羽衣石城', kind='castle', at=9, side='r', col=BLUE, lsize=22)],
        units=[unit(label='吉川経家', sub='毛利方', col=RED, pts=[W(CASTLE[0] - 0.1, CASTLE[1] - 0.12), W(*CASTLE)], legs=[[4, 6]], at=4, head=22, lab_off=(36, 10), lsize=20, dashed=True)])]),
 dict(key='forces', title='顔ぶれと、数', chapter_title='顔ぶれと、数', scene=[
   dict(t='art', name='docs', box=ART_BOX, at=0, dim=0.8, dir=-1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.66),
   dict(t='cols2', size=31, xm=940, xm2=980, until=3, left=dict(title='攻める側', title_at=0, items=[
        dict(at=0, text='羽柴秀吉。弟の秀長らも加わった（説）'), dict(at=1, text='『信長公記』：秀吉の軍は、二万余騎')]),
        right=dict(title='守る側', title_at=2, items=[dict(at=2, text='吉川経家（公記は「橘川式部少輔」と書く）')])),
   dict(t='cols2', size=30, xm=940, xm2=980, at=3, left=dict(title='降伏の場面で、公記が名を挙げる大将', title_at=3, items=[
        dict(at=3, text='吉川式部少輔・森下道祐・日本介の三人')]),
        right=dict(title='分からないこと', title_at=4, items=[dict(at=4, text='降伏した人は、三人だけではなかった、という解説も（説）'), dict(at=5, text='城の兵の数は、公記にない'), dict(at=6, text='籠城した人の数は、分かっていない')]))]),
 dict(key='terrain', title='地形と、城', chapter_title='地形と、城', scene=[
   pn('鳥取城は、四方から離れた険しい山城（『信長公記』）', 0, 1, 38, col='gold'), pn('因幡の国は、北から西が海（『信長公記』）', 1, 2, 40),
   pn('城の西を、舟で渡る大きな川が流れていた（『信長公記』）', 2, 3, 38), pn('川のそばに「つなぎの出城」。海の口にも要害（『信長公記』）', 3, 4, 36),
   pn('毛利の味方を引き入れるためのもの（『信長公記』）', 4, 5, 38), pn('城の東、七、八町の所に、高い山', 5, 6, 40),
   pn('一町は約109メートル', 6, 7, 42), pn('秀吉は、この山に登り、陣を構えた（『信長公記』）', 7, 8, 38, col='gold'),
   pn('当時の川筋は、現代とは違っていた（説）', 8, 9, 40), pn('画面の地形は現代のもの。川・城・陣の位置は概略の推定', 9, None, 36),
   amap(places=[NOTE_POS(0, '※現代の地形。城・陣の位置は概略の推定'),
                dict(xy=A(*CASTLE), label='鳥取城（久松山）', kind='castle', at=0, side='l', col=RED, lsize=26),
                dict(xy=A(*MARUYAMA), label='丸山城（つなぎの出城）', kind='castle', at=3, side='l', col=RED, lsize=22),
                dict(xy=A(*KARO), label='海の口（賀露）', kind='spot', at=3, side='r', col=RED, lsize=22),
                dict(xy=A(*TAIKO), label='太閤ヶ平（秀吉の本陣）', kind='castle', at=7, side='r', col=BLUE, lsize=24)],
        units=[unit(label='羽柴秀吉', col=BLUE, portrait='p_hideyoshi', pts=[A(TAIKO[0] + 0.02, TAIKO[1] + 0.02), A(*TAIKO)], legs=[[7, 8]], at=7, head=24, lab_off=(36, -10), lsize=22, dashed=True)])]),
 dict(key='siege', title='包囲網', chapter_title='包囲網', scene=[
   pn('『信長公記』は、秀吉の包囲の様子を、詳しく書く', 0, 1, 38, col='gold'), pn('まず、二つの出城の間を、断ち切った', 1, 2, 40),
   pn('鹿垣を結いまわし、堀を掘っては柵、また掘っては塀', 2, 3, 38), pn('土の塀を高く築き、二重三重の見張りの櫓を上げた', 3, 4, 38),
   pn('塀は、前後二里にわたった', 4, 5, 40), pn('その内側に、陣屋を町屋のように作り、夜は篝火', 5, 6, 38),
   pn('海には警固の舟。浦々を焼き払った', 6, 7, 40), pn('丹後・但馬から、海上で兵糧を届けさせた', 7, 8, 38),
   pn('何年でも在陣できる、用意をした', 8, 9, 40), pn('毛利が救援に来れば、二万の軍勢で討ち果たす備えも堅固', 9, 10, 36),
   pn('鹿垣は、鹿や猪を防ぐ柵。ここでは敵を閉じ込める柵', 10, None, 38),
   amap(places=[NOTE_POS(0, EST), dict(xy=A(*CASTLE), label='鳥取城', kind='castle', at=0, side='l', col=RED, lsize=26),
                dict(xy=A(*MARUYAMA), label='丸山城', kind='castle', at=1, side='l', col=RED, lsize=22),
                dict(xy=A(*TAIKO), label='太閤ヶ平', kind='castle', at=0, side='r', col=BLUE, lsize=24)],
        lines=[dict(pts=[A(CASTLE[0] - 0.025, CASTLE[1] + 0.012), A(CASTLE[0] - 0.02, CASTLE[1] - 0.012), A(CASTLE[0] + 0.005, CASTLE[1] - 0.02), A(CASTLE[0] + 0.03, CASTLE[1] - 0.008), A(CASTLE[0] + 0.03, CASTLE[1] + 0.014), A(CASTLE[0] + 0.005, CASTLE[1] + 0.022), A(CASTLE[0] - 0.025, CASTLE[1] + 0.012)],
                    label='包囲の柵（模式）', at=1, col=BLUE, dash=True, lab=[0.55, 0.25])],
        units=[unit(label='警固の舟', col=BLUE, pts=[A(KARO[0] - 0.02, KARO[1] + 0.012)], at=6, head=20, lab_off=(-36, -10), lsize=20)])]),
 dict(key='claims', title='通説と、記録', chapter_title='通説と、記録', scene=[
   dict(t='art', name='docs', box=ART_BOX, at=0, dim=0.8, dir=1, note='イメージ（生成画像）。実際の資料の再現ではありません'), dict(t='shade', box=ART_BOX, at=0, alpha=0.66),
   dict(t='cols2', size=30, xm=940, xm2=980, until=5, left=dict(title='通説①：米の買い占め', title_at=1, items=[
        dict(at=1, text='秀吉は、城の周りの米を買い占めた（通説）'), dict(at=2, text='後世の書物『陰徳太平記』などが書く、と解説される（説）'), dict(at=3, text='『信長公記』には、ない'), dict(at=4, text='史実かどうか、留保が付けられている（説）')]),
        right=dict(title='', title_at=1, items=[])),
   dict(t='cols2', size=29, xm=940, xm2=980, at=5, left=dict(title='通説②：住民を追い込んだ', title_at=5, items=[
        dict(at=5, text='秀吉は、住民を城に追い込んだ（通説）。二千人という数もある（説）')]),
        right=dict(title='『信長公記』', title_at=7, items=[dict(at=7, text='鳥取の一郡の男女が、ことごとく城中へ逃げ入って、立てこもった'), dict(at=9, text='下々の百姓は、長陣の覚悟がなく、すぐ飢えた'), dict(at=10, text='「追い込んだ」と「逃げ込んだ」は、両立しうる')]))]),
 dict(key='famine', title='飢え', chapter_title='飢え', scene=[
   dict(t='art', name='mountain', box=ART_BOX, at=0, dim=0.8, dir=-1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.7),
   pn('『信長公記』は、飢えの様子を書く', 0, 1, 40, col='gold'), pn('はじめは、五日に一度、三日に一度、鐘をついた', 1, 2, 38),
   pn('鐘が鳴ると、雑兵が柵の際に出て、木や草の葉を取った', 2, 3, 36), pn('中でも、稲の株が、上等の食べ物', 3, 4, 40),
   pn('それも尽きると、牛や馬を食べた', 4, 5, 40), pn('霜や露に打たれ、弱い者は際限なく餓死した', 5, 6, 38),
   pn('助けを叫ぶ人を、鉄砲で撃ち倒した、と書かれる', 6, 7, 38), pn('さらに、人が人を食べた、とまで書かれる', 7, 8, 38, col='gold'),
   pn('餓死した人の数は、書かれていない', 8, None, 40)]),
 dict(key='mori', title='毛利の援軍は', chapter_title='毛利の援軍は', scene=[
   pn('毛利は、鳥取城を、助けられなかったのか', 0, 1, 40), pn('『信長公記』8/13：毛利・吉川・小早川が、救援に出るという風聞', 1, 2, 34, col='gold'),
   pn('信長は、先手の者たちに、参陣の用意を命じた（『信長公記』）', 2, 3, 36), pn('丹後の永岡・丹波の明智光秀・摂津の池田勝三郎ら', 3, 4, 38),
   pn('信長自身も、東国と西国の軍勢で、一戦するつもりだった（『信長公記』）', 4, 5, 34), pn('永岡と明智の船に兵糧を積み、因幡の川の内へ着けさせた（『信長公記』）', 5, 6, 34),
   pn('毛利方の吉川元長は、伯耆で足止めされ、届かなかった（説）', 6, 7, 36), pn('9月　松井康之が、海上の補給路を断った（説）', 7, 8, 38),
   pn('こうして、信長の出陣は、見送られた（説）', 8, None, 40),
   amap('wide', places=[NOTE_POS(0, EST), dict(xy=W(*CASTLE), label='鳥取城', kind='castle', at=0, side='r', col=RED, lsize=26), dict(xy=W(*HOUKI), label='羽衣石城', kind='castle', at=6, side='b', col=BLUE, lsize=22)],
        units=[unit(label='毛利方の援軍', sub='伯耆で足止め（説）', col=RED, pts=[W(HOUKI[0] - 0.25, HOUKI[1] - 0.08), W(HOUKI[0] + 0.02, HOUKI[1] - 0.02)], legs=[[6, 7]], at=6, head=22, lab_off=(36, 10), lsize=20, dashed=True)])]),
 dict(key='surrender', title='降伏', chapter_title='降伏', scene=[
   dict(t='art', name='mountain', box=ART_BOX, at=0, dim=0.8, dir=1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.7),
   pn('『信長公記』は、降伏の様子を、こう書く', 0, 1, 40, col='gold'), pn('城中から、降参の申し出があった', 1, 2, 40),
   pn('吉川式部少輔・森下道祐・日本介。三大将の首を差し出すので、残った者を助けてほしい', 2, 3, 30, col='gold'), pn('秀吉は、信長に伺いを立て、信長は「別儀なし」と答えた', 3, 4, 36),
   pn('秀吉は、同意した', 4, 5, 42), pn('間もなく、三人は腹を切り、首が届けられた（『信長公記』）', 5, 6, 38),
   pn('10/24　経家は、吉川広家に、遺書を送った（説）', 6, 7, 38), pn('「日本を二つに分ける弓矢の境で腹を切るのは、末代までの名誉」（説）', 7, 8, 34),
   pn('降伏した人は、公記の三人とは限らない、という解説もある（説）', 8, None, 34)]),
 dict(key='after', title='開城のあと', chapter_title='開城のあと', scene=[
   pn('10/25　『信長公記』：籠城していた者が、助け出された', 0, 2, 36, col='gold'), pn('不憫に思われて、食べ物が与えられた（与えたのは秀吉と解釈される）', 2, 3, 32),
   pn('ところが、食べ物に酔って、過半の人が、すぐに死んだ（『信長公記』）', 3, 4, 34), pn('『豊鑑』：粥をたくさん食べた者は、すぐに死んだ（軍記）', 4, 5, 36),
   pn('本当に、餓鬼のように痩せ衰えていた（『信長公記』）', 5, 6, 38), pn('現代では「リフィーディング症候群」ではないか、という説（説）', 6, 7, 34, col='gold'),
   pn('鳥取城には、宮部善祥坊が城代として入った（『信長公記』）', 7, None, 36),
   amap(places=[NOTE_POS(0, EST), dict(xy=A(*CASTLE), label='鳥取城', kind='castle', at=0, side='l', col=BLUE, lsize=26)],
        units=[unit(label='宮部善祥坊', sub='城代', col=BLUE, pts=[A(CASTLE[0] + 0.01, CASTLE[1] - 0.004)], at=7, head=20, lab_off=(36, 10), lsize=20)])]),
 dict(key='source', title='資料を、分けて見る', chapter_title='資料を、分けて見る', scene=[
   dict(t='art', name='docs', box=ART_BOX, at=0, dim=0.8, dir=1, note='イメージ（生成画像）。実際の資料の再現ではありません'), dict(t='shade', box=ART_BOX, at=0, alpha=0.66),
   dict(t='cols2', size=30, xm=940, xm2=980, until=4, left=dict(title='『信長公記』', title_at=0, items=[
        dict(at=0, text='同時代に近い記録。信長の側の記録で、簡潔'), dict(at=2, text='包囲の仕組み、飢え、降伏、開城後の死を書く')]),
        right=dict(title='書かれていないこと', title_at=3, items=[dict(at=3, text='米の買い占め／住民の追い込み／餓死した人の数／経家の遺書')])),
   dict(t='cols2', size=30, xm=940, xm2=980, at=4, left=dict(title='日付', title_at=4, items=[
        dict(at=4, text='公記：6/25に軍勢が出た'), dict(at=5, text='解説：秀吉自身は6/27に姫路を出て、7/12に本陣に着いた（説）')]),
        right=dict(title='見方', title_at=6, items=[dict(at=6, text='通説・軍記・同時代の記録。分けて見るのが、確かめる第一歩')]))]),
 dict(key='summary', title='分かること、決められないこと', chapter_title='分かること、決められないこと', scene=[
   dict(t='art', name='castle', box=ART_BOX, at=0, dim=0.8, dir=-1, note=NOTE_IMG), dict(t='shade', box=ART_BOX, at=0, alpha=0.62),
   dict(t='cols2', size=32, xm=940, xm2=980, until=7, left=dict(title='分かること', title_at=0, items=[
        dict(at=0, text='天正9年、秀吉が鳥取城を囲んだ'), dict(at=1, text='城内は飢え、多くが亡くなった'), dict(at=2, text='10/25、城は開城した')]),
        right=dict(title='決められないこと', title_at=3, items=[
        dict(at=3, text='米の買い占めが、あったのか'), dict(at=4, text='住民が、追い込まれたのか、逃げ込んだのか'),
        dict(at=5, text='籠城した人の数と、餓死した人の数'), dict(at=6, text='すべて、秀吉の計画どおりだったのか')])),
   dict(t='cols2', size=33, xm=940, xm2=980, at=7, left=dict(title='見方', title_at=7, items=[
        dict(at=7, text='同時代の記録と、後の話を、分けて見ると、「渇え殺し」の見え方が変わる')]), right=dict(title='', title_at=7, items=[]))]),
]

images = dict(
    area=dict(file='assets/tottori/map_area.png'), wide=dict(file='assets/tottori/map_wide.png'),
    p_hideyoshi=dict(file='assets/portraits/hideyoshi.jpg', crop=YC['hideyoshi']),
    mountain=dict(file='assets/tottori/art_mountain.png'), docs=dict(file='assets/tottori/art_docs.png'), castle=dict(file='assets/tottori/art_castle.png'))


def _line_to_sentence_starts():
    import re
    t = (R / 'docs' / 'themes' / '20270102_tottori' / '09_script_v2.md').read_text(encoding='utf8')
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

T1 = '【鳥取の渇え殺しは計画どおり？】鳥取城の戦い 米の買い占めは本当か｜地図と『信長公記』で検証'
spec = dict(slug='tottori', theme_dir='20270102_tottori', pack='35_tottori', header_sub='鳥取城の戦いを、地図の上で、『信長公記』と後世の話に分けて確かめる',
 images=images,
 bgm=[['intro', 'terrain', 'piano36'], ['siege', 'surrender', 'piano12'], ['after', 'summary', 'piano40']],
 chapters=chapters,
 desc=dict(title_main=T1, title_no=1,
  titles=[T1, '鳥取城の戦いを地図で解説 「鳥取の渇え殺し」米の買い占め・住民の追い込みは同時代の記録にある？', '鳥取城の戦い 秀吉の兵糧攻めと有名な話を、『信長公記』と後世の書物で分けて確かめる'],
  intro='天正9年10月25日（ユリウス暦1581年11月21日、グレゴリオ暦では12月1日）、因幡の鳥取城が開城しました。城を囲んだのは羽柴秀吉、守っていたのは毛利方の吉川経家。城内の飢えの凄惨さから、「鳥取の渇え殺し」と呼ばれます。この動画では、地図の上で包囲の様子を追いながら、「秀吉は米を買い占めた」「住民を城に追い込んだ」という有名な話を、『信長公記』と、後世の書物、研究者の見方に分けて確かめます。分かることと決められないことを分けて、最後にまとめます。',
  points=['『信長公記』が書くこと：6/25に秀吉の軍が二万余騎で出陣し、但馬口から因幡へ入った。鳥取城は四方から離れた険しい山城で、西に舟で渡る大河があり、川際に「つなぎの出城」がある。秀吉は城の東の高山に陣を置き、鹿垣を結いまわし、堀・塀・築地・二重三重の矢蔵を築き、築地は前後二里にわたった。海には警固舟を置き、丹後・但馬から海上で兵糧を届けさせた。鳥取の一郡の男女がことごとく城中へ逃げ入って立てこもり、長陣の覚悟がない百姓以下はすぐに餓死した。初めは五日に一度、三日に一度鐘をつき、木草の葉・稲株・牛馬を食べ、人が人を食べたとまで書く。吉川式部少輔・森下道祐・日本介の三大将の首を差し出して残党を助けてほしいという詫言を、信長が「別儀なし」とし、10/25に籠城の者が助け出されたが、食べ物に酔って過半が頓死した。城代は宮部善祥坊。(Wikisourceの翻刻で原文を確認)',
          '『信長公記』に書かれていないこと：米の買い占め、住民の追い込み、餓死した人の数、経家の遺書。米の買い占めは後世の『陰徳太平記』などが書くとされ、解説は史実性に留保を付けています。住民については「追い込んだ」「逃げ込んだ」と書き方が分かれ、両者は両立しうると考えられます。一方、『信長公記』の8/13条には、毛利・吉川・小早川が救援に出るという風聞を受け、信長が先手に参陣の用意を命じ、永岡・維任の船に兵糧を積ませたことが書かれています。',
          '開城後の死について、『信長公記』は「食にゑひ過半頓死」と書き、『豊鑑』は粥をたくさん食べた者がすぐに死んだと書くとされます。現代では、長い飢えのあとの急な栄養摂取によるリフィーディング症候群だったのではないか、という説があります。',
          '数字と日付：秀吉の軍は二万余騎（『信長公記』）。城の人数・餓死者数は書かれておらず、確かな数は分かっていません。日付は、『信長公記』が6/25に軍勢が出たと書き、解説は秀吉自身が6/27に姫路を出て7/12に鳥取の本陣に着いたと整理しています。降伏した人は三人とは限らない、という解説もあります。',
          '経家は入城した時点で兵糧不足を書き送っていた、10/24付の吉川広家宛の遺書が伝わる、とされます(日本語版Wikipediaなどを通した紹介。原典は未確認で、研究者名は出していません)。地図上の軍勢の動きは、記録にもとづく大まかな図で、実際の経路・順序ではありません。当時の川筋は現代と違っていたとされます。'],
  refs=['太田牛一『信長公記』巻十四「因幡国取鳥城取詰之事」「因幡国取鳥果口之事」「八月朔日御馬揃之事」（Wikisource）:https://ja.wikisource.org/wiki/信長公記/我自刊我書', 'Wikipedia「鳥取城の戦い」(研究者の説と出典の整理)', '鳥取市歴史博物館やまびこ館の解説', '国立天文台 暦計算室「日本の暦日データベース」', '国土地理院 地理院タイル:https://maps.gsi.go.jp/development/ichiran.html'],
  credit_lines=['・図：自作（国土地理院タイル(陰影起伏図・標準地図)を加工して作成。現代の地形で、当時の川筋・海岸・道ではありません。城・陣・経路の位置は、案内をもとにした概略の推定です）',
                '・肖像：豊臣秀吉：古い肖像画。Wikimedia Commonsで公開されているパブリックドメインの画像です。',
                '・イラスト：ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['地図上の軍勢の動きは、記録の描写と推定にもとづく概略の図で、実際の経路・時刻ではありません。', '『信長公記』は、Wikisourceの翻刻（旧字版）で該当部分を確認しました。『陰徳太平記』『豊鑑』『吉川家文書』、研究者の説、毛利方の動き（吉川元長・松井康之）、リフィーディング症候群説、暦の換算（天正9年10月25日＝1581年11月21日）は、日本語版Wikipedia「吉川経家」と暦日対照表で確認した（国立天文台での確認は未了）。ほかは、日本語版Wikipediaや博物館の解説など二次資料を通して確認したもので、原典は直接確認していません。'],
  tags='鳥取城の戦い, 羽柴秀吉, 吉川経家, 鳥取の渇え殺し, 信長公記, 戦国時代, 戦況解説, 検証, 兵糧攻め, 因幡',
  checks=['経家遺書（吉川家文書）の原文', '『豊鑑』『陰徳太平記』の該当部分', '米の買い占め説の出典', '国立天文台の換算ツールで、1581年11月21日（ユリウス暦）＝12月1日（グレゴリオ暦）の再確認', '降伏者の人数・名前（石見吉川家文書）']),
 thumb=dict(bg='assets/tottori/thumb_art.png', lines=[['鳥取城の戦い', 112, 'white'], ['米の買い占めは', 96, 'white'], ['本当だった？', 112, 'gold']], sub='『信長公記』と後世の話を分けて確かめる', shade_col=[10, 14, 28], accent=[238, 96, 84], bar_col=[238, 96, 84], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and not o.get('title') and o['box'][3] - o['box'][1] <= 70: o['size'] = min(o.get('size', 40), 40)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


_fit(spec)
(R / 'data' / 'tottori_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
