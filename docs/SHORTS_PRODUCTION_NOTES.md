# Shorts 制作のノウハウ（実測ベース）

更新日: 2026-11-04。**制作で分かったことは、その都度この文書か `docs/SHORTS_STANDARD_INTEGRATION.md` に追記してコミットする**（AGENTS.md のルール）。推測ではなく、実際に描画・確認して分かったことだけを書く。

## 1. 資料画像（実物）を背景に使う

模式図だけだと説明が続いて退屈になる。**PDM の実資料**を使うと一気に強くなる。今回は国立国会図書館デジタルコレクションの「武州豊嶋郡江戸〔庄〕図」を使った。

### 取得（IIIF）

```python
url = 'https://dl.ndl.go.jp/api/iiif/1286168/R0000001/full/1600,/0/default.jpg'
```

- マニフェスト: `https://dl.ndl.go.jp/api/iiif/<PID>/manifest.json`（`metadata` に出版年・`Access Restrictions`、`description` に解説文がある）
- 画像: `https://dl.ndl.go.jp/api/iiif/<PID>/R0000001/full/<幅>,/0/default.jpg`
- PDM の資料は再利用可。**画面と概要欄の両方に出典を書く**（`https://dl.ndl.go.jp/pid/<PID>`）

### そのまま貼ってはいけないもの

デジタル化画像には**上部のカラーチャートと下部の物差し**が写り込む。切り取る（今回の比率）:

| 用途 | 切り出し（元画像比 x0,y0,x1,y1） |
| --- | --- |
| 全体 | `0.070, 0.082, 0.978, 0.872` |
| やや引き（変化をつける） | `0.115, 0.120, 0.940, 0.815` |
| 詞書（文字ブロック） | `0.058, 0.585, 0.372, 0.870` |
| 屋敷名が並ぶ領域 | `0.415, 0.300, 0.720, 0.610` |

- **横長の帯を cover で貼ると、中央だけが異常に拡大される**（題額の帯で実際に失敗）。帯を見せたいときは幅に合わせて上下に余白を置く（`contain`）。
- 資料の上に文字を載せるので、明度は 0.72〜0.75 に落とす。落としすぎると資料の価値が消える。
- 最低限「資料：国立国会図書館デジタルコレクション（PDM）」「原図の一部を暗く加工」「史実の再現図ではない」を画面に出す。

## 2. 画面の安全領域（1080x1920、`make_short2.py` 実測）

| 要素 | 位置（px） | 注意 |
| --- | --- | --- |
| タイトル | y=200、1行・58px | **全角18文字を超えると左右が切れる**。13文字前後が安全 |
| 大テロップ（`big`） | y=520 中心、92px | 1行14文字以内。長いと自動で縮むが、2行になると下とぶつかる |
| データ帯（`sub`） | y=800〜960 | 任意 |
| 字幕（ナレーション） | y≈1470〜1540、右下がり | 3行までなら収まる |
| 画面下の注記 | y≈1556 以降 | ここと字幕パネルは重なるので、注記は 1556 より下に置く |

背景画像（1080x1920）を作るときは、**y=500〜1470 を資料の見せ場**、**y<460 と y>1550 を注記**に使う。

## 3. シーンごとに背景を変える（`art_map.json`）

`shorts/<slug>/art_map.json` に**シーン数と同じ長さの配列**で画像パスを書くと、`to-spec` がシーン別に割り当てる（無ければ `--art` の1枚）。

```json
["assets/<slug>/bg_full.png", "assets/<slug>/bg_text.png", "..."]
```

- 同じ背景が続くと単調。**全体 → 部分拡大（詞書・屋敷名）→ 全体へ戻す**の順で変化をつけると飽きない。
- Ken Burns（ゆっくり拡大）が各シーンに付くので、静止画でも動いて見える。
- 端に置いた小さなラベルは拡大で切れる。**チップは作らず、上部の注記行に「／部分拡大：詞書」と書く**。

## 4. レンダラ（`scripts/make_short2.py`）の前提

| 挙動 | 内容 |
| --- | --- |
| 尺 | 音声の長さで決まる。設計値を書いても実測が優先（今回は設計36秒 → 実測32.17秒） |
| BGM | 既定で `assets/bgm_maou/maou_bgm_piano12.mp3` を重ね、-14 LUFS に揃える。`bgm: 'none'` で無し |
| CTA | 既定で末尾に登録誘導を足す。制作標準では `cta: false` を出力（無意味な誘導は禁止） |
| `long_id` | 対応する長尺が無い単独Shortsでは案内行を出さない（2026-11-04 修正） |
| クレジット | 素材の実態に合わせる。`to-spec --credit` で指定（既定文言は「ChatGPT生成イラスト」なので注意） |

## 5. 検証の手順（描画後）

```bash
export PATH="/e/rekishikaisetu/tools/ffmpeg/bin:$PATH"   # Windows は PATH に ffmpeg\bin を追加

ffprobe -v error -show_entries format=duration,size \
  -show_entries stream=codec_name,width,height,r_frame_rate -of default=noprint_wrappers=1 out/short_<slug>.mp4
ffmpeg -v error -i out/short_<slug>.mp4 -f null -                       # 全編デコード（無音でエラー無し）
ffmpeg -hide_banner -i out/short_<slug>.mp4 -af loudnorm=print_format=json -f null -   # -14 LUFS / TP -1.5 を確認
ffmpeg -ss 16 -i out/short_<slug>.mp4 -frames:v 1 -vf scale=540:-1 /tmp/f.png           # 代表フレームを目視
```

- **代表フレームの目視で終わりにしない。** 全編の聴取・スマホ実機・出典の原文照合は別のゲート。
- 確認した範囲と未確認の範囲を分けて報告する（`docs/VIDEO_CREATION_PRECHECK.md`）。

## 6. 投稿（アップロード）で分かったこと

- 単独Shortsは長尺パックが無い。`pack_short.py <slug> --tags=江戸,地図,歴史` で投稿パックを作る（2026-11-04 追加。長尺パックを渡す従来の使い方も可）
- `yt_api.py upload <pack>` は**常に private**。公開は人が Studio で行う（`yt_api.py schedule <ID> "<JST>"` で予約公開も可）
- アップロードの順序は **動画 → 台帳記録 → サムネ → 字幕**。字幕で失敗しても、動画と台帳は残る
  - 実例（2026-11-04）: 動画 `m-2eoljbdLA` は private で成功、字幕だけ `quotaExceeded` で失敗
- `captions.insert` は約 400 units。1日の割り当て（10,000 units）を他の作業で使うと字幕で止まる
- 字幕だけ後で入れる手順は [`VIDEO_PRODUCTION_RUNBOOK.md`](VIDEO_PRODUCTION_RUNBOOK.md) の「YouTube API の割り当てが切れた日の字幕」に従う（Studio の `translations` から手動アップロード → 公開）
- アップロード後は `data/youtube_ids.json` に記録される。二重投稿しないため、次の制作前にこの台帳を見る

### 字幕だけを Studio で入れる（APIクォータ切れ時・2026-11-04 実測）

ログイン済みの Chrome を bsk（browser-skill）で操作する。座標クリックではなく VOM の ref（`@eNN`）で進める。

```bash
bsk session start --browser <instance-id> --name studio --width 1600 --height 1000 --focus
bsk step --session studio --action navigate --json \
  --params '{"url":"https://studio.youtube.com/video/<VIDEO_ID>/translations"}'
bsk cooperate --session studio sync --json          # context_id を取得（以降 --context に渡す）
bsk step --session studio --context <ctx> --action click --params '{"ref":"@e22"}'   # 手動でアップロード
bsk upload '@e27' --file '<SRTの絶対パス>' --session studio --context <ctx>          # 続行→ファイル選択を横取り
bsk step --session studio --context <ctx> --action click --params '{"ref":"@e21"}'   # 字幕を編集
bsk step --session studio --context <ctx> --action click --params '{"ref":"@e30"}'   # 公開
bsk session stop studio
```

- `@eNN` は**同期のたびに変わる**。操作の前に必ず `bsk cooperate sync` で読み直す（古い ref は `target_hidden` で失敗する）
- 「続行」を素で押すと **OS のファイル選択ダイアログ**が開く。`bsk upload` の対象に「続行」を指定すると横取りできる
- 完了の合図は「日本語の字幕を公開しました」。公開後に「公開」「ドラフトを保存」が disabled になるのが正常
- **字幕の公開 ≠ 動画の公開**。動画は private のまま（確認は `scripts/yt_api.py list`）
- 失敗したら操作を繰り返さず、まず `bsk cooperate sync` で画面の実際の状態を見る

### 公開予約とクォータの残量（2026-11-04 実測）

```bash
python scripts/yt_api.py schedule <VIDEO_ID> "2026-11-05 20:00"   # 日本時間で指定
# -> 公開予約(日本時間): 2026-11-05 20:00 -> 2026-11-05T11:00:00Z
```

- 予約後も `status.privacyStatus` は `private` のまま。`status.publishAt` に UTC が入る（API で確認できる）
- **クォータは「残量」で落ち方が変わる**。同じ日に `captions.insert`（約400 units）が `quotaExceeded` で失敗しても、`videos.update`（約50 units）は通った。単価の高い操作から先に落ちる
- 予約の変更も同じコマンド（新しい日時を渡す）。取り消して非公開のままにするときは、日時を未来のまま放置せず Studio で予約を取り消す



## 7. 今回ハマったこと（再発防止）


| 症状 | 原因 | 対処 |
| --- | --- | --- |
| タイトルが左右で切れる | 1行固定・折り返し無し | タイトルを13文字に短縮 |
| `KeyError: 'long_id'` で概要欄が作れない | 単独Shortsに長尺リンクが無い | `long_id` 任意化 |
| 概要欄が「ChatGPT生成イラスト」になる | 既定クレジット | `--credit` で実素材を明記 |
| 背景の注記が画面外 | 下端すぎる | 資料ラベルは 1556 以降、資料は 500〜1470 |
| 色票・物差しが写る | デジタル化画像の仕様 | 切り出し比率で除外 |
| 横長の帯が異常拡大 | cover の拡大率 | `contain`（幅合わせ）で表示 |
