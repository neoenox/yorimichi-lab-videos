"""Writes data/sigdeepseek_spec.json（信号の「青」は、なぜ緑色に見えるのか）。
台本：docs/themes/20261104_signal/09_script_v2.md（固定・変更しない）。
画面は style='pop'。素材は assets/sigcmp/ の3枚だけ（intro / law / world）。
at・until は台本の行ではなく「文」の番号（章の中の0始まり）。"""
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]

A = dict(dim=.55, blur=4)


def bg(name):
    return dict(t='anim', name='pop_bgimg', img=name, at=0, **A)


def telop(text, x, y, size, at, until=None, plate=None, rot=0.0):
    o = dict(t='anim', name='pop_telop', text=text, x=x, y=y, size=size, at=at)
    if until is not None:
        o['until'] = until
    if plate:
        o['plate'] = plate
    if rot:
        o['rot'] = rot
    return o


def rows(items, y0, size=48, x0=150, x1=1770, gap=16):
    return dict(t='anim', name='pop_rows', items=items, x0=x0, x1=x1, y0=y0, size=size, gap=gap)


def row(text, tag, col, at, until=None, **kw):
    o = dict(at=at, text=text, tag=tag, col=col)
    if until is not None:
        o['until'] = until
    o.update(kw)
    return o


spec = dict(
    slug='sigdeepseek',
    theme_dir='20261104_signal',
    pack='sigcmp_sigdeepseek',
    header_sub='信号の「青」を、法令と言葉から確かめる',
    style='pop',
    images={
        'intro': dict(file='assets/sigcmp/art_intro.png'),
        'law': dict(file='assets/sigcmp/art_law.png'),
        'world': dict(file='assets/sigcmp/art_world.png'),
    },
    bgm=[['intro', 'language', 'acoustic45'], ['world', 'end', 'piano37']],
    chapters=[
        # ---------------------------------------------------------- 章1 導入
        dict(key='intro', title='信号の青は、緑じゃない？', chapter_title='導入：信号の青は、緑じゃない？', scene=[
            bg('intro'),
            telop('青なのに緑に見える', 960, 300, 104, at=0, until=2, plate='yellow', rot=-1.5),
            rows([row('青信号と呼ぶのに見た目は緑に近い', 'ふしぎ', 'orange', 1, 2)], 520, size=50),
            rows([row('日本語の「青」の歴史から来た呼び方（とされる）', '由来', 'orange', 2, 4)], 300, size=48),
            rows([row('法令と言葉の2つの面から、確かめる', 'この動画', 'green', 3)], 450, size=50),
        ]),
        # ---------------------------------------------------------- 章2 法令
        dict(key='law', title='法令では何色？', chapter_title='法令では何色？', scene=[
            bg('law'),
            telop('法令', 960, 300, 120, at=0, until=1, plate='yellow', rot=-2),
            telop('「青色の灯火」', 960, 430, 120, at=1, until=4, plate='yellow', rot=-2),
            rows([row('道路交通法施行令に、こう書いている', '第2条', 'orange', 1, 2)], 650, size=46),
            rows([row('法令上の名前も「青色」', '名前', 'blue', 2, 3)], 650, size=52),
            rows([row('実際に光る色は緑のなかでも青みが強い（とされる）', '実際の色', 'green', 3, 4)], 650, size=44),
            telop('名前は青 見た目は緑寄り', 960, 420, 100, at=4, until=5, plate='yellow', rot=1.5),
            telop('ここにずれがある', 960, 420, 100, at=5, plate='pink', rot=-1.5),
        ]),
        # ---------------------------------------------------------- 章3 日本初
        dict(key='history', title='日本初の信号機', chapter_title='日本で最初の3色信号', scene=[
            telop('1930年', 960, 230, 150, at=0, until=1, plate='yellow', rot=-2),
            rows([row('日比谷交差点に3色の灯火の信号機（とされる）', '場所', 'orange', 0, 1)], 400, size=46),
            dict(t='anim', name='pop_card', inner='img', img='intro', box=[660, 500, 1260, 830],
                 rot=-1.2, at=0, until=1, cap='交差点の信号機（イメージ）'),
            rows([row('進めの合図を「青」と呼ぶ言い方（その後広く定着）', '呼び方', 'orange', 1, 3),
                  row('英語の呼び名は、グリーンライト', '英語', 'blue', 2, 3)], 250, size=50),
            telop('「青」', 960, 640, 130, at=1, until=2, plate='yellow', rot=-2),
            telop('GREEN LIGHT', 960, 640, 96, at=2, until=3),
            rows([row('日本語だけが違う名前を付けたわけではない', '結論', 'green', 3)], 520, size=48),
        ]),
        # ---------------------------------------------------------- 章4 言葉
        dict(key='language', title='言葉の「青」', chapter_title='言葉の「青」', scene=[
            telop('「青」は緑も含む色だった？', 960, 210, 84, at=0, until=1),
            rows([row('昔の「青」は緑も含む広い色の名前（と考えられる）', '昔の言葉', 'orange', 0, 1)], 380, size=46),
            rows([row('緑のものにも「青」が付く', '例', 'green', 1, 2)], 250, size=50),
            telop('青葉', 666, 430, 60, at=1, until=2, plate='green'),
            telop('青菜', 900, 430, 60, at=1, until=2, plate='green'),
            telop('青りんご', 1194, 430, 60, at=1, until=2, plate='green'),
            rows([row('古い色名はあか・くろ・しろ・あおの4つ（説がある）', '色名', 'orange', 2, 3)], 210, size=46),
            telop('あか', 420, 430, 76, at=2, until=3, plate='red'),
            telop('くろ', 780, 430, 76, at=2, until=3, plate='purple'),
            telop('しろ', 1140, 430, 76, at=2, until=3, plate='white'),
            telop('あお', 1500, 430, 76, at=2, until=3, plate='blue'),
            rows([row('信号の青もこの使い方を受け継いだ名前（と説明される）', '信号', 'orange', 3)], 400, size=46),
        ]),
        # ---------------------------------------------------------- 章5 世界
        dict(key='world', title='他の国では？', chapter_title='他の国では？', scene=[
            bg('world'),
            telop('青と緑の区別は一様ではない', 960, 220, 76, at=0, until=1),
            rows([row('青信号は「パランブル」（青い火）', '韓国語', 'blue', 1, 3),
                  row('青と緑の両方を指す色の言葉がある', 'ベトナム語', 'green', 2, 3)], 300, size=50),
            telop('色の名前の切り方は言語で違う', 960, 620, 84, at=3),
        ]),
        # ---------------------------------------------------------- 章6 結論
        dict(key='end', title='結論', chapter_title='結論', scene=[
            telop('青信号の「青」', 960, 280, 120, at=0, until=1, plate='yellow', rot=-1.5),
            rows([row('見た目ではなく日本語の「青」の使い方（と考えられる）', '名前', 'orange', 1, 4)], 230, size=46),
            rows([row('法令の名前も青色 光る色は緑寄り', '法令', 'blue', 2, 4)], 380, size=50),
            telop('緑に見えるのは間違いではない', 960, 620, 84, at=3, until=4),
            telop('信号を待つ間に思い出して', 960, 620, 72, at=4),
        ]),
    ],
    desc=dict(
        title_main='信号の「青」は、なぜ緑色に見えるのか',
        title_no=1,
        titles=[
            '信号の青は、なぜ緑に見える？ 法令と言葉から確かめる',
            '青信号なのに緑色。その理由を「青」の歴史からたどる',
            '青信号はなぜ「青」？ 道路交通法施行令と日本語の色名から考える',
        ],
        intro='信号の青は、緑色に見えませんか。青信号と呼ぶのに、見た目は緑に近い。この動画では、その理由を、法令と言葉の2つの面から確かめます。道路交通法施行令は、信号の灯火の意味を「青色の灯火」と書いています。一方、実際に光る色は緑寄りだとされます。日本語の「青」は、昔は緑も含む広い色の名前だったと考えられており、韓国語やベトナム語でも、青と緑の切り方は一様ではありません。',
        points=[
            '道路交通法施行令では、信号の灯火の意味を「青色の灯火」と書いています（第2条。e-Gov法令検索で条文を確認できます）。',
            '実際に光る色は、緑のなかでも青みの強い色にされているとされます（この点は規格の原文を確認できていません）。',
            '日本で3色の灯火を使う信号機が日比谷交差点に置かれたのは1930年とされます（警察庁・警視庁の沿革として紹介されることが多い、という意味です）。',
            '日本語の「青」は、昔は緑も含む広い色の名前だったと考えられています。青葉・青菜・青りんごのように、緑のものにも「青」が付きます。',
            '古い日本語の色名が、あか・くろ・しろ・あおの4つだったという説があります。',
            '韓国語では青信号を「パランブル」と言い、ベトナム語には青と緑の両方を指す色の言葉があるとされます。',
        ],
        refs=[
            '道路交通法施行令 第2条（灯火の意味。e-Gov法令検索）:https://elaws.e-gov.go.jp/',
            '警察庁・警視庁の沿革（3色灯式信号機の設置。未確認）',
            '国語辞典「あお」の項（古い色名についての説。未確認）',
            '韓国語・ベトナム語の辞書（파란불、xanh。未確認）',
        ],
        credit_lines=[
            '・背景のイラスト:ChatGPT(OpenAI)による生成イラスト（イメージです。実際の交差点・信号機の写真ではありません）',
        ],
        notes=[
            'この動画で条文として確認したのは、道路交通法施行令 第2条（「青色の灯火」）です。',
            '光る色の規格、1930年の日比谷交差点の設置、古い色名の説、韓国語・ベトナム語の語は、いずれも未確認です。本文では「とされる」「説がある」「と考えられる」と、確認できた範囲を限って述べています。',
            'イラストはイメージで、実際の交差点・信号機を写したものではありません。',
        ],
        tags='信号, 青信号, 道路交通法, 色の名前, 日本語, 韓国語, ベトナム語, 雑学, 言葉, 解説',
        checks=[
            '道路交通法施行令 第2条の原文を、公開前にもう一度 e-Gov で開いて確認する。',
            '1930年・日比谷交差点、色の規格、韓国語・ベトナム語の語は未確認のままなので、断定に直さない。',
        ],
    ),
)

(R / 'data' / 'sigdeepseek_spec.json').write_text(
    json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8')
print('spec written')
