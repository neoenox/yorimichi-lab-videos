# 既存Shortの説明欄クリーンアップ（2026-11-26）

## 実施内容

- `scripts/clean_public_notes.py` で40件の spec の `notes` から内部メモ行（言い過ぎを避けた点／使っていないこと／未確認／指摘：／採用：／レビューで直した点／【試作】など）を削除した。
- 「指摘もある」「〜と指摘しています」は史実の説明なので削除対象外とし、誤削除を避けた。
- `scripts/check_public_notes.py` の検出基準を削除基準と揃え、全 `data/short_*.json` で ERROR 0 を確認。
- `scripts/_fix_published_descriptions.py` で `pack_short.py` → `yt_api.py redesc` を実行し、169件のアップ済み動画の説明欄を更新した。

## 未完了

- 106件は API クォータ超過で失敗。内3件（short_islands / short_lightning / short_moon）は API 上に存在しない動画なので対象外。残り103件はクォータ回復後（日本時間夕方ごろ）に `python scripts/_fix_published_descriptions.py --apply` を再実行する。再実行は成功済みの分も上書きするが、内容は同じなので問題ない。
- 台帳の spec は全件クリーンなので、新規制作では内部メモは混入しない状態になっている。

## 再発防止

- `scripts/check_public_notes.py` を `docs/SOLO_SHORT_PROCEDURE.md` の合格基準に組み込んだ（2026-11-26）。
