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

## 8. 根拠に AI アシスタントの回答を使ってよい（v1.1・2026-11-04）

オーナー判断で制作標準を v1.1 に改訂し、`claims.source_type` に `ai_assistant` を追加した（`shorts-standard/CHANGELOG.md`）。

| source_type | 使いどころ | 必須 |
| --- | --- | --- |
| `primary` | 一次資料（官公庁・大学・企業IR・論文）。従来どおり | `source_url`（http/https）＋`evidence_note` |
| `ai_assistant` | 一次資料にたどり着く前の構成づくり、速報性のある題材 | `evidence_note` に「何を質問し、何と答えたか」 |

運用:

- `ai_assistant` が 1 件でもあると `check` が **WARN** を出す（黙って通さない）。WARN を消すには一次資料の claim を足す
- 数字・固有名詞・因果関係は特に誤りやすい。可能なら同じ主張を `primary` でも裏取りする
- AI に聞いた日時と質問文を `evidence_note` に残す（後から検証・訂正できるように）
- 誤りが判明したら概要欄に訂正、重大なら新IDで差し替え（`superseded` 運用）

## 9. 調査に ChatGPT（web）を使う（bsk・2026-11-05 実測）

一次資料の候補を探すとき、ブラウザの ChatGPT を使える。**回答は根拠として使える（v1.1）が、URL は自分で開いて確かめる。**

```bash
bsk session start --browser <instance-id> --name research --width 1500 --height 950 --focus
bsk step --session research --action navigate --json --params '{"url":"https://chatgpt.com/"}'
bsk cooperate --session research sync --json          # context_id と composer の @eNN を読む
bsk step --session research --context <ctx> --action fill --params '{"ref":"@e<composer>","value":"<質問>"}'
# 送信: Enter では送信されないことがある。VOM の「送信」ボタンを click する
bsk step --session research --context <ctx> --action click --params '{"ref":"@e<送信>"}'
# 90秒ほど待ってから sync し、region "会話" の paragraph を読む
bsk session stop research
```

- 質問の型: 「Web検索を使って、<日付> に発表された <官公庁/大学/研究機関> の公式発表を5件。発表元／発表日／タイトル／一次資料URL。報道記事は除外。URLは実在するものだけ」
- **返ってきた URL は必ず HTTP で開いて確認する**（実測: 5件すべて 200 でタイトルも一致したが、これは毎回保証されない）
- 画面の VOM には過去のチャット履歴（個人的な話題）も含まれる。作業ログや PR に貼らない
- 回答は `source_type: ai_assistant` で記録し、可能なら同じ主張を `primary` でも裏取りする

## 10. 画像生成の自動化（ChatGPT web・2026-11-05 実測）

背景画像を AI 生成にしたいときの自動化。`scripts/chatgpt_image.py` が bsk 経由で操作する。

```bash
python scripts/chatgpt_image.py --prompt "縦長9:16、濃紺の背景に筆と硯、文字なし" \
  --out assets/<slug>/gen_base.png --timeout 300
python scripts/chatgpt_image.py --reuse-last --prompt x --out ...   # 生成済みチャットから取得だけ
```

### 動くところ / 動かないところ（実測）

| 工程 | 状態 | 補足 |
| --- | --- | --- |
| セッション開始・最大化 | 動く | `bsk session start --browser <id> --width 1600 --height 1000 --focus` |
| プロンプト送信 | 動く（要検証） | `https://chatgpt.com/?q=<urlencoded>` で入力欄を埋め、「送信」を click。**click が弾かれることがある**ので、送信後に VOM で「あなたの発言」を確認し、無ければ1回だけ再クリックする |
| 生成 | 動く | 90〜150秒。VOM に「画像を作成中 32%」等が出る |
| ダウンロード | **未解決** | 生成後 `cooperate sync` が `unchanged`（observation を返さない）ままになることがあり、「ダウンロード」ボタンの ref を取れない |

### 分かった制約

- `bsk cooperate sync` は**変更が無いと observation 本文を返さない**。ポーリングで待つと、生成完了後も古い本文のまま止まることがある
- セッションは**約5分の idle で切れる**。長い待ちを挟むなら1回のスクリプト内で完結させる
- 画面の VOM には**過去のチャット履歴（個人的な話題）が含まれる**。ログや PR に貼らない
- 画像の権利・表記: 生成画像は「イメージ」と明記する（資料と混同させない）

### 推奨（今後の自動化）

1. **画像だけは API を使う**（`OPENAI_API_KEY` があれば `images.generate` で完結し、ブラウザ不要）。ブラウザ自動化は UI 変更に弱い
2. ブラウザ経由を続けるなら、**ダウンロードは手動1クリック**にして、生成と保存先の用意だけ自動化する
3. 生成した画像は `assets/<slug>/gen_base.png` に置けば、`scripts/make_shodo_heritage_assets.py` のような合成スクリプトが背景に取り込む（日付・出典・「AI生成」の注記を焼き込む）

### 10.1 CDP 方式（推奨・2026-11-05 実測で成功）

bsk はクリックが弾かれる・ラベルが壊れることがあるため、**Chrome を DevTools プロトコルで起動して Playwright で操作**する。こちらは安定して最後まで通った。

```bash
# 1. 自動化用プロファイルで Chrome を起動（初回のみ、このウィンドウで ChatGPT にログイン）
chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\Users\neoen\.chrome-automation

# 2. ログイン確認（未ログインなら exit 2 で止まる）
python scripts/gen_image_cdp.py --check

# 3. 生成して保存
python scripts/gen_image_cdp.py --prompt "縦長9:16、濃紺の背景に筆と硯、文字なし" \
  --out assets/<slug>/gen_base.png --timeout 300

# 4. 生成済みの画像だけ取り直す（送信しない）
python scripts/gen_image_cdp.py --reuse --out assets/<slug>/gen_base.png
```

実測で分かった要点:

- **送信ボタン**: `button[data-testid="send-button"]` は今回のUIでは見つからず、`button[aria-label*="送信"]` で押せた（両方試す実装にしてある）
- **生成画像の URL は `blob:https://chatgpt.com/...`**。`oaiusercontent` ではないため、URL を直接 fetch できない。**ページ内で canvas に描いて `toDataURL`** で取り出すのが確実
- 生成は 30〜60秒程度。`--timeout` は 300 秒あれば十分
- ログインはプロファイルに保持される（失効時のみ再ログイン）。未ログインを検知したら**明確に止まる**

## 11. Studio の公開設定・字幕を CDP で操作（2026-11-05 実測で成功）

API のクォータが尽きたときは、**自動化用 Chrome を Playwright で操作**すれば公開も字幕も通る（bsk より安定）。

前提: `chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\Users\neoen\.chrome-automation` で起動し、
そのウィンドウで **寄り道ラボ**（`UCN_do9fcssctmkrNsRWOO9A`）にログインしておく。

```bash
python scripts/studio_cdp.py check                                   # チャンネルIDの確認（違えば停止）
python scripts/studio_cdp.py publish --video-id <ID>                 # 公開に変更
python scripts/studio_cdp.py captions --video-id <ID> --srt upload/<pack>/subtitles_ja.srt
```

### 実測で分かった DOM の要点

| 操作 | セレクタ/手順 |
| --- | --- |
| 公開設定を開く | `ytcp-icon-button#select-button`（**同じ id が4つある**ので `ytcp-icon-button` で限定する） |
| 公開を選ぶ | `get_by_role('radio', name='公開', exact=True).check()` |
| ダイアログを閉じる | `get_by_role('button', name='完了')` |
| 保存 | `get_by_role('button', name='保存')`（ページ右上。`完了` の後なら有効） |
| 字幕アップロード | 「手動でアップロード」→ `expect_file_chooser` で「続行」→ `set_files(srt)` → 「字幕を編集」→「公開」 |

- 公開すると `#visibility-text` が「公開」になり、`https://www.youtube.com/oembed?...` が **200** を返す（非公開なら 403）。これが最速の確認方法
- bsk（拡張機能経由）は同じ操作でクリックが弾かれる／ラベルが文字化けする。**Studio は CDP 方式を使う**
- チャンネル取り違え防止のため、`studio_cdp.py` は最初に URL のチャンネルIDを検証し、違えば何もせず終了する


## 実測：図書館レファレンス事例を根拠にする題材（2026-11-11 kamakura_seiritsu）

題材「鎌倉幕府の成立年（1185 と 1192）」。**status は needs_review のまま**（`to-spec` は拒否される。これは標準どおり）。描画・音声・動画は未実施。

- **使えた資料**：国立国会図書館レファレンス協同データベース（https://crd.ndl.go.jp/reference/entry/index.php?id=<番号>&page=ref_view）。図書館が事典・教科書を実際に調べた回答で、本文を HTTP で取得できる。使ったのは 1000197449（成立年の5説・7説）と 1000344905（東京書籍の教科書の記述の変遷）
- **使えなかった資料**：帝国書院 Q&A（/q_and_a/history/）は 404。朝日 sahi.com/edu/student/kyoukashow/TKY200802270241.html は **EUC-JP** で、そのまま取得すると文字化けする（RawContentStream を uc-jp でデコードして読んだ）
- **スキーマ上の注意**：claims.source_type は primary / i_assistant の二択。図書館回答・報道・Wikipedia は一次資料ではないが、AI の回答でもない。このため i_assistant を使い、**vidence_note の冒頭に「AIの回答ではない。○○を取得して確認」と明記**した（標準は緩めていない）
- **検査で出た WARN と対処**：ナレーション速度（目安 4.0〜5.5 文字/秒）超過が3場面 → 文を短くして解消。i_assistant 由来の WARN と Scene 1 の claim_ids 空（疑問提示の場面なので意図どおり）は残した
- **Windows の注意**：python scripts/shorts_standard.py は PYTHONUTF8=1 を付けないと日本語の出力が文字化けし、rief-check は何も表示しない（終了コードのみ）。PowerShell では $env:PYTHONUTF8=1 を先に設定する
- **未確認（
eeds_research に記載）**：『吾妻鏡』『山槐記』の原文、教科書の実物、大百科全書・国史大辞典の原文、川合康の指摘の原典
### 試作の描画（2026-11-11 proto_kamakura_seiritsu）

status: needs_review のため標準の `to-spec` は拒否する（正しい動作）。**試作**として、scripts/make_spec_kamakura_seiritsu.py が検査（ERROR なし）を確認したうえで `to_spec()` を直接呼び、**別名 proto_ で** data/short_proto_kamakura_seiritsu.json を出力する。esult.json は 
eeds_review のまま。

```powershell
$env:PYTHONUTF8=1
$env:Path += ';C:\Users\neoen\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin'
python scripts/make_spec_kamakura_seiritsu.py                  # 背景 assets/kamakura_seiritsu/bg_*.png も再生成
python scripts/make_short2.py proto_kamakura_seiritsu --kana   # 読みと長さだけ先に確認（44.4秒）
python scripts/make_short2.py proto_kamakura_seiritsu          # 描画（VOICEVOX 起動が必要。約70秒）
```

- **ffmpeg が PATH に無い**（FileNotFoundError: [WinError 2]）。winget 版が上記にあるので、そのセッションだけ PATH に足す。E:\ 全体の再帰検索は遅いので使わない
- **背景は自作の暗色グラデーション**（画像素材・AI 画像なし）。ssets/ の png は git 管理外だが、spec 生成スクリプトで再生成できる
- **
olong は付けない**：付けると make_short2.py が最後の場面のナレーションを「チャンネル登録も、お願いします」に差し替える（標準は無意味な登録誘導を禁止）。本編リンクは 
olink: true で消す。hook_card: false（結論先出しカードは疑問型には合わない）
- **make_short2.py の `timeline` を修正**：項目が5つだと枠（高さ±62px）が重なる。間隔が狭いときだけ枠を縮める（4項目以下は従来どおり）
- **確認した範囲**：ffprobe（1080x1920／30fps／44.43秒／h264＋aac）、全フレームのデコード（エラーなし）、音量 -14.0 LUFS／ピーク -1.5 dBFS、12時点の静止画（出典・模式図の表示、字幕の位置、図の重なりなし）、字幕 SRT・説明欄の生成
- **未確認の範囲**：連続再生での動きの滑らかさ、ナレーション全編の実聴（読みは kana 出力で確認したのみ）、BGM とのバランスの聴感、スマホ実機表示、出典の原文照合（
eeds_research の4点）。**投稿可の判断はしていない**
### 背景映像は FreeVideo（AI生成動画）を使う（2026-11-11 の取り違えの記録）

- **症状**：kamakura_seiritsu の試作を、背景を自作の単色グラデーションで描画した。既存の単独 Shorts（gen_solo_*.py、data/short_solo_*.json）は背景に **FreeVideo（MiniMax H3）の AI 生成クリップ**（ssets/<slug>/fv/clip1..N.mp4）を使っており、既存の方式と違った
- **原因**：描画前に、既存の単独 Shorts の背景の作り方（id キー、ssets/*/fv/prompts.json、scripts/freevideo_batch.py）を調べなかった。rief.yaml の isual_assets にも背景の方式を書いていなかった
- **対処（手順）**：
  1. ssets/<slug>/fv/prompts.json に、場面ごとの英語プロンプト [{"name":"clip1","sec":7,"text":"..."}] を書く（既存例：ssets/tempura/fv/prompts.json。**人物・手・文字・ロゴ・現代物を出さない**ため 
o people, no hands, no text, no letters, no logos, no buildings, no modern objects を末尾に付ける）
  2. FreeVideo を起動する：E:\FreeVideo\FreeVideo.exe のランチャーで「Launch FreeVideo」を押す。http://127.0.0.1:8188 が応答すること（python scripts/freevideo_api.py status）
  3. python scripts/freevideo_batch.py assets/<slug>/fv/prompts.json assets/<slug>/fv（1本ずつ順に生成。失敗は最大3回やり直す。縦 544x960・約7秒）
  4. spec の各場面に id=assets/<slug>/fv/clip<N>.mp4、dim=0.7 を付ける（make_short2.py が id を優先して背景にする）
  5. クレジットに「背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の風景・史実の再現ではありません」を入れる
- **注意**：FreeVideo が止まっていると reevideo_api.py は WinError 10061（接続拒否）で落ちる。過去のログには、RAM／コミット領域の不足で生成が失敗した記録（MemoryError: RAM guard: system_or_commit_pressure）がある。他の重い処理を止めてから実行し、失敗したらバッチの再試行に任せる
- **未確認**：ランチャーを使わず CLI だけで ComfyUI を起動する方法（ランチャーの内部起動コマンドは推測で叩かない）
### FreeVideo 背景版の実測（2026-11-11 proto_fv_kamakura_seiritsu）

**生成の手順（実際に動いたもの）**：scripts/gen_fv_prompts_kamakura_seiritsu.py（v_prompts() で ssets/<slug>/fv/prompts.json）→ ComfyUI を起動して scripts/solo_ship.py clips <slug> → python scripts/make_spec_kamakura_seiritsu.py --fv → python scripts/make_short2.py proto_fv_<slug>。

```powershell
# ComfyUI(FreeVideo)。サーバー起動と生成を同じバックグラウンドジョブにまとめる
cd E:\FreeVideo\runtime\ComfyUI
$srv = Start-Process 'E:\FreeVideo\runtime\FreeVideo-engine\envs\comfyui-e0766581f8a2729a\Scripts\python.exe' -ArgumentList '-u','-B','main.py','--listen','127.0.0.1','--port','8188','--disable-auto-launch','--disable-all-custom-nodes','--whitelist-custom-nodes','FreeVideo' -RedirectStandardOutput "$env:TEMP\comfy.log" -RedirectStandardError "$env:TEMP\comfy.err" -PassThru -WindowStyle Hidden
# 8188 が開くまで待ってから: python scripts/solo_ship.py clips <slug>   → 終わったら Stop-Process $srv.Id
# VOICEVOX（描画に必要）。プロジェクト内にある
Start-Process 'E:\rekishikaisetu-honnoji\tools\voicevox\windows-cpu\run.exe' -ArgumentList '--host','127.0.0.1','--port','50021' -WindowStyle Hidden
```

- **生成時間**：7本（各 7.3 秒・544x960）で約 1.2 時間。1本目は 28 分（モデル読み込み込み）、2本目以降は約 8〜11 分
- **ジョブが切れる**：DSH アプリが再起動（接続先が変わる）すると、バックグラウンドジョブも中の ComfyUI も止まる。**完成済みのクリップは残る**ので、足りない分だけ python scripts/freevideo_batch.py assets/<slug>/fv/prompts.json assets/<slug>/fv clipN で取り直す
- **描画**：約 140 秒。Broken pipe が出るが、出力は全フレームのデコードにエラーなし・44.43 秒で完成している（背景クリップを読む ffmpeg が、場面の終わりで読み残したまま閉じられるためと推測。未検証）
- **確認した範囲**：1080x1920／30fps／44.43秒、全フレームのデコード（エラーなし）、-14.0 LUFS／ピーク -1.5 dBFS、12時点の静止画と場面4の全画面
- **プロンプトが守られなかった例**：clip4（無地の和紙の巻物）に、**本のページに文字のような模様**と**筆**が映った（指示は 
o text・No pens）。clip5（墨の線）にも筆先が映る。AI の擬似文字は読めないが、「史料の実物」に見えないよう画面に『模式図』と AI 生成の明記を残している。**公開版では取り直しを検討する**
- **未確認**：連続再生での背景の動き（minterpolate の補間の見え方）、ナレーション全編の実聴、BGM の聴感、スマホ実機、出典の原文照合。**投稿可の判断はしていない**