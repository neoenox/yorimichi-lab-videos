# -*- coding: utf-8 -*-
"""既存の動画に「焼き込んだ字幕の指紋」を付ける（build.json が無い回の移行用）。

    python scripts\\stamp_build.py yakubusoku

`vp.py build` は 2026-10-31 から out/<slug>_build.json に字幕の sha256 を残す。
それ以前に焼いた動画は指紋が無く、preflight が mtime で判定するため
「replace() がアップロード直前に srt を書き直した」だけで NG になる。

安全条件（満たさなければ何もしない）:
  - out/<slug>_video.mp4 がある
  - out/<slug>_audio_report.json が動画より古い（焼き込みに使った音声レポートのまま）
  - data/<slug>_spec.json が動画より古い（字幕の元が変わっていない）
字幕は audio_report と spec から決まる純粋な関数（regen_srt_vp.py の docstring）なので、
この2つが動画より古ければ、いまの srt の中身は焼き込んだものと一致する。
"""
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf8')
R = Path(__file__).resolve().parent.parent


def stamp(slug):
    out = R / 'out'
    video = out / f'{slug}_video.mp4'
    srt = out / f'{slug}_subtitles.srt'
    rep = out / f'{slug}_audio_report.json'
    spec = R / 'data' / f'{slug}_spec.json'
    if not video.exists() or not srt.exists():
        print(f'!! {slug}: 動画か字幕が無い')
        return 1
    vm = video.stat().st_mtime
    for p, name in ((rep, 'audio_report'), (spec, 'spec')):
        if p.exists() and p.stat().st_mtime > vm + 1:
            print(f'!! {slug}: {name} が動画より新しい（{p.name}）。焼き直しが必要')
            return 1
    rec = {
        'srt_sha256': hashlib.sha256(srt.read_bytes()).hexdigest(),
        'srt_mtime': srt.stat().st_mtime,
        'video_mtime': vm,
        'at': 'stamped',
        'note': 'build.json 導入前の動画に、audio_report/spec が動画より古いことを確認して付けた',
    }
    (out / f'{slug}_build.json').write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding='utf8')
    print(f'ok {slug}: srt_sha256={rec["srt_sha256"][:16]}...')
    return 0


if __name__ == '__main__':
    rc = 0
    for s in sys.argv[1:]:
        rc |= stamp(s)
    sys.exit(rc)
