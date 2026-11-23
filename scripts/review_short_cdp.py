"""Short の台本を ChatGPT / Gemini（web）にレビューさせる（CDP 接続）。

前提: Chrome を --remote-debugging-port=9222 --user-data-dir=...\\.chrome-automation で起動し、
      両サイトにログイン済みであること。

usage:
  python scripts/review_short_cdp.py <slug> chatgpt|gemini [--out PATH] [--timeout 300]

結果は指摘として扱う。採用・不採用の判断と理由は docs/research/<date>_<slug>_reviews.md に人が記録する。
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CDP_PORT = os.environ.get('CHATGPT_CDP_PORT', '9222')
CDP = f'http://127.0.0.1:{CDP_PORT}'
SITES = {
    'chatgpt': ('chatgpt.com', '#prompt-textarea, div[contenteditable="true"]',
                'div[class*="DilResponseRoot"], div[data-message-author-role="assistant"]'),
    'gemini': ('gemini.google.com', 'div[aria-label="Gemini へのプロンプトを入力"]',
               '.model-response-text, div[data-response-id], model-response'),
}


def build_prompt(slug):
    d = json.loads((ROOT / 'data' / f'short_{slug}.json').read_text(encoding='utf-8'))
    lines = [
        'あなたは歴史・科学解説Shortの台本査読者です。ファイルは変更せず、評価だけしてください。',
        f'【題材】{d.get("title", "")}',
        f'【問い】{d.get("hook", "")}',
        f'【答え】{d.get("answer", "")}',
        '',
        '【シーン（ナレーション／大テロップ／小テロップ／画面の出典ラベル）】',
    ]
    for i, sc in enumerate(d.get('scenes', []), 1):
        lines.append(f'{i}. {sc.get("text", "")}')
        lines.append(f'   大: {sc.get("big", "")} / 小: {sc.get("sub", "")} / 出典: {sc.get("src", "")}')
    lines += ['', '【概要欄の根拠メモ】', d.get('notes', '')]
    claims = d.get('claims') or []
    if claims:
        lines += ['', '【根拠テーブル（主張／根拠URL／確認内容）】']
        for c in claims:
            lines.append(f'- {c.get("id")}: {c.get("statement")} | {c.get("source_url", "")} | {c.get("evidence_note", "")}')
    needs = d.get('needs_research') or []
    if needs:
        lines += ['', '【答えに影響しないとして残した未確認】'] + [f'- {x}' for x in needs]
    lines += [
        '',
        '見てほしい点:',
        '1. 事実の誤り・取り違え。根拠より強く断定していないか。',
        '2. 誤解を招く表現（例: 「1月15日が完全になくなる」と言っていないか）。',
        '3. 音声で聞いたときの読み間違い・言いにくさ（漢数字・固有名詞・年号）。',
        '4. 未確認の扱いが適切か。',
        '5. 公開可否: 「公開可」か「修正必要」か。修正必要なら最小限の指摘にする。',
        '',
        '根拠が手元にない点は「未確認」と分け、推測で断定しないでください。',
    ]
    return '\n'.join(lines)


def stable_text(page, selector, timeout, min_len=120):
    deadline = time.time() + timeout
    last = ''
    stable = 0
    while time.time() < deadline:
        page.wait_for_timeout(2000)
        found = page.locator(selector)
        if found.count() == 0:
            continue
        text = found.last.inner_text().strip()
        if len(text) < min_len or text == last:
            stable += 1 if text else 0
        else:
            stable = 0
        last = text
        if stable >= 3 and text:
            return text
    return last


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('slug')
    ap.add_argument('site', choices=sorted(SITES))
    ap.add_argument('--out')
    ap.add_argument('--timeout', type=int, default=300)
    ap.add_argument('--reuse', action='store_true', help='送信せず、いま開いている回答を取得する')
    a = ap.parse_args()
    domain, composer, response = SITES[a.site]
    prompt = build_prompt(a.slug)
    print(f'prompt chars: {len(prompt)}')

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = next((pg for pg in ctx.pages if domain in (pg.url or '')), None)
        if page is None:
            page = ctx.new_page()
        page.bring_to_front()
        if not a.reuse:
            page.goto(f'https://{domain}/', wait_until='domcontentloaded')
            page.wait_for_selector(composer, timeout=30000)
            print('url:', page.url)
            page.locator(composer).first.fill(prompt)
            page.wait_for_timeout(800)
            if a.site == 'chatgpt':
                try:
                    page.click('button[data-testid="send-button"]', timeout=5000)
                except Exception:
                    page.keyboard.press('Enter')
            else:
                page.keyboard.press('Enter')
            print('sent; waiting...')
        else:
            print('reuse: 既存の回答を取得します', page.url)
        answer = stable_text(page, response, a.timeout)
        if not answer:
            raise SystemExit('回答を取得できませんでした')
        out = Path(a.out) if a.out else ROOT / 'out' / f'{a.site}_review_{a.slug}_short.txt'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(f'# {a.site} review: {a.slug} short (2026-11-20)\n\n{answer}\n', encoding='utf-8')
        print('saved:', out)
        print('---- answer head ----')
        print(answer[:1200])


if __name__ == '__main__':
    main()
