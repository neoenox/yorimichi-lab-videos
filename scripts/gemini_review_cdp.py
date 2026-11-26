"""Gemini(web) に動画を添付してレビュー依頼を送る（CDP + Playwright）。

前提:
    Chrome を自動化プロファイルで起動しておく:
        chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\\Users\\<user>\\.chrome-automation
    そのプロファイルで gemini.google.com にログイン済み（初回のみ手動）。

usage:
    python scripts/gemini_review_cdp.py --video <mp4> --prompt <file>
    python scripts/gemini_review_cdp.py --check   # 接続とログイン状態の確認だけ
"""
import argparse
import sys
import time
from pathlib import Path

CDP = 'http://127.0.0.1:9222'
COMPOSER = 'div[contenteditable="true"], textarea[aria-label*="プロンプト"]'
SEND = 'button[aria-label*="送信"], button[data-testid*="send"], button[aria-label*="Send"]'
# Gemini の動画受け付け input。accept に video/* を含むものを優先する。
VIDEO_INPUT = 'input[type="file"][accept*="video"]'


def find_page(browser):
    for ctx in browser.contexts:
        for pg in ctx.pages:
            if 'gemini.google.com' in (pg.url or ''):
                return pg
    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    return ctx.new_page()


def main():
    ap = argparse.ArgumentParser(description='Gemini(web) へ動画レビュー依頼（CDP）')
    ap.add_argument('--video', required=True)
    ap.add_argument('--prompt', required=True)
    ap.add_argument('--timeout', type=int, default=240)
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = find_page(browser)
        page.bring_to_front()
        if 'gemini.google.com' not in (page.url or ''):
            page.goto('https://gemini.google.com/app', wait_until='domcontentloaded')
        page.wait_for_timeout(2500)

        logged_in = False
        try:
            page.wait_for_selector(COMPOSER, timeout=15000)
            logged_in = True
        except Exception:
            pass
        print('url:', page.url)
        print('logged_in:', logged_in)
        if a.check or not logged_in:
            if not logged_in:
                print('NOT_LOGGED_IN: 自動化プロファイルで gemini.google.com にログインしてください')
            return 0 if logged_in else 2

        # 既存の添付を消す（無い場合は無視）
        try:
            for btn in page.query_selector_all('button[aria-label*="添付ファイルを閉じる"]'):
                btn.click(timeout=2000)
        except Exception:
            pass

        video = Path(a.video)
        if not video.is_file():
            raise SystemExit('video not found: %s' % video)

        # input は動的に生成されることがある。メニューを開いてから探す。
        for _ in range(3):
            inputs = page.query_selector_all('input[type="file"]')
            if any('video' in (e.get_attribute('accept') or '') for e in inputs):
                break
            trigger = page.query_selector('button[aria-label*="アップロードとツール"]')
            if trigger:
                try:
                    trigger.click(timeout=3000)
                except Exception:
                    pass
            page.wait_for_timeout(1200)

        # 動画 input に直接ファイルを設定（UI のファイルダイアログを経由しない）
        inp = None
        inputs = page.query_selector_all('input[type="file"]')
        print('file_inputs:', len(inputs),
              [e.get_attribute('accept') for e in inputs])
        try:
            inp = page.wait_for_selector(VIDEO_INPUT, timeout=10000, state='attached')
        except Exception:
            for el in inputs:
                accept = el.get_attribute('accept') or ''
                if 'video' in accept:
                    inp = el
                    break
        if inp is None:
            raise SystemExit('video file input not found')
        inp.set_input_files(str(video))
        print('attached:', video.name, video.stat().st_size, 'bytes')

        # 添付の処理完了を待つ（「読み込んでいます」が消えるまで）
        deadline = time.time() + 120
        while time.time() < deadline:
            loading = page.query_selector('button:has-text("読み込んでいます")')
            if loading is None:
                break
            page.wait_for_timeout(1000)

        composer = page.wait_for_selector(COMPOSER, timeout=15000)
        prompt_text = Path(a.prompt).read_text(encoding='utf-8')
        composer.fill(prompt_text)
        page.wait_for_timeout(500)

        sent = False
        for sel in [
            'button[aria-label*="プロンプトを送信"]',
            'button[aria-label*="送信"]',
            'button[data-testid*="send"]',
        ]:
            btn = page.query_selector(sel)
            if btn and btn.is_enabled():
                btn.click()
                sent = True
                break
        if not sent:
            composer.press('Enter')
            sent = True
        print('sent: True')

        # 応答が完全に出るまで待つ（生成中は「停止」ボタンが出る）
        deadline = time.time() + a.timeout
        text = ''
        stable = 0
        prev_len = -1
        while time.time() < deadline:
            page.wait_for_timeout(2500)
            bodies = page.query_selector_all('model-response')
            if not bodies:
                continue
            cur = bodies[-1].inner_text()
            generating = bool(page.query_selector('button[aria-label*="応答を停止"], button[data-testid*="stop"]'))
            if cur == prev_len and not generating and len(cur.strip()) > 200:
                stable += 1
            else:
                stable = 0
            prev_len = cur
            if stable >= 2:
                text = cur
                break
        if not text:
            bodies = page.query_selector_all('model-response')
            text = bodies[-1].inner_text() if bodies else page.locator('body').inner_text()[-6000:]

        out = Path(a.prompt).with_suffix('.response.txt')
        out.write_text(text, encoding='utf-8')
        print('response_saved:', out)
        print('--- response ---')
        print(text[:6000])
    return 0


if __name__ == '__main__':
    sys.exit(main())
