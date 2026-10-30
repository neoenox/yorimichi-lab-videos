"""Writes data/vitaminc_spec.json（ビタミンCは、風邪に効く？）。台本：docs/themes/20261226_vitaminc/09_script_v2.md"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from specart import inject
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]
spec = dict(slug='vitaminc', theme_dir='20261226_vitaminc', pack='30_vitaminc', header_sub='コクランのレビュー（2013年）で、ビタミンCと風邪を確かめる',
 images={},
 bgm=[['intro', 'method', 'piano36'], ['general', 'after', 'piano12'], ['safety', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='ビタミンCは、風邪に効く？', chapter_title='導入：ビタミンCは、風邪に効く？', opener='ビタミンCは、風邪に効く？', opener_until=1, scene=[
   dict(t='big', text='ビタミンCは、風邪に効く？', y=270, at=0, size=58, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='毎日とるのか、ひいてからとるのか。誰がとるのか。それで結果が分かれる', at=3, size=42, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='資料：コクランのレビュー（2013年）・厚生労働省', at=4, size=34)]),
 dict(key='why', title='なぜ、効くと言われるのか', chapter_title='なぜ、効くと言われるのか', scene=[
   dict(t='panel', box=TOP, text='ビタミンCは、壊血病に効く（前の動画）', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='風邪にも効く？ この話が広まったのは、1970年代', at=1, until=2, size=40),
   dict(t='panel', box=TOP, text='1970年：ポーリング（ノーベル賞を2度受賞）が、ビタミンCと風邪の本を書いた', at=2, until=3, size=34, hi=True),
   dict(t='panel', box=TOP, text='主張：大量のビタミンCで、風邪を予防し、軽くできる', at=3, until=4, size=40, col='gold'),
   dict(t='panel', box=TOP, text='大きな関心を集め、その後、たくさんの試験が行われた', at=4, size=40)]),
 dict(key='method', title='コクランのレビューとは', chapter_title='コクランのレビューとは', scene=[
   dict(t='panel', box=TOP, text='試験を、まとめて分析する（コクランのレビュー）', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='ビタミンCと風邪のレビュー：2013年公開（2012年11月までの論文）', at=1, until=2, size=38),
   dict(t='panel', box=TOP, text='偽薬と比べた試験／ビタミンC 1日0.2g以上／44論文・63の比較', at=2, until=3, size=38, hi=True),
   dict(t='panel', box=TOP, text='ふだんの食事に加えて、とった場合の話', at=3, size=40, col='gold'),
   dict(t='chips', y=330, w=520, h=150, gap=60, size=40, items=[dict(at=1, text='2013年のレビュー'), dict(at=2, text='44論文・63比較'), dict(at=3, text='追加でとる場合')])]),
 dict(key='general', title='毎日とると、風邪をひかなくなるのか', chapter_title='毎日とると、風邪をひかなくなるのか', scene=[
   dict(t='panel', box=TOP, text='毎日、追加でとり続けた一般の人：1万700人あまり', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='風邪をひいた人の割合を、偽薬の群と比べた比：0.97', at=1, until=2, size=40, hi=True),
   dict(t='panel', box=TOP, text='1なら変わらない。0.97は、ほとんど変わらない', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='追加でとり続けても、風邪をひく人はほとんど減らない', at=3, until=4, size=40, col='gold'),
   dict(t='panel', box=TOP, text='著者：一般の人が日常的にとり続けることは、正当化できない', at=4, size=38),
   dict(t='bars', box=[60, 300, 1860, 560], title='風邪をひいた人の割合の比（偽薬の群＝1）', unit='', max=1.1, lab_w=520, data=[
     dict(at=1, label='偽薬の群', value=1.0, vlabel='1.00', col='blue'),
     dict(at=1, label='一般の人（1万700人あまり）', value=0.97, vlabel='0.97（95%区間 0.94〜1.00）', col='org')])]),
 dict(key='except', title='例外は、あるのか', chapter_title='例外は、あるのか', scene=[
   dict(t='panel', box=TOP, text='例外がある', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='短い間に、強い運動をする人：マラソン走者・スキー選手・寒い地域の演習の兵士', at=1, until=2, size=34),
   dict(t='panel', box=TOP, text='5試験・598人：比は 0.48', at=2, until=3, size=40, hi=True),
   dict(t='panel', box=TOP, text='偽薬の群と比べて、風邪をひく割合が、約半分', at=3, until=4, size=40, col='gold'),
   dict(t='panel', box=TOP, text='人数は約600人。一般の人（1万人あまり）と比べると少ない（自作）', at=4, until=5, size=36),
   dict(t='panel', box=TOP, text='この5試験の結果を、運動をする人すべてに広げることはできない', at=5, size=38, col='gold'),
   dict(t='bars', box=[60, 300, 1860, 600], title='風邪をひいた人の割合の比（偽薬の群＝1）', unit='', max=1.1, lab_w=520, data=[
     dict(at=0, label='偽薬の群', value=1.0, vlabel='1.00', col='blue'),
     dict(at=0, label='一般の人（1万700人あまり）', value=0.97, vlabel='0.97', col='org'),
     dict(at=2, label='強い運動をする人（598人）', value=0.48, vlabel='0.48（95%区間 0.35〜0.64）', col='grn')])]),
 dict(key='duration', title='ひいたとき、早く治るのか', chapter_title='ひいたとき、早く治るのか', scene=[
   dict(t='panel', box=TOP, text='毎日とっていた人が、風邪をひいたとき', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='風邪の期間は、平均して、成人で8%、子どもで14%、短くなった', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='子どもに1日1〜2gの試験だけを見ると、18%短くなった（その量を勧める意味ではない）', at=2, until=3, size=32),
   dict(t='panel', box=TOP, text='症状の重さも、小さな改善が報告されている', at=3, until=4, size=40),
   dict(t='panel', box=TOP, text='たとえば、1週間の風邪が8%短くなると、半日ほど（自作の計算）', at=4, size=38, col='gold'),
   dict(t='bars', box=[60, 300, 1860, 600], title='風邪の期間が短くなった割合（%・平均）', unit='%', max=22, lab_w=520, data=[
     dict(at=1, label='成人', value=8, vlabel='8%（95%区間 3〜12%）', col='blue'),
     dict(at=1, label='子ども', value=14, vlabel='14%（95%区間 7〜21%）', col='grn'),
     dict(at=2, label='子ども（1日1〜2gの試験）', value=18, vlabel='18%', col='org')])]),
 dict(key='after', title='ひいてから、とっても効くのか', chapter_title='ひいてから、とっても効くのか', scene=[
   dict(t='panel', box=TOP, text='風邪をひいてから、とった場合は？', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='7つの比較・風邪の件数で約3,200件', at=1, until=2, size=40),
   dict(t='panel', box=TOP, text='風邪の期間にも、重さにも、一貫した効果は見られなかった', at=2, until=3, size=40, hi=True),
   dict(t='panel', box=TOP, text='この種類の試験は数が少なく、子どもは含まれていない', at=3, until=4, size=40),
   dict(t='panel', box=TOP, text='毎日とった人では短くなったが、ひいてからでは確かめられていない', at=4, size=36, col='gold'),
   dict(t='panel', box=[60, 300, 930, 520], title='毎日とる（追加で）', text='風邪の期間：平均して短くなった（成人8%・子ども14%）', at=3, size=36, hi=True),
   dict(t='panel', box=[990, 300, 1860, 520], title='ひいてからとる', text='一貫した効果は見られなかった（試験が少ない）', at=4, size=36, col='gold')]),
 dict(key='safety', title='安全なのか、日本の基準は', chapter_title='安全なのか、日本の基準は', scene=[
   dict(t='panel', box=TOP, text='安全面は？（コクランの著者の見方）', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='発表された試験では、副作用は報告されていない。重い症状の報告もない', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='1日1g以上の大規模な7試験：薬のせいと感じた症状の自己申告は、ほぼ同じ', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='ただし、調べた試験と量についての話。全条件で安全とは確かめられていない', at=3, until=4, size=34, col='gold'),
   dict(t='panel', box=TOP, text='試験で使った量と、ふだんの栄養の基準は、目的が違う', at=4, until=5, size=40),
   dict(t='panel', box=TOP, text='厚生労働省（2025年版）：成人の推奨量は、男女とも、1日100mg', at=5, until=6, size=38, hi=True),
   dict(t='panel', box=TOP, text='推定平均必要量：壊血病を防ぐ最小量だけでなく、良好な栄養状態を保つ考えで決定', at=6, until=7, size=34),
   dict(t='panel', box=TOP, text='風邪の予防や治療のための量ではない', at=7, size=40, col='gold'),
   dict(t='bars', box=[60, 300, 1860, 540], title='薬のせいと感じた症状を自分で申告した人の割合（%）', unit='%', max=8, lab_w=520, data=[
     dict(at=2, label='ビタミンCの群', value=5.8, vlabel='5.8%', col='blue'),
     dict(at=2, label='偽薬の群', value=6.0, vlabel='6.0%', col='org')]),
   dict(t='panel', box=[60, 580, 930, 800], title='試験で使った量（コクラン）', text='1日0.2g（200mg）以上を、追加でとる', at=4, size=36, hi=True),
   dict(t='panel', box=[990, 580, 1860, 800], title='日本の推奨量（成人）', text='1日100mg（男女とも）', at=5, size=36, hi=True)]),
 dict(key='end', title='分かること、決められないこと', chapter_title='結論：分かること、決められないこと', scene=[
   dict(t='cols2', size=34, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=1, text='追加で毎日とっても、一般の人の風邪は、ほとんど減らない'),
      dict(at=2, text='短い間に強い運動をする人（5試験）では、約半分'),
      dict(at=3, text='毎日とっていた人の風邪は、平均して成人8%・子ども14%短い')]),
     right=dict(title='決められないこと', title_at=4, items=[
      dict(at=4, text='ひいてから、とって、効くのか（試験が少ない）'),
      dict(at=5, text='2013年のレビューまで。それ以後の試験は確認していない'),
      dict(at=6, text='著者は、自分で試す価値はあるかもしれないと述べた（効くと確かめられた意味ではない）')]))])
 ],
 desc=dict(title_main='ビタミンCは、風邪に効くのか', title_no=1,
  titles=['ビタミンCは、風邪に効く？ コクランのレビューで確かめる', '風邪にビタミンCは効く？ 毎日とる・ひいてからとるで結果が分かれる', 'ビタミンCと風邪：予防は？ 早く治る？ 2013年のレビューの数字を確かめる'],
  intro='「風邪をひかないように、ビタミンCをとる」「風邪をひいたら、ビタミンCをとる」。そんな人は多いのではないでしょうか。この動画では、世界の臨床試験をまとめたコクランのレビュー（2013年）で、ビタミンCは風邪に効くのかを確かめます。毎日とるのか、ひいてからとるのか、誰がとるのかで、結果が分かれます。',
  points=['コクランのレビュー(Hemilä & Chalker、2013年1月公開、2012年11月までの論文)は、偽薬と比べた試験のうち、ビタミンCを1日0.2g以上、追加でとったものを集めています(44論文・63の比較)。', '毎日とり続けた一般の人(約1万700人)で、風邪をひいた人の割合の比は0.97(95%区間0.94〜1.00)で、ほとんど変わりませんでした。', 'マラソン走者・スキー選手・寒い地域で演習をする兵士など、短い間に強い運動をする人(5試験・598人)では、比は0.48(95%区間0.35〜0.64)で、風邪をひく割合が約半分でした。', '毎日とっていた人が風邪をひいたとき、期間は平均して成人で8%、子どもで14%短くなりました。ひいてから、とった場合(7つの比較・約3,200件)は、期間・重さに一貫した効果は見られませんでした。', 'レビューの著者は、発表された試験ではビタミンCの副作用は報告されていないとしています。大規模な7試験(1日1g以上)で、薬のせいと感じた症状を自分で申告した人は、ビタミンCの群5.8%、偽薬の群6.0%で、ほとんど同じでした。', '厚生労働省「日本人の食事摂取基準(2025年版)」では、成人の推奨量は男女とも1日100mgです。風邪の予防や治療のための量ではありません。'],
  refs=['Hemilä H, Chalker E.「Vitamin C for preventing and treating the common cold」Cochrane Database of Systematic Reviews 2013, Issue 1, CD000980:https://www.cochrane.org/CD000980/ARI_vitamin-c-preventing-and-treating-common-cold', 'レビューの全文(著者公開のPDF):https://www.mv.helsinki.fi/home/hemila/CC/CochraneColds_2013.pdf', '厚生労働省「日本人の食事摂取基準(2025年版) 策定のポイント」(2025年2月。策定検討会報告書 p.185〜242のビタミンCの表を含む):https://www.mhlw.go.jp/content/10904750/001734207.pdf'],
  credit_lines=['・図:自作(コクランのレビューの数字をもとにしたグラフです。比0.97・0.48は、偽薬の群を1としたときの、風邪をひいた人の割合の比で、実際の割合ではありません)', '・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実際の人物・場面・製品の再現ではありません)'],
  notes=['この動画で見たのは、2013年のコクランのレビューです。それ以後の試験・更新は確認していません。', '「風邪の期間が半日ほど」は、1週間の風邪の8%を計算した自作の例です。', '「約半分」は、短い間に強い運動をした5試験の結果で、運動をする人すべてに当てはまるとは限りません。', '一般的な食事からとる量の話ではなく、サプリメントなどで追加でとった試験の結果です。体質や病気のある人、薬を飲んでいる人の摂取は、医師や薬剤師に相談してください。', '数字と、試験の期間中に風邪をひいた人の割合という指標の定義は、レビューの全文(著者公開のPDF)で確認しました。「コクランは国際的な団体」は一般的な説明で、原文の該当箇所は確認していません。'],
  tags='ビタミンC, 風邪, かぜ, コクラン, レビュー, ポーリング, サプリメント, 厚生労働省, 食事摂取基準, 科学, 雑学, 検証',
  checks=['コクランのレビューの2013年以降の更新・新しい試験の有無を確認する(docs/themes/20261226_vitaminc/08_fact_check.md)', 'NIH ODSのビタミンCのファクトシートを開いて、風邪の記述と矛盾がないか確認する(取得時は403)', '一般論としての安全性の記述が、医療の助言と受け取られないか、概要欄を確認する']),
 thumb=dict(bg='assets/vitaminc/thumb_art.png', lines=[['ビタミンCは', 96, 'white'], ['風邪に', 110, 'white'], ['効く？', 140, 'gold']], sub='コクランのレビューで確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


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
    """台本の番号つきの行（1行に複数の文がある）→ 各行の最初の文の番号（vp.py の sentences と同じく「。」で区切る）。
    この spec の at / until / title_at は『行の番号（0始まり）』で書き、ここで文の番号に直す。"""
    import re
    t = (R / 'docs' / 'themes' / '20261226_vitaminc' / '09_script_v2.md').read_text(encoding='utf8')
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
            if k in ('at', 'until', 'title_at') and isinstance(v, int): o[k] = f(v)
            else: _remap(v, st)
    elif isinstance(o, list):
        for v in o: _remap(v, st)


_S = _line_to_sentence_starts()
assert len(_S) == len(spec['chapters']), (len(_S), len(spec['chapters']))
for _ch, _st in zip(spec['chapters'], _S):
    _remap(_ch['scene'], _st)
    if 'opener_until' in _ch: _ch['opener_until'] = _st[min(_ch['opener_until'], len(_st) - 1)]

_fit(spec)
inject(spec, {'intro': 'intro', 'why': 'book', 'method': 'review', 'general': 'review', 'except': 'snow', 'duration': 'intro', 'after': 'book', 'safety': 'end', 'end': 'end'})
(R / 'data' / 'vitaminc_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
