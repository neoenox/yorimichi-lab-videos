"""字幕・画面の修正を反映して作り直す（音声は変えない）。srt再生成 → story → build → upload/<pack>/ の video.mp4 と subtitles_ja.srt を入れ替え。
usage: python scripts/rebuild_all.py slug... [--sync-main|--sync-main-pr|--sync-main-dry]
       ログ：out/rebuild_all.log（最後に ALL_DONE）。VP_MAXPAR で並列数。
       --sync-main 作り終えたらテキストのみを main へ push（素材は push しない）
       --sync-main-pr 同上だが PR を作る。--sync-main-dry 何が入るか表示だけ。"""
import json, shutil, subprocess, sys, time
from pathlib import Path
R = Path(__file__).resolve().parents[1]; PY = sys.executable; LOG = R / 'out' / 'rebuild_all.log'
FLAGS = {a for a in sys.argv[1:] if a.startswith('--')}; SLUGS = [a for a in sys.argv[1:] if not a.startswith('--')]
def log(m):
    l = time.strftime('%H:%M:%S ') + m
    with LOG.open('a', encoding='utf-8') as f: f.write(l + '\n')
def run(a): return subprocess.run([PY, *a], cwd=R, capture_output=True, text=True, encoding='utf-8', errors='replace')
def probe(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True); return float(r.stdout.strip() or 0)
ok = []
for s in SLUGS:
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
log(f'完了 {len(ok)}/{len(SLUGS)}')
# 仕上げ：テキストのみを main へ反映（素材は push しない）。失敗しても ALL_DONE は書く。
if FLAGS & {'--sync-main', '--sync-main-pr', '--sync-main-dry'}:
    sys.path.insert(0, str(R / 'scripts'))
    try:
        from main_push_textonly import push_text_only, MediaInDiff
        r = push_text_only(pr='--sync-main-pr' in FLAGS, direct='--sync-main' in FLAGS,
                           dry_run='--sync-main-dry' in FLAGS)
        if not r['changed']: log('main 同期: 変更なし')
        elif r['pr_url']: log(f'main 同期: PR {r["pr_url"]}')
        else: log(f'main 同期: {r["files"]} ファイル / commit {(r["commit"] or "dry-run")[:7]}')
    except MediaInDiff as e:
        log(f'main 同期: 中止（素材 {len(e.paths)} 件が差分に残っている。gitignore を確認）')
    except Exception as e:
        log(f'main 同期: 失敗 {e}')
log('ALL_DONE')
