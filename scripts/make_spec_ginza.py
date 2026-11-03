"""Writes data/ginza_spec.json（銀座は、昔は海に突き出た砂州だった？）。台本：docs/themes/20271101_ginza/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。
素材は scripts/make_ginza_assets.py で作る（国土地理院のタイル。加工して作成）。
見せ場：江戸前島（約4m）と、両側の埋め立て地（約3m）の段差。
本編の形成図は国土地理院の現在地図へ地理座標で重ね、砂州・海・埋立地・堀の変化をナレーション順に累積表示する。位置と形は模式化してある。
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize

R = Path(__file__).resolve().parents[1]
PLAYLIST_LOWLAND = 'PLV4MJdcpAGpM'   # 再生リスト「東京の低地」（日比谷・渋谷・銀座）
IMG = ('aerial_1936', 'aerial_1961', 'aerial_now', 'relief', 'relief_plain',
       'fillmap_0', 'fillmap_1', 'fillmap_2', 'fillmap_3')
IMAGES = {n: dict(file=f'assets/ginza/{n}.png') for n in IMG}
IMAGES.update({
    'pale_map_z15': dict(file='upload/80_ginza_vector_prototype/pale_current_map_z15_r3.png'),
    'pale_map_z17': dict(file='upload/80_ginza_vector_prototype/pale_current_map_z17_r6.png'),
    'street_wako': dict(file='out/ginza_remaster_work/assets/ginza_street/wako.jpg'),
    'street_crossing': dict(file='out/ginza_remaster_work/assets/ginza_street/crossing.jpg'),
})
CAP_RELIEF = '色別標高図（国土地理院の5mメッシュ標高から作成）'
CAP_1936 = '国土地理院 空中写真（1936〜42年頃）'


# --- ポップスタイルの部品（vp_anim_pop）。at/until は章内の行番号
def pop(name, **kw):
    return dict(t='anim', name=name, **kw)


def tel(text, x, y, size, **kw):
    return dict(t='anim', name='pop_telop', text=text, x=x, y=y, size=size, **kw)


def rows(items, **kw):
    kw.setdefault('x0', 100)
    kw.setdefault('x1', 1820)
    kw.setdefault('y0', 180)
    kw.setdefault('size', 38)
    kw.setdefault('gap', 18)
    return dict(t='anim', name='pop_rows', items=items, **kw)


def card(box, **kw):
    kw.setdefault('at', 0)
    kw.setdefault('rot', -2)
    return dict(t='anim', name='pop_card', inner='img', box=box, **kw)


spec = dict(
    slug='ginza', theme_dir='20271101_ginza', pack='80_ginza',
    header_sub='江戸前島・銀座の埋立てで、地形の成り立ちを確かめる',
    images=IMAGES,
    bgm=[['intro', 'maejima', 'piano36'], ['maejima', 'end', 'piano12'], ['end', 'end', 'piano40']],
    style='pop',
    chapters=[
        {'key': 'intro', 'title': '銀座は、昔は海に突き出た砂州だった？',
         'chapter_title': '導入：銀座は昔は海に突き出た砂州だった？',
         'opener': '銀座は、昔は海に突き出た砂州だった？', 'opener_until': 1,
         'scene': [pop('pop_bgimg', img='aerial_1936', at=0, dim=.5, blur=3),
                   tel('銀座は、昔は\n[[海に突き出た砂州]]だった？', 960, 450, 130, at=0, until=2, rot=-3),
                   tel('正確には、[[砂が積もってできた半島]]の先端ちかく', 960, 700, 92, at=1, until=3, plate='green', rot=1.5),
                   tel('半島の西は入り江、東は海', 960, 470, 76, at=2, until=4, plate='yellow', rot=-1.5),
                   tel('両側が埋め立てられて、今の銀座になった', 960, 660, 78, at=3, until=4, plate='blue', rot=1),
                   tel('順を追って、地形の成り立ちを確かめる', 960, 560, 96, at=4, plate='pink', rot=-2)]},
        {'key': 'maejima', 'title': '江戸前島', 'chapter_title': '江戸前島：砂州がつくった半島',
         'scene': [pop('ginza_formation_map', at=0)]},
        {'key': 'west', 'title': '西を埋める', 'chapter_title': '西を埋める：1603年〜',
         'scene': [pop('ginza_formation_map', at=0)]},
        {'key': 'east', 'title': '東を埋める', 'chapter_title': '東を埋める：1657年〜',
         'scene': [pop('ginza_formation_map', at=0)]},
        {'key': 'moat', 'title': '島になり、また陸になる', 'chapter_title': '島になり、また陸になる',
         'scene': [pop('ginza_formation_map', at=0)]},        {'key': 'end', 'title': '名残りとまとめ', 'chapter_title': '名残りとまとめ',
         'scene': [pop('pop_bgimg', img='street_wako', alts=['street_crossing'], seg=12, at=0, dim=.24, blur=0, zoom=.08),
                   tel('まとめ！', 960, 400, 150, at=0, until=1, rot=-3),
                   rows([dict(at=0, tag='分かった', text='銀座は、海ではなく砂州の半島の先端ちかくだった', col='green'),
                         dict(at=1, tag='分かった', text='西・東・堀は、時期も理由も別に埋め立てられた', col='green'),
                         dict(at=2, tag='高さ', text='標高を測ると、銀座はまわりの埋め立て地より少し高い', col='orange'),
                         dict(at=3, tag='柳', text='1874年に植えた木が根腐れし、柳に替えられたとされる', col='red'),
                         dict(at=4, tag='通り', text='中央通りの向きは、京橋・日本橋と少し違う。地形に沿ったためとされる', col='purple')],
                        y0=180, size=40, gap=18),
                   tel('次に銀座を歩くとき、\n[[砂州の先端]]を思い出してみて', 960, 740, 52, at=5, plate='yellow', rot=-1)]},
    ],
    desc={
        'title_main': '銀座は、昔は海に突き出た砂州だった？',
        'title_no': 1,
        'titles': ['銀座は、昔は海に突き出た砂州だった？ 江戸前島と埋め立ての歴史',
                   '江戸前島とは？ 銀座と築地の地形を地図と標高で確かめる',
                   '三十間堀川・外堀の埋め立てから辿る銀座の歴史'],
        'intro': '銀座には海の名残が残っています。実は海ではなく、江戸前島という砂州の半島の先端ちかくでした。'
                 '半島の西は日比谷入江、東は海で、それぞれ別の理由で埋め立てられ、今の街になりました。'
                 '順を追って、地図・標高・空中写真で確かめます。'
                 '\n\n■ シリーズ「東京の低地」\n'
                 '昔は水だった土地を、地図・標高・空中写真で確かめます。\n'
                 '再生リスト:https://www.youtube.com/playlist?list=' + PLAYLIST_LOWLAND,
        'points': ['江戸前島は、隅田川が運んだ砂が積もってできた砂州の半島です。'
                   '中央通り付近を尾根筋とし、汐留付近を先端としていました。'
                   '日本橋・京橋・銀座の町は、この半島の上に広がっていきました。',
                   '半島の西側は日比谷入江という入り江でした。1603年の江戸開府後、天下普請で埋め立てが始まり、'
                   '1612年に駿府の銀座が移って地名の由来になりました。埋め立て地は日本橋台地と呼ばれます。',
                   '東側は1657年の明暦の大火をきっかけに、西本願寺の代替地として佃島の住人が造成しました。そこが「築地（埋立地の意）」です。',
                   '銀座は東を三十間堀川、西を外堀、南を汐留川、北を京橋川に囲まれた島になりました。'
                   '1949年に三十間堀川の埋め立てが始まり、1964年に東京高速道路が完成するまで、堀は順に道路へ変わりました。',
                   '国土地理院の標高データでは、銀座四丁目が約4.1m、京橋が約4.0m、築地本願寺が約3.4m、汐留が約3.3mで、'
                   '日比谷入江側の埋め立て地（約3m）よりわずかに高く、砂州の微高地であることが分かります。',
                   '1874年に植えた桜・松・楓が根腐れし、湿地に強い柳に植え替えられたエピソードは、埋立地の性質を物語ります。',
                   '中央通りの軸線は、京橋・日本橋・神田の軸線と方向が異なります。地形の尾根筋に沿って通したためとされます。'],
        'refs': ['Wikipedia「銀座」:https://ja.wikipedia.org/wiki/銀座',
                 'Wikipedia「築地」:https://ja.wikipedia.org/wiki/築地',
                 'Wikipedia「江戸前島」:https://ja.wikipedia.org/wiki/江戸前島',
                 '国土地理院 地理院タイル一覧:https://maps.gsi.go.jp/development/ichiran.html',
                 '国土地理院コンテンツ利用規約:https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html'],
        'credit_lines': [
            '・映像素材:国土地理院撮影の空中写真(1936〜42年頃)と地理院タイルの現在地図を加工',
            '・色別標高図:国土地理院の標高タイル(5mメッシュ)から作成',
            '・模式図:現在の地理院地図に砂州・水域・埋立地・堀の範囲を地理座標で重ねて表示(復元範囲・海岸線は模式図)',
            '・銀座和光の写真:Supanut Arunoprayote / CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)',
            '・銀座四丁目交差点の写真:ノボホショコロトソ / CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)',
            '・場面のイラスト:ChatGPT・Codex(OpenAI)による生成イラスト(イメージです。実際の場面・人物・資料の再現ではありません)',
        ],
        'notes': ['「海」ではなく「砂州の半島」。表現には注意する。',
                  '埋め立ては「西（日比谷入江）→東（築地）→堀」の3段階で、別々の理由・時期に進んだ。1つの事業として語らない。',
                  '「島」は比喩ではなく、4本の堀に囲まれた事実。行政的な島ではない。',
                  '築地の造成は「銀座のため」ではなく、西本願寺の代替地として造成された。',
                  '中央通りの向きが京橋・日本橋と違うのは、砂州の尾根筋に沿ったため。現地で確認できる。',
                  '標高は国土地理院の5mメッシュ標高から、地点の周り9×9画素の平均を取った概算です。',
                  '柳の根腐れの原因は「埋立地の水分」とされるが、確定した説ではない。',
                  '1262年の「前嶋村」、中央通り＝尾根筋、楓川・三十間堀川の掘削は、二次資料（Wikipedia等）のみで確認したため「〜とされる」「との説」と弱めています。',
                  '三井住友トラスト不動産「このまちアーカイブス」は 2026-11-01 時点で HTTP 503 で再取得できず、日比谷回の参照情報から補っています。'],
        'tags': '銀座, 江戸前島, 江戸, 埋め立て, 日比谷入江, 築地, 明暦の大火, 地形, 検証',
        'checks': ['中央区「銀座・銀座西地区 町名の由来」で1612年の記述を直接確認',
                   '築地の造成（1657年・佃島の住人）を中央区の資料で確認',
                   '標高の値を国土地理院の標高確認ページで1点照合',
                   '模式図の範囲（砂州の幅・堀の位置）を古地図または治水地形分類図と見比べて調整'],
    },
    thumb=dict(bg='assets/ginza/relief_plain.png',
               lines=[['銀座は', 76, 'white'], ['砂州の先端？', 130, 'gold']],
               sub='地図と標高で、確かめる', shade_col=[8, 20, 36], accent=[255, 178, 72],
               bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=640, sub_size=42,
               shade_x=700, shade_w=520))

finalize(spec, {})