# 変更履歴

このディレクトリは上流の「寄り道ラボ Shorts 制作標準 v1.0」を取り込んだもの。
このリポジトリでの変更はここに記録する（上流と差分が出たことを明示するため）。

## v1.1（2026-11-04、オーナー判断）

**claims の根拠に AI アシスタントの回答を使ってよいことにした。**

- `output.schema.json`
  - `claims[].source_type` を追加（`primary` / `ai_assistant`、必須）
  - `claims[].source_url` を必須から任意へ（`source_type=primary` のときだけ必須）
- `validate.py`
  - `primary` は `source_url` が http(s) であることを検査
  - `ai_assistant` は `evidence_note`（質問と回答の要点）を必須にし、URL は不要
- `README.md` / `PROMPT.md`
  - 上記の使い分けと、`ai_assistant` 使用時は一次資料での裏取りが未実施である旨を明記

### 理由

- 速報性のある題材（ニュースの背景など）では、一次資料にたどり着く前でも構成を作る必要がある
- ブラウザ経由の ChatGPT など、調査の補助としての利用が現実的

### リスクと運用

- AI の回答は誤りうる（幻覚・古い情報・出典の取り違え）。**数字・固有名詞・因果関係は特に危険**
- `scripts/shorts_standard.py` は `ai_assistant` の claim があると **WARN を出す**（黙って通さない）
- 公開前に、可能な範囲で一次資料の URL を併記する（`primary` の claim を追加する）
- 誤りが判明したら、概要欄に訂正を残し、重大なら新IDで差し替える（`superseded` 運用）
