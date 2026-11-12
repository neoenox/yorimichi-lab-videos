# ノウハウの入口（まずこれを読む）

更新日: 2026-11-11。**制作で分かったことは必ず git に残す**（AGENTS.md）。この文書は「どこに何が書いてあるか」の索引。

## 1. 動画を作るときに読む順番

| 順 | 文書 | 内容 |
| --- | --- | --- |
| 1 | [`VIDEO_CREATION_PRECHECK.md`](VIDEO_CREATION_PRECHECK.md) | 制作前の必須確認（工程・根拠と演出の分離・未確認を完了扱いしない） |
| 2 | [`SHORTS_STANDARD_INTEGRATION.md`](SHORTS_STANDARD_INTEGRATION.md) | Shorts 制作標準の使い方・既存パイプラインとの差分・検査の階層 |
| 3 | [`SHORTS_PRODUCTION_NOTES.md`](SHORTS_PRODUCTION_NOTES.md) | **実測ノウハウ本体**（画面の安全領域、資料画像、AI生成、投稿、失敗と対処） |
| 4 | [`VIDEO_PRODUCTION_RUNBOOK.md`](VIDEO_PRODUCTION_RUNBOOK.md) | 長尺の手順（VOICEVOX・描画・公開・トラブル対処） |
| 5 | [`MAIN_TEXT_ONLY_WORKFLOW.md`](MAIN_TEXT_ONLY_WORKFLOW.md) | リモートへ素材を上げない運用（push の作法） |

## 2. ツール（スクリプト）と役割

| スクリプト | 役割 | 実測 |
| --- | --- | --- |
| `scripts/shorts_standard.py` | 標準 JSON の検査（`validate.py` 実行＋追加規則）とレンダラ spec への変換 | 2026-11-04 |
| `scripts/gen_image_cdp.py` | **ChatGPT の画像生成**（Chrome を CDP で操作、blob 画像を canvas 経由で取得） | 2026-11-05 |
| `scripts/studio_cdp.py` | **Studio の公開設定・字幕**（Playwright、チャンネルID検証つき） | 2026-11-05 |
| `scripts/chatgpt_image.py` | bsk 経由の画像生成（**不安定・非推奨**。CDP 版を使う） | 2026-11-05 |
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
- 画面の安全領域: タイトル y≈200（**全角18文字まで**）／大テロップ y≈520／字幕 1470–1540／注記は 1556 以降
- 背景は **シーンごとに変える**（`art_map.json`）。同じ絵が続くと単調
- 明るい画像の上に字幕を置くときは、**下半分に暗幕**を入れる（入れないと読めない）
- **TikTok 向けの制作は廃止**（2026-11-11 オーナー判断：投稿しても動画が再生されないため）。**新規制作・投稿準備・背景の作り直しはしない**。`check_tiktok.py` / `tiktok_launch_audit.py` / `tiktok_post.py` も実行不要
  - 既存の物は**削除せず残す**（方針A）：`out/short_tiktok_*.mp4`、`data/short_tiktok_*.json`、`assets/*/tiktok/`、`docs/TIKTOK_*.md`、関連スクリプト。再開する場合の参考資料扱い
  - `docs/TIKTOK_STRATEGY.md` / `docs/TIKTOK_POSTING_PACK.md` は廃止前の計画（11/02 時点）。**現行の方針ではない**
  - 経緯：11/08 に一度「廃止」として削除→同日 `git revert` で復元。git 管理外の mp4 と `assets/<slug>/tiktok/bg_*.png` は戻らず、元画像（`aerial_1936.png` / `relief.png` / `fillmap_N.png`）のコピーで再描画した（hibiya・ginza・fukagawa・shibuya の背景。元のトリミングとは違う可能性あり）。代用背景の見た目確認は、廃止により行わない
  - 再生されない原因は**未調査**（アカウント側か動画側か不明。推測は書かない）

### 根拠
- claims は `source_type: primary`（一次資料URL必須）か `ai_assistant`（AI回答可・WARN が出る）
- 数字・固有名詞・因果関係は可能なら一次資料で裏取り。誤りが判明したら概要欄で訂正
- **政府PDFの数値は、取得してテキスト抽出（PyMuPDF）＋該当ページの画像目視で確認する**（例: koharu の 51.7%/41.7%、文化庁「平成26年度 国語に関する世論調査」報告書 p.82/86/90・概要版 p.19。`web_fetch` はPDF非対応、PowerShell で取得→`fitz` で抽出）
- 調査結果の数値は「約5割」のような丸めより公表値（小数第1位）を出し、原典の表現（差10ポイント等）を使う

### ブラウザ自動化（重要）
- **Studio と画像生成は CDP + Playwright を使う**（bsk はクリックが弾かれ、ラベルが文字化けする）
- Chrome は `--remote-debugging-port=9222 --user-data-dir=C:\Users\neoen\.chrome-automation` で起動
- 未ログイン・チャンネル違いを検知したら**止まる**（無限リトライしない）
- ChatGPT の生成画像は `blob:` URL。**ページ内 canvas → toDataURL** で取り出す
- Studio の公開設定は `ytcp-icon-button#select-button`（同じ id が4つあるので限定する）

### 公開
- API は**常に private** でアップロード。公開は Studio（または `studio_cdp.py publish`）
- **「AI の使用」の設定確認は Studio の radio を CDP+Playwright で読む**（`get_by_role('radio')` は shadow DOM を貫通する。`aria-checked` と `aria-label` で「はい、AI を使用しました」が選択済みか判定。`containsSyntheticMedia` は API で書き込めても読み戻しは None）
- Studio の自動化は CDP 9222 の Chrome（`--user-data-dir=%USERPROFILE%\.chrome-automation`）で、**寄り道ラボにログイン済み**であること。未ログインだと `accounts.google.com` へ飛ぶ
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

## 5. 調査・検証の記録（2026-11-11、エージェントチーム作業）

| 文書 | 内容 | 要点 |
| --- | --- | --- |
| [`research/20261111_kamakura_release_check.md`](research/20261111_kamakura_release_check.md) | 公開予約済み Shorts `kamakura_seiritsu`（11/16 17:00）の公開前チェック | validate PASS・check は ERROR 0/WARN 7。`status` は `needs_review` のまま（標準は緩めない）。公開前に Studio で「AIの使用」と概要欄全文を目視。`FreeVideo(MiniMax H3)` の利用条件が権利台帳に無い |
| [`research/20261111_worktree_review.md`](research/20261111_worktree_review.md) | 未コミット変更の検証 | `scripts/_chain3.sh` は使い捨てキューによる事故 → 復元。`end_q` は休眠機能で安全。`proto_spec.json` の credit は描画済み FV 版と一致 |
| [`research/20261111_takatenjin_sources.md`](research/20261111_takatenjin_sources.md) | 高天神城（天正9年落城）の一次資料到達性 | 『信長公記』『三河物語』『甲陽軍鑑』の本文に到達（NDL・PDM）。落城日は諸説（22日／25日）。**救援不出の理由は後世の『甲陽軍鑑』に依存**＝制作時の最大リスク |
| [`research/20261112_toji_sources.md`](research/20261112_toji_sources.md) | 冬至 Short の根拠（気象庁平年値・国立天文台） | 東京の1991〜2020年平年値では気温の底は**1月下旬（日別1/21〜22）**、冬至から**約1か月**。NEXT_TOPICS の「2月上旬」「1か月半」は不支持。日の出最遅は半月後・日の入最早は半月前 |
| [`research/20261112_edo_shuiki_sources.md`](research/20261112_edo_shuiki_sources.md) | 江戸朱引図の到達性（12/10 枠） | 公文書館「旧江戸朱引内図」は高精細画像2コマが認証なしで取得可（IIIF非対応）、NDL切絵図は IIIF+PDM。**朱引＝御府内／墨引＝町奉行支配**で前提修正が必要。二次利用条件と朱引線の視認は未了 |
| [`research/20261112_yoritomo_zo_sources.md`](research/20261112_yoritomo_zo_sources.md) | 神護寺「伝源頼朝像」＝足利直義説の根拠到達性 | 文化庁の2DBで名称「絹本著色伝源頼朝像」・国宝1951.06.09・神護寺蔵を直接確認。**所蔵者は公式サイトで新説に反論**。願文の年は1345年（帝国書院FAQのみ1354年で不一致→動画では年を言わない）。教科書の会社別・年度別比較は未取得。Commons の画像は PD だが**撮影者不明** |

## 6. 未対応・残課題

- 画像は API（`OPENAI_API_KEY`）にできれば最も安定（ブラウザは UI 変更に弱い）
- 既存の `data/short_*.json`（旧形式）の標準形式への移行
- 長尺と Shorts の自動ペアリング（現在は手動）
