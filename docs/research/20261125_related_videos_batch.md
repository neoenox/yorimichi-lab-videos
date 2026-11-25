# 関連動画（回遊設定）の一括設定（2026-11-25）

## 実施内容

- `scripts/related_todo.py` で未設定の Short を監査し、21件の TODO を検出。
- CDP 9222 経由の Playwright で Studio の関連動画を設定（`scripts/_set_related_batch.py`）。
- 1件目（akashi）で動作確認後に残り20件を実行。成功21件、失敗0件。
- 再監査で TODO は0件。`data/related_done.json` は既存10件＋今回21件の31件。
- Studio で1件（LgePZBLaOTk）の関連動画に「日本の標準時は、なぜ明石の時刻？」が設定されていることを確認。

## 設定した21件

akashi / gps / honnoji / ninja / oceanblue / oke / rain30 / rice / shimabara / solo_anegawa_suugyou_nl / solo_horagatoge_yamazaki / solo_kishomon_sekigahara / solo_miso_mikata / solo_news_kanto_rain / solo_sandan_nagashino / solo_taiko_mikata / solo_toiteppo_sekigahara / tedorigawa / tottori / worldmap / yakubusoku

## 運用の要点

- Studio の関連動画ダイアログは `[role=dialog]` が複数あり、検索欄 `input[placeholder="自分の動画を検索"]` を持つものを選ぶ。
- 長尺タイトルを検索欄に入れると候補が1件に絞れる。一覧の先頭50件から探すより確実。
- 設定完了分は `related_todo.py done <ShortのID>` ではなく、`data/related_done.json` に直接記録した（スクリプト側で実施）。

## 未確認

- 実際の流入効果（長尺再生÷Short再生、関連動画経由の流入）は48時間後の週次計測で確認する。
