# ノウハウの入口（まずこれを読む）

更新日: 2026-11-20。**制作で分かったことは必ず git に残す**（AGENTS.md）。この文書は「どこに何が書いてあるか」の索引。

## 1. 動画を作るときに読む順番

| 順 | 文書 | 内容 |
| --- | --- | --- |
| 1 | [`VIDEO_CREATION_PRECHECK.md`](VIDEO_CREATION_PRECHECK.md) | 制作前の必須確認（工程・根拠と演出の分離・未確認を完了扱いしない） |
| 2 | [`SHORTS_STANDARD_INTEGRATION.md`](SHORTS_STANDARD_INTEGRATION.md) | Shorts 制作標準の使い方・既存パイプラインとの差分・検査の階層 |
| 3 | [`SHORTS_PRODUCTION_NOTES.md`](SHORTS_PRODUCTION_NOTES.md) | **実測ノウハウ本体**（画面の安全領域、資料画像、AI生成、投稿、失敗と対処） |
| 4 | [`VIDEO_PRODUCTION_RUNBOOK.md`](VIDEO_PRODUCTION_RUNBOOK.md) | 長尺の手順（VOICEVOX・描画・公開・トラブル対処） |
| 5 | [`MAIN_TEXT_ONLY_WORKFLOW.md`](MAIN_TEXT_ONLY_WORKFLOW.md) | リモートへ素材を上げない運用（push の作法） |

Short の根拠テーブルゲート（2026-11-20 判断）は [`SHORT_EVIDENCE_GATE_20261120.md`](SHORT_EVIDENCE_GATE_20261120.md)。日々の Short は `data/short_*.json` に `claims` を書き、`scripts/check_short_evidence.py` を通さないとアップできない。

## レビューは Google AI モード（2026-11-20 オーナー指示）
動画レビューは **Google AI モード**（https://www.google.com/ai）のみ。**台本レビューは Google AI モード＋ChatGPT の併用**（`python scripts/google_ai_review.py <slug> --mode script` と `python scripts/review_short_cdp.py <slug> chatgpt`）。Gemini は必須ではない。`python scripts/google_ai_review.py <slug> --mode script|video [--video out/...mp4]` で、CDP 9222 が落ちていても自動起動する。AIの指摘は根拠の原文と照合して採用・不採用を決め、判断を `docs/research/` に残す。Muse は起動しない。

## 2. ツール（スクリプト）と役割

| スクリプト | 役割 | 実測 |
| --- | --- | --- |
| `scripts/shorts_standard.py` | 標準 JSON の検査（`validate.py` 実行＋追加規則）とレンダラ spec への変換 | 2026-11-04 |
| `scripts/check_short_evidence.py` | **`data/short_*.json` の根拠テーブル検査**。アップ前・CI・pre-commit で変更分のみ | 2026-11-20 |
| `scripts/review_short_cdp.py` | **ChatGPT / Gemini へ台本を送る**（CDP、ログイン済みセッション）。応答は `out/<site>_review_<slug>_short.txt`。ChatGPTの応答要素は `div[class*="DilResponseRoot"]`（2026-11-20時点） | 2026-11-20 |
| `scripts/gen_image_cdp.py` | **ChatGPT の画像生成**（Chrome を CDP で操作、blob 画像を canvas 経由で取得） | 2026-11-05 |
| `scripts/studio_cdp.py` | **Studio の公開設定・字幕**（Playwright、チャンネルID検証つき） | 2026-11-05 |
| `scripts/chatgpt_image.py` | bsk 経由の画像生成（**不安定・非推奨**。CDP 版を使う） | 2026-11-05 |
| `scripts/check_slots.py` | **公開予約の実測**（時刻の重複を API で検査。重複ありで終了コード1） | 2026-11-19 |
| `scripts/make_short2.py` | 縦型 Short の描画（1080x1920、VOICEVOX、FFmpeg） | 既存 |
| `scripts/pack_short.py` | 投稿パック作成（`--tags=` で単独 Shorts も可） | 2026-11-04 |
| `scripts/main_push_textonly.py` | 素材を含めずに main を更新（`--path` で範囲限定） | 2026-11-04 |
| `scripts/install_git_hooks.py` | pre-push（素材の push 防止）/ pre-commit（Shorts 検査） | 2026-11-04 |
| `scripts/spec_common.py` | `make_spec_*.py` の共通部品（`TOP`／`_starts`／`_fit`／`_remap`／`finalize`）。**ここが唯一の定義元** | 2026-11-08 |

## 3. これだけは覚えておく（要点）

### コード
- `scripts/` は 300 本以上の単発スクリプトが平坦に並ぶ。**共通部品は `spec_common.py`（spec 生成）／`specart.py`（画像差し込み）／`vp.py`（描画）** に寄せる
- `make_spec_*.py` は「データ（台本の行番号と画面要素）」だけを書き、`TOP`・`_starts`・`_fit`・`_remap` は `spec_common` から import する（コピーしない）
- `scripts/*_before_*.py` は過去のスナップショット。**現行版ではない**ので、動かす前に `vp.py` / `make_spec_<slug>.py` のどれが現行か確認する
- `data/*_spec.json` は生成物だが、スクリプトが古いと**古い形式で上書きされる**。生成し直す前に `git diff data/` を見る

### 制作
- Shorts は **brief → result.json → check → to-spec → 描画**。`needs_review` のままでは `to-spec` が通らない
- 日々の Short（solo／ペア共通）は `data/short_*.json` に `claims[]` / `needs_research[]` と `scenes[].claim_ids` を書き、`python scripts/check_short_evidence.py <spec>` を通す。答えを変えない未確認は理由を添えて `needs_research` に残す（[`SHORT_EVIDENCE_GATE_20261120.md`](SHORT_EVIDENCE_GATE_20261120.md)）
- 画面の安全領域: タイトル y≈200（**全角18文字まで**）／大テロップ y≈520／字幕 1470–1540／注記は 1556 以降
- 背景は **シーンごとに変える**（`art_map.json`）。同じ絵が続くと単調
- **FreeVideoのクリップ指定は `scripts/fv_clips.sh <slug> clipN`**（`1` だと該当なしで何も作らず「ALL OK」。2026-11-19）。「古い地図」を頼むとAIは擬似文字を描くので、「無地の紙＋線だけ」を明示する（[`SHORTS_PRODUCTION_NOTES.md`](SHORTS_PRODUCTION_NOTES.md)）
- 明るい画像の上に字幕を置くときは、**下半分に暗幕**を入れる（入れないと読めない）
- **TikTok 向けの制作は廃止**（2026-11-11 オーナー判断：投稿しても動画が再生されないため）。**新規制作・投稿準備・背景の作り直しはしない**。`check_tiktok.py` / `tiktok_launch_audit.py` / `tiktok_post.py` も実行不要
  - 既存の物は**削除せず残す**（方針A）：`out/short_tiktok_*.mp4`、`data/short_tiktok_*.json`、`assets/*/tiktok/`、`docs/TIKTOK_*.md`、関連スクリプト。再開する場合の参考資料扱い
  - `docs/TIKTOK_STRATEGY.md` / `docs/TIKTOK_POSTING_PACK.md` は廃止前の計画（11/02 時点）。**現行の方針ではない**
  - 経緯：11/08 に一度「廃止」として削除→同日 `git revert` で復元。git 管理外の mp4 と `assets/<slug>/tiktok/bg_*.png` は戻らず、元画像（`aerial_1936.png` / `relief.png` / `fillmap_N.png`）のコピーで再描画した（hibiya・ginza・fukagawa・shibuya の背景。元のトリミングとは違う可能性あり）。代用背景の見た目確認は、廃止により行わない
  - 再生されない原因は**未調査**（アカウント側か動画側か不明。推測は書かない）

### 根拠
- claims は `source_type: primary`（一次資料URL必須）か `ai_assistant`（AI回答可・WARN が出る）
- **出典URLの一括到達性チェック**: `docs/themes` 全96テーマ206URLを2026-11-19に実施。結果は [`SOURCE_REVIEW_20261119.md`](SOURCE_REVIEW_20261119.md)。死にリンク4件。到達性と内容の一致は別の確認（後者は未実施）
- **政府PDFの数値は、取得してテキスト抽出（PyMuPDF）＋該当ページの画像目視で確認する**（例: koharu の 51.7%/41.7%、文化庁「平成26年度 国語に関する世論調査」報告書 p.82/86/90・概要版 p.19。`web_fetch` はPDF非対応、PowerShell で取得→`fitz` で抽出）
- 調査結果の数値は「約5割」のような丸めより公表値（小数第1位）を出し、原典の表現（差10ポイント等）を使う
- **年ごとに変わる日付は、その年の公式案内で確認する**（例: 年賀状は2027年用が2026年12月20日引受開始・元日配達の目安が12月27日。過年度の12/15・12/25を一般則にしない。`docs/research/20261118_nenga_sources.md`）

### ブラウザ自動化（重要）
- **Studio と画像生成は CDP + Playwright を使う**（bsk はクリックが弾かれ、ラベルが文字化けする）
- Chrome は `--remote-debugging-port=9222 --user-data-dir=C:\Users\neoen\.chrome-automation` で起動
- 未ログイン・チャンネル違いを検知したら**止まる**（無限リトライしない）
- ChatGPT の生成画像は `blob:` URL。**ページ内 canvas → toDataURL** で取り出す
- **Muse の添付確認は、`img` の blob URL と「添付ファイルを削除」ボタンで判定する**（Muse はファイル名を本文に出さない。前回の下書きが残っていると新しい添付が付かないので、先に削除ボタンを押す。`muse_review.py`、2026-11-18）
- **Muse の「届いていない」検知は、動画・添付を主語にした文だけを見る**（部分一致だと `0.0 dB には届いてない` `偽文字も見当たらない` で誤検知して有効な返答を捨てる。2026-11-19 inou）
- **非公開動画の確認用コピーは Studio のプレビュー配信から取れる**: `studio.youtube.com/video/<id>/edit` の `<video>.currentSrc` を CDP で読み、`context.request.get()` で保存すると 360x640（Short）／640x360（長尺）の圧縮版が得られる。元解像度の確認にはならない（2026-11-20 seijin）。
- **根拠ゲートの `.ac.jp` 判定に注意**（2026-11-20）: 旧版は `.ac.jp` をすべて「大学による再掲」として「代替」明記を要求していたため、発行主体の国立天文台（`www.nao.ac.jp`）まで誤検知した。再掲先は `web.archive.org` と `jahis.law.nagoya-u.ac.jp` の明示ホストに限定し、`.go.jp` / `.ac.jp` は一次発行主体として扱う（回帰テスト追加）。
- **Gemini の動画添付は「アップロードとツール」ボタンを押すと `input[type=file]` が出る**。Short（3.8MB）は送信・回答まで成功したが、長尺（6.7MB）はアップロードが完了せず送信ボタンが無効のまま。Enter ではなく `button[aria-label="プロンプトを送信"]` の有効化を確認する。
- Studio の公開設定は `ytcp-icon-button#select-button`（同じ id が4つあるので限定する）

### 公開
- API は**常に private** でアップロード。公開は Studio（または `studio_cdp.py publish`）
- **同時刻の予約重複は `python scripts/check_slots.py` で API 実測して確認する**（`videos().list` のみ・約7ユニット。重複ありで終了コード1）。**`data/youtube_ids.json` の `publishAt` は予約時にしか書かれず実態より古いので、台帳を正にしない**（2026-11-19、11/19 19:00 の長尺2本を見落とした）。予約経路は3系統（長尺／`_nl` 一括再投稿／新作単独Short）あり、互いの枠を見ていない。枠の原則は 12:00・17:00 に単独Short 1本ずつ、19:00 に長尺1本、20:00 に 19:00 長尺と同題材の Short（`PRODUCTION_CYCLE.md`）
- **「AI の使用」の設定確認は Studio の radio を CDP+Playwright で読む**（`get_by_role('radio')` は shadow DOM を貫通する。`aria-checked` と `aria-label` で「はい、AI を使用しました」が選択済みか判定。`containsSyntheticMedia` は API で書き込めても読み戻しは None）
- Studio の自動化は CDP 9222 の Chrome（`--user-data-dir=%USERPROFILE%\.chrome-automation`）で、**寄り道ラボにログイン済み**であること。未ログインだと `accounts.google.com` へ飛ぶ
- **Xのページが空になるときはリロードする**（2026-11-20）: Chromeのメモリ節約でタブが休止すると `document.body.innerText` が空になり、`x_schedule.py` のアカウント確認や予約オプション検出が失敗する。プロフィール確認と予約オプションの待機に3回のリロード再試行を入れた。成功済みの予約は再実行しない（重複防止）。
- **アップロード前に `data/youtube_ids.json` に同じ `short_<slug>` キーが無いか確認する**（koharu は既に public で登録済みなのに「未アップロード」と誤認し、新版を別IDで上げることになった。作り直しは `--new-version`、旧IDは `superseded` に残る）
- 公開判定は `https://www.youtube.com/oembed?url=...&format=json` が **200/403** で確認できる
- API クォータは**残量で落ち方が変わる**（captions 400 units が落ちても videos.update 50 units は通ることがある）
- 1日のクォータ回復は太平洋時間の深夜（日本時間の夕方ごろ）

### 記録
- 失敗したら「症状 → 原因 → 対処」を [`SHORTS_PRODUCTION_NOTES.md`](SHORTS_PRODUCTION_NOTES.md) に追記する
- 再現できる粒度で書く（URL形式、切り出し比率、セレクタ、コマンド）
- **アップロード済みの動画はローカルから消す**（2026-11-08 実施）。台帳は `data/youtube_ids.json`（全キーに `video_id` がある）
  - 対象は `out/<key>.mp4`、`upload/<key>/video.mp4`、および `scripts/make_upload_pack.py` の対応表にある長尺の元ファイル（`out/gm_video.mp4` など）
  - 台帳にキーが無いもの（`out/short_tiktok_*`、`80_ginza_*_candidate`、モデル比較の `*_video.mp4`）は消さない
  - 再生成は `scripts/make_spec_*.py` → `scripts/vp.py` / `scripts/make_short2.py`。元の台本・素材（`docs/themes/`、`assets/`、`data/*_spec.json`）は残す
- **中間音声（`out/*.wav`）と旧版レンダー（`out/_archive/`）も削除してよい**（2026-11-08）。
  - `out/*_narration.wav` / `out/*_bgm.wav` は描画時に毎回作り直される中間ファイル。描画後に読むスクリプトは無い
  - 例外：`scripts/build_earth_film.py` / `build_youtube_trial.py` は `out/earth_narration.wav` / `out/trial_narration.wav` を入力にするので、その2本を作り直すときは先に wav を再生成する
  - `out/_archive/superseded_renders/` は置き換え済みの旧版。コードからの参照ゼロを確認して削除した（4.4GB）
- **レビュー用の派生物も削除してよい**（2026-11-08 実施、計 3.9GB）。
  - 削除：`out/*_watch/*.png`（フレーム確認用。`audio_report.txt` などのテキストは残す）、`out/*_review/`、`out/*_pv/`、`out/cs*`（コンタクトシート）、`out/qa_tiktok/`、モデル比較の `*_video.mp4`、`upload/80_ginza_*_candidate` などの候補 mp4、`out/ginza_*_work/` の `cache/` と `out/*.mp4`
  - 残す：`out/ginza_*_work/scripts`・`data`・`assets`（`scripts/make_spec_ginza.py` が `out/ginza_remaster_work/assets/ginza_street/*.jpg` を参照）、`out/codex/`（`docs/` から参照）
  - 残す：`out/short_tiktok_*.mp4`、`out/short_mikatagahara.mp4`、`out/short_solo_news_tohoku.mp4`（台帳にキーが無く、アップロード済みか確認できない）
  - `docs/` には `out/oke_review/sheet_*.png` のような**削除済みパスへの記述が残る**（当時の確認記録なので書き換えない）

## 4. 直近の実例（時系列）

| 日付 | 題材 | 学んだこと |
| --- | --- | --- |
| 2026-11-04 | `edo_map_date`（江戸図の年代） | NDL の IIIF 画像利用、資料の切り出し、タイトル文字数、`long_id` 任意化 |
| 2026-11-05 | `shodo_heritage`（書道の無形文化遺産） | ニュース題材、AI生成背景、日付表示、CDP での画像取得と Studio 操作 |
| 2026-11-11 | `kamakura_seiritsu`（鎌倉幕府の成立年） | 図書館レファレンス（NDL crd）を根拠にする方法、`ai_assistant` の使い方、EUC-JP 記事の取得。**needs_review のまま。試作を描画済み（`proto_`・投稿不可）**（[`SHORTS_PRODUCTION_NOTES.md`](SHORTS_PRODUCTION_NOTES.md)） |
| 2026-11-12 | `koharu`（小春日和） | 文化庁世論調査の原典PDF（p.82/86/90）で数値を確認し、Wikipedia の丸め（約5割/約4割）を 51.7%/41.7% に差し替え。画面の出典ラベル（Wikipedia→文化庁・辞書・歳時記）も同時に更新。59.8秒で描画 |
| 2026-11-12 | `yoritomo_zo`（伝源頼朝像＝足利直義説） | 「昔の説→いまの説」型（高年齢層向け）。文化庁DBで国宝指定名称を直接確認、所蔵者（神護寺）の反論も公式ページで確認。**PD の肖像画像を Commons から使い、`sub` パネル・画像の上端境界・`flow` 図の偏りを実測で直した**。**needs_review のまま。試作のみ**（[`SHORTS_PRODUCTION_NOTES.md`](SHORTS_PRODUCTION_NOTES.md)） |
| 2026-11-18 | `nenga`（年賀状の元日配達） | 2027年用は**受付開始2026/12/20・元日配達の目安12/27**（日本郵便FAQ）。過年度の12/15・12/25を一般則にしない。ChatGPTの「場面3が誤解を招く」指摘を採用、Geminiの「年内に届く」は公式に説明がないため不採用。**単独Short経路で制作中（11/26 19:00枠）**（[`research/20261118_nenga_sources.md`](research/20261118_nenga_sources.md) / [`research/20261118_nenga_reviews.md`](research/20261118_nenga_reviews.md)） |
| 2026-11-19 | 予約枠の棚卸し（同時刻の重複） | API 実測で 11/19〜11/21 の5枠に同時刻予約。11/19 19:00 は**長尺2本**（`27_forest` と `79_hibiya`）。原因は予約経路が3系統に分かれていること。**台帳の `publishAt` は実態より古い**ので `scripts/check_slots.py`（API実測）で確認する。当日分4件を移動し重複ゼロ（[`SHORTS_PRODUCTION_NOTES.md`](SHORTS_PRODUCTION_NOTES.md)） |
| 2026-11-20 | 根拠テーブルゲート＋`seijin` 再利用 | `data/short_*.json` に `claims` を埋め、アップ前・CI・pre-commit で検査。既存284本は祖父化。成人の日は未公開の `short_seijin` を再利用し、1/11 19:00 長尺＋20:00 Short のペア公開を予定（**AIレビューは両方「公開可」完了。実聴・予約は未実施**）。[`SHORT_EVIDENCE_GATE_20261120.md`](SHORT_EVIDENCE_GATE_20261120.md) |
| 2026-11-22 | `baby_hone` / `baby_namida` / `fuji` のAIレビュー | Google AIモードで台本・動画をレビューし、指摘を原文と実フレームで照合して再描画。3本とも最終版「公開可」。ChatGPTはCDP未ログインで未実施。根拠テーブル・アップ・予約は未実施（[`research/20261122_baby_fuji_reviews.md`](research/20261122_baby_fuji_reviews.md)） |
| 2026-11-22 | `thunder_metal`（雷と金属） | 提案3案のうち制作可能と判断して新規制作。学会論文p.53/54/56と気象庁本文で根拠を確認し、根拠ゲートOK（WARN 3）。自作イラスト背景、60.4秒。Google AIモードで台本3回・動画4回レビューし、残る指摘は原文・silencedetectで照合して不採用（[`research/20261122_thunder_metal_sources.md`](research/20261122_thunder_metal_sources.md)） |

## 5. 調査・検証の記録（2026-11-11、エージェントチーム作業）

| 文書 | 内容 | 要点 |
| --- | --- | --- |
| [`research/20261120_channel_performance_28d.md`](research/20261120_channel_performance_28d.md) | 過去28日間のパフォーマンス要約 | Shorts 72,467回／長尺198回。Shorts優先方針の裏付け。11/16に視聴回数の集計仕様変更あり |
| [`SHORTS_ANALYTICS_20261120.md`](SHORTS_ANALYTICS_20261120.md) / [`data/shorts_analytics_20261120.json`](../data/shorts_analytics_20261120.json) | 全Shorts（127本）のアナリティクス調査と戦略 | 30〜45秒が中値715回、歴史622回、再生率>100%の13本は918回。新型フックはスワイプ悪化で11/26まで保留 |
| [`research/20261120_seijin_reviews.md`](research/20261120_seijin_reviews.md) | 成人の日Shortの ChatGPT/Gemini 台本レビュー | 両方「公開可」。軽微な改善提案（シーン5の文言・小テロップ等）は、再描画と新ID差し替えが必要なため今回は不採用。次回の新規制作の候補として記録 |
| [`research/20261120_seijin_video_qa.md`](research/20261120_seijin_video_qa.md) | 成人の日Short/長尺の動画確認 | Studio プレビュー配信から非公開動画を取得。全編デコード・音量・字幕時刻＋Gemini 動画レビュー（Short は「公開可」）＋代表フレーム目視。元解像度・スマホ実機・人間の実聴は未実施 |
| [`research/20261120_islands_reviews.md`](research/20261120_islands_reviews.md) | 日本の島の数Shortの台本レビューと候補変更 | ChatGPT「公開可」／Gemini「修正必要」（表現のみ）。計算表現に難のあった magnitude 候補から差し替え。国土地理院の報道発表本文を確認 |
| [`research/20261120_islands_video_qa.md`](research/20261120_islands_video_qa.md) | 同Shortの動画確認と予約 | 全編デコード・音量・字幕時刻・代表フレーム目視はOK。Geminiの動画添付は失敗。1/11 12:00に予約、他2件は予約解除 |
| [`research/20261120_equinox_sources.md`](research/20261120_equinox_sources.md) / [`20261120_equinox_reviews.md`](research/20261120_equinox_reviews.md) | 春分／秋分Shortの根拠と台本レビュー | 国立天文台FAQの数値・2理由を確認。ChatGPT公開可／Gemini修正必要の共通指摘を描画前に反映 |
| [`research/20261120_equinox_video_qa.md`](research/20261120_equinox_video_qa.md) | 同Shortの動画確認と予約 | 56.5秒・-14.08 LUFS・ASR一致。出典行の見切れを直してMuse「公開可」。`ZSRepHwe500` を1/12 12:00に予約 |
| [`research/20261120_proto_tatsumaki.md`](research/20261120_proto_tatsumaki.md) | 戦略を試す試作（竜巻注意報） | 今日のニュースを30〜45秒で検証。44.0秒・Muse「公開可」。背景は既存クリップ流用で、未アップ・未予約 |
| [`research/20261120_rain0.md`](research/20261120_rain0.md) | 降水確率0%ショートの調査・制作 | 0%=5%未満の丸め＋1ミリ未満対象外。気象庁＋市立気象館を確認。44.1秒・Muse公開可。11/22 20:00予約 |
| [`research/20261120_ambulance.md`](research/20261120_ambulance.md) | 救急車の軽症ショート | Ask Studioの提案から選択。消防庁の46.9%=軽症＋その他を一次確認。Google AIモードで公開可。11/23 20:00予約 |
| [`research/20261122_baby_fuji_reviews.md`](research/20261122_baby_fuji_reviews.md) | 赤ちゃん2本＋富士山Shortの台本・動画AIレビュー | 字幕の改行誤読は実フレームで確認してから修正。結論カードの出し順・日付の読み上げを調整。ChatGPT未ログインと根拠テーブル未記入を明記 |
| [`research/20261122_thunder_metal_sources.md`](research/20261122_thunder_metal_sources.md) | 雷と金属Shortの出典確認とAIレビュー | 金属を外す必要はない（論文p.56）。気象庁は「まず安全な空間へ」、木は幹・枝・葉から2m以上。AIの無音1.2秒指摘は実測0.4秒で不採用 |
| [`research/20261111_kamakura_release_check.md`](research/20261111_kamakura_release_check.md) | 公開予約済み Shorts `kamakura_seiritsu`（11/16 17:00）の公開前チェック | validate PASS・check は ERROR 0/WARN 7。`status` は `needs_review` のまま（標準は緩めない）。公開前に Studio で「AIの使用」と概要欄全文を目視。`FreeVideo(MiniMax H3)` の利用条件が権利台帳に無い |
| [`research/20261111_worktree_review.md`](research/20261111_worktree_review.md) | 未コミット変更の検証 | `scripts/_chain3.sh` は使い捨てキューによる事故 → 復元。`end_q` は休眠機能で安全。`proto_spec.json` の credit は描画済み FV 版と一致 |
| [`research/20261111_takatenjin_sources.md`](research/20261111_takatenjin_sources.md) | 高天神城（天正9年落城）の一次資料到達性 | 『信長公記』『三河物語』『甲陽軍鑑』の本文に到達（NDL・PDM）。落城日は諸説（22日／25日）。**救援不出の理由は後世の『甲陽軍鑑』に依存**＝制作時の最大リスク |
| [`research/20261112_toji_sources.md`](research/20261112_toji_sources.md) | 冬至 Short の根拠（気象庁平年値・国立天文台） | 東京の1991〜2020年平年値では気温の底は**1月下旬（日別1/21〜22）**、冬至から**約1か月**。NEXT_TOPICS の「2月上旬」「1か月半」は不支持。日の出最遅は半月後・日の入最早は半月前 |
| [`research/20261112_edo_shuiki_sources.md`](research/20261112_edo_shuiki_sources.md) | 江戸朱引図の到達性（12/10 枠） | 公文書館「旧江戸朱引内図」は高精細画像2コマが認証なしで取得可（IIIF非対応）、NDL切絵図は IIIF+PDM。**朱引＝御府内／墨引＝町奉行支配**で前提修正が必要。二次利用条件と朱引線の視認は未了 |
| [`research/20261112_yoritomo_zo_sources.md`](research/20261112_yoritomo_zo_sources.md) | 神護寺「伝源頼朝像」＝足利直義説の根拠到達性 | 文化庁の2DBで名称「絹本著色伝源頼朝像」・国宝1951.06.09・神護寺蔵を直接確認。**所蔵者は公式サイトで新説に反論**。願文の年は1345年（帝国書院FAQのみ1354年で不一致→動画では年を言わない）。教科書の会社別・年度別比較は未取得。Commons の画像は PD だが**撮影者不明** |

## 6. 未対応・残課題

- **楽天アフィリエイト（商品起点）の企画は別プロジェクトへ移設した**（2026-11-16）。移設先は `E:\rakuten-shorts-affiliate`（独立した git リポジトリ）。調査・設計・台本・制作標準のコピーはそちらにある。このリポジトリには残していない
- 画像は API（`OPENAI_API_KEY`）にできれば最も安定（ブラウザは UI 変更に弱い）
- 既存の `data/short_*.json`（旧形式）の標準形式への移行
- 長尺と Shorts の自動ペアリング（現在は手動）
| [`SHORTS_PRODUCTION_NOTES.md`](SHORTS_PRODUCTION_NOTES.md) | 2026-11-17追記: Analyticsの日別区切りは**太平洋時間**（JST 17:00）／**離脱は4〜7秒**（Ask Studio実測）／未予約在庫94本は既出の別版が多い |


## 差し替え版（AIクリップ未使用のREJECT対応、2026-11-22）

- 自作イラスト背景の `solo_thunder_metal` が「AIクリップを使っていない」とREJECTされたときは、元成果物を残したまま別slug（`thunder_metal_fv`）で台本・根拠を共有して作り直す（[`SHORTS_PRODUCTION_NOTES.md`](SHORTS_PRODUCTION_NOTES.md) の同名節）。
- `scripts/google_ai_review.py` は **システムの Python312**（`C:/Users/neoen/AppData/Local/Programs/Python/Python312/python.exe`）で実行する。プロジェクトの `.venv` には playwright も pip も入っていない。返答が「考えっています」のまま保存されることがあるので、保存文に回答本文があるか確認する。

- YouTube API（アップロード／予約）は **Python312 + `PYTHONPATH=C:/Users/neoen/AppData/Local/Programs/Python/Python311/Lib/site-packages`** で動かす（Python311 は site-packages だけ残っていて python.exe が無い）。`check_slots.py` / `yt_api.py` はこの組み合わせで実動確認済み。
- オーナーが「お試しにアップロード」と明示した場合は、根拠ゲートを緩めずに `yt_api.py upload` 経路で手動アップし、二次資料のみであることを research に残す（2026-11-22 赤ちゃん2本）。

- **概要欄（説明欄）は視聴者向けだけにする。** レビューの採用／不採用、字幕の改行判断、「動画では使っていないこと」、調査のタイムアウト記録などは内部メモで、`docs/research/` に残す。2026-11-22 に3本の公開ずみ説明欄へ内部メモが混入したため、`gen_solo_*.py` の `notes` を公開用に短縮し、APIで説明欄を差し替えた（予約時刻は維持）。`bg_note=''` を渡すと背景クレジットの重複を省ける（`solo_spec.build()` が空文字を尊重）。

- 2026-11-22: 全377本の説明欄を走査し、内部メモが残っていた57本をAPIで除去（`docs/research/20261122_description_cleanup.md`）。`scripts/solo_spec.py` の `public_notes()` が `build()` 時に内部メモ行を落とすので、generator を再実行すれば清潔な説明欄が作れる。走査は `videos().list(part='snippet,status')` とパターン照合で再現可能。

- スワイプ率は Analytics API に無く Studio 画面のみ。`scripts/studio_swipe.py <video_id>` で CDP 9222 の Studio 分析から「視聴を継続／スワイプして消去」を読める（2026-11-23追加、既存3本で実測一致を確認）。KPI判定は [`kpi_swipe_tracking.md`](kpi_swipe_tracking.md) の閾値と手順に従う。

- YouTube APIのrefresh tokenは失効することがある。`invalid_grant` が出たら `scripts/yt_api.py auth` を実行し、ブラウザで「寄り道ラボ」を選んで承認してもらう（2026-11-23実例）。予約時刻の変更はAPIの `videos().update(part='status', publishAt=...)`、X予約の変更は `scripts/x_reschedule.py <video_id> "YYYY-MM-DD HH:MM"`（CDP 9223）。

- `google_ai_review.py` が「送信ボタンが有効にならない」で止まったときは、ファイル添付済みのタブから続きを送信する `scripts/google_ai_followup.py <slug> [--extra "..."]` を使う（2026-11-23追加、CDP 9222）。レビュー完了後に自分で開いたタブは閉じる。

- 予約済みX投稿のURLだけを差し替えるときは `scripts/x_replace_url.py <old_id> <new_id>`（CDP 9223）。本文のURLを置換し、日時が変わらないことを確認してから保存し、予約一覧で旧ID0件・新ID1件を確認する（2026-11-23実例）。動画差し替えは新IDアップ→旧IDを2027-01-01へ退避→X URL差し替えの順。

- 予約済み動画を即時公開するとき、Studio UI の「公開」ラジオが出ない場合は API で `videos().update(part='status', privacyStatus='public')` に `publishAt` を入れずに送れば予約が消えて公開される（2026-11-23実例）。更新後に `privacyStatus=public` / `publishAt=None` を読み戻して確認し、台帳は `privacy=public`・`publishedAt` を記録して `publishAt` を消す。
