"""TikTok用の書き出しを検査する。

usage:
    python scripts/check_tiktok.py                     # out/short_tiktok_*.mp4 を全部
    python scripts/check_tiktok.py tiktok_shibuya ...  # 指定したslugだけ

見るもの: 1080x1920 / 20〜45秒 / 音声トラック / 禁止語（チャンネル登録・概要欄・youtu.be等）/
クレジット（VOICEVOX）/ 出典の有無。ffmpegとffprobeはPATH、無ければ tools/ffmpeg/bin を使う。
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_BIN = ROOT / 'tools' / 'ffmpeg' / 'bin'
if not shutil.which('ffprobe') and _BIN.exists():
    os.environ['PATH'] = str(_BIN) + os.pathsep + os.environ.get('PATH', '')
BANNED = ['チャンネル登録', '概要欄', 'youtu.be', '高評価', '拡散希望', '長い動画', '本編']
MIN_SEC, MAX_SEC = 20.0, 45.0


def probe(p):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                          'stream=codec_type,width,height,r_frame_rate:format=duration',
                          '-of', 'json', str(p)], capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    v = next(s for s in d['streams'] if s['codec_type'] == 'video')
    has_audio = any(s['codec_type'] == 'audio' for s in d['streams'])
    return int(v['width']), int(v['height']), float(d['format']['duration']), has_audio


def main():
    if not sys.argv[1:]:
        slugs = sorted(p.stem.replace('short_', '') for p in (ROOT / 'out').glob('short_tiktok_*.mp4'))
    else:
        slugs = sys.argv[1:]
    bad = 0
    for slug in slugs:
        mp4 = ROOT / 'out' / f'short_{slug}.mp4'
        srt = ROOT / 'out' / f'short_{slug}_subtitles.srt'
        cap = ROOT / 'out' / f'short_{slug}_description.md'
        if not mp4.exists():
            print(f'FAIL  {slug}: mp4 がない')
            bad += 1
            continue
        w, h, dur, has_audio = probe(mp4)
        text = ''.join(p.read_text(encoding='utf8') for p in (srt, cap) if p.exists())
        hits = [b for b in BANNED if b in text]
        rows = [
            ('解像度', f'{w}x{h}', w == 1080 and h == 1920),
            ('尺', f'{dur:.1f}s', MIN_SEC <= dur <= MAX_SEC),
            ('音声', 'あり' if has_audio else 'なし', has_audio),
            ('禁止語', 'なし' if not hits else ', '.join(hits), not hits),
            ('クレジット', 'VOICEVOX', 'VOICEVOX' in text),
            ('出典', '出典/参考', ('出典' in text or '参考' in text)),
        ]
        ok = all(r[2] for r in rows)
        print(f'{"PASS" if ok else "FAIL"}  {slug}  ({dur:.1f}s, {w}x{h})')
        for name, val, good in rows:
            if not good:
                print(f'   - {name}: {val}')
        bad += 0 if ok else 1
    print(f'\n{len(slugs) - bad}/{len(slugs)} PASS')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
