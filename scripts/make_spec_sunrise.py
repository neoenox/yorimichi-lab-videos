"""Writes data/sunrise_spec.json（日の出が一番早いのは、夏至の日？）。台本：docs/themes/20261107_sunrise/09_script_v2.md"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from specart import inject
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]
spec = dict(slug='sunrise', theme_dir='20261107_sunrise', pack='20_sunrise_solstice', header_sub='日の出と日の入りを、国立天文台の暦で確かめる',
 images={},
 bgm=[['intro', 'rise', 'piano36'], ['set', 'why', 'piano12'], ['end', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='日の出が一番早いのは、夏至の日？', chapter_title='導入：日の出が一番早いのは、夏至の日？', scene=[
   dict(t='chips', y=230, w=760, h=130, gap=100, size=46, items=[dict(at=0, text='昼が一番長い日：夏至'), dict(at=1, text='日の出が一番早い日も？')]),
   dict(t='panel', box=[120, 430, 1800, 550], text='国立天文台：日の出が最も早い日は、夏至の約1週間前', at=2, size=42, hi=True),
   dict(t='panel', box=[120, 580, 1800, 680], text='東京の暦（2027年）で、確かめる', at=3, size=44, col='gold'),
   dict(t='panel', box=[120, 730, 1800, 800], text='資料：国立天文台（よくある質問・暦計算室）', at=4, size=32)]),
 dict(key='rise', title='東京の日の出は、いつが一番早いのか', chapter_title='東京の日の出は、いつが一番早いのか', scene=[
   dict(t='panel', box=TOP, text='国立天文台 暦計算室：東京の2027年の暦（分単位）', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='夏至：6月21日', at=1, until=2, size=42, hi=True),
   dict(t='panel', box=TOP, text='6月1日の日の出：4時27分', at=2, until=3, size=42),
   dict(t='panel', box=TOP, text='6月6日〜6月21日：毎日、4時25分', at=3, until=4, size=42, hi=True),
   dict(t='panel', box=TOP, text='夏至の日の日の出も、同じ4時25分', at=4, until=5, size=42, col='gold'),
   dict(t='panel', box=TOP, text='分単位の暦：4時25分が16日間続き、一番早い一日は、一つに絞れない', at=5, until=7, size=38, hi=True),
   dict(t='panel', box=TOP, text='それでも、分単位の表示では、日の出は、夏至より前から同じ時刻になっている', at=7, size=40, col='gold'),
   dict(t='shade', box=[60, 250, 1860, 850], at=0, alpha=0.5),
   dict(t='anim', name='suncurve', box=[60, 250, 1860, 850], at=2, s_a=2, mode='rise')]),
 dict(key='set', title='日の入りは、いつが一番遅いのか', chapter_title='日の入りは、いつが一番遅いのか', scene=[
   dict(t='panel', box=TOP, text='夏至の日（6月21日）の日の入り：19時00分', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='ところが、そのあとも、日の入りは遅くなる', at=1, until=2, size=42, col='gold'),
   dict(t='panel', box=TOP, text='6月24日〜7月5日：毎日、19時01分', at=2, until=3, size=42, hi=True),
   dict(t='panel', box=TOP, text='国立天文台：日の入りが最も遅い日は、夏至の約1週間後', at=3, until=4, size=40, hi=True),
   dict(t='panel', box=TOP, text='昼の長さ（日の出・日の入りの時刻から計算：自作）', at=4, until=8, size=40),
   dict(t='panel', box=TOP, text='昼の長さは、夏至の前後で、ほとんど変わらない', at=8, size=42, col='gold'),
   dict(t='shade', box=[60, 250, 1860, 850], at=0, alpha=0.5),
   dict(t='anim', name='suncurve', box=[60, 250, 1860, 850], at=0, until=4, s_a=1, mode='set'),
   dict(t='bars', box=[160, 330, 1760, 700], title='昼の長さ（東京2027年・日の出と日の入りから計算）', unit='分', max=900, lab_w=300, data=[
     dict(at=5, label='6月14日', value=873, vlabel='14時間33分', col='blue'),
     dict(at=6, label='6月21日（夏至）', value=875, vlabel='14時間35分', col='gold'),
     dict(at=7, label='6月28日', value=874, vlabel='14時間34分', col='blue')])]),
 dict(key='why', title='なぜ、ずれるのか', chapter_title='なぜ、ずれるのか', scene=[
   dict(t='panel', box=TOP, text='国立天文台：昼の長さは、太陽の高さで決まる', at=0, until=2, size=42, hi=True),
   dict(t='panel', box=TOP, text='けれども、日の出・日の入りは、南中の時刻にも左右される', at=2, until=3, size=40, hi=True),
   dict(t='panel', box=TOP, text='東京の南中：6月1日 11時39分 → 夏至 11時43分 → 7月1日 11時45分', at=3, until=6, size=36),
   dict(t='panel', box=TOP, text='夏至の前後は、南中が、毎日少しずつ遅くなる時期', at=6, until=7, size=42, col='gold'),
   dict(t='panel', box=TOP, text='日の出・日の入りは、南中を挟んで前後に分かれる。南中が遅くなると、どちらも同じ向きにずれる', at=7, until=9, size=32, hi=True),
   dict(t='panel', box=TOP, text='昼が最長の日・日の出が最早の日・日の入りが最遅の日は、一致しなくなる', at=9, until=10, size=38, hi=True),
   dict(t='panel', box=TOP, text='南中が変わる理由：自転軸の傾きと、公転軌道が楕円であること（国立天文台）', at=10, size=36, col='gold'),
   dict(t='shade', box=[60, 250, 1860, 850], at=0, alpha=0.5),
   dict(t='anim', name='suncurve', box=[60, 250, 1860, 850], at=3, until=7, s_a=3, mode='noon'),
   dict(t='anim', name='dayline', box=[60, 250, 1860, 850], at=7, s_a=7, s_b=8)]),
 dict(key='end', title='分かること、決められないこと', chapter_title='結論：分かること、決められないこと', scene=[
   dict(t='cols2', size=36, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=0, text='国立天文台：日の出が最も早い日は夏至の約1週間前、日の入りが最も遅い日は約1週間後'),
      dict(at=2, text='東京の2027年の暦：日の出は6月6日から同じ時刻、日の入りは夏至のあとに、さらに遅くなる'),
      dict(at=4, text='国立天文台によれば、昼が最長の日と、日の出が最早の日は、およそ1週間ずれる')]),
     right=dict(title='決められないこと', title_at=5, items=[
      dict(at=5, text='東京の暦（分単位）だけでは、一番早い一日は決められない'),
      dict(at=6, text='他の年・他の地点の、細かい日付')]))])
 ],
 desc=dict(title_main='日の出が一番早いのは、夏至の日なのか', title_no=1,
  titles=['日の出が一番早いのは、夏至の日？ 国立天文台の暦で確かめる', '日の出が一番早い日は夏至じゃない？ 東京の暦を確かめる', '夏至なのに日の出は一番早くない？ 国立天文台の説明と東京の暦'],
  intro='一年で昼が一番長い日は夏至です。では、日の出が一番早い日も、夏至でしょうか。この動画では、国立天文台の説明と、国立天文台暦計算室の東京の暦(2027年)から、日の出と日の入りの時刻を確かめます。東京の日の出はいつが一番早いのか、日の入りはいつが一番遅いのか、なぜずれるのか、を分けて見ていきます。分かることと決められないことを分けて、国立天文台の説明に帰属して述べます。',
  points=['国立天文台の説明では、日本で日の出が最も早い日は夏至の約1週間前、日の入りが最も遅い日は夏至の約1週間後です(国立天文台「1年のうちで、日の出、日の入が一番早い日(遅い日)はいつ？」)。', '東京の2027年の暦(国立天文台暦計算室)では、夏至は6月21日、日の出は6月6日〜21日が毎日4時25分でした。夏至の日の日の出も4時25分です。暦は分単位なので、一番早い一日は一つに決められません。日の入りは、夏至の日が19時00分、6月24日〜7月5日が19時01分でした。', '日の出と日の入りは、太陽が真南に来る南中の時刻にも左右されます。夏至の前後は南中の時刻が毎日少しずつ遅くなる時期にあたり(東京は6月1日11時39分、夏至11時43分、7月1日11時45分)、昼が最長の日と、日の出が最早の日・日の入りが最遅の日は一致しなくなります。南中の時刻が変わるのは、地球の自転軸の傾きと、公転軌道が楕円であることによります(国立天文台)。', '昼の長さを日の出・日の入りの時刻から計算すると、6月14日が14時間33分、夏至の日が14時間35分、6月28日が14時間34分で、夏至の前後でほとんど変わりません(自作の計算)。'],
  refs=['国立天文台「1年のうちで、日の出、日の入が一番早い日(遅い日)はいつ？」:https://www.nao.ac.jp/faq/a0104.html', '国立天文台 暦計算室「東京の日の出・南中・日の入り 2027年6月」:https://eco.mtk.nao.ac.jp/koyomi/dni/2027/s1306.html', '国立天文台 暦計算室「同 2027年7月」:https://eco.mtk.nao.ac.jp/koyomi/dni/2027/s1307.html', '国立天文台 暦要項 2027年(二十四節気):https://eco.mtk.nao.ac.jp/koyomi/yoko/2027/rekiyou272.html'],
  credit_lines=['・図・グラフ・計算:自作(国立天文台暦計算室の数字をもとにしています。分単位の数字です)', '・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実際の風景の再現ではありません)'],
  notes=['時刻は日本標準時、分単位です。暦計算室の数字をもとにした自作のグラフ・計算を含みます。', '他の年・他の地点の日付、冬の側(日の出が最も遅い日など)は、この動画では確認していません。', '地域によるずれの大きさは、情報源によって説明が異なるため、扱っていません。'],
  tags='日の出, 日の入り, 夏至, 南中, 昼の長さ, 国立天文台, 暦, 天文, 雑学, 検証',
  checks=['国立天文台FAQ(a0104)の原文を、公開前にもう一度開いて確認する(`docs/themes/20261107_sunrise/08_fact_check.md`)', '暦計算室の2027年6月・7月の東京の表を、公開前に開き直して数字を照合する', '夏至の日時(2027年6月21日23時11分)の原文(暦要項)を確認する']),
 thumb=dict(bg='assets/sunrise/thumb_art.png', lines=[['日の出が一番', 80, 'white'], ['早いのは', 80, 'white'], ['夏至の日？', 130, 'gold']], sub='国立天文台の暦で確かめる', shade_col=[54, 16, 44], accent=[255, 190, 140], bar_col=[255, 190, 140], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


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


_fit(spec)
inject(spec, dict(intro='intro', rise='rise', set='set', why='why', end='end'))
(R / 'data' / 'sunrise_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
