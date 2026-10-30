"""Writes data/shinkansen_spec.json（新幹線の遅延は、平均で何秒？）。台本：docs/themes/20261226_shinkansen/09_script_v2.md
at / until は『章内の行番号（0始まり）』。末尾で文の番号に直す。"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
R = Path(__file__).resolve().parents[1]
from specart import inject
TOP = [60, 170, 1860, 235]
spec = dict(slug='shinkansen', theme_dir='20261226_shinkansen', pack='46_shinkansen', header_sub='JR東海の資料と記事の数字で、新幹線の遅れを確かめる',
 images={},
 bgm=[['intro', 'y16', 'piano36'], ['compare', 'avg', 'piano12'], ['disaster', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='新幹線の遅れは、平均で何秒？', chapter_title='導入：新幹線の遅れは、平均で何秒？', opener='新幹線の遅れは、平均で何秒？', opener_until=1, scene=[
   dict(t='big', text='新幹線の遅れは、平均で何秒？', y=270, at=0, size=54, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='「平均の遅れは、数十秒」と聞いたことはありませんか？', at=1, size=40, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：JR東海の資料と、報道記事', at=3, size=38),
   dict(t='panel', box=[120, 750, 1800, 830], text='答え：年度で違う。2016年度は24秒、2024年度は1.4分（84秒）', at=4, size=36, col='gold')]),
 dict(key='y24', title='2024年度の数字', chapter_title='2024年度の数字', scene=[
   dict(t='panel', box=TOP, text='JR東海のサステナビリティのページに、2024年度の数字がある', at=0, until=1, size=36, hi=True),
   dict(t='panel', box=TOP, text='平均遅延時分：運行1列車あたり1.4分', at=1, until=2, size=38, col='gold'),
   dict(t='panel', box=TOP, text='注記：自然災害等による遅延も含む', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='1.4分＝60秒×1.4＝84秒（自作の計算）', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='1日の本数：383本（臨時列車を含む）。輸送人員：1日46万人', at=4, size=36),
   dict(t='table', box=[60, 300, 1860, 640], cols=['東海道新幹線（2024年度）', '数字'], colw=[1100, 700], size=38, rows=[
     dict(at=1, cells=['平均遅延時分（運行1列車あたり）', '1.4分（84秒）'], col='gold'),
     dict(at=2, cells=['注記', '自然災害等による遅延も含む']),
     dict(at=4, cells=['列車本数（臨時列車を含む）', '383本／日']),
     dict(at=4, cells=['輸送人員', '約46万人／日'])])]),
 dict(key='y16', title='「24秒」は、どこから来たのか', chapter_title='「24秒」は、どこから来たのか', scene=[
   dict(t='panel', box=TOP, text='「平均24秒」という数字も、広く知られている', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='2016年度：年間約13万本、1列車あたりの平均遅延時間は24秒', at=1, until=2, size=38),
   dict(t='panel', box=TOP, text='この記事も、自然災害による遅延を含む数字と書いている', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='表の注記：JR東海アニュアルレポート2017をもとに編集部作成', at=3, until=4, size=36),
   dict(t='panel', box=TOP, text='アニュアルレポートの原本は、この動画では未確認', at=4, size=40, col='gold'),
   dict(t='table', box=[60, 300, 1860, 680], cols=['2016年度（nippon.com・二次情報）', '数字'], colw=[760, 1040], size=34, rows=[
     dict(at=1, cells=['年間の運行本数', '約13万本']),
     dict(at=1, cells=['1列車あたりの平均遅延時間', '24秒'], col='gold'),
     dict(at=2, cells=['自然災害による遅延', '含む']),
     dict(at=3, cells=['出典の記載', 'JR東海アニュアルレポート2017をもとに編集部作成'])])]),
 dict(key='compare', title='数字を、並べてみる', chapter_title='数字を、並べてみる', scene=[
   dict(t='panel', box=TOP, text='2016年度：24秒。2024年度：84秒', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='差は60秒。84÷24で、約3.5倍', at=1, until=2, size=38),
   dict(t='panel', box=TOP, text='2つの数字だけで「3.5倍悪くなった」とは言えない。集計方法は未確認', at=2, until=3, size=34, col='gold'),
   dict(t='panel', box=TOP, text='別の記事：2015年度は0.2分（12秒）。2019年度も0.2分という記述（原本は未確認）', at=3, until=4, size=32),
   dict(t='panel', box=TOP, text='古い資料：2002〜2005年度は、0.4分・0.1分・0.7分・0.6分（2008年作成の自治体の資料）', at=4, until=5, size=30),
   dict(t='panel', box=TOP, text='年度によって、数字が大きく動くことは確かなようだ', at=5, size=40, col='gold'),
   dict(t='table', box=[60, 300, 1860, 700], cols=['年度（二次情報）', '平均遅延時分'], colw=[1100, 700], size=32, rows=[dict(at=3, cells=['2015年度（記事）', '0.2分（12秒）']), dict(at=3, cells=['2019年度（記事）', '0.2分']), dict(at=4, cells=['2002年度（自治体の資料）', '0.4分']), dict(at=4, cells=['2003年度', '0.1分']), dict(at=4, cells=['2004年度', '0.7分']), dict(at=4, cells=['2005年度', '0.6分'])]),
   dict(t='bars', box=[60, 300, 1860, 640], title='1列車あたりの平均遅延（秒に換算。年度で出典が異なる）', unit='秒', max=100, lab_w=620, data=[dict(at=0, label='2016年度（二次情報）', value=24, vlabel='24秒', col='blue', until=3), dict(at=0, label='2024年度（JR東海）', value=84, vlabel='84秒', col='gold', until=3)])]),
 dict(key='total', title='遅れを、合計すると', chapter_title='遅れを、合計すると', scene=[
   dict(t='panel', box=TOP, text='平均を、身近な量に直してみる', at=0, until=1, size=38),
   dict(t='panel', box=TOP, text='2024年度：1日383本×平均1.4分', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='掛けると約536分＝約8.9時間分', at=2, until=3, size=38, col='gold'),
   dict(t='panel', box=TOP, text='集計の定義は未確認。年度の平均からの仮定による概算で、実際の一日の合計ではない', at=3, until=4, size=36),
   dict(t='panel', box=TOP, text='2016年度：年間約13万本×24秒＝約5.2万分＝約867時間分', at=4, until=5, size=36),
   dict(t='panel', box=TOP, text='本数が多いので、平均が小さくても、合計は大きくなる', at=5, size=40, col='gold'),
   dict(t='table', box=[60, 300, 1860, 640], cols=['自作の概算（仮定による試算）', '計算', '結果'], colw=[600, 760, 440], size=34, rows=[
     dict(at=2, cells=['2024年度・1日あたり', '383本×1.4分', '約536分（約8.9時間）'], col='gold'),
     dict(at=4, cells=['2016年度・年間', '約13万本×24秒', '約5.2万分（約867時間）'])])]),
 dict(key='avg', title='「平均」は、何を意味するか', chapter_title='「平均」は、何を意味するか', scene=[
   dict(t='panel', box=TOP, text='「平均」という言葉を、考えてみる', at=0, until=1, size=38),
   dict(t='panel', box=TOP, text='平均1.4分＝すべての列車が、1.4分ずつ遅れる、ではない', at=1, until=2, size=38, hi=True),
   dict(t='panel', box=TOP, text='仮に、ほとんどが定刻でも、一部が大きく遅れれば、平均は上がる', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='例：100本のうち99本が定刻で、1本が140分遅れる→平均1.4分', at=3, until=4, size=36, col='gold'),
   dict(t='panel', box=TOP, text='この例は考え方を示すもの。実際の分布は未確認', at=4, size=40),
   dict(t='table', box=[60, 300, 1860, 560], cols=['たとえ話（実際の分布ではない）', '遅れ'], colw=[1100, 700], size=38, rows=[
     dict(at=3, cells=['99本', '0分（定刻）']),
     dict(at=3, cells=['1本', '140分'], col='gold'),
     dict(at=3, cells=['100本の平均', '1.4分'], col='gold')])]),
 dict(key='disaster', title='自然災害を含む、ということ', chapter_title='自然災害を含む、ということ', scene=[
   dict(t='panel', box=TOP, text='JR東海の数字には、自然災害等による遅延も含まれる', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='大雨・地震・大雪で大きく遅れた日が増えれば、年度の平均も上がる', at=1, until=2, size=36),
   dict(t='panel', box=TOP, text='2024年度の1.4分のうち、災害が何分分かは、資料からはわからない', at=2, until=3, size=34, col='gold'),
   dict(t='panel', box=TOP, text='災害を除いた数字は、この動画では未確認', at=3, size=40)]),
 dict(key='know', title='わかることと、わからないこと', chapter_title='わかることと、わからないこと', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='わかること', title_at=0, items=[
      dict(at=0, text='JR東海は、2024年度の平均遅延時分を1.4分と示している'),
      dict(at=1, text='2016年度は24秒と紹介されている（二次情報）')]),
     right=dict(title='わからないこと', title_at=2, items=[
      dict(at=2, text='何分以上を遅れと数えるのか（定義）'),
      dict(at=2, text='途中の年度の数字（確かめきれていない）'),
      dict(at=3, text='他の国や飛行機との比較（根拠が未確認なので扱わない）')]))]),
 dict(key='read', title='数字を読むときの三つの確認', chapter_title='数字を読むときの三つの確認', scene=[
   dict(t='panel', box=TOP, text='「平均遅延は何秒」の数字を見たとき、確かめたいこと', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='① いつの年度か：24秒＝2016年度、1.4分＝2024年度', at=1, until=2, size=38),
   dict(t='panel', box=TOP, text='② 何を含むか：どちらも、自然災害等による遅延を含む', at=2, until=3, size=38),
   dict(t='panel', box=TOP, text='③ 平均か、一本ごとの数字か：平均は、一本ごとの遅れはわからない', at=3, until=4, size=34, col='gold'),
   dict(t='panel', box=TOP, text='この3つで、同じ「新幹線の遅れ」でも数字が違う理由が見えてくる', at=4, size=36),
   dict(t='table', box=[60, 300, 1860, 640], cols=['確認すること', '24秒', '1.4分（84秒）'], colw=[760, 520, 520], size=36, rows=[
     dict(at=1, cells=['① 年度', '2016年度', '2024年度']),
     dict(at=2, cells=['② 自然災害等の遅延', '含む', '含む']),
     dict(at=3, cells=['③ 数字の種類', '平均', '平均'], col='gold')])]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かったこと', title_at=0, items=[
      dict(at=1, text='2016年度は24秒、2024年度は1.4分（84秒）。どちらも自然災害等を含む'),
      dict(at=2, text='平均は、一本ごとの遅れを示すものではない')]),
     right=dict(title='言い方の注意', title_at=3, items=[
      dict(at=3, text='数字を見るときは、年度と、何を含むかを確かめる')]))]),
 ],
 desc=dict(title_main='新幹線の遅れは、平均で何秒なのか', title_no=1,
  titles=['新幹線の遅延は、平均で何秒？ JR東海の資料と記事で確かめる', '東海道新幹線の平均遅延：2016年度は24秒、2024年度は1.4分（84秒）', '新幹線の「平均24秒」は本当？ 年度で違う数字と「平均」の読み方'],
  intro='「新幹線の平均の遅れは、数十秒」。そう聞いたことはありませんか。この動画では、JR東海の資料と報道記事の数字で、東海道新幹線の平均遅延を確かめます。',
  points=['JR東海は、東海道新幹線の2024年度の平均遅延時分を、運行1列車あたり1.4分(84秒)と示しています。自然災害等による遅延も含みます。', '2016年度は、1列車あたり24秒と、報道記事で紹介されています(JR東海アニュアルレポート2017をもとに編集部が作成した表。原本は未確認)。', '年度によって数字は動きます。2つの数字だけで、定時運行が3.5倍悪くなったとは言えません。', '平均は、全体をならした数字で、一本ごとの遅れを示すものではありません。', '遅延の定義(何分以上を遅れと数えるか)と、途中の年度の数字は、確かめきれていません。'],
  refs=['JR東海「東海道新幹線～不断のサービスの充実～」:https://company.jr-central.co.jp/sustainability/social/service/', '国際高速鉄道協会「新幹線のKey Facts」:https://www.ihra-hsr.org/jp/hsr/_pdf/keyfact.pdf', 'nippon.com「東海道新幹線の平均遅延時間は24秒」(2016年度。二次情報):https://www.nippon.com/ja/features/h00201/', '現代ビジネス(gendai.media)の記事(2015年度の12秒。二次情報):https://gendai.media/articles/-/54719', '鉄道コム(tetsudo.com)の記事(JR東海アニュアルレポート2020を引用。2019年度の0.2分。二次情報):https://www.tetsudo.com/report/300/', '小樽市の資料「新幹線の定時性」(2008年作成。2002〜2005年度の数字。出典は政府・与党整備新幹線検討委員会ワーキンググループ資料の注記):https://www.city.otaru.lg.jp/docs/2020120400236/file_contents/P8.pdf'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['84秒(1.4分)、約3.5倍、約536分(約8.9時間)、約867時間は、公表値や記事の数字からの自作の計算(概算)です。', '2016年度の24秒、2015年度の0.2分(12秒)、2019年度の0.2分、2002〜2005年度の0.4・0.1・0.7・0.6分は、記事や自治体の資料(2008年作成)で紹介された二次情報で、JR東海の原本は確認できていません。', '遅延の定義(何分以上を遅れと数えるか)、2017〜2023年度の数字、他の国・飛行機との比較は、確かめていません。'],
  tags='新幹線, 東海道新幹線, 遅延, JR東海, 定時運行, 平均, 検証, 鉄道',
  checks=['JR東海のアニュアルレポート(2017など)の原本で、平均遅延時分の年度別の数字と定義を確認する', '2025年度の数字が公表されたら、更新する']),
 thumb=dict(bg='assets/shinkansen/thumb_art.png', lines=[['新幹線の遅れ', 100, 'white'], ['平均', 110, 'white'], ['何秒？', 130, 'gold']], sub='JR東海の資料で確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=38, shade_x=700, shade_w=520))


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
    t = (R / 'docs' / 'themes' / '20261226_shinkansen' / '09_script_v2.md').read_text(encoding='utf8')
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
_ART = {'intro': 'intro', 'y24': 'platform', 'y16': 'tracks', 'compare': 'tracks', 'total': 'platform', 'avg': 'tracks', 'disaster': 'storm', 'know': 'platform', 'read': 'tracks', 'end': 'intro'}
if all((R / 'assets' / 'shinkansen' / f'art_{v}.png').exists() for v in set(_ART.values())):
    inject(spec, _ART)
(R / 'data' / 'shinkansen_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
