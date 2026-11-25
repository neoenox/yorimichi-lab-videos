import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
p = R / 'data' / 'short_solo_white_breath.json'
d = json.loads(p.read_text(encoding='utf8'))

JMA = 'https://www.jma.go.jp/jma/kids/kids/faq/a2_01.html'
TOYOKAWA = ('https://warp.ndl.go.jp/info:ndljp/pid/10299136/'
            'www.city.toyokawa.lg.jp/shisetsu/sonota/seisokojo/hakuen.html')
JST = 'https://koushien.jst.go.jp/koushien/pastexam/2016/files/1-1.pdf'

d['claims'] = [
    {
        'id': 'c1',
        'statement': '冬の寒い日に人間がはく息が白く見えるのは、水蒸気が小さな水滴になる現象で、ひこうき雲と同じ仕組みである',
        'source_type': 'primary',
        'source_url': JMA,
        'evidence_note': '気象庁「はれるんランド」に「冬の寒い日に人間がはく息が白く見えるのと同じこと」と明記。2026年11月25日に web_fetch で本文を確認。',
    },
    {
        'id': 'c2',
        'statement': '息が白く見えるかどうかは温度だけでなく湿度にも関係し、湿度の高い雨天時には特に目立つ',
        'source_type': 'primary',
        'source_url': JMA,
        'evidence_note': '気象庁「はれるんランド」に「上空の温度や湿度、ジェット機のはい気ガスの温度などにより、ひこうき雲ができるときとできないときがあります」と明記。湿度の高い雨天時に目立つ旨は豊川市の資料（c3）の記述。',
    },
    {
        'id': 'c3',
        'statement': '水蒸気が冷えて水滴になる結露は、気温が低い冬場、特に湿度の高い雨天時に目立ち、吐く息が白くなるのとほぼ同じである',
        'source_type': 'primary',
        'source_url': TOYOKAWA,
        'evidence_note': '豊川市清掃工場の白煙の説明に「吐く息が白くなる寒い季節とほぼ同じ」「特に湿度の高い雨天時に目立つ」と明記。2026年11月25日に web_fetch で本文を確認。',
    },
    {
        'id': 'c4',
        'statement': '水蒸気が白く見えるかどうかは温度だけでなく、空気に含まれる水蒸気の量（混合）にも関係する',
        'source_type': 'primary',
        'source_url': JST,
        'evidence_note': 'JST「高校生のための科学」2016年度問題で、やかんの湯気について「温度だけを考えましたけれども…空気とその中に含まれる水蒸気も混ざる」と解説。',
    },
]
d['needs_research'] = [
    '息が白くなる目安とされる「気温13℃以下」は JAL の天気情報の記述で、気象庁の値ではない。台本ではこの数字を使っていない。答えは変わらない。',
]
for scene, claim in zip(d['scenes'], [['c1', 'c2'], ['c1', 'c4'], ['c1'], ['c2', 'c3'], None]):
    if claim is not None:
        scene['claim_ids'] = claim

p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf8')
print('claims added')
