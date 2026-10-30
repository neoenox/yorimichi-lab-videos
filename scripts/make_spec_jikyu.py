"""Writes data/jikyu_spec.json（日本の食料自給率37％なら、食べ物の63％は輸入？）。台本：docs/themes/20270130_jikyu/09_script_v2.md
at / until は『章内の行番号（0始まり）』。末尾で文の番号に直す。イラスト（specart.inject）は、画像ができてから足す。"""
import json, sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
R = Path(__file__).resolve().parents[1]
from specart import inject
TOP = [60, 170, 1860, 235]
spec = dict(slug='jikyu', theme_dir='20270130_jikyu', pack='42_jikyu', header_sub='農林水産省の資料で、「37％」の中身を確かめる',
 images={},
 bgm=[['intro', 'feed', 'piano36'], ['rest', 'scale', 'piano12'], ['eaten', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='食料自給率37％なら、63％は輸入？', chapter_title='導入：食料自給率37％なら、63％は輸入？', opener='食料自給率37％なら、63％は輸入？', opener_until=1, scene=[
   dict(t='big', text='食料自給率は、37％', y=270, at=0, size=62, col='gold'),
   dict(t='panel', box=[120, 450, 1800, 570], text='では、食べ物の63％は、輸入？', at=1, size=46, hi=True),
   dict(t='panel', box=[120, 620, 1800, 700], text='確かめる材料：農林水産省の資料（令和7年度・概算）', at=2, size=38),
   dict(t='panel', box=[120, 750, 1800, 830], text='農水省も「国産37・輸入63」と示す。ただし、63の中身はひとつではない', at=3, size=34, col='gold')]),
 dict(key='base', title='37％は、何の割合か', chapter_title='37％は、何の割合か', scene=[
   dict(t='panel', box=TOP, text='令和7年度の食料自給率：37％（概算）', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='カロリーベース：国産の熱量 ÷ 供給された熱量の全体', at=1, until=2, size=38),
   dict(t='panel', box=TOP, text='1人1日あたり：国産 830kcal ÷ 全体 2,237kcal', at=2, until=3, size=38, col='gold'),
   dict(t='panel', box=TOP, text='830 ÷ 2,237 ＝ 約37％。使うのは、重さではなく熱量', at=3, until=4, size=38),
   dict(t='panel', box=TOP, text='品目別の例：小麦は、国内生産 約103万トン ÷ 消費 約659万トン ＝ 約16％', at=4, size=32, hi=True),
   dict(t='bars', box=[60, 300, 1860, 540], title='小麦（重量ベース。熱量ではなく、重さで比べる）', unit='万トン', max=700, lab_w=520, data=[dict(at=4, label='国内で作られた量', value=103, vlabel='約103万トン', col='blue'), dict(at=4, label='国内で消費に向けられた量', value=659, vlabel='約659万トン', col='gold')]),
   dict(t='bars', box=[60, 300, 1860, 540], title='1人1日あたりの供給熱量（令和7年度・概算）', unit='kcal', max=2500, lab_w=420, data=[dict(at=2, label='国産', value=830, vlabel='830kcal', col='blue', until=4), dict(at=2, label='供給された全体', value=2237, vlabel='2,237kcal', col='gold', until=4)])]),
 dict(key='feed', title='「国産」に入らないもの', chapter_title='「国産」に入らないもの', scene=[
   dict(t='panel', box=TOP, text='決まり：輸入飼料で国内で育てた畜産物は、国産に入れない', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='日本で育てた牛や鶏でも、えさが輸入なら、その分は国産に数えない', at=1, until=2, size=36),
   dict(t='panel', box=TOP, text='家畜のえさの自給率：約24％', at=2, until=3, size=40),
   dict(t='panel', box=TOP, text='えさの産地を問わない指標：「食料国産率」', at=3, until=4, size=40, col='gold'),
   dict(t='panel', box=TOP, text='卵：自給率11％、ところが国産率は97％', at=4, until=5, size=40, hi=True),
   dict(t='panel', box=TOP, text='国内でほとんど作られていても、えさが輸入なら、国産に数えない', at=5, until=6, size=36),
   dict(t='panel', box=TOP, text='ほかの例：牛肉、豚肉、鶏肉も、自給率と国産率が大きく違う', at=6, size=36),
   dict(t='table', box=[60, 300, 1860, 760], cols=['品目（カロリーベース）', '自給率', '国産率（えさの産地を問わない）'], colw=[760, 420, 620], size=38, rows=[
     dict(at=4, cells=['卵', '11％', '97％'], col='gold'),
     dict(at=6, cells=['牛肉', '13％', '50％']),
     dict(at=6, cells=['豚肉', '5％', '49％']),
     dict(at=6, cells=['鶏肉', '7％', '65％'])])]),
 dict(key='rest', title='「残り63％」の中身', chapter_title='「残り63％」の中身', scene=[
   dict(t='panel', box=TOP, text='残りの63％には、何が入っているのか', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='農水省：輸入飼料による畜産物の分は、輸入の熱量として数える', at=1, until=2, size=36),
   dict(t='panel', box=TOP, text='食料全体の国産率46％：国産の熱量は 1,040kcal（自給率は 830kcal）', at=2, until=3, size=34),
   dict(t='panel', box=TOP, text='差の210kcal ＝ 輸入飼料で国内で育てた畜産物の分。全体の約9％', at=3, until=4, size=36, col='gold'),
   dict(t='panel', box=TOP, text='2,237 − 1,040 ＝ 約1,197kcal：国内で作られていない、輸入の食料（約54％）', at=4, until=5, size=32),
   dict(t='panel', box=TOP, text='63％ ＝ 輸入の食料 約54％ ＋ 輸入飼料の畜産物 約9％', at=5, until=6, size=38, hi=True),
   dict(t='panel', box=TOP, text='「63％は輸入」は表示のとおり。ただし、全体の約9％は国内で育てた家畜の分', at=6, size=34, col='gold'),
   dict(t='bars', box=[60, 300, 1860, 590], title='供給熱量2,237kcalの内訳（令和7年度・概算。9％と54％は自作の計算）', unit='％', max=60, lab_w=600, data=[dict(at=2, label='国産（自給率）', value=37, vlabel='37％', col='blue'), dict(at=3, label='輸入飼料の畜産物', value=9, vlabel='約9％', col='org'), dict(at=4, label='輸入の食料', value=54, vlabel='約54％', col='gold')])]),
 dict(key='where', title='輸入は、どこから来ているか', chapter_title='輸入は、どこから来ているか', scene=[
   dict(t='panel', box=TOP, text='農水省の試算：供給熱量の国別の構成（令和7年度）', at=0, until=1, size=38, hi=True),
   dict(t='panel', box=TOP, text='国産・米国・カナダ・豪州の4つで、84％', at=1, until=2, size=40),
   dict(t='panel', box=TOP, text='米国の26％の内訳（グラフの表示）：とうもろこし13％、小麦5％、大豆4％', at=2, until=3, size=32),
   dict(t='panel', box=TOP, text='国別の輸入量をもとにした試算。実際の数字そのものではない', at=3, size=36, col='gold'),
   dict(t='bars', box=[60, 300, 1860, 690], title='供給熱量の国別構成（試算・令和7年度）', unit='％', max=40, lab_w=420, data=[dict(at=0, label='国産', value=37, vlabel='37％', col='blue', until=2), dict(at=0, label='米国', value=26, vlabel='26％', col='gold', until=2), dict(at=0, label='カナダ', value=11, vlabel='11％', col='gold', until=2), dict(at=0, label='豪州', value=10, vlabel='10％', col='gold', until=2), dict(at=1, label='その他の国', value=16, vlabel='約16％', col='dim', until=2)]),
   dict(t='bars', box=[60, 300, 1860, 640], title='米国の26％の内訳（元資料のグラフの表示。供給熱量全体に対する割合）', unit='％', max=30, lab_w=420, data=[dict(at=2, label='とうもろこし', value=13, vlabel='13％', col='gold'), dict(at=2, label='小麦', value=5, vlabel='5％', col='gold'), dict(at=2, label='大豆', value=4, vlabel='4％', col='gold'), dict(at=2, label='その他', value=4, vlabel='4％', col='dim')])]),
 dict(key='scale', title='ものさしを変えると', chapter_title='ものさしを変えると', scene=[
   dict(t='panel', box=TOP, text='自給率は、ものさしで数字が変わる', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='生産額ベース：国内生産額 14.5兆円 ÷ 国内消費額 21.8兆円 ＝ 約66％', at=1, until=2, size=34),
   dict(t='panel', box=TOP, text='同じ年度でも、カロリーでは37％、金額では66％', at=2, until=3, size=40, col='gold'),
   dict(t='panel', box=TOP, text='金額で見た品目別の自給率：米99％、野菜87％、魚介類42％、小麦16％', at=3, until=4, size=34),
   dict(t='panel', box=TOP, text='米と野菜は、消費額の約3割。国産の割合が高いので、金額では高く出る', at=4, until=5, size=34, hi=True),
   dict(t='panel', box=TOP, text='どれが正しい、ではなく、何を測るかの違い', at=5, size=40),
   dict(t='bars', box=[60, 300, 1860, 540], title='令和7年度・食料自給率（概算）', unit='％', max=100, lab_w=480, data=[dict(at=2, label='カロリーベース', value=37, vlabel='37％', col='blue', until=3), dict(at=2, label='生産額ベース', value=66, vlabel='66％', col='gold', until=3)]),
   dict(t='bars', box=[60, 300, 1860, 640], title='生産額ベースの品目別自給率（令和7年度）', unit='％', max=100, lab_w=380, data=[dict(at=3, label='米', value=99, vlabel='99％', col='gold'), dict(at=3, label='野菜', value=87, vlabel='87％', col='gold'), dict(at=3, label='魚介類', value=42, vlabel='42％', col='blue'), dict(at=3, label='小麦', value=16, vlabel='16％', col='blue')])]),
 dict(key='eaten', title='「食べた量」ではない。最近の動き', chapter_title='「食べた量」ではない。最近の動き', scene=[
   dict(t='panel', box=TOP, text='この数字は、実際に食べた量の割合ではない', at=0, until=1, size=40, hi=True),
   dict(t='panel', box=TOP, text='食料需給表の食料には、売れ残りや、賞味期限切れの廃棄などが含まれる', at=1, until=2, size=34),
   dict(t='panel', box=TOP, text='分母は「口に入った量」ではなく「供給された量」', at=2, until=3, size=40, col='gold'),
   dict(t='panel', box=TOP, text='令和6年度38％ → 令和7年度37％（−1ポイント）', at=3, until=4, size=40),
   dict(t='panel', box=TOP, text='主因：国産の供給熱量の減少。米の消費減と、民間在庫の増加も', at=4, until=5, size=36),
   dict(t='panel', box=TOP, text='生産額ベースは、64％ → 66％。米・畜産物の国内価格の上昇で', at=5, until=6, size=36, hi=True),
   dict(t='panel', box=TOP, text='2000年代に入ってから、おおむね横ばい。令和7年度は概算で、確定すると変わることがある', at=6, size=30)]),
 dict(key='end', title='まとめ', chapter_title='まとめ', scene=[
   dict(t='cols2', size=32, xm=940, xm2=980, left=dict(title='分かること', title_at=0, items=[
      dict(at=0, text='37％は、カロリーで見た、国産の割合'),
      dict(at=1, text='輸入飼料で育てた畜産物は、国産に入れない（卵は自給率11％）'),
      dict(at=2, text='農水省は、国産37・輸入63と示している'),
      dict(at=3, text='63％の内訳（全体に対して）：輸入の食料 約54％、輸入飼料の畜産物 約9％（自作の計算）')]),
     right=dict(title='言い方の注意', title_at=4, items=[
      dict(at=4, text='金額で見ると66％。ものさしで数字は変わる'),
      dict(at=5, text='「63％は輸入」はそのとおり。ただし全体の約9％は国内で育てた家畜の分')]))]),
 ],
 desc=dict(title_main='日本の食料自給率37％なら、食べ物の63％は輸入か', title_no=1,
  titles=['日本の食料自給率37％なら、食べ物の63％は輸入？ 農林水産省の資料で確かめる', '食料自給率37％の中身：63％の内訳は、輸入の食料と、国内で育てた家畜の分', '卵の自給率は11％、国産率は97％：食料自給率の「国産」とは'],
  intro='「日本の食料自給率は37％。食べ物の63％は輸入」と聞いたことはないでしょうか。この動画では、農林水産省の令和7年度の資料(概算)で、37％が何の割合なのか、残りの63％に何が入っているのかを確かめます。',
  points=['食料自給率37％は、カロリーベースの数字です。1人1日あたり、国産830kcal÷供給熱量2,237kcalです。', '輸入した飼料で国内で育てた畜産物は、自給率では国産に数えません。卵は、自給率11％、国産率97％です。', '農林水産省は、供給熱量を「国産37％・輸入63％」と示しています。', '国産率(1,040kcal)と自給率(830kcal)の差210kcalは、輸入飼料の畜産物の分で、全体の約9％です(自作の計算)。国内で作られていない輸入の食料は、約54％です(自作の計算)。', '生産額ベースでは66％です。ものさしで数字が変わります。'],
  refs=['農林水産省「令和7年度食料自給率について」(令和8年8月7日公表、概算):https://www.maff.go.jp/j/press/kanbo/anpo/260807.html', '農林水産省「令和7年度食料自給率」参考資料(令和8年8月18日差し替え版):https://www.maff.go.jp/j/press/kanbo/anpo/attach/pdf/260807-3.pdf', '農林水産省「食料自給率の考え方」:https://www.maff.go.jp/j/zyukyu/zikyu_ritu/011.html', '農林水産省「食料自給率Q&A」:https://www.maff.go.jp/j/zyukyu/faq/index.html', '農林水産省「食料自給率の推移」:https://www.maff.go.jp/j/zyukyu/zikyu_ritu/012.html'],
  credit_lines=['・サムネイルの背景と場面のイラスト:ChatGPT(OpenAI)による生成イラスト(イメージです。実在の場面・人物・資料の再現ではありません)'],
  notes=['令和7年度の数字は概算です。確定すると変わることがあります。', '輸入の食料(約54％)と輸入飼料の畜産物(約9％)は、農林水産省の公表値(国産率1,040kcal、自給率830kcal、供給熱量2,237kcal)からの自作の計算です。', '国別の輸入(米国26％など)は、農林水産省の試算です。米国の内訳は、グラフの表示を読んだものです。', '食料需給表の本表は、この動画では確認していません。', '「2000年代に入ってからは、おおむね横ばい」は、農林水産省が食料自給率全体について述べた文です。動画ではカロリーベースの話の中で紹介していますが、カロリーベースに限った記述かどうかは、確認できていません。'],
  tags='食料自給率, 農林水産省, カロリーベース, 食料国産率, 輸入, 検証, 農業, 食料安全保障',
  checks=['令和7年度食料需給表の本表で、国産供給熱量・供給熱量の内訳を確認する', '食料国産率と自給率の差(210kcal)が輸入飼料分であることを、農林水産省の説明で確認する', '参考資料p.13(国別構成)の米国の内訳を、数値表で確認する', '令和7年度が確定したときの値を確認する', '「2000年代は横ばい」が、どの指標についての記述かを、グラフと表（EXCEL）で確認する']),
 thumb=dict(bg='assets/jikyu/thumb_art.png', lines=[['自給率37％', 110, 'white'], ['残り63％は', 100, 'white'], ['全部輸入？', 120, 'gold']], sub='農林水産省の資料で確かめる', shade_col=[10, 24, 44], accent=[255, 178, 72], bar_col=[255, 178, 72], y0=14, bar_y=520, bar_w=620, sub_size=44, shade_x=700, shade_w=520))


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
    t = (R / 'docs' / 'themes' / '20270130_jikyu' / '09_script_v2.md').read_text(encoding='utf8')
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
_ART = {'intro': 'intro', 'base': 'desk', 'feed': 'farm', 'rest': 'ship', 'where': 'harbor', 'scale': 'market', 'eaten': 'kitchen', 'end': 'intro'}
if all((R / 'assets' / 'jikyu' / f'art_{v}.png').exists() for v in set(_ART.values())):
    inject(spec, _ART)
(R / 'data' / 'jikyu_spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8'); print('spec written')
