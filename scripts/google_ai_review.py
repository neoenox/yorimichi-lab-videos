"""Google AI モード（https://www.google.com/ai）で台本／動画をレビューする。

2026-11-20 のオーナー指示で、Muse の代わりに動画・台本の両方を Google AI モードでレビューする。
使い方:
  # 台本のみ（spec の scenes/claims から依頼文を自動生成）
  python scripts/google_ai_review.py solo_x --mode script
  # 動画を添付（尺・字幕・音・事実・公開可否を依頼）
  python scripts/google_ai_review.py solo_x --mode video --video out/short_solo_x.mp4
  # 任意の依頼文
  python scripts/google_ai_review.py solo_x --mode custom --question "…"

前提: Chrome を --remote-debugging-port=9222 --user-data-dir=...\\.chrome-automation で起動。
出力: out/google_ai_review_<slug>_<mode>.txt
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
CDP_PORT = os.environ.get('GOOGLE_AI_CDP_PORT', '9222')
CDP = f'http://127.0.0.1:{CDP_PORT}'
URL = 'https://www.google.com/ai'


VIDEO_QUESTION = (
    'この動画を最後まで通して見て、Short動画としてレビューしてください。'
    'まず、ナレーションを時刻つきで書き起こしてください。'
    '次に、次の項目をそれぞれ分けて報告してください。'
    '(1) 音声の読み間違い・音割れ・無音。'
    '(2) 字幕の表記そのものの違和感。人名のカタカナ／ひらがな、漢数字と算用数字、専門用語の表記、'
    '読み仮名をそのまま字幕に出していないかを、音声の読みとは別に評価してください。'
    '音声が正しく読めていても、字幕の文字が不自然なら必ず指摘してください。'
    '(3) 字幕と音声の一致と、タイミングのズレ。'
    '(4) 文字の重なり・はみ出し・見切れ・折り返し。'
    '(5) 事実関係と、根拠より強い断定。'
    '(6) 冒頭1〜3秒の引き。'
    '(7) AI映像の不自然さ（文字・人物・現代物の混入）。'
    '(8) 画面下端や右端のUI被り。実際に被っている場合だけ指摘し、'
    '推測になる場合は「要確認」と分けてください。'
    '指摘には時刻と、修正後の文字列の候補を具体的に書いてください。'
    '最後に「公開可」か「修正必要」かを明示してください。'
)


def build_question(slug, mode):
    if mode == 'video':
        return VIDEO_QUESTION
    p = ROOT / 'data' / f'short_{slug}.json'
    if not p.exists():
        return ('この動画を最後まで確認して、Short動画としてのレビューをしてください。'
                'ナレーションの書き起こし、字幕との一致、読み・音の異常、'
                '字幕の表記そのものの違和感（人名のカタカナ／ひらがな、漢数字と算用数字、'
                '読み仮名の直出し）を音声の読みとは別に評価し、'
                '文字の重なり・見切れ、事実関係、公開可か修正必要かを報告してください。'
                '指摘には時刻と修正後の文字列の候補を書いてください。')
    d = json.loads(p.read_text(encoding='utf-8'))
    lines = [f'Short動画「{d.get("title", slug)}」の台本を査読してください。']
    for i, sc in enumerate(d.get('scenes', [])[:-1], 1):
        lines.append(f'場面{i}: {sc.get("text", "")} / 大:{sc.get("big", "")} / 出典:{sc.get("src", "")}')
    for c in d.get('claims', []):
        lines.append(f'根拠 {c.get("id")}: {c.get("statement")} | {c.get("source_url", "")}')
    if d.get('needs_research'):
        lines.append('未確認: ' + ' / '.join(d['needs_research']))
    lines.append('見てほしい点: 事実の誤り、根拠より強い断定、誤解を招く表現、'
                 '音声で聞きにくい語、画面に出る文字の表記（人名のカタカナ／ひらがな、'
                 '漢数字と算用数字、読み仮名の直出し）、公開可か修正必要か。'
                 'AIの指摘は根拠の原文と照合してから採用します。')
    return '\n'.join(lines)


def wait_enabled_send(pg, limit=90):
    end = time.time() + limit
    while time.time() < end:
        btn = pg.locator('button[aria-label="送信"]')
        for i in range(btn.count()):
            if btn.nth(i).is_visible() and btn.nth(i).get_attribute('disabled') is None:
                return btn.nth(i)
        pg.wait_for_timeout(2000)
    raise SystemExit('送信ボタンが有効にならない（アップロード未完了の可能性）')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('slug')
    ap.add_argument('--mode', choices=['script', 'video', 'custom'], default='script')
    ap.add_argument('--video')
    ap.add_argument('--question')
    ap.add_argument('--timeout', type=int, default=180)
    ap.add_argument('--keep-open', action='store_true')
    a = ap.parse_args()
    question = a.question or build_question(a.slug, a.mode)
    import socket
    from chrome_launch import launch_minimized
    try:
        socket.create_connection(('127.0.0.1', int(CDP_PORT)), 1).close()
    except OSError:
        launch_minimized(r'C:\Program Files\Google\Chrome\Application\chrome.exe', int(CDP_PORT),
                         r'C:\Users\neoen\.chrome-automation', URL)
        time.sleep(8)


    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(CDP)
        # video モードは既存の会話を再利用すると別動画のレビューに化ける。
        # 常に新しいタブを開き、動画を添付してから質問する（2026-11-23 実例）。
        created = True
        pg = b.contexts[0].new_page()
        pg.goto(URL, wait_until='domcontentloaded')
        pg.wait_for_timeout(8000)
        pg.bring_to_front()

        if a.mode == 'video' or (a.mode == 'custom' and a.video):
            if not a.video:
                raise SystemExit('--video が必要です')
            pg.locator('button[aria-label="ファイルとツールを追加し、モデルを選択します"]').first.click()
            pg.wait_for_timeout(1500)
            fis = pg.locator('input[type=file]')
            target = next((fis.nth(i) for i in range(fis.count())
                           if 'image' not in (fis.nth(i).get_attribute('accept') or '')), fis.last)
            target.set_input_files(str((ROOT / a.video).resolve() if not Path(a.video).is_absolute() else a.video))
            pg.wait_for_timeout(5000)
            print('attached', a.video, flush=True)

        ta = pg.locator('[aria-label="質問する"]')
        ta.first.fill(question)
        pg.wait_for_timeout(600)
        pg.wait_for_timeout(1000)
        wait_enabled_send(pg)

        wait_enabled_send(pg).click()
        print('sent', a.mode, flush=True)

        # 「AI モードの回答」という見出しは思考中にも出る。回答本文が3回連続で
        # 変わらないまで待ち、途中経過だけを保存しない（2026-11-22 実例）。
        mark = 'に対する AI モードの回答'
        t = ''
        last_answer = ''
        stable = 0
        end = time.time() + a.timeout
        while time.time() < end:
            pg.wait_for_timeout(4000)
            t = pg.locator('body').first.inner_text()
            i = t.rfind(mark)
            answer = t[i + len(mark):].strip() if i >= 0 else ''
            if answer and len(answer) > 150 and 'AI モードが質問について考えています' not in answer:
                if answer == last_answer:
                    stable += 1
                else:
                    stable, last_answer = 0, answer
                if stable >= 3:
                    break
        else:
            print('警告: 回答の完了を確認できませんでした', flush=True)
        out = ROOT / 'out' / f'google_ai_review_{a.slug}_{a.mode}.txt'
        out.write_text(t + '\n', encoding='utf-8')
        print('saved', out, 'chars', len(t), flush=True)
        if not a.keep_open and created:
            pg.close()



if __name__ == '__main__':
    main()
