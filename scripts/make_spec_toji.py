"""Writes data/toji_spec.json（冬至は、一年でいちばん寒い日？）。台本：docs/themes/20261219_toji/09_script_v2.md
at / until は『章内の行番号（0始まり）』。finalize が文の番号に直す。"""
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


def bg(name, **kw):
    return pop('pop_bgimg', img=name, at=0, **kw)


IMG = {n: dict(file=f'assets/toji/{n}.png') for n in
       ('art_intro', 'art_toji', 'art_sunalt', 'art_temp', 'art_why', 'art_sun', 'art_range', 'art_end', 'fig_alt')}

spec = dict(slug='toji', theme_dir='20261219_toji', pack='47_toji_solstice',
            header_sub='国立天文台の暦と、気象庁の平年値で確かめる',
            style='pop', images=IMG,
            bgm=[['intro', 'toji', 'piano34'], ['sunalt', 'temp', 'piano37'],
                 ['why', 'sun', 'acoustic50'], ['range', 'end', 'acoustic48']],
            chapters=[
  dict(key='intro', title='冬至は、いちばん寒い日？', chapter_title='導入：冬至は、いちばん寒い日？', scene=[
    bg('art_intro', dim=.45, blur=3),
    tel('冬至は、一年で\n[[いちばん寒い日]]？', 960, 400, 110, at=0, until=2, rot=-2),
    tel('答え：気温の底は[[1月]]', 960, 400, 104, at=2, until=4, plate='red', rot=2),
    tel('東京の平年値で確かめる', 960, 700, 52, at=3, until=4, plate='blue', rot=1)]),
  dict(key='toji', title='冬至の日を、確かめる', chapter_title='冬至の日を、確かめる', scene=[
    bg('art_toji', dim=.55, blur=3),
    tel('冬至と夏至を、並べる', 960, 180, 62, at=0, rot=-1),
    dict(t='table', box=[110, 265, 1810, 700], cols=['', '冬至（12/22）', '夏至（6/21）'], colw=[520, 590, 590], size=40, rows=[
      dict(at=1, cells=['日の出', '6:47', '4:25']),
      dict(at=1, cells=['日の入り', '16:32', '19:00']),
      dict(at=2, cells=['昼の長さ', '9時間45分', '14時間35分'], col='gold')]),
    tel('昼の差は[[4時間50分]]', 960, 770, 54, at=4, plate='yellow', rot=1)]),
  dict(key='sunalt', title='太陽の高さも、違う', chapter_title='太陽の高さも、違う', scene=[
    bg('art_sunalt', dim=.5, blur=3),
    dict(t='anim', name='pop_card', inner='img', img='fig_alt', box=[170, 120, 1750, 700], at=0, rot=-1),
    tel('南中の高さ [[30.9度]] と 77.8度', 960, 760, 48, at=1, plate='blue', rot=1)]),
  dict(key='temp', title='気温の底は、いつか', chapter_title='気温の底は、いつか', scene=[
    bg('art_temp', dim=.55, blur=4),
    tel('東京の月平均気温（平年値）', 960, 180, 56, at=0, until=1, rot=-1),
    tel('底は[[1月]] 5.4℃', 960, 180, 66, at=3, plate='red', rot=1.5),
    dict(t='bars', box=[140, 285, 1780, 790], unit='℃', max=15, lab_w=260, data=[
      dict(at=1, label='11月', value=12.5, vlabel='12.5℃', col='blue'),
      dict(at=1, label='12月', value=7.7, vlabel='7.7℃', col='blue'),
      dict(at=1, label='1月', value=5.4, vlabel='5.4℃', col='gold'),
      dict(at=1, label='2月', value=6.1, vlabel='6.1℃', col='blue')])]),
  dict(key='why', title='なぜ、ずれるのか', chapter_title='なぜ、ずれるのか', scene=[
    bg('art_why', dim=.55, blur=4),
    tel('なぜ、ずれる？', 960, 210, 92, at=0, until=1, rot=-1),
    rows([dict(at=1, tag='日射', text='冬至がいちばん弱い', col='blue'),
          dict(at=2, tag='地面・海', text='温まりにくく、冷えにくい', col='orange'),
          dict(at=3, tag='気温', text='底は、およそ1か月あと', col='red'),
          dict(at=4, tag='暦', text='二十四節気は古代中国の目安', col='purple')],
         x0=120, x1=1800, y0=330, size=56, gap=30)]),
  dict(key='sun', title='日照時間の底は、6月', chapter_title='もう一つの思い込み：日照時間の底', scene=[
    bg('art_sun', dim=.5, blur=4),
    tel('冬至の月＝日照最少、ではない', 960, 200, 62, at=0, until=2, rot=-1),
    tel('日照時間の底は[[6月]]', 960, 200, 76, at=3, plate='yellow', rot=1.5),
    dict(t='bars', box=[140, 310, 1780, 800], unit='時間', max=210, lab_w=260, data=[
      dict(at=2, label='12月', value=174.4, vlabel='174.4時間', col='blue'),
      dict(at=2, label='1月', value=192.6, vlabel='192.6時間', col='blue'),
      dict(at=2, label='6月', value=124.2, vlabel='124.2時間', col='gold')])]),
  dict(key='range', title='この数字の、範囲', chapter_title='この数字の、範囲', scene=[
    bg('art_range', dim=.55, blur=4),
    tel('この数字の、範囲', 960, 220, 92, at=0, until=1, rot=-1),
    rows([dict(at=1, tag='場所', text='東京の平年値だけ', col='blue'),
          dict(at=1, tag='期間', text='1991〜2020年の30年平均', col='orange'),
          dict(at=2, tag='日ごと', text='いちばん寒い日は、また別', col='red')],
         x0=120, x1=1800, y0=360, size=56, gap=30)]),
  dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
    bg('art_end', dim=.5, blur=3),
    rows([dict(at=0, tag='冬至', text='昼がいちばん短い日（9時間45分）', col='blue'),
          dict(at=1, tag='気温', text='底は1月 5.4℃', col='orange'),
          dict(at=2, tag='日照', text='底は6月 124.2時間', col='green')],
         x0=120, x1=1800, y0=190, size=52, gap=26),
    tel('暦の節目と、底は[[同じじゃない]]', 960, 690, 60, at=3, plate='yellow', rot=-1)]),
            ],
            desc=dict(title_main='冬至は、一年でいちばん寒い日なのか', title_no=1,
  titles=['冬至は、一年でいちばん寒い日？ 東京の気温の底は1月だった',
          '冬至は寒さのピークじゃない？ 気象庁の平年値で底を確かめる',
          '冬至の昼は9時間45分。でも気温の底は1月、日照の底は6月だった'],
  intro='十二月二十二日は冬至。一年で昼がいちばん短い日です。では、いちばん寒い日でもあるのでしょうか。この動画では、国立天文台の暦と気象庁の平年値で、冬至と、気温・日照の底の関係を確かめます。',
  points=['2026年の冬至は12月22日5時50分(国立天文台 暦要項)。東京の日の出は6:47、日の入りは16:32で、昼は9時間45分。夏至(6月21日)の昼は14時間35分で、差は4時間50分です。',
          '東京の南中高度は、冬至30.9度、夏至77.8度で、46.9度の差があります(国立天文台 暦計算室)。',
          '気象庁の平年値(1991〜2020年)では、東京の月平均気温は11月12.5℃、12月7.7℃、1月5.4℃、2月6.1℃。底は1月で、冬至からおよそ1か月あとです。',
          '同じ平年値で、日照時間は12月174.4時間、1月192.6時間、6月124.2時間。日照の底は6月(梅雨)で、冬至の月ではありません。'],
  refs=['国立天文台 暦要項 令和8年(2026) 二十四節気および雑節:https://eco.mtk.nao.ac.jp/koyomi/yoko/2026/rekiyou262.html',
        '国立天文台 暦計算室 東京の日の出・南中・日の入り 2026年12月:https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s1312.html',
        '国立天文台 暦計算室 同 2026年6月:https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s1306.html',
        '国立天文台 暦Wiki「二十四節気とは？」:https://eco.mtk.nao.ac.jp/koyomi/wiki/B5A8C0E12FC6F3BDBDBBCDC0E1B5A4A4C8A4CFA1A9.html',
        '気象庁 過去の気象データ検索 東京 平年値(年・月ごとの値、1991〜2020年):https://www.data.jma.go.jp/stats/etrn/view/nml_sfc_ym.php?prec_no=44&block_no=47662&year=&month=&day=&view='],
  credit_lines=['・背景・図・グラフ:自作(国立天文台・気象庁の公表値をもとにしています)'],
  notes=['昼の長さ(9時間45分・14時間35分・差4時間50分)と南中高度の差(46.9度)は、公表されている時刻・数値からの自作の計算です。',
         '気温の底が遅れる仕組み(地面や海が冷えにくい)と、太陽が低いと光の量が減ることは、一般的な説明として述べています。特定の資料の引用ではありません。',
         '地域差、日ごとの底(1月の何日が最も寒いか)、長期の変化は、この動画では扱っていません。'],
  tags='冬至, 夏至, 気温, 平年値, 気象庁, 国立天文台, 日照時間, 暦, 季節, 雑学, 検証',
  checks=['国立天文台の暦要項・暦計算室の表を、公開前にもう一度開いて数字を照合する(docs/themes/20261219_toji/08_fact_check.md)',
          '気象庁の平年値のページを開き、気温と日照時間の数字を照合する']),
  thumb=dict(bg='assets/toji/thumb_art.png', lines=[['冬至は', 110, 'white'], ['一年で', 100, 'white'], ['寒い日？', 130, 'gold']],
             sub='気象庁の平年値で確かめる', shade_col=[10, 12, 34], accent=[255, 200, 120], bar_col=[255, 200, 120],
             y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))

finalize(spec, {})
