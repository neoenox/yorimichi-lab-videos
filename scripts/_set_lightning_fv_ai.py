"""DvZPhYeA8hQ の「AIの使用」を studio の詳細設定で確認・設定する。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from playwright.sync_api import sync_playwright

VIDEO = 'DvZPhYeA8hQ'
CHANNEL = 'UCN_do9fcssctmkrNsRWOO9A'

with sync_playwright() as pw:
    browser = pw.chromium.connect_over_cdp('http://127.0.0.1:9222')
    ctx = browser.contexts[0]
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    # チャンネルは studio_cdp.py check で UCN_do9fcssctmkrNsRWOO9A を確認済み
    page.goto(f'https://studio.youtube.com/video/{VIDEO}/edit', wait_until='domcontentloaded')
    page.wait_for_timeout(7000)
    # 詳細設定を開く
    try:
        page.locator('button[aria-label="詳細設定を表示"]').first.click(timeout=15000)
    except Exception as e:
        print('すべて表示ボタンが見つからない:', str(e)[:200])
    page.wait_for_timeout(1500)
    radios = page.evaluate("""() => [...document.querySelectorAll('tp-yt-paper-radio-button')]
        .filter(e => /^(はい|いいえ)$/.test(e.innerText.trim()))
        .map(e => ({name: e.getAttribute('name'), checked: e.getAttribute('aria-checked'), text: e.innerText.trim()}))""")
    print('radios before:', radios)
    yes = [r for r in radios if r['name'] == 'VIDEO_HAS_ALTERED_CONTENT_YES']
    if not yes:
        print('AI使用のラジオが見つからない。保存しない。')
    elif yes[0]['checked'] == 'true':
        print('AIの使用は既に「はい」')
    else:
        page.evaluate("""() => { const e = [...document.querySelectorAll('tp-yt-paper-radio-button')]
            .find(x => x.getAttribute('name') === 'VIDEO_HAS_ALTERED_CONTENT_YES'); e.click(); }""")
        page.wait_for_timeout(1000)
        page.get_by_role('button', name='保存').click(timeout=15000)
        page.wait_for_timeout(4000)
        print('AIの使用を「はい」にして保存した')
    after = page.evaluate("""() => [...document.querySelectorAll('tp-yt-paper-radio-button')]
        .filter(e => e.getAttribute('name') === 'VIDEO_HAS_ALTERED_CONTENT_YES')
        .map(e => e.getAttribute('aria-checked'))""")
    print('after:', after)
