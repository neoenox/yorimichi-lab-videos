from playwright.sync_api import sync_playwright

SHORT = 'LgePZBLaOTk'
TITLE = '日本の標準時は、なぜ明石の時刻？'

with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp('http://127.0.0.1:9222')
    p = b.contexts[0].pages[0]
    p.goto(f'https://studio.youtube.com/video/{SHORT}/edit', wait_until='domcontentloaded')
    p.wait_for_timeout(7000)
    trg = p.locator('YTCP-TEXT-DROPDOWN-TRIGGER').filter(has_text='関連動画')
    print('trigger', trg.count())
    trg.first.click()
    p.wait_for_timeout(6000)
    dlg = p.locator('[role=dialog]')
    print('dialog', dlg.count())
    if dlg.count():
        print('inputs', dlg.locator('input').count())
        for i in range(dlg.locator('input').count()):
            e = dlg.locator('input').nth(i)
            print(i, e.get_attribute('type'), e.get_attribute('placeholder'), e.get_attribute('aria-label'))
        print('options', dlg.get_by_role('option').count())
        for i in range(min(5, dlg.get_by_role('option').count())):
            print('opt', i, dlg.get_by_role('option').nth(i).inner_text()[:80])
