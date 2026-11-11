# 作業ツリーの未コミット変更の検証（2026-11-11）

確認日：2026-11-11 22:50〜23:10（JST）
対象：`E:\rekishikaisetu-honnoji`（branch `master`、HEAD `9b39233`）
立場：検証のみ。**ファイルの削除・revert・stash・commit・push・描画の再実行は行っていない**。書き込みはこの文書だけ。
注意：秘密情報（`secrets/`、トークン等）は開いていない。

## 0. 結論（要約）

| 変更 | 判定 |
| --- | --- |
| `scripts/solo_spec.py` + `scripts/make_short2.py`（`end_q`） | **コミット可**。既存呼び出し・既存データへの影響はゼロ（後述の AST 確認）。ただし現時点で `end_q` を渡す台本は 0 件で、休眠機能。 |
| `shorts/kamakura_seiritsu/proto_spec.json`（credit） | **コミット可**。実際に描画済みの `-fv` 版と完全一致しており、むしろツリーが描画物に追いついていなかった状態。 |
| `scripts/_chain3.sh`（中身の置換） | **事故。復元推奨**（`git checkout -- scripts/_chain3.sh`）。内容自体は意図的だが、追跡済みの再構築ループを、再現不能な使い捨てキューで上書きしている。しかも参照先の一時ファイルは既に無く、実行すると無限に待つ。 |
| `assets/kamakura_seiritsu/fv/*.old` 3件（未追跡） | **コミットしない**。削除はオーナー判断。恒久対策は `.gitignore` に `*.old` 追加（任意の別コミット）。 |

→ 推奨は **「`_chain3.sh` を復元 → 2コミット（end_q / proto_spec）→ `.old` は除外」**。

## 1. 変更一覧

`git status --porcelain=v1 -uall` の結果（全 7 件）：

```
 M scripts/_chain3.sh
 M scripts/make_short2.py
 M scripts/solo_spec.py
 M shorts/kamakura_seiritsu/proto_spec.json
?? assets/kamakura_seiritsu/fv/clip4.mp4.old
?? assets/kamakura_seiritsu/fv/clip4_tatami.old
?? assets/kamakura_seiritsu/fv/clip5.mp4.old
```

| # | パス | 変更内容 | 推定目的 | 根拠 | リスク | 推奨 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `scripts/solo_spec.py` | `build()` の末尾に `end_q=None` を追加。出力 spec の `end_q` キーと、台本 txt の「終わりの画面のナレーション」行に前置 | 終わりの定型文の前に視聴者への問いかけを差し込めるようにする | 差分 3 箇所がすべて対で動く（引数 → spec → 台本 txt）。既定 `None` で従来文と完全一致 | 出力 JSON に常に `"end_q": null` が入るため、再生成時に既存 29 本の data spec に null キーが増える（表示上のノイズ） | コミット可（#2 と同一コミット） |
| 2 | `scripts/make_short2.py` | `nolong` 分岐の `texts[-1]` に `(spec.get('end_q') or '')` を前置（1 行） | #1 で書いた `end_q` を実際に読み上げ・字幕に反映する | `spec.get('end_q') or ''` なので未指定時は従来と同一文字列 | `end_q` が句点で終わらないと文が連結する。優先順は `is_tt+end_text` → `nolong` → `cta` のままで、他分岐には影響なし | コミット可（#1 と同一コミット） |
| 3 | `scripts/_chain3.sh` | shizugatake/sekigahara/yamazaki の再構築ループ（HEAD）が、`_queue_after_file.sh` を一時ファイル待ちで呼ぶ 2 行に置換 | koharu / torinoichi / kinrou の FreeVideo クリップを、別タスクの完了後に再生成する | 先行例 `scripts/_queue_after_mito.sh`（同じ temp ルート `b97b36f3dc9c3c26`）と `scripts/_regen4.sh` が同一パターン → 内容は意図的 | (a) 呼び先 `_queue_after_file.sh` は **未追跡（ignore）**、(b) 参照先 temp ファイルが **不在** → 履歴から再現不能、実行すると無限待ち、(c) 追跡済みの再構築ループを失う | **復元** |
| 4 | `shorts/kamakura_seiritsu/proto_spec.json` | `credit` の「背景：自作の単色グラデーション…」を「背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです…」に差し替え | `-fv`（FreeVideo 背景）版として、描画・投稿した内容に権利表記を合わせる | `data/short_proto_fv_kamakura_seiritsu.json` の `credit` と**文字列完全一致**（Python 比較で True）。描画物 `out/short_proto_fv_kamakura_seiritsu.mp4`（20:00:10）と `_description.md` に同じ表記が入っている | なし（`out/` は ignore なので spec が唯一の記録。むしろ追いついていなかった） | コミット可 |
| 5 | `assets/kamakura_seiritsu/fv/clip4.mp4.old` | 旧テイクの退避（732,306 B、17:13:34） | clip4 の取り直し前の控え | `docs/SHORTS_PRODUCTION_NOTES.md` 326〜350 行の取り直し記録（室内→板の間→屋外）と一致 | `*.mp4` は ignore だが `*.mp4.old` は **非 ignore**。`git add -A` で誤って入る。pre-push フックが素材 push を中止する | コミットしない／削除はオーナー判断 |
| 6 | `assets/kamakura_seiritsu/fv/clip4_tatami.old` | 同上（806,231 B、19:33:43） | 2 回目の取り直し（板の間）の控え | 同上（「室内はNG（現代設備と文字が混ざりやすい）」の回） | 同上 | 同上 |
| 7 | `assets/kamakura_seiritsu/fv/clip5.mp4.old` | 同上（611,734 B、17:22:50） | clip5（墨を和紙に引く）の旧テイク | 同上（「水に墨を落とす」に変更した回） | 同上 | 同上 |

3 件合計 **2,150,271 B（約 2.1 MB）**。数 GB の `.old` は無い（`Get-Item` の `Length` のみで確認し、中身は開いていない）。

## 2. 詳細

### 2.1 `end_q` の追加（make_short2.py / solo_spec.py）

**利用箇所**（`git grep -n "end_q"`、ヒットは 4 行のみ）：

| ファイル | 行 | 内容 |
| --- | --- | --- |
| `scripts/solo_spec.py` | 14 | `def build(..., hook_label=None, end_q=None)` |
| `scripts/solo_spec.py` | 24 | 出力 spec dict に `end_q=end_q` |
| `scripts/solo_spec.py` | 32 | 台本 txt の終わり画面ナレーション行に前置 |
| `scripts/make_short2.py` | 337 | `nolong` 分岐で `(spec.get('end_q') or '')` を前置 |

**供給元があるか（＝実際に効いているか）**：

- `data/*.json` に `"end_q"` は **0 件**（`short_solo_*.json` は 176 本あるが、いずれも持たない）。
- `shorts/**/*.json` にも **0 件**（`shorts/kamakura_seiritsu/proto_spec.json` のキーは `art, claims, credit, cta, hook, needs_research, notes, pron, refs, scenes, status, title` で `end_q` なし）。
- どの生成スクリプトも `build(..., end_q=...)` を渡していない。
- ドキュメントにも `end_q` の記述は無い。

→ **現時点では休眠機能**。挙動は変わらない（`None` → `''`）。

**既存呼び出しを壊さないか**：`scripts/gen_solo_*.py` 29 本の `build(...)` 呼び出しを Python `ast` で全数検査した。

- 呼び出し箇所：29
- 位置引数の最大数：**8**（`slug, title, head, answer, pron, scenes, bg_plan, notes` まで。追加引数より前で止まる）
- キーワード引数として使われている名前：`bg_note, credit, end_vid, hook_label, hook_text` のみ
- `*args` / `**kwargs` 展開：**0 件**
- `end_q` を渡している呼び出し：**0 件**

追加引数は既存キーワード引数より後ろ（末尾）に置かれているため、位置引数呼び出し・キーワード呼び出しのどちらも壊れない。両ファイルとも `compile()` で構文検査済み。

**残る注意点（コミット時に添えるとよい）**：

1. `json.dumps` は `None` を `"end_q": null` として書く。`scripts/gen_solo_*.py` を再実行すると、29 本の `data/short_solo_*.json` に無意味な null キーが増える。避けたい場合は `**({'end_q': end_q} if end_q else {})` に変える。
2. 前置は区切り文字なしの文字列連結なので、`end_q` 側を「…？ 」のように句読点で終える運用ルールが要る。
3. `nolong` 分岐は `is_tt and spec.get('end_text')` の次に評価される。TT（TikTok）spec や `end_text` 持ちには効かない仕様で、これは従来どおり。

### 2.2 `scripts/_chain3.sh` の上書き

**差分**（作業ツリー、全 2 行・217 B）：

```bash
#!/bin/bash
bash /e/rekishikaisetu-honnoji/scripts/_queue_after_file.sh "C:/Users/neoen/AppData/Local/Temp/claude/b97b36f3dc9c3c26/2afc157e-fb2d-4b13-bbf8-d55c0fb18ee4/tasks/bsd7t6ti3.output" koharu torinoichi kinrou
```

**HEAD の内容**（`git show HEAD:scripts/_chain3.sh`）：`cd /e/rekishikaisetu-honnoji` → `export PYTHONUTF8=1` → `for s in shizugatake sekigahara yamazaki` で `vp.py story/kana/audio/bgm/stage_build/desc/pack` を回し、`out/chain3_done.txt` に `DONE_$s` と `ALL` を追記する 15 行のループ。

**判断材料**：

| 確認項目 | 結果 | 意味 |
| --- | --- | --- |
| `scripts/_queue_after_file.sh` の有無 | **存在**（403 B、2026-11-08 23:54:40）。`<waitfile> <topic>...` を受け、`grep -q "ALLDONE"` で待ってから `freevideo_batch.py` を回す | 呼び出し自体は成立する形 |
| 同ファイルの git 管理 | **未追跡**。`git check-ignore -v` → `.gitignore:65:scripts/_queue*.sh` | 履歴・クローンには存在しない。`_chain3.sh` 単体では動かない |
| 参照先一時ファイル `.../tasks/bsd7t6ti3.output` | **不在**（親ディレクトリ `.../b97b36f3dc9c3c26/...` は存在し、他の `*.output` は残っている） | 再現不能。しかも `until grep -q "ALLDONE" "$W"` は不在ファイルだと grep 失敗のまま**無限ループ**（20 秒ごとに stderr）。今実行するとハングする |
| 他の `_chain*.sh`（追跡済み 10 本） | すべて `cd /e/...` + `export PYTHONUTF8=1` + `vp.py` の再構築ループ | `_chain3.sh` はこのファミリーの一員だった |
| `out/chain3_done.txt` | 51 B、2026-10-25 19:08 | HEAD 版は実際に使われた記録がある |
| 追跡済みスクリプトで `AppData/Local/Temp/claude` を含むもの | **`_chain3.sh` のみ**（`git grep -ln`） | このパスをコミットする前例は無い |
| 先行する同型の使い捨て | `scripts/_regen4.sh`（`until grep -q REGENDONE "…/tasks/b4uwykljo.output"`）、`scripts/_queue_after_mito.sh`（同じ temp ルート、`F=` に一時ファイル） | 内容は「一時ファイル待ち → freevideo_batch」の定型的な使い捨て。**書いた本人の意図は明確** |
| `.gitignore` の設計意図 | 65 行目付近のコメント「使い捨てのキュー/再生成シェル（一時パスを参照するため再現できない。再生成は make_spec_*.py → vp.py / make_short2.py）」 | リポジトリの規約上、こうしたスクリプトは**コミットしない**もの |

**結論**：**内容は意図的、ファイル選択が事故**。タスクを待たせて FreeVideo を回す使い捨てを、たまたま空いていた（ように見えた）追跡済みファイル `_chain3.sh` に上書きしたもの。結果として (1) 復元可能な再構築ループが失われ、(2) 参照先が消えた再現不能な 2 行が残り、(3) 実行するとハングする、という三重の悪化。

**復元案**：

```bash
git checkout -- scripts/_chain3.sh        # HEAD の再構築ループに戻す
# 使い捨てとして残したい場合のみ（ignore 対象なのでコミットされない）
# scripts/_queue_kamakura_fv.sh のような別名で新規作成する
```

`git checkout --` を使う理由：作業ツリーの内容に救うべき情報が無い（一時ファイルは既に無い）。もし「koharu/torinoichi/kinrou を再生成した」という事実を残したいなら、スクリプトではなく `docs/SHORTS_PRODUCTION_NOTES.md` に 1 行書くのが筋。

### 2.3 `shorts/kamakura_seiritsu/proto_spec.json` の credit

**差分**：`credit` の 1 行目だけが「背景：自作の単色グラデーション（画像素材は使用していません）」→「背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の風景・史実の再現ではありません」。他は同一（末尾改行なしも HEAD と同じ）。

**描画済みの動画と一致するか**：

| 確認 | 結果 |
| --- | --- |
| `data/short_proto_fv_kamakura_seiritsu.json`（`-fv` 版の描画入力）の `credit` | 作業ツリーの `proto_spec.json` と**完全一致**（Python で比較して True） |
| 同 data ファイルの mtime | 2026-11-11 19:58:06（= `proto_spec.json` の mtime と同一） |
| 同 data ファイルの初出コミット | `544353c feat(shorts): kamakura_seiritsu の FreeVideo 背景版を描画…`（**HEAD に既にコミット済み**） |
| 描画物 `out/short_proto_fv_kamakura_seiritsu.mp4` | 2026-11-11 20:00:10（credit 変更 19:58:06 より後＝新しい表記で描画されている） |
| `out/short_proto_fv_kamakura_seiritsu_description.md` | 「・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の風景・史実の再現ではありません」を含む（credit は `make_short2.py` の説明欄生成で埋め込まれる） |
| `out/` の git 管理 | `.gitignore:4:out/` で **ignore**。描画物は git に無い → spec が唯一の記録 |
| HEAD `9b39233`（"AI使用を明示"）の変更 | `data/youtube_ids.json` と `docs/SHORTS_PRODUCTION_NOTES.md` のみ。`proto_spec.json` は未更新のまま残っていた |

**結論**：作業ツリーの変更は「描画・投稿した内容に spec を追いつかせる」もの。`shorts/` 配下の spec が単色背景のままだと、後から見た人が「この動画は単色背景で作られた」と誤読する。**コミットすべき**。

### 2.4 `.old` 3 件

| ファイル | サイズ (B) | 更新時刻 | 追跡 | ignore |
| --- | --- | --- | --- | --- |
| `assets/kamakura_seiritsu/fv/clip4.mp4.old` | 732,306 | 2026-11-11 17:13:34 | 未追跡 | **されない** |
| `assets/kamakura_seiritsu/fv/clip4_tatami.old` | 806,231 | 2026-11-11 19:33:43 | 未追跡 | **されない** |
| `assets/kamakura_seiritsu/fv/clip5.mp4.old` | 611,734 | 2026-11-11 17:22:50 | 未追跡 | **されない** |
| 合計 | 2,150,271 | — | — | — |

- `git check-ignore -v` は 3 件とも **exit 1（非 ignore）**。`.gitignore:21 *.mp4` は `.mp4.old` に一致せず、`*.old` の規則が無い。
- 一方 `assets/kamakura_seiritsu/fv/` で追跡されているのは `prompts.json` だけで、`clip*.mp4` は `*.mp4` により ignore。
- `.old` は手動退避と見られる（`git grep -n "\.old" -- scripts` は **0 件**＝`freevideo_batch.py` などが自動で作る命名ではない）。
- 由来は `docs/SHORTS_PRODUCTION_NOTES.md` 326〜350 行の取り直し記録と一致：clip4 は「室内（白いエアコン＋文字入り掛け軸）」→「板の間」→「屋外の竹林」の 3 段階、clip5 は「墨を和紙に引く（筆先が映る）」→「水に墨を落とす」。現行 `clip4.mp4`（19:53:56）と `clip5.mp4`（19:42:28）が採用版。
- 危険：`git add -A` / `git add .` で 2.1 MB の旧素材がステージされる。さらに `scripts/hooks/pre-push` は「素材（画像・動画・音声・PDF 等）を含む push を中止する」ため、push が失敗するか、テキストのみ push の運用（`scripts/main_push_textonly.py`）を崩す。

**推奨**：コミットしない。取り直しの経緯は既に docs に記録済みなので、消しても情報は失われない。ただし削除はこのレビューの範囲外（オーナー判断）。恒久対策は `.gitignore` に `*.old` を追加する別コミット（`*.bak` は既に ignore されているのに `*.old` だけ抜けている）。

## 3. コミット分割案

前提：`_chain3.sh` は**コミットせず復元**。`.old` は**コミットしない**。`git add -A` は使わない。

| 順 | 操作 | パス | メッセージ案 |
| --- | --- | --- | --- |
| 0 | 復元（コミット不要） | `scripts/_chain3.sh` | — |
| 1 | コミット | `scripts/solo_spec.py`, `scripts/make_short2.py` | `feat(shorts): 終わりの定型文の前に問いかけ(end_q)を前置できるようにする` |
| 2 | コミット | `shorts/kamakura_seiritsu/proto_spec.json` | `docs(shorts): kamakura_seiritsu の試作spec のcreditを、描画済みのFreeVideo版に合わせる` |
| 3 | 任意コミット | `.gitignore` | `chore: 退避した素材(*.old)を誤ってコミットしないよう ignore に追加` |

実行コマンド例（このレビューでは実行していない）：

```bash
cd /e/rekishikaisetu-honnoji
git checkout -- scripts/_chain3.sh

git add scripts/solo_spec.py scripts/make_short2.py
git commit -m "feat(shorts): 終わりの定型文の前に問いかけ(end_q)を前置できるようにする" \
           -m "build() に end_q を追加し、nolong 分岐と台本txtに反映する。未指定時は従来と同一文字列。既存のbuild呼び出しは全て位置引数8個までで、末尾へのキーワード引数追加のため影響なし。"

git add shorts/kamakura_seiritsu/proto_spec.json
git commit -m "docs(shorts): kamakura_seiritsu の試作spec のcreditを、描画済みのFreeVideo版に合わせる" \
           -m "data/short_proto_fv_kamakura_seiritsu.json と out/ の描画物・説明欄の表記に一致させた。"

# 任意
git add .gitignore && git commit -m "chore: 退避した素材(*.old)を誤ってコミットしないよう ignore に追加"

# .old は追加しない（必要なら削除はオーナー判断）
```

コミットを分ける理由：#1 は共通部品（solo_spec / make_short2 の両方に波及）、#2 は特定 Shorts の記録で、revert 单位が違う。#3 はリポジトリ全体の設定で、上記 2 つとは独立。

## 4. 確認に使ったコマンドと結果（再現用）

PowerShell（`cd E:\rekishikaisetu-honnoji`）で実行。結果は上記の各表に反映済み。

```powershell
# 全体像
git status --porcelain=v1 -uall
git --no-pager diff --stat
git --no-pager diff
git --no-pager log -12 --oneline

# end_q の利用箇所と供給元
git --no-pager grep -n "end_q"          # → make_short2.py:337 / solo_spec.py:14,24,32 の4行のみ
Select-String -Path 'data\*.json' -Pattern '"end_q"' -SimpleMatch -List      # → 0件
Get-ChildItem -Recurse -Path shorts -Filter '*.json' |
  Select-String -Pattern 'end_q' -SimpleMatch -List                          # → 0件
(Get-ChildItem data -Filter 'short_solo_*.json').Count                       # → 176

# build() 呼び出しの全数検査（Python ast）
python -c "..."   # scripts/gen_solo_*.py 29本を ast.parse し、build() の位置引数数・キーワード名・**kwargs の有無を列挙
                 # → 呼び出し29箇所 / 位置引数最大8 / *args,**kwargs 0 / end_q を渡す呼び出し 0
python -c "import ast; [compile(open(p,encoding='utf8').read(),p,'exec') for p in ['scripts/make_short2.py','scripts/solo_spec.py']]"

# _chain3.sh の正体
git --no-pager diff -- scripts/_chain3.sh
git --no-pager show HEAD:scripts/_chain3.sh
Test-Path scripts/_queue_after_file.sh          # → True（403 B、2026-11-08 23:54:40）
Get-Content scripts/_queue_after_file.sh
git ls-files --error-unmatch scripts/_queue_after_file.sh      # → pathspec 不一致（未追跡）
git check-ignore -v scripts/_queue_after_file.sh               # → .gitignore:65:scripts/_queue*.sh
Test-Path 'C:\Users\neoen\AppData\Local\Temp\claude\b97b36f3dc9c3c26\2afc157e-fb2d-4b13-bbf8-d55c0fb18ee4\tasks\bsd7t6ti3.output'   # → False
Get-ChildItem 'C:\Users\neoen\AppData\Local\Temp\claude\b97b36f3dc9c3c26\2afc157e-fb2d-4b13-bbf8-d55c0fb18ee4\tasks'               # → 親は存在（他の *.output あり）
git ls-files 'scripts/*.sh'                     # → _chain3.sh は追跡、_queue_after_file.sh は無い
foreach($f in (git ls-files 'scripts/_chain*.sh')){ (Get-Content $f -TotalCount 2) -join ' | ' }   # 他10本は cd + PYTHONUTF8
git --no-pager grep -ln "AppData/Local/Temp/claude" -- scripts    # → _chain3.sh のみ
Get-Item out\chain3_done.txt                    # → 51 B、2026-10-25 19:08
Get-Content scripts/_regen4.sh, scripts/_queue_after_mito.sh      # → 同型の「一時ファイル待ち」

# proto_spec.json の credit 照合
git --no-pager log --oneline -- shorts/kamakura_seiritsu/proto_spec.json   # → ec0a9a3 のみ
git --no-pager show HEAD:shorts/kamakura_seiritsu/proto_spec.json
git --no-pager log --oneline -3 -- data/short_proto_fv_kamakura_seiritsu.json   # → 544353c
python -c "import json;d=json.load(open('shorts/kamakura_seiritsu/proto_spec.json',encoding='utf8'));d2=json.load(open('data/short_proto_fv_kamakura_seiritsu.json',encoding='utf8'));print(d['credit']==d2['credit'])"   # → True
Get-Item out\short_proto_fv_kamakura_seiritsu.mp4, shorts\kamakura_seiritsu\proto_spec.json | Select Name,Length,LastWriteTime
Select-String -Path out\short_proto_fv_kamakura_seiritsu_description.md -Pattern '背景|AI' -Encoding utf8
git --no-pager show --stat 9b39233              # → data/youtube_ids.json と docs のみ

# .old 3件
Get-ChildItem assets\kamakura_seiritsu\fv | Select Name,Length,LastWriteTime
foreach($f in 'clip4.mp4.old','clip4_tatami.old','clip5.mp4.old'){ git check-ignore -v "assets/kamakura_seiritsu/fv/$f" }   # → 3件とも exit 1（非 ignore）
git ls-files 'assets/kamakura_seiritsu/fv/*'    # → prompts.json のみ
(Get-ChildItem 'assets\kamakura_seiritsu\fv\*.old' | Measure-Object Length -Sum).Sum   # → 2150271
git --no-pager grep -n "\.old" -- scripts       # → 0件（自動生成ではない）

# 安全確認
git --no-pager diff --check                     # → 出力なし（空白エラーなし）
git config --get core.autocrlf                  # → true（作業コピーは CRLF。_chain3.sh は LF で警告が出る）
```

## 5. 未確認・制約

- **描画・音声合成は再実行していない**（禁止事項）。`end_q` を実際に渡したときの VOICEVOX の読み・字幕の改行・尺は未確認。
- `end_q` を渡す台本が存在しないため、機能としての動作確認は「コードの型・呼び出し安全・未指定時の文字列一致」まで。実データでの確認は未了。
- YouTube にアップロード済みの動画の説明欄そのものは確認していない（Studio / API は操作範囲外）。確認したのは `out/` のローカル生成物と `data/youtube_ids.json` の記録のみ。
- `_chain3.sh` の上書きが「同じセッション内の事故」か「別セッションからの意図的な再利用」かは、ファイル内容と更新時刻（2026-11-09 0:20、`_queue_after_file.sh` 作成の 26 分後）からの推定。書いた本人の意図を示すログは残っていない。
- `.old` 3 件の中身（映像）は開いていない。サイズ・更新時刻・命名・docs の記録からの推定。
