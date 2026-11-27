# 夕焼けShortのAI生成模式図の生成・採用判断（2026-11-27、image-maker）

## 依頼と方針

- タスク: team task-17。上部の3列吹き出し（`timeline` viz）を消す代わりの図示をAI画像生成で作る。
- 改訂済みルール（commit `cab097f`）: AI生成画像の模式図も许可。ただし生成ごとに (1) 目視、(2) 気象庁FAQ原文との照合、(3) 問題があれば再生成、のゲートを必須とする。文字・ラベルはAIに描かせない。
- オーナー判断で途中から方針変更。線画的なベクター模式図ではなく、**人に説明する用のプレゼン資料風のリッチな画像**を作る。文字は従来どおり描かせない。

## 生成経路の確認

1. **google.com/ai（AI Mode）で画像生成が使えることを実証した。** isolated bsk セッションで `https://www.google.com/ai/`（実際の URL は `https://www.google.com/search?udm=50&aep=11`）にプロンプトを送ると、Nano Banana 2 Lite が画像を生成した。
2. **ダウンロード経路も確立した。** 生成後に「この AI 生成画像をダウンロード」ボタンが有効になり、`C:\Users\neoen\Downloads\` に JPEG として保存される。bsk の ref クリックが「pointer target is covered」で失敗したため、`bsk evaluate` で同一ボタンを JS から `.click()` して取得した（`cache/bsk_click_download.py`）。
3. FreeVideo は動画専用で still 画像の経路が無いため使わない。ChatGPT 経由（`scripts/gen_image_cdp.py`）は予備として残すが、今回は google.com/ai で通ったので使っていない。
4. 生成画像はすべて `assets/solo_sunset/diagram/` に PNG として保存した。元のダウンロード JPEG は既存ファイルを上書きせず Downloads に残している。

## 描く内容（気象庁FAQ原文）

出典: 気象庁FAQ「空はどうして青いのですか？夕焼けはどうして赤いのですか？」 https://www.jma.go.jp/jma/kishou/know/faq/faq13.html （2026-11-26 確認。全文引用は `docs/research/20261126_sunset_sources.md`）

| 記号 | 原文どおりの内容 |
| --- | --- |
| (a) | 太陽光は波長の短い方から順に、むらさき、青、緑、黄、だいだい、赤を含む |
| (b) | 晴天時は空気分子が波長の短い光をより強く散乱する。紫は空の高いところで散乱され、地上に届く量は少なくなる |
| (c) | 届く量の多い青色の光が強調されて、空が青く見える |
| (d) | 夕方は太陽が地平線に近く大気を通過する距離が長くなり、短い波長は途中で散乱され、長い波長の赤色の光が多く地上に届く |

照合で退ける表現: 「紫が消える」「青だけ残る」「大気の厚さが厚くなる」（気象庁は「通過する距離が長くなり」）、波長の4乗、nm などの数値・数式。

## 生成した画像とゲート結果

| ファイル | 内容 | 目視 | 原文照合 | 判定 |
| --- | --- | --- | --- | --- |
| `diagram_light_path.png` | 白い光が大気で6色に分かれる線画風。元は `image_437e7634.jpg`（1408x768）。 | 擬似文字・署名なし。色順 violet→blue→green→yellow→orange→red。光は左上→大気→右下。 | (a) はOK。(b)(c)(d) はこの1枚では表現しきれていない。 | **参考として残す**（線画風でオーナー希望のリッチさ不足。単体では採用しない） |
| `diagram_scattering.png` | 空気分子と短い波長の散乱を線画で表現。元は `image_cc0cf45d.jpg`。 | **上部に "Rayleigh scattering" の文字が写った。** no-text ゲート違反。 | 表現自体は (b) に沿うが、原文に無い用語を画像に書いている。 | **却下**（文字あり。再生成せず別案へ） |
| `diagram_presentation_day.png` | リッチな青空、太陽、光の束、散乱。元は `image_b5b2c379.jpg`。 | 色順・光向きはOK。**右下に署名らしき小さな記号**があった。 | (a)(b)(c) は表現できている。(d) はこの1枚だけでは弱い。 | **却下**（署名・透かしゲート違反） |
| `diagram_presentation_day_v2.png` | 上の再生成版。署名・透かし・文字・サインを明示的に禁止したプロンプト。元は `image_1a75ce14.jpg`。 | 768x1376。文字・署名・透かしなし（右下を300%拡大して確認）。色順 violet/pink→blue/cyan→green/yellow→orange/red。光は太陽（左上）→大気層→右下の柔らかな光点。紫は上空で散乱し、わずかに下へ届く。青全体が青く発光。 | (a)(b)(c) を原文どおり。(d) は比較スライド版でカバー。「紫が消える」「青だけ残る」表現なし。数値・数式なし。 | **採用** |
| `diagram_presentation_compare.png` | プレゼン比較スライド風。左＝昼（短い経路・青空）、右＝夕方（長い経路・赤い地平線）。元は `image_e4e6acea.jpg`。 | 768x1376。文字・署名・透かしなし（右下を拡大して確認）。左は高い太陽＋短い白い経路。右は低い太陽＋長い経路で紫→青→緑→黄→赤の順に色が並び、赤い光が右下へ届く。 | (d) を原文どおり。「通過する距離が長い」を左右の経路長で表現。「大気が厚くなる」と言い切る表現なし。数値・数式なし。 | **採用** |

## 採用画像のプロンプト

プロンプト全文は `cache/prompt_presentation_day_v2.txt` と `cache/prompt_presentation_compare_v2.txt` に保存した。共通の必須文言は次。

```
STRICT NO-MARKS REQUIREMENT: absolutely no text, no letters, no words, no titles,
no labels, no captions, no numbers, no logos, no watermarks, no signatures,
no artist marks, no initials, no symbols of any kind anywhere in the image,
especially not in the bottom-right corner.
```

1枚目は青空・太陽光の束・空気分子による短い波長の散乱・青の強調を1枚にまとめる構図。2枚目は「昼＝短い経路／夕＝長い経路」を左右2パネルで比較する構図。どちらも光の向きは「太陽→大気→目（右下の柔らかな光点）」で統一した。

## 確認した範囲と未確認の範囲

- 確認済み: google.com/ai での画像生成とダウンロード、5枚すべての目視（右下コーナーの拡大含む）、気象庁FAQ原文との照合、文字・署名・数値・数式のないこと、色順、光の進行方向、採用2枚の PNG 保存。
- 未確認: 最終動画に重ねたときの見え方（`make_short2.py` の cover＋dim＋字幕・見出しとの重なり）、スマホ実機表示、連続再生、ナレーション同期、投稿可。これらは別担当のゲート。
- 今回は動画の描画・アップ・予約には進んでいない。

## 再現に使ったコマンド・場所

- 生成スクリプト: `cache/gen_ai_mode_v3.py`（bsk open → fill → click 送信 → 生成待ち → JS ダウンロード）
- ダウンロード補助: `cache/bsk_click_download.py`（cooperate wait/sync → `evaluate` でボタンを JS click）
- bsk セッション: `--scope sunset-p-day-v2c` と `--scope sunset-p-compare-1`、`--browser 133d3412`
- bsk の Chrome 接続が数分おきに切れることがある。`bsk browsers --json` が `[]` のときは復帰を待つ。bsk daemon は Job Object の制限で自動起動に失敗することがあるが、既存プロセスが生きていれば再接続で回復した。
