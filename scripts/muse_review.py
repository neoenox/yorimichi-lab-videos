"""Muse(Meta AI, https://muse.ai/) に動画を送ってレビューを受ける。1コマンドで完結する。

  1回の実行で「Chrome の確認(無ければ起動) → 360p圧縮 → 添付 → 依頼文 → 送信 → 返答待ち → 保存」まで行う。
  ステップごとにプロセスを起動し直さない・固定の sleep を入れないことで、待ち時間を縮める。

  python scripts/muse_review.py <slug> --video out/short_<slug>.mp4 [--note "追記"] [--dry-run] [--timeout 900]

  --dry-run は送信の直前で止める（添付と入力の確認だけ）。
  返答は out/muse_reply_<slug>.txt に保存する。圧縮ファイルは E:/rekishikaisetu/sigcmp_view/ に置く
  （Chrome の file_upload は作業フォルダの外を受け付けないため）。
"""
import argparse
import atexit
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
sys.stdout.reconfigure(encoding='utf8')

ROOT = Path(__file__).resolve().parents[1]
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
PROFILE = r'C:\Users\neoen\.chrome-automation'
CDP_PORT = 9222
VIEW = Path('E:/rekishikaisetu/sigcmp_view')
MUSE_MARK = '問題点は時刻つきで具体的にお願いします。'
TEXTBOX = '[contenteditable=true], textarea, [role=textbox]'   # Muse は contenteditable とは限らない（実測: textarea か role=textbox）
FFMPEG = shutil.which('ffmpeg') or r'C:\Users\neoen\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe'
LAUNCHED = []   # このスクリプトが起動した Chrome のプロセス（終了時に閉じる）

TEMPLATE = ('この動画のレビューをお願いします。添付は、{topic}のYouTube Shorts(約{sec}秒)です。'
            '背景は{background}で、概要欄に出典とAI生成の明示を書きます。{notes}'
            'まず、ナレーションを文字に書き起こしてください(台本と照合します)。'
            '見てほしい点は、(1)字幕と音声の一致、(2)読み間違い・音割れ・無音、(3)文字の重なり・はみ出し・見切れ、'
            '(4)事実関係と日付、(5)冒頭1〜3秒の引き、(6)AI映像の不自然さ、(7)公開してよいか。'
            + MUSE_MARK)


def port_open(port, timeout=1.0):
    try:
        socket.create_connection(('127.0.0.1', port), timeout).close()
        return True
    except Exception:
        return False


def ensure_chrome():
    """CDP の Chrome が無ければ起動する。DSH の再起動で落ちていても、ここで立て直す。

    自分で起動したときは、プロセスを LAUNCHED に控えておき、終了時に閉じる
    （2026-11-16 ユーザー指示: ウィンドウが増えるのがイヤ。レビューが終わったら残さない）。
    """
    if port_open(CDP_PORT):
        return False
    proc = subprocess.Popen([CHROME, f'--remote-debugging-port={CDP_PORT}', f'--user-data-dir={PROFILE}',
                             'https://muse.ai/'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    LAUNCHED.append(proc)
    for _ in range(30):
        if port_open(CDP_PORT):
            return True
        time.sleep(1)
    raise SystemExit('Chrome(CDP %d) を起動できない。手で起動してから再実行する' % CDP_PORT)


def close_launched():
    """このスクリプトが起動した Chrome だけを閉じる（ユーザーのChromeには触らない）。"""
    for p in LAUNCHED:
        subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True)
    LAUNCHED.clear()


atexit.register(close_launched)


def compress(src, slug):
    VIEW.mkdir(parents=True, exist_ok=True)
    dst = VIEW / f'muse_{slug}.mp4'
    subprocess.run([FFMPEG, '-v', 'error', '-y', '-i', str(src), '-vf', 'scale=360:-2',
                    '-c:v', 'libx264', '-crf', '30', '-preset', 'fast', '-c:a', 'aac', '-b:a', '64k', str(dst)],
                   check=True)
    return dst


def probe_sec(path):
    out = subprocess.run([FFMPEG.replace('ffmpeg.exe', 'ffprobe.exe'), '-v', 'error', '-show_entries',
                          'format=duration', '-of', 'csv=p=0', str(path)], capture_output=True, text=True).stdout.strip()
    return round(float(out.split(',')[0])) if out else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slug')
    ap.add_argument('--video', required=True)
    ap.add_argument('--topic', default='')
    ap.add_argument('--background', default='AI生成映像')
    ap.add_argument('--notes', default='')
    ap.add_argument('--note', default='', help='依頼文に足す一文')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--timeout', type=int, default=900)
    a = ap.parse_args()

    from playwright.sync_api import sync_playwright

    started = ensure_chrome()
    note = (a.notes + (' ' if a.notes and a.note else '') + a.note).strip()
    msg = TEMPLATE.format(topic=a.topic or a.slug, sec=probe_sec(ROOT / a.video), background=a.background, notes=note)
    clip = compress(ROOT / a.video, a.slug)
    print('圧縮: %s (%.1f MB) / Chrome起動=%s' % (clip, clip.stat().st_size / 1e6, started))

    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(f'http://127.0.0.1:{CDP_PORT}')
        ctx = b.contexts[0]
        ctx.set_default_timeout(8000)   # 既定30秒の待ちで止まらないようにする
        pg = next((x for x in ctx.pages if 'muse.ai' in x.url), None) or ctx.new_page()
        if 'muse.ai' not in pg.url:
            pg.goto('https://muse.ai/', wait_until='domcontentloaded')
        pg.bring_to_front()
        if 'Chat' not in pg.title() and pg.locator(TEXTBOX).count() == 0:
            raise SystemExit('Muse にログインしていない（この Chrome のプロファイルで手でログインする）')

        pg.locator('input[type=file]').first.set_input_files(str(clip))
        box = pg.locator(TEXTBOX).first
        box.click()
        # 前回の下書きが残っていることがある（dry-run の後など）。先に空にしてから入力する
        pg.keyboard.press('Control+a')
        pg.keyboard.press('Delete')
        pg.wait_for_timeout(150)
        pg.keyboard.insert_text(msg)
        got = box.input_value() if box.evaluate('e => e.tagName === "TEXTAREA"') else box.inner_text()
        print('入力 %d 文字 (末尾: %s)' % (len(got), got[-16:]))
        if len(got) != len(msg):
            raise SystemExit('入力欄の文字数が合わない（%d != %d）。送信しない' % (len(got), len(msg)))
        if a.dry_run:
            pg.screenshot(path=str(ROOT / 'out' / f'muse_{a.slug}_dryrun.png'))
            print('--dry-run: 送信しない')
            return

        # 送信: Enter を押し、入力欄が空になったかで「送れた」ことを確かめる（2026-11-16: 送信ボタン頼みで失敗した）
        box.click()
        pg.keyboard.press('Enter')
        pg.wait_for_timeout(2500)
        free = pg.evaluate("""() => { const el = document.querySelector('[contenteditable=true], textarea');
            if (!el) return -1; return (el.tagName === 'TEXTAREA' ? el.value : el.innerText).trim().length; }""")
        if free not in (0, -1):
            sb = pg.locator('button[aria-label]').filter(has_text=re.compile('送信|Send')).first
            if sb.count():
                sb.click()
            else:
                bb = box.bounding_box()
                pg.mouse.click(bb['x'] + bb['width'] + 62, bb['y'] + bb['height'] - 18)
            pg.wait_for_timeout(2500)
            free = pg.evaluate("""() => { const el = document.querySelector('[contenteditable=true], textarea');
                if (!el) return -1; return (el.tagName === 'TEXTAREA' ? el.value : el.innerText).trim().length; }""")
        if free not in (0, -1):
            pg.screenshot(path=str(ROOT / 'out' / f'muse_{a.slug}_sendfail.png'))
            raise SystemExit('送信できていない（入力欄に文字が残っている）。スクリーンショット: out/muse_%s_sendfail.png' % a.slug)
        print('送信した。返答を待つ（最大 %d 秒）' % a.timeout)

        t0 = time.time()
        reply, last = '', None
        while time.time() - t0 < a.timeout:
            # チャット本文だけを読む（ページ全体だと、送信した自分の文に含まれる目印の後ろ＝サイドバーを拾ってしまう）
            log = pg.locator('[role=log]').first
            txt = log.inner_text() if log.count() else pg.inner_text('body')
            i = txt.rfind(MUSE_MARK)
            reply = txt[i + len(MUSE_MARK):] if i >= 0 else ''
            if len(reply.strip()) > 200 and reply == last and 'レビュー中' not in reply:
                break
            last = reply
            time.sleep(5)   # 手順書の30秒より短く（ページ取得は0.02秒なので安い）
        out = ROOT / 'out' / f'muse_reply_{a.slug}.txt'
        out.write_text(reply, encoding='utf8')
        pg.screenshot(path=str(ROOT / 'out' / f'muse_reply_{a.slug}.png'))
        print('返答 %d 文字 (%.0f秒) -> %s' % (len(reply), time.time() - t0, out))


if __name__ == '__main__':
    main()
