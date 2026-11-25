"""誤って予約解除したShortのうち、nolong=true（長尺と無関係）のものを洗い出す。
復元は別途判断。まず対象を表示する。"""
import glob
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
rows = []
for f in sorted((R / 'data').glob('short_*.json')):
    d = json.loads(f.read_text(encoding='utf8'))
    if not isinstance(d, dict):
        continue
    if not d.get('long_id'):
        continue
    if d.get('nolong') is True:
        rows.append((f.stem[6:], d['long_id']))
print('nolong=true かつ long_id あり:', len(rows))
for r in rows:
    print(*r, sep=' | ')
