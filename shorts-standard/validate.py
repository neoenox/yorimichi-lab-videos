"""Usage: python validate.py result.json; requires jsonschema (pip install jsonschema)."""
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
if data.get('needs_research') and data.get('status') == 'ready': errors.append('Research incomplete: status must be needs_review')
if errors:
    print('FAIL\n'+'\n'.join(errors)); sys.exit(1)
print('PASS: structural checks only. Human fact/audio/visual review still required.')
