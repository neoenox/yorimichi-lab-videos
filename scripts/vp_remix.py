"""BGMだけを替えて、動画の音を作り直す（映像は作り直さない。1本1〜2分）。
spec の bgm を使って out/<slug>_bgm.wav を作り、out/<slug>_video_nobgm.mp4 の声と混ぜて out/<slug>_video.mp4 を出す。
usage: python scripts/vp_remix.py slug...   （事前に bgm_plan.py --apply）。upload/<pack>/video.mp4 にも入れ替える。"""
import json, shutil, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]; PY = sys.executable
for s in sys.argv[1:]:
    sp = json.loads((R / 'data' / f'{s}_spec.json').read_text(encoding='utf8'))
    r = subprocess.run([PY, 'scripts/vp.py', s, 'bgm'], cwd=R, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode: print(s, 'bgm 失敗', r.stderr[-200:]); continue
    code = f'''
import sys; sys.argv=['vp.py','{s}','x']
import vp
from pathlib import Path
vp.SLUG='{s}'; vp.load_runtime()
'''
    # vp.py の build 後半と同じ混ぜ方
    wav = R / 'out' / f'{s}_narration.wav'; nob = R / 'out' / f'{s}_video_nobgm.mp4'; bgm = R / 'out' / f'{s}_bgm.wav'
    mix = R / 'cache' / f'{s}_mix.wav'; out = R / 'out' / f'{s}_video.mp4'
    fc = "[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,asplit=2[n1][n2];[1:a]volume=-6.0dB[bg];[bg][n2]sidechaincompress=threshold=0.02:ratio=4:attack=30:release=900:makeup=1[duck];[n1][duck]amix=inputs=2:normalize=0:duration=first[m]"
    subprocess.run(['ffmpeg', '-y', '-v', 'warning', '-i', str(wav), '-i', str(bgm), '-filter_complex', fc, '-map', '[m]', '-c:a', 'pcm_s16le', str(mix)], check=True)
    import re
    def loud(path):
        q = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(path), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json', '-f', 'null', '-'], capture_output=True, text=True)
        j = json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}', q.stderr, re.S).group(0))
        return f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true"
    subprocess.run(['ffmpeg', '-y', '-v', 'warning', '-i', str(nob), '-i', str(mix), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', loud(mix), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', str(out)], check=True)
    shutil.copyfile(out, R / 'upload' / sp['pack'] / 'video.mp4')
    # 概要欄の曲名（クレジット）を、新しい曲に合わせて作り直し、アップロード用フォルダも更新
    for cmd in ('desc', 'pack'):
        q = subprocess.run([PY, 'scripts/vp.py', s, cmd], cwd=R, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if q.returncode: print(s, cmd, '失敗', q.stderr[-200:])
    print(s, 'OK')
