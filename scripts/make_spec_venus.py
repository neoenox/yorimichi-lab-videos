"""Writes data/venus_spec.json（金星では、1日が1年より長い？）。台本：docs/themes/20261108_venus/09_script_v2.md
ポップ形式（style='pop'）。台本・音声は変えず、画面だけを作り直した。旧版は make_spec_venus_before_pop.py。
at / until は台本の『行の番号』（章内の0始まり）。anim の s_a だけは『文の番号』（章内の0始まり）。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize
R = Path(__file__).resolve().parents[1]


def pop(name, **kw):
    return dict(t='anim', name=name, **kw)


def tel(text, x, y, size, **kw):
    return dict(t='anim', name='pop_telop', text=text, x=x, y=y, size=size, **kw)


def rows(items, **kw):
    return dict(t='anim', name='pop_rows', items=items, **kw)


def card(inner, box, **kw):
    kw.setdefault('at', 0)
    return dict(t='anim', name='pop_card', inner=inner, box=box, **kw)


SPIN = [60, 110, 1860, 690]
NL = chr(92) + 'n'

spec = dict(slug='venus', theme_dir='20261108_venus', pack='21_venus_day', header_sub='金星の自転と公転を、NASAの表で確かめる',
 style='pop',
 images={n: dict(file=f'assets/venus/{n}.png') for n in ('art_intro', 'art_nums', 'art_sun', 'art_why', 'art_end', 'chart_days')},
 bgm=[['intro', 'sun', 'piano36'], ['why', 'why', 'piano12'], ['end', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='金星では、一日が一年より長い？', chapter_title='導入：金星では、一日が一年より長い？', scene=[
   pop('pop_bgimg', img='art_intro', at=0, dim=.5, blur=3),
   tel('金星では\n一日が一年より[[長い]]？', 960, 440, 130, at=0, until=1, rot=-2),
   tel('「一日」を何と考えるかで\n[[答えが変わる]]', 960, 440, 108, at=1, until=2, plate='yellow', rot=2),
   tel('資料：NASAの表（Venus Fact Sheet）', 960, 440, 76, at=2, until=3, plate='blue', rot=-1.5),
   tel('分かることと、決められないことを\n分けて見る', 960, 440, 92, at=3, plate='pink', rot=1.5)]),
 dict(key='nums', title='星を基準にした、自転と公転', chapter_title='星を基準にした、自転と公転', scene=[
   pop('pop_bgimg', img='art_nums', at=0, dim=.5, blur=4),
   tel('遠くの星を基準にした\n[[自転周期]]は？', 960, 440, 120, at=0, until=1, rot=-2),
   rows([dict(at=1, tag='自転周期', text='5,832.6時間 ＝ 約243日', col='blue', until=4),
         dict(at=3, tag='公転周期', text='224.701日', col='orange', until=4)], x0=130, x1=1790, y0=260, size=64, gap=40),
   dict(t='shade', box=SPIN, at=4, alpha=0.62),
   pop('venusspin', box=SPIN, at=4, s_a=5, dur=9),
   tel('自転一回は、公転一周より約18日[[長い]]', 960, 770, 60, at=4, plate='red', rot=-1.2)]),
 dict(key='sun', title='太陽の動きで決める、一日', chapter_title='太陽の動きで決める、一日', scene=[
   pop('pop_bgimg', img='art_sun', at=0, dim=.5, blur=4),
   tel('もう一つの行：\n[[Length of day]]', 960, 440, 120, at=0, until=1, rot=-2),
   tel('赤道上の一点で、太陽が\n正午の位置に戻るまでの\n[[平均の時間]]', 960, 440, 84, at=1, until=2, plate='yellow', rot=1.5),
   card('img', [170, 250, 1750, 840], img='chart_days', at=2, until=5, rot=-1),
   tel('公転周期より[[短い]]', 960, 150, 84, at=3, until=4, plate='red', rot=-1.5),
   tel('地球は、ほぼ24時間', 960, 150, 84, at=4, until=5, plate='blue', rot=1.5)]),
 dict(key='why', title='なぜ、短くなるのか', chapter_title='なぜ、短くなるのか', scene=[
   pop('pop_bgimg', img='art_why', at=0, dim=.5, blur=4),
   tel('自転周期に[[マイナス]]の符号', 960, 440, 108, at=0, until=1, rot=-2),
   tel('NASA：マイナス＝[[逆向き]]の自転', 960, 440, 100, at=1, until=2, plate='blue', rot=1.5),
   tel('地球など多くの惑星と\n[[逆向き]]に自転', 960, 440, 108, at=2, until=3, plate='yellow', rot=-1.5),
   dict(t='shade', box=SPIN, at=3, until=5, alpha=0.62),
   pop('venusspin', box=SPIN, at=3, until=5, s_a=3, dur=16),
   tel('公転とは反対向きに自転', 960, 770, 60, at=3, until=4, plate='blue', rot=-1.2),
   tel('太陽が戻るのが[[早くなる]]', 960, 770, 60, at=4, until=5, plate='red', rot=1.2),
   tel('1/243.0 ＋ 1/224.7\n＝ 1/116.75', 960, 440, 128, at=5, until=6, plate='yellow', rot=-1.5),
   tel('NASAの表：116.75日\n[[ほぼ一致]]（自作の計算）', 960, 440, 112, at=6, plate='green', rot=1.5)]),
 dict(key='end', title='分かること、決められないこと', chapter_title='結論：分かること、決められないこと', scene=[
   pop('pop_bgimg', img='art_end', at=0, dim=.55, blur=6),
   rows([dict(at=0, tag='分かる', text='自転周期（約243日）は、公転周期（224.7日）より長い', col='green'),
         dict(at=1, tag='分かる', text='「自転一回」を一日とすれば、一日は一年より長い', col='green'),
         dict(at=2, tag='分かる', text='太陽の動きで決める一日は、約116.75日で一年より短い', col='green'),
         dict(at=4, tag='不明', text='金星の地表から、空が実際にどう見えるか', col='red')], x0=110, x1=1810, y0=170, size=50, gap=26),
   tel('一日の意味が違えば、[[答えも変わる]]', 960, 760, 72, at=3, until=4, plate='yellow', rot=-1)])
 ],
 desc=dict(title_main='金星では、一日が一年より長いのか', title_no=1,
  titles=['金星では、1日が1年より長い？ NASAの表で確かめる', '金星の「1日」は何日？ 自転と公転をNASAの表で確かめる', '金星の1日は1年より長い？ 「1日」の意味で答えが変わる理由'],
  intro='「金星では、一日が一年より長い」と聞いたことはありませんか。この動画では、NASAの金星のファクトシートの数字から、金星の自転と公転を確かめます。星を基準にした自転周期と公転周期、太陽の動きで決める一日、なぜ短くなるのか、を分けて見ていきます。「一日」を何と考えるかで、答えが変わります。分かることと決められないことを分けて、NASAの表に帰属して述べます。',
  points=['NASAの表では、金星の自転周期(遠くの星を基準にした一回転の時間)は5,832.6時間(符号はマイナスで逆向き)、公転周期は224.701日です。自転周期を24時間=1日で換算すると約243日で、公転周期より約18日長くなります(NASA Venus Fact Sheet、日数への換算と差は自作の計算)。', '同じ表の「Length of day」は、赤道上の地点で太陽が正午の位置に戻るまでの平均の時間で(NASAのNotes)、金星では2,802.0時間=116.75日です。公転周期224.701日より短い時間です(NASA Venus Fact Sheet)。', '金星の自転は公転とは反対向きなので、二つの動きは金星から見た太陽の向きを同じ向きに動かし、太陽が元の位置に戻るのが早くなります。1/243.025+1/224.701≒1/116.75 の計算は、小数第2位まで、NASAの値と一致します(自作の計算)。', 'NASAの表では天王星の自転周期にもマイナスが付いており、金星だけが逆向きではありません(NASA Uranus Fact Sheet)。'],
  refs=['NASA NSSDC「Venus Fact Sheet」:https://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html', 'NASA NSSDC「Notes on the Fact Sheets」:https://nssdc.gsfc.nasa.gov/planetary/factsheet/planetfact_notes.html', 'NASA NSSDC「Uranus Fact Sheet」:https://nssdc.gsfc.nasa.gov/planetary/factsheet/uranusfact.html'],
  credit_lines=['・図・グラフ・計算:自作(NASAの表の数字をもとにした模式図です。実際の金星の見え方ではありません)', '・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実際の金星の姿・景色の再現ではありません)'],
  notes=['図は、NASAの表の周期をもとにした自作の模式図で、実際の金星の見え方ではありません。', '金星の地表から実際に空がどう見えるか、自転周期の測定方法、時期による変化は、この動画では確認していません。', '日数への換算は、24時間=1日として行った自作の計算です。'],
  tags='金星, 自転, 公転, 1日, 1年, NASA, 太陽系, 天文, 雑学, 検証',
  checks=['NASAのファクトシートとNotesの原文を、公開前にもう一度開いて確認する(`docs/themes/20261108_venus/08_fact_check.md`)', '「天王星の自転周期にもマイナスが付く」の根拠(NASAの天王星の表)を開き直して確認する']),
 thumb=dict(bg='assets/venus/thumb_art.png', lines=[['金星の一日は', 90, 'white'], ['一年より', 100, 'white'], ['長い？', 150, 'gold']], sub='NASAの表で確かめる', shade_col=[8, 46, 52], accent=[255, 190, 110], bar_col=[255, 190, 110], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


finalize(spec, {})
