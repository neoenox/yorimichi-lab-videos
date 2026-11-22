# 赤ちゃん2本＋富士山ShortのAIレビューと修正（2026-11-22）

## 対象と到達点

| slug | 題材 | 最終尺 | Google AI モード動画レビュー |
| --- | --- | --- | --- |
| `solo_baby_hone` | 赤ちゃんの骨は大人より100本多い？ | 55.9秒 | 最終版「このまま公開可」 |
| `solo_baby_namida` | 赤ちゃんは泣いても涙が出ない？ | 51.1秒 | 最終版「このまま公開可」 |
| `solo_fuji` | 富士山頂はどの県のもの？ | 56.6秒 | 「このまま公開可」 |

ここまでで**台本レビュー（Google AI モード）と動画レビュー（Google AI モード）は完了**。
アップロード・予約・根拠テーブルゲートは未実施（下記「未実施」を参照）。

## 方法

- 台本レビュー: `python scripts/google_ai_review.py <slug> --mode script`
  - 出力: `out/google_ai_review_<slug>_script.txt`
  - `solo_fuji` は初回が途中で切れたため、回答が安定するまで待つ inline Playwright で再取得（4103文字）。
- 動画レビュー: 専用 Chrome（CDP 9222、`.chrome-automation`）に最終 mp4 を添付し、書き起こし・字幕一致・読み・音・レイアウト・事実・冒頭フック・AI映像・公開可否を依頼。
  - 出力: `out/google_ai_review_<slug>_video.txt`（修正版で上書き。初回レビューは `cache/_tmp_video_review.py` の前段階として実施）
- **ChatGPT は不使用**: CDP 9222 の ChatGPT は未ログイン（ログイン画面のみ）で、台本レビューを送信できなかった。オーナー指示の「台本は Google AI モード＋ChatGPT」のうち ChatGPT 分は未実施として記録する。Gemini / Muse は起動していない。
- AI の指摘は、保存済みの出典原文（`cache/research_baby/en_skeleton.txt` / `cc_skeleton.txt` / `ruisen_extract.txt`）と実フレーム（該当時刻の PNG）で照合してから採否を決めた。

## 台本レビューの採否

### `solo_baby_hone`

| 指摘 | 判定 | 根拠・対応 |
| --- | --- | --- |
| 「約300本」は Human skeleton の本文に無い | 採用 | キャッシュ本文は出生時 about 270 / 成人 about 206。「300本」は歴史的記述等に見られる語で、一次資料で確認できていない。出典帯を Wikipedia／Cleveland Clinic とし、ナレーションは「300本という言い方も、数え方で変わります」に変更 |
| 「骨盤は3つが1つ」は骨盤全体を誤解させる | 採用 | 本文の Pelvis の項目は ilium / ischium / pubis。左右の寛骨が3つから1つになる表現「骨盤の左右の骨は3つ」に変更 |
| 「300本」を削除 | 不採用 | 問い「100本多い？」の前提。断定を避けた形で残す（概要欄に未確認を明記済み） |

### `solo_baby_namida`

| 指摘 | 判定 | 根拠・対応 |
| --- | --- | --- |
| 「赤ちゃん」では広すぎる | 採用 | 出典本文は「新生児（出生時）」。「生まれたばかりの赤ちゃん」に限定 |
| 「個人差が大きく、数ヶ月かかる」は原文に無い | 採用 | 原文は「生後数週間から数ヶ月をかけて腺組織が拡大・成熟」。「個人差が大きく」を削り「涙腺が育つまでには、数ヶ月かかることもあります」に変更 |
| 出典に Wikipedia を出すのは信頼性が落ちる | 不採用 | 二次資料であることを画面と概要欄で開示する方針を優先。隠すと根拠が不明になる |

### `solo_fuji`

| 指摘 | 判定 | 根拠・対応 |
| --- | --- | --- |
| 「八合目から上すべて」は西側の境界線と矛盾 | 採用 | 調査メモは「山頂付近と東側斜面が未定」。「山頂付近は県境が未定」に変更 |
| 地図の「表示」ではなく「住所表示」 | 採用 | 2014年の騒動は地理院地図の住所表記。ナレーションを「電子地図の住所表示に…と出て」に変更 |
| 所有権を「確定」と強める | 不採用 | 判例原文・判例番号を確認できていないため「とされています」を維持。2004年財務省決定も今回の確認範囲外 |
| 「富士山本宮浅間大社」の読み | 採用（確認） | 読み辞書 `data/fuji_pron.json` に `フジサンホングウセンゲンタイシャ` を指定済み。動画レビューで正しく読まれていることを確認 |

## 動画レビューのラウンドと修正

1. 初回（`baby_hone` / `baby_namida`）は「直してから公開」。
2. `baby_hone`:
   - 字幕の「300本とゆ言い方」指摘 → SRT と 13.5秒の実フレームを確認すると「300本という言い／方もありますが」の**改行**が誤読されたもの。改行で単語が割れない文に変更して再描画。再レビューで「このまま公開可」。
   - 「206本」の発音違和感 → カナは `ニヒャクロッポン` で正しく、再レビューでも問題なし。不採用。
   - 白い立方体の背景 → 癒合の比喩として意図したもの。不採用（概要欄に AI イメージと明記済み）。
   - 結論カードのモーフィング → 軽微な映像継ぎ目として記録のみ。
3. `baby_namida`:
   - 0:00〜0:01 に結論カードが先に出る → `hook_card=False` を指定して再描画。
   - 字幕「赤／ちゃん」の改行 → 文を「生まれたばかりの赤ちゃん。涙腺の形は…」に変更。
   - 0:39 の日付読み上げが唐突 → 音声から削り、画面の出典帯（`src`）と概要欄に「2026/11/21時点」を残す。
   - 冒頭フックに赤ちゃんの顔を出す提案 → 人物を写さない制作方針のため不採用。
   - 3回目のレビューで「このまま公開可」。
4. `solo_fuji` は初回から「このまま公開可」。修正なし。

## 検証したこと

- 再描画後、3本とも `ffmpeg -v error -i ... -f null -` が終了コード0・エラーなし。
- ffprobe: 55.9 / 51.1 / 56.6秒、1080x1920、h264 + AAC。
- 指摘箇所は該当時刻のフレームを抽出して目視（13.5秒の字幕、0.5秒の冒頭カード）。
- 最終動画で投稿パックを作り直し: `python scripts/pack_short.py <slug> --tags=...`（`upload/short_solo_*/`）。

## 未実施（完了扱いにしない）

- **ChatGPT の台本レビュー**: CDP 9222 が未ログインで送信不可。
- **`claims` / `needs_research` の記入と `check_short_evidence.py`**: 3本とも空。アップ前ゲートに通すには記入が必要。
- 人間の全編実聴、連続通し視聴、スマホ実機確認、Studio の公開設定、アップロード・予約: 未実施。
- 移動・表情のあるフック映像の作り直し: 未実施（上記のとおり不採用）。

## 使ったコマンド（再現用）

```bash
python scripts/gen_solo_baby_hone.py
python scripts/gen_solo_baby_namida.py
python scripts/gen_solo_fuji.py
python scripts/make_short2.py solo_baby_hone
python scripts/make_short2.py solo_baby_namida
python scripts/make_short2.py solo_fuji
python scripts/google_ai_review.py solo_baby_hone --mode script
python scripts/review_short_cdp.py solo_baby_hone chatgpt   # 未ログインで失敗
python scripts/pack_short.py solo_baby_hone --tags=...
```
