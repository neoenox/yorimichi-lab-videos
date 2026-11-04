"""Usage: python validate.py result.json; requires jsonschema (pip install jsonschema).

v1.1（このリポジトリ）: claims.source_type を追加。
  primary      … source_url（一次資料）が必須。http(s) であること
  ai_assistant … AI アシスタントの回答を根拠にしてよい。source_url は任意（質問・回答の要点を evidence_note に残す）
"""
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

p = Path(__file__).resolve().parent
if len(sys.argv) != 2:
    raise SystemExit('Usage: python validate.py result.json')
data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
schema = json.loads((p / 'output.schema.json').read_text(encoding='utf-8'))
errors = [str(e) for e in Draft202012Validator(schema).iter_errors(data)]
scenes = data.get('scenes', [])
if scenes:
    if abs(scenes[0]['start']) > 0.01: errors.append('First scene must start at 0')
    if abs(scenes[-1]['end'] - data['duration_sec']) > 0.01: errors.append('Last scene must end at duration_sec')
    for i, s in enumerate(scenes):
        length = s['end'] - s['start']
        if not 3 <= length <= 9: errors.append(f'Scene {i+1}: duration must be 3-9s')
        if i and abs(scenes[i-1]['end'] - s['start']) > 0.01: errors.append(f'Scene {i+1}: gap/overlap')
claim_ids = {c['id'] for c in data.get('claims', [])}
for i,s in enumerate(scenes):
    for cid in s.get('claim_ids', []):
        if cid not in claim_ids: errors.append(f'Scene {i+1}: unknown claim ID {cid}')
for c in data.get('claims', []):
    kind = c.get('source_type', 'primary')
    url = str(c.get('source_url') or '')
    if kind == 'primary':
        if not url:
            errors.append(f"claim {c.get('id')}: source_type=primary には source_url が必要")
        elif not (url.startswith('http://') or url.startswith('https://')):
            errors.append(f"claim {c.get('id')}: source_url は http(s) で指定する")
    elif kind == 'ai_assistant':
        if not str(c.get('evidence_note') or '').strip():
            errors.append(f"claim {c.get('id')}: ai_assistant は evidence_note に質問と回答の要点を書く")
if data.get('needs_research') and data.get('status') == 'ready': errors.append('Research incomplete: status must be needs_review')
if errors:
    print('FAIL\n'+'\n'.join(errors)); sys.exit(1)
print('PASS: structural checks only. Human fact/audio/visual review still required.')
