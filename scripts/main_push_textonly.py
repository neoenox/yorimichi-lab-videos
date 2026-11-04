"""main を「テキストだけ」で最新化する（素材は push しない）。

背景:
    動画制作の素材（png/jpg 等）は 1GB を超え、GitHub への push が失敗する。
    リモートの main にはコード・台本・タイムライン（テキスト）だけを置く方針。

使い方:
    python scripts/main_push_textonly.py --dry-run          何が入るか確認するだけ
    python scripts/main_push_textonly.py --pr              作業ツリーの現状を 1 コミットにして PR を作る
    python scripts/main_push_textonly.py --direct          同じ内容を main へ直接 push（fast-forward）
    python scripts/main_push_textonly.py --from ninja --pr 指定コミットの内容から素材を除いて積む

やること:
    1. origin/main（--base）を最新化する
    2. 一時インデックスに「作業ツリーの現状」または「指定コミットの内容」を読み込む
       （.gitignore に従うので、素材は自然に落ちる）
    3. 素材拡張子が差分に残っていないか検査する（残っていれば中止）
    4. origin/main の上に 1 コミットとして積み、ブランチに push（--pr なら PR も作る）
    5. 変更ファイル数・行数・追加バイト数を表示する

注意:
    作業ツリー（カレントブランチ）は変更しない。コミットは plumbing で組み立てる。
"""
import argparse
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# push しない拡張子（素材・原典資料・一時バイナリ）
MEDIA_EXT = {
    '.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.tif', '.tiff',
    '.pdf', '.zip', '.npy', '.npz',
    '.mp4', '.mov', '.mkv', '.webm', '.avi', '.wav', '.mp3', '.m4a', '.aac', '.flac',
    '.glb', '.fbx', '.blend', '.blend1',
}
# 追加が大きすぎるファイルの警告しきい値
WARN_BYTES = 5 * 1024 * 1024


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
    a = ap.parse_args()

    if a.pr and a.direct:
        raise SystemExit('--pr と --direct は同時に使えません')

    # 1. 土台を最新化する
    if not a.no_fetch:
        git(['fetch', a.remote, '--prune'])
    base = git(['rev-parse', '--verify', a.base + '^{commit}']).strip()
    now = datetime.now()
    branch = a.branch or ('agent/text-only-%s' % now.strftime('%Y%m%d-%H%M%S'))

    # 2. 一時インデックスでツリーを組み立てる（作業ツリーには触らない）
    idx_dir = tempfile.mkdtemp(prefix='textonly-')
    idx = os.path.join(idx_dir, 'index')
    env = dict(os.environ, GIT_INDEX_FILE=idx)
    try:
        git(['read-tree', base], env=env)
        if a.from_ref:
            src = git(['rev-parse', '--verify', a.from_ref + '^{commit}']).strip()
            git(['read-tree', '--reset', src], env=env)
            # 素材をインデックスから落とす（.gitignore は効かないので明示的に）
            git(['rm', '-r', '--cached', '--quiet', '--ignore-unmatch', '--'] +
                ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.webp', '*.pdf', '*.zip', '*.npy', '*.npz',
                 '*.mp4', '*.mov', '*.mkv', '*.webm', '*.wav', '*.mp3', '*.m4a', '*.aac', '*.flac',
                 '*.glb', '*.fbx', '*.blend', '*.blend1'], env=env)
        else:
            # 作業ツリーの現状（.gitignore に従う）
            git(['add', '-A', '--', '.'], env=env)

        tree = git(['write-tree'], env=env).strip()

        # 3. 差分に素材が残っていないか検査する
        changed = split_z(git(['diff', '--name-only', '-z', '--no-renames', base, tree]))
        media = [p for p in changed if is_media(p)]
        if media and not a.allow_media:
            sys.stderr.write('✖ 素材ファイルが差分に含まれています（%d 件）:\n' % len(media))
            for p in media[:20]:
                sys.stderr.write('    %s\n' % p)
            if len(media) > 20:
                sys.stderr.write('    ... 他 %d 件\n' % (len(media) - 20))
            sys.stderr.write('  .gitignore を確認するか、--allow-media で強行してください。\n')
            raise SystemExit(1)

        # 4. 中身の集計
        rows = []
        for p in changed:
            out = git(['cat-file', '-s', '%s:%s' % (tree, p)], check=False).strip()
            rows.append((int(out) if out.isdigit() else 0, p))
        total = sum(s for s, _ in rows)
        rows.sort(reverse=True)
        numstat = git(['diff', '--numstat', base, tree]).strip().splitlines()
        adds = sum(int(x.split('\t')[0]) for x in numstat if x.split('\t')[0].isdigit())
        dels = sum(int(x.split('\t')[1]) for x in numstat if x.split('\t')[1].isdigit())

        print('土台      : %s (%s)' % (a.base, base[:7]))
        if a.from_ref:
            print('内容      : %s' % a.from_ref)
        else:
            print('内容      : 作業ツリーの現状（.gitignore に従う）')
        print('変更      : %d ファイル / +%d / -%d' % (len(changed), adds, dels))
        print('追加容量  : %s' % human(total))
        if rows:
            print('最大のもの: %s  %s' % (human(rows[0][0]), rows[0][1]))
        big = [(s, p) for s, p in rows if s > WARN_BYTES]
        if big:
            print('⚠ %s を超えるファイル: %d 件' % (human(WARN_BYTES), len(big)))
            for s, p in big[:5]:
                print('    %s  %s' % (human(s), p))
        if not changed:
            print('差分がありません。push するものはありません。')
            return 0

        if a.dry_run:
            print('\n(--dry-run のため commit / push は行いません)')
            print('例に含まれるファイル（先頭 20 件）:')
            for s, p in rows[:20]:
                print('    %8s  %s' % (human(s), p))
            return 0

        # 5. コミットを作る
        msg = a.message or (
            'chore: main をテキストのみで最新化（%s）\n\n'
            '素材（画像・動画・音声・PDF 等）は .gitignore 方針により含めない。\n'
            'scripts/main_push_textonly.py で生成。\n' % now.strftime('%Y-%m-%d %H:%M')
        )
        commit = git(['commit-tree', tree, '-p', base, '-m', msg]).strip()
        git(['update-ref', 'refs/heads/' + branch, commit])
        print('\nコミット  : %s  (%s)' % (commit[:7], branch))

        # 6. push（--direct なら main へ）
        target = 'main' if a.direct else branch
        git(['push', a.remote, '%s:%s' % (branch, target)])
        print('push      : %s %s -> %s' % (a.remote, branch, target))

        # 7. 必要なら PR を作る
        if a.pr:
            body = tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8')
            body.write('## 変更内容\n\n')
            body.write('- テキストのみ（素材なし）で main を最新化\n')
            body.write('- 変更: %d ファイル / +%d / -%d（追加 %s）\n\n' % (len(changed), adds, dels, human(total)))
            body.write('### 主な変更ファイル\n\n')
            for s, p in rows[:30]:
                body.write('- `%s`（%s）\n' % (p, human(s)))
            if len(rows) > 30:
                body.write('- ... 他 %d 件\n' % (len(rows) - 30))
            body.write('\n### 含めていないもの\n\n- 画像・動画・音声・PDF などの素材（.gitignore 方針）\n')
            body.close()
            cmd = ['gh', 'pr', 'create', '--base', 'main', '--head', branch,
                   '--title', 'chore: main をテキストのみで最新化（%s）' % now.strftime('%Y-%m-%d %H:%M'),
                   '--body-file', body.name]
            if a.draft:
                cmd.append('--draft')
            p = subprocess.run(cmd, text=True, encoding='utf-8', errors='replace',
                               capture_output=True)
            os.unlink(body.name)
            if p.returncode != 0:
                sys.stderr.write(p.stdout + p.stderr)
                raise SystemExit('PR の作成に失敗しました（push 済み）')
            print('PR        : %s' % p.stdout.strip())
        return 0
    finally:
        try:
            os.unlink(idx)
        except OSError:
            pass
        try:
            os.rmdir(idx_dir)
        except OSError:
            pass


if __name__ == '__main__':
    sys.exit(main())
