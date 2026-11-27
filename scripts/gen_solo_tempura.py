"""単独Short：家康の死因は鯛の天ぷら？(solo_tempura)。nolong, nolink。
根拠は日本語版Wikipedia「徳川家康」(2026年11月8日に原文を確認)。『徳川実紀』などの原本は読めていない。
背景はFreeVideo(各場面の中身に合わせた4本：天ぷらの鍋・鷹狩の鷹・薬研・油の火)、図は自作。日付は旧暦。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
IDS = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))
slug = 'tempura'
V = lambda n: f'assets/{slug}/fv/clip{n}.mp4'
T = lambda gap, ev: dict(type='timeline', gap=gap, events=ev)
W = 'Wikipedia（徳川家康）'
pron = {'家康': 'イエヤス', '鯛': 'タイ', '鷹狩': 'タカガリ', '田中': 'タナカ', '駿府': 'スンプ', '駿府城': 'スンプジョウ', '徳川実紀': 'トクガワジッキ',
        '胃癌': 'イガン', '元和': 'ゲンナ', '榧': 'カヤ', '韮': 'ニラ', '食中毒': 'ショクチュウドク', '大奥': 'オオオク', '療養': 'リョウヨウ', '見る間に': 'ミルマニ'}
(R / 'data' / f'{slug}_pron.json').write_text(json.dumps(pron, ensure_ascii=False), encoding='utf8')
scenes = [
    dict(text='家康は、鯛の天ぷらにあたって亡くなった。有名な話ですが、天ぷらを食べてから亡くなるまで、約3か月あります。', big='家康の死因は天ぷら？', sub='元和2年（1616年）の話', src=W,
         viz=T(2.6, [('有名な話', '鯛の天ぷらで食中毒'), ('食べた日', '1月21日の夕食'), ('問い', '本当に天ぷらが原因？')])),
    dict(text='元和2年、1616年の1月21日。鷹狩に出た田中で、家康は、夕食に鯛の天ぷらを食べ、同じ日に、病に倒れた、とされます。', big='天ぷらも倒れたのも同じ日', sub='1616年1月21日（旧暦）', src=W,
         viz=T(2.6, [('1616年1月21日', '鷹狩に出た田中で'), ('同じ日', '夕食に鯛の天ぷら／病に倒れる'), ('1月25日', '駿府に戻って療養')])),
    dict(text='亡くなったのは、4月17日。食べてから、約3か月後です。食中毒にしては、日数がかかりすぎます。いま主流なのは、胃癌説です。', big='約3か月後に死去', sub='1616年4月17日（旧暦）', src=W,
         viz=dict(type='compare', l_label='天ぷら', l_val='1月21日', r_label='死去', r_val='4月17日')),
    dict(text='徳川実紀には、見る間に痩せ、腹に大きなしこりがあった、と書かれ、胃癌に多い症状とされます。江戸城の天ぷら禁止も、火事を出しかけたため、とされます。', big='胃癌説の根拠', sub='徳川実紀の記述', src=W,
         viz=T(2.6, [('徳川実紀', '痩せて、腹に大きなしこり'), ('主流の説', '胃癌'), ('天ぷら禁止', '火事を出しかけたため、とされる')])),
]
sc = []
for i, s in enumerate(scenes):
    d = dict(s, vid=V(i + 1), dim=0.7)
    d['big'] = d['big'].replace('、', ''); d['sub'] = d['sub'].replace('、', '')
    if i: d['col'] = 'white'
    sc.append(d)
sc.append(dict(text='', end=True, vid=V(1), dim=0.7))
notes = ('■ 日本語版Wikipedia「徳川家康」(2026年11月8日に原文を確認)にもとづく整理です。『徳川実紀』などの原本は読めていません。日付はすべて旧暦です。\n'
         '・元和2年(1616年)1月21日、鷹狩に出た田中で病に倒れ、25日に駿府へ帰還、療養生活に入る(同)。\n'
         '・同年4月17日巳の刻(午前10時ごろ)、駿府城で死去。75歳(満73歳4か月)(同)。\n'
         '・死因：「鯛を榧の油で揚げ、その上にすった韮をふりかけた天ぷらによる食中毒説が長く一般化されてきた。しかし、家康が鯛の天ぷらを食べたのは、1月21日の夕食で、死去したのは4月17日と日数がかかり過ぎていることから、食中毒を死因とするには無理があった。替わって主流となっているのは胃癌説である」(同)。\n'
         '・根拠：『徳川実紀』が「見る間に痩せていき、吐血と黒い便、腹にできた大きなシコリは、手で触って確認できるくらいだった」と書き留めていること、これらの症状が胃癌患者に多いこと(同)。\n'
         '・江戸城内の天ぷら禁止：死因にちなむ禁忌と説明されることもあるが、実際には大奥の侍女の一人が天ぷらを料理していて火事を出しかけたため(同)。\n'
         '・未確認：『徳川実紀』の原文。天ぷら禁止の一次史料。\n'
         '・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の風景・史実の再現ではありません。\n')
o = dict(title='家康の死因は、鯛の天ぷら？', head='家康の死因は天ぷら？', pron=f'data/{slug}_pron.json', art='assets/tohoku/bg_one.png',
         hook=scenes[0]['text'], notes=notes, answer='天ぷらから死去まで約3か月。主流は胃癌説',
         credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の風景・史実の再現ではありません\n・図・表：自作',
         suffix='整理', nolong=True, nolink=True, long_id=IDS['43_bukka']['video_id'], long_title='43_bukka', scenes=sc)
(R / 'data' / f'short_solo_{slug}.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')
print('ok')
