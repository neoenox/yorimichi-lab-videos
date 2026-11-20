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
- `python scripts/yt_analytics.py videos` → 旧型の平均視聴率（玉川上水 74.2% / プラニマル 97.7%）を取得。凌雲閣は Studio でスワイプ90.0% / 継続10.0% / 平均視聴割合53.3%を取得（11/20時点、n=1のため判定保留）

## 未実施（未確認を完了扱いにしない）

- **ChatGPT / Gemini による 6シーン台本レビュー**: 完了。両方とも「公開可」。指摘は軽微な改善提案のみで、今回は再描画しない（採用しない理由を含め [`research/20261120_seijin_reviews.md`](research/20261120_seijin_reviews.md) に記録）。
- **スワイプ率**: 凌雲閣は取得済み（スワイプ90.0%／継続10.0%／平均視聴割合53.3%）。発電は11/24公開のため11/26まで未取得。矛盾したシグナルのためn=2で判定する。
- **連続視聴・全編実聴・スマホ実機確認**: 圧縮版の全編デコード・音量・字幕時刻、Gemini による Short の動画レビュー（公開可）、代表フレームの目視は完了（[`research/20261120_seijin_video_qa.md`](research/20261120_seijin_video_qa.md)）。元解像度・スマホ実機・人間の実聴は未実施。
- **1/11 の公開予約**: 未実施。連続視聴・全編実聴・スマホ確認が済んでから行う。


## 方針変更（2026-11-20 オーナー判断）

- **Shorts を優先する。長尺動画の新規公開は一旦停止する**。
- したがって 1/11 19:00 の長尺 `48_seijin` 公開は取りやめ、動画は非公開のまま残す（削除しない）。
- 既存の Short の確認・根拠テーブル整備は継続する。長尺のゲートは引き続き対象外。
- 1/11 の Short 枠は `short_solo_islands_kazu`（国土地理院の一次情報、単独Short）で埋める。`short_seijin` は長尺が解禁になるまで公開保留（`long_id` が非公開長尺を指すため）。根拠テーブルと台本レビューは完了済みで、再描画不要。
- 予約の実測（2026-11-20）: `2QegxztoVw4` を 2027-01-11 12:00 に予約。`short_solo_seijin1115`（二次情報の主張）と `66_yakurei`（長尺停止方針）は予約解除し private のまま維持。`check_slots.py --days 60` で重複なしを確認。


## 次のShort（春分／秋分）の進行（2026-11-20）

- 題材はグリリングで確定。答えは「同じではない。2020年東京で昼12時間8分・夜11時間52分」（国立天文台FAQ a0303）。
- `scripts/gen_solo_equinox.py` と `data/short_solo_equinox.json` を作成。根拠は3主張（a0303／a0102／a0303）。ゲート OK。
- 台本レビュー: ChatGPT「公開可」、Gemini「修正必要」。共通指摘（年・場所の明示、角度単位の誤解）を描画前に反映済み（[`research/20261120_equinox_reviews.md`](research/20261120_equinox_reviews.md)）。
- **完了**: 背景4クリップ生成、ビルド（56.5秒）、機械検査、ASR、Muse「公開可」（初回の出典行の見切れを修正）、非公開アップロードと1/12 12:00予約（ID `ZSRepHwe500`）。詳細は [`research/20261120_equinox_video_qa.md`](research/20261120_equinox_video_qa.md)。
- **X予約**: 2027-01-12 12:05 JST に紹介投稿を予約（重複なし）。
- **未確認**: 通し再生、人間の全編実聴、スマホ実機、StudioのAI開示UI（API設定済み）。


## 長尺予約の一括解除（2026-11-20 オーナー判断）

- 「Shorts優先・長尺の新規公開停止」を全予約に適用。APIで対象を洗い出したところ、+60日窓では37件だったが全体では**49件**の長尺が予約状態だったため、49件すべて `publishAt=None` に変更（動画は削除せず private のまま）。
- 解除後: 長尺の予約 0件／Shorts 74件。`check_slots.py --days 60` で同時刻の重複なしを確認。
- 台帳 `data/youtube_ids.json` の該当キーの `publishAt` も None に更新。解禁時に再予約できるよう動画IDは保持。
