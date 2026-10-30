"""Writes data/gps_spec.json（GPS衛星は、あなたの居場所を知っている？）。台本：docs/themes/20261114_gps/09_script_v2.md"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from specart import inject
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]
import shutil
_src = R / 'assets' / 'gps' / 'thumb_art.png'; _dst = R / 'assets' / 'gps' / 'art_finale.png'
if _src.exists() and not _dst.exists(): shutil.copy(_src, _dst)
spec = dict(slug='gps', theme_dir='20261114_gps', pack='25_gps', header_sub='GPSの仕組みを、GPS.govの説明で確かめる',
 images={},
 bgm=[['intro', 'sat', 'piano36'], ['device', 'out', 'piano12'], ['end', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='GPS衛星は、あなたの居場所を知っている？', chapter_title='導入：GPS衛星は、居場所を知っている？', opener='GPS衛星は、居場所を知っている？', opener_until=1, scene=[
   dict(t='big', text='GPS衛星は、あなたの居場所を、知っている？', y=270, at=0, size=56, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='スマホの地図は、居場所を表示する。では、空の上の衛星は？', at=1, size=42, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='資料：GPS.gov（アメリカ政府のGPS公式サイト）', at=2, size=34)]),
 dict(key='sat', title='衛星が送っているもの', chapter_title='衛星が送っているもの', scene=[
   dict(t='panel', box=TOP, text='GPS衛星：高さ約20,200kmの上空を回っている', at=0, until=1, size=42, hi=True),
   dict(t='panel', box=TOP, text='運用：アメリカ宇宙軍（GPS.gov）', at=1, until=2, size=44),
   dict(t='panel', box=TOP, text='衛星が電波で送る：自分の位置、状態、正確な時刻（GPS.gov）', at=2, until=3, size=40, hi=True),
   dict(t='panel', box=TOP, text='正確な時刻の元：衛星に積んだ原子時計', at=3, size=44, col='gold')]),
 dict(key='device', title='端末がすること', chapter_title='端末がすること', scene=[
   dict(t='panel', box=TOP, text='端末は、衛星の電波を受け取り、届いた時刻を記録する', at=0, until=1, size=42, hi=True),
   dict(t='panel', box=TOP, text='時間 × 光の速さ ＝ 衛星までの、おおよその距離', at=1, until=2, size=44),
   dict(t='panel', box=TOP, text='端末の時計にはずれがあるため、さらに計算が必要', at=2, until=3, size=42, col='gold'),
   dict(t='panel', box=TOP, text='位置を求めるには、通常、4基以上の衛星の電波を使う', at=3, until=4, size=42, hi=True),
   dict(t='panel', box=TOP, text='なぜ、4基も必要なのか？', at=4, until=5, size=44, hi=True),
   dict(t='panel', box=TOP, text='東西・南北・高さ＋端末の時計のずれ、の4つを求めるため', at=5, until=6, size=40, hi=True),
   dict(t='panel', box=TOP, text='こうして、緯度・経度・高さが分かる', at=6, until=7, size=44, col='gold'),
   dict(t='panel', box=TOP, text='この計算は、あなたの端末の中で行われる', at=7, size=44, col='gold'),
   dict(t='anim', name='gpsdevice', box=[60, 250, 1860, 850], at=0, s_a=0, s_b=1, s_c=2, s_d=3, s_e=4, s_f=6)]),
 dict(key='track', title='衛星は、追跡しているのか', chapter_title='衛星は、追跡しているのか', scene=[
   dict(t='panel', box=TOP, text='GPS.govのFAQ：GPS衛星そのものは、地上のものを追跡していない', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='灯台のように、一方向に、信号を送っているだけ', at=1, until=2, size=44),
   dict(t='panel', box=TOP, text='だから、運用する政府は、スマホの位置を特定できない（GPS.gov FAQ）', at=2, until=3, size=40, col='gold'),
   dict(t='panel', box=TOP, text='携帯電話会社などが、端末に組み込まれた機能で探せる場合は、別（同FAQ）', at=3, size=38, hi=True),
   dict(t='shade', box=[60, 250, 1860, 850], at=0, alpha=0.5),
   dict(t='anim', name='gpstrack', box=[60, 250, 1860, 850], at=0, s_a=0, s_b=1, s_c=2)]),
 dict(key='out', title='居場所が外に出るとき', chapter_title='居場所が外に出るとき', scene=[
   dict(t='chips', y=250, w=840, h=140, gap=80, size=44, items=[dict(at=0, text='居場所は、絶対に外に出ない？'), dict(at=1, text='→ いいえ。出ることがある')]),
   dict(t='panel', box=[60, 430, 1860, 530], text='MIT：GPSの計算そのものは、居場所を外へ知らせない', at=3, until=4, size=42, hi=True),
   dict(t='panel', box=[60, 430, 1860, 570], text='通信機能を持つ機器やサービスが、位置情報を外へ送る場合がある', at=4, size=40, hi=True),
   dict(t='panel', box=[60, 610, 1860, 720], text='位置の履歴を、端末に記録する場合もある。記録することと、外へ送ることは、別', at=5, size=38, col='gold')]),
 dict(key='end', title='分かること、決められないこと', chapter_title='結論：分かること、決められないこと', scene=[
   dict(t='cols2', size=38, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=1, text='GPS衛星そのものは、地上の人やスマホを追跡していない'),
      dict(at=2, text='衛星は一方向に電波を送り、端末が自分の位置を計算する'),
      dict(at=3, text='居場所が誰かに知られる可能性はある（通信機能・アプリ）')]),
     right=dict(title='決められないこと', title_at=5, items=[
      dict(at=6, text='どのアプリが、どこへ位置情報を送っているか'),
      dict(at=7, text='機種・設定・アプリの動作の確認が必要')]))])
 ],
 desc=dict(title_main='GPS衛星は、あなたの居場所を知っているのか', title_no=1,
  titles=['GPS衛星は、あなたの居場所を知っている？ GPS.govの説明で確かめる', 'GPSは衛星が居場所を追跡している？ 仕組みを公式サイトで確かめる', 'スマホの位置情報はGPS衛星に知られる？ 灯台にたとえて確かめる'],
  intro='スマホの地図は、あなたの居場所を表示します。では、空の上のGPS衛星は、あなたの居場所を知っているのでしょうか。この動画では、アメリカ政府のGPS公式サイト(GPS.gov)などの説明から、GPSの仕組みを確かめます。衛星は何を送っているのか、端末は何をするのか、衛星は追跡しているのか、居場所が外に出るのはどんなときか、を分けて見ていきます。分かることと決められないことを分けて、各資料に帰属して述べます。',
  points=['GPS.govによると、GPS衛星は、自分の位置、状態、正確な時刻(搭載した原子時計による)を電波で送っています。衛星は約20,200kmの上空を回り、運用はアメリカ宇宙軍です(GPS.gov「How GPS Works」「GPS and Telling Time」、衛星の説明)。', '端末は、電波が届いた時刻を記録し、時間に光の速さをかけて衛星までのおおよその距離を出します。端末の時計にはずれがあるため、東西・南北・高さに加えて時計のずれも求める必要があり、通常は4基以上の衛星の電波を使います。この計算は端末の中で行われます(GPS.gov、米国沿岸警備隊の技術資料)。', 'GPS.govのFAQは、GPS衛星そのものは地上のものを追跡しておらず、灯台のように一方向の基準信号を送るだけで、GPSを運用する政府は端末の位置を特定できない、と説明しています。', 'MIT School of Engineeringの解説によると、GPSの計算そのものが居場所を外へ知らせるわけではありませんが、通信機能を持つ機器やサービスが、位置情報を外へ送る場合があります。位置の履歴を記録することと、外へ送ることは別です。'],
  refs=['GPS.gov「How GPS Works」:http://archive.gps.gov/multimedia/poster/poster.txt', 'GPS.gov「GPS and Telling Time」:https://www.gps.gov/gps-and-telling-time', 'GPS.gov 衛星の説明(Space Segment):https://archive.gps.gov/systems/gps/space/', 'GPS.gov「FAQ」:https://www.gps.gov/faq', 'GPS.gov「GPS Location Privacy」:https://archive.gps.gov/policy/privacy/', '米国沿岸警備隊(Navcen)「NAVSTAR GPS User Equipment Introduction」(1996):https://navcen.uscg.gov/sites/default/files/pubs/gps/gpsuser/gpsuser.pdf', '米国沿岸警備隊(Navcen)「GPS SPS Signal Specification」:https://navcen.uscg.gov/sites/default/files/pdf/gps/sigspec/gpssps1.pdf', 'MIT School of Engineering「Ask an Engineer」:https://engineering.mit.edu/ask-an-engineer/could-a-gps-device-reveal-my-location-to-others'],
  credit_lines=['・図:自作(GPS.govなどの説明をもとにした模式図です。実際の衛星の位置・数ではありません)', '・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実際の衛星・機器の再現ではありません)'],
  notes=['衛星の数は、GPS.gov内でも資料によって食い違う(同じ日付で31基と25基)ため、この動画では扱っていません。', '「4つを求めるため」の説明は、GPS.govと米国沿岸警備隊の技術資料の説明に基づきます。実際の測位の精度は、衛星の配置・遮蔽物・電波の反射・大気などで変わります。', 'あなたのスマホのどのアプリが位置情報をどこへ送っているかは、この動画では確認していません。'],
  tags='GPS, GPS衛星, 位置情報, スマホ, 仕組み, 原子時計, GPS.gov, プライバシー, 雑学, 検証',
  checks=['GPS.govのFAQ・位置情報のプライバシーのページの原文を、公開前にもう一度開いて確認する(`docs/themes/20261114_gps/08_fact_check.md`)', '米国沿岸警備隊(Navcen)の資料(1996年のNAVSTAR GPS User Equipment Introduction)の該当箇所を、公開前にもう一度確認する']),
 thumb=dict(bg='assets/gps/thumb_art.png', lines=[['GPS衛星は', 100, 'white'], ['居場所を', 100, 'white'], ['知っている？', 110, 'gold']], sub='GPS.govの説明で確かめる', shade_col=[4, 14, 40], accent=[130, 200, 255], bar_col=[130, 200, 255], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and not o.get('title') and o['box'][3] - o['box'][1] <= 70: o['size'] = min(o.get('size', 40), 40)
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
inject(spec, dict(intro='sky', sat='orbit', track='lighthouse', out='phone', end='finale'))
(R / 'data' / 'gps_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
