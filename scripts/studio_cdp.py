"""YouTube Studio を CDP(Chrome) + Playwright で操作する（公開設定・字幕）。

前提:
    ・Chrome を自動化プロファイルで起動:
        chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\\Users\\<user>\\.chrome-automation
    ・そのウィンドウで **寄り道ラボ** のアカウントにログイン済み（初回のみ）

usage:
    python scripts/studio_cdp.py --check
    python scripts/studio_cdp.py publish --video-id 8D0TWxHM6ko
    python scripts/studio_cdp.py captions --video-id 8D0TWxHM6ko --srt upload/short_x/subtitles_ja.srt

安全装置:
    チャンネルIDが CHANNEL_ID と一致しなければ何もせず停止する（誤操作防止）。
"""
import argparse
import sys
import time

CDP = 'http://127.0.0.1:9222'
CHANNEL_ID = 'UCN_do9fcssctmkrNsRWOO9A'  # 寄り道ラボ


def connect():
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    browser = pw.chromium.connect_over_cdp(CDP)
    ctx = browser.contexts[0]
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    return pw, page


def check_channel(page):
    page.goto('https://studio.youtube.com/', wait_until='domcontentloaded')
    page.wait_for_timeout(5000)
    url = page.url
    ok = CHANNEL_ID in url
    print('studio url:', url)
    print('channel ok:', ok)
    return ok


def publish(page, video_id):
    page.goto('https://studio.youtube.com/video/%s/edit' % video_id, wait_until='domcontentloaded')
    page.wait_for_timeout(6000)
    # 公開設定の行までスクロールして開く
    try:
        page.get_by_role('button', name='動画の公開設定を編集').click(timeout=15000)
    except Exception:
        page.get_by_text('公開設定', exact=False).first.scroll_into_view_if_needed()
        page.wait_for_timeout(1000)
        page.get_by_role('button', name='動画の公開設定を編集').click(timeout=15000)
    page.wait_for_timeout(2000)
    page.get_by_role('radio', name='公開', exact=True).check(timeout=15000)
    page.wait_for_timeout(1000)
    page.get_by_role('button', name='保存').click(timeout=15000)
    page.wait_for_timeout(5000)
    print('published (clicked 保存)')
    page.screenshot(path='out/studio_publish_after.png')


def captions(page, video_id, srt):
    page.goto('https://studio.youtube.com/video/%s/translations' % video_id, wait_until='domcontentloaded')
    page.wait_for_timeout(6000)
    page.get_by_role('button', name='手動でアップロード').click(timeout=20000)
    page.wait_for_timeout(1500)
    with page.expect_file_chooser(timeout=20000) as fc:
        page.get_by_role('button', name='続行').click()
    fc.value.set_files(srt)
    page.wait_for_timeout(6000)
    page.get_by_role('button', name='字幕を編集').click(timeout=30000)
    page.wait_for_timeout(4000)
    page.get_by_role('button', name='公開', exact=True).click(timeout=20000)
    page.wait_for_timeout(4000)
    print('captions published')
    page.screenshot(path='out/studio_captions_after.png')


def main():
    ap = argparse.ArgumentParser(description='Studio 操作（CDP）')
    ap.add_argument('command', choices=['check', 'publish', 'captions'])
    ap.add_argument('--video-id')
    ap.add_argument('--srt')
    a = ap.parse_args()

    pw, page = connect()
    try:
        if not check_channel(page):
            print('チャンネルが違います。寄り道ラボ（%s）に切り替えてから再実行してください。' % CHANNEL_ID)
            return 2
        if a.command == 'check':
            return 0
        if a.command == 'publish':
            publish(page, a.video_id)
        else:
            captions(page, a.video_id, a.srt)
        return 0
    finally:
        pw.stop()


if __name__ == '__main__':
    sys.exit(main())
