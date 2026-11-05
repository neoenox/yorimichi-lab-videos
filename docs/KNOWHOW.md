# ノウハウの入口（まずこれを読む）

更新日: 2026-11-05。**制作で分かったことは必ず git に残す**（AGENTS.md）。この文書は「どこに何が書いてあるか」の索引。

## 1. 動画を作るときに読む順番

| 順 | 文書 | 内容 |
| --- | --- | --- |
| 1 | [`VIDEO_CREATION_PRECHECK.md`](VIDEO_CREATION_PRECHECK.md) | 制作前の必須確認（工程・根拠と演出の分離・未確認を完了扱いしない） |
| 2 | [`SHORTS_STANDARD_INTEGRATION.md`](SHORTS_STANDARD_INTEGRATION.md) | Shorts 制作標準の使い方・既存パイプラインとの差分・検査の階層 |
| 3 | [`SHORTS_PRODUCTION_NOTES.md`](SHORTS_PRODUCTION_NOTES.md) | **実測ノウハウ本体**（画面の安全領域、資料画像、AI生成、投稿、失敗と対処） |
| 4 | [`VIDEO_PRODUCTION_RUNBOOK.md`](VIDEO_PRODUCTION_RUNBOOK.md) | 長尺の手順（VOICEVOX・描画・公開・トラブル対処） |
| 5 | [`MAIN_TEXT_ONLY_WORKFLOW.md`](MAIN_TEXT_ONLY_WORKFLOW.md) | リモートへ素材を上げない運用（push の作法） |

## 2. ツール（スクリプト）と役割

| スクリプト | 役割 | 実測 |
| --- | --- | --- |
| `scripts/shorts_standard.py` | 標準 JSON の検査（`validate.py` 実行＋追加規則）とレンダラ spec への変換 | 2026-11-04 |
| `scripts/gen_image_cdp.py` | **ChatGPT の画像生成**（Chrome を CDP で操作、blob 画像を canvas 経由で取得） | 2026-11-05 |
| `scripts/studio_cdp.py` | **Studio の公開設定・字幕**（Playwright、チャンネルID検証つき） | 2026-11-05 |
| `scripts/chatgpt_image.py` | bsk 経由の画像生成（**不安定・非推奨**。CDP 版を使う） | 2026-11-05 |
| `scripts/make_short2.py` | 縦型 Short の描画（1080x1920、VOICEVOX、FFmpeg） | 既存 |
| `scripts/pack_short.py` | 投稿パック作成（`--tags=` で単独 Shorts も可） | 2026-11-04 |
| `scripts/main_push_textonly.py` | 素材を含めずに main を更新（`--path` で範囲限定） | 2026-11-04 |
| `scripts/install_git_hooks.py` | pre-push（素材の push 防止）/ pre-commit（Shorts 検査） | 2026-11-04 |

## 3. これだけは覚えておく（要点）

### 制作
- Shorts は **brief → result.json → check → to-spec → 描画**。`needs_review` のままでは `to-spec` が通らない
- 画面の安全領域: タイトル y≈200（**全角18文字まで**）／大テロップ y≈520／字幕 1470–1540／注記は 1556 以降
- 背景は **シーンごとに変える**（`art_map.json`）。同じ絵が続くと単調
- 明るい画像の上に字幕を置くときは、**下半分に暗幕**を入れる（入れないと読めない）

### 根拠
- claims は `source_type: primary`（一次資料URL必須）か `ai_assistant`（AI回答可・WARN が出る）
- 数字・固有名詞・因果関係は可能なら一次資料で裏取り。誤りが判明したら概要欄で訂正

### ブラウザ自動化（重要）
- **Studio と画像生成は CDP + Playwright を使う**（bsk はクリックが弾かれ、ラベルが文字化けする）
- Chrome は `--remote-debugging-port=9222 --user-data-dir=C:\Users\neoen\.chrome-automation` で起動
- 未ログイン・チャンネル違いを検知したら**止まる**（無限リトライしない）
- ChatGPT の生成画像は `blob:` URL。**ページ内 canvas → toDataURL** で取り出す
- Studio の公開設定は `ytcp-icon-button#select-button`（同じ id が4つあるので限定する）

### 公開
- API は**常に private** でアップロード。公開は Studio（または `studio_cdp.py publish`）
- 公開判定は `https://www.youtube.com/oembed?url=...&format=json` が **200/403** で確認できる
- API クォータは**残量で落ち方が変わる**（captions 400 units が落ちても videos.update 50 units は通ることがある）
- 1日のクォータ回復は太平洋時間の深夜（日本時間の夕方ごろ）

### 記録
- 失敗したら「症状 → 原因 → 対処」を [`SHORTS_PRODUCTION_NOTES.md`](SHORTS_PRODUCTION_NOTES.md) に追記する
- 再現できる粒度で書く（URL形式、切り出し比率、セレクタ、コマンド）

## 4. 直近の実例（時系列）

| 日付 | 題材 | 学んだこと |
| --- | --- | --- |
| 2026-11-04 | `edo_map_date`（江戸図の年代） | NDL の IIIF 画像利用、資料の切り出し、タイトル文字数、`long_id` 任意化 |
| 2026-11-05 | `shodo_heritage`（書道の無形文化遺産） | ニュース題材、AI生成背景、日付表示、CDP での画像取得と Studio 操作 |

## 5. 未対応・残課題

- 画像は API（`OPENAI_API_KEY`）にできれば最も安定（ブラウザは UI 変更に弱い）
- 既存の `data/short_*.json`（旧形式）の標準形式への移行
- 長尺と Shorts の自動ペアリング（現在は手動）
