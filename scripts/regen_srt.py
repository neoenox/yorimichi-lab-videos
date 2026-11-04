"""音声はそのまま、字幕（srt）だけを作り直す（読点を減らした表示に）。VOICEVOX不要。usage: python scripts/regen_srt.py slug..."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import vp
for s in sys.argv[1:]:
    vp.load_spec(s); vp.load_runtime()
    rep = json.loads(vp.P(f'out/{s}_audio_report.json').read_text(encoding='utf8'))
    st = lambda t: (lambda ms: f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}')(round(t * 1000))
    cues = []
    for x in rep['segments']:
        ch = vp.split_clauses(vp.thin(vp.display(x['text']))); tot = sum(len(c) for c in ch); cum = 0; fr = []
        for c in ch: fr.append(cum / tot); cum += len(c)
        fr.append(1.0)
        ct = x.get('cue_times'); ts = ct if ct and len(ct) == len(ch) + 1 else vp.snap_bounds(x, fr)
        for i, c in enumerate(ch): cues.append((ts[i], ts[i + 1], c))
    vp.P(f'out/{s}_subtitles.srt').write_text('\n\n'.join(f'{i+1}\n{st(a)} --> {st(b)}\n{c}' for i, (a, b, c) in enumerate(cues)) + '\n', encoding='utf8')
    print(s, len(cues), 'cues')
