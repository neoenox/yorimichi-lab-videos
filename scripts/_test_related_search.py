from playwright.sync_api import sync_playwright

SHORT = 'LgePZBLaOTk'
TITLE = '日本の標準時は、なぜ明石の時刻？'

with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp('http://127.0.0.1:9222')
    p = b.contexts[0].pages[0]
    p.goto(f'https://studio.youtube.com/video/{SHORT}/edit', wait_until='domcontentloaded')
    p.wait_for_timeout(7000)
    p.locator('YTCP-TEXT-DROPDOWN-TRIGGER').filter(has_text='関連動画').first.click()
    p.wait_for_timeout(5000)
    dlg = p.locator('[role=dialog]').filter(has=p.locator('input[placeholder="自分の動画を検索"]'))
    search = dlg.locator('input[placeholder="自分の動画を検索"]')
    print('search count', search.count())
    search.first.fill(TITLE)
    p.wait_for_timeout(4000)
    opts = dlg.get_by_role('option')
    print('options after search', opts.count())
    for i in range(min(10, opts.count())):
        print(i, opts.nth(i).inner_text()[:100])
