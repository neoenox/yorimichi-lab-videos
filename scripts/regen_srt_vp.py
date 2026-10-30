"""audio_report から SRT を作り直す（vp.py stage_audio と同じ式。焼き込み字幕と完全に一致させる）。
usage: python scripts/regen_srt_vp.py oke [--write]
"""
import json, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))
from hn_text import display
from vp import split_clauses


def st(t):
    ms = round(t * 1000)
    return f'{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}'


slug = sys.argv[1]
rep = json.loads((R / 'out' / f'{slug}_audio_report.json').read_text(encoding='utf8'))
cues = []
for x in rep['segments']:
    ch = split_clauses(display(x['text']))
    tot = sum(len(c) for c in ch)
    cum = 0
    for c in ch:
        cues.append((x['start'] + (x['end'] - x['start']) * cum / tot,
                     x['start'] + (x['end'] - x['start']) * (cum + len(c)) / tot, c))
        cum += len(c)

text = '\n\n'.join(f'{i + 1}\n{st(a)} --> {st(b)}\n{c}' for i, (a, b, c) in enumerate(cues)) + '\n'
p = R / 'out' / f'{slug}_subtitles.srt'
old = p.read_text(encoding='utf8')
print(f'{slug}: segment-based cues={len(cues)}, file cues={old.strip().count(chr(10) + chr(10)) + 1}, identical={old == text}')
if '--write' in sys.argv:
    p.write_text(text, encoding='utf8')
    print('written', p.name)
