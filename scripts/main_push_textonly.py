"""main を「テキストだけ」で最新化する（素材は push しない）。

背景:
    動画制作の素材（png/jpg 等）は 1GB を超え、GitHub への push が失敗する。
    リモートの main にはコード・台本・タイムライン（テキスト）だけを置く方針。

使い方:
    python scripts/main_push_textonly.py --dry-run          何が入るか確認するだけ
    python scripts/main_push_textonly.py --pr              作業ツリーの現状を 1 コミットにして PR を作る
    python scripts/main_push_textonly.py --direct          同じ内容を main へ直接 push（fast-forward）
    python scripts/main_push_textonly.py --from ninja --pr 指定コミットの内容から素材を除いて積む

他のスクリプトから使う:
    from main_push_textonly import push_text_only
    push_text_only(pr=True)                     # 現状をテキストのみで PR にする
    push_text_only(direct=True, dry_run=True)   # 何が入るかだけ調べる

やること:
    1. origin/main（base）を最新化する
    2. 一時インデックスに「作業ツリーの現状」または「指定コミットの内容」を読み込む
       （.gitignore に従うので、素材は自然に落ちる）
    3. 素材拡張子が差分に残っていないか検査する（残っていれば中止）
    4. origin/main の上に 1 コミットとして積み、ブランチに push（pr=True なら PR も作る）
    5. 変更ファイル数・行数・追加バイト数を表示する

注意:
    作業ツリー（カレントブランチ）は変更しない。コミットは plumbing で組み立てる。
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

# 定数は rebuild_all.py などからも参照する
MEDIA_EXT = {
    '.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.tif', '.tiff',
    '.pdf', '.zip', '.npy', '.npz',
    '.mp4', '.mov', '.mkv', '.webm', '.avi', '.wav', '.mp3', '.m4a', '.aac', '.flac',
    '.glb', '.fbx', '.blend', '.blend1',
}
# --from で素材を落とすときのパターン（.gitignore は利かないため明示する）
MEDIA_GLOBS = ['*' + e for e in sorted(MEDIA_EXT)]
# 追加が大きすぎるファイルの警告しきい値
WARN_BYTES = 5 * 1024 * 1024


class MediaInDiff(RuntimeError):
    """差分に素材が残っていたときの例外。"""

    def __init__(self, paths):
        super().__init__('素材ファイルが差分に含まれています（%d 件）' % len(paths))
        self.paths = paths


def git(args, env=None, check=True):
    """git を実行し、標準出力を文字列で返す（失敗時は check に従う）。"""
    p = subprocess.run(
        ['git', *args],
        text=True, encoding='utf-8', errors='replace',
        capture_output=True, env=env,
    )
    if check and p.returncode != 0:
        sys.stderr.write(p.stdout + p.stderr)
        raise SystemExit('git %s に失敗しました（exit %d）' % (' '.join(args), p.returncode))
    return p.stdout


def split_z(out):
    return [x for x in out.split('\0') if x]


def is_media(path):
    return Path(path).suffix.lower() in MEDIA_EXT


def human(n):
    for unit in ('B', 'KB', 'MB', 'GB'):
        if n < 1024 or unit == 'GB':
            return '%.1f %s' % (n, unit)
        n /= 1024.0
    return '%d B' % n


def push_text_only(base='origin/main', from_ref=None, remote='origin', branch=None,
                   message=None, pr=False, draft=False, direct=False,
                   dry_run=False, allow_media=False, do_fetch=True, quiet=False,
                   paths=None):
    """テキストだけを 1 コミットにまとめて main へ積む。結果を dict で返す。

    paths を渡すと、そのパスだけを対象にする（他の作業と混ざらない）。
    """
    def say(*a):
        if not quiet:
            print(*a)

    if pr and direct:
        raise ValueError('pr と direct は同時に使えません')

    # 1. 土台を最新化する
    if do_fetch:
        git(['fetch', remote, '--prune'])
    base_sha = git(['rev-parse', '--verify', base + '^{commit}']).strip()
    now = datetime.now()
    branch = branch or ('agent/text-only-%s' % now.strftime('%Y%m%d-%H%M%S'))

    # 2. 一時インデックスでツリーを組み立てる（作業ツリーには触らない）
    idx_dir = tempfile.mkdtemp(prefix='textonly-')
    idx = os.path.join(idx_dir, 'index')
    env = dict(os.environ, GIT_INDEX_FILE=idx)
    try:
        git(['read-tree', base_sha], env=env)
        if from_ref:
            src = git(['rev-parse', '--verify', from_ref + '^{commit}']).strip()
            git(['read-tree', '--reset', src], env=env)
            git(['rm', '-r', '--cached', '--quiet', '--ignore-unmatch', '--'] + MEDIA_GLOBS, env=env)
        else:
            git(['add', '-A', '--'] + (list(paths) if paths else ['.']), env=env)  # .gitignore に従う
        tree = git(['write-tree'], env=env).strip()

        # 3. 差分に素材が残っていないか検査する
        changed = split_z(git(['diff', '--name-only', '-z', '--no-renames', base_sha, tree]))
        media = [p for p in changed if is_media(p)]
        if media and not allow_media:
            raise MediaInDiff(media)

        # 4. 集計
        rows = []
        for p in changed:
            out = git(['cat-file', '-s', '%s:%s' % (tree, p)], check=False).strip()
            rows.append((int(out) if out.isdigit() else 0, p))
        total = sum(s for s, _ in rows)
        rows.sort(reverse=True)
        numstat = git(['diff', '--numstat', base_sha, tree]).strip().splitlines()
        adds = sum(int(x.split('\t')[0]) for x in numstat if x.split('\t')[0].isdigit())
        dels = sum(int(x.split('\t')[1]) for x in numstat if x.split('\t')[1].isdigit())

        say('土台      : %s (%s)' % (base, base_sha[:7]))
        say('内容      : %s' % (from_ref if from_ref else '作業ツリーの現状（.gitignore に従う）'))
        if paths:
            say('対象      : %s' % ' '.join(paths))
        say('変更      : %d ファイル / +%d / -%d' % (len(changed), adds, dels))
        say('追加容量  : %s' % human(total))
        if rows:
            say('最大のもの: %s  %s' % (human(rows[0][0]), rows[0][1]))
        big = [(s, p) for s, p in rows if s > WARN_BYTES]
        if big:
            say('⚠ %s を超えるファイル: %d 件' % (human(WARN_BYTES), len(big)))
            for s, p in big[:5]:
                say('    %s  %s' % (human(s), p))

        result = {
            'base': base, 'base_sha': base_sha, 'branch': branch, 'commit': None,
            'changed': [p for _, p in rows], 'files': len(changed),
            'adds': adds, 'dels': dels, 'bytes': total,
            'pushed': False, 'pr_url': None, 'messages': [],
        }

        if not changed:
            say('差分がありません。push するものはありません。')
            return result

        if dry_run:
            say('\n(--dry-run のため commit / push は行いません)')
            say('含まれるファイル（先頭 20 件）:')
            for s, p in rows[:20]:
                say('    %8s  %s' % (human(s), p))
            return result

        # 5. コミットを作る
        msg = message or (
            'chore: main をテキストのみで最新化（%s）\n\n'
            '素材（画像・動画・音声・PDF 等）は .gitignore 方針により含めない。\n'
            'scripts/main_push_textonly.py で生成。\n' % now.strftime('%Y-%m-%d %H:%M')
        )
        commit = git(['commit-tree', tree, '-p', base_sha, '-m', msg]).strip()
        git(['update-ref', 'refs/heads/' + branch, commit])
        result['commit'] = commit
        say('\nコミット  : %s  (%s)' % (commit[:7], branch))

        # 6. push（direct なら main へ）
        target = 'main' if direct else branch
        git(['push', remote, '%s:%s' % (branch, target)])
        result['pushed'] = True
        say('push      : %s %s -> %s' % (remote, branch, target))

        # 7. 必要なら PR を作る
        if pr:
            fd, body_path = tempfile.mkstemp(suffix='.md')
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write('## 変更内容\n\n')
                f.write('- テキストのみ（素材なし）で main を最新化\n')
                f.write('- 変更: %d ファイル / +%d / -%d（追加 %s）\n\n' % (len(changed), adds, dels, human(total)))
                f.write('### 主な変更ファイル\n\n')
                for s, p in rows[:30]:
                    f.write('- `%s`（%s）\n' % (p, human(s)))
                if len(rows) > 30:
                    f.write('- ... 他 %d 件\n' % (len(rows) - 30))
                f.write('\n### 含めていないもの\n\n- 画像・動画・音声・PDF などの素材（.gitignore 方針）\n')
            cmd = ['gh', 'pr', 'create', '--base', 'main', '--head', branch,
                   '--title', 'chore: main をテキストのみで最新化（%s）' % now.strftime('%Y-%m-%d %H:%M'),
                   '--body-file', body_path]
            if draft:
                cmd.append('--draft')
            p = subprocess.run(cmd, text=True, encoding='utf-8', errors='replace', capture_output=True)
            os.unlink(body_path)
            if p.returncode != 0:
                sys.stderr.write(p.stdout + p.stderr)
                raise RuntimeError('PR の作成に失敗しました（push 済み）')
            result['pr_url'] = p.stdout.strip()
            say('PR        : %s' % result['pr_url'])
        return result
    finally:
        shutil.rmtree(idx_dir, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description='main をテキストだけ（素材なし）で最新化する')
    ap.add_argument('--from', dest='from_ref', help='このリビジョンの内容を使う（既定: 作業ツリーの現状）')
    ap.add_argument('--base', default='origin/main', help='積む土台（既定: origin/main）')
    ap.add_argument('--remote', default='origin', help='push 先のリモート名（既定: origin）')
    ap.add_argument('--branch', help='push するブランチ名（既定: agent/text-only-<日付>-<時刻>）')
    ap.add_argument('--message', help='コミットメッセージ（既定: 自動生成）')
    ap.add_argument('--pr', action='store_true', help='push 後に gh で PR を作る')
    ap.add_argument('--draft', action='store_true', help='--pr のとき draft で作る')
    ap.add_argument('--direct', action='store_true', help='ブランチを作らず main へ直接 push する')
    ap.add_argument('--allow-media', action='store_true', help='素材が残っていても続行する（非推奨）')
    ap.add_argument('--dry-run', action='store_true', help='検査と集計だけ行い、commit/push しない')
    ap.add_argument('--no-fetch', action='store_true', help='fetch を省略する')
    ap.add_argument('--path', action='append', dest='paths',
                    help='このパスだけを対象にする（複数可。他の作業と混ざらない）')
    a = ap.parse_args()

    t0 = time.time()
    try:
        r = push_text_only(
            base=a.base, from_ref=a.from_ref, remote=a.remote, branch=a.branch,
            message=a.message, pr=a.pr, draft=a.draft, direct=a.direct,
            dry_run=a.dry_run, allow_media=a.allow_media, do_fetch=not a.no_fetch,
            paths=a.paths,
        )
    except MediaInDiff as e:
        sys.stderr.write('✖ %s:\n' % e)
        for p in e.paths[:20]:
            sys.stderr.write('    %s\n' % p)
        if len(e.paths) > 20:
            sys.stderr.write('    ... 他 %d 件\n' % (len(e.paths) - 20))
        sys.stderr.write('  .gitignore を確認するか、--allow-media で強行してください。\n')
        return 1
    if not a.dry_run and r['changed']:
        print('所要      : %.1f 秒' % (time.time() - t0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
