# 説明欄の内部メモ除去（2026-11-26）

## 問題

月食Short（`vG2kAiQVG9E`）の説明欄に、`web_fetch` で文字化けしたことや Python で `decode("euc_jp")` したという内部作業手順が混ざっていた。説明欄は視聴者向けで、内部メモは `docs/research/` に残すのがルール（KNOWHOW.md）。オーナーから指摘を受けた。

## 対処

- `scripts/gen_solo_eclipse.py` の `notes` を、出典と視聴者向けの事実だけに書き直した。取得方法・レビュー判断・使っていないこと等の内部記述は削除し、`docs/research/20261126_eclipse_sources.md` と `20261126_eclipse_review.md` に残っている。
- API でアップ済みの `vG2kAiQVG9E` の説明欄を差し替え、内部記述が残っていないことを確認した。
- 再発防止のため `scripts/check_public_notes.py` を作成。取得方法・レビュー判断・ゲート名などの内部ワードが `notes` に入っていないか検査する。
- `docs/SOLO_SHORT_PROCEDURE.md` の合格基準に説明欄検査を追加した。手順書更新に伴い、全4部分を読み直して確認印を取り直した。

## 全件検査の結果

既存の `data/short_*.json` を検査したところ、33件に内部記述が残っていた。うち `short_eclipse.json` はコピー元の古い spec なので最新化して解消。残り32件は既に公開・予約済みで、今回はメタデータを一括変更せず記録に留める（1円玉、キトサン、クロロプラスト、カマクラ試作など）。

## 今後のルール

`notes` には出典 URL・確認日・視聴者向けの事実・クレジットだけを書く。取得方法、レビューで直した点、言い過ぎを避けた点、使っていないこと、needs_review / needs_research / to-spec などのゲート名は `docs/research/` に書く。アップ前に `python scripts/check_public_notes.py data/short_solo_<slug>.json` を通す。
