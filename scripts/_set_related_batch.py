"""Studio で Short の関連動画に長尺を設定する（CDP 9222）。

使い方:
  python scripts/_set_related_batch.py --dry     # 対象を表示
  python scripts/_set_related_batch.py --apply   # 1件ずつ設定
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

R = Path(__file__).resolve().parents[1]
CHANNEL = 'UCN_do9fcssctmkrNsRWOO9A'
apply = '--apply' in sys.argv

# related_todo.py の出力をパース
env = dict(os.environ)
env['PYTHONPATH'] = r'C:/Users/neoen/AppData/Local/Programs/Python/Python311/Lib/site-packages'
proc = subprocess.run([sys.executable, str(R / 'scripts' / 'related_todo.py')],
                      cwd=R, capture_output=True, text=True, encoding='utf8', env=env)
if proc.stderr:
    print('related_todo stderr:', proc.stderr[:300])
out = proc.stdout
targets = []
for line in out.splitlines():
    if not line.startswith('TODO'):
        continue
    parts = line.split('\t')
    slug = parts[0].split()[1]
    short = parts[1].split('=')[1]
    long_id = parts[2].split('=')[1]
    title = parts[3]
    targets.append((slug, short, long_id, title))

limit = None
for a in sys.argv[1:]:
    if a.startswith('--limit='):
        limit = int(a.split('=')[1])
if limit is not None:
    targets = targets[:limit]
print('対象:', len(targets))
if not apply:
    for t in targets:
        print(*t, sep=' | ')
    sys.exit(0)

ok, fail = [], []
with sync_playwright() as pw:
    browser = pw.chromium.connect_over_cdp('http://127.0.0.1:9222')
    page = browser.contexts[0].pages[0]
    page.goto('https://studio.youtube.com/', wait_until='domcontentloaded')
    page.wait_for_timeout(5000)
    assert CHANNEL in page.url, 'wrong channel'

    for slug, short, long_id, title in targets:
        try:
            page.goto(f'https://studio.youtube.com/video/{short}/edit', wait_until='domcontentloaded')
            page.wait_for_timeout(6000)
            trigger = page.locator('YTCP-TEXT-DROPDOWN-TRIGGER').filter(has_text='関連動画')
            if trigger.count() == 0:
                fail.append((slug, 'trigger not found'))
                continue
            trigger.first.click()
            page.wait_for_timeout(4000)
            # ダイアログの検索欄に長尺のタイトルを入れる
            dlg = page.locator('[role=dialog]').filter(
                has=page.locator('input[placeholder="自分の動画を検索"]'))
            if dlg.count() == 0:
                fail.append((slug, 'dialog not found'))
                continue
            search = dlg.locator('input[placeholder="自分の動画を検索"]')
            search.first.fill(title)
            page.wait_for_timeout(3000)
            opts = dlg.get_by_role('option')
            hit = None
            for i in range(opts.count()):
                if title[:20] in (opts.nth(i).inner_text() or ''):
                    hit = opts.nth(i)
                    break
            if hit is None:
                fail.append((slug, 'long not found in dialog'))
                page.keyboard.press('Escape')
                continue
            hit.click()
            page.wait_for_timeout(1000)
            save = page.get_by_role('button', name='保存')
            if save.count():
                save.last.click()
                page.wait_for_timeout(2000)
            # related_done に記録
            done_path = R / 'data' / 'related_done.json'
            done = json.loads(done_path.read_text(encoding='utf8'))
            if short not in done:
                done.append(short)
                done_path.write_text(json.dumps(done), encoding='utf8')
            ok.append(slug)
            print('OK', slug, short, long_id)
        except Exception as e:
            fail.append((slug, str(e)[:120]))
            print('FAIL', slug, str(e)[:120])

print(f'完了: 成功 {len(ok)} / 失敗 {len(fail)}')
for f in fail:
    print('FAILED', f)
