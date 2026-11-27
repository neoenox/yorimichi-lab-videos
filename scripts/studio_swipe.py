"""Studio の Shorts 分析から「視聴を継続／スワイプして消去」を読む（CDP 9222）。
  python scripts/studio_swipe.py <video_id> [<video_id> ...]
Analytics API に無いスワイプ率を、11/26 のKPI判定用に取得する。読み取ったタブは閉じる。
"""
import argparse, json, re, sys
from playwright.sync_api import sync_playwright

CDP = 'http://127.0.0.1:9222'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('ids', nargs='+')
    a = ap.parse_args()
    out = []
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(CDP)
        ctx = b.contexts[0]
        for vid in a.ids:
            pg = ctx.new_page()
            try:
                pg.goto(f'https://studio.youtube.com/video/{vid}/analytics/hub_overview', wait_until='domcontentloaded')
                pg.wait_for_timeout(9000)
                t = pg.locator('body').first.inner_text()
                m = re.search(r'([\d.]+)%\s*\n視聴を継続\s*\n([\d.]+)%\s*\nスワイプして消去', t)
                row = dict(video_id=vid,
                           continue_pct=float(m.group(1)) if m else None,
                           swipe_pct=float(m.group(2)) if m else None,
                           url=pg.url)
                out.append(row)
                print(json.dumps(row, ensure_ascii=False), flush=True)
            finally:
                pg.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())
