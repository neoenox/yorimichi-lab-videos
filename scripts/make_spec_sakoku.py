"""Writes data/sakoku_spec.json（ポップスタイル・地図つき）。台本：docs/themes/20270602_sakoku/09_script_v2.md
at / until は『章内の行番号（0始まり）』。素材は scripts/make_sakoku_assets.py（国土地理院のタイルから地図を作る）。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize, TOP
IMAGES = {n: dict(file=f'assets/sakoku/{n}.png') for n in ('art_intro', 'art_gate', 'art_scroll', 'map_s0', 'map_s1', 'map_s2', 'map_s3', 'map_s4')}


def pop(name, **kw):
    return dict(t='anim', name=name, **kw)


def tel(text, x, y, size, **kw):
    return dict(t='anim', name='pop_telop', text=text, x=x, y=y, size=size, **kw)


def rows(items, **kw):
    return dict(t='anim', name='pop_rows', items=items, **kw)


def card(inner, box, **kw):
    kw.setdefault('at', 0)
    return dict(t='anim', name='pop_card', inner=inner, box=box, **kw)


MAPBOX = [60, 120, 900, 860]


def mapcard(n, at, until=None):
    kw = dict(img=f'map_s{n}', at=at, rot=-1.5)
    if until is not None:
        kw['until'] = until
    return card('img', MAPBOX, **kw)


spec = dict(slug='sakoku', theme_dir='20270602_sakoku', pack='77_sakoku', header_sub='解説記事と地図で、鎖国と四つの窓口を確かめる',
 images=IMAGES,
 bgm=[['intro', 'mado', 'piano36'], ['yuiitsu', 'kinshi', 'piano12'], ['wakaranai', 'end', 'piano40']],
 style='pop',
 chapters=[
 {'key': 'intro', 'title': '江戸時代の日本は、鎖国をして、長崎でしか外国と付き合わなかった？', 'chapter_title': '導入：鎖国で、外国との窓口は長崎だけ？',
  'scene': [pop('pop_bgimg', img='art_intro', at=0, dim=.5, blur=3),
            tel('鎖国で\n窓口は[[長崎だけ]]？', 960, 470, 170, at=0, until=1, rot=-3),
            tel('答え：窓口は[[4つ]]あった！', 960, 470, 130, at=1, until=2, plate='green', rot=-2),
            tel('荒野泰典さんの解説記事 ×', 960, 330, 80, at=2, plate='blue', rot=1),
            tel('[[地図]]で確かめる！', 960, 600, 150, at=2, rot=-2)]},
 {'key': 'mado', 'title': '四つの窓口', 'chapter_title': '四つの窓口',
  'scene': [pop('pop_bgimg', img='map_s0', at=0, dim=.4, blur=12),
            mapcard(0, 0, 1), mapcard(1, 1, 2), mapcard(2, 2, 3), mapcard(3, 3, 4), mapcard(4, 4),
            tel('窓口は\n[[4つ]]！', 1400, 300, 130, at=0, until=1, rot=-3),
            rows([dict(at=1, tag='長崎', text='オランダ・中国', col='orange'),
                  dict(at=2, tag='対馬', text='朝鮮', col='blue'),
                  dict(at=3, tag='薩摩', text='琉球', col='green'),
                  dict(at=4, tag='松前', text='蝦夷地', col='purple')], x0=950, x1=1860, y0=190, size=60, gap=26),
            tel('出典：荒野泰典「「四つの口」と長崎貿易」（nippon.com）', 1400, 810, 36, at=1)]},
 {'key': 'yuiitsu', 'title': '唯一の窓口ではない', 'chapter_title': '唯一の窓口ではない',
  'scene': [pop('pop_bgimg', img='art_gate', at=0, dim=.5, blur=4),
            tel('長崎だけ？\n[[成り立たない]]', 960, 420, 150, at=0, until=1, plate='red', rot=-2),
            tel('と、記事は述べる', 960, 720, 80, at=0, until=1, plate='yellow', rot=1.5),
            rows([dict(at=1, tag='提唱', text='「四つの口」＝荒野泰典さん（1978年）', col='orange')], x0=110, x1=1810, y0=330, size=64, gap=34),
            tel('朝鮮通信使 [[12回]]\n琉球使節 [[18回]]', 960, 700, 110, at=2, plate='blue', rot=-1.5)]},
 {'key': 'kinshi', 'title': '禁じたことと、鎖国という言葉', 'chapter_title': '禁じたことと、鎖国という言葉',
  'scene': [pop('pop_bgimg', img='art_scroll', at=0, dim=.5, blur=4),
            tel('でも、[[禁じたこと]]も！', 960, 250, 110, at=0, until=1, rot=-2),
            rows([dict(at=0, tag='1635年', text='中国人の来航地は、長崎だけに', col='red', until=1),
                  dict(at=0, tag='1639年', text='ポルトガルとの関係を断つ', col='red', until=1)], x0=110, x1=1810, y0=430, size=62, gap=40),
            tel('では、「鎖国」って\nどこから来た言葉？', 960, 470, 110, at=1, until=2, rot=2),
            tel('[[1801年]]\n志筑忠雄『鎖国論』', 960, 440, 130, at=2, until=3, plate='yellow', rot=-2),
            tel('国を閉ざした史実は…\n[[ない]]、と記事は述べる', 960, 460, 110, at=3, plate='pink', rot=2)]},
 {'key': 'wakaranai', 'title': '分からないこと', 'chapter_title': '分からないこと',
  'scene': [pop('pop_bgimg', img='art_intro', at=0, dim=.55, blur=6),
            tel('分からないこと', 960, 250, 120, at=0, rot=-2),
            rows([dict(at=0, tag='教科書', text='今の書き方は、未確認', col='orange'),
                  dict(at=0, tag='原文', text='『鎖国論』の原文は、未確認', col='red'),
                  dict(at=1, tag='研究者', text='四つの口の見方が、どこまで共有されているか', col='purple')], x0=110, x1=1810, y0=420, size=60, gap=34)]},
 {'key': 'end', 'title': 'まとめ', 'chapter_title': 'まとめ',
  'scene': [tel('窓口は[[4つ]]！\n鎖国は1801年の訳語', 960, 400, 130, at=0, until=1, rot=-2),
            tel('国を閉ざした史実は[[ない]]、と解説', 960, 700, 66, at=0, until=1, plate='green', rot=1.5),
            tel('[[国を閉ざした]]とは言えず、\n窓口は[[4つ]]あった', 960, 480, 120, at=1, plate='yellow', rot=-1.5)]}],
 desc={'title_main': '江戸時代の日本は鎖国をしていたのか',
 'title_no': 1,
 'titles': ['江戸時代の日本は、鎖国で外国は長崎だけだった？ 解説記事で確かめる', '鎖国は、1801年の訳語だった？ 窓口は四つあった？', '「鎖国」は本当に国を閉ざしていた？ 荒野泰典さんの解説で確かめる'],
 'intro': '「江戸時代の日本は鎖国をして、外国との付き合いは長崎だけだった」と習いませんでしたか。この動画では、立教大学名誉教授の荒野泰典さんの解説記事で、鎖国と海外との窓口を確かめます。',
 'points': ['荒野泰典さんの解説記事(nippon.com、2012年)によると、「鎖国」は国を閉ざすという意味のオランダ語を訳した言葉で、志筑忠雄が1801年の『鎖国論』で作ったとされます。国を閉ざした史実はない、と記事は述べます。',
            '海外との窓口は、長崎(オランダ・中国)、対馬(朝鮮)、薩摩(琉球)、松前(蝦夷地)の「四つの口」で、荒野さんが1978年に提唱した見方です。朝鮮通信使は1609〜1811年に12回、琉球の使節は1634〜1850年に18回来日しました。',
            '一方で、1635年に中国人の来航地が長崎に限られ、1639年にポルトガルと断交しました。今の教科書の書き方や『鎖国論』の原文は、今回確認できていません。'],
 'refs': ['荒野泰典「「四つの口」と長崎貿易――近世日本の国際関係再考のために――」nippon.com(二次情報):https://www.nippon.com/ja/features/c00104/'],
 'credit_lines': ['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
 'notes': ['読んだのは荒野泰典さんの解説記事の一本で、教科書の現在の書き方や、『鎖国論』の原文は確認していません。', '四つの口の見方が研究者の間でどこまで共有されているかは、今回確認できていません。', '数字(12回・18回など)は記事の記載で、原典は確認していません。'],
 'tags': '江戸時代, 鎖国, 四つの口, 長崎, 志筑忠雄, 荒野泰典, 検証',
 'checks': ['現在の教科書での「鎖国」の書き方を確認する', '『鎖国論』(1801年)の成立の事情を確認する', '朝鮮通信使・琉球使節の回数を別の資料で確認する']},
 thumb=dict(bg='assets/sakoku/thumb_art.png', lines=[['鎖国で、窓口は', 80, 'white'], ['長崎だけ？', 130, 'gold']], sub='解説記事で、確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))
finalize(spec, {})
