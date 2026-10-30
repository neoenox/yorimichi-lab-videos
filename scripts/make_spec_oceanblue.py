"""Writes data/oceanblue_spec.json（海が青いのは、空が映っているから？）。台本：docs/themes/20261110_oceanblue/09_script_v2.md"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from specart import inject
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]
spec = dict(slug='oceanblue', theme_dir='20261110_oceanblue', pack='22_ocean_blue', header_sub='海の色を、NOAAとウッズホール海洋研究所の解説で確かめる',
 images={},
 bgm=[['intro', 'light', 'piano36'], ['colors', 'colors', 'piano12'], ['end', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='海が青いのは、空が映っているから？', chapter_title='導入：海が青いのは、空が映っているから？', scene=[
   dict(t='chips', y=240, w=1100, h=140, gap=100, size=50, items=[dict(at=0, text='海が青い：空が映っているから？')]),
   dict(t='panel', box=[120, 450, 1800, 570], text='空が映るのは、本当。でも、それだけでは、理由を説明できない', at=2, size=42, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='資料：NOAA・ウッズホール海洋研究所（WHOI）', at=4, size=34)]),
 dict(key='sky', title='空は、映るのか', chapter_title='空は、映るのか', scene=[
   dict(t='panel', box=TOP, text='WHOI：「空を映している」という考えを、まず取り上げている', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='WHOI：水面では、空を映す', at=1, until=2, size=42, hi=True),
   dict(t='panel', box=TOP, text='沿岸の水：嵐の日は灰色、日の出・日の入りはピンク色に見えることがある', at=2, until=3, size=36),
   dict(t='panel', box=TOP, text='しかし、水面の下に潜っても、青い色は残る', at=3, until=4, size=42, col='gold'),
   dict(t='panel', box=TOP, text='つまり、青く見える理由は、空の映り込みだけではない', at=4, until=5, size=40, hi=True),
   dict(t='panel', box=TOP, text='水そのものの、光に対する働きも、関係している', at=5, size=42, col='gold'),
   dict(t='shade', box=[60, 250, 1860, 850], at=0, alpha=0.5),
   dict(t='anim', name='oceanlight', box=[60, 250, 1860, 850], at=0, mode='surface', s_a=1, s_b=3)]),
 dict(key='light', title='水は、光をどうするのか', chapter_title='水は、光をどうするのか', scene=[
   dict(t='panel', box=TOP, text='NOAA：海が青いのは、水が、光の赤い側の色を吸収するから', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='NOAA：海は、太陽の光のフィルターのように働き、青い側の色が残る', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='水の中では、赤やオレンジの光が先に弱まり、青い光は比較的残りやすい（WHOI）', at=2, until=4, size=34),
   dict(t='panel', box=TOP, text='WHOI：数メートル潜ると、赤とオレンジは、ほとんど消える', at=4, until=5, size=40, hi=True),
   dict(t='panel', box=TOP, text='黄色と緑も弱まり、青と紫の光が、最も深くまで届く（WHOI）', at=5, until=6, size=38, hi=True),
   dict(t='panel', box=TOP, text='WHOI：青と紫の光は、水中の粒子で散乱され、水そのものが青く見える', at=6, size=36, col='gold'),
   dict(t='shade', box=[60, 250, 1860, 850], at=0, alpha=0.5),
   dict(t='anim', name='oceanlight', box=[60, 250, 1860, 850], at=0, until=7, mode='depth', s_a=0, s_b=4, s_c=5),
   dict(t='anim', name='oceanlight', box=[60, 250, 1860, 850], at=7, mode='scatter', s_a=7, s_b=8)]),
 dict(key='colors', title='いつも、青いのか', chapter_title='いつも、青いのか', scene=[
   dict(t='panel', box=TOP, text='NOAA：浮遊する堆積物や粒子で光が跳ね返ると、緑や赤など別の色にもなる', at=0, until=2, size=34, hi=True),
   dict(t='panel', box=TOP, text='WHOI：堆積物が多いと、水は茶色に見える', at=2, until=3, size=42),
   dict(t='panel', box=TOP, text='WHOI：植物プランクトンが多い場所では、緑や赤に見えることがある', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='WHOI：浅くて砂の底では、光が底で跳ね返り、鮮やかな青に見えることがある', at=4, size=34, col='gold'),
   dict(t='shade', box=[60, 250, 1860, 850], at=0, alpha=0.5),
   dict(t='chips', y=420, w=520, h=150, gap=60, size=40, items=[dict(at=0, text='堆積物 → 茶色'), dict(at=0, text='プランクトン → 緑・赤'), dict(at=0, text='浅い砂底 → 鮮やかな青')])]),
 dict(key='end', title='分かること、決められないこと', chapter_title='結論：分かること、決められないこと', scene=[
   dict(t='cols2', size=36, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=1, text='海が青い主な理由：水が赤い側の色を吸収し、青い側の色が残る（NOAA）'),
      dict(at=2, text='空は水面では映るが、水面の下でも青は残る（WHOI）'),
      dict(at=3, text='海は、空を映すだけの鏡ではない。水が光の色を選んで吸収し、残る光の色が変わる')]),
     right=dict(title='決められないこと', title_at=5, items=[
      dict(at=6, text='空の反射や水中の粒子が、色にどのくらい影響するかは、場所や条件で変わる'),
      dict(at=7, text='この動画の資料だけでは、その割合は分からない')]))])
 ],
 desc=dict(title_main='海が青いのは、空が映っているからなのか', title_no=1,
  titles=['海が青いのは、空が映っているから？ NOAAの解説で確かめる', '海が青い本当の理由は？ 空の映り込みと水の吸収を確かめる', '海が青いのは空のせいじゃない？ NOAAとWHOIの解説で確かめる'],
  intro='「海が青いのは、空が青くて、その空が水面に映っているから」。そう思っていませんか。空が映るのは本当です。でも、それだけでは海が青い理由を説明できません。この動画では、NOAAとウッズホール海洋研究所(WHOI)の解説から、海の色を確かめます。空は映るのか、水は光をどうするのか、いつも青いのか、を分けて見ていきます。分かることと決められないことを分けて、各機関の説明に帰属して述べます。',
  points=['WHOIの解説では、空を映しているという考えは水面では正しく、沿岸の水は嵐の日に灰色、日の出・日の入りにピンク色に見えることがあります。しかし水面の下に潜っても青い色は残り、青い色は水そのものがつくる、と説明されています(WHOI「Why is the ocean blue?」)。', 'NOAAの解説によると、海が青いのは、水が光の赤い側の色を吸収するからです。海は太陽光のフィルターのように働き、青い側の色が残ります(NOAA National Ocean Service「Why is the ocean blue?」)。', 'WHOIは、波長の長い色は水に吸収され、数メートル潜ると赤とオレンジはほとんど消え、黄色と緑も弱まって、青と紫が最も深くまで届き、水中の粒子で散乱されて水そのものが青く見える、と説明しています(WHOI)。', '海は、浮遊する堆積物や粒子で光が跳ね返ると、緑や赤など別の色になることもあります(NOAA)。堆積物で茶色、植物プランクトンで緑や赤、浅い砂の底では鮮やかな青に見えることがある、とWHOIは説明しています。'],
  refs=['NOAA National Ocean Service「Why is the ocean blue?」:https://oceanservice.noaa.gov/facts/oceanblue.html', 'ウッズホール海洋研究所(WHOI)「Why is the ocean blue?」:https://whoi.edu/ocean-learning-hub/ocean-facts/why-is-the-ocean-blue/'],
  credit_lines=['・図:自作(NOAAとWHOIの説明をもとにした模式図です。実際の写真・観測値ではありません。深さの数値は示していません)', '・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実際の海の景色の再現ではありません)'],
  notes=['図は、解説を理解するための自作の模式図で、実際の写真・観測値ではありません。', '吸収と散乱が、青さにどのくらい影響しているかの割合、特定の海の色の要因は、この動画では確認していません。', '「数メートル」はWHOIの説明に基づく言い方で、具体的な深さの数値は確認していません。'],
  tags='海, 海の色, 青, 水, 光, 吸収, 散乱, NOAA, 科学, 雑学, 検証',
  checks=['NOAAとWHOIの原文を、公開前にもう一度開いて確認する(`docs/themes/20261110_oceanblue/08_fact_check.md`)', 'WHOIの「浅い砂底」の説明の前提(水の澄み具合)を原文で確認する']),
 thumb=dict(bg='assets/oceanblue/thumb_art.png', lines=[['海が青いのは', 90, 'white'], ['空が映って', 90, 'white'], ['いるから？', 120, 'gold']], sub='NOAAとWHOIの解説で確かめる', shade_col=[6, 30, 60], accent=[120, 215, 255], bar_col=[120, 215, 255], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


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
inject(spec, dict(intro='intro', sky='sky', light='light', colors='colors', end='end'))
(R / 'data' / 'oceanblue_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
