import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
U = 'https://www.bipm.org/en/history-si/metre'
CLAIMS = [
    {
        'id': 'c1',
        'statement': '1889年に第1回CGPMが白金とイリジウムの国際原器を認定した',
        'source_type': 'primary',
        'source_url': U,
        'evidence_note': 'BIPM「metre」本文に The original international prototype of the metre, which was sanctioned by the 1st CGPM in 1889 と明記。2026年11月25日にbskで本文を直接確認。',
    },
    {
        'id': 'c2',
        'statement': '1960年に第11回CGPMがクリプトン86の遷移の波長による定義に置き換えた',
        'source_type': 'primary',
        'source_url': U,
        'evidence_note': 'BIPM本文に 11th CGPM (1960) using a definition based on the wavelength of the radiation corresponding to a particular transition in krypton 86 と明記。精度向上のため干渉計でフリンジを数えて実現する旨も本文にある。2026年11月25日確認。',
    },
    {
        'id': 'c3',
        'statement': '1983年に第17回CGPM決議1が真空中の光の距離による定義に置き換えた',
        'source_type': 'primary',
        'source_url': U,
        'evidence_note': 'BIPM本文に replaced in 1983 by the 17th CGPM (Resolution 1) with a definition referenced to the distance that light travels in vacuum in a specified interval of time と明記。2026年11月25日確認。',
    },
]
NEEDS = [
    '1799年のダンケルク〜バルセロナの測量は Wikipedia「History of the metre」で確認した二次資料で、BIPM 本文には無い。一次史料照合は未実施。1889年の国際原器は BIPM 本文で確認できており、答えは変わらない。',
    '現在のメートルが当初の定義より約0.197ミリ短いという数値も Wikipedia 二次資料のみで一次史料照合は未実施。台本では「とされます」と留保しており、基準が替わった理由の説明には使っていない。答えは変わらない。',
]

for name in ('meter_light', 'meter_before'):
    p = R / 'data' / f'short_solo_{name}.json'
    d = json.loads(p.read_text(encoding='utf8'))
    d['claims'] = CLAIMS
    d['needs_research'] = NEEDS
    scenes = d['scenes']
    if name == 'meter_light':
        ids = [['c1', 'c2', 'c3'], ['c1'], ['c2', 'c3'], ['c2', 'c3'], None]
    else:
        ids = [['c1', 'c2', 'c3'], ['c1'], ['c2', 'c3'], ['c2', 'c3'], None]
    for scene, claim in zip(scenes, ids):
        if claim is not None:
            scene['claim_ids'] = claim
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf8')
    print(name, 'updated')
