"""BGM差し替え（vp_remix.py）後の一括検証。映像は再エンコードせず、音声だけを解析する。

見るもの:
  1. 尺   : 映像尺 ≒ spec の timeline 末尾 ≒ out/<slug>_video_nobgm.mp4 ≒ フレーム数
  2. 音   : -14 LUFS 付近 / ピーク -1.5 以下 / 無音でない
  3. BGM  : サイド成分(L-R)に音楽が乗っているか（ナレーションはモノラル複製なので L=R）
  4. 曲   : 同一動画内で同じ曲が連続しない・1曲への偏りが無い／動画間で並びを使い回していない
  5. 台帳 : upload/<pack>/description.txt と out/<slug>_description.md に、使った曲名が全部載っている
  6. パック: upload/<pack>/video.mp4 が out/<slug>_video.mp4 と同じ尺

usage: python scripts/verify_bgm_remix.py [slug...]
  引数なし = out/bgm_remix_all.log の「OK」行（実際に差し替えた本）を対象。
出力: out/bgm_remix_verify.json, out/BGM_REMIX_VERIFY.md
"""
import concurrent.futures as cf
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
_BIN = R / 'tools' / 'ffmpeg' / 'bin'
if not shutil.which('ffprobe') and _BIN.exists():
    os.environ['PATH'] = str(_BIN) + os.pathsep + os.environ.get('PATH', '')
FFMPEG, FFPROBE = 'ffmpeg', 'ffprobe'
TO_JP = {'piano': 'ピアノ', 'ethnic': '民族', 'orchestra': 'オーケストラ', 'acoustic': 'アコースティック'}
SIM = {}


def jp(track):
    m = re.match(r'([a-z]+)(\d+)$', track)
    if not m:
        return track
    return TO_JP.get(m.group(1), m.group(1)) + m.group(2)


def sh(args):
    return subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')


def probe(p):
    r = sh([FFPROBE, '-v', 'error', '-show_entries',
            'format=duration:stream=codec_type,codec_name,width,height,nb_frames,duration', '-of', 'json', str(p)])
    j = json.loads(r.stdout or '{}')
    v = next((s for s in j.get('streams', []) if s.get('codec_type') == 'video'), {})
    a = next((s for s in j.get('streams', []) if s.get('codec_type') == 'audio'), {})
    return {
        'dur': float(j.get('format', {}).get('duration') or 0),
        'v_dur': float(v.get('duration') or 0), 'v_frames': int(v.get('nb_frames') or 0),
        'w': v.get('width'), 'h': v.get('height'), 'v_codec': v.get('codec_name'), 'a_codec': a.get('codec_name'),
    }


def loud(p):
    r = sh([FFMPEG, '-hide_banner', '-nostats', '-i', str(p), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json', '-f', 'null', '-'])
    m = re.search(r'\{[^{}]*"input_i"[^{}]*\}', r.stderr, re.S)
    if not m:
        return None
    j = json.loads(m.group(0))
    try:
        return float(j['input_i']), float(j['input_tp'])
    except (KeyError, ValueError):
        return None


def side_rms(p, ss=None, t=None):
    """L-R 成分の平均音量。BGMがステレオで入っていれば -40dB 前後、ナレーションだけなら無音に近い。"""
    head = [FFMPEG, '-hide_banner', '-nostats']
    if ss is not None:
        head += ['-ss', f'{ss:.2f}', '-t', f'{t:.2f}']
    r = sh(head + ['-i', str(p), '-af', 'pan=mono|c0=0.5*c0-0.5*c1,volumedetect', '-f', 'null', '-'])
    m = re.search(r'mean_volume:\s*(-?[\d.]+) dB', r.stderr)
    return float(m.group(1)) if m else None


def gaps(p, min_len=1.0, limit=4):
    """ナレーションの無音区間（長い順）。BGMだけが鳴っている区間を取るために使う。"""
    r = sh([FFMPEG, '-hide_banner', '-nostats', '-i', str(p), '-af', 'silencedetect=n=-35dB:d=0.6', '-f', 'null', '-'])
    st, en = [], []
    for line in r.stderr.splitlines():
        m = re.search(r'silence_start:\s*([\d.]+)', line)
        if m:
            st.append(float(m.group(1)))
        m = re.search(r'silence_end:\s*([\d.]+)\s*\|\s*silence_duration:\s*([\d.]+)', line)
        if m:
            en.append((float(m.group(1)), float(m.group(2))))
    out = [(e - d, d) for e, d in en if d >= min_len]
    out.sort(key=lambda x: -x[1])
    return out[:limit]


def check(slug):
    out = {'slug': slug, 'problems': []}
    sp_path = R / 'data' / f'{slug}_spec.json'
    if not sp_path.exists():
        out['problems'].append('spec が無い')
        return out
    spec = json.loads(sp_path.read_text(encoding='utf8'))
    pack = spec.get('pack')
    out['pack'] = pack
    vid = R / 'out' / f'{slug}_video.mp4'
    nob = R / 'out' / f'{slug}_video_nobgm.mp4'
    if not vid.exists():
        out['problems'].append('out/<slug>_video.mp4 が無い')
        return out
    out['mtime'] = vid.stat().st_mtime
    v = probe(vid)
    out.update(v)

    # 2. 音
    ln = loud(vid)
    if not ln:
        out['problems'].append('ラウドネスが測れない')
    else:
        out['lufs'], out['true_peak'] = ln
        if not -15.5 <= ln[0] <= -13.0:
            out['problems'].append(f'ラウドネス {ln[0]:.1f} LUFS（-14から外れ）')
        if ln[1] > -0.8:
            out['problems'].append(f'ピーク {ln[1]:.1f} dBTP（-1.5目標に対し高い）')
    out['side_rms'] = side_rms(vid)
    # ナレーションの無音区間ではBGMだけが鳴る。そこで測れば「BGMが入っているか」を直接見られる
    nar0 = R / 'out' / f'{slug}_narration.wav'
    lv = []
    if nar0.exists():
        for s, d in gaps(nar0):
            v0 = side_rms(vid, ss=s + min(0.25, d / 3), t=min(1.2, d * 0.6))
            if v0 is not None:
                lv.append(v0)
    out['bgm_pause_db'] = round(sorted(lv)[len(lv) // 2], 1) if lv else None
    if out['bgm_pause_db'] is not None:
        out['bgm_pause_n'] = len(lv)
        if out['bgm_pause_db'] < -52:
            out['problems'].append(f'無音区間にBGMが無い（{out["bgm_pause_db"]:.1f} dB）')
    elif out['side_rms'] is not None and out['side_rms'] < -48:
        out['problems'].append(f'BGMのステレオ成分がほぼ無い ({out["side_rms"]:.1f} dB)')

    # 1. 尺
    tl = R / 'data' / f'{slug}_timeline.json'
    if tl.exists():
        tl_end = json.loads(tl.read_text(encoding='utf8'))[-1]['end']
        out['timeline_end'] = round(tl_end, 2)
        if abs(tl_end - v['dur']) > 1.0:
            out['problems'].append(f'尺が timeline と合わない {v["dur"]:.1f}s vs {tl_end:.1f}s')
    if nob.exists():
        n = probe(nob)
        out['nobgm_dur'], out['nobgm_frames'] = n['dur'], n['v_frames']
        if abs(n['dur'] - v['dur']) > 0.5:
            out['problems'].append(f'nobgm と尺が違う {v["dur"]:.1f}s vs {n["dur"]:.1f}s')
        if v['v_frames'] and n['v_frames'] and abs(v['v_frames'] - n['v_frames']) > 2:
            out['problems'].append(f'フレーム数が違う {v["v_frames"]} vs {n["v_frames"]}')
    else:
        out['problems'].append('nobgm が無い')

    nar = R / 'out' / f'{slug}_narration.wav'
    if nar.exists():
        out['narration_dur'] = round(probe(nar)['dur'], 2)
        if out['narration_dur'] > v['dur'] + 0.3:
            out['problems'].append(f'ナレーション({out["narration_dur"]:.1f}s)が映像より長い')

    # 4. 曲
    plan = spec.get('bgm') or []
    tracks = [b[2] for b in plan]
    out['segments'] = len(plan)
    out['tracks'] = tracks
    if not plan:
        out['problems'].append('bgm の指定が無い')
    else:
        for i in range(1, len(tracks)):
            if tracks[i] == tracks[i - 1]:
                out['problems'].append(f'{i}番目の区間で同じ曲が連続（{tracks[i]}）')
        top = max(set(tracks), key=tracks.count)
        out['top_track_share'] = round(tracks.count(top) / len(tracks), 2)
        if len(tracks) >= 5 and out['top_track_share'] > 0.6:
            out['problems'].append(f'{jp(top)} が{out["top_track_share"]*100:.0f}%を占める')
        if len(set(tracks)) < min(3, len(tracks)):
            out['problems'].append(f'曲数が少なすぎる（{len(set(tracks))}曲）')

    # 5. 台帳（クレジット）
    need = list(dict.fromkeys(jp(t) for t in tracks))
    descs = []
    if pack:
        p = R / 'upload' / pack / 'description.txt'
        if p.exists():
            descs.append(('upload/description.txt', p.read_text(encoding='utf-8', errors='replace')))
        else:
            out['problems'].append('upload/<pack>/description.txt が無い')
    md = R / 'out' / f'{slug}_description.md'
    if md.exists():
        descs.append(('out/<slug>_description.md', md.read_text(encoding='utf-8', errors='replace')))
    if not descs:
        out['problems'].append('クレジット台帳が見つからない')
    for name, text in descs:
        if '魔王魂' not in text:
            out['problems'].append(f'{name} に魔王魂のクレジットが無い')
        missing = [t for t in need if t not in text]
        if missing:
            out['problems'].append(f'{name} に曲名が無い: {", ".join(missing)}')

    # 6. パック
    if pack:
        pv = R / 'upload' / pack / 'video.mp4'
        if pv.exists():
            pd = probe(pv)['dur']
            out['pack_dur'] = round(pd, 2)
            if abs(pd - v['dur']) > 0.6:
                out['problems'].append(f'upload/<pack>/video.mp4 の尺が古い {pd:.1f}s vs {v["dur"]:.1f}s')
        else:
            out['problems'].append('upload/<pack>/video.mp4 が無い')
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    if args:
        slugs = args
    else:
        log = R / 'out' / 'bgm_remix_all.log'
        slugs = []
        if log.exists():
            for line in log.read_text(encoding='utf-8', errors='replace').splitlines():
                m = re.match(r'^(\S+) OK$', line.strip())
                if m:
                    slugs.append(m.group(1))
    slugs = list(dict.fromkeys(slugs))
    print(f'対象 {len(slugs)} 本')
    rows = []
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(check, s): s for s in slugs}
        for k, f in enumerate(cf.as_completed(futs), 1):
            try:
                r = f.result()
            except Exception as e:  # 1本の失敗で全体を止めない
                r = {'slug': futs[f], 'problems': [f'例外 {e}']}
            rows.append(r)
            print(f'[{k}/{len(slugs)}] {r["slug"]:14} {"OK" if not r["problems"] else str(len(r["problems"])) + "件"}', flush=True)
    rows.sort(key=lambda r: r['slug'])

    # 動画間の使い回し
    seq = {}
    for r in rows:
        t = tuple(r.get('tracks') or [])
        if t:
            seq.setdefault(t, []).append(r['slug'])
    dup = {k: v for k, v in seq.items() if len(v) > 1}
    first = {}
    for r in rows:
        t = r.get('tracks') or []
        if t:
            first[t[0]] = first.get(t[0], 0) + 1

    res = {
        'checked': len(rows),
        'fail': sum(1 for r in rows if r['problems']),
        'duplicate_sequences': [{'slugs': v, 'tracks': list(k)} for k, v in dup.items()],
        'first_track': first,
        'rows': rows,
    }
    (R / 'out' / 'bgm_remix_verify.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf8')

    bad = [r for r in rows if r['problems']]
    L = ['# BGM差し替えの検証（' + __import__('datetime').date.today().isoformat() + '）', '',
         f'- 対象: {len(rows)}本 / 問題あり: {len(bad)}本', '']
    if bad:
        L += ['## 要確認', '', '| slug | 指摘 |', '|---|---|']
        for r in bad:
            L.append(f'| {r["slug"]} | {"／".join(r["problems"])} |')
        L.append('')
    L += ['## 数値', '', '| slug | 尺 | LUFS | TP | 無音時BGM | 全体サイド | 区間 | 先頭曲 | パック尺 |', '|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        L.append('| {slug} | {dur:.1f}s | {lufs} | {tp} | {pz} | {side} | {seg} | {first} | {pack} |'.format(
            slug=r['slug'], dur=r.get('dur') or 0,
            lufs=f'{r["lufs"]:.1f}' if r.get('lufs') is not None else '—',
            tp=f'{r["true_peak"]:.1f}' if r.get('true_peak') is not None else '—',
            pz=f'{r["bgm_pause_db"]:.0f}dB' if r.get('bgm_pause_db') is not None else '—',
            side=f'{r["side_rms"]:.0f}dB' if r.get('side_rms') is not None else '—',
            seg=r.get('segments', '—'),
            first=jp(r['tracks'][0]) if r.get('tracks') else '—',
            pack=f'{r["pack_dur"]:.1f}s' if r.get('pack_dur') else '—'))
    L += ['', '## 曲の散らばり', '',
          f'- 先頭曲の種類: {len(first)}種', '',
          '| 先頭曲 | 本数 |', '|---|---|']
    for k, v in sorted(first.items(), key=lambda kv: -kv[1]):
        L.append(f'| {jp(k)} | {v} |')
    L += ['', f'- 同じ並びの動画: {len(dup)}組']
    for k, v in dup.items():
        L.append(f'  - {", ".join(v)}: {" / ".join(jp(x) for x in k)}')
    (R / 'out' / 'BGM_REMIX_VERIFY.md').write_text('\n'.join(L) + '\n', encoding='utf8')
    print(f'\n問題あり {len(bad)}/{len(rows)}  → out/BGM_REMIX_VERIFY.md')
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
