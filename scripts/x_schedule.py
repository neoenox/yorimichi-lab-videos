"""X(@yorimichi_lab1)の予約投稿。Playwright MCP の専用プロファイルで動かす（拡張機能側のChromeは使わない）。

  1回で「Chrome(CDP 9223)の起動 → アカウント確認 → 予約日時の設定 → 本文入力 → 事前チェック → 投稿 → 予約一覧で重複確認」まで行う。

  python scripts/x_schedule.py --video <動画ID> --day 21 --hour 12 --min 5 --question "問いの文" [--ai] [--tags "#タグ #寄り道ラボ"] [--dry-run]

  --ai を付けると「※背景映像はAI生成のイメージです」を入れる（AI映像の動画は必須）。
  投稿前に、URLが1つだけ・ボタンが有効・予約日時が意図どおり、を確かめ、合わなければ投稿しない。
"""
import argparse
import os
import socket
import subprocess
import sys
import time

os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
sys.stdout.reconfigure(encoding='utf8')

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
PROFILE = r'C:\Users\neoen\AppData\Local\ms-playwright-mcp\mcp-chrome-666d4fb'   # ここに x.com のログインがある
CDP = 9223
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def port_open(port, timeout=1.0):
    try:
        socket.create_connection(('127.0.0.1', port), timeout).close()
        return True
    except Exception:
        return False


def ensure_chrome():
    if port_open(CDP):
        return False
    subprocess.Popen([CHROME, f'--remote-debugging-port={CDP}', f'--user-data-dir={PROFILE}',
                      '--no-first-run', '--no-default-browser-check', 'https://x.com/home'],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(40):
        if port_open(CDP):
            return True
        time.sleep(1)
    raise SystemExit('Chrome(CDP %d) を起動できない' % CDP)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--video', required=True)
    ap.add_argument('--day', type=int, required=True)
    ap.add_argument('--hour', type=int, required=True)
    ap.add_argument('--min', type=int, default=5)
    ap.add_argument('--year', type=int, default=2026)
    ap.add_argument('--month', type=int, default=11)
    ap.add_argument('--question', required=True, help='投稿の1行目（問い）')
    ap.add_argument('--ai', action='store_true', help='AI背景の明示を入れる')
    ap.add_argument('--tags', default='#歴史 #雑学 #寄り道ラボ')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    text = a.question + '\n約1分でこたえを確かめました。\n'
    if a.ai:
        text += '※背景映像はAI生成のイメージです\n'
    text += f'https://www.youtube.com/shorts/{a.video}\n' + a.tags
    when = f"{MONTHS[a.month - 1]} {a.day}, {a.year} at " + (f"{a.hour}:{a.min:02d} " ) + ('PM' if a.hour >= 12 else 'AM')

    from playwright.sync_api import sync_playwright

    started = ensure_chrome()
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(f'http://127.0.0.1:{CDP}')
        ctx = b.contexts[0]
        ctx.set_default_timeout(25000)
        pg = next((x for x in ctx.pages if 'x.com' in x.url), None) or ctx.new_page()
        pg.bring_to_front()
        print('Chrome起動=', started)

        # アカウントの確認（自分のプロフィールなら「プロフィールを編集」が出る）
        pg.goto('https://x.com/yorimichi_lab1', wait_until='domcontentloaded')
        pg.wait_for_timeout(4000)
        own = pg.evaluate("() => /プロフィールを編集|Edit profile/.test(document.body.innerText)")
        print('@yorimichi_lab1 でログイン:', own)
        if not own:
            raise SystemExit('ログイン中のアカウントが違う。投稿しない')

        pg.goto('https://x.com/compose/post', wait_until='domcontentloaded')
        pg.wait_for_selector('[data-testid=scheduleOption]', timeout=40000)
        pg.wait_for_timeout(1200)
        pg.evaluate("() => document.querySelector('[data-testid=scheduleOption]').click()")
        pg.wait_for_selector('#SELECTOR_1', timeout=20000)
        vals = pg.evaluate("""([y,m,d,h,mi]) => {
            const set = (id, v) => { const e = document.querySelector('#' + id);
              const s = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value').set;
              s.call(e, String(v)); e.dispatchEvent(new Event('change', {bubbles: true})); return e.value; };
            return [set('SELECTOR_1', m), set('SELECTOR_2', d), set('SELECTOR_3', y), set('SELECTOR_4', h), set('SELECTOR_5', mi)];
        }""", [a.year, a.month, a.day, a.hour, a.min])
        print('select値(月,日,年,時,分):', vals)
        pg.evaluate("""() => { const c = [...document.querySelectorAll('button,[role=button],span')]
            .find(e => e.textContent.trim() === 'Confirm'); if (!c) throw new Error('Confirm が無い'); c.click(); }""")
        pg.wait_for_timeout(1500)

        ta = pg.locator('[role=dialog] [data-testid=tweetTextarea_0]')
        ta.click()
        pg.keyboard.press('Control+a')
        pg.keyboard.press('Delete')
        pg.keyboard.insert_text(text)
        pg.wait_for_timeout(800)
        chk = pg.evaluate("""() => { const d = document.querySelector('[role=dialog]');
            const t = d.querySelector('[data-testid=tweetTextarea_0]').innerText;
            const b = d.querySelector('[data-testid=tweetButton]');
            return { urls: (t.match(/youtube\\.com/g) || []).length, len: t.length,
                     disabled: !!(b && b.disabled), when: (d.innerText.match(/[A-Z][a-z]{2} \\d+, \\d{4} at [^\\n]{0,12}/) || [''])[0] }; }""")
        print('確認:', chk, '/ 期待:', when)
        if chk['urls'] != 1 or chk['disabled'] or not chk['when'].startswith(when[:20]):
            raise SystemExit('チェック不一致。投稿しない')
        if a.dry_run:
            pg.screenshot(path=str(__import__('pathlib').Path(__file__).resolve().parents[1] / 'out' / 'x_dryrun.png'))
            print('--dry-run: 送信しない')
            return
        pg.evaluate("() => document.querySelector('[role=dialog] [data-testid=tweetButton]').click()")
        pg.wait_for_timeout(6000)
        print('投稿した。URL=', pg.url, '( /i/graduated-access に移っても投稿は通っている)')

        pg.goto('https://x.com/compose/post/unsent/scheduled', wait_until='domcontentloaded')
        pg.wait_for_timeout(9000)
        n = pg.evaluate("(v) => document.body.innerText.split(v).length - 1", a.video)
        print('予約一覧でこの動画IDの件数:', n, '(1なら重複なし)')


if __name__ == '__main__':
    main()
