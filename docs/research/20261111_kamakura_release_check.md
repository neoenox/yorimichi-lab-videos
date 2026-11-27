# kamakura_seiritsu 公開前チェック（2026-11-16 17:00 公開予約分）

- 実施日: 2026-11-11（日本時間）
- 対象: Shorts「鎌倉幕府は1192年じゃないの？」（台帳キー `short_solo_kamakura_seiritsu` / video id `bi8n0NrsQAo`）
- 根拠にした commit: `9b39233`（非公開アップと公開予約の記録）
- 実施者: release-checker（共有タスク task-1）
- 制約: **YouTube 側の状態は一切変更していない**（アップロード・公開設定・予約の変更なし）。描画・エンコード・git commit/push もしていない。
- Windows / PowerShell / `python`（このリポジトリの `.venv`）。日本語の文字化け対策として、全文を通して次の2つを先に実行している。

```powershell
$env:PYTHONUTF8=1
chcp 65001
[Console]::OutputEncoding=[Text.Encoding]::UTF8
```

## 0. 結論（先に要点）

| 項目 | 結果 |
| --- | --- |
| 形式検査（`validate.py`） | **PASS** |
| リポジトリ追加検査（`shorts_standard.py check`） | **ERROR 0件 / WARN 7件**（終了コード 0） |
| `brief.yaml` の必須項目検査 | **指摘なし**（終了コード 0） |
| 標準ゲート上の公開可否 | **公開可ではない**。`status` は `needs_review`、`needs_research` が4件残っており、標準のルールでは `ready` にできない。したがって `to-spec` は通らない（**拒否されるのが正しい動作**） |
| 実際の運用 | オーナー判断（`docs/SHORTS_PRODUCTION_NOTES.md` の「オーナー判断（2026-11-11）」）で内容が承認され、**非公開アップロード＋2026-11-16 17:00 の公開予約が済んでいる**。標準ルールは緩められていない（`shorts-standard/` と `scripts/shorts_standard.py` の固定値は未変更。後述の `unittest` で確認） |
| YouTube 側の実状態 | **未確認**（API・ブラウザ操作をしていないため。ローカル記録のみ確認） |

**要対応トップ3**（詳細は §5）

1. YouTube の「AIの使用」が「はい」になっているかが未確認（API の読み戻しでは `None`。Studio での目視が必要）。
2. 概要欄の**全文**がローカルの最終稿と一致しているか未確認（記録では先頭のみ読み戻し）。加えて最終稿 `upload/short_solo_kamakura_seiritsu/description.txt` は `upload/` が `.gitignore` 対象のため版管理されていない。
3. `FreeVideo(MiniMax H3)` の利用条件（商用利用・公開可否）が `docs/HONNOJI_RIGHTS_LEDGER.md` に未記載。あわせて、確認した実フレームには**画面内の AI 生成明示が見当たらない**（概要欄には明記あり）。

## 1. 対象ファイル（ローカル成果物）

| パス | 役割 |
| --- | --- |
| `shorts/kamakura_seiritsu/brief.yaml` | 題材・出典URL・確認済み事実・留保 |
| `shorts/kamakura_seiritsu/result.json` | 制作標準 v1.1 の納品 JSON（`status: needs_review`） |
| `shorts/kamakura_seiritsu/proto_spec.json` | 試作用 spec（FreeVideo 背景版。**作業ツリーで未コミット変更あり**） |
| `shorts/kamakura_seiritsu/pron.json` | 読み（VOICEVOX 用） |
| `data/short_proto_fv_kamakura_seiritsu.json` | 実際に描画へ渡した spec（FV=FreeVideo 背景版） |
| `out/short_proto_fv_kamakura_seiritsu.mp4` | 描画済み動画（アップロード元） |
| `out/short_proto_fv_kamakura_seiritsu_subtitles.srt` | 字幕（アップロード元） |
| `upload/short_solo_kamakura_seiritsu/{video.mp4,subtitles_ja.srt,title.txt,description.txt,tags.txt}` | 投稿パック（`upload/` は `.gitignore` 対象） |
| `data/youtube_ids.json` | 台帳（`video_id`・`privacy`・`publishAt`） |

## 2. 確認済み

### 2.1 検査コマンドの結果（実行したもの）

```powershell
$env:PYTHONUTF8=1
python scripts/shorts_standard.py check shorts/kamakura_seiritsu/result.json
```

出力（全文）:

```
meta: shorts/kamakura_seiritsu/result.json (validate.py PASS)
WARN  claim c_shosetsu: AI アシスタントの回答を根拠にしている（一次資料での裏取りは未実施）
WARN  claim c_1185: AI アシスタントの回答を根拠にしている（一次資料での裏取りは未実施）
WARN  claim c_1192: AI アシスタントの回答を根拠にしている（一次資料での裏取りは未実施）
WARN  claim c_textbook: AI アシスタントの回答を根拠にしている（一次資料での裏取りは未実施）
WARN  claim c_stage: AI アシスタントの回答を根拠にしている（一次資料での裏取りは未実施）
WARN  Scene 1: claim_ids が空（事実を述べる場面なら根拠IDを付ける）
WARN  形式検査は PASS でも、出典の原文照合・読み・スマホ可読性は人が確認する
```

終了コード: `0`（ERROR 0件）。

```powershell
python shorts-standard/validate.py shorts/kamakura_seiritsu/result.json
```

```
PASS: structural checks only. Human fact/audio/visual review still required.
```

終了コード: `0`。

```powershell
python scripts/shorts_standard.py brief-check shorts/kamakura_seiritsu/brief.yaml
```

出力なし（指摘 0 件）、終了コード: `0`。
※ この点は `docs/SHORTS_PRODUCTION_NOTES.md`（実測メモ）の「`PYTHONUTF8=1` を付けないと brief-check は何も表示せず終了コードのみになる」という注意に従い、`PYTHONUTF8=1` を設定したうえで実行した。

```powershell
python scripts/shorts_standard.py list
```

```
edo_map_date                 ready         36.0s  7 scenes  needs_research=0
kamakura_seiritsu            needs_review  40.0s  7 scenes  needs_research=4
sample_edo_map_compare       needs_review  36.0s  7 scenes  needs_research=2
shodo_heritage               ready         36.0s  7 scenes  needs_research=0
```

### 2.2 標準ルールが緩められていないことの確認（CI と同じテスト）

```powershell
python -m unittest discover -s tests -p "test_shorts_standard.py"
```

```
......................
----------------------------------------------------------------------
Ran 22 tests in 3.251s

OK
```

`tests/test_shorts_standard.py` は `output.schema.json` の固定値（30〜45秒、5〜7シーン、字幕2行14文字）と `scripts/shorts_standard.py` の定数を直接読み、`needs_research` が空でない JSON を `ready` にできないこと、`to-spec` が `needs_review` を拒否することを検査している。**これが通っている＝今回の作業でゲートを緩めていない**。

### 2.3 WARN の中身の確認

- **`ai_assistant` の5件**: `result.json` の5つの claim はすべて `source_type: ai_assistant`。ただし `evidence_note` の冒頭に「AIの回答ではない。○○を取得して確認」と書かれている（例: `c_shosetsu` は国立国会図書館レファレンス協同データベース、`c_1185` は朝日新聞 asahi.com）。
  - **事実**: スキーマ上 `primary` は一次資料の URL を要求するため、図書館レファレンス・報道・Wikipedia は `primary` に当たらず、`ai_assistant` を使っている。これは標準 v1.1 の枠内の使い方で、ルールの緩和ではない（WARN は「一次資料での裏取りが未実施」の表明）。
  - **推測**: この WARN は今回の公開予約にとって「新しい問題」ではなく、`needs_research` に残した未了事項と同じ内容を指している。
- **`Scene 1: claim_ids が空`**: 冒頭0〜3秒は疑問提示のみで事実を述べていないため、意図どおり（`docs/SHORTS_PRODUCTION_NOTES.md` にも同旨の記録あり）。
- **最後の WARN（人が確認する）**: 機械検査は形式のみ、という標準の注意書き。

### 2.4 `to-spec` が通るか（実行せずに仕様を読んで判断）

**`to-spec` は実行していない。** 理由: タスクの指示（ready でなければ実行しない）に従った。判断根拠は `scripts/shorts_standard.py` の `cmd_to_spec()`:

- `result.json` の `status` が `needs_review`（`shorts/kamakura_seiritsu/result.json` 5行目: `"status": "needs_review"`）。
- `cmd_to_spec()` は ERROR が無いことを確認した後、`if data.get('status') != 'ready':` で `中止: status=needs_review。出典の原文照合を終えて ready にしてから変換する` を出して終了コード 1 を返す（`scripts/shorts_standard.py` 301〜305行）。
- さらに `shorts-standard/validate.py` 40行が `needs_research` が空でない `ready` を弾く。`result.json` の `needs_research` は4件。

→ **通らない理由は「出典の原文照合が未了（`needs_research` 4件）」であり、ゲートの不具合ではない。** 描画に使った spec（`data/short_proto_fv_kamakura_seiritsu.json`）は、`scripts/make_spec_kamakura_seiritsu.py` が検査 ERROR なしを確認したうえで `S.to_spec()` を**直接**呼び、`proto_` 接頭辞の別名で出した試作用の出力（同スクリプトの docstring に明記）。

### 2.5 ファイル間の整合（タイトル・claims・出典・credit・AI生成の明示）

| 確認項目 | 結果 |
| --- | --- |
| タイトル | `result.json` / `proto_spec.json` / `data/short_proto_fv_*.json` / 概要欄1行目 / `title.txt`（`+ #Shorts`）がすべて「鎌倉幕府は1192年じゃないの？」で一致 |
| claims の ID と参照 | 7シーンのうち Scene 1 以外が `c_shosetsu` / `c_1185` / `c_1192` / `c_textbook` / `c_stage` を参照。未知 ID・重複 ID なし（`validate.py` が検査済み） |
| 出典URL | `brief.yaml` の `source_urls` 4件（NDL crd 1000197449・1000344905、朝日 2008-02-28、Wikipedia 鎌倉幕府）が、claims の `source_url` にすべて現れる |
| 数値・年号の扱い | result.json の主張は「1185年・1192年・諸説あり」で、brief の caveats（断定しない・「全国の教科書が変わった」と言わない）と矛盾しない |
| AI生成の明示（概要欄） | 投稿 `description.txt` 14行目「背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の風景・史実の再現ではありません」を確認 |
| AI生成の明示（spec） | `data/short_proto_fv_*.json` の `credit` に同じ行あり（`scripts/make_spec_kamakura_seiritsu.py` の `CREDIT_FV`） |
| credit 表記 | 概要欄に 背景映像（AI）／図・表は自作の模式図／VOICEVOX:四国めたん／魔王魂「ピアノ12（作曲：森田交一。音量調整）」を確認。`docs/HONNOJI_RIGHTS_LEDGER.md` が要求する「音楽：魔王魂＋曲名＋作曲者」の表記を満たす |
| 試作表記の除去 | `out/short_proto_fv_kamakura_seiritsu_description.md`（描画時の自動生成）は「【試作】…公開前の確認用です」を含むが、投稿用 `description.txt` からは除去され、代わりに「※ 出典の原文（『吾妻鏡』などの史料、教科書の実物）の照合は未了です。…誤りがあれば概要欄で訂正します。」が入っている（差分を `Compare-Object` で確認） |

概要欄の差分（再現コマンド）:

```powershell
Compare-Object `
  (Get-Content out/short_proto_fv_kamakura_seiritsu_description.md -Encoding UTF8) `
  (Get-Content upload/short_solo_kamakura_seiritsu/description.txt -Encoding UTF8)
```

結果（`=>` は投稿用のみ、`<=` は描画時のみ）:

```
=> ※ 出典の原文（『吾妻鏡』などの史料、教科書の実物）の照合は未了です。国立国会図書館レファレンス協同データベース、報道、Wikipedia に基づく整理です。誤りがあれば概要欄で訂正します。
<= 【試作】出典の原文照合が未了のため、この動画は公開前の確認用です。
<= 背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の風景・史実の再現ではありません。
<= ・【試作】出典の原文照合は未了です（吾妻鏡・山槐記・教科書の実物など）
```

（AI生成の明示は、投稿用では §2.5 のクレジット行に残っている。消えたのは「試作」の2行。）

### 2.6 投稿パックと描画物の同一性（ハッシュ）

```powershell
(Get-FileHash out/short_proto_fv_kamakura_seiritsu.mp4 -Algorithm SHA256).Hash
(Get-FileHash upload/short_solo_kamakura_seiritsu/video.mp4 -Algorithm SHA256).Hash
(Get-FileHash out/short_proto_fv_kamakura_seiritsu_subtitles.srt -Algorithm SHA256).Hash
(Get-FileHash upload/short_solo_kamakura_seiritsu/subtitles_ja.srt -Algorithm SHA256).Hash
```

| 対象 | SHA256 | 一致 |
| --- | --- | --- |
| `out/…mp4` | `B032BD1C103F932971AB332A9E6E641C7D3F7A35C0DB10BC17C42DDD7102DD20` | — |
| `upload/…/video.mp4` | `B032BD1C103F932971AB332A9E6E641C7D3F7A35C0DB10BC17C42DDD7102DD20` | **一致** |
| `out/…subtitles.srt` | `7AD65828851573B95DEBF805208A5298E8CF5025219CF1B19A50ABFBD6F2CC85` | — |
| `upload/…/subtitles_ja.srt` | `7AD65828851573B95DEBF805208A5298E8CF5025219CF1B19A50ABFBD6F2CC85` | **一致** |

→ 投稿パックの動画・字幕は、レビュー済みの描画物そのもの（サイズ 23,671,932 バイト）。

背景クリップの取り直しとの前後関係も確認した（`assets/kamakura_seiritsu/fv` の更新時刻）:

- `clip4.mp4`（竹林に取り直し）= 2026-11-11 19:53:56、`clip5.mp4`（水に墨）= 19:42:28
- 描画 `out/short_proto_fv_kamakura_seiritsu.mp4` = 20:00:10
- → **取り直し後のクリップで描画された動画**が投稿パックに入っている。
- `clip4.mp4.old` / `clip4_tatami.old` / `clip5.mp4.old` は取り直し前の控え（未追跡ファイル）。描画では参照されない（spec は `clip4.mp4` 等を指す）。

### 2.7 公開予約の記録（ローカル記録のみ）

```powershell
Select-String -Path data/youtube_ids.json -Pattern 'kamakura' -Context 0,6 -Encoding UTF8
```

```
"short_solo_kamakura_seiritsu": {
  "video_id": "bi8n0NrsQAo",
  "privacy": "private",
  "via": "api",
  "superseded": [],
  "deleted": [],
  "publishAt": "2026-11-16T08:00:00Z"
```

- `2026-11-16T08:00:00Z` = **2026-11-16 17:00 JST**（UTC+9）。`docs/SHORTS_PRODUCTION_NOTES.md` の「公開予約」記述と一致。
- `data/youtube_ids.json` の全エントリを走査し、**同じ公開時刻の二重予約は無い**ことを確認した。2026-11-16 に予約されているのは次の2本のみ:
  - `short_solo_skytree` = `SUfRV2YnNMY` / `2026-11-16T03:00:00Z`（12:00 JST）
  - `short_solo_kamakura_seiritsu` = `bi8n0NrsQAo` / `2026-11-16T08:00:00Z`（17:00 JST）
- `docs/SHORTS_FIRST_SCHEDULE_20261104.md` には「2026-11-16 17:00 = ooka_shirakoya」とあるが、同文書の表題は「Shorts先行の日程案（2026-11-04、**未適用**）」であり、台帳（`data/youtube_ids.json`）にその時刻の予約は無い。**矛盾ではなく、適用されなかった案**。
- 2026-11-16 19:00 の長尺（`lHNfr-MxXEs`、`docs/YOUTUBE_ACTUAL_SCHEDULE_20261103.md`）は別時刻のため衝突しない。

### 2.8 音声・映像の数値記録の相互整合（再測はしていない）

`docs/SHORTS_PRODUCTION_NOTES.md` の実測記録、説明欄、台帳を突き合わせた。

| 記録元 | 値 |
| --- | --- |
| `docs/SHORTS_PRODUCTION_NOTES.md`（試作の実測） | 1080x1920 / 30fps / 44.43秒 / h264+aac / -14.0 LUFS / ピーク -1.5 dBFS |
| 投稿説明欄 1行目 | 「（約44秒）」 |
| 台帳 `docs/SHORTS_PRODUCTION_NOTES.md` | 長さ `PT45S` |
| 字幕 SRT の最終キュー | `00:00:40,224 --> 00:00:43,470` |
| 標準の許容範囲（30〜45秒） | 44.43秒は範囲内 |

→ 相互に整合。**ただし今回 ffprobe/ffmpeg は実行していない**（描画・エンコードの再実行は禁止のため）。数値は上記記録の引用であり、私が再測した値ではない。

### 2.9 実フレームで確認したこと（描画後の見え方）

`out/proto_fv2_watch/`（2026-11-11 20:01 に生成された、20:00 描画の動画からのフレーム。11枚＋コンタクトシート）を目視した。

- 上部ヘッダ「鎌倉幕府は1192年？」、場面ごとの大きな字幕、下部の字幕パネルが表示されている。文字化け・欠けは見られない。
- 各場面に小さな出典ラベル（例: 「基準で変わる / 模式図（諸説の例）」「2012年度版から1185年から / 模式図（東京書籍・中学歴史の年表）」）が出ている。**図が「模式図」であることは画面内で明示されている。**
- 背景は AI 生成クリップ（山道・渓流・竹林・墨・灯籠・雲海）。確認したフレームに人物・現代物・読める文字は見当たらない。
- 年表図は 1180→1183→1185→1190→1192 の5項目が重ならず表示され、1185年・1192年の図も読める。
- **注意点（画面の数字）**: 1場面目の大きな数字は、フレームによって「1191年？」と表示される。`scripts/make_short2.py` 171〜175行の `count` 図は `_ease(tt/1.4)` で 0 から 1192 へカウントアップする実装なので、これは**アニメーション途中の値**であり、1.4秒以降は 1192 で止まる（実装を読んで確認）。誤植ではない。
- **画面内に AI 生成であることの明記は、確認した11フレームには見当たらない**（「模式図」ラベルのみ）。概要欄には明記がある。→ §5 の要対応に記載。

## 3. 未確認（確認していないこと）

以下は**確認していない**。事実として断定しない。

1. **YouTube 側の実状態**（`privacy`・`publishAt`・「AIの使用」設問・概要欄全文・字幕2本の状態）。API もブラウザ操作も実行していないため、根拠は `data/youtube_ids.json` と `docs/SHORTS_PRODUCTION_NOTES.md` の記録のみ。
2. **YouTube の「AIの使用（改変または合成されたコンテンツ）」が「はい」になっているか**。記録では `videos().update(part=status)` で `containsSyntheticMedia=True` を送ったが、**API の読み戻しでは `None`** が返るため、Studio での目視確認が必要と記録されている（`docs/SHORTS_PRODUCTION_NOTES.md` 391行）。
3. **概要欄の全文一致**。記録では「タイトル・タグ・概要欄の**先頭**は API で読み戻して一致を確認」とある。末尾（※行・クレジット・ハッシュタグ）の一致は未確認。
4. **投稿用ファイルが版管理されているか**。`upload/` と `out/` は `.gitignore` 対象（`git check-ignore -v` で確認: `.gitignore:51: upload/`、`.gitignore:4: out/`）。したがって、公開された概要欄の最終稿は**リポジトリに残っていない**。
5. **動画・音声の再計測**（ffprobe の実測、全編の実聴、BGM との聴感、連続再生での動き、スマホ実機表示）。§2.8 はすべて既存記録の引用。
6. **`FreeVideo(MiniMax H3)` の利用条件**（商用利用・公開可否・クレジット条件の原文）。`docs/HONNOJI_RIGHTS_LEDGER.md` に FreeVideo の行が無い。FreeVideo に触れている記述は `docs/SHORTS_PRODUCTION_NOTES.md` の手順・実測（背景映像の作り方、クレジット文）が中心で、**利用条件そのものの記録・出典URLは見当たらない**（私が `docs/` 配下を `FreeVideo` で検索した範囲）。
7. **`out/` 側に残る `short_proto_kamakura_seiritsu`（単色背景版）との関係**。投稿パックは FV 版（`short_proto_fv_`）で、単色版は使われていないことをハッシュとファイル名で確認したが、単色版の扱い（破棄してよいか）は決めていない。
8. **`proto_spec.json` の作業ツリー差分**（`git diff` で `credit` の1行のみ、単色→FreeVideo の差し替え）。未コミットのまま。公開物の再現性に影響するかは未判断。
   - 参考: 同じ作業ツリーを点検した別担当の `docs/research/20261111_worktree_review.md` は、この差分を「描画・投稿した内容に権利表記を合わせる意図的な変更」と評価している。私は同文書を読んだだけで、その評価を独立に検証してはいない。

## 4. 標準ルールを緩めていないことの明記

- `shorts/kamakura_seiritsu/result.json` の `status` は **`needs_review` のまま**（`ready` にしていない）。
- `needs_research` 4件も**削除していない**:
  1. 『吾妻鏡』『山槐記』など一次史料の原文照合
  2. 東京書籍の教科書の実物／検定済教科書データでの確認
  3. 『日本大百科全書』『世界大百科事典』『国史大辞典』の該当項目の原文確認
  4. 川合康「少なくとも3段階」の原典確認
- `shorts-standard/` の schema・validate.py・README・PROMPT は**変更していない**。`scripts/shorts_standard.py` の固定値も**変更していない**（`git status --porcelain` で modified になっているのは `scripts/_chain3.sh`・`scripts/make_short2.py`・`scripts/solo_spec.py`・`shorts/kamakura_seiritsu/proto_spec.json` の4件で、標準のゲート定義は含まれない。私はこの4件を編集していない。更新時刻はそれぞれ 2026-11-09 00:20、2026-11-11 22:35、2026-11-11 22:35、2026-11-11 19:58 で、私の作業開始（22:47）より前。**推測**: 22:35 の2件は別の作業（他の担当）による変更）。
- 緩和が必要だと判断した場合は変更せず理由を報告する、という指示に従い、**緩和は行っていない**。今回の「公開予約」は、標準の判定を `ready` に変えたのではなく、オーナー判断として `needs_review` のまま別経路（`make_spec_kamakura_seiritsu.py` → 描画 → `private` アップロード）で進めたもの。この経緯は `docs/SHORTS_PRODUCTION_NOTES.md` に記録されている。

## 5. 要対応

### 5.1 公開前（2026-11-16 17:00 まで）

| # | 要対応 | 理由・根拠 | 担当の目安 |
| --- | --- | --- | --- |
| 1 | **Studio で「詳細設定 → AI の使用」が「はい」か目視確認** | API の読み戻しが `None`。`containsSyntheticMedia` の実状態がローカルから確認できない（§3-2） | 人（Studio 操作） |
| 2 | **Studio で概要欄の全文（※行・クレジット・ハッシュタグまで）を目視確認** | 記録は「先頭のみ一致確認」。ローカルの最終稿と一致している保証が無い（§3-3, §3-4） | 人（Studio 操作） |
| 3 | **公開された最終稿（タイトル・概要欄・タグ）を git 管理下に記録** | `upload/` は `.gitignore` 対象。現状、公開文面を再現できるのはローカルファイルのみ（§3-4） | エージェント可（`docs/` へ転記） |
| 4 | **`FreeVideo(MiniMax H3)` の利用条件を権利台帳に追記** | `docs/HONNOJI_RIGHTS_LEDGER.md` に該当行が無い。AI 生成映像を公開物に使っているのに、条件の記録が無い（§3-6） | 人（条件の確認）＋エージェント（転記） |
| 5 | **画面内の AI 生成明示をどうするか決める**（追記する／概要欄のみで可とする） | 確認した11フレームに画面内の AI 明示が無い。標準 README は「AI画像は…必要に応じ『イメージ』と明記」。`docs/SHORTS_PRODUCTION_NOTES.md` 326行の「画面に…AI 生成の明記を残している」は、少なくとも画面内の明記としては裏付けられない | 人（判断） |
| 6 | 予約日時・公開状態の最終確認（`17:00 JST` / `private` のまま予約待ち） | 台帳と docs は一致（§2.7）だが、YouTube 側の実値は未確認 | 人（Studio / API 読み取り） |

### 5.2 公開後

1. oEmbed で公開を確認する（`https://www.youtube.com/oembed?url=…&format=json`）。記録では**非公開なら 403、公開なら 200**（`docs/SHORTS_PRODUCTION_NOTES.md` 257行）。→ 公開直後に 200 になることを確認。
2. 魔王魂 BGM の **Content ID の誤検出**を監視（`docs/HONNOJI_RIGHTS_LEDGER.md` 63行が「公開後に注意」としている）。
3. スマートフォンの小さい表示でサムネイル・字幕・テロップの可読性を確認（`docs/PREPUBLICATION_SOURCE_CHECKLIST.md` 47行の共通項目）。
4. 概要欄のリンク（`https://maou.audio/`）が「動画認証」の状態でクリック可能かを確認（`docs/YOUTUBE_UPLOAD_PROCEDURE.md` §3 に、認証完了まで外部リンクが押せない注意の記載）。
5. `needs_research` の4件は**公開後も未了のまま**。原典（『吾妻鏡』『山槐記』、教科書の実物、事典、川合論文）を確認できたら、`result.json` の `needs_research` を減らし、必要なら `status` を `ready` にする。誤りが見つかった場合は概要欄で訂正する（概要欄にそう書いてある）。
6. `data/youtube_ids.json` と `docs/SHORTS_PRODUCTION_NOTES.md` に公開結果（公開時刻、初日の状態）を追記する。

## 6. 参考: 実行したコマンド一覧（再現用）

```powershell
$env:PYTHONUTF8=1
chcp 65001
[Console]::OutputEncoding=[Text.Encoding]::UTF8

# 1) 形式検査＋追加検査
python scripts/shorts_standard.py check shorts/kamakura_seiritsu/result.json
python shorts-standard/validate.py shorts/kamakura_seiritsu/result.json

# 2) brief の必須項目
python scripts/shorts_standard.py brief-check shorts/kamakura_seiritsu/brief.yaml

# 3) 一覧（status の確認）
python scripts/shorts_standard.py list

# 4) 標準ルールの非緩和（CI と同じ）
python -m unittest discover -s tests -p "test_shorts_standard.py"

# 5) 投稿パックの同一性
(Get-FileHash out/short_proto_fv_kamakura_seiritsu.mp4 -Algorithm SHA256).Hash
(Get-FileHash upload/short_solo_kamakura_seiritsu/video.mp4 -Algorithm SHA256).Hash
(Get-FileHash out/short_proto_fv_kamakura_seiritsu_subtitles.srt -Algorithm SHA256).Hash
(Get-FileHash upload/short_solo_kamakura_seiritsu/subtitles_ja.srt -Algorithm SHA256).Hash

# 6) 概要欄の差分
Compare-Object `
  (Get-Content out/short_proto_fv_kamakura_seiritsu_description.md -Encoding UTF8) `
  (Get-Content upload/short_solo_kamakura_seiritsu/description.txt -Encoding UTF8)

# 7) 台帳・予約の確認
Select-String -Path data/youtube_ids.json -Pattern 'kamakura' -Context 0,6 -Encoding UTF8
select-string -Path data/youtube_ids.json -Pattern '2026-11-1[5-7]' -Encoding UTF8

# 8) 背景クリップの更新時刻（取り直し後の描画か）
Get-ChildItem assets/kamakura_seiritsu/fv -Force | Sort-Object LastWriteTime |
  Select-Object Length,LastWriteTime,Name

# 9) 版管理の有無
git check-ignore -v upload/short_solo_kamakura_seiritsu/description.txt
git check-ignore -v out/short_proto_fv_kamakura_seiritsu_description.md
git ls-files | Select-String -Pattern 'kamakura'

# 10) 公開物の spec と git の差分
git diff -- shorts/kamakura_seiritsu/proto_spec.json
```

実行**していない**もの（意図的）: `python scripts/shorts_standard.py to-spec …`（status が `needs_review` のため。§2.4）、`ffmpeg`/`ffprobe`、`make_short2.py`、YouTube API の呼び出し、`scripts/check_publish.py`（`--check` は API を叩くため。また `data/publish_snapshot.json` は 2026-10-21 のスナップショットで、kamakura を含まない）。
