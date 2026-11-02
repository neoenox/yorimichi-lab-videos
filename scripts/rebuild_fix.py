"""表示不具合を直した後の再ビルド（to_pop は通さない。specはそのまま）。story → build → upload/<pack>/video.mp4 に入れ替え。
usage: python scripts/rebuild_fix.py slug...   ログ：out/rebuild_fix.log（最後に REBUILD_DONE）"""
import json, shutil, subprocess, sys, time
from pathlib import Path
R = Path(__file__).resolve().parents[1]; PY = sys.executable; LOG = R / 'out' / 'rebuild_fix.log'
def log(m):
    l = time.strftime('%H:%M:%S ') + m; print(l, flush=True)
    with LOG.open('a', encoding='utf-8') as f: f.write(l + '\n')
def run(a): return subprocess.run([PY, *a], cwd=R, capture_output=True, text=True, encoding='utf-8', errors='replace')
def probe(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True); return float(r.stdout.strip() or 0)
ok = []
for s in sys.argv[1:]:
    t0 = time.time()
    try:
        sp = R / 'data' / f'{s}_spec.json'; pack = json.loads(sp.read_text(encoding='utf8'))['pack']
        r = run(['scripts/vp.py', s, 'story'])
        if r.returncode: log(f'{s}: story 失敗 {r.stderr[-200:]}'); continue
        r = run(['scripts/vp.py', s, 'build']); vid = R / 'out' / f'{s}_video.mp4'
        if r.returncode or 'QA' not in r.stdout: log(f'{s}: build 失敗 {(r.stderr or r.stdout)[-300:]}'); continue
        old = R / 'upload' / pack / 'video.mp4'; dn, do = probe(vid), (probe(old) if old.exists() else 0)
        if do and abs(dn - do) > 2: log(f'{s}: 長さが違う {dn:.1f} vs {do:.1f}'); continue
        shutil.copyfile(vid, old); qa = [l for l in r.stdout.splitlines() if l.startswith('QA')]
        log(f'{s}: OK {dn:.1f}s {qa[-1] if qa else ""} ({(time.time()-t0)/60:.1f}分)'); ok.append(s)
    except Exception as e: log(f'{s}: 例外 {e}')
log(f'完了 {len(ok)}/{len(sys.argv)-1}'); log('REBUILD_DONE')
