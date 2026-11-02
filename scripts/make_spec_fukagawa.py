"""Writes data/fukagawa_spec.json（深川・木場は、昔は海だった？）。台本：docs/themes/20271102_fukagawa/09_script_v2.md
at / until は『章内の行番号（0始まり）』。spec_common.finalize が文の番号に直す。
素材は scripts/make_fukagawa_assets.py で作る（国土地理院のタイル。加工して作成）。
見せ場：門前仲町（約1m）・木場（約1m）・豊洲（約2-3m）の超低地。銀座（約4m）よりさらに低い。
fillmap は標高だけを土台に、干潟・自然河川・運河網・木場・埋め立ての範囲を手で描いた模式図。位置と形は模式化してある。
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize

R = Path(__file__).resolve().parents[1]
PLAYLIST_LOWLAND = 'PLV4MJdcpAGpM'   # 再生リスト「東京の低地」（日比谷・渋谷・銀座・深川）
IMG = ('aerial_1936', 'aerial_1961', 'aerial_now', 'relief', 'relief_plain',
       'fillmap_0', 'fillmap_1', 'fillmap_2', 'fillmap_3')
IMAGES = {n: dict(file=f'assets/fukagawa/{n}.png') for n in IMG}
CAP_RELIEF = '色別標高図（国土地理院の5mメッシュ標高から作成）'
CREDIT = '国土地理院の標高データから作成・位置と形は模式化'
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
    slug='fukagawa', theme_dir='20271102_fukagawa', pack='81_fukagawa',
    header_sub='深川・木場の埋立てと運河網で、地形の成り立ちを確かめる',
    images=IMAGES,
    bgm=[['intro', 'kiba', 'piano36'], ['kiba', 'end', 'piano12'], ['end', 'end', 'piano40']],
    style='pop',
    chapters=[
        {'key': 'intro', 'title': '深川・木場は、昔は海だった？',
         'chapter_title': '導入：深川・木場は昔は海だった？',
         'opener': '深川・木場は、昔は海だった？', 'opener_until': 1,
         'scene': [pop('pop_bgimg', img='aerial_1936', at=0, dim=.5, blur=3),
                   tel('深川・木場は、昔は\n[[海]]だった？', 960, 450, 130, at=0, until=2, rot=-3),
                   tel('正確には、[[入り江の最奥部]]だった', 960, 700, 92, at=1, until=3, plate='green', rot=1.5),
                   tel('干潟と湿地が、開拓されて街になった', 960, 470, 76, at=2, until=4, plate='yellow', rot=-1.5),
                   tel('地形と資料で、[[確かめる]]', 960, 660, 78, at=3, until=4, plate='blue', rot=1),
                   tel('名残りも見ていこう', 960, 560, 96, at=4, plate='pink', rot=-2)]},
        {'key': 'kaihatu', 'title': '開拓と門前町', 'chapter_title': '開拓と門前町：1600〜1657',
         'scene': [pop('pop_bgimg', img='relief_plain', at=0, dim=.65, blur=12),
                   card([60, 150, 960, 840], at=0, rot=-2, img='relief', cap=CAP_RELIEF),
                   rows([dict(at=0, tag='開拓', text='八郎右衛門が小名木川北岸を開拓', col='orange'),
                         dict(at=1, tag='創建', text='1627年、富岡八幡宮と永代寺を創建', col='blue'),
                         dict(at=2, tag='橋', text='1659年、両国橋が架かり江戸に組み込まれた', col='green'),
                         dict(at=3, tag='入り江', text='入り江がすぐそばまで迫っていた', col='purple'),
                         dict(at=4, tag='文人', text='馬琴や源内も、この街に暮らしたとされる', col='pink')],
                        x0=1000, x1=1860, y0=160, size=40, gap=14),
                   tel('入り江の果てが、\n[[街の種]]になった', 1430, 730, 54, at=3, until=5, plate='yellow', rot=2)]},
        {'key': 'kiba', 'title': '木場の誕生', 'chapter_title': '木場の誕生：1657年〜',
         'scene': [pop('pop_bgimg', img='aerial_1961', at=0, dim=.6, blur=11, alts=['aerial_1936'], seg=16),
                   pop('pop_fill', base='fillmap_0', at=0, box=[60, 150, 960, 840], rot=-2,
                       cap='入り江と運河・木場の模式図（位置・形は模式化）', credit=CREDIT,
                       steps=[dict(img='fillmap_1', at=0)]),
                   rows([dict(at=0, tag='大火', text='明暦の大火（1657）で江戸の大半が焼けた', col='orange'),
                         dict(at=1, tag='命令', text='材木河岸を深川へ移す命令が出た', col='blue'),
                         dict(at=2, tag='貯木場', text='材木を水に浮かべて保管する場所', col='green'),
                         dict(at=3, tag='賑わい', text='材木商と職人が集まり大いに賑わった', col='purple')],
                        x0=1000, x1=1860, y0=180, size=40, gap=14),
                   tel('木材を水で扱う、\n[[木の街]]になった', 1430, 770, 52, at=4, plate='yellow', rot=-1)]},
        {'key': 'unga', 'title': '運河網と水運ハブ', 'chapter_title': '運河網と水運ハブ：1700年〜',
         'scene': [pop('pop_bgimg', img='aerial_now', at=0, dim=.55, blur=6, alts=['aerial_1961'], seg=16),
                   pop('pop_fill', base='fillmap_0', at=0, box=[60, 150, 960, 840], rot=-2,
                       cap='入り江と運河・木場の模式図（位置・形は模式化）', credit=CREDIT,
                       steps=[dict(img='fillmap_2', at=0)]),
                   rows([dict(at=0, tag='物資', text='米・塩・生糸も船で集まった', col='orange'),
                         dict(at=1, tag='運河', text='運河が格子状に掘られた', col='blue'),
                         dict(at=2, tag='生糸', text='生糸は横浜へ船で運ばれた', col='green'),
                         dict(at=3, tag='拠点', text='江戸と各地の物流の要所に', col='purple'),
                         dict(at=4, tag='花街', text='辰巳の花街として名を知られた', col='pink')],
                        x0=1000, x1=1860, y0=180, size=40, gap=14),
                   tel('水運で栄えた、\n[[江戸の台所]]', 1430, 770, 52, at=4, plate='yellow', rot=-1)]},
        {'key': 'umetate', 'title': '埋め立てと海の消滅', 'chapter_title': '埋め立てと海の消滅：明治〜',
         'scene': [pop('pop_bgimg', img='aerial_now', at=0, dim=.5, blur=8, alts=['aerial_1961'], seg=16),
                   pop('pop_fill', base='fillmap_0', at=0, box=[60, 150, 960, 840], rot=-2,
                       cap='入り江と運河・木場の模式図（位置・形は模式化）', credit=CREDIT,
                       steps=[dict(img='fillmap_3', at=0)]),
                   rows([dict(at=0, tag='埋立', text='明治以降、沖の埋め立てが進んだ', col='orange'),
                         dict(at=1, tag='災害', text='大水害・震災・空襲で焦土になった', col='blue'),
                         dict(at=2, tag='公園', text='旧木場は埋め立てられ、木場公園に', col='green'),
                         dict(at=3, tag='伝承', text='貯木場の記憶は「角乗」に残る', col='purple')],
                        x0=1000, x1=1860, y0=180, size=40, gap=14),
                   tel('入り江の果ては、\n[[工場からタワマンへ]]変わった', 1430, 770, 52, at=4, plate='yellow', rot=-1)]},
        {'key': 'end', 'title': '名残りとまとめ', 'chapter_title': '名残りとまとめ',
         'scene': [pop('pop_bgimg', img='relief_plain', at=0, dim=.5, blur=8),
                   tel('まとめ！', 960, 400, 150, at=0, until=1, rot=-3),
                   rows([dict(at=0, tag='分かった', text='深川は、海ではなく入り江の最奥部（干潟・湿地）だった', col='green', until=4),
                         dict(at=1, tag='分かった', text='開拓→木場→運河網→埋め立てで、順に街になった', col='green', until=4),
                         dict(at=2, tag='高さ', text='門前仲町 約0.9m・木場 約1.1m・豊洲 約2.7m。銀座（約4m）よりずっと低い', col='orange', until=4),
                         dict(at=3, tag='川', text='小名木川・仙台堀川・横十間川…運河の名は、今も地図に残る', col='red', until=4),
                         dict(at=3, tag='祭り', text='富岡八幡宮の水掛け祭りに、江戸の賑わいの面影がある', col='purple', until=4)],
                        y0=180, size=40, gap=18),
                   tel('次に深川を歩くとき、\n[[入り江の底]]を思い出してみて', 960, 400, 58, at=4, rot=-1), tel('チャンネル登録と、再生リスト[[「東京の低地」]]もどうぞ', 960, 700, 52, at=4, plate='yellow', rot=1)]},
    ],
    desc={
        'title_main': '深川・木場は、昔は海だった？',
        'title_no': 1,
        'titles': ['深川・木場は、昔は海だった？ 入り江の果てから木場・運河網へ',
                   '深川八幡宮と木場の歴史 材木と生糸が支えた江戸の物流',
                   '明暦の大火から木場公園まで 運河の街・深川の変遷'],
        'intro': '深川には海の名残があちこちに残っています。実は海ではなく、東京湾の最奥まで入り込んだ「入り江の果て（干潟・湿地）」でした。'
                 '慶長年間の開拓から始まり、明暦の大火で木場が移転、運河網が整備されて材木・米・生糸の水運ハブになり、明治以降の埋め立てで海が消えて今の街になりました。'
                 '順を追って、地図・標高・空中写真で確かめます。'
                 '\n\n■ シリーズ「東京の低地」\n'
                 '昔は水だった土地を、地図・標高・空中写真で確かめます。\n'
                 '再生リスト:https://www.youtube.com/playlist?list=' + PLAYLIST_LOWLAND,
        'points': ['東京湾の最奥部まで入り込んだ入り江が、干潟と湿地として広がっていました。銀座（約4m）よりさらに低い、海抜0〜3mの超低地です。',
                   '慶長年間（1596-1614）に深川八郎右衛門が小名木川北岸を開拓したと伝わり、寛永4年（1627）に富岡八幡宮と永代寺が創建されて門前町として発展しました。',
                   '明暦の大火（1657年）後、幕府命令で日本橋の材木河岸が深川に移転。「木場」とは材木を水に浮かべて保管・加工する貯木場のことです。材木商と川並鳶が集まり大いに賑わいました。',
                   '横十間川・仙台堀川・大横川・北十間川・小名木川…運河が格子状に掘削され、材木・米・塩・生糸が船で集まる江戸の物流拠点になりました。富岡製糸場の生糸も深川から横浜へ船で運ばれたとされます。',
                   '明治以降、沖合の埋め立てが進み海岸線が後退。1910年大水害、1923年関東大震災、1945年東京大空襲で何度も壊滅的被害を受けました。1969年新木場建設で旧木場は木場公園になり、川並鳶の「角乗」だけが貯木場の記憶を伝えます。',
                   '国土地理院の標高データでは、門前仲町約0.9m、木場三丁目約1.1m、豊洲四丁目約2.7mで、銀座四丁目（約4.1m）よりずっと低く、入り江の最奥部だったことが分かります。',
                   '小名木川・仙台堀川・横十間川など運河の名は今も地図に残り、富岡八幡宮の水掛け祭り（深川八幡祭り）に江戸の賑わいの面影があります。'],
        'refs': ['Wikipedia「深川区」:https://ja.wikipedia.org/wiki/深川区',
                 'Wikipedia「木場」:https://ja.wikipedia.org/wiki/木場',
                 'Wikipedia「富岡製糸場」:https://ja.wikipedia.org/wiki/富岡製糸場',
                 '江東区 深川江戸資料館:https://www.city.koto.lg.jp/',
                 '国土地理院 地理院タイル一覧:https://maps.gsi.go.jp/development/ichiran.html',
                 '国土地理院コンテンツ利用規約:https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html'],
        'credit_lines': [
            '・空中写真:国土地理院撮影の空中写真(1936〜42年頃、1961〜69年頃)と全国最新写真を、地理院タイルから加工して作成',
            '・色別標高図:国土地理院の標高タイル(5mメッシュ)から作成',
            '・模式図:国土地理院の標高タイルを土台に、干潟・自然河川・運河網・木場・埋め立ての範囲を描き足して作成(位置と形は模式化)',
            '・場面のイラスト:ChatGPT・Codex(OpenAI)による生成イラスト(イメージです。実際の場面・人物・資料の再現ではありません)',
        ],
        'notes': ['「海」ではなく「入り江の最奥部（干潟・湿地）」。表現には注意する。',
                  '木場移転の時期は「明暦の大火（1657）後」が通説だが、幕府の都市改造計画の一環として段階的だった。「〜とされる」で弱める。',
                  '富岡製糸場の生糸輸送ルート（深川→横浜）は二次資料のみ。「〜とされる」で弱める。',
                  '深川八郎右衛門の開拓・赤穂浪士の会議・文人の居住は、二次資料（Wikipedia系・区史）のみ。「〜と伝わる」「〜とされる」で弱める。',
                  '標高は国土地理院の5mメッシュ標高から、地点の周り9×9画素の平均を取った概算です。',
                  '一次資料（古地図・幕府公文書・船問屋帳簿）での裏取りは未了。公開時は弱めて扱う。'],
        'tags': '深川, 木場, 門前仲町, 江東区, 埋め立て, 明暦の大火, 富岡八幡宮, 運河, 生糸, 江戸, 地形, 検証',
        'checks': ['江東区「深川区史」「木場の歴史」で開拓・木場移転・運河掘削の年号を直接確認',
                   '深川江戸資料館の常設展示解説で干潟・貯木場・生糸輸出の記述を確認',
                   '標高の値を国土地理院の標高確認ページで3点（門前仲町・木場・豊洲）手で照合',
                   '模式図の範囲（入り江の形・運河の位置・木場の広がり）を古地図（寛永江戸図・明治初期迅速測図）と見比べて調整',
                   '「角乗」「川並鳶」の伝承を木場公園公式サイト・江東区観光協会で確認'],
    },
    thumb=dict(bg='assets/fukagawa/relief_plain.png',
               lines=[['深川・木場は', 76, 'white'], ['昔は入江？', 130, 'gold']],
               sub='地図と標高で、確かめる', shade_col=[8, 20, 36], accent=[255, 178, 72],
               bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=640, sub_size=42,
               shade_x=700, shade_w=520))

finalize(spec, {})