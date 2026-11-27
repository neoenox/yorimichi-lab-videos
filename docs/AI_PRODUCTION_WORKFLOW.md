# AI活用 動画制作ワークフロー（寄り道ラボ）

作成：2026-11-24。目的：品質の関門を落とさずに、1本あたりの人手を減らす。

このリポジトリには既に自動化が進んでいる。制作は1本約10分（待ち時間込み、`docs/PRODUCTION_CYCLE.md`）。足りないのは作る速度ではなく、題材の決定、一次資料の確認、AI指摘の裏取り、導線の設定に人要ること。したがってAIを入れる場所は「調べる・書く・作る」ではなく「候補を出す・確かめる・測る」に寄せる。

## 0. 原則

1. 最終決定は人。AIは候補と下書きを出す。
2. 事実の断定は一次資料と原文照合が済んだものだけ。AIの回答は `ai_assistant` として扱い、単独で断定に使わない。
3. 同じ型が5本たまるまで「勝ち」と呼ばない（[hook_patterns.md](hook_patterns.md)）。
4. 時間が足りないときは本数を減らす。品質の関門は省かない（`docs/PRODUCTION_CYCLE.md`）。
5. 試作・編集版・完成候補・投稿済みは版を分ける。元成果物を上書きしない（[VIDEO_CREATION_PRECHECK.md](VIDEO_CREATION_PRECHECK.md)）。

## 1. 推奨ツール（このリポジトリで実際に使われているもの）

| 工程 | 道具 | 役割 | 出典・実測 |
|---|---|---|---|
| 題材探し | 公式新着一覧を `curl`、WebSearch、ChatGPT | 一次情報の新着を直接読む。ChatGPTは候補出しのみ | [SOLO_SHORT_PROCEDURE.md](SOLO_SHORT_PROCEDURE.md) 2b |
| 既出照合 | `data/youtube_ids.json`＋`docs/` 全体 grep＋[NICHE_AND_100_IDEAS_20261124.md](NICHE_AND_100_IDEAS_20261124.md) | 重複提案を防ぐ | 2026-11-23 オーナー指示 |
| 需要 | サジェストAPI（`data/suggestion_20261124.json`）＋`topic_pick.py` | 検索語の実測と採点 | [NICHE_AND_100_IDEAS_20261124.md](NICHE_AND_100_IDEAS_20261124.md) |
| 原文取得 | `curl`、`fitz`（PDF）、Wikipedia REST、国土地理院 | 一次資料の本文を UTF-8 で保存 | [SOLO_SHORT_PROCEDURE.md](SOLO_SHORT_PROCEDURE.md) 2 |
| 台本下書き | `solo_spec.build`、`vp.py`、完成例の `gen_solo_*.py` | 台本・spec を生成 | [SOLO_SHORT_PROCEDURE.md](SOLO_SHORT_PROCEDURE.md) 3 |
| 台本レビュー | Google AIモード＋ChatGPT（`scripts/google_ai_review.py`、`scripts/review_short_cdp.py`） | 指摘を出す。裏取りは人がする | [KNOWHOW.md](KNOWHOW.md) |
| 音声 | VOICEVOX 四国めたん、`scripts/hn_audio.py` | 自動合成 | [PRODUCTION_CYCLE.md](PRODUCTION_CYCLE.md) |
| 背景 | FreeVideo（MiniMax H3）の `fv_clips.sh`、国土地理院 | AI映像と地図 | AGENTS.md（2026-11-23 置換） |
| 描画 | `make_short2.py`、`vp.py`、Blender、FFmpeg | 縦型Shortと長尺 | [PRODUCTION_CYCLE.md](PRODUCTION_CYCLE.md) |
| 読み検証 | `asr_kotoba.py`、`_kana.txt` | 数字・日付・固有名詞の一致 | [SOLO_SHORT_PROCEDURE.md](SOLO_SHORT_PROCEDURE.md) 5 |
| 動画レビュー | Google AIモード（`--mode video`） | 「公開可」が出るまで | [KNOWHOW.md](KNOWHOW.md) |
| 投稿 | `solo_schedule.py`、`yt_api.py`、`finish_all.py` | 非公開アップ・予約・台帳 | [SOLO_SHORT_PROCEDURE.md](SOLO_SHORT_PROCEDURE.md) 7 |
| X宣伝 | Playwright（`scripts/x_reschedule.py`） | 公開5分後の予約投稿 | [SOLO_SHORT_PROCEDURE.md](SOLO_SHORT_PROCEDURE.md) 8 |
| 計測 | `yt_api.py stats`、`collect_stats.py`、`studio_swipe.py`、Ask Studio | APIとStudioの両方 | [PRODUCTION_CYCLE.md](PRODUCTION_CYCLE.md) |

Museは起動しない。Geminiは必須ではない（AGENTS.md、2026-11-20）。

## 2. 工程ごとのワークフロー

### 2-1. テーマ調査

1. 曜日の担当を決める。月曜に週分まとめて候補を出す（[PRODUCTION_CYCLE.md](PRODUCTION_CYCLE.md)）。
2. AIに10案を出させる。各案に「問い・見せ場・必要素材・根拠の見通し・懸念」を書かせる。知らないことは「不明」と書かせる（[THEME_SELECTION_PROCEDURE_V2.md](THEME_SELECTION_PROCEDURE_V2.md) 4）。
3. 既出を3系統で照合する。台帳、docs全体のgrep、100本の候補表。重複が見つかったら提案を取り下げる。
4. 需要をサジェストAPIで確かめる。AIの需要判断は使わない。
5. 一次資料の関門を通す。一次史料または専門書で骨格を確認できない案は落とす（同手順 3）。
6. 人が上位3案から選ぶ。落とした案の理由を1行で残す。

AIに任せるのは2まで。3〜6は人が行う。

### 2-2. 台本作成

1. 近い型の完成例を1つ選び、書き写して直す（[SOLO_SHORT_PROCEDURE.md](SOLO_SHORT_PROCEDURE.md) 冒頭）。ゼロから書かない。
2. `08_fact_check.md` に主張ごとの根拠と原文を先に書く。台本より先。
3. 台本v1を `gen_solo_<slug>.py` で作る。`solo_spec.build` に `tags=[...]` を必ず渡す。欠けると前の動画のタグが引き継がれる（2026-11-16に実例）。
4. 台本レビューをGoogle AIモードとChatGPTに依頼する。背景生成の前に行う。
5. 指摘を原文と実フレームで照合してから採用・不採用を決める。判断を `docs/research/` に残す。
6. 台本v2を凍結する。台本を変えると音声の尺と全シーンの開始時刻がずれ、描画が作り直しになる（[VIDEO_PRODUCTION_RUNBOOK.md](VIDEO_PRODUCTION_RUNBOOK.md)）。

短尺の実測は30〜45秒が中央値715回・平均視聴率60.9%で最良（[SHORTS_ANALYTICS_20261120.md](SHORTS_ANALYTICS_20261120.md)）。手順書の50〜58秒は古い目標なので、新しいShortは30〜45秒を優先する。矛盾がある場合はユーザーに確認する。

### 2-3. ナレーションと収録

- 顔出し・声出しなし。VOICEVOXで自動合成する。
- `pron`（読み辞書）に固有名詞・難読語を登録する。ナレーション全文を `_kana.txt` で目で確認し、ASRで数字・日付の一致を見る。
- カタカナを入れると逆に誤読になる語がある（[VIDEO_PIPELINE_VP.md](VIDEO_PIPELINE_VP.md)）。辞書を足したら必ず `vp.py <slug> kana` で確認する。
- 日付の読み上げは独立文にしない。不自然に間が空くため、音声から削り、`src` と概要欄に残す（2026-11-19の判断）。

### 2-4. 編集と描画

- 長尺は `vp.py` の `story→kana→audio→ends→still→build→desc→pack`。Shortは `solo_ship.py build` または `make_short2.py`。
- 描画の前に `still` で全場面を試し描画する。表の行が増えて枠を越えると、本番ビルドで `part render failed` になる（[VIDEO_PIPELINE_VP.md](VIDEO_PIPELINE_VP.md)）。
- 差分再描画は部品の指紋でスキップされる。台本を変えない限り全部作り直さない。
- 画面の安全領域、文字数、音量の基準は [SOLO_SHORT_PROCEDURE.md](SOLO_SHORT_PROCEDURE.md) 0b をそのまま使う。

### 2-5. サムネイル

- `vp.py thumb` の spec で分野ごとに配色を変える（[PRODUCTION_CYCLE.md](PRODUCTION_CYCLE.md) 方針変更）。
- 1つの対象と1つの数字。生成画像・模式図は明示する。
- 動画別CTRはStudioから取得する。APIには無い。同じ型が5本たまるまで判断しない。

### 2-6. 公開

1. 機械検査を通す。`check_short_evidence.py`、`shorts_standard.py check`、ffmpegの音量・デコード。
2. Google AIモードの動画レビューで「公開可」が出るまで直す。
3. 非公開アップ→予約→AI使用「はい」→台帳→X予約。
4. 公開前に `check_slots.py` で同時刻の重複を確認する。台帳の `publishAt` は古いことがあるのでAPI実測を正とする（[KNOWHOW.md](KNOWHOW.md)）。
5. Shortを長尺へ導く場合は、長尺19:00→19:30までに関連動画設定→Short 20:00の順を守る（[CHANNEL_STRATEGY_20261124.md](CHANNEL_STRATEGY_20261124.md)）。

### 2-7. データ分析

- 48時間後と7日後に数字を記録する。インプレッション・CTR・維持率・流入元はStudio、再生数と登録者はAPI（[PRODUCTION_CYCLE.md](PRODUCTION_CYCLE.md) 3）。
- 月曜に集計して `channel_profile.json` を更新し、次の題材採点に反映する。
- 活用7割・探索3割。15本公開までは実績の重みを小さくする（同 4）。
- 相関は因果ではない。尺・題材・時期を揃えない比較は仮説として扱う。

## 3. 複数プラットフォームへの再利用

現状の方針を先に述べる。

- **YouTube Shorts**：主戦場。30〜45秒を標準にする。
- **X**：新作の紹介投稿を公開5分後に予約する運用が確立している（[SOLO_SHORT_PROCEDURE.md](SOLO_SHORT_PROCEDURE.md) 8）。再利用というより宣伝。
- **TikTok**：2026-11-11に展開中止。投稿しても再生されなかったため。[TIKTOK_POSTING_PACK.md](TIKTOK_POSTING_PACK.md) は廃止文書で、現行の方針ではない。したがってTikTok向けの自動再投稿システムは作らない。再開するならオーナーの明示的な判断が要る。
- **Instagram Reels**：このリポジトリに制作・投稿の記録は無い。未着手。

再利用するときの共通ルールは3つ。

1. 切り抜きはShortの完走率を落とすので、単独Shortは独立した問いとして作る（[CHANNEL_STRATEGY_20261124.md](CHANNEL_STRATEGY_20261124.md)）。
2. 縦型の字幕安全領域はプラットフォームのUIで隠れる。TikTokの廃止前のチェックでは「字幕が画面下のUIに隠れていない」を確認していた（[TIKTOK_POSTING_PACK.md](TIKTOK_POSTING_PACK.md)）。再利用先が増えたら同じ確認をする。
3. AI映像・生成画像を使った動画は、各プラットフォームの表明ルールに従う。YouTubeでは「AIの使用＝はい」と概要欄への明記。ほかは未確認。

## 4. テンプレート

### 4-1. 台本レビュー依頼（そのまま使う）

```
この動画のレビューをお願いします。添付は、〈題材〉のYouTube Shorts(約〈秒〉秒)です。
背景は〈AI生成の映像(…)／国土地理院の写真〉で、概要欄に〈出典〉と〈AI生成の明示〉を書きます。
まず、ナレーションを文字に書き起こしてください(台本と照合します)。
見てほしい点は、(1)字幕と音声の一致、(2)読み間違い・音割れ・無音(〈気になる語〉の読みを特に)、(3)文字の重なり・はみ出し・見切れ、(4)事実関係と日付・数字、(5)冒頭1〜3秒の引き、(6)AI映像の不自然さ(文字や額が映っていないか)、(7)公開してよいか。
問題点は時刻つきで具体的にお願いします。
```

出典：[SOLO_SHORT_PROCEDURE.md](SOLO_SHORT_PROCEDURE.md) 9章のひな形。

### 4-2. 題材候補の依頼

```
あなたは日本史・科学の解説動画の企画者です。
条件：〈01_conditions.md〉
需要の下調べ：〈02_demand.md〉
次の形式で10案を出してください。他のAIの案は見ていません。
1. テーマ名　2. 問い　3. 見せ場(3つまで)　4. 必要素材と権利の見込み
5. 事実確認の見通し(どの一次史料で確かめられるか。分からなければ「不明」)
6. 懸念(炎上・誤情報・権利)
知らないことを、あるように書かないでください。
```

出典：[THEME_SELECTION_PROCEDURE_V2.md](THEME_SELECTION_PROCEDURE_V2.md) 4。

### 4-3. 説明欄 `notes` に書くこと

確認日、URL、使った事実、使わなかった事実、言い過ぎを避けた点、未確認、レビューで直した点（[SOLO_SHORT_PROCEDURE.md](SOLO_SHORT_PROCEDURE.md) 3）。内部メモは書かない。2026-11-22に内部レビューメモが混入した事例がある。

## 5. 品質管理チェックリスト

### 公開前（すべて満たすまで予約しない）

- [ ] 一次資料の原文を開き、主張ごとに `08_fact_check.md` へ記録した
- [ ] 既出を台帳・docs全体・100本の表で照合した
- [ ] AIの指摘を原文と実フレームで照合し、採否を `docs/research/` に残した
- [ ] 台本を凍結してから音声と描画を作った
- [ ] `tags=[...]` を渡し、アップ後にタグをAPIで読み戻した
- [ ] 尺が基準内（Short 30〜45秒を優先）
- [ ] 冒頭に挨拶が無く、1秒目に結論か数字がある
- [ ] 大見出し12字以内、カード14〜15字以内、重なり・はみ出しなし
- [ ] `pron` を登録し、`_kana.txt` を目で確認し、ASRで数字・日付が一致した
- [ ] 音量 −14 LUFS前後、ピーク −1.0〜−1.5 dBTP、0.8秒以上の無音なし（末尾除く）
- [ ] 背景に文字・額・刻印・電線・人物が出ていない（AI映像の場合）
- [ ] 「イメージです」「模式図」を画面と概要欄に明記した
- [ ] Google AIモードの動画レビューで「公開可」が出た
- [ ] `check_short_evidence.py` と形式検査が通った
- [ ] `check_slots.py` で同時刻の重複がない
- [ ] AI使用「はい」、台帳の `publishAt`、X予約を確認した

### 書き出し後

- [ ] 代表場面を時間順に並べ、変化の順番と字幕の対応を確認した
- [ ] 場面の前後、ズーム端、素材切替、画面端、テロップ出入りを静止画で確認した
- [ ] 最終候補をプレーヤーで連続再生した
- [ ] 音声付き動画は全編を実際に聴いた（LUFSとデコード検査では代替しない）
- [ ] スマホ表示で要点が読める
- [ ] 報告で「確認した範囲」と「未確認」を分けた

出典：[VIDEO_CREATION_PRECHECK.md](VIDEO_CREATION_PRECHECK.md)、[SOLO_SHORT_PROCEDURE.md](SOLO_SHORT_PROCEDURE.md) 0b。

## 6. 人が残る場所

AIに委ねないのは次だけ。

- 題材の最終決定と需要の責任
- 一次資料の原文照合と、AI指摘の採用・不採用
- 台本の凍結
- 公開可の最終判断
- 予約枠の実測と台帳の修正
- 報告での「未確認」の線引き

ここを自動化すると、1円玉の製造コストのような「一次資料で確認できない数字」が台本に戻る。時間が足りないときは本数を減らし、この一覧は削らない。

## 7. 未確認・注意

- Instagram Reelsの制作・投稿手順はこのリポジトリに無い。着手するなら新たに調べる。
- TikTokは中止済み。再開はオーナー判断が要る。
- 手順書のShort尺（50〜58秒）と実測（30〜45秒が有利）が食い違う。新しいShortは実測を優先するが、手順書自体はオーナーの承認なしに書き換えない。
- `jsonschema` がこの環境のPythonに入っていないため、公式 `validate.py` は実行できない。同等の構造検査で代用している。
- 作業可能時間は未設定（[CHANNEL_STRATEGY_20261124.md](CHANNEL_STRATEGY_20261124.md)）。ここに書いた工数は既存記録の目安で、実測ではない。
