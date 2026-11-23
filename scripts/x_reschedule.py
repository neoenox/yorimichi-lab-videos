"""予約済みX投稿の日時を変更する（CDP 9223）。
  python scripts/x_reschedule.py <video_id> "2026-11-26 11:05"
変更後に予約一覧で動画IDが1件だけであることを確認する。
"""
import argparse, datetime, sys
from playwright.sync_api import sync_playwright

CDP = 'http://127.0.0.1:9223'
MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

CARD_JS = """e=>{let a=e;for(let i=0;i<8&&a;i++,a=a.parentElement){if(a.getAttribute('data-testid')==='unsentTweet')return a.parentElement;}return null;}"""
SET_JS = """([m,d,y,h,mi])=>{const set=(id,v)=>{const e=document.querySelector('#'+id);const s=Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype,'value').set;s.call(e,String(v));e.dispatchEvent(new Event('change',{bubbles:true}));return e.value;};return [set('SELECTOR_1',m),set('SELECTOR_2',d),set('SELECTOR_3',y),set('SELECTOR_4',h),set('SELECTOR_5',mi)];}"""

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('video_id')
    ap.add_argument('when')
    a=ap.parse_args()
    dt=datetime.datetime.strptime(a.when,'%Y-%m-%d %H:%M')
    h12=dt.hour % 12 or 12
    expect=f"{MONTHS[dt.month-1]} {dt.day}, {dt.year} at {h12}:{dt.minute:02d} "+('AM' if dt.hour<12 else 'PM')
    with sync_playwright() as p:
        b=p.chromium.connect_over_cdp(CDP)
        pg=next((x for x in b.contexts[0].pages if 'x.com' in x.url),None) or b.contexts[0].new_page()
        pg.goto('https://x.com/compose/post/unsent/scheduled',wait_until='domcontentloaded')
        pg.wait_for_timeout(9000)
        card=pg.locator(f'text={a.video_id}')
        if card.count()!=1:
            raise SystemExit(f'予約一覧の一致が {card.count()} 件。中止')
        card.first.evaluate_handle(CARD_JS).as_element().click()
        pg.wait_for_timeout(3000)
        if a.video_id not in pg.locator('body').first.inner_text():
            raise SystemExit('編集対象の本文が見つからない。中止')
        pg.locator('text=/Will send on/').first.evaluate('e=>e.click()')
        pg.wait_for_timeout(1500)
        vals=pg.evaluate(SET_JS,[dt.month,dt.day,dt.year,dt.hour,dt.minute])
        if vals != [str(dt.month),str(dt.day),str(dt.year),str(dt.hour),str(dt.minute)]:
            raise SystemExit(f'select値が一致しない: {vals}')
        pg.locator('[data-testid=scheduledConfirmationPrimaryAction]').evaluate('e=>e.click()')
        pg.wait_for_timeout(1800)
        t=pg.locator('body').first.inner_text()
        if expect not in t:
            raise SystemExit(f'表示时刻が期待と違う: {expect} / {t[:300]}')
        pg.locator('[data-testid=tweetButton]').evaluate('e=>e.click()')
        pg.wait_for_timeout(6000)
        pg.goto('https://x.com/compose/post/unsent/scheduled',wait_until='domcontentloaded')
        pg.wait_for_timeout(9000)
        t=pg.locator('body').first.inner_text()
        n=t.count(a.video_id)
        idx=t.find(a.video_id)
        print(a.video_id, expect, 'count', n, repr(t[max(0,idx-220):idx+220]))
        if n!=1 or expect not in t[max(0,idx-300):idx]:
            raise SystemExit('予約一覧の確認に失敗')
    return 0

if __name__=='__main__':
    sys.exit(main())
