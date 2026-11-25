import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
p = R / 'data' / 'short_solo_postbox.json'
d = json.loads(p.read_text(encoding='utf8'))
U = 'https://www.postalmuseum.jp/column/transition/post_10.html'

d['claims'] = [
    {
        'id': 'c1',
        'statement': '日本最初のポストは1871年の木製「書状集箱」で、東京12・京都5・大阪8・東海道の宿場62か所に設置された',
        'source_type': 'primary',
        'source_url': U,
        'evidence_note': '郵政博物館「郵便ポストの移り変わり」（2014年3月12日掲載）の「（1）初めてのポスト」節に、明治4(1871)年、書状集め箱、東京12カ所・京都5カ所・大阪8カ所・東海道の宿場62カ所と明記。2026年11月18日と11月25日の2回、本文を確認。',
    },
    {
        'id': 'c2',
        'statement': '1872年に杉板と鉄板で作られた黒い柱型ポストが登場し、高さは123cmだった',
        'source_type': 'primary',
        'source_url': U,
        'evidence_note': '同ページ「（2）ポストの発達」の黒ポストの写真説明に「明治5（1872）年 幅24.2cm 奥行24.2cm 高さ123cm」とあり、本文にも杉板を四角い柱のように組み合わせかどに鉄板を張って黒いペンキを塗ったとの記述。2026年11月25日に本文を再確認。',
    },
    {
        'id': 'c3',
        'statement': '1901年に火事に強い鉄製の赤色丸型ポストが考案され、赤は位置をわかりやすくするためだった',
        'source_type': 'primary',
        'source_url': U,
        'evidence_note': '同ページ本文に「明治34(1901)年に火事に強い鉄製の赤色丸型ポストが考案される」と「赤色に塗ったのはポストの位置をわかりやすくするため」と明記。俵谷式・中村式が1901年に試験設置されたとの記載もある。2026年11月25日確認。',
    },
    {
        'id': 'c4',
        'statement': '1908年10月に鉄製赤色ポストが正式に制定され、2026年11月18日時点の情報である',
        'source_type': 'primary',
        'source_url': U,
        'evidence_note': '同ページ「回転式ポスト」の節に「明治41(1908)年10月に正式に鉄製赤色のポストが制定されました」と明記。確認日は2026年11月18日・11月25日。',
    },
]
d['needs_research'] = [
    '郵政博物館のページは2014年3月12日掲載で、その後のポストの増減までは扱っていない。動画は「最初から赤かったか」という歴史の問いに答えるもので、現在のポストの設置数は結論に使っていない。答えは変わらない。',
]
for scene, claim in zip(d['scenes'], [['c1', 'c3'], ['c1'], ['c2'], ['c3', 'c4'], None]):
    if claim is not None:
        scene['claim_ids'] = claim

p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf8')
print('claims added')
