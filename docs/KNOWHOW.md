# ノウハウの入口（まずこれを読む）

更新日: 2026-11-26。**制作で分かったことは必ず git に残す**（AGENTS.md）。この文書は「どこに何が書いてあるか」の索引。

**AIレビューは厳しめに**（2026-11-26 オーナー指示）。「公開可」をそのまま受け取らず、低重大度の指摘も原文・実フレームで照合し、根拠を超えた表現を actively 探す。詳細は [`SHORTS_PRODUCTION_NOTES.md`](SHORTS_PRODUCTION_NOTES.md) の「AIレビューは厳しめに」節。

既存ShortをFreeVideo背景に作り直すときの実測（古い spec の `vid` 差し替え、同じID差し替え不可、根拠テーブル、Studio の AI 設定）は [`SHORTS_PRODUCTION_NOTES.md`](SHORTS_PRODUCTION_NOTES.md) の「既存ShortをFreeVideo背景に作り直す」節。夕焼けShortの7シーン分の背景生成と、clip5 の電柱・電線を構図変更で直した実測は同文書の「夕焼けShortのFreeVideo背景」節、対応表は `data/solo_sunset_art_map.json`。

エージェントチームの役割分担・受け渡し・ゲートは [`AGENT_TEAM.md`](AGENT_TEAM.md)。Shorts 制作を複数エージェントで進めるときは、担当を起動する前にまずこの定義を読む。動画に触れる担当は各自で `VIDEO_CREATION_PRECHECK.md` と `SOLO_SHORT_PROCEDURE.md` を読む必要がある。

夕焼けShortの成果物判定（`_fv` が元ファイルと SHA256 完全一致した実測）、修正台本を上書きせず別 slug で再描画する手順、kana・字幕・末尾3カードの確認結果は [`SHORTS_PRODUCTION_NOTES.md`](SHORTS_PRODUCTION_NOTES.md) の「夕焼けShortの成果物判定と修正台本の再描画」節。`make_short2.main()` は slug から出力名を決めるので、**slug を変えないと既存 mp4 を上書きする**。

新規動画のテーマ提案・着手前は、台帳（`data/youtube_ids.json`）に加えて `docs/` 全体（SHORTS_PRODUCTION_NOTES / research / themes）を grep して既出を確認すること（2026-11-23 にオーナー指示。「1円玉」が制作済みだった見落としによる）。

視聴傾向とコメント（10件以上）からの関心トピック分析は [`research/20261126_audience_topics_from_ask_studio.md`](research/20261126_audience_topics_from_ask_studio.md)。3分類（経済・時事／歴史の通説のウラ／自然科学・天文の検証）と、議論が活性化する結びの投げかけを記録している。新規題材の選定と台本の結び方に使う。

2026-11-23 に AGENTS.md の「イラスト・背景画像は必ずChatGPTに依頼する」を削除し、「背景映像は FreeVideo の AI 映像を使う」に置き換えた（オーナー確認）。古い記述を見て ChatGPT 画像生成を前提にしないこと。

味覚マップ制作の振り返りは [`research/20261123_tongue_taste_map_retro.md`](research/20261123_tongue_taste_map_retro.md)。ルールファイルの古さ、予約枠の重複、カタカナ字幕と発音辞書の両立、動画添付の別ポート回避などを記録している。公開後の比較記録の準備は [`research/20261123_tongue_taste_map_followup.md`](research/20261123_tongue_taste_map_followup.md)。

**チャンネル全体の運営方針は [`CHANNEL_STRATEGY_20261124.md`](CHANNEL_STRATEGY_20261124.md)。** 収益化の2段階（早期アクセス500人・本則1,000人）、長尺とShortの役割分担、投稿枠（長尺 火金19:00／Short 火金20:00と木・土12:00）、週次カレンダーをまとめてある。個々の制作手順より上位の方針なので、題材や投稿ペースを変える前に必ず読む。

**ニッチの決定と100本の題材候補は [`NICHE_AND_100_IDEAS_20261124.md`](NICHE_AND_100_IDEAS_20261124.md)。** サジェストAPIの実測（`data/suggestion_20261124.json`）で需要を確かめ、全384本との既出照合を済ませた100本を採点順に並べてある。新しい題材を出す前に、まずこの表に無いかを確認する（重複した3本は差し替え済み）。

**アルゴリズム指標ごとの成長戦略は [`YOUTUBE_ALGORITHM_GROWTH_STRATEGY.md`](YOUTUBE_ALGORITHM_GROWTH_STRATEGY.md)。** インプレッション、動画別CTR、スワイプ率、視聴時間、リピーター、検索流入、関連動画の導線を実測値つきで整理し、テスト方法と週次計測を設計してある。動画別CTR、トラフィックソース、視聴者属性、リピーター回数は未取得と明記している。**Shortの台本設計の型は [`YOUTUBE_GROWTH_SYSTEM.md`](YOUTUBE_GROWTH_SYSTEM.md)**（CTR・維持率を設計するフック／タイトル／サムネイル／構成／CTAのルール）。**AI活用の制作ワークフローは [`AI_PRODUCTION_WORKFLOW.md`](AI_PRODUCTION_WORKFLOW.md)**（工程ごとの道具・テンプレート・公開前チェックリスト・人が残す場所）。**収益化システム一式は [`MONETIZATION_SYSTEM.md`](MONETIZATION_SYSTEM.md)**（YPP申請準備、AdSense、各収入源の導入時期、権利の未確認、リスク）。**パフォーマンス分析システムは [`ANALYTICS_SYSTEM.md`](ANALYTICS_SYSTEM.md)**（指標ごとの取得状況、成功パターンの実測、低パフォーマンスの切り分け、週次・月次レビュー、未取得のTo Do）。題材や投稿ペースを変える前に、まず運営方針とこの5つを読む。

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
- 日々の Short（solo／ペア共通）は `data/short_*.json` に `claims[]` / `needs_research[]` と `scenes[].claim_ids` を書き、`python scripts/check_short_evidence.py <spec>` を通す。答えを変えない未確認は理由を添えて `needs_research` に残す（[`SHORT_EVIDENCE_GATE_20261120.md`](SHORT_EVIDENCE_GATE_20261120.md)）
- **`python` は Windows Store のスタブでゲートが実行できない**（2026-11-26、夕焼けShortで実測）。`python scripts/check_short_evidence.py ...` は `[exit code: 1]` で stderr に `Python` だけ出る。`C:/Users/neoen/AppData/Local/Programs/Python/Python312/python.exe` を明示すると実行でき、出力は文字化けするが終了コードと「OK／ERROR」は読める。
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
