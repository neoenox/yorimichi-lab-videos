"""Create the signal comparison video specification."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def background(image):
    return dict(t='anim', name='pop_bgimg', img=image, at=0, dim=.38, blur=2, zoom=.06)

def card(text, at, until=None, y=270, color='blue'):
    item = dict(at=at, text=text, col=color)
    if until is not None:
        item['until'] = until
    return dict(t='anim', name='pop_rows', items=[item], x0=160, x1=1760, y0=y, size=58, gap=12)

def title(text, at, until=None, y=510, color='yellow'):
    obj = dict(t='anim', name='pop_telop', text=text, at=at, x=960, y=y, size=88, plate=color, maxw=1500)
    if until is not None:
        obj['until'] = until
    return obj

def chapter(key, name, image, content):
    return dict(key=key, title=name, chapter_title=name, scene=[background(image)] + content)

spec = dict(slug='sigterra', theme_dir='20261104_signal', pack='sigcmp_sigterra', style='pop',
    header_sub='信号の色と名前', images={k:dict(file=f'assets/sigcmp/art_{k}.png') for k in ('intro','law','world')},
    bgm=[['intro','history','piano34'], ['language','end','acoustic48']], chapters=[
    chapter('intro','信号の青は緑色？','intro',[
        title('信号の青は緑色？',0,2), card('青信号　見た目は緑に近い',1,2, y=230),
        card('日本語の「青」の歴史から来たとされる',2,3), title('法令と言葉から確かめる',3)]),
    chapter('law','法令では何色？','law',[
        title('法令上の名前',0,1), card('道路交通法施行令',1,3), title('「青色の灯火」',1,3),
        card('緑の中でも青みの強い色とされる',3,4), title('名前は青　見た目は緑寄り',4)]),
    chapter('history','日本初の信号機','intro',[
        card('1930年　日比谷交差点とされる',0,1), title('三色の灯火',0,1),
        card('進めの合図を「青」と呼ぶ言い方が定着',1,2),
        title('英語ではグリーンライト',2,3), card('日本語だけが違う名前を付けたわけではない',3)]),
    chapter('language','言葉の「青」','intro',[
        card('昔の「青」は緑も含む広い色名と考えられる',0,1),
        title('青葉　青菜　青りんご',1,2),
        card('基本の色名は四つだったという説',2,3), title('あか　くろ　しろ　あお',2,3),
        card('信号の青も使い方を受け継いだと説明される',3)]),
    chapter('world','他の国では？','world',[
        card('青と緑の区別は一様ではない',0,1),
        card('韓国語　パランブル＝青い火とされる',1,2),
        card('ベトナム語　青と緑の両方を指す言葉があるとされる',2,3),
        title('色の名前の切り方は言語によって違う',3)]),
    chapter('end','結論','intro',[
        title('結論',0,1), card('「青」の使い方を受け継いだ名前と考えられる',1,2),
        card('法令の名前は青色　光る色は緑寄りとされる',2,3),
        title('緑に見えるのは間違いではない',3,4), title('信号待ちで思い出してみよう',4)])])

(ROOT/'data/sigterra_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding='utf8')
