"""Git フックを .git/hooks に導入する。

    python scripts/install_git_hooks.py          導入（既存があれば .bak に退避）
    python scripts/install_git_hooks.py --check   導入済みか確認だけする

導入されるもの:
    pre-push  素材（画像・動画・音声・PDF 等）を含む push を中止する

背景: 動画素材は 1GB を超えて push が失敗するため、リモートにはテキストだけを置く。
テキストのみ反映するには scripts/main_push_textonly.py を使う。
"""
import argparse
import shutil
import stat
import subprocess
import sys
from pathlib import Path

HOOKS = ('pre-push',)


def hooks_dir():
    out = subprocess.run(['git', 'rev-parse', '--git-path', 'hooks'], text=True,
                         encoding='utf-8', errors='replace', capture_output=True)
    if out.returncode != 0:
        sys.stderr.write(out.stderr)
        raise SystemExit('git リポジトリ内で実行してください')
    return Path(out.stdout.strip())


def is_installed(src, dst):
    if not dst.exists():
        return False
    return src.read_bytes() == dst.read_bytes()


def main():
    ap = argparse.ArgumentParser(description='Git フックを導入する')
    ap.add_argument('--check', action='store_true', help='確認だけ行う')
    a = ap.parse_args()

    src_dir = Path(__file__).resolve().parent / 'hooks'
    dst_dir = hooks_dir()
    dst_dir.mkdir(parents=True, exist_ok=True)

    ok = True
    for name in HOOKS:
        src = src_dir / name
        dst = dst_dir / name
        installed = is_installed(src, dst)
        if a.check:
            print('%-10s %s' % (name, '導入済み' if installed else '未導入'))
            ok = ok and installed
            continue
        if installed:
            print('%-10s 導入済み（変更なし）' % name)
            continue
        if dst.exists():
            shutil.copy2(dst, str(dst) + '.bak')
            print('%-10s 既存を %s.bak に退避' % (name, name))
        shutil.copyfile(src, dst)
        dst.chmod(dst.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print('%-10s 導入した（%s）' % (name, dst))

    if a.check and not ok:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
