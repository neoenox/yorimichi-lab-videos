"""Google AI モードの添付済みタブに、テンプレート改善用の質問だけを送る。"""
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from google_ai_review import CDP, wait_enabled_send

QUESTION = (
    'このYouTube Shortsの制作テンプレート（4場面構成・結論カード・大見出し12字以内・'
    '小見出し・出典表示・図・テロップ・ナレーション・背景映像の組み立て）を改善したいです。'
    '動画を通して見て、個別の修正ではなく、今後の制作テンプレートに反映すべき改善点を5つ提案してください。'
    '特に(1)冒頭の結論カードとナレーション開始のズレ、(2)小見出しと出典行の画面中央での並べ方、'
    '(3)下部字幕の行分割ルール、(4)大見出し・小見出し・図の情報の重複、'
    '(5)背景映像とテーマの対応、の観点から、テンプレート側のルールとしてどう変えるべきか具体的に書いてください。'
)
MARK = 'に対する AI モードの回答'

with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp(CDP)
    pg = next((x for x in b.contexts[0].pages
               if 'google' in x.url and 'mp4' in x.locator('body').first.inner_text()), None)
    if pg is None:
        raise SystemExit('ファイル添付済みのGoogle AIページが無い')
    pg.bring_to_front()
    ta = pg.locator('[aria-label="質問する"]').first
    ta.click()
    pg.keyboard.press('Control+a')
    pg.keyboard.press('Delete')
    pg.keyboard.insert_text(QUESTION)
    pg.wait_for_timeout(1500)
    wait_enabled_send(pg, 120).click()
    print('sent framework question', flush=True)

    last, stable = '', 0
    end = time.time() + 420
    while time.time() < end:
        pg.wait_for_timeout(4000)
        t = pg.locator('body').first.inner_text()
        i = t.rfind(MARK)
        ans = t[i + len(MARK):].strip() if i >= 0 else ''
        if ans and len(ans) > 150 and '考えています' not in ans:
            if ans == last:
                stable += 1
            else:
                stable, last = 0, ans
            if stable >= 3:
                break
    out = Path(__file__).resolve().parents[1] / 'out' / 'google_ai_framework_improvement.txt'
    out.write_text(last + '\n', encoding='utf8')
    print('saved', out, len(last), flush=True)
