# short_drain の long_id 修正（2026-11-25）

## 内容

台帳 `data/youtube_ids.json` の `short_drain.related` で `long_id` が空文字だったため、`qjXxDENAZZE`（06_drain_vortex）を設定した。

- Short: `60hEGrmryiY`（排水の渦は、南半球で逆回転する？）
- 長尺: `qjXxDENAZZE`（06_drain_vortex）
- 根拠: `docs/ANALYSIS_2026-11-01_long_zero_views.md` 43–45行に、Short `60hEGrmryiY`（排水）と長尺 `qjXxDENAZZE` が同じ排水題材で並んで記録されている。

## 理由

2026-11-25 に台帳へ回遊設定情報を反映した際、`data/short_drain.json` が無く `long_id` を特定できず空文字のまま `done: true` とした。271件の `related`  entries で空文字はこの1件だけだった。今日の予約誤解除インシデントの原因も `long_id` の誤判定だったため、空文字を残すと再発リスクになる。

## 未確認

- Studio で `60hEGrmryiY` の関連動画に `qjXxDENAZZE` が実際に設定されているかは未確認（CDP 9222 が停止中のため確認できなかった）。設定済み（`done: true`）という記録は `related_done.json` に基づく。
