"""CDP 9222 の Google AI モードで、ファイル添付済みのページからレビューを送信する。
  python scripts/google_ai_followup.py <slug> [--extra "追加の依頼文"]
google_ai_review.py が「送信ボタンが有効にならない」で止まったときの続き用。
"""
import argparse, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0,str(Path(__file__).resolve().parent))
from google_ai_review import CDP, build_question, wait_enabled_send

MARK='に対する AI モードの回答'

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('slug'); ap.add_argument('--extra',default='')
    a=ap.parse_args()
    ROOT=Path(__file__).resolve().parents[1]
    question=build_question(a.slug,'video')+a.extra
    with sync_playwright() as p:
        b=p.chromium.connect_over_cdp(CDP)
        pg=next((x for x in b.contexts[0].pages
                 if 'google' in x.url and 'mp4' in x.locator('body').first.inner_text()),None)
        if pg is None: raise SystemExit('ファイル添付済みのGoogle AIページが無い')
        pg.bring_to_front()
        ta=pg.locator('[aria-label="質問する"]').first
        ta.click(); pg.keyboard.press('Control+a'); pg.keyboard.press('Delete')
        pg.keyboard.insert_text(question)
        pg.wait_for_timeout(1500)
        wait_enabled_send(pg,120).click()
        print('sent',flush=True)
        last,stable='',0
        end=time.time()+420
        while time.time()<end:
            pg.wait_for_timeout(4000)
            t=pg.locator('body').first.inner_text()
            i=t.rfind(MARK)
            ans=t[i+len(MARK):].strip() if i>=0 else ''
            if ans and len(ans)>150 and 'AI モードが質問について考えています' not in ans:
                if ans==last: stable+=1
                else: stable,last=0,ans
                if stable>=3: break
        else: print('TIMEOUT',len(last),flush=True)
        out=ROOT/'out'/f'google_ai_review_{a.slug}_video.txt'
        out.write_text(last+'\n',encoding='utf-8')
        print('saved',out,len(last),flush=True)
    return 0

if __name__=='__main__': sys.exit(main())
