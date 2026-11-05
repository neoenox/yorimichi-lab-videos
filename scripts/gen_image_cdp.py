"""ChatGPT(web) で画像を生成し、保存する（Chrome を CDP で操作）。

前提:
    ・Chrome を自動化プロファイルで起動しておく:
        chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\\Users\\<user>\\.chrome-automation
    ・そのウィンドウで ChatGPT にログイン済み（初回だけ。以降はプロファイルに保持される）
    ・pip install playwright（ブラウザ本体は不要。既存 Chrome に接続するだけ）

usage:
    python scripts/gen_image_cdp.py --prompt "縦長9:16、濃紺の背景に筆と硯、文字なし" \
        --out assets/<slug>/gen_base.png
    python scripts/gen_image_cdp.py --check          # 接続とログイン状態の確認だけ
"""
import argparse
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

CDP = 'http://127.0.0.1:9222'

COMPOSER = '#prompt-textarea, div[contenteditable="true"]'
SEND = 'button[data-testid="send-button"], button[aria-label*="Send"], button[aria-label*="送信"]'


def cdp_alive():
    try:
        with urllib.request.urlopen(CDP + '/json/version', timeout=5) as r:
            return True
    except Exception:
        return False


def find_page(browser):
    for ctx in browser.contexts:
        for pg in ctx.pages:
            if 'chatgpt.com' in (pg.url or ''):
                return pg
    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    return ctx.new_page()


def logged_in(page):
    if 'auth' in page.url or 'accounts.google.com' in page.url:
        return False
    try:
        page.wait_for_selector(COMPOSER, timeout=8000)
        return True
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser(description='ChatGPT(web) で画像生成（CDP）')
    ap.add_argument('--prompt')
    ap.add_argument('--out')
    ap.add_argument('--timeout', type=int, default=240)
    ap.add_argument('--check', action='store_true', help='接続とログイン状態の確認だけ')
    ap.add_argument('--reuse', action='store_true', help='送信せず、いま開いているページの画像を保存する')
    a = ap.parse_args()

    if not cdp_alive():
        raise SystemExit(
            'CDP に接続できません。Chrome を次のように起動してください:\n'
            '  chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\\Users\\<user>\\.chrome-automation')

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = find_page(browser)
        page.bring_to_front()
        if 'chatgpt.com' not in (page.url or ''):
            page.goto('https://chatgpt.com/', wait_until='domcontentloaded')
        ok = logged_in(page)
        print('url:', page.url)
        print('logged_in:', ok)
        if a.check or not ok:
            if not ok:
                print('未ログインです。開いている Chrome で ChatGPT にログインしてください。')
            return 0 if ok else 2
        if not a.out:
            raise SystemExit('--out が必要です')
        if not a.reuse and not a.prompt:
            raise SystemExit('--prompt が必要です')

        if a.reuse:
            print('reuse: いま開いているページから画像を取得します')
        else:
            page.goto('https://chatgpt.com/?q=' + urllib.parse.quote(a.prompt), wait_until='domcontentloaded')
            page.wait_for_selector(COMPOSER, timeout=20000)
            page.wait_for_timeout(1500)
            try:
                page.click('button[data-testid="send-button"]', timeout=8000)
            except Exception:
                try:
                    page.click('button[aria-label*="送信"]', timeout=6000)
                except Exception:
                    page.keyboard.press('Enter')
            print('sent; waiting for image...')

        deadline = time.time() + a.timeout
        src = None
        while time.time() < deadline:
            srcs = page.eval_on_selector_all(
                'img',
                'els => els.map(e => e.currentSrc || e.src || "").filter(s => s && (s.startsWith("blob:") || s.includes("oaiusercontent") || s.includes("estuary")))')
            if srcs:
                src = srcs[-1]
                break
            page.wait_for_timeout(4000)
        if not src:
            raise SystemExit('画像が生成されませんでした（timeout %ds）' % a.timeout)
        print('image:', src[:80])

        # blob: はページ内で canvas 経由で取り出す（同一オリジンなので確実）
        data_url = page.evaluate(
            """async (u) => {
                 const img = Array.from(document.querySelectorAll('img'))
                   .find(e => (e.currentSrc || e.src) === u);
                 if (!img) return null;
                 if (!img.complete) { await new Promise(r => { img.onload = r; img.onerror = r; }); }
                 const c = document.createElement('canvas');
                 c.width = img.naturalWidth || img.width;
                 c.height = img.naturalHeight || img.height;
                 c.getContext('2d').drawImage(img, 0, 0);
                 return c.toDataURL('image/png');
               }""", src)
        if not data_url:
            raise SystemExit('画像データを取り出せませんでした')

        import base64
        raw = base64.b64decode(data_url.split(',', 1)[1])
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_suffix('.download')
        tmp.write_bytes(raw)
        from PIL import Image
        Image.open(tmp).convert('RGB').save(out)
        tmp.unlink()
        print('saved', out, out.stat().st_size, 'bytes')
    return 0


if __name__ == '__main__':
    sys.exit(main())
