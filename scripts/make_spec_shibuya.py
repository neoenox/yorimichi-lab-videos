"""Writes data/shibuya_spec.json。台本：docs/themes/20270609_shibuya_river/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。
素材は scripts/make_shibuya_assets.py で作る（国土地理院のタイル。加工して作成）。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
R = Path(__file__).resolve().parents[1]
HOK = (R / 'assets' / 'shibuya' / 'hokusai.jpg').exists()
LEFT = [60, 170, 960, 850]
RX0, RX1 = 1000, 1860
CAP_GSI = '国土地理院撮影の空中写真（{}）を加工して作成'
IMAGES = {n: dict(file=f'assets/shibuya/{n}.png') for n in ('aerial_1936', 'aerial_1961', 'aerial_now', 'relief', 'relief_plain')}
if HOK:
    IMAGES['hokusai'] = dict(file='assets/shibuya/hokusai.jpg')


def stack(items, y0=190, size=32, gap=18, ymax=850, x0=RX0, x1=RX1):
    return dict(t='stack', x0=x0, x1=x1, y0=y0, size=size, gap=gap, ymax=ymax, items=items)


edo_scene = [dict(t='anim', name='sb_edo', box=[60, 170, 1860, 760], at=0, steps=[dict(at=1), dict(at=2), dict(at=3)], until=4)] + (
    [dict(t='image', name='hokusai', box=[560, 170, 1360, 760], at=4, cap='葛飾北斎「冨嶽三十六景 隠田の水車」（東京都江戸東京博物館蔵）')] if HOK else []) + [
    dict(t='panel', box=[60, 775, 1860, 845], text='北斎が「穏田の水車」、広重が「広尾ふる川」を描いた', at=4, size=34, hi=True)]

# --- ポップスタイルの部品（vp_anim_pop）。at/until は章内の行番号
def pop(name, **kw):
    return dict(t='anim', name=name, **kw)


def tel(text, x, y, size, **kw):
    return dict(t='anim', name='pop_telop', text=text, x=x, y=y, size=size, **kw)


def rows(items, **kw):
    return dict(t='anim', name='pop_rows', items=items, **kw)


def card(inner, box, **kw):
    kw.setdefault('at', 0)
    return dict(t='anim', name='pop_card', inner=inner, box=box, **kw)


spec = dict(slug='shibuya', theme_dir='20270609_shibuya_river', pack='78_shibuya', header_sub='東京都の資料と空中写真で、渋谷の谷と川を確かめる',
 images=IMAGES,
 bgm=[['intro', 'edo', 'piano36'], ['edo', 'photo', 'piano12'], ['photo', 'end', 'piano40']],
 style='pop',
 chapters=[
 {'key': 'intro', 'title': '渋谷の谷底には、昔は川が流れていた？', 'chapter_title': '導入：渋谷の谷底には、昔は川が流れていた？',
  'scene': [pop('pop_bgimg', img='aerial_1936', at=0, dim=.5, blur=3),
            tel('渋谷は\n[[坂]]だらけ！', 960, 460, 150, at=0, until=2, rot=-3),
            tel('坂が多い ＝ 谷がある', 960, 720, 78, at=1, until=2, plate='yellow', rot=1.5),
            tel('昔、[[川]]が\n流れていた？', 960, 470, 140, at=2, until=4, rot=-2),
            tel('東京都の資料 × 空中写真で確かめる', 960, 740, 56, at=3, until=4, plate='blue', rot=1),
            tel('答え：[[流れていた！]]', 960, 480, 120, at=4, plate='green', rot=-2),
            tel('そして、その上流は今…下水道に！', 960, 690, 58, at=4, plate='yellow', rot=1.5)]},
 {'key': 'tani', 'title': '谷の形', 'chapter_title': '谷の形',
  'scene': [pop('pop_bgimg', img='relief_plain', at=0, dim=.45, blur=7),
            card('img', [60, 150, 960, 840], at=0, rot=-2, img='relief', cap='標高の色別図（国土地理院の標高から自作）'),
            rows([dict(at=1, tag='資料', text='渋谷は、武蔵野台地の末端', col='orange'),
                  dict(at=2, tag='資料', text='渋谷川がつくった谷が、シカの角のように西へ伸びる', col='orange')], x0=1000, x1=1860, y0=160, size=34, gap=16),
            tel('渋谷駅前 [[15m]]', 1430, 590, 84, at=4, until=5, rot=2),
            tel('道玄坂の上 [[33m]]\n松濤 [[35m]]', 1430, 600, 66, at=5, until=6, rot=-2),
            tel('駅前は周りより\n約[[20m]]低い谷底！', 1430, 650, 70, at=6, plate='red', rot=2)]},
 {'key': 'edo', 'title': '江戸の頃の川', 'chapter_title': '江戸の頃の川',
  'scene': [card('edo', [60, 150, 1860, 770], at=0, rot=0, until=4, steps=[dict(at=1), dict(at=2), dict(at=3)]),
            tel('北斎『穏田の水車』\n広重『広尾ふる川』', 960, 470, 70, at=4, plate='yellow', rot=-2),
            tel('絵に描かれるほどの[[名所]]だった川', 960, 690, 54, at=4, plate='pink', rot=1.5)]},
 {'key': 'yowaru', 'title': '水量が減り、街が変わった', 'chapter_title': '水量が減り、街が変わった',
  'scene': [tel('その川に、\n何があった？', 960, 480, 130, at=0, until=1, rot=-2),
            rows([dict(at=1, tag='1898年', text='淀橋浄水場が完成', col='orange'),
                  dict(at=2, tag='同じ頃', text='約250年続いた玉川上水の落とし水が、なくなる', col='red'),
                  dict(at=3, tag='のち', text='電力の普及も重なって、水車は衰える', col='blue'),
                  dict(at=4, tag='街の成長', text='大雨のたびの氾濫と、水の汚れが問題に', col='purple'),
                  dict(at=5, tag='昭和の初め', text='石積みの護岸が完成', col='green')], x0=110, x1=1810, y0=170, size=42, gap=20)]},
 {'key': 'photo', 'title': '空中写真で見る今と昔', 'chapter_title': '空中写真で見る今と昔',
  'scene': [pop('pop_bgimg', img='aerial_1961', at=0, dim=.6, blur=8),
            card('photos', [90, 150, 790, 850], at=0, rot=-2, imgs=[dict(name='aerial_1936', label='1936〜42年頃', at=1), dict(name='aerial_1961', label='1961〜69年', at=4), dict(name='aerial_now', label='今の地理院地図の写真', at=7)],
                 mark=dict(img=0, pts=[(.635, .557), (.719, .625), (.791, .688), (.865, .750), (.917, .807)], at=2, until=4, label='川筋と考えられる筋（推定）', lab=(.5, .92))),
            rows([dict(at=2, tag='1936〜42', text='駅の南東に、細く曲がった筋', col='orange'),
                  dict(at=3, tag='推定', text='川筋と考えられるが、写真だけでは断定できない', col='red'),
                  dict(at=5, tag='1961〜69', text='上流で、下水道への切り替えが進んだ時期', col='blue'),
                  dict(at=6, tag='変化', text='道路は広く直線に。駅の北側に並木の帯', col='purple'),
                  dict(at=8, tag='今', text='ビルの谷間に、細い水辺', col='green')], x0=930, x1=1860, y0=160, size=36, gap=14),
            tel('出典：国土地理院撮影の空中写真（加工して作成）', 1390, 800, 28, at=1)]},
 {'key': 'gesui', 'title': '上流は下水道になった', 'chapter_title': '上流は下水道になった',
  'scene': [pop('pop_bgimg', img='aerial_1961', at=0, dim=.6, blur=6),
            rows([dict(at=0, tag='1961年', text='審議会が、渋谷川を下水道幹線にする答申', col='orange'),
                  dict(at=1, tag='1961〜70年', text='宮益橋より上流と、宇田川・河骨川などの支流が下水道幹線に', col='red'),
                  dict(at=2, tag='1964年', text='東京オリンピックを契機に、下水道や道路の整備が進む', col='blue')], x0=110, x1=1810, y0=190, size=42, gap=22),
            tel('写真だけでは、\n地下の川筋の位置は[[分からない]]', 960, 690, 62, at=3, plate='yellow', rot=-1.5)]},
 {'key': 'ima', 'title': '地上の渋谷川（平成20年の資料）', 'chapter_title': '地上の渋谷川（平成20年の資料）',
  'scene': [card('flow', [60, 150, 1860, 790], at=0, rot=0, until=5, steps=[dict(at=i) for i in range(5)]),
            rows([dict(at=5, tag='都の資料', text='昔の谷や支流の跡は、今ではほとんど目立たない', col='orange'),
                  dict(at=6, tag='豆知識', text='『春の小川』は暗渠になった河骨川をうたったもの、といわれている', col='pink')], x0=110, x1=1810, y0=170, size=42, gap=20),
            tel('川は消えたのではなく\n[[姿を変えた]]！', 960, 650, 96, at=5, rot=-2)]},
 {'key': 'end', 'title': 'まとめと、分からないこと', 'chapter_title': 'まとめと、分からないこと',
  'scene': [tel('まとめ！', 960, 480, 160, at=0, until=1, rot=-3),
            rows([dict(at=1, tag='分かった', text='渋谷の谷には、昔、川が流れ、水車が回っていた', col='green'),
                  dict(at=2, tag='分かった', text='1961〜70年に、上流と支流は下水道幹線に', col='green'),
                  dict(at=3, tag='分かった', text='平成20年の資料では、地上の川は処理水で水を保つ', col='green'),
                  dict(at=4, tag='分からない', text='暗渠になった年は資料ごとに幅。『春の小川』＝河骨川は、いわれている段階', col='orange')], x0=110, x1=1810, y0=170, size=40, gap=18),
            tel('次に渋谷で坂を下りるとき、\n[[谷の底の川]]を思い出してみて', 960, 730, 56, at=5, plate='yellow', rot=-1)]}],
 desc={'title_main': '渋谷の谷底には、昔は川が流れていた？', 'title_no': 1,
 'titles': ['渋谷の谷底には、昔は川が流れていた？ 空中写真と東京都の資料で確かめる', '渋谷川は消えた？ 上流は下水道に、地上の川は処理水で', '渋谷の坂は、川がつくった谷？ 1936年と今の空中写真を比べる'],
 'intro': '渋谷駅の周りは、坂だらけです。坂が多いのは谷があるから。では、その谷の底に、昔は川が流れていたのでしょうか。この動画では、東京都の資料と、国土地理院の空中写真・標高データで確かめます。',
 'points': ['東京都建設局『渋谷川・古川 河川整備基本方針』(平成20年5月)によると、渋谷は武蔵野台地の末端にあり、渋谷川がつくった谷と支流の谷が、シカの角のように西へ伸びています。江戸時代の川は、玉川上水の落とし水や湧き水を集め、水車が営まれていました。',
            '1898年(明治31年)に淀橋浄水場が完成して落とし水がなくなり、電力の普及も重なって水車は衰えました。1961〜70年(昭和36〜45年)に、宮益橋より上流と宇田川・河骨川などの支流が下水道幹線になりました。',
            '同資料(2008年時点)では、宮益橋から約200m下流の稲荷橋から、川は地上に出ます。上流が下水道になったため、ふだんの水量は少なくなり、下水を高度に処理した水を導水して水を保っています。'],
 'refs': ['東京都建設局『渋谷川・古川 河川整備基本方針』(平成20年5月):https://www.kensetsu.metro.tokyo.lg.jp/content/000054913.pdf',
          '国土地理院 地理院タイル一覧:https://maps.gsi.go.jp/development/ichiran.html',
          '国土地理院コンテンツ利用規約:https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html'],
 'credit_lines': ['・空中写真:国土地理院撮影の空中写真(1936〜42年頃、1961〜69年)と全国最新写真を、地理院タイルから加工して作成。標高の色別図:国土地理院の標高タイル(5mメッシュ)から作成',
                  '・写真の「川筋と考えられる筋」の印は、動画の作者が写真を見て付けた推定で、国土地理院が作成したものではありません'] + (['・葛飾北斎「冨嶽三十六景 隠田の水車」(東京都江戸東京博物館) 出典:Tokyo Museum Collection(https://museumcollection.tokyo/en/works/6249440/)'] if HOK else []),
 'notes': ['暗渠になった年は、資料ごとに幅があります。この動画では、東京都の資料の1961〜70年(昭和36〜45年)で説明しています。',
           '川の上流端の呼び方は資料によって違います。この動画は2008年(平成20年)の東京都の資料に従い、現在の資料との照合はしていません。',
           '『春の小川』が河骨川をうたったものという話は、東京都の資料に「いわれている」と書かれている段階です。',
           '標高は国土地理院の5mメッシュ標高から、地点の周り9×9画素の平均を取った概算です。'],
 'tags': '渋谷, 渋谷川, 暗渠, 宇田川, 河骨川, 春の小川, 空中写真, 地形, 検証',
 'checks': ['現在の資料での渋谷川の上流端を確認する', '写真上の川筋の位置を、都資料の付図と照合する', '収益化動画での地理院データの扱いを国土地理院に確認する']},
 thumb=dict(bg='assets/shibuya/thumb_bg.png', lines=[['渋谷の谷底に', 76, 'white'], ['昔、川が？', 130, 'gold']], sub='空中写真と都の資料で、確かめる', shade_col=[8, 20, 36], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=640, sub_size=42, shade_x=700, shade_w=520))
finalize(spec, {})
