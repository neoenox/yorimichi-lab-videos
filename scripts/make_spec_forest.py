"""Writes data/forest_spec.json（日本の森林率は世界で何位？）。台本：docs/themes/20261119_forest/09_script_v2.md
文の番号（at）は `python scripts/vp.py forest sents` の番号。図は棒グラフ（自作）のみ。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]


def pn(text, at, until=None, size=40, hi=True, col=None, box=TOP):
    d = dict(t='panel', box=box, text=text, at=at, size=size, hi=hi)
    if until is not None: d['until'] = until
    if col: d['col'] = col
    return d


spec = dict(slug='forest', theme_dir='20261119_forest', pack='27_forest', header_sub='日本の森林率を、FAOと林野庁の統計で確かめる',
 images={},
 bgm=[['intro', 'jp', 'piano36'], ['world', 'oecd', 'piano12'], ['stock', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='日本の森林率は、世界で何位？', chapter_title='導入：日本の森林率は、世界で何位？', opener='日本の森林率は、世界で何位？', opener_until=3, scene=[
   dict(t='big', text='日本の森林率は、世界で何位？', y=270, at=0, size=58, col='gold'),
   pn('国土の約3分の2は森林。森林率は約68％', 0, 3, 44, box=[120, 450, 1800, 530]),
   pn('「世界3位」とは言えない：比べる国と、統計の年で、順位が変わる', 3, 5, 40, box=[120, 560, 1800, 640]),
   pn('数字の出どころを確かめる', 5, None, 44, box=[120, 670, 1800, 750])]),
 dict(key='jp', title='日本の数字', chapter_title='日本の数字', scene=[
   dict(t='cols2', size=34, xm=940, xm2=980,
        left=dict(title='FAO（2020年の評価）', title_at=0, items=[dict(at=0, text='陸地：約3645万ha'), dict(at=1, text='森林：約2494万ha'), dict(at=2, text='森林率：68.4％')]),
        right=dict(title='林野庁（令和4年3月末）', title_at=3, items=[dict(at=3, text='森林：約2502万ha'), dict(at=4, text='国土：約3730万ha'), dict(at=5, text='森林率：67％')]))]),
 dict(key='world', title='世界と比べる', chapter_title='世界と比べる', scene=[
   pn('FAO 2020年の評価：森林率（％）', 0, None, 40),
   dict(t='bars', box=[60, 260, 1860, 800], title='森林率（FAO 2020年の評価・陸地に占める森林の割合）', unit='％', max=100, lab_w=520, data=[
     dict(at=1, label='世界全体', value=31.1, vlabel='約31％', col='blue'),
     dict(at=2, label='日本', value=68.4, vlabel='68.4％', col='grn'),
     dict(at=6, label='ガボン', value=91.3, vlabel='約91％', col='org'),
     dict(at=5, label='ガイアナ', value=93.6, vlabel='約94％', col='org'),
     dict(at=4, label='スリナム', value=97.4, vlabel='約97％', col='org')])]),
 dict(key='oecd', title='OECDなら三位', chapter_title='OECDなら三位', scene=[
   pn('OECD加盟国に限る（FAO 2020年の統計をもとに林野庁が比較）', 0, None, 38),
   dict(t='bars', box=[60, 260, 1860, 700], title='OECD加盟国の上位（森林率・％）', unit='％', max=100, lab_w=520, data=[
     dict(at=1, label='1位 フィンランド', value=73.7, vlabel='73.7％', col='blue'),
     dict(at=2, label='2位 スウェーデン', value=68.7, vlabel='68.7％', col='blue'),
     dict(at=3, label='3位 日本', value=68.4, vlabel='68.4％', col='grn')]),
   pn('「世界3位」ではなく「2020年の統計で、OECD加盟国の中で3位」', 4, 5, 40, col='gold', box=[60, 730, 1860, 800]),
   pn('FAOは2025年の評価も公表。順位は、年によっても変わる', 5, None, 40, box=[60, 730, 1860, 800])]),
 dict(key='stock', title='中身は変わった', chapter_title='中身は変わった', scene=[
   pn('森林の面積：この50年ほど、約2500万haでほぼ横ばい', 0, 1, 40),
   pn('木の量（蓄積）：林野庁の集計。約3倍に', 1, 4, 42),
   pn('森林の約4割は、人が植えた人工林', 4, 6, 42),
   pn('人工林で最も多いのは、スギ（約440万ha）', 6, None, 42),
   dict(t='bars', box=[60, 260, 1860, 500], title='森林の蓄積（億立方メートル）', unit='億m3', max=60, lab_w=520, data=[
     dict(at=1, label='1966年度', value=18.9, vlabel='約19', col='blue'),
     dict(at=2, label='令和4年3月末', value=55.6, vlabel='約56', col='grn')]),
   dict(t='bars', box=[60, 530, 1860, 780], title='森林の面積（万ha・令和4年3月末）', unit='万ha', max=1600, lab_w=520, data=[
     dict(at=4, label='人工林', value=1009, vlabel='約1009（約4割）', col='org'),
     dict(at=5, label='天然林など', value=1493, vlabel='約1493（約6割）', col='grn')])]),
 dict(key='end', title='分かること、決められないこと', chapter_title='結論：分かること、決められないこと', scene=[
   dict(t='cols2', size=34, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=1, text='FAO 2020年：森林率 約68％。世界全体の2倍以上'),
      dict(at=3, text='同じ年の統計で、OECD加盟国の中では3位'),
      dict(at=4, text='森林の面積はほぼ一定。木の量は増えた')]),
     right=dict(title='決められないこと', title_at=5, items=[
      dict(at=6, text='世界での順位：比べる範囲と年で変わる'),
      dict(at=7, text='67％と68％の違い：割る面積と統計の違い')]))])
 ],
 desc=dict(title_main='日本の森林率は世界で何位か', title_no=1,
  titles=['日本の森林率は世界で何位？ FAOと林野庁の統計で確かめる', '日本の国土の約3分の2は森林？ 「世界3位」は本当か確かめる', '森林率68％と67％の違いは？ 日本の森林を統計で確かめる'],
  intro='日本の国土の約3分の2は森林です。では、その森林率は世界で何番目でしょうか。この動画では、国連食糧農業機関(FAO)の2020年の評価と、林野庁の「森林資源の現況」で、数字の出どころと順位の言い方を確かめます。',
  points=['FAOの2020年の評価では、日本の森林率は68.4％(陸地約3645万ha、森林約2494万ha)。世界全体の森林は陸地の約31％です。', '林野庁の令和4年3月末の集計では、森林面積は約2502万ha。国内の国土面積約3730万haで割ると、森林率は67％です。68％との違いは、割る面積と統計の違いです。', '日本より森林率が高い国は、スリナム(約97％)、ガイアナ(約94％)、ガボン(約91％)など、いくつもあります。「世界3位」とは言えません。', 'FAOの2020年の統計をもとに林野庁がOECD加盟国を比べた表では、日本は、フィンランド73.7％、スウェーデン68.7％に次ぐ3位です。FAOは2025年の評価も公表しており、順位は年によっても変わります。', '森林面積は約2500万haでほぼ横ばいですが、蓄積は1966年度の約19億立方メートルから令和4年3月末の約56億立方メートルに増えました。森林の約4割は人工林です。'],
  refs=['FAO「世界森林資源評価2020」(Global Forest Resources Assessment 2020):https://www.fao.org/forest-resources-assessment/', '林野庁「森林資源の現況(令和4年3月31日現在)」:https://www.rinya.maff.go.jp/j/keikaku/genkyou/r4/index.html'],
  credit_lines=['・図：自作(FAOと林野庁の公表数字をもとにした棒グラフです)'],
  notes=['比較表の数字は、FAO「世界森林資源評価2020」の国別表(林野庁掲載)にもとづきます。世界での順位は、比べる国や地域の範囲と統計の年で変わります。', '林野庁の67％は国内の国土面積で割った値、FAOの68.4％は別に定められた陸地面積で割った値です。', '蓄積の「約56億立方メートル」は、林野庁の資料の記述(令和4年3月末)にもとづきます。'],
  tags='森林率, 森林, 世界ランキング, FAO, 林野庁, OECD, 人工林, 雑学, 検証',
  checks=['林野庁「森林資源現況総括表」で、令和4年3月末の蓄積(約56億立方メートル)を確認する', 'FAO2025年版の国別表で、日本の順位・数字を確認する(動画では2020年版と明記)', '国内の国土面積(約3730万haか約3780万ha)を、国土地理院と林野庁の注記で確認する', '`docs/themes/20261119_forest/08_fact_check.md`']),
 thumb=dict(bg='assets/forest/thumb_bg.png', lines=[['森林率は', 100, 'white'], ['世界3位？', 120, 'gold']], sub='FAOと林野庁の統計で確かめる', shade_col=[8, 40, 20], accent=[120, 220, 140], bar_col=[120, 220, 140], y0=14, bar_y=470, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and not o.get('title') and o['box'][3] - o['box'][1] <= 70: o['size'] = min(o.get('size', 40), 40)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


_fit(spec)
(R / 'data' / 'forest_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
