# -*- coding: utf-8 -*-
"""差し替え用に動画を作り直す（音声はキャッシュ済みなので合成しない）。

    python -X utf8 scripts\\rebuild_for_replace.py yakubusoku oke
    python -X utf8 scripts\\rebuild_for_replace.py --audio venus   # 字幕の息継ぎ同期も当て直す
    python -X utf8 scripts\\rebuild_for_replace.py --dry yakubusoku

各 slug について `vp.py <slug> bgm` → `build` → `pack` → `qa_lint <slug>` を順に実行する。
`--audio` を付けると先に `vp.py <slug> audio`（narration.wav がキャッシュ済みなら合成しない。
cue_times が作り直されるので、字幕が変わる＝build が必須）。

build は stage_qa まで含む（尺・デコード・LUFS・黒区間）。ログは out/codex/rebuild_<slug>.log。
1本でも失敗したらそこで止める（GPU を無駄に回さない）。終了コード 0=全部成功。
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / 'scripts'))
import replace_versions as rv  # noqa: E402  (PACK の対応表を使う)

FFMPEG_BIN = R / 'tools' / 'ffmpeg' / 'bin'
LOG_DIR = R / 'out' / 'codex'


def env():
    e = dict(os.environ)
    e['PATH'] = str(FFMPEG_BIN) + os.pathsep + e.get('PATH', '')
    e['PYTHONIOENCODING'] = 'utf8'
    return e


def run(cmd, log_path):
    """1段階を実行し、標準出力/エラーをログに追記する。戻り値は終了コード。"""
    with log_path.open('a', encoding='utf8') as f:
        f.write(f'\n$ {" ".join(cmd)}\n')
        f.flush()
        p = subprocess.run(cmd, cwd=str(R), env=env(), stdout=f, stderr=subprocess.STDOUT)
    return p.returncode


def has_cue_times(slug):
    p = R / 'out' / f'{slug}_audio_report.json'
    if not p.exists():
        return False
    try:
        d = json.loads(p.read_text(encoding='utf8'))
    except Exception:  # noqa: BLE001
        return False
    segs = d.get('segments') or []
    return bool(segs) and all('cue_times' in s for s in segs)


def rebuild(slug, with_audio=False, dry=False):
    if slug not in rv.PACK:
        print(f'!! {slug}: replace_versions.PACK に無い（パック名が分からない）')
        return 1
    if not (R / 'data' / f'{slug}_spec.json').exists():
        # 旧系統（*_compose.py）は vp.py の対象外。専用の作り直しを使う。
        print(f'!! {slug}: data/{slug}_spec.json が無い（vp.py の対象外）。'
              f'`python scripts\\rebuild_old_compose.py {slug}` を使う')
        return 1
    pack = rv.PACK[slug]
    log = LOG_DIR / f'rebuild_{slug}.log'
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log.write_text('', encoding='utf8')

    stages = []
    if with_audio and not has_cue_times(slug):
        stages.append(['audio'])
    stages += [['bgm'], ['build'], ['pack']]
    print(f'== {slug} ({pack}) stages: {" ".join(s[0] for s in stages)} + qa_lint')
    if dry:
        return 0

    t0 = time.time()
    for st in stages:
        cmd = [sys.executable, '-X', 'utf8', str(R / 'scripts' / 'vp.py'), slug, *st]
        rc = run(cmd, log)
        if rc != 0:
            print(f'!! {slug}: {st[0]} が失敗（exit {rc}）。{log} を見る')
            return rc
        print(f'   {st[0]} ok ({time.time() - t0:.0f}s)')

    # 最終確認：差し替えに必要なものが揃っているか
    out_v = R / 'out' / f'{slug}_video.mp4'
    pack_v = R / 'upload' / pack / 'video.mp4'
    if not out_v.exists() or not pack_v.exists():
        print(f'!! {slug}: out かパックに video.mp4 が無い（out={out_v.exists()} pack={pack_v.exists()}）')
        return 1
    if not rv.same_file(out_v, pack_v):
        print(f'!! {slug}: パックの video.mp4 が今の書き出しと違う')
        return 1

    rc = run([sys.executable, '-X', 'utf8', str(R / 'scripts' / 'qa_lint.py'), slug], log)
    print(f'   qa_lint exit {rc} ({time.time() - t0:.0f}s)  -> {log}')
    return 0 if rc in (0,) else rc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slugs', nargs='+')
    ap.add_argument('--audio', action='store_true', help='先に audio（字幕の息継ぎ同期）を当て直す')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    for s in a.slugs:
        rc = rebuild(s, with_audio=a.audio, dry=a.dry)
        if rc != 0:
            sys.exit(rc)
    print('all ok')


if __name__ == '__main__':
    main()
