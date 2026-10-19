"""Build data/oke_spec.json for the Okehazama explainer.

Every scene item's 'at' is a SENTENCE index inside the chapter (see 09_script_v2.md), not seconds.
Run:  .venv\\Scripts\\python.exe scripts\\make_spec_oke.py
"""
import json
from pathlib import Path

import oke_maps  # 地図の画素位置は、地図を作った式（oke_maps.map_at）から直接もらう

ROOT = Path(__file__).resolve().parents[1]
MAPS = 'assets/okehazama/'
GSI = 'https://cyberjapandata.gsi.go.jp/xyz/hillshademap/{z}/{x}/{y}.png'

images = {
    'situ': dict(file=MAPS + 'map_situ.png',
                 credit='自作図「合戦前の情勢図」（国土地理院「陰影起伏図」を加工）', source_url=GSI),
    'march': dict(file=MAPS + 'map_march.png',
                  credit='自作図「両軍の動き」（国土地理院「陰影起伏図」を加工）', source_url=GSI),
    'field': dict(file=MAPS + 'map_field.png',
                  credit='自作図「桶狭間の周辺」（国土地理院「陰影起伏図」を加工）', source_url=GSI),
}

_AT = {n: oke_maps.map_at(n) for n in ('map_situ', 'map_march', 'map_field')}


def map_pt(name, key):
    """地図画像の中の位置（左上=(0,0)、右下=(1,1)）。key は地点名か (lon,lat)。"""
    x, y = _AT[name](key)
    m = oke_maps.MAPS[name]
    return [round(x / m[5], 4), round(y / m[6], 4)]


def march_in(name, frm, to, margin=0.03):
    """地図の外から来る軍勢は、地図の縁の少し外で切った入口から動かす（画面外を延々と歩かせない）。"""
    a, b = map_pt(name, frm), map_pt(name, to)
    if all(-margin <= v <= 1 + margin for v in a):
        return a
    ts = [t for i in (0, 1) if b[i] != a[i]
          for t in ((v - a[i]) / (b[i] - a[i]) for v in (-margin, 1 + margin)) if 0 < t < 1]
    t = max(ts) if ts else 1.0
    return [round(a[0] + (b[0] - a[0]) * t, 4), round(a[1] + (b[1] - a[1]) * t, 4)]

chapters = []

# ---------------------------------------------------------------- 1. 導入
chapters.append(dict(
    key='intro', title='導入：二万五千の大軍は、なぜ敗れたのか',
    chapter_title='導入：二万五千の大軍は、なぜ敗れたのか',
    opener='永禄三年五月十九日　尾張国・桶狭間', opener_until=1, opener_y=300,
    scene=[
        dict(t='chips', y=440, w=520, h=140, gap=50, size=54, items=[
            dict(text='今川 二万五千', at=1),
            dict(text='織田 三千未満', at=1),
            dict(text='大将 戦死', at=2)]),
        dict(t='big', at=3, y=650, size=52, col='gold',
             text='なぜ、大軍の大将が討たれたのか。'),
        dict(t='panel', box=[120, 745, 1800, 825], at=4, size=30,
             text='手がかり：ウィキペディア「桶狭間の戦い」と、記事が挙げる史料名'),
    ]))

# ---------------------------------------------------------------- 2. 情勢
chapters.append(dict(
    key='joukyou', title='合戦の前：尾張と今川のせめぎ合い',
    chapter_title='合戦の前の情勢',
    scene=[
        dict(t='image', name='situ', box=[40, 150, 956, 850]),
        dict(t='stack', x0=980, x1=1860, y0=170, ymax=845, size=29, gap=10, items=[
            dict(text='十五世紀末、今川氏親が駿河と遠江に領国を作る。', at=0, until=2),
            dict(text='尾張では、斯波氏の家臣・織田弾正忠家が力をつける。', at=1, until=3),
            dict(text='天文七年までに、織田信秀が那古野城を奪う。', at=2, until=4),
            dict(text='天文二十年、信秀の死で家督争いが起こる。', at=3, until=5),
            dict(text='山口教継が、鳴海城と笠寺城を今川方に渡す。', at=4, until=6),
            dict(text='大高城と沓掛城の一帯も、今川軍の手に落ちる。', at=5, until=7),
            dict(text='四つの城が、尾張の中心部と知多半島を分断する。', at=6, until=8),
            dict(text='信長は村木砦を攻め落とし、鳴海城の周りに三つの砦を築く。', at=7, until=8),
            dict(text='大高城の周りにも、丸根砦と鷲津砦を築く。', at=8, until=9),
        ]),
    ]))

# ---------------------------------------------------------------- 3. 経過
chapters.append(dict(
    key='keika', title='五月十二日から、十九日へ',
    chapter_title='合戦までの経過',
    scene=[
        # 軍勢が地図の上を動く（vp_anim.oke_march）。legs=[[i0,i1]] は「文 i0 の開始から、文 i1 の開始まで」。
        dict(t='anim', name='oke_march', img='march', box=[40, 150, 956, 850], at=0,
             armies=[
                 # 今川軍：駿府方面から地図の東端を越えて沓掛城へ（5/12 出陣 → 5/18 到着）、
                 #          のち本隊は沓掛城を出て桶狭間へ西進（5/19）
                 dict(col=(255, 150, 90), legs=[[0, 1], [11, 12]],
                      pts=[march_in('map_march', 'sunpu', 'kutsukake'),
                           map_pt('map_march', 'kutsukake'),
                           map_pt('map_march', 'okehazama_den')]),
                 # 織田軍：清洲城（四時ごろ出発）→ 熱田神宮（八時ごろ）→ 善照寺砦（十時ごろ）
                 dict(col=(120, 190, 255), legs=[[6, 8], [8, 9]],
                      pts=[map_pt('map_march', 'kiyosu'), map_pt('map_march', 'atsuta'),
                           map_pt('map_march', 'zenshoji')]),
             ]),
        dict(t='stack', x0=980, x1=1860, y0=170, ymax=845, size=28, gap=9, items=[
            dict(text='五月十二日、義元が駿府を出陣。', at=0, until=2),
            dict(text='十八日、義元は沓掛城に入る。', at=1, until=3),
            dict(text='同じ夜、松平元康が大高城へ兵糧を届ける。', at=2, until=4),
            dict(text='織田方の軍議では、具体策が出なかった。', at=3, until=5),
            dict(text='十九日未明、元康が丸根砦と鷲津砦を攻める。', at=4, until=6),
            dict(text='信長は飛び起き、『敦盛』を舞って支度する。', at=5, until=8),
            dict(text='四時ごろ、清洲城を出発。', at=6, until=10),
            dict(text='供をしたのは、小姓衆の五騎だけ。', at=7, until=10),
            dict(text='八時ごろ、熱田神宮で黒煙を見る。', at=8, until=10),
            dict(text='十時ごろ、善照寺砦で二千から三千に整える。', at=9, until=11),
            dict(text='丸根の佐久間盛重、鷲津の飯尾定宗らが討死。', at=10, until=12),
            dict(text='義元の本隊は沓掛城を出て、大高方面へ西進。', at=11, until=12),
        ]),
    ]))

# ---------------------------------------------------------------- 4. 合戦
chapters.append(dict(
    key='kessen', title='桶狭間の合戦',
    chapter_title='桶狭間の合戦',
    scene=[
        dict(t='stack', x0=60, x1=1860, y0=170, ymax=845, size=31, gap=10, items=[
            dict(text='正午ごろ、佐々政次と千秋四郎の三百人ほどが、単独で今川軍の前衛に攻めかかる。', at=0, until=3),
            dict(text='しかし、逆に討ち取られてしまう。', at=1, until=3),
            dict(text='砦を順調に落とした義元は喜び、謡をうたわせた。', at=2, until=3),
        ]),
        # この章の図は「桶狭間山はどこか」を見るためのもの。どの候補地へ進んだかを描くと
        # 一つの説を選んだことになるので、軍勢の移動は経過の章（行軍図）にだけ入れる。
        dict(t='image', name='field', box=[40, 150, 956, 850], at=3, until=7),
        dict(t='stack', x0=980, x1=1860, y0=170, ymax=845, size=28, gap=12, items=[
            dict(text='義元が本隊を布陣して休息していたのは、「桶狭間山」という山だった。', at=3, until=7),
            dict(text='午後一時ごろ、視界を妨げるほどの豪雨が降る。', at=4, until=7),
            dict(text='『信長公記』には「石氷を投げ打つ様に」とあり、雹だった可能性も指摘される。', at=5, until=7),
            dict(text='織田軍はこれに乗じて兵を進め、義元の本隊に攻めかかった。', at=6, until=7),
        ]),
        dict(t='big', at=7, y=330, size=42, col='gold', until=10,
             text='ただし、豪雨の中の奇襲ではなく、雨が止んでから正面から攻めた、という見方もある。'),
        dict(t='stack', x0=60, x1=1860, y0=520, ymax=845, size=36, gap=20, items=[
            dict(text='今川軍の総勢は二万五千とされるが、荷駄兵なども多く含まれていた。', at=8, until=10),
            dict(text='兵を分散させていたため、義元を守る実際の兵力は少なかったとされる。', at=9, until=10),
        ]),
        dict(t='stack', x0=60, x1=1860, y0=170, ymax=845, size=31, gap=10, items=[
            dict(text='義元の本陣の前衛は、織田軍と接すると、戦わずに崩れ去った。', at=10, until=16),
            dict(text='織田軍はその混乱に乗じて、本陣を目指して突撃した。', at=11, until=16),
            dict(text='義元は輿を捨て、三百人の旗本に守られて、馬で逃げた。', at=12, until=16),
            dict(text='しかし五度にわたる攻撃で周りの兵を失い、馬廻に追いつかれる。', at=13, until=16),
        ]),
        dict(t='big', at=14, y=545, size=48, col='gold', until=16,
             text='義元は自ら太刀を抜いて戦い、毛利新介に組み伏せられ、首を討ち取られた。'),
        dict(t='panel', box=[60, 650, 1860, 720], at=16, size=31,
             text='享年四十二歳。討たれた場所は、今川家の資料では「田楽窪」と記される。'),
        dict(t='panel', box=[60, 735, 1860, 800], at=17, size=31, col='gold',
             text='大将を失った今川軍は総崩れとなり、合戦は織田軍の勝利に終わった。'),
    ]))

# ---------------------------------------------------------------- 5. 兵力
chapters.append(dict(
    key='heiryou', title='兵力は、どれくらいだったのか',
    chapter_title='兵力は、どれくらいだったのか',
    scene=[
        dict(t='panel', box=[60, 155, 1860, 215], at=0, size=31,
             text='今川軍の兵力は、史料によって数字が違う。'),
        dict(t='table', box=[60, 230, 1860, 630], size=26,
             cols=['史料', '兵力'], colw=[820, 900], rows=[
                 dict(cells=['『信長公記』', '四万五千'], at=1),
                 dict(cells=['『甲陽軍鑑』', '二万余'], at=1),
                 dict(cells=['『武功夜話』', '三万有余'], at=1),
                 dict(cells=['『徳川実紀』など', '四万余'], at=2),
                 dict(cells=['『絵本太閤記』', '五万余'], at=2),
                 dict(cells=['陸軍参謀本部『日本戦史 桶狭間役』', '二万五千'], at=3, col='gold'),
                 dict(cells=['小和田哲男（石高から）', '二万五千'], at=4, col='gold'),
             ]),
        dict(t='panel', box=[60, 640, 1860, 700], at=5, size=28, col='gold',
             text='一方、二万五千でも多すぎる、という異論も唱えられている。'),
        dict(t='chips', y=710, w=600, h=112, gap=70, size=44, items=[
            dict(text='織田 約2,000', at=6, until=8),
            dict(text='今川 5,000〜6,000', at=7, until=8)]),
        dict(t='big', at=8, y=700, size=44, col='gold',
             text='数字は、一つに決まっていない。'),
    ]))

# ---------------------------------------------------------------- 6. 見方
chapters.append(dict(
    key='kaishaku', title='なぜ勝てたのか、いくつもの見方',
    chapter_title='なぜ勝てたのか：いくつもの見方',
    scene=[
        dict(t='stack', x0=60, x1=1860, y0=170, ymax=845, size=26, gap=10, items=[
            dict(text='合戦がどのように行われたかも、議論があります。', at=0, until=5, hi=True),
            dict(text='信長は義元の居場所を知り、密かに迂回して、豪雨に乗じて丘の上から奇襲した、という説。'
                      '江戸時代の小瀬甫庵『信長記』で取り上げられ、長く定説とされました。',
                 title='一つ目　迂回攻撃説', at=1, until=5),
            dict(text='信長は中嶋砦まで進み、雨のあと、桶狭間山の今川軍に正面から攻めかかった、という説。'
                      '太田牛一『信長公記』に基づき、前軍が突破された乱戦が本陣になだれ込んだ、とします。',
                 title='二つ目　正面攻撃説', at=5, until=9),
            dict(text='現在は、迂回攻撃説には否定的な見解が多いとされています。', at=8, until=13, col='red'),
            dict(text='別動隊による、背後からの奇襲を組み合わせた説。', title='三つ目　別動隊説', at=9, until=13),
            dict(text='義元が酒宴を開いていたところを襲った、という『甲陽軍鑑』の記述を評価する説。',
                 title='四つ目　酒宴説', at=10, until=13),
            dict(text='義元が三河へ戻る途中で攻められた、という説。', title='五つ目　三河戻り説', at=11, until=13),
            dict(text='『信長公記』を重んじる立場では、信長は義元の居場所を知らず、偶然に本陣へ突撃した、と考えます。',
                 title='六つ目　偶然説', at=12, until=13),
            dict(text='つまり桶狭間の勝利は、いくつもの条件が重なった結果だ、という解釈になります。',
                 at=13, until=14, hi=True),
        ]),
    ]))

# ---------------------------------------------------------------- 7. 戦場
chapters.append(dict(
    key='senjou', title='戦場は、どこだったのか',
    chapter_title='戦場は、どこだったのか',
    scene=[
        dict(t='image', name='field', box=[40, 150, 956, 850]),
        dict(t='stack', x0=980, x1=1860, y0=170, ymax=845, size=26, gap=9, items=[
            dict(text='戦場の場所も、はっきりとは分かっていない。', at=0, until=2, hi=True),
            dict(text='義元が本陣を置いた「桶狭間山」の位置が、議論になっている。', at=1, until=3),
            dict(text='藤本正行：一つの丘ではなく、中嶋砦の東側の丘陵の一帯。', at=2, until=5),
            dict(text='小和田哲男：豊明市の古戦場の南方、標高六十四・七メートルの地点。', at=3, until=5),
            dict(text='小島廣次：その丘の北側の高地との間の鞍部に本陣があった。', at=4, until=6),
            dict(text='磯田道史：江戸時代の『天保十一年道中日記』を紹介。', at=5, until=7),
            dict(text='そこには、義元の戦死の場所と、七人の武将の墓が書かれていた。', at=6, until=8),
            dict(text='現在、桶狭間古戦場は豊明市と名古屋市緑区の二か所にある。', at=7, until=9),
            dict(text='小和田哲男：どちらの古戦場も本物だ、としている。', at=8, until=9),
        ]),
    ]))

# ---------------------------------------------------------------- 8. あと
chapters.append(dict(
    key='sengo', title='合戦のあと',
    chapter_title='合戦のあと',
    scene=[
        dict(t='panel', box=[60, 160, 1860, 222], at=1, until=4, size=28,
             text='大高城の松平元康は、義元の戦死を聞くと大高城を退去した。'),
        dict(t='timeline', y=330, x0=150, x1=1780, w=310, size=28, ymax=560, nodes=[
            dict(x=270, label='5/19', col='red', at=0, sub='義元、戦死'),
            dict(x=610, label='5/23', col='blue', at=2, sub='元康、岡崎城へ'),
            dict(x=950, label='6/21', col='org', at=3, sub='沓掛城を攻略'),
            dict(x=1290, label='2年後', col='blue', at=5, sub='今川氏と手を切る'),
            dict(x=1630, label='永禄11年', col='vio', at=9, sub='三国同盟の終わり'),
        ]),
        dict(t='panel', box=[60, 560, 1860, 616], at=4, until=10, size=28,
             text='西三河から尾張にかけての今川氏の勢力は、一掃された。'),
        dict(t='panel', box=[60, 626, 1860, 682], at=6, until=10, size=28,
             text='信長は東の危険を取り除き、美濃の斎藤氏との戦いに専念できるようになった。'),
        dict(t='panel', box=[60, 692, 1860, 748], at=7, until=10, size=28,
             text='三国同盟の一角の当主が討たれ、越後の長尾景虎が勢いづいた。'),
        dict(t='panel', box=[60, 758, 1860, 814], at=8, until=10, size=26,
             text='武田氏と今川氏の関係も悪化した。'),
        dict(t='big', at=10, y=700, size=40, col='gold', until=11,
             text='同年十二月、武田氏による駿河への侵攻が始まった。'),
        dict(t='panel', box=[60, 780, 1860, 848], at=11, size=28, col='gold',
             text='桶狭間の戦いは、戦国時代の転機の一つになった。'),
    ]))

# ---------------------------------------------------------------- 9. まとめ
chapters.append(dict(
    key='matome', title='分かること、決められないこと',
    chapter_title='分かること、決められないこと',
    scene=[
        dict(t='cols2', size=30, xm=940, xm2=980, left=dict(
            title='分かること', title_at=0, items=[
                dict(at=1, text='信長が義元の本陣を攻め、義元を討ち取ったこと'),
                dict(at=2, text='義元の戦死地は「田楽窪」とされ、地名が残ること')]),
            right=dict(title='決められないこと', title_at=3, items=[
                dict(at=4, text='奇襲だったのか、正面攻撃だったのか'),
                dict(at=5, text='「桶狭間山」が、どこにあったのか')])),
        dict(t='panel', box=[60, 560, 1860, 620], at=6, size=27,
             text='この動画の主要な記述は、公開されている史料の翻刻でも確かめている。'),
        dict(t='panel', box=[60, 630, 1860, 690], at=7, size=27,
             text='ただし、原本や専門書までは確認できていない。'),
        dict(t='panel', box=[60, 700, 1860, 760], at=8, until=10, size=27,
             text='誤りがあれば、コメントで教えてください。確認のうえ、訂正します。'),
        dict(t='big', at=10, y=790, size=40, col='gold',
             text='また、別の動画でお会いしましょう。'),
    ]))

spec = dict(
    slug='oke', theme_dir='20261019_okehazama', pack='14_okehazama',
    header_sub='ウィキペディアの記事と史料名から、桶狭間の戦いを確かめる',
    images=images,
    bgm=[['intro', 'keika', 'ethnic06'], ['kessen', 'kaishaku', 'ethnic26'], ['senjou', 'matome', 'piano36']],
    chapters=chapters,
    desc=dict(
        title_main='二万五千の大軍は、なぜ敗れたのか：桶狭間の戦い',
        title_no=1,
        titles=[
            '二万五千の大軍は、なぜ敗れたのか？ 桶狭間の戦いを史料の数字から確かめる',
            '桶狭間の戦い：義元はなぜ討たれたのか。兵力・経過・戦場の謎をたどる',
            '桶狭間の戦いの兵力は本当に二万五千だったのか。諸説と地形を整理する',
        ],
        intro='永禄三年五月十九日、尾張国の桶狭間で、今川義元の大軍と織田信長の軍がぶつかりました。'
              '二万五千ともいわれる大軍を率いた義元が、三千にも満たない信長の軍に討たれた、という展開で知られます。'
              'この動画では、ウィキペディア日本語版「桶狭間の戦い」の記事と、そこに示された史料名を手がかりに、'
              '合戦までの経過、兵力をめぐる数字の違い、勝因をめぐる諸説、戦場の場所の議論を整理します。'
              '分かることと、決められないことを分けて見ていきます。',
        points=[
            '永禄三年五月十九日、桶狭間で今川義元が討たれ、織田軍が勝利しました。義元の兵力は二万五千とされますが、'
            '『信長公記』四万五千、『甲陽軍鑑』二万余、『武功夜話』三万有余、『徳川実紀』など四万余、'
            '『絵本太閤記』五万余と、史料によって数字が違います。',
            '戦前に広く使われた二万五千は、陸軍参謀本部『日本戦史 桶狭間役』の数字で、'
            '小和田哲男さんは義元の領地を九十万石から百万石と見て二万五千としました。'
            '一方、太田満明さんや橋場日月さんなど、二万五千でも多すぎるという異論を唱える論者もいます。',
            '合戦の行われ方には、迂回攻撃説（小瀬甫庵『信長記』）、正面攻撃説（太田牛一『信長公記』）、'
            '別動隊説（橋場日月）、酒宴説（黒田日出男が評価する『甲陽軍鑑』の記述）、三河戻り説、偶然説など、'
            'いくつもの見方があります。現在は迂回攻撃説には否定的な見解が多いとされます。',
            '義元が本陣を置いた「桶狭間山」の位置は決まっておらず、藤本正行・小和田哲男・小島廣次らの説があります。'
            '桶狭間古戦場は豊明市と名古屋市緑区の二か所にあり、小和田哲男さんはどちらも本物だとしています。',
            'この動画は、ウィキペディアの記事を手がかりにしています。主要な記述は、公開されている史料の翻刻'
            '（『信長公記』『甲陽軍鑑』）でも確かめましたが、原本・影印本や専門書は確認していません。'
            '地図は国土地理院の陰影起伏図（現在の地形）に、記事の記述から位置関係を模式的に重ねた自作図です。',
        ],
        refs=[
            'ウィキペディア日本語版「桶狭間の戦い」:https://ja.wikipedia.org/wiki/桶狭間の戦い',
            '国土地理院 地理院タイル（陰影起伏図）:https://cyberjapandata.gsi.go.jp/xyz/hillshademap/{z}/{x}/{y}.png',
            '国土地理院 住所検索API（地点の座標の取得に使用）:https://msearch.gsi.go.jp/address-search/AddressSearch',
        ],
        credit_lines=[
            '・地図（合戦前の情勢図・両軍の動き・桶狭間の周辺）:自作（国土地理院「陰影起伏図」を加工。'
            '現在の地形に、記事の記述から位置関係を模式的に重ねたもので、当時の地形・道筋の再現ではありません）',
            '・サムネイルの背景:自作（同じ地図素材を加工）',
            '・場面のイラスト:ChatGPT（OpenAI）による生成イラスト（イメージです。実際の場面・人物・資料の再現ではありません）',
        ],
        notes=[
            '地図の矢印と、地図の上で動く軍勢の印（今川軍＝橙、織田軍＝青）は、両軍の位置関係を示す模式で、'
            '実際の行軍路・時刻ではありません。地点の座標は住所検索APIが'
            '返す大字の代表点で、史跡そのものの位置ではありません。数百メートルから1キロメートル以上、'
            'ずれている地点があります。',
            '原史料は、公開されている翻刻（『信長公記』『甲陽軍鑑』）で確認しました。原本・影印本と専門書は'
            '確認していません。内容はウィキペディア日本語版「桶狭間の戦い」の記事と、そこに示された史料名に'
            '基づいています。',
            '確認の結果、佐々政次と千秋四郎の部隊を三十人余りから三百人ほどに、豪雨の記述を『信長公記』の'
            '「石氷を投げ打つ様に」に直しました。',
            '誤りがあればコメントでお知らせください。確認のうえ、訂正します。',
        ],
        tags='桶狭間の戦い,織田信長,今川義元,戦国時代,日本史,歴史,桶狭間,田楽窪,松平元康,兵力,諸説',
        checks=[
            '原史料・専門書の確認は着手済み。原史料は『信長公記』『甲陽軍鑑』の公開翻刻まで、専門書は書誌まで（本文は未読）',
            '地図の地点座標は史跡の位置と比較した（差は67m〜2.1km。正しい座標への差し替えは未了）',
            '「桶狭間山」の諸説の要約の確認は済み（小島廣次の「鞍部」は記事内で食い違いがあり、断定を避けた）',
            '生成イラスト6枚が、実在の人物・場所・作品の再現に見えないか（顔・文字・家紋が入っていないか）確認する',
        ],
    ),
    thumb=dict(
        bg='assets/okehazama/thumb_art.png',
        lines=[['桶狭間の戦い', 84, 'white'],
               ['二万五千の大軍は', 84, 'white'],
               ['なぜ敗れたのか', 124, 'gold']],
        sub='兵力・経路・戦場の謎を、史料の数字からたどる',
        y0=24, bar_y=520, bar_w=700, sub_size=38, shade_x=740, shade_w=540,
    ),
)

# ---------------------------------------------------------------- 生成イラスト（背景）
# 地図のある章（joukyou / keika / senjou）は図で足りるので敷かない。それ以外の章は、
# 文字の後ろに場面の挿絵を敷く（挿絵はイメージで、実際の場面の再現ではない）。
# 注意書きは、どの章でも空いている header の右（y=100）に逃がす（vp.py it_art の note_y）。
ART = [
    ('intro',    'field_dusk',   1),
    ('kessen',   'downpour',    -1),
    ('heiryou',  'old_records',  1),
    ('kaishaku', 'war_council', -1),
    ('sengo',    'quiet_field',  1),
    ('matome',   'old_book',    -1),
]
ART_NOTE = 'イメージ（生成画像）。実際の場面の再現ではありません'
for key, name, direction in ART:
    images[name] = dict(file=MAPS + f'art_{name}.png')
    ch = next(c for c in chapters if c['key'] == key)
    box = [60, 170, 1860, 850]
    ch['scene'][:0] = [
        dict(t='art', name=name, box=box, at=0, dim=1.0, dir=direction, drift=36,
             note=ART_NOTE, note_y=100),
        dict(t='shade', box=box, at=0, alpha=0.48),
    ]

out = ROOT / 'data' / 'oke_spec.json'
out.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8')
print(out, len(chapters), 'chapters')
for c in chapters:
    n = max((it.get('at', 0) for it in c['scene']), default=0)
    print(f"  {c['key']:10s} items={len(c['scene']):2d} max_at={n}")
