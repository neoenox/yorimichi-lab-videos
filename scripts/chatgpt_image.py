"""ChatGPT(web) で画像を生成し、ダウンロードして保存する（bsk 経由）。

背景: この環境では Web 検索 API が使えないため、ログイン済み Chrome を bsk（browser-skill）で
操作して画像生成を依頼する。手作業の手順は docs/SHORTS_PRODUCTION_NOTES.md を参照。

usage:
    python scripts/chatgpt_image.py --prompt "縦長9:16、濃紺の背景に筆と硯…" --out assets/x/gen_base.png
    python scripts/chatgpt_image.py --prompt "..." --out ... --timeout 300 --keep-session

前提:
    ・bsk のデーモンが動いていて、ログイン済みブラウザが 1 つ接続されている（`bsk browsers`）
    ・ChatGPT にログイン済み（画像生成が使えるプラン）

やること:
    1. `bsk session start` で Agent Window を開く（ウィンドウは最大化）
    2. `https://chatgpt.com/?q=<prompt>` で入力欄を埋めて送信（Enter ではなく「送信」ボタン）
    3. 「ダウンロード」が出るまで待ち、クリックして Downloads の新規ファイルを拾う
    4. `--out` に保存（webp/jpg は png に変換）。セッションは終了する
"""
import argparse
import json
import shutil
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

DOWNLOADS = Path.home() / 'Downloads'


def bsk(args, timeout=120):
    p = subprocess.run(['bsk', *args], text=True, encoding='utf-8', errors='replace',
                       capture_output=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def bsk_json(args, timeout=120):
    code, out, err = bsk([*args, '--json'], timeout=timeout)
    try:
        return code, json.loads(out or '{}')
    except json.JSONDecodeError:
        return code, {'raw': out, 'err': err}


def obs_text(doc):
    post = doc.get('post') or {}
    obs = post.get('observation') or doc.get('observation') or {}
    return obs.get('text', '')


def ctx_of(doc):
    post = doc.get('post') or {}
    return post.get('context_id') or doc.get('context_id')


def ref_for(text, pattern):
    """VOM の行から `@eNN` を取り出す。"""
    for line in text.splitlines():
        if pattern in line:
            for tok in line.split():
                if tok.startswith('@e'):
                    return tok
    return None


def pick_browser():
    code, data = bsk_json(['browsers'])
    items = data if isinstance(data, list) else data.get('browsers') or []
    if not items:
        raise SystemExit('接続中のブラウザがありません（bsk browsers を確認）')
    return items[0]['instance_id']


def wait_for_send(session, timeout=60):
    """送信ボタンの ref を探す（入力欄が埋まっていないと出ない）。"""
    end = time.time() + timeout
    last = ''
    while time.time() < end:
        code, doc = bsk_json(['cooperate', '--session', session, 'sync'])
        text = obs_text(doc)
        last = text or last
        ref = ref_for(last, 'button "送信"')
        if ref:
            return ref, ctx_of(doc) or ctx_of({'post': {}})
        time.sleep(3)
    raise SystemExit('送信ボタンが見つかりません（入力欄が空の可能性）')


def wait_sent(session, snippet, timeout=25):
    """送信されたかを VOM で確認する（送信クリックが弾かれることがある）。"""
    end = time.time() + timeout
    while time.time() < end:
        code, doc = bsk_json(['cooperate', '--session', session, 'sync'])
        text = obs_text(doc)
        if text and ('あなたの発言' in text) and (snippet in text):
            return True
        time.sleep(3)
    return False


def wait_for_download_button(session, base_count, timeout):
    """生成完了を待ち、ダウンロードボタンの ref を返す。"""
    end = time.time() + timeout
    last = ''
    while time.time() < end:
        code, doc = bsk_json(['cooperate', '--session', session, 'sync'])
        text = obs_text(doc)
        last = text or last
        if last.count('ダウンロード') > base_count:
            ref = ref_for(last, 'ダウンロード')
            if ref:
                return ref, ctx_of(doc)
        time.sleep(10)
    raise SystemExit('生成が完了しませんでした（timeout %ds）' % timeout)


def snapshot_downloads():
    return {p.name for p in DOWNLOADS.iterdir() if p.is_file()} if DOWNLOADS.exists() else set()


def newest_new_file(before, wait=20):
    end = time.time() + wait
    while time.time() < end:
        now = {p.name for p in DOWNLOADS.iterdir() if p.is_file()} if DOWNLOADS.exists() else set()
        new = now - before
        if new:
            files = sorted((DOWNLOADS / n for n in new), key=lambda p: p.stat().st_mtime, reverse=True)
            return files[0]
        time.sleep(2)
    return None


def save_as(src, out):
    from PIL import Image
    out.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() == '.png':
        shutil.move(str(src), str(out))
        return
    Image.open(src).convert('RGB').save(out)
    src.unlink()


def main():
    ap = argparse.ArgumentParser(description='ChatGPT(web) で画像を生成して保存する')
    ap.add_argument('--prompt', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--timeout', type=int, default=240, help='生成待ちの秒数（既定240）')
    ap.add_argument('--browser', help='bsk のブラウザ instance id（既定: 最初の接続）')
    ap.add_argument('--keep-session', action='store_true', help='終了時にセッションを残す')
    ap.add_argument('--reuse-last', action='store_true',
                    help='新規生成せず、直近の「画像生成」チャットからダウンロードだけ行う')
    a = ap.parse_args()

    out = Path(a.out)
    browser = a.browser or pick_browser()
    before = snapshot_downloads()

    code, start = bsk_json(['session', 'start', '--browser', browser, '--name', 'image',
                            '--width', '1600', '--height', '1000', '--focus'])
    sid = start.get('session_id')
    if not sid:
        raise SystemExit('セッションを開始できません: %s' % start)
    print('session', sid)

    try:
        if a.reuse_last:
            dl_ref, ctx2 = wait_for_download_button(sid, -1, a.timeout)
        else:
            url = 'https://chatgpt.com/?q=' + urllib.parse.quote(a.prompt)
            bsk(['step', '--session', sid, '--action', 'navigate', '--params', json.dumps({'url': url}, ensure_ascii=False)])
            time.sleep(6)

            send_ref, ctx = wait_for_send(sid)
            print('send', send_ref)
            code, doc = bsk_json(['cooperate', '--session', sid, 'sync'])
            base_count = obs_text(doc).count('ダウンロード')
            bsk(['step', '--session', sid, '--context', ctx or ctx_of(doc),
                 '--action', 'click', '--params', json.dumps({'ref': send_ref})])

            if not wait_sent(sid, a.prompt[:12]):
                print('送信が確認できないため、もう一度クリックします')
                code, doc = bsk_json(['cooperate', '--session', sid, 'sync'])
                send_ref2 = ref_for(obs_text(doc), 'button "送信"') or send_ref
                bsk(['step', '--session', sid, '--context', ctx_of(doc) or ctx,
                     '--action', 'click', '--params', json.dumps({'ref': send_ref2})])
                if not wait_sent(sid, a.prompt[:12], timeout=30):
                    raise SystemExit('送信できませんでした（クリックが弾かれている可能性）')
            print('sent ok')
            dl_ref, ctx2 = wait_for_download_button(sid, base_count, a.timeout)

        print('download', dl_ref)
        bsk(['step', '--session', sid, '--context', ctx2,
             '--action', 'click', '--params', json.dumps({'ref': dl_ref})])

        got = newest_new_file(before)
        if not got:
            raise SystemExit('ダウンロードされたファイルが見つかりません')
        save_as(got, out)
        print('saved', out, out.stat().st_size, 'bytes')
    finally:
        if not a.keep_session:
            bsk(['session', 'stop', sid])
            print('session stopped')
    return 0


if __name__ == '__main__':
    sys.exit(main())
