"""予約済みX投稿のURL（動画ID）を差し替える（CDP 9223）。
  python scripts/x_replace_url.py <old_video_id> <new_video_id>
差し替え後に予約一覧で旧ID=0件・新ID=1件を確認する。
"""
import argparse, sys
from playwright.sync_api import sync_playwright

CDP='http://127.0.0.1:9223'
CARD_JS="""e=>{let a=e;for(let i=0;i<8&&a;i++,a=a.parentElement){if(a.getAttribute('data-testid')==='unsentTweet')return a.parentElement;}return null;}"""

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('old'); ap.add_argument('new')
    a=ap.parse_args()
    with sync_playwright() as p:
        b=p.chromium.connect_over_cdp(CDP)
        pg=next((x for x in b.contexts[0].pages if 'x.com' in x.url),None) or b.contexts[0].new_page()
        pg.goto('https://x.com/compose/post/unsent/scheduled',wait_until='domcontentloaded')
        pg.wait_for_timeout(9000)
        card=pg.locator(f'text={a.old}')
        if card.count()!=1: raise SystemExit(f'旧IDの予約が {card.count()} 件。中止')
        card.first.evaluate_handle(CARD_JS).as_element().click()
        pg.wait_for_timeout(3000)
        ta=pg.locator('[data-testid=tweetTextarea_0]').first
        before=ta.inner_text()
        if a.old not in before: raise SystemExit('本文に旧IDが無い。中止')
        when_before=pg.locator('[data-testid=scheduledTweetIndicator]').first.inner_text()
        ta.evaluate('e=>e.click()'); pg.keyboard.press('Control+a'); pg.keyboard.press('Delete')
        pg.keyboard.insert_text(before.replace(a.old,a.new))
        pg.wait_for_timeout(1200)
        after=pg.locator('[data-testid=tweetTextarea_0]').first.inner_text()
        when_after=pg.locator('[data-testid=scheduledTweetIndicator]').first.inner_text()
        print('when',when_before,'->',when_after)
        print('old in text',a.old in after,'new in text',a.new in after,'urls',after.count('youtube.com/shorts/'))
        if a.old in after or a.new not in after or when_before!=when_after or after.count('youtube.com/shorts/')!=1:
            raise SystemExit('本文/日時の確認に失敗。保存しない')
        pg.locator('[data-testid=tweetButton]').evaluate('e=>e.click()')
        pg.wait_for_timeout(6000)
        pg.goto('https://x.com/compose/post/unsent/scheduled',wait_until='domcontentloaded')
        pg.wait_for_timeout(9000)
        t=pg.locator('body').first.inner_text()
        n_old=t.count(a.old); n_new=t.count(a.new)
        print('scheduled list old',n_old,'new',n_new)
        if n_old!=0 or n_new!=1: raise SystemExit('予約一覧の確認に失敗')
    return 0

if __name__=='__main__': sys.exit(main())
