"""YouTube Studio の公開設定を bsk 経由で変更する。

API のクォータが尽きたとき用。ログイン済み Chrome（bsk 接続）で操作する。

usage:
    python scripts/studio_publish.py --video-id 8D0TWxHM6ko --visibility public
    python scripts/studio_publish.py --video-id ... --visibility public --dry-run
"""
import argparse
import json
import subprocess
import sys
import time

EDIT_URL = 'https://studio.youtube.com/video/%s/edit'
LABELS = {'public': '公開', 'private': '非公開', 'unlisted': '限定公開'}


def bsk(args, timeout=180):
    p = subprocess.run(['bsk', *args], text=True, encoding='utf-8', errors='replace',
                       capture_output=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def bsk_json(args, timeout=180):
    code, out, err = bsk([*args, '--json'], timeout=timeout)
    try:
        return code, json.loads(out or '{}')
    except json.JSONDecodeError:
        return code, {'raw': out[:300], 'err': err[:300]}


def obs(doc):
    post = doc.get('post') or {}
    o = post.get('observation') or doc.get('observation') or {}
    return o.get('text', '')


def ctx(doc):
    post = doc.get('post') or {}
    return post.get('context_id') or doc.get('context_id')


def ref_of(text, pattern):
    for line in text.splitlines():
        if pattern in line:
            tok = line.split()[0] if line.split() else ''
            if tok.startswith('@e'):
                return tok
    return None


def pick_browser():
    code, data = bsk_json(['browsers'])
    items = data if isinstance(data, list) else data.get('browsers') or []
    if not items:
        raise SystemExit('接続中のブラウザがありません')
    return items[0]['instance_id']


def click(session, context, ref, wait=2.0):
    code, doc = bsk_json(['step', '--session', session, '--context', context or '',
                          '--action', 'click', '--params', json.dumps({'ref': ref})])
    time.sleep(wait)
    return doc


def main():
    ap = argparse.ArgumentParser(description='Studio の公開設定を変更する')
    ap.add_argument('--video-id', required=True)
    ap.add_argument('--visibility', choices=list(LABELS), default='public')
    ap.add_argument('--browser')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    code, start = bsk_json(['session', 'start', '--browser', a.browser or pick_browser(),
                            '--name', 'studio', '--width', '1600', '--height', '1000', '--focus'])
    sid = start.get('session_id')
    if not sid:
        raise SystemExit('セッション開始に失敗: %s' % start)
    print('session', sid)

    try:
        bsk(['step', '--session', sid, '--action', 'navigate',
             '--params', json.dumps({'url': EDIT_URL % a.video_id})])
        time.sleep(10)
        code, doc = bsk_json(['cooperate', '--session', sid, 'sync'])
        text = obs(doc)
        if not text:
            raise SystemExit('ページの観測が取れませんでした（再実行してください）')
        print('page chars', len(text))

        # 現在の公開設定チップ（非公開 / 公開 / 限定公開）を押す
        chip = None
        chip_line = ''
        for label in ('非公開', '公開', '限定公開'):
            for line in text.splitlines():
                if 'button "%s' % label in line:
                    chip = line.split()[0]
                    chip_line = line.strip()[:80]
                    break
            if chip:
                break
        if not chip:
            raise SystemExit('公開設定のボタンが見つかりません')
        print('chip', chip, '|', chip_line)
        if a.dry_run:
            print('dry-run: ここで停止')
            return 0

        doc = click(sid, ctx(doc), chip)
        text2 = obs(doc) or text
        target = LABELS[a.visibility]
        radio = ref_of(text2, 'radio "%s' % target)
        if not radio:
            radio = ref_of(text2, '"%s"' % target)
        print('radio', radio, 'len', len(text2))
        if not radio:
            for line in text2.splitlines():
                if 'radio' in line:
                    print('  ', line.strip()[:110])
            raise SystemExit('公開設定のラジオボタンが見つかりません')

        doc = click(sid, ctx(doc), radio)
        text3 = obs(doc) or text2
        save = ref_of(text3, 'button "保存') or ref_of(text3, 'button "保')
        if not save:
            # VOM のラベルが文字化けする場合があるため、ダイアログ末尾のボタンを保存とみなす
            buttons = [ln.split()[0] for ln in text3.splitlines()
                       if 'button "' in ln and ln.split() and ln.split()[0].startswith('@e')]
            save = buttons[-1] if buttons else None
        print('save', save)
        if not save:
            print('--- dialog text ---')
            for line in text3.splitlines():
                if 'button' in line or 'radio' in line:
                    print('  ', line.strip()[:120])
            raise SystemExit('保存ボタンが見つかりません')
        doc = click(sid, ctx(doc), save, wait=4)
        text4 = obs(doc) or text3
        ok = ('公開' in text4) or ('保存しました' in text4)
        print('result chars', len(text4), 'looks_ok', ok)
        return 0
    finally:
        bsk(['session', 'stop', sid])
        print('session stopped')


if __name__ == '__main__':
    sys.exit(main())
