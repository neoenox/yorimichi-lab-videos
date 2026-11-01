"""旧形式の動画を、ポップ形式に自動で作り直す（1本ずつ順番に）。台本・音声・概要欄・字幕は変えず、画面だけ。
usage: python scripts/batch_pop.py slug1 slug2 ...
各 slug：to_pop.py → vp.py story → vp.py build（検査つき）→ upload/<pack>/video.mp4 に入れ替え（概要欄・サムネイルは、そのまま）。
ログ：out/batch_pop.log。失敗した slug は、記録して次へ進む。"""
import json, subprocess, sys, time, shutil
from pathlib import Path
R = Path(__file__).resolve().parents[1]
PY = sys.executable
LOG = R / 'out' / 'batch_pop.log'


def log(msg):
    line = time.strftime('%H:%M:%S ') + msg
    print(line, flush=True)
    with LOG.open('a', encoding='utf-8') as f: f.write(line + '\n')


def run(args, **kw):
    return subprocess.run([PY, *args], cwd=R, capture_output=True, text=True, encoding='utf-8', errors='replace', **kw)


def probe(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def one(slug):
    t0 = time.time()
    spec_p = R / 'data' / f'{slug}_spec.json'
    if not spec_p.exists(): log(f'{slug}: spec が無い'); return False
    pack = json.loads((R / 'data' / f'{slug}_spec_before_pop.json').read_text(encoding='utf8'))['pack'] if (R / 'data' / f'{slug}_spec_before_pop.json').exists() else json.loads(spec_p.read_text(encoding='utf8'))['pack']
    r = run(['scripts/to_pop.py', slug])
    if r.returncode: log(f'{slug}: to_pop 失敗 {r.stderr[-300:]}'); return False
    r = run(['scripts/vp.py', slug, 'story'])
    if r.returncode: log(f'{slug}: story 失敗 {r.stderr[-300:]}'); return False
    for need, stage in (('narration', 'audio'), ('bgm', 'bgm')):
        if not (R / 'out' / f'{slug}_{need}.wav').exists():
            r0 = run(['scripts/vp.py', slug, stage])
            if r0.returncode: log(f'{slug}: {stage} 失敗 {(r0.stderr or r0.stdout)[-300:]}'); return False
    r = run(['scripts/vp.py', slug, 'build'])
    vid = R / 'out' / f'{slug}_video.mp4'
    if r.returncode or 'QA' not in r.stdout:
        log(f'{slug}: build 失敗 {(r.stderr or r.stdout)[-400:]}'); return False
    qa = [l for l in r.stdout.splitlines() if l.startswith('QA')]
    if not vid.exists() or vid.stat().st_mtime < spec_p.stat().st_mtime:
        log(f'{slug}: 動画が新しくない'); return False
    old = R / 'upload' / pack / 'video.mp4'
    d_new, d_old = probe(vid), probe(old) if old.exists() else 0
    if d_old and abs(d_new - d_old) > 2.0:
        log(f'{slug}: 長さが違う new={d_new:.1f} old={d_old:.1f}（入れ替えない）'); return False
    shutil.copyfile(vid, old)
    log(f'{slug}: OK {pack} {d_new:.1f}s {qa[-1] if qa else ""} ({(time.time()-t0)/60:.1f}分)')
    return True


if __name__ == '__main__':
    ok = []
    for s in sys.argv[1:]:
        try:
            if one(s): ok.append(s)
        except Exception as e:
            log(f'{s}: 例外 {e}')
    log(f'完了 {len(ok)}/{len(sys.argv) - 1}: {ok}')
    log('BATCH_DONE')
