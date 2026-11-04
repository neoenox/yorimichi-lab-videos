"""字幕・画面の修正を反映して作り直す（音声は変えない）。srt再生成 → story → build → upload/<pack>/ の video.mp4 と subtitles_ja.srt を入れ替え。
usage: python scripts/rebuild_all.py slug...   ログ：out/rebuild_all.log（最後に ALL_DONE）。VP_MAXPAR で並列数。"""
import json, shutil, subprocess, sys, time
from pathlib import Path
R = Path(__file__).resolve().parents[1]; PY = sys.executable; LOG = R / 'out' / 'rebuild_all.log'
def log(m):
    l = time.strftime('%H:%M:%S ') + m
    with LOG.open('a', encoding='utf-8') as f: f.write(l + '\n')
def run(a): return subprocess.run([PY, *a], cwd=R, capture_output=True, text=True, encoding='utf-8', errors='replace')
def probe(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True); return float(r.stdout.strip() or 0)
ok = []
for s in sys.argv[1:]:
    t0 = time.time()
    try:
        pack = json.loads((R / 'data' / f'{s}_spec.json').read_text(encoding='utf8'))['pack']
        for step in (['scripts/regen_srt.py', s], ['scripts/vp.py', s, 'story']):
            r = run(step)
            if r.returncode: raise RuntimeError(f'{step[0]} {r.stderr[-200:]}')
        r = run(['scripts/vp.py', s, 'build']); vid = R / 'out' / f'{s}_video.mp4'
        if r.returncode or 'QA' not in r.stdout: raise RuntimeError('build ' + (r.stderr or r.stdout)[-300:])
        d = R / 'upload' / pack
        if d.exists():
            if abs(probe(vid) - probe(d / 'video.mp4')) > 2: raise RuntimeError('長さが違う')
            shutil.copyfile(vid, d / 'video.mp4'); shutil.copyfile(R / 'out' / f'{s}_subtitles.srt', d / 'subtitles_ja.srt')
        log(f'{s}: OK ({(time.time()-t0)/60:.1f}分)'); ok.append(s)
    except Exception as e: log(f'{s}: 失敗 {e}')
log(f'完了 {len(ok)}/{len(sys.argv)-1}'); log('ALL_DONE')
