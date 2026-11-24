# Shorts 制作エージェントチーム定義

作成日: 2026-11-24。目的は、YouTube Shorts の制作全工程を役割ごとに分担し、`AGENTS.md` と `docs/KNOWHOW.md` のルールを各担当が自分で守れるようにすること。ここに書いた役割は DSH のサブエージェント（`lead` 配下）として起動する前提。

## 全員に共通するルール

どの担当も、作業を始める前に次を読む。親が読んだだけでは代わりにならない。

1. `AGENTS.md`（ルート）全文
2. `docs/VIDEO_CREATION_PRECHECK.md` 全文（動画・素材・台本・字幕・音声・レンダリングに触れる場合）
3. `docs/KNOWHOW.md` と、そこから辿れる自分の工程の文書（`SHORTS_PRODUCTION_NOTES.md` / `SHORTS_STANDARD_INTEGRATION.md` / `SOLO_SHORT_PROCEDURE.md` / `shorts-standard/README.md` / `PROMPT.md` など）

守る要点は次のとおり。

- **新規題材は提案・着手前に既出チェック**。台帳 `data/youtube_ids.json` を見るだけでは足りず、`docs/` 配下（`SHORTS_PRODUCTION_NOTES.md`、`research/`、`themes/`、`NICHE_AND_100_IDEAS_20261124.md`）を grep する。重複が見つかったら提案を取り下げる。
- **単独 Short の工程に触れる担当は、自分で `docs/SOLO_SHORT_PROCEDURE.md` を全文読み、`scripts/read_procedure.py` の全部分表示と確認問題に答える**。印が無い状態で `gen_solo_*.py` / `solo_ship.py` / `solo_schedule.py` を実行しない。印の偽造と `PROCEDURE_ACK_SKIP=1` は禁止。
- **Shorts 制作標準 v1.2 を緩めない**。`shorts-standard/README.md` / `PROMPT.md` / `output.schema.json` に従う。形式検査は `scripts/shorts_standard.py check`、根拠ゲートは `scripts/check_short_evidence.py`。`needs_review` / `needs_research` が残る JSON を `to-spec` に渡さない。
- **背景映像は FreeVideo**（`bash scripts/fv_clips.sh <slug> clipN`）。自作してよいのはデータ由来の図・地図だけ。「イメージです」を概要欄に明記し、アップ時に AI の使用＝はいを設定する。
- **ニュース系は日付を年月日で**。「2026年11月5日時点」のような過去版表示を画面・ナレーション・説明欄・タイトルに入れる。
- **根拠と演出を分ける**。未確認の数字・発言・因果関係を書かない。推測は推測と明記し、確認した範囲と未確認の範囲を分けて報告する。
- **元成果物を守る**。完成候補を上書きせず、試作・編集版・完成版を別名で分ける。既存スクリプト・動画を勝手に消さない。
- **レビューは Google AI モード**。台本は Google AI モード＋ChatGPT の併用。AI の指摘は必ず根拠の原文と実フレームで照合して採用・不採用を決め、判断を `docs/research/` に残す。Muse は起動しない。
- **動画の生成・デコード成功をもって投稿可と宣言しない**。連続視聴、全編の実聴、字幕同期、史実照合、スマホ可読性は別のゲートとして扱う。
- **ノウハウはその場で git に残す**。まず `docs/KNOWHOW.md` を更新し、必要な追記先（`SHORTS_PRODUCTION_NOTES.md` / `SHORTS_STANDARD_INTEGRATION.md` / `VIDEO_PRODUCTION_RUNBOOK.md`）に書いてコミットする。

## 役割一覧

`lead`（このセッションのルートエージェント）が進行役。各担当は独立したサブエージェントとして起動し、`send_message` で指揮する。担当名は起動時の `name` に合わせる。

| 担当名 | 役割 | 主な入力 | 主な成果物 |
| --- | --- | --- | --- |
| `scout` | 題材選定と既出チェック | 台帳、`docs/` 全体、`NICHE_AND_100_IDEAS_20261124.md`、サジェスト実測 | 重複なしと確認した題候補、選定理由、必要な一次資料のリスト |
| `researcher` | 一次資料の調査と根拠テーブル作成 | 題材、出典候補 URL | `brief.yaml` の `source_urls` / `verified_facts` / `needs_research`、`data/short_*.json` の `claims[]`、調査記録 `docs/research/` |
| `scriptwriter` | 台本構成と標準 JSON | 調査結果、`shorts-standard/PROMPT.md` | `shorts/<slug>/result.json`（疑問→方向性→根拠→回収、30〜45秒、5〜7シーン）、`brief.yaml`。単独 Short は `solo_spec.build()` 経由 |
| `asset maker` | 背景映像・図・素材 | 台本のシーン、利用条件 | `bash scripts/fv_clips.sh <slug> clipN` のクリップ、データ由来の図、素材の出典と利用条件の記録 |
| `builder` | 音声・字幕・描画 | 検査済みの spec / `data/short_*.json` | `out/short_<slug>.mp4`、音声、SRT、投稿パック。既存成果物は別名で分ける |
| `reviewer` | 台本・動画の AI レビュー | 台本 JSON、動画ファイル | `docs/research/` のレビュー記録、原文照合と採用・不採用の判断。Google AI モードと ChatGPT を使う |
| `qa` | 技術検証と視聴確認 | 書き出した動画 | ffprobe / 全フレームデコード / 音量・字幕時刻 / 代表フレーム目視 / 連続視聴 / 全編実聴の別々の結果。未実施項目の明示 |
| `shipper` | アップロード・公開予約・X予約 | 承認済みの動画と投稿パック | private アップロード、Studio での公開設定、予約、`scripts/check_slots.py` での重複確認、台帳更新 |
| `scribe` | ナレッジの記録とコミット | 各担当の実測結果 | `docs/KNOWHOW.md` の更新、`SHORTS_PRODUCTION_NOTES.md` 等への追記、git コミット |

## 工程の受け渡し

```
scout → researcher → scriptwriter → asset maker → builder → reviewer → qa → shipper
                                                                        ↓
                                                                      scribe
```

各受け渡しでは、成果物のパスと「確認済み／未確認」を添えて `lead` に報告する。`lead` は次担当へ `send_message` で渡す。ゲートに引っかかった場合は差し戻し、勝手にルールを緩めない。

### ゲート

1. **題材ゲート**: `scout` が既出なしを確認。`NICHE_AND_100_IDEAS_20261124.md` にある候補は既出照合済みでも、制作前に再確認する。
2. **根拠ゲート**: `researcher` が一次資料の原文を確認し、`scripts/check_short_evidence.py` が通る `claims[]` を埋める。未確認は `needs_research` に残す。
3. **形式ゲート**: `scripts/shorts_standard.py check` で ERROR 0。WARN は内容を確認して判断。`status` が `needs_review` のものは `to-spec` に進めない。
4. **手順ゲート**: 単独 Short は担当者自身の `SOLO_SHORT_PROCEDURE.md` 確認印が必要。
5. **レビューゲート**: Google AI モード＋ChatGPT の指摘を原文照合し、`docs/research/` に記録。修正が必要なら差し戻す。
6. **視聴ゲート**: `qa` が技術検証・連続視聴・全編実聴・字幕同期・スマホ可読性を別結果として出す。
7. **公開ゲート**: `shipper` が `check_slots.py` で予約枠の重複を確認し、台帳の同じキーが無いことを確認。API アップは常に private、公開は Studio。

## 起動時のテンプレート

`lead` は必要な担当だけを起動する。すべてを同時に走らせると成果物の受け渡しが追えなくなる。1案件につき `scout` → `researcher` → `scriptwriter` の順に起動し、その先は工程に沿って追加する。

起動プロンプトには次を必ず含める。

```
あなたは <担当名> です。E:\rekishikaisetu-honnoji を作業ディレクトリとしてください。
作業開始前に AGENTS.md と docs/VIDEO_CREATION_PRECHECK.md を全文読み、
docs/KNOWHOW.md から自分の工程の文書を辿って読んでください。
docs/AGENT_TEAM.md の「全員に共通するルール」と担当の責務を守ってください。
```

動画に触れる担当（asset maker / builder / reviewer / qa / shipper）には、上記に加えて `SOLO_SHORT_PROCEDURE.md` の自分での確認を明示的に指示する。親エージェントの確認では代替できない。
