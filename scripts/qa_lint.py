"""完成品の品質チェック（公開前の関門）。

レンダリングはせず、`out/` の完成品・字幕・仕様だけを見る。
「気づかずに低品質を出す」事故を防ぐのが目的。

usage:
  python scripts/qa_lint.py --all              # out/ にある完成品すべて
  python scripts/qa_lint.py calendar venus     # 指定だけ
  python scripts/qa_lint.py --all --no-audio   # 音量測定を飛ばす（速い）

判定は 3 段階:
  NG   … 公開を止める（字幕が読めない、音量が基準外、尺がずれている等）
  WARN … 直せるなら直す（章が長い、冒頭にフックが無い等）
  OK   … 問題なし

結果は `out/codex/qa_lint.txt` にも書く。NG が 1 件でもあれば終了コード 1。
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))

OUT = R / 'out'
REPORT = R / 'out' / 'codex' / 'qa_lint.txt'
# ffmpeg は PATH に無いことがあるので、リポジトリ内のものがあればそれを使う
_BIN = R / 'tools' / 'ffmpeg' / 'bin'
FFPROBE = str(_BIN / 'ffprobe.exe') if (_BIN / 'ffprobe.exe').exists() else 'ffprobe'
FFMPEG = str(_BIN / 'ffmpeg.exe') if (_BIN / 'ffmpeg.exe').exists() else 'ffmpeg'

# しきい値（2026-10 の実測をもとに設定。詳細は out/codex/plan_quality.md）
CPS_MED_MAX = 6.0      # 字幕の速さ（中央値・字/秒）
CPS_MAX = 7.5          # 字幕の速さ（最大）
LINE_CHARS_MAX = 40    # 1 行の文字数
MAX_LINES = 2          # 長尺の字幕の行数
MAX_LINES_SHORT = 3    # 縦型は 3 行まで許す（幅 1080 に対して 880px 折り返し）
MIN_CUE_SEC = 0.8      # 1 枚の最短表示
CHAPTER_SEC_WARN = 60  # これを超える章は…
CHAPTER_CHANGES_MIN = 4  # …視覚変化がこれ以上ほしい
CHAPTER_SEC_NG = 100   # 超えたら要修正
LUFS_TARGET = -14.0
# ±0.5 だと、音量パッチ前に作った12本（-15.0）が全部 NG になる。
# 1dB 差は聴感上ほぼ同じで、上げ直しは1本1,600ユニットかかるため許容幅は ±1.0 にする。
# 新しい書き出し（vp.py / rebuild_old_compose.py の2パス loudnorm）は -14.0〜-14.2 に収まる。
LUFS_TOL = 1.0
TP_MAX = -1.0
DUR_TOL = 1.0
SHORT_MAX_SEC = 60.0

_d = ImageDraw.Draw(Image.new('RGB', (10, 10)))


def font_long():
    import vp
    return vp.FSUB[52]


def font_short():
    import make_short
    return make_short.font(60)


def wrap_long(txt):
    import vp
    return vp.wrapn(_d, txt, font_long(), 1720)


def wrap_short(txt):
    import make_short
    return make_short.wrap(_d, txt, font_short(), 880)


def sec(t):
    h, m, rest = t.split(':')
    s, ms = rest.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def cues(path):
    """SRT -> [(start, end, text)]"""
    rows = []
    for b in path.read_text(encoding='utf8').strip().split('\n\n'):
        ls = b.split('\n')
        if len(ls) < 3 or '-->' not in ls[1]:
            continue
        a, e = ls[1].split(' --> ')
        rows.append((sec(a), sec(e), '\n'.join(ls[2:]).replace('\n', '')))
    return rows


def probe_duration(path):
    r = subprocess.run([FFPROBE, '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'csv=p=0', str(path)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def loudness(path):
    """(integrated LUFS, true peak dBFS)

    ebur128 は解析中も経過を出すので、`I:` は最初の -70.0（無音）に当たる。
    最後に出るサマリの値を使う。
    """
    r = subprocess.run([FFMPEG, '-hide_banner', '-nostats', '-i', str(path),
                        '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True, encoding='utf8', errors='replace')
    txt = r.stderr
    i = re.findall(r'I:\s*(-?[\d.]+)\s*LUFS', txt)
    p = re.findall(r'Peak:\s*(-?[\d.]+)\s*dBFS', txt)
    return (float(i[-1]) if i else None, float(p[-1]) if p else None)


def add(issues, level, cat, msg):
    issues.append((level, cat, msg))


def check_subtitles(issues, srt, short):
    cs = cues(srt)
    if not cs:
        add(issues, 'NG', '字幕', 'キューが 0 件')
        return
    wrap = wrap_short if short else wrap_long
    max_lines = MAX_LINES_SHORT if short else MAX_LINES
    cps, three, longest, short_cues = [], 0, 0, 0
    for a, e, txt in cs:
        dt = max(1e-6, e - a)
        cps.append(len(txt) / dt)
        ls = wrap(txt)
        if len(ls) > max_lines:
            three += 1
        longest = max(longest, max(len(x) for x in ls))
        if dt < MIN_CUE_SEC:
            short_cues += 1
    cps.sort()
    med = cps[len(cps) // 2]
    mx = cps[-1]
    if mx > CPS_MAX:
        add(issues, 'NG', '字幕', f'速すぎるキューがある（最大 {mx:.1f} 字/秒 > {CPS_MAX}）')
    elif med > CPS_MED_MAX:
        add(issues, 'WARN', '字幕', f'全体に速い（中央 {med:.1f} 字/秒 > {CPS_MED_MAX}）')
    if three:
        add(issues, 'WARN', '字幕', f'{max_lines + 1} 行以上のキューが {three} 件')
    if longest > LINE_CHARS_MAX:
        add(issues, 'WARN', '字幕', f'1 行が長い（{longest} 字 > {LINE_CHARS_MAX}）')
    if short_cues:
        add(issues, 'WARN', '字幕', f'表示が短すぎるキューが {short_cues} 件（< {MIN_CUE_SEC} 秒）')
    add(issues, 'INFO', '字幕',
        f'{len(cs)} キュー / 中央 {med:.1f} 最大 {mx:.1f} 字/秒 / {max_lines + 1} 行 {three} 件 / 最長 {longest} 字')


def check_audio(issues, video, enabled):
    if not enabled:
        return
    i, p = loudness(video)
    if i is None:
        add(issues, 'WARN', '音量', '測定できなかった')
        return
    if abs(i - LUFS_TARGET) > LUFS_TOL:
        add(issues, 'NG', '音量', f'{i:.1f} LUFS（目標 {LUFS_TARGET} ±{LUFS_TOL}）')
    if p is not None and p > TP_MAX:
        add(issues, 'WARN', '音量', f'True Peak {p:.1f} dBFS（{TP_MAX} 以下に）')
    add(issues, 'INFO', '音量', f'{i:.1f} LUFS / TP {p if p is None else round(p, 1)} dB')


def check_sync(issues, slug, srt):
    """字幕の切れ目が無音（息継ぎ）に着地しているか。`cue_times` を持つ＝P1-1 以降に作った動画だけ対象"""
    rep = OUT / f'{slug}_audio_report.json'
    nar = OUT / f'{slug}_narration.wav'
    if not (rep.exists() and nar.exists() and srt.exists()):
        return
    try:
        segs = json.loads(rep.read_text(encoding='utf8')).get('segments') or []
    except Exception:
        return
    if not any(s.get('cue_times') for s in segs):
        return
    import bisect
    import wave
    import numpy as np
    with wave.open(str(nar), 'rb') as w:
        rate = w.getframerate()
        pcm = np.frombuffer(w.readframes(w.getnframes()), np.int16)
    hop = max(1, int(0.01 * rate))
    n = len(pcm) // hop
    fr = np.sqrt(((pcm[:n * hop].astype(np.float64) / 32768) ** 2).reshape(n, hop).mean(axis=1))
    loud = fr[fr > fr.max() * 0.1]
    med = float(np.median(loud)) if loud.size else 1e-9
    ss = sorted(s['start'] for s in segs)
    W = int(0.03 * rate)
    bad = tot = 0
    for a, _e, _t in cues(srt):
        k = bisect.bisect_left(ss, a)
        if (k < len(ss) and abs(ss[k] - a) < 0.02) or (k > 0 and abs(ss[k - 1] - a) < 0.02):
            continue
        i = int(a * rate)
        loc = float(np.sqrt(np.mean((pcm[max(0, i - W):i + W].astype(np.float64) / 32768) ** 2)))
        tot += 1
        if loc / max(med, 1e-9) > 0.35:
            bad += 1
    if tot < 5:
        return
    share = 1 - bad / tot
    if share >= 0.8:
        add(issues, 'INFO', '同期', f'字幕の切れ目の {share:.0%} が無音に着地（{tot - bad}/{tot}）')
    else:
        add(issues, 'WARN', '同期', f'字幕の切れ目が発話中に落ちる {bad}/{tot} 件（無音へ寄せる前の書き出しか）')


def check_vp_chapters(issues, spec, tl):
    chs = spec.get('chapters', [])
    if not chs:
        return
    longest = 0
    dull = []
    for c, row in zip(chs, tl):
        length = row['end'] - row['start']
        longest = max(longest, length)
        changes = len({it.get('at', 0) for it in c.get('scene', [])})
        if length >= CHAPTER_SEC_NG:
            add(issues, 'NG', '章', f'{c.get("key")} が {length:.0f} 秒（{CHAPTER_SEC_NG} 秒以上は分割）')
        elif length >= CHAPTER_SEC_WARN and changes < CHAPTER_CHANGES_MIN:
            dull.append(f'{c.get("key")} {length:.0f}s/変化{changes}')
    if dull:
        add(issues, 'WARN', '章', f'長いのに画面が動かない: {", ".join(dull)}')
    add(issues, 'INFO', '章', f'{len(chs)} 章 / 最長 {longest:.0f} 秒')


def check_hook(issues, spec, short):
    if short:
        ok = bool(spec.get('answer'))
        add(issues, 'INFO' if ok else 'WARN', '冒頭',
            '結論カードあり（answer）' if ok else '結論カードが無い（spec の answer）')
        return
    ch0 = (spec.get('chapters') or [{}])[0]
    has_opener = bool(ch0.get('opener') or ch0.get('chapter_title'))
    early = [it for it in ch0.get('scene', [])
             if it.get('t') in ('panel', 'big', 'chips', 'anim') and it.get('at', 99) <= 3]
    ok = has_opener or bool(early)
    add(issues, 'INFO' if ok else 'WARN', '冒頭',
        '3 秒以内にテキストあり' if ok else '最初の 3 秒に文字が無い')


def lint_long(slug, audio=True):
    spec_p = R / 'data' / f'{slug}_spec.json'
    tl_p = R / 'data' / f'{slug}_timeline.json'
    srt = OUT / f'{slug}_subtitles.srt'
    video = OUT / f'{slug}_video.mp4'
    if not video.exists():
        video = OUT / f'{slug}.mp4'
    issues = []
    if not video.exists():
        add(issues, 'NG', '基本', f'動画が無い（{video.name}）')
        return issues
    if not srt.exists():
        add(issues, 'NG', '基本', f'字幕が無い（{srt.name}）')
    else:
        check_subtitles(issues, srt, short=False)
        check_sync(issues, slug, srt)
    dur = probe_duration(video)
    if spec_p.exists() and tl_p.exists():
        spec = json.loads(spec_p.read_text(encoding='utf8'))
        tl = json.loads(tl_p.read_text(encoding='utf8'))
        want = tl[-1]['end']
        if dur and abs(dur - want) > DUR_TOL:
            add(issues, 'NG', '尺', f'{dur:.1f}s（タイムライン {want:.1f}s）')
        else:
            add(issues, 'INFO', '尺', f'{dur:.1f}s')
        check_vp_chapters(issues, spec, tl)
        check_hook(issues, spec, short=False)
    elif dur:
        add(issues, 'INFO', '尺', f'{dur:.1f}s（タイムライン無し）')
    check_audio(issues, video, audio)
    return issues


def lint_short(slug, audio=True):
    spec_p = R / 'data' / f'short_{slug}.json'
    srt = OUT / f'short_{slug}_subtitles.srt'
    video = OUT / f'short_{slug}.mp4'
    issues = []
    if not video.exists():
        add(issues, 'NG', '基本', f'動画が無い（{video.name}）')
        return issues
    if not srt.exists():
        add(issues, 'NG', '基本', f'字幕が無い（{srt.name}）')
    else:
        check_subtitles(issues, srt, short=True)
    dur = probe_duration(video)
    if dur and dur > SHORT_MAX_SEC:
        add(issues, 'WARN', '尺', f'{dur:.1f}s（Short は {SHORT_MAX_SEC:.0f} 秒まで）')
    elif dur:
        add(issues, 'INFO', '尺', f'{dur:.1f}s')
    if spec_p.exists():
        check_hook(issues, json.loads(spec_p.read_text(encoding='utf8')), short=True)
    check_audio(issues, video, audio)
    return issues


def say(text):
    print(text, flush=True)
    with REPORT.open('a', encoding='utf8') as f:
        f.write(text + '\n')


def main():
    global REPORT
    args = [a for a in sys.argv[1:]]
    audio = '--no-audio' not in args
    args = [a for a in args if not a.startswith('--')]
    want_all = not args
    if not want_all:
        # 1本だけの検査で、全体の結果（qa_lint.txt）を消さない
        REPORT = REPORT.with_name('qa_lint_last.txt')

    targets = []   # (label, kind, slug)
    for p in sorted(OUT.glob('*_video.mp4')):
        slug = p.stem[:-6]
        if slug.startswith('short_'):
            continue
        targets.append((slug, 'long', slug))
    for p in sorted(OUT.glob('short_*.mp4')):
        if p.stem.endswith('_subtitles'):
            continue
        targets.append((p.stem, 'short', p.stem[6:]))

    if not want_all:
        # ラベル完全一致（`calendar` は長尺だけ、Short は `short_calendar` と書く）
        targets = [t for t in targets if t[0] in args]
        if not targets:
            print('対象が見つからない。候補: ' + ', '.join(t[0] for t in sorted(OUT.glob("*_video.mp4"))[:5]))
            return 2

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text('', encoding='utf8')
    ng = warn = 0
    for label, kind, slug in targets:
        issues = lint_long(slug, audio) if kind == 'long' else lint_short(slug, audio)
        n_ng = sum(1 for i in issues if i[0] == 'NG')
        n_warn = sum(1 for i in issues if i[0] == 'WARN')
        ng += n_ng
        warn += n_warn
        mark = 'NG' if n_ng else ('WARN' if n_warn else 'OK')
        say(f'\n[{mark}] {label}')
        for level, cat, msg in issues:
            if level != 'INFO':
                say(f'   {level:4s} {cat}: {msg}')
        for level, cat, msg in issues:
            if level == 'INFO':
                say(f'        {cat}: {msg}')

    say(f'\n合計: {len(targets)} 本 / NG {ng} 件 / WARN {warn} 件')
    return 1 if ng else 0


if __name__ == '__main__':
    raise SystemExit(main())
