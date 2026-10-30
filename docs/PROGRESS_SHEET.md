# 制作進捗シートの使い方・メンテ方法

動画ごとの進み具合を、複数のエージェントと人で共有するための管理シート。

- URL：https://claude.ai/artifact/J4ZSSj2X5X2BLJEtXVciy8 （作成：2026-10-21。持ち主のみ閲覧可。他のエージェントや人に見せるときは、ページの共有メニューで共有する）
- 中身：Claude の Artifact（ページ）＋共有データベース（`db`）。ページの表示はデータから自動で作られる。**表の数字や行は、データを直せば直る。ページ（HTML）を作り直す必要はない。**
- データの置き場：コレクション `videos`（動画1本＝1件）と `todos`（要対応）。

## 1. 工程の決まり（stage）

| stage | 工程 | 目安（これが済んだら次へ） |
|---|---|---|
| 0 | 題材 | 題材が決まった |
| 1 | 事実確認 | `08_fact_check.md` ができた |
| 2 | 台本 | 台本v2ができた（ChatGPT web査読の反映まで） |
| 3 | 画像・図 | 画像と、必要な動く図が揃った |
| 4 | 動画制作 | `vp.py build` が通り、QA（黒フレームなし・音量）が通った |
| 5 | Codex確認 | 通し視聴・読み確認の指摘を反映した |
| 6 | 非公開アップ | YouTube に非公開で上がった（動画ID あり） |
| 7 | 予約済み | 公開日時（日本時間19:00）を設定した |
| 8 | 公開済み | 公開された |

- **止まっている**ときは、`blocked: true` と `blockReason`（理由）を書く。進捗バーが赤になり、「止まっている」の絞り込みに出る。
- **Short** は、工程とは別に `shortStatus` で管理する（なし／作成中／アップ済み／予約済み／公開済み）。

## 2. 1本ぶんの項目（`videos/<slug>`）

| 項目 | 内容 |
|---|---|
| `title` | 画面に出す短い題名 |
| `category` | 分野（天文・暦・医学など） |
| `type` | 構成の型（A 答え先出し／B 逆転／C 仕組み。不明なら空） |
| `stage` | 0〜8 の数（上の表） |
| `shortStatus` | Short の状態 |
| `publishAt` | 公開日 `YYYY-MM-DD`（時刻は常に日本時間19:00。Shortは20:00） |
| `longId` / `shortId` | YouTube の動画ID（長尺／Short） |
| `owner` | 担当（Claude／Codex／人 など） |
| `note` | メモ（注意点・次にやること） |
| `blocked` / `blockReason` | 止まっているか／その理由 |
| `updated` | 最終更新 `YYYY-MM-DD HH:MM`（日本時間） |

`<slug>` は `data/<slug>_spec.json` の slug と同じ（例：akashi、gps、rice、oceanblue）。新しい動画は、新しい slug で行を足す。

## 3. 更新のしかた

### A. ページから（人向け）
1. ページを開き、動画の行を押す。
2. 工程・Short・公開日・担当・メモなどを直し、「保存」を押す。
3. 「要対応」は、チェックで完了、「追加」でやることを足せる。

### B. Claude のエージェントから（`ArtifactData` ツール）
`url` は上記のURL。書く前に、その行を一度読んで `version` を取り、`if_version` を付ける（他の人の更新を上書きしないため）。

- 工程を進める（例：標準時を「Codex確認」に）：`update`、`collection: videos`、`doc_id: akashi`、`data: {"stage": 5, "updated": "2026-10-22 10:30"}`
- 新しい動画を足す：`set`、`collection: videos`、`doc_id: <slug>`、`data`（上の表の項目をすべて入れる。`stage: 0`、`shortStatus: "なし"`、`blocked: false`）
- 数本まとめて：`batch`（1回50件まで）
- 要対応を足す：`set`、`collection: todos`、`doc_id: t09` など、`data: {"text": "…", "who": "…", "status": "open", "video": "<slug>", "created": "…"}`
- 要対応を終える：`update`、`data: {"status": "done"}`
- 項目を消す：`update` で `{"項目名": {"__delete__": true}}`

### C. Codex など、ツールで書けないエージェント
Codex は直接書けない。作業の最後に、**Claude か人に「どの動画が、どの工程まで進んだか」を伝えて**、書いてもらう。

その「伝える」を自動にするのが `scripts/sync_progress_sheet.py`（OpenCode / Codex 側）。

```
python scripts/sync_progress_sheet.py
```

リポジトリの実状態（`data/youtube_ids.json`、`data/publish_snapshot.json`、`out/*.mp4`、`docs/themes/<…>`、`out/codex/qa_lint.txt`）から、次の3つを出す。

| 出力 | 中身 |
|---|---|
| `data/progress_sheet.json` | あるべき行の正本（版管理できる。差分は git で見る） |
| `out/codex/progress_sheet.md` | 人が読める表（そのままチャットに貼れる） |
| `out/codex/progress_batch.json` | `ArtifactData` の `batch` にそのまま渡せる `update`（videos）と `set`（todos） |

- **`update` だけを出す**（`category`・`type`・`owner` は人が決めた値なので触らない）。
- slug は `data/<slug>_spec.json` の slug。spec が無い古い3本（worldmap / honnoji / ninja）は Short の `long_id` から引く。
- 公開状態はスナップショット時点。**クォータ切れで `check_publish.py --write` が通らない日は、公開時刻を過ぎた予約を「公開済み」として扱う**（YouTube は予約時刻に自動公開するため）。
- **`data/pending_replace.json`** に載っている slug は、note に「差し替え待ち」と入り、要対応に「差し替え（理由・公開日・約2,200ユニット）」が立つ。`replace_versions.py` が差し替えに成功すると、その slug を自動で外す。
- 反映は Claude（`ArtifactData`）か人が行う。反映したら、その旨を `note` か この文書に残す。

## 4. 運用のきまり

1. **工程が終わったら、その場で更新する**。終わった順に stage を進め、`updated` と `note` も書く。
2. **戻すときも書く**。作り直しになったら、stage を戻して、理由を `note` に残す。
3. **公開の予約を入れたら** stage を 7 にして、`publishAt` と ID を入れる。**作り直して別IDで上げ直したら**、`longId` を新しいIDにして、旧版を削除したことを `note` に書く（旧版が残ると、同じ時刻に2本公開される）。
4. **公開日を過ぎたら**、YouTube で公開されたか確かめて、stage を 8 にする（ページの「公開日を過ぎています」が目印）。
5. **このシートは進捗の記録で、事実の正本ではない**。動画IDと公開状態の正本は YouTube（`yt_api.py list`）と `data/youtube_ids.json`、題材ごとの詳細は `docs/themes/<日付_slug>/` にある。食い違ったら、YouTube を正としてシートを直す。
6. 書き込みは、**他の人の行を消さない・全体を作り直さない**。1行ずつ `update` する。
7. 要対応は、**公開前に必ず片づけること**を優先して上に置く（旧版の削除、原本の確認など）。完了したら、削除せずチェックを付けて残す（履歴になる）。

## 5. 週の点検（目安）

- 月曜：全行を見て、stage と公開日のずれを直す。**予約済みの在庫が7日分を下回っていないか**を見る（`docs/PRODUCTION_CYCLE.md`）。
- 公開の翌日・7日後：反応の数字を `data/channel_profile.json` に追記する（シートには入れない）。
- 月初：公開済みの古い行は消さずに残す（分野・型の偏りを見るため）。

## 6. 壊れたとき

- **ページが「データを読み込めません」と出る**：サインインしていない、または権限がない。ページの共有設定を確認する。
- **保存できない**：その人の権限が閲覧のみ。編集権限をもらうか、Claude に頼む。
- **行を誤って消した**：`set` で同じ `doc_id` に作り直す（項目は上の表）。
- **ページの見た目を変えたい**：Claude に「シートの表示を直して」と頼む（データはそのまま残る）。ページを作り直しても、データは消えない。

## 7. 付記

- 初期データは、2026-10-21 時点の YouTube の一覧（API）と、`data/youtube_ids.json` から転記した。
- 工程の目安は、このリポジトリの制作の流れ（`docs/PRODUCTION_CYCLE.md`、`docs/VIDEO_PIPELINE_VP.md`）に合わせている。
