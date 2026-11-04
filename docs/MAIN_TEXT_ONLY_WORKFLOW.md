# リモートはテキストだけ（素材を push しない運用）

更新日: 2026-11-04。`main` へ素材（画像・動画・音声・原典資料）を入れない理由と、日々の手順。

## なぜ

動画素材（`assets/` と `docs/themes/**/_pdf/` の png/jpg）は **1.09 GB** あり、`git push` が
`Writing objects: 100% (3184/3184), 1.00 GiB` の直後に `fatal: the remote end hung up unexpectedly` で失敗した。
リモート（GitHub）にはコード・台本・タイムライン（テキスト）だけを置き、素材はローカルに保持する。

## push しないもの

| 種類 | 拡張子 |
| --- | --- |
| 画像（動画素材・絵コンテ・資料スキャン） | `.png` `.jpg` `.jpeg` `.gif` `.webp` `.bmp` `.tif` `.tiff` |
| 原典資料・アーカイブ | `.pdf` `.zip` `.npy` `.npz` |
| 動画・音声 | `.mp4` `.mov` `.mkv` `.webm` `.avi` `.wav` `.mp3` `.m4a` `.aac` `.flac` |
| 3D・Blender | `.glb` `.fbx` `.blend` `.blend1` |

これらは [`.gitignore`](../.gitignore) で除外されている。**追跡済みのファイルは残る**
（例: `assets/army/*`, `assets/earth/*`, `assets/portraits/*` の 45 枚は main に常在）。

## 日常の手順

```bash
# 1. 何が main に入るか確認する（push はしない）
python scripts/main_push_textonly.py --dry-run

# 2. PR を作る（作業ツリーの現状を 1 コミットにまとめる）
python scripts/main_push_textonly.py --pr

# 3. 中身を確認してマージ
gh pr view <番号>
gh pr merge <番号> --squash --delete-branch

# 4. ローカルの master を追従させる
git fetch --prune origin && git branch -f master origin/main
```

`--pr` の代わりに `--direct` を付けるとブランチを作らず `main` へ直接 push する。
過去のリビジョンから素材を除いて積みたいときは `--from <ref>` を使う。

### 仕組み

1. `origin/main` を `fetch` する
2. 一時インデックスに作業ツリーの現状を読み込む（`.gitignore` に従うので素材は自然に落ちる）
3. 差分に素材拡張子が**残っていないか検査**する（残っていれば中止）
4. `origin/main` の上に 1 コミットを組み立て、ブランチに push（必要なら `gh pr create`）
5. 変更ファイル数・行数・追加容量・最大ファイルを表示する

作業ツリー（カレントブランチ）は変更しない。

## フック（事故防止）

```bash
python scripts/install_git_hooks.py          # 導入
python scripts/install_git_hooks.py --check  # 導入済みか確認
```

`pre-push` フックが、push しようとしているコミットに素材の**追加・変更**が含まれていたら中止する
（削除は許可）。どうしても素材込みで push する場合だけ `git push --no-verify` を使う。

> このディレクトリは `E:\rekishikaisetu` の worktree。フックは `E:\rekishikaisetu\.git\hooks\` に
> 入るため、**全 worktree に効く**。

## 素材はどこにあるか

- 作業ディレクトリ（`assets/`, `docs/themes/`）にそのまま置く。git からは untracked + ignored として見える
- `ninja` ブランチ（素材 618 ファイルを含む履歴）は退役させ、`backup/ninja-pre-mainpush-20261104` に退避した
- 素材を誤って消した場合は、その退避ブランチから取り出せる:

```bash
git checkout backup/ninja-pre-mainpush-20261104 -- assets/anegawa/map_main.png
```

## トラブルシューティング

| 症状 | 対処 |
| --- | --- |
| push が `remote end hung up` で落ちる | 素材が混ざっている。`--dry-run` で確認し、`main_push_textonly.py` を使う |
| フックに中止された | `scripts/main_push_textonly.py --pr` に切り替える。素材を push したい場合のみ `--no-verify` |
| `git add -A` で素材が入りそう | `.gitignore` が効いているか `git check-ignore -v <path>` で確認 |
| ブランチ切替で素材が消えた | 素材は main に無いため checkout で削除される。退避ブランチから復元する |
