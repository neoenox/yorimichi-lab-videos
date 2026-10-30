"""Writes data/bukka_spec.json（物価が2％上がったら、どの家庭の生活費も2％増える？）。台本：docs/themes/20270206_bukka/09_script_v2.md
at / until は『章内の行番号（0始まり）』。末尾で文の番号に直す。イラスト（specart.inject）は、画像ができてから足す。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
R = Path(__file__).resolve().parents[1]
from specart import inject
TOP = [60, 170, 1860, 235]
spec = dict(slug='bukka', theme_dir='20270206_bukka', pack='43_bukka', header_sub='総務省の統計で、世帯ごとの物価の上がり方を確かめる',
 images={},
 bgm=[['intro', 'basket', 'piano36'], ['numbers', 'five', 'piano12'], ['method', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='物価が2％上がったら、どの家庭も2％増える？', chapter_title='導入：物価が2％上がったら、どの家庭も2％増える？', opener='物価2％上昇＝どの家庭も生活費2％増？', opener_until=1, scene=[
   dict(t='big', text='物価が2％上がった。生活費も、2％増える？', y=270, at=0, size=54, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='どの家庭でも、同じ割合で増える？', at=1, size=44, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：総務省の統計（収入の違う世帯ごとの物価指数）', at=2, size=36),
   dict(t='panel', box=[120, 750, 1800, 830], text='答えは「同じではない」。ただし、総務省の指数では、差は小さい', at=3, size=36, col='gold')]),
 dict(key='index', title='物価の指数とは、何か', chapter_title='物価の指数とは、何か', scene=[
   dict(t='panel', box=TOP, text='ニュースの「物価」＝消費者物価指数（総務省が毎月作成）', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='決まった「買い物かご」の値段の変化を見るもの', at=1, until=2, size=40),
   dict(t='panel', box=TOP, text='かごの中身＝品目ごとの割合（ウエイト）。食料は何割、住居は何割…', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='ウエイトは、家計調査（家計の支出を調べる統計）から作る', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='2025年の全国の消費者物価：前年より3.2％上昇（2％ではなく3％台）', at=4, size=36, col='gold'),
   dict(t='bars', box=[60, 300, 1860, 540], title='全国の消費者物価の上昇率（総合・前年比）', unit='％', max=4, lab_w=480, data=[dict(at=4, label='ニュースの例え', value=2, vlabel='2％', col='blue'), dict(at=4, label='2025年の実際（全国）', value=3.2, vlabel='3.2％', col='gold')])]),
 dict(key='basket', title='家庭ごとに、買い物かごは違う', chapter_title='家庭ごとに、買い物かごは違う', scene=[
   dict(t='panel', box=TOP, text='総務省は、収入の違う世帯ごとの指数も作っている', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='対象：二人以上の世帯のうち、勤労者世帯（年収の低い順に5つに分ける）', at=1, until=2, size=34),
   dict(t='panel', box=TOP, text='2020年基準のかご：食料は 最も低い層26％、最も高い層24％', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='光熱・水道は 約8％と約5％。住居は 約23％と約18％', at=3, until=4, size=38, hi=True),
   dict(t='panel', box=TOP, text='逆に、教育は 約3％と約8％', at=4, until=5, size=40),
   dict(t='panel', box=TOP, text='同じ値上がりでも、何が上がったかで、響き方は変わる', at=5, size=40, col='gold'),
   dict(t='table', box=[60, 300, 1860, 640], cols=['かごの中の割合（2020年基準）', '年収が最も低い5分の1', '年収が最も高い5分の1'], colw=[740, 560, 500], size=36, rows=[
     dict(at=2, cells=['食料', '26.3％', '23.6％'], col='gold'),
     dict(at=3, cells=['光熱・水道', '7.9％', '5.1％']),
     dict(at=3, cells=['住居', '22.5％', '18.2％']),
     dict(at=4, cells=['教育', '2.6％', '7.6％'])])]),
 dict(key='numbers', title='実際の数字', chapter_title='実際の数字', scene=[
   dict(t='panel', box=TOP, text='2025年の物価上昇率を、年収の順に（勤労者世帯・総合・前年比）', at=0, until=1, size=34, hi=True),
   dict(t='panel', box=TOP, text='最も低い層3.3％ → 3.1％ → 真ん中3.0％ → 2.9％ → 最も高い層2.7％', at=1, until=2, size=34),
   dict(t='panel', box=TOP, text='最も低い層と最も高い層の差：0.6ポイント', at=2, until=3, size=40, col='gold'),
   dict(t='panel', box=TOP, text='前の年は？ 2024年は2.5〜2.6％、2023年は全層で3.2％', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='差がはっきり出たのは2025年。ただし、1ポイントも違わない差', at=4, size=36, hi=True),
   dict(t='bars', box=[60, 300, 1860, 640], title='2025年の物価上昇率（総合・前年比。年収の低い順）', unit='％', max=4, lab_w=520, data=[dict(at=0, label='最も低い5分の1', value=3.3, vlabel='3.3％', col='gold', until=3), dict(at=0, label='2番目', value=3.1, vlabel='3.1％', col='gold', until=3), dict(at=0, label='真ん中', value=3.0, vlabel='3.0％', col='gold', until=3), dict(at=0, label='4番目', value=2.9, vlabel='2.9％', col='gold', until=3), dict(at=0, label='最も高い5分の1', value=2.7, vlabel='2.7％', col='blue', until=3)]),
   dict(t='table', box=[60, 300, 1860, 560], cols=['年（勤労者世帯・総合・前年比）', '最も低い層', '最も高い層'], colw=[800, 500, 500], size=38, rows=[
     dict(at=3, cells=['2023年', '3.2％', '3.2％']),
     dict(at=3, cells=['2024年（全5層は2.5〜2.6％）', '2.6％', '2.6％']),
     dict(at=3, cells=['2025年', '3.3％', '2.7％'], col='gold')])]),
 dict(key='why', title='なぜ、差が出るのか', chapter_title='なぜ、差が出るのか', scene=[
   dict(t='panel', box=TOP, text='理由として考えられる：食料の値上がり（2025年は平均6.7％上昇）', at=0, until=1, size=34, hi=True),
   dict(t='panel', box=TOP, text='穀類（米を含む）は約20％上昇：最も低い層22.4％、最も高い層19.8％', at=1, until=2, size=34),
   dict(t='panel', box=TOP, text='そこで、食料の割合×値上がり率で、押し上げた分をおおまかに計算', at=2, until=3, size=34),
   dict(t='panel', box=TOP, text='最も低い層 約1.9ポイント、最も高い層 約1.5ポイント。差は約0.36ポイント', at=3, until=4, size=34, col='gold'),
   dict(t='panel', box=TOP, text='差は約0.36ポイントで、0.6ポイントの差のおよそ6割。厳密な分解ではない', at=4, until=5, size=36),
   dict(t='panel', box=TOP, text='電気代は、どの層も5.3％上昇。光熱・水道の割合が大きい世帯ほど、影響は大きい', at=5, size=30),
   dict(t='bars', box=[60, 300, 1860, 540], title='食料が物価を押し上げた分（自作の近似。食料の割合×前年比）', unit='ポイント', max=2.5, lab_w=620, data=[dict(at=3, label='最も低い5分の1', value=1.87, vlabel='約1.9', col='gold', until=5), dict(at=3, label='最も高い5分の1', value=1.51, vlabel='約1.5', col='blue', until=5)])]),
 dict(key='five', title='五年間で、見てみる', chapter_title='五年間で、見てみる', scene=[
   dict(t='panel', box=TOP, text='2020年→2025年：勤労者世帯の平均で、約11.1％の上昇', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='最も低い層：約11.5％。最も高い層：約10.9％', at=1, until=2, size=40),
   dict(t='panel', box=TOP, text='差は約0.6ポイント。ただし、基準を改めたときにつなげた指数での計算', at=2, until=3, size=34, col='gold'),
   dict(t='panel', box=TOP, text='一方、内閣府の試算：2021年からの5年間で、3％程度の差', at=3, until=4, size=36, hi=True),
   dict(t='panel', box=TOP, text='なぜ、数字が違うのか', at=4, size=36),
   dict(t='bars', box=[60, 300, 1860, 590], title='2020年→2025年の物価上昇率（勤労者世帯・総合。自作の計算）', unit='％', max=14, lab_w=620, data=[dict(at=0, label='勤労者世帯の平均', value=11.1, vlabel='約11.1％', col='blue', until=3), dict(at=1, label='最も低い5分の1', value=11.5, vlabel='約11.5％', col='gold', until=3), dict(at=1, label='最も高い5分の1', value=10.9, vlabel='約10.9％', col='gold', until=3)])]),
 dict(key='method', title='数字が違う理由と、注意点', chapter_title='数字が違う理由と、注意点', scene=[
   dict(t='panel', box=TOP, text='総務省：かごの中身を、決まった年のものに固定して計算', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='内閣府：家計調査をもとに、かごの中身を毎年更新して試算', at=1, until=2, size=38),
   dict(t='panel', box=TOP, text='対象の世帯や費目の範囲も同じとは限らない。要因の内訳は未確認', at=2, until=3, size=34, col='gold'),
   dict(t='panel', box=TOP, text='世帯ごとの指数：全国の価格の変化は共通で、ウエイトだけを世帯ごとに変える', at=3, until=4, size=32),
   dict(t='panel', box=TOP, text='安い店に変えた、量を減らした、といった工夫は入っていない', at=4, until=5, size=38, hi=True),
   dict(t='panel', box=TOP, text='対象は、二人以上の世帯のうちの勤労者世帯。単身世帯・年金暮らしの世帯などは含まれない', at=5, until=6, size=30),
   dict(t='panel', box=TOP, text='内閣府：光熱費の補助や、高校の授業料の支援制度の変更も影響', at=6, size=34),
   dict(t='table', box=[60, 300, 1860, 640], cols=['', '総務省の指数', '内閣府の試算'], colw=[420, 720, 660], size=34, rows=[
     dict(at=0, cells=['かごの中身', '決まった年で固定（2020年基準）', '毎年更新（家計調査）'], col='gold'),
     dict(at=1, cells=['期間', '2025年／2020→2025年', '2021年からの5年間']),
     dict(at=3, cells=['最も低い層と高い層の差', '0.6ポイント', '3％程度'], col='gold')])]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=1, text='2025年は、最も低い層が3.3％、最も高い層が2.7％'),
      dict(at=2, text='差の理由として、食料などのかごの中身の違いが考えられる'),
      dict(at=3, text='総務省の指数では、差は0.6ポイント。内閣府の試算では、5年間で3％程度')]),
     right=dict(title='言い方の注意', title_at=4, items=[
      dict(at=4, text='「物価の上昇」と「自分の家の生活費の増え方」は同じではない。自分の家計の中身で考える')]))]),
 ],
 desc=dict(title_main='物価が2％上がったら、どの家庭の生活費も2％増えるのか', title_no=1,
  titles=['物価が2％上がったら、どの家庭の生活費も2％増える？ 総務省の統計で確かめる', '物価上昇は家庭で違う？ 年収の低い層は3.3％、高い層は2.7％（2025年）', '「物価2％上昇＝生活費も2％増」は本当か：買い物かごの中身で変わる'],
  intro='「物価が2％上がった」というニュース。どの家庭でも、生活費が2％増えるのでしょうか。この動画では、総務省の消費者物価指数(2025年基準)の、年収の違う世帯ごとの指数で、物価の上がり方を確かめます。',
  points=['2025年の全国の消費者物価は、前年より3.2％上昇でした。', '二人以上の世帯のうち勤労者世帯を、年収の低い順に5つに分けると、2025年の上昇率は、最も低い層3.3％、最も高い層2.7％でした(差0.6ポイント)。', '買い物かごの中身(食料・光熱・水道などの割合)が、世帯で違います。食料の寄与の差は、約0.4ポイントと近似できます(自作の近似計算)。', '内閣府の試算では、2021年からの5年間で、最も高い層と最も低い層の間に3％程度の差があります。総務省の指数とは、かごの更新などの方法が違います。', '物価指数は、同じものを買い続けた場合の価格の変化です。実際の生活費は、買い方や収入でも変わります。'],
  refs=['総務省統計局「2025年基準 消費者物価指数」第7表 勤労者世帯年間収入五分位階級別中分類指数(年平均):https://www.e-stat.go.jp/stat-search/files?toukei=00200573&tstat=000001243876', '総務省「2025年(令和7年)平均 全国消費者物価指数」:https://www.stat.go.jp/data/cpi/sokuhou/nen/index-z.htm', '内閣府「日本経済レポート(2025年度)」第2章第1節 物価上昇が家計に与える影響と属性ごとの違い:https://www5.cao.go.jp/keizai3/2025/0210nk/n25_2_1.html', '総務省統計局「消費者物価指数(CPI)」:https://www.stat.go.jp/data/cpi/'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['0.6ポイントの差、5年間の累積(約11.5％／約10.9％)、食料の寄与(約1.9／約1.5ポイント)は、公表値からの自作の計算です。食料の寄与は、2020年基準のウエイト×前年比の近似で、厳密な分解ではありません。', '2025年の前年比は、2020年基準で公表した値を引き継いでいます(総務省の解説による)。食料の寄与の計算には、2020年基準のウエイトを使いました。', '内閣府の試算と総務省の指数の差が、どの要因で何ポイント生じたかは、確かめていません。', '内閣府の試算と総務省の指数は、計算の方法・比べる期間などが違うため、そのまま比べられません。'],
  tags='物価, 消費者物価指数, 総務省, 家計, 年収, 食料, 物価高, 検証',
  checks=['2026年の最新の年平均が公表されたら、数字を更新する', '内閣府の第2-1-9図の注(対象世帯・帰属家賃の扱い)を、原本の図で確認する', '食料の寄与の近似を、総務省の寄与度表(あれば)と照合する']),
 thumb=dict(bg='assets/bukka/thumb_art.png', lines=[['物価2％上昇', 110, 'white'], ['どの家庭も', 100, 'white'], ['2％増える？', 120, 'gold']], sub='総務省の統計で確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and o.get('title'):
            h = o['box'][3] - o['box'][1]
            if h < 112:
                tx = o['title'] + '：' + o['text']; sz = min(o.get('size', 40), 40, int((o['box'][2] - o['box'][0] - 70) / len(tx)))
                if sz >= 26: o['title'] = None; o['text'] = tx; o['size'] = sz
                else: o['size'] = min(o.get('size', 40), 30)
            else: o['size'] = min(o.get('size', 40), 40 if h < 125 else 46)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


def _line_to_sentence_starts():
    """台本の番号つきの行（1行に複数の文がある）→ 各行の最初の文の番号（vp.py の sentences と同じく「。」で区切る）。"""
    import re
    t = (R / 'docs' / 'themes' / '20270206_bukka' / '09_script_v2.md').read_text(encoding='utf8')
    out = []
    for c in re.split('\n## ', t)[1:]:
        if not re.match('章(\\d+)　', c.split('\n')[0]): continue
        starts, n = [], 0
        for l in c.split('\n'):
            if re.match('^\\d+\\. ', l):
                body = re.sub('〔[^〕]*〕', '', re.sub('^\\d+\\. ', '', l)).strip()
                starts.append(n); n += len([x for x in body.split('。') if x.strip()])
        starts.append(n)
        out.append(starts)
    return out


def _remap(o, st):
    f = lambda i: None if i is None else st[min(i, len(st) - 1)]
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if k in ('at', 'until', 'title_at', 'at2') and isinstance(v, int): o[k] = f(v)
            else: _remap(v, st)
    elif isinstance(o, list):
        for v in o: _remap(v, st)


_S = _line_to_sentence_starts()
assert len(_S) == len(spec['chapters']), (len(_S), len(spec['chapters']))
for _ch, _st in zip(spec['chapters'], _S):
    _remap(_ch['scene'], _st)
    if 'opener_until' in _ch: _ch['opener_until'] = _st[min(_ch['opener_until'], len(_st) - 1)]

_fit(spec)
_ART = {'intro': 'intro', 'index': 'office', 'basket': 'shop', 'numbers': 'office', 'why': 'home', 'five': 'wallet', 'method': 'office', 'end': 'intro'}
if all((R / 'assets' / 'bukka' / f'art_{v}.png').exists() for v in set(_ART.values())):
    inject(spec, _ART)
(R / 'data' / 'bukka_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
