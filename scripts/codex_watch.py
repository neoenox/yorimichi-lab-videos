"""Codex に「通し視聴」をしてもらう（動画を最初から最後まで、時刻つきの静止画・字幕・音声の測定値で確認）。
usage: python scripts/codex_watch.py <slug> [<theme_dir>]
  材料: out/<slug>_video.mp4 から 4秒おきの静止画（時刻入りのコンタクトシート）、字幕SRT、音声の測定値
  出力: out/<slug>_watch/（材料）、<theme_dir>/14_codex_watch.md（Codexの所見。theme_dir 省略時は out/<slug>_watch/codex_watch.md）
Codexは音を直接聞けない。音の確認は ffmpeg の測定値（ラウドネス・無音・ピーク）で代える。助言のみ。指摘は一次資料で裏取りしてから反映する。"""
import json, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
STEP = 4          # 秒
COLS, ROWS = 4, 4  # 1枚に16コマ（64秒分）
W, H = 480, 270


import os
VIDEO=os.environ.get('VIDEO');SRTP=os.environ.get('SRT');WIN=[float(x) for x in os.environ['WIN'].split(',')] if os.environ.get('WIN') else None;TAG=os.environ.get('TAG','')


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding='utf8', errors='replace')


def srt_cues(p):
    cues = []
    for blk in re.split(r'\n\s*\n', p.read_text(encoding='utf-8-sig').strip()):
        ln = blk.strip().splitlines()
        if len(ln) >= 3 and '-->' in ln[1]:
            a, b = [sum(float(x) * m for x, m in zip(t.replace(',', '.').split(':'), (3600, 60, 1))) for t in ln[1].split('-->')]
            cues.append((a, b, ''.join(ln[2:])))
    return cues


def frames(video, out):
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob('f_*.jpg'):
        f.unlink()
    a, b = sh(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=avg_frame_rate', '-of', 'csv=p=0', str(video)]).stdout.strip().split('/')
    n_step = round(float(a) / float(b) * STEP)  # fpsフィルタは時刻が約2秒ずれたので、フレーム番号で正確に選ぶ
    t0 = WIN[0] if WIN else 0.0
    ss = ['-ss', str(t0), '-t', str(WIN[1] - WIN[0])] if WIN else []
    sh(['ffmpeg', '-y'] + ss + ['-i', str(video), '-vf', f"select='not(mod(n,{n_step}))',scale={W}:{H}", '-fps_mode', 'vfr', '-q:v', '4', str(out / 'f_%04d.jpg')])
    fs = sorted(out.glob('f_*.jpg'))
    font = ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc', 22)
    n = COLS * ROWS
    sheets = []
    for si in range(0, len(fs), n):
        sheet = Image.new('RGB', (COLS * W, ROWS * H), 'black')
        d = ImageDraw.Draw(sheet)
        for k, f in enumerate(fs[si:si + n]):
            x, y = (k % COLS) * W, (k // COLS) * H
            sheet.paste(Image.open(f), (x, y))
            t = int(t0) + (si + k) * STEP
            d.rectangle([x, y, x + 92, y + 28], fill='black')
            d.text((x + 4, y + 1), f'{t // 60}:{t % 60:02d}', fill='yellow', font=font)
        p = out / f'watch_{si // n + 1:02d}.png'
        sheet.save(p)
        sheets.append(p)
    for f in fs:
        f.unlink()
    return sheets


def audio_report(video, srt, out):
    L = []
    dur = float(sh(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(video)]).stdout.strip())
    L.append(f'動画の長さ: {dur:.1f}秒')
    ss = ['-ss', str(WIN[0]), '-t', str(WIN[1] - WIN[0])] if WIN else []
    r = sh(['ffmpeg', '-nostats'] + ss + ['-i', str(video), '-af', 'ebur128=peak=true', '-f', 'null', '-']).stderr
    m = r[r.rfind('Summary:'):]
    L.append('ラウドネス(EBU R128) 抜粋:\n' + '\n'.join(x for x in m.splitlines() if re.search(r'I:|LRA:|Peak:', x)))
    r = sh(['ffmpeg', '-nostats'] + ss + ['-i', str(video), '-af', 'silencedetect=noise=-45dB:d=1.2', '-f', 'null', '-']).stderr
    sil = re.findall(r'silence_start: ([\d.]+)|silence_end: ([\d.]+) \| silence_duration: ([\d.]+)', r)
    ss = [a for a, b, c in sil if a]
    es = [(b, c) for a, b, c in sil if b]
    L.append('1.2秒以上の無音(-45dB以下): ' + (', '.join(f'{float(s):.1f}s〜{float(e):.1f}s({float(d):.1f}s)' for s, (e, d) in zip(ss, es)) or 'なし'))
    cues = srt_cues(srt)
    if WIN:
        cues = [c for c in cues if WIN[0] <= c[0] < WIN[1]]
    L.append(f'字幕: {len(cues)}件、最後の字幕の終了 {cues[-1][1]:.1f}s')
    fast = [(a, len(t) / max(b - a, .1), t) for a, b, t in cues if len(t) / max(b - a, .1) > 9.5]
    L.append('読む速さが 9.5字/秒 を超える字幕: ' + ('; '.join(f'{a:.1f}s {v:.1f}字/秒「{t[:24]}」' for a, v, t in fast) or 'なし'))
    long_ = [(a, len(t), t) for a, b, t in cues if len(t) > 42]
    L.append('42字を超える字幕: ' + ('; '.join(f'{a:.1f}s {n}字' for a, n, t in long_) or 'なし'))
    gaps = [(cues[i][1], cues[i + 1][0] - cues[i][1]) for i in range(len(cues) - 1) if cues[i + 1][0] - cues[i][1] > 2.0]
    L.append('字幕の途切れ(2秒超): ' + ('; '.join(f'{s:.1f}s〜(+{g:.1f}s)' for s, g in gaps) or 'なし'))
    (out / 'audio_report.txt').write_text('\n\n'.join(L), encoding='utf8')
    return cues


PROMPT = """あなたは、解説動画（YouTubeチャンネル「寄り道ラボ」、合成音声のナレーション＋図解）を、公開前に**最初から最後まで通して視聴する**査読者です。
**ファイルは変更せず、読むだけ**にしてください。結果は日本語で、重大度（高／中／低）の高い順に出してください。

【材料と、その使い方】添付ファイルの中身がすべてです。全部読んでから書いてください。
- {srt}：**字幕。ナレーションの読み上げそのもの（時刻つき）。ナレーションの正本はこれ。**
- {spec}：**画面の正本。**どの章に何が、どの時刻から、どの位置・大きさで出るかがJSONで書かれています。
- {script}
- {desc}：概要欄。
- {audio}：音声の測定値（ラウドネス、無音区間、字幕の読む速さ）。
- 添付画像 watch_01.png〜：動画を{step}秒おきに切り出した静止画。各コマの左上に動画の時刻（分:秒）。左上から右へ、上から下の順。
  **1コマは480×270に縮小されているので、画面の文字は読めません。**画像は「レイアウト・重なり・空白・同じ画面が長く続く区間」の確認にだけ使ってください。

【禁止（ここを外すと査読が無意味になります）】
- **画像から読み取れない文字を、推測で補わないこと。** 文面は必ず {srt} から引用してください。
- **{srt}・{spec}・台本のどこにも無い固有名詞・年号・事件を書かないこと。** 書く場合は、SRTの時刻と文面を引用して示してください。
- 確かめられないことは「未確認」と書いてください。自信のない読み取りを断定にしないこと。

動画の音は聞けません。音は測定値で判断してください。

【見てほしい点】
1. **時刻ごとの画面とナレーションの対応**：SRTの各時刻に、specのどの章の要素が出ているか。話と画面がずれている区間はないか。
2. **画面の不具合**：文字のはみ出し・欠け・重なり、小さすぎる文字、真っ黒・空白のコマ、同じ画面が長く続いて動きがない区間。
3. **ナレーションの正しさ**：事実関係、数字、年号、固有名詞。根拠より強い断定。画面の数字（spec）と字幕の数字（SRT）の不一致。
4. **音声**：測定値から、音量不足・超過、不自然な無音、冒頭と末尾の余白の問題。
5. **字幕**：長すぎる・読む速さが速すぎる字幕、誤字、画面の文字との重複。
6. **公開してよいか**：上を総合して、「公開してよい／直せば公開してよい／公開不可」の3段階で判定し、直すべき点を優先順に挙げる。

出力形式：先頭に判定。その後、指摘ごとに「重大度／時刻／**根拠にしたファイルと引用**／問題／直し案」。最後に、確認した範囲（見たシート数と、読んだファイル名）を書く。問題がなければ「指摘なし」。
"""


def main():
    slug = sys.argv[1]
    theme = sys.argv[2] if len(sys.argv) > 2 else None
    video = Path(VIDEO) if VIDEO else ROOT / 'out' / f'{slug}_video.mp4'
    srt = Path(SRTP) if SRTP else ROOT / 'out' / f'{slug}_subtitles.srt'
    work = ROOT / 'out' / f'{slug}{TAG}_watch'
    work.mkdir(parents=True, exist_ok=True)
    sheets = frames(video, work)
    audio_report(video, srt, work)
    spec = ROOT / 'data' / f'{slug}_spec.json'
    desc = ROOT / 'out' / f'{slug}_description.md'
    mats = [srt, work / 'audio_report.txt']          # 正本（字幕）と音声の測定値は必ず渡す
    script = '（台本ファイルなし。字幕を台本として扱う）'
    if theme and (ROOT / 'docs' / 'themes' / theme / '09_script_v2.md').exists():
        td = ROOT / 'docs' / 'themes' / theme
        script = f'docs/themes/{theme}/09_script_v2.md（最終台本）と docs/themes/{theme}/08_fact_check.md（事実確認の記録）'
        mats += [td / '09_script_v2.md', td / '08_fact_check.md']
    script += os.environ.get('EXTRA', '')
    if spec.exists():
        mats.append(spec)                            # 画面の正本（どの時刻に何が出るか）
    if desc.exists():
        mats.append(desc)
    mats = [m for m in mats if m.exists()]
    prompt = PROMPT.format(step=STEP, srt=srt.relative_to(ROOT).as_posix(),
                           audio=(work / 'audio_report.txt').relative_to(ROOT).as_posix(), script=script,
                           spec=spec.relative_to(ROOT).as_posix() if spec.exists() else '（なし）',
                           desc=desc.relative_to(ROOT).as_posix() if desc.exists() else '（なし）')
    out = (ROOT / 'docs' / 'themes' / theme / f'14_codex_watch{TAG}.md') if theme else work / 'codex_watch.md'
    cmd = ['codex', 'exec', '-s', 'read-only', '--skip-git-repo-check', '-C', str(ROOT), '-o', str(out)]
    for s in sheets:
        cmd += ['-i', str(s)]
    cmd.append('-')
    if os.environ.get('REVIEWER') == 'opencode':  # Codex が使えないときの代替（環境変数 MODEL で指定。画像を読めるモデルが必要）
        prompt += (f'\n\n【出力】所見は {out.relative_to(ROOT).as_posix()} に書き出してください。'
                   'このファイル以外は、作成も変更もしないでください。')
        cmd = ['opencode.cmd', 'run', '-m', os.environ.get('MODEL', 'opencode/nemotron-3.5-super-vl-free'), '--auto']
        for m in mats:          # 正本（字幕SRT・仕様JSON・台本・概要欄・音声の測定値）を先に添付する。
            cmd += ['-f', str(m)]   # これが無いとモデルは低解像度の画から文字を拾おうとして推測で埋める
        for sh_ in sheets:
            cmd += ['-f', str(sh_)]
        cmd.append(prompt)
        before = out.stat().st_mtime if out.exists() else None
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=str(ROOT), timeout=5400)
        txt = r.stdout.decode('utf8', 'replace')
        log = ROOT / 'out' / 'codex' / f'{slug}{TAG}_watch_oc.log'
        log.parent.mkdir(exist_ok=True, parents=True)
        log.write_text(txt, encoding='utf8')
        after = out.stat().st_mtime if out.exists() else None
        if after and after != before:
            print(slug, 'sheets', len(sheets), 'opencode ->', out, '(written by the reviewer)')
        else:
            clean = re.sub(r'\x1b\[[0-9;]*m', '', txt)
            body = '\n'.join(l for l in clean.splitlines() if not l.startswith(('> ', '$ ', '→ '))).strip()
            if r.returncode == 0 and len(body) > 200:
                out.write_text(body + '\n', encoding='utf8')
                print(slug, 'sheets', len(sheets), 'opencode ->', out, '(from stdout)')
            else:
                print(slug, 'sheets', len(sheets), 'opencode exit', r.returncode, 'NO OUTPUT (see', log, ')', txt[-300:])
        return
    log = ROOT / 'out' / 'codex' / f'{slug}{TAG}_watch.log'
    log.parent.mkdir(exist_ok=True, parents=True)
    with log.open('wb') as lf:
        r = subprocess.run(cmd, input=prompt.encode('utf8'), stdout=lf, stderr=subprocess.STDOUT, cwd=str(ROOT))
    print(slug, 'sheets', len(sheets), 'exit', r.returncode, '->', out if out.exists() else 'NO OUTPUT (see ' + str(log) + ')')


if __name__ == '__main__':
    main()
