# Short の根拠テーブルゲート（2026-11-20 オーナー確認）

## 目的と優先順位

最優先の制約は **A：根拠の完全性**（一次資料で確認できない数字・発言・因果を台本に書かない）。
B：成長（KPI）は A の内側での最適化、C：量・カデンスは最後。

## 決定事項

| # | 決定 |
|---|---|
| 1 | 制作標準 `shorts-standard/` は変更しない。日々の production path（単独Short／ペアShort）に、標準の `claims` 相当を機械可読で持たせる |
| 2 | ゲートは **答えを変える未確認だけを止める**。答えを変えない未確認は `needs_research` に残し、「なぜ答えが変わらないか」の一行を必須にする。概要欄にも開示する |
| 3 | 根拠は `data/short_*.json` に `claims[]` / `needs_research[]` として埋め込み、`scenes[].claim_ids` で参照する。レンダラは追加キーを無視するので描画系は無変更 |
| 4 | `primary` は公式本文の再掲なら大学DB・Wayback も可。**`evidence_note` に「代替」と明記必須**。e-Gov が取れない法令は名古屋大学DBで代替する |
| 5 | ゲートは `scripts/check_short_evidence.py`。`scripts/solo_schedule.py` の `procedure_gate` 直後に呼び、通らなければアップロードしない。CI と pre-commit は**変更された** `data/short_*.json` を検査する |
| 6 | 既存 284 本は祖父化。新規・変更分だけをゲートに通す（全件遡及はしない） |
| 7 | KPI の型判定は 11/20〜21 から **11/26** へ後ろ倒し。凌雲閣は公開直後で数値が無く、発電は 11/24 公開。**事前登録の閾値は変更しない** |
| 8 | 台本レビュー（ChatGPT / Gemini）は**背景生成前**に必須。指摘と採否を `docs/research/` に記録。Muse は最終レビューとして残す。既存動画の再利用でも台本レビューを省略しない |
| 9 | 成人の日（seijin）を次の題材にする。未公開の `short_seijin` を再利用し、作り直さない |
| 10 | 1/11 19:00 に長尺 `48_seijin`、20:00 に `short_seijin` をペア公開する。長尺はゲート対象外とし、`08_fact_check.md` と `10_review_log.md` のサインオフで代替する |
| 11 | `short_solo_seijin1115` は「1949〜1999年」が二次情報依存のため公開しない。`short_seijin` の `superseded` に記録し、private のまま残す（削除しない） |

## ゲートの検査項目

`python scripts/check_short_evidence.py data/short_*.json ...`（終了コード 1＝公開準備停止）

- ERROR: `claims` が空 / id 重複 / `statement` 空 / `source_type` 不正 / `evidence_note` が短い
- ERROR: `primary` に http(s) の `source_url` が無い / 大学DB・Wayback なのに `evidence_note` に「代替」が無い / `ai_assistant` に質問内容が無い
- ERROR: 断定のあるシーン（`end: true` 以外）に `claim_ids` が無い / 存在しない id / `primary` 以外を根拠にしている
- ERROR: `needs_research` に「答えは変わらない」系の理由が無い
- WARN: 公式ドメイン外のURL / `claim` がどのシーンからも参照されていない

## 実行した検証（2026-11-20）

- `python -m unittest discover -s tests -p 'test_short_evidence.py'` → 11 tests OK
- `python scripts/check_short_evidence.py data/short_seijin.json` → OK（ERROR 0 / WARN 0）
- `sh -n scripts/hooks/pre-commit` → 構文 OK
- `python scripts/yt_analytics.py videos` → 旧型の平均視聴率（玉川上水 74.2% / プラニマル 97.7%）を取得。凌雲閣・発電・スワイプ率は未取得

## 未実施（未確認を完了扱いにしない）

- **ChatGPT / Gemini による 6シーン台本レビュー**: 完了。両方とも「公開可」。指摘は軽微な改善提案のみで、今回は再描画しない（採用しない理由を含め [`research/20261120_seijin_reviews.md`](research/20261120_seijin_reviews.md) に記録）。
- **凌雲閣・発電のスワイプ率（Studio のショート動画分析）**：API に項目が無く、ブラウザ/login が必要。11/26 に n=2 を揃えてから判定。
- **`short_seijin` / `48_seijin` の連続視聴・全編実聴・スマホ実機確認**：未実施。`VIDEO_CREATION_PRECHECK.md` に従い、技術検査と視聴品質は別ゲートとして残す。
- **1/11 の公開予約**: 未実施。連続視聴・全編実聴・スマホ確認が済んでから行う。
