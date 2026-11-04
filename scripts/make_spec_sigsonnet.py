"""Writes data/sigsonnet_spec.json（信号の青は、なぜ緑に見えるのか。モデル比較検証・Sonnet 5.5）。台本：docs/themes/20261104_signal/09_script_v2.md（固定）"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
BG = dict(t='anim', name='pop_bgimg', dim=0.3, blur=3, seg=22)


def bg(img, alts):
    return dict(BG, img=img, at=0, alts=alts)


def telop(text, at, until=None, y=330, size=100, plate=None, rot=-1.5, x=960):
    d = dict(t='anim', name='pop_telop', text=text, x=x, y=y, size=size, at=at, plate=plate, rot=rot, maxw=1560)
    if until is not None:
        d['until'] = until
    return d


def rows(items, y0, size=56, x0=110, x1=1810, gap=16):
    return dict(t='anim', name='pop_rows', items=items, x0=x0, x1=x1, y0=y0, size=size, gap=gap)


spec = dict(slug='sigsonnet', theme_dir='20261104_signal', pack='sigcmp_sigsonnet', header_sub='法令と言葉の歴史で確かめる', style='pop',
 images={n: dict(file=f'assets/sigcmp/art_{n}.png') for n in ('intro', 'law', 'world')},
 bgm=[['intro', 'history', 'piano35'], ['language', 'end', 'acoustic47']],
 chapters=[
 dict(key='intro', title='信号の青は、緑じゃない？', chapter_title='導入：信号の青は、緑じゃない？', scene=[
   bg('intro', ['law', 'world']),
   telop('信号の青は、[[緑色]]に見えない？', 0, 2, y=340, size=104, plate='blue'),
   telop('[[青信号]]なのに、見た目は緑', 1, 3, y=600, size=96, plate='green', rot=1.5),
   rows([dict(at=2, tag='とされる', text='日本語の「青」の歴史から来た呼び方', col='orange')], y0=290),
   rows([dict(at=3, tag='確かめる', text='法令と、言葉の面から', col='orange')], y0=460)]),
 dict(key='law', title='法令では何色？', chapter_title='法令では何色？', scene=[
   bg('law', ['intro']),
   telop('まず、[[法令]]', 0, 1, y=420, size=130, plate='yellow'),
   rows([dict(at=1, tag='道路交通法施行令', text='信号の灯火の意味は「青色の灯火」', col='orange', until=3)], y0=260),
   telop('法令の名前も[[「青色」]]', 2, 3, y=560, size=100, plate='blue'),
   rows([dict(at=3, tag='とされる', text='実際に光る色は、緑のなかでも青みの強い色', col='green', until=4)], y0=260),
   telop('名前は[[青]]、見た目は[[緑寄り]]', 4, y=430, size=104, plate='red')]),
 dict(key='history', title='日本初の信号機', chapter_title='日本初の信号機', scene=[
   bg('intro', ['law', 'world']),
   telop('[[1930年]]', 0, 1, y=520, size=140, plate='yellow'),
   rows([dict(at=0, tag='とされる', text='日比谷交差点に三色灯の信号機', col='orange', until=1)], y0=250),
   telop('進めは「[[青]]」と呼ぶ言い方が定着', 1, 2, y=450, size=88, plate='blue'),
   rows([dict(at=2, tag='英語', text='green light（グリーンライト）', col='green', until=3)], y0=260),
   telop('[[green light]]', 2, 3, y=520, size=130, plate='green'),
   telop('日本語だけが、[[特別]]ではない', 3, y=450, size=96, plate='pink')]),
 dict(key='language', title='言葉の「青」', chapter_title='言葉の「青」', scene=[
   bg('world', ['intro', 'law']),
   telop('昔の「青」は、[[緑も含む]]？', 0, 1, y=420, size=104, plate='green'),
   rows([dict(at=1, tag='例', text='緑のものにも「青」が付く', col='green', until=2)], y0=250),
   telop('[[青]]葉・[[青]]菜・[[青]]りんご', 1, 2, y=520, size=110, plate='green'),
   rows([dict(at=2, tag='説がある', text='古い日本語の基本の色名は4つ', col='orange', until=3)], y0=250),
   telop('あか・くろ・しろ・[[あお]]', 2, 3, y=520, size=110, plate='orange'),
   telop('信号の青も、その[[名残]]', 3, y=450, size=100, plate='purple')]),
 dict(key='world', title='他の国では？', chapter_title='他の国では？', scene=[
   bg('world', ['intro', 'law']),
   telop('青と緑の区別は、[[言語しだい]]', 0, 1, y=320, size=96, plate='yellow'),
   rows([dict(at=1, tag='韓国語', text='青信号は「パランブル」', col='cyan', until=3)], y0=260),
   telop('パランブル＝[[青い火]]', 1, 2, y=640, size=104, plate='blue'),
   rows([dict(at=2, tag='ベトナム語', text='青と緑を、一つの色の言葉で指す', col='cyan')], y0=400),
   telop('[[青と緑]]を一語で指す', 2, 3, y=640, size=104, plate='blue'),
   telop('色の切り方は、言語で[[違う]]', 3, y=620, size=96, plate='green')]),
 dict(key='end', title='結論', chapter_title='結論', scene=[
   bg('intro', ['world', 'law']),
   telop('[[結論]]', 0, 1, y=430, size=150, plate='yellow'),
   rows([dict(at=1, tag='考えられる', text='日本語の「青」の使い方を受け継いだ名前', col='orange'),
         dict(at=2, tag='法令', text='名前は青色 ／ 光る色は緑寄り', col='green')], y0=230, gap=22),
   telop('名前は、[[受け継いだ]]もの', 1, 3, y=600, size=100, plate='purple'),
   telop('緑に見えるのは、[[間違いじゃない]]', 3, 4, y=600, size=92, plate='red'),
   telop('信号待ちで、[[思い出して]]', 4, y=600, size=100, plate='blue')])
 ],
 desc=dict(title_main='信号の青は、なぜ緑色に見えるのか', title_no=1,
  titles=['信号の青は、なぜ緑色に見える？ 法令と言葉の歴史で確かめる'],
  intro='信号の青は、本当は緑色に見えませんか。青信号と呼ぶのに、見た目は緑に近い。この動画では、その理由を、法令と言葉の面から確かめます。',
  points=['道路交通法施行令は、信号の灯火の意味を「青色の灯火」と書いています。', '日本語の「青」は、昔は緑も含む広い色の名前だったと考えられています（説）。'],
  refs=['道路交通法施行令 第2条（e-Gov法令検索）'],
  credit_lines=['・背景イラスト:ChatGPT(OpenAI)による生成イラスト(イメージです)'],
  notes=['K2〜K5は未確認で、「とされる」「説がある」の表現で述べています。'],
  tags='信号, 青信号, 緑, 日本語, 色, 雑学, 検証',
  checks=['K2〜K5の出典を、公開前に確認する']),
 thumb=dict(bg='assets/sigcmp/art_intro.png', lines=[['青信号は', 110, 'white'], ['緑色？', 130, 'gold']], sub='法令と言葉で確かめる'))
(R / 'data' / 'sigsonnet_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8')
print('spec written')
