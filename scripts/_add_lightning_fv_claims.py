import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
p = R / 'data' / 'short_lightning_fv.json'
d = json.loads(p.read_text(encoding='utf8'))
U = 'https://www.weather.gov/safety/lightning-myths'

d['claims'] = [
    {
        'id': 'c1',
        'statement': '米国立気象局は「雷は同じ場所に二度落ちない」を俗説としている',
        'source_type': 'primary',
        'source_url': U,
        'evidence_note': 'docs/themes/20261123_lightning/08_fact_check.md に原文を記録。2026-10-23に原文取得済み。',
    },
    {
        'id': 'c2',
        'statement': '雷は特に高く・とがった・孤立したものに繰り返し落ちることがよくある',
        'source_type': 'primary',
        'source_url': U,
        'evidence_note': '原文 Lightning often strikes the same place repeatedly, especially if it is a tall, pointy, isolated object. を確認。',
    },
    {
        'id': 'c3',
        'statement': 'エンパイア・ステート・ビルには平均で年に23回雷が落ちる',
        'source_type': 'primary',
        'source_url': U,
        'evidence_note': '原文 The Empire State Building is hit an average of 23 times a year を確認。二次記事の25回・100回は使っていない。',
    },
    {
        'id': 'c4',
        'statement': '雷の音が聞こえたら頑丈な建物か屋根が硬い車へ避難し、木の下は避ける',
        'source_type': 'primary',
        'source_url': U,
        'evidence_note': '原文 Run to a substantial building or hard topped vehicle. と Being underneath a tree is the second leading cause of lightning casualties. を確認。',
    },
]
d['needs_research'] = [
    '詳しい物理の仕組みは動画で扱わず、説明欄にもその旨を書いている。答えは「俗説かどうか」と「落ちやすい条件」までで、物理の仕組みは結論に使っていない。答えは変わらない。',
    '気象庁の日本語の雷の安全解説は本次で原文確認できていない。動画と説明欄はNWSの記述に限定して帰属を明示しているため、答えは変わらない。',
]
for scene, claim in zip(d['scenes'], [['c1'], ['c1'], ['c2'], ['c3'], ['c4'], None]):
    if claim is not None:
        scene['claim_ids'] = claim

d['title'] = '雷は、同じ場所に二度落ちない？ AI映像版'
for scene in d['scenes']:
    scene.pop('art', None)
p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf8')
print('claims added, art removed')
