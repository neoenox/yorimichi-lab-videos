# 全動画の説明欄から内部メモを除去（2026-11-22）

## 経緯

オーナーが赤ちゃんShortの説明欄に「Google AIモードの台本レビューで採用」「regarding…不採用」等の制作メモが入っているのを指摘。全チャンネルを走査したところ、公開済み・予約済みの動画にも同様な内部メモが残っていた。

## 範囲と結果

- YouTube API でチャンネル全 **377本** の `snippet.description` を取得し走査。
- 内部メモのパターン（言い過ぎを避けた点／使っていないこと／未確認：／レビューで直した点／不採用／Gemini／Muse／Ask Studio 等）が残っていた **57本** を除去。
- 除去後に再走査し、**該当0件** を確認。予約時刻（`status.publishAt`）は更新前後で維持。
- 正当なクレジット行（`ChatGPT(OpenAI)による生成イラスト` 等）は残した。URLを含む行も出典として保持し、その行の内部判断の文だけを文単位で削除した。
- ローカルの `upload/<pack>/description.txt` / `out/<slug>_description.md` も同じ内容に更新。該当specは generator を再実行（43本）、generator が無い6本は JSON の notes を直接整理。

## 恒久対策

- `scripts/solo_spec.py` に `public_notes()` を追加。`build()` が spec・説明欄を書く前に内部メモ行を除く。
- レビューの採否・未確認の調査ログは `docs/research/` に残す運用を維持。

## 未確認

- 人間の全編実聴・スマホ実機確認は今回の対象外。
