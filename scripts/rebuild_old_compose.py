"""旧系統（*_compose.py）で作られた長尺を、いまの焼き込み字幕（算用数字）で作り直す。

vp.py を使わない3本（world map / 本能寺 / 忍者）専用。
- 既存の cache/<slug>_part_*.mp4 は cache/prev_<日時>/ へ退避（final が混ざらないように）
- フレームを描き直して連結（映像のみ）
- 音声は「いま公開予約している動画」からそのままコピー（BGM・ラウドネスを触らない）

usage: python scripts/rebuild_old_compose.py gm|hn|nj [...]
"""
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

R = Path(__file__).resolve().parents[1]
# ffmpeg をこのプロセス自身の PATH にも入れる（連結・多重化で使う）
os.environ['PATH'] = str(R / 'tools' / 'ffmpeg' / 'bin') + os.pathsep + os.environ.get('PATH', '')
SPEC = {
    'gm': dict(script='gm_compose.py', out='out/gm_video.mp4', old='out/gm_video.mp4',
               prefix='gm_part_', timeline='data/gm_timeline.json'),
    'nj': dict(script='nj_compose.py', out='out/nj_video.mp4', old='out/nj_video.mp4',
               prefix='nj_part_', timeline='data/nj_timeline.json'),
    'hn': dict(script='hn_compose4.py', out='out/hn_video.mp4', old='out/honnoji.mp4',
               prefix='hn4_part_', timeline='data/hn_timeline.json'),
}


def dur(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'csv=p=0', str(p)], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def ok_mp4(p):
    """書きかけの mp4（moov が無い）を弾く。"""
    if not p.exists() or p.stat().st_size < 1024:
        return False
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'csv=p=0', str(p)], capture_output=True, text=True)
    return r.returncode == 0 and r.stdout.strip() not in ('', 'N/A')


def ok_chunk(p, a, b):
    """パートが最後まで書けているかを、想定尺（(b-a)/30 秒）で確かめる。

    ffmpeg を強制終了すると、moov は書かれて「読める」が途中で切れた mp4 が残る。
    ok_mp4 だけだとそれを正常と誤認して結合から抜け、尺が足りない完成品になる。
    """
    if not ok_mp4(p):
        return False
    try:
        d = dur(p)
    except Exception:
        return False
    return abs(d - (b - a) / 30) < 1.0


def expected_span(p, prefix):
    """ファイル名から (a, b) を取り出す。取れなければ None。"""
    try:
        stem = p.stem[len(prefix):]
        a, b = stem.split('_')
        return int(a), int(b)
    except Exception:
        return None


def total_frames(slug):
    import json
    t = json.loads((R / SPEC[slug]['timeline']).read_text(encoding='utf8'))
    return round(t[-1]['end'] * 30), round(t[-1]['end'])


def run(slug):
    s = SPEC[slug]
    env = dict(os.environ)
    env['PATH'] = str(R / 'tools' / 'ffmpeg' / 'bin') + os.pathsep + env['PATH']
    env['PYTHONIOENCODING'] = 'utf8'

    prev = R / 'cache' / f'prev_{dt.datetime.now():%Y%m%d_%H%M}'
    # パートの命名は系統ごとに違う（gm_part_ / nj_part_ / hn4_part_）
    prefix = s.get('prefix', f'{slug}_part_')
    parts = sorted((R / 'cache').glob(prefix + '*.mp4'))
    chunk = int(os.environ.get('CHUNK', '0'))
    if not os.environ.get('SKIP_RENDER'):
        # 壊れた（書きかけの）パートは退避。CHUNK 指定時は正常なパートを再利用する
        def good(p):
            span = expected_span(p, prefix)
            return ok_chunk(p, *span) if span else ok_mp4(p)

        bad = [p for p in parts if not good(p)]
        if bad:
            prev.mkdir(parents=True, exist_ok=True)
            for p in bad:
                shutil.move(str(p), str(prev / p.name))
            print(f'{slug}: 壊れたパート {len(bad)} 本を {prev.name} へ退避', flush=True)
        elif not chunk:
            prev.mkdir(parents=True, exist_ok=True)
            for p in parts:
                shutil.move(str(p), str(prev / p.name))
            print(f'{slug}: 旧パート {len(parts)} 本を {prev.name} へ退避', flush=True)

        if chunk:
            n_frames, n_sec = total_frames(slug)
            print(f'{slug}: {n_frames} フレーム（{n_sec}秒）を {chunk} フレームずつ', flush=True)
            for a in range(0, n_frames, chunk):
                b = min(a + chunk, n_frames)
                out = R / 'cache' / f'{prefix}{a}_{b}.mp4'
                if ok_chunk(out, a, b):
                    print(f'  {a}-{b} は作成済み', flush=True)
                    continue
                t0 = time.time()
                p = subprocess.run([sys.executable, str(R / 'scripts' / s['script']),
                                    'part', str(a), str(b)],
                                   cwd=str(R), env=env, capture_output=True, text=True,
                                   encoding='utf8', errors='replace')
                print(f'  {a}-{b} rc={p.returncode} {time.time() - t0:.0f}s', flush=True)
                if p.returncode != 0:
                    print((p.stderr or '')[-1500:], flush=True)
                    return False
        else:
            t0 = time.time()
            p = subprocess.run([sys.executable, str(R / 'scripts' / s['script']), 'part', '0', '999999'],
                               cwd=str(R), env=env, capture_output=True, text=True,
                               encoding='utf8', errors='replace')
            print(f'{slug}: render rc={p.returncode} {time.time() - t0:.0f}s', flush=True)
            if p.returncode != 0:
                print((p.stderr or '')[-2000:], flush=True)
                return False

    new_parts = sorted((R / 'cache').glob(prefix + '*.mp4'),
                       key=lambda x: int(x.stem.split('_')[2]))
    if not new_parts:
        print(f'{slug}: パートができていない', flush=True)
        return False
    lst = R / 'cache' / f'{slug}_new_parts.txt'
    lst.write_text(''.join(f"file '{x.as_posix()}'\n" for x in new_parts), encoding='utf8')
    silent = R / 'cache' / f'{slug}_video_silent.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'warning', '-f', 'concat', '-safe', '0',
                    '-i', str(lst), '-c', 'copy', str(silent)], check=True)

    old = R / s['old']
    if not old.exists():
        print(f'{slug}: 元の完成版 {old} が無い（音声を借りられない）', flush=True)
        return False
    target = R / s['out']
    tmp = R / 'cache' / f'{slug}_mux.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'warning', '-i', str(silent), '-i', str(old),
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9',
                    '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
                    '-shortest', str(tmp)], check=True)
    a, b = dur(silent), dur(old)
    if abs(a - b) > 1.0:
        print(f'{slug}: 尺が合わない 新 {a:.1f}s / 元 {b:.1f}s → 中止', flush=True)
        return False
    shutil.move(str(tmp), str(target))
    print(f'{slug}: 完成 {target} {dur(target):.1f}s（元 {b:.1f}s）', flush=True)
    return True


def from_cache(slug):
    """cache に残っている「無音映像」と「ミックス音声」から完成品を作る（再レンダリングなし）。

    2026-10-28 以降 out/<slug>_video.mp4 と upload/<pack>/video.mp4 が消えた回の復旧用。
    `rebuild_old_compose.run()` は音声を「元の完成版」から借りるが、それも消えている場合は
    `cache/<slug>_video_silent.mp4`（10/21 に作り直した映像）と `cache/<slug>_mix.wav`
    （ナレーション＋BGMのミックス）で同じものが作れる。尺が一致することを確かめてから結合する。
    """
    s = SPEC[slug]
    silent = R / 'cache' / f'{slug}_video_silent.mp4'
    mix = R / 'cache' / f'{slug}_mix.wav'
    if not ok_mp4(silent) or not mix.exists():
        print(f'{slug}: cache に無音映像かミックス音声が無い', flush=True)
        return False
    a, b = dur(silent), dur(mix)
    if abs(a - b) > 1.0:
        print(f'{slug}: 尺が合わない 映像 {a:.1f}s / 音声 {b:.1f}s → 中止', flush=True)
        return False
    target = R / s['out']
    tmp = R / 'cache' / f'{slug}_restore.mp4'
    # loudnorm は2パス（測ってから当てる）。mix は既に BGM 込みなので、そのまま -14 LUFS に揃える。
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(mix), '-af',
                        'loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True, encoding='utf8', errors='replace')
    import re
    j = json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}', r.stderr, re.S).group(0))
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(['ffmpeg', '-y', '-v', 'warning', '-i', str(silent), '-i', str(mix),
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', af,
                    '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart',
                    '-shortest', str(tmp)], check=True)
    d = dur(tmp)
    if abs(d - a) > 1.0:
        print(f'{slug}: 書き出しの尺が合わない {d:.1f}s / 映像 {a:.1f}s → 中止', flush=True)
        return False
    shutil.move(str(tmp), str(target))
    print(f'{slug}: cache から復元 {target} {d:.1f}s（{j["input_i"]} LUFS 入力 → -14 目標）', flush=True)
    return True


if __name__ == '__main__':
    args = sys.argv[1:]
    use_cache = '--from-cache' in args
    args = [a for a in args if not a.startswith('--')]
    ok = True
    for slug in args:
        ok = (from_cache(slug) if use_cache else run(slug)) and ok
    sys.exit(0 if ok else 1)
