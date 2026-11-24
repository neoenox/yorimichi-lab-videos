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

status: needs_review のため標準の `to-spec` は拒否する（正しい動作）。**試作**として、scripts/make_spec_kamakura_seiritsu.py が検査（ERROR なし）を確認したうえで `to_spec()` を直接呼び、**別名 proto_ で** data/short_proto_kamakura_seiritsu.json を出力する。
esult.json は 
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
### Muse によるレビュー（2026-11-11 proto_fv_kamakura_seiritsu）

手順は E:\rekishikaisetu\docs\SOLO_SHORT_PROCEDURE.md の第6節（このリポジトリには無い。別の作業ツリー）。**標準フロー（
esult.json）の動画でも同じ手順で送れた**。

- **送り方（実際に動いたもの）**：360p 圧縮 fmpeg -i out/short_<slug>.mp4 -vf scale=360:-2 -c:v libx264 -crf 30 -preset fast -c:a aac -b:a 64k E:\rekishikaisetu\sigcmp_view\muse_<slug>.mp4（1.2MB）→ CDP の Chrome（chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\Users\neoen\.chrome-automation https://muse.ai/）に Playwright（connect_over_cdp）で接続 → input[type=file] に set_input_files → 入力欄（[contenteditable=true]）をクリックして keyboard.insert_text（文字数と末尾を確認）→ 送信ボタンを座標クリック（約 522,871）→ ページ本文から、依頼文の末尾「問題点は時刻つきで具体的にお願いします。」の後ろを読む
- **sk は使えない**：デーモンを起動できない（Job Object ... does not allow breakaway、os error 5）。CDP 版を使う
- **ログイン**：自動操作用プロファイルは、初回だけ Muse に手でログインが必要（メール/電話の認証は代行できない）。以降は .chrome-automation に残る
- **Muse は1本の長い会話**。新規チャットを作らず、同じ画面に添付して送る。返答は **2分**で届いた（手順書の 5〜12分より速い）。返答本文は out/muse_reply_<slug>.txt に保存した
- **Muse の判定：公開可**（FreeVideo 版）。書き起こしは台本と**一致率 98.4%**（差は「一」→「1」の表記と、「守護と地頭」→「守護・地頭」の1か所のみ。読み違いではない）
- **裏取り（手元の計測）**：平均 -17.3 dB は一致。**最大音量は Muse が -0.4 dB、手元の元ファイルは -1.5 dB**（Muse は 360p に圧縮後のファイルを測ったため、圧縮で変わる。元ファイルを正とする）。無音は手元では検出なし（Muse は冒頭 0.4 秒と言う）。ナレーション終了は Muse が約 43.1 秒、字幕の最終時刻は 43.47 秒（概ね一致）
- **Muse が読めないこと**：実際の聴感（BGM とのバランス）、元画質。**Muse の「公開可」は、出典の原文照合の代わりにならない**。Muse は「出典原文は未照合とのことだったので、こちらで照合」として NDL レファレンスと Wikipedia を根拠にしたが、これは私が使った資料と同じ二次資料である
- **Muse の判断のうち、鵜呑みにしなかった点**：clip4 の本のページの擬似文字を「ピンボケで判読できず、背景の質感の範囲」とした。実際のフレーム（16〜22 秒）では、**文字らしい行が見える**。公開版では取り直すか、画面の明記を維持する（判断はユーザー）
### clip4/clip5 の取り直し（2026-11-11、proto_fv_kamakura_seiritsu 第2版）

Muse が「ピンボケで問題なし」とした clip4 を、自分で描画後の見え方（cover 切り出し＋暗さ 0.7）にして確認したら、**白いエアコン（現代物）**と**文字の入った掛け軸**がはっきり映っていた。指示文の 
o modern objects / 
o text は守られていない。

- 1回目の取り直し（室内→板の間）: エアコンと掛け軸が出た。**室内はNG**（現代設備と文字が混ざりやすい）
- 2回目の取り直し（屋外の竹林）: 現代物・文字・人物なし。動きは 3.5 秒で画素の 84% が変化（静止ではない）
- clip5（墨を和紙に引く→**水に墨を落とす**）: 筆・紙・文字が出なくなった
- **教訓**: FreeVideo の出力は、**最終的な描画と同じ処理（cover＋dim）で見て**判断する。縮小・等倍のクリップだけでは、画面端の現代物を見落とす。室内・机・紙・筆を題材にすると、文字や小物が混ざりやすい。**屋外の自然物（竹林・水・霧・稲穂・雲）は安定**
- 確認した範囲: 11時点のフレーム、全フレームのデコード（エラーなし）、-14.0 LUFS／ピーク -1.5 dBFS、44.43 秒
- 未確認: 連続再生での動き、全編の実聴、BGM の聴感、スマホ実機、出典の原文照合

### Muse 再レビュー（改訂版）と、返答取得の罠（2026-11-11）

- 依頼文の末尾の目印「問題点は時刻つきで具体的にお願いします。」は、**自分が送った文にも入っている**。ページ全体（document.body）から目印の直後を読むと、**自分の文以降＝サイドバーの文字**を拾い、20秒で「返答完了」と誤判定した（実際は「レビュー中」）
- 正しい読み取り: **[role=log]**（チャット本文のコンテナ）の inner_text() から、目印の**最後**の出現より後ろを取る。レビュー中 が本文に無いことも完了条件にする
- 入力欄は前回の下書きが残ることがある（dry-run の後など）。**送信前に Control+a → Delete で空にする**。文字数が合わなければ送信しない（誤送信の防止に効いた）
- **Muse の判定（改訂版）: 公開可**。16〜22秒=竹林（本・筆・擬似文字なし）、22〜29秒=水に墨（文字・不自然な物体なし）を確認。書き起こしは前回と完全一致（背景だけ差し替え）。事実関係は前回と同じ資料に基づくため変更なし
- 所要時間: 送信から返答まで約2〜3分。scripts/muse_review.py で 1 コマンド（圧縮〜送信〜待ち〜保存）
### 一次資料の探索（2026-11-11 kamakura_seiritsu、ready 化の試み）

**到達できたもの**
- **国立公文書館デジタルアーカイブ『吾妻鏡』（金澤文庫本、重要文化財、請求番号 特103-0001）**: 簿冊 https://www.digital.archives.go.jp/file/4503889 → 各巻 https://www.digital.archives.go.jp/item/<id> → ビューア https://www.digital.archives.go.jp/img/<id> → IIIF manifest https://www.digital.archives.go.jp/api/iiif/<id>/manifest.json
  - 巻一=2589952、巻三=2589954、**巻五=2589947**（68コマ）、巻十=2589956。ID は巻順ではないので、ile/4503889 の HTML から item/<id> を全部拾って title を引く
  - 画像 URL: manifest の canvas → 
esource.service['@id'] + /full/max/0/native.jpg。**Referer と User-Agent を付けないと 403**（Referer: https://www.digital.archives.go.jp/img/<id>）
  - 画像は 1 コマ＝見開き。解像度は十分で、**くずし字が読める**（実測: 巻五のコマ58〜60で「八日 丁巳」「十一日 庚申」「十二日 甲子」など）
- **CiNii Research（論文＝標準の一次資料に該当）**: 川合康「鎌倉幕府の成立を問い直す」『歴史地理教育』815号 p.10（https://cir.nii.ac.jp/crid/1010282257135043585、NDL書誌 025173719）。同号には河野通郷「高校の授業 日本史「鎌倉幕府の成立年」を話し合う」p.48-51 も収録（NDLレファレンス crd 1000197449 が参照）

**到達できなかったもの**
- 東京大学史料編纂所の各 DB（SHIPS https://wwwap.hi.u-tokyo.ac.jp/ships/）は Vue の SPA で、検索 API の URL を HTML/JS から特定できなかった
- 国立国会図書館 次世代デジタルライブラリーも SPA。pp.bundle.js に検索 API のパスが見当たらない（/dl/api/imagefeatures のみ）
- 日本語 Wikisource の『吾妻鏡』は**巻一・二のみ**（1180年まで）。文治元年・建久3年は無い

**未了の理由（正直な記録）**
- 巻五の該当見開きらしきコマは見つけたが、**日付と干支の照合が合わず**（八日 丁巳／十一日 庚申／十二日 甲子）、十一月の条だと断定できなかった。月の表題コマを特定していない
- 『山槐記』『玉葉』の原文、教科書の実物、日本大百科全書・世界大百科事典・国史大辞典の原文、川合論文の本文は、**オンラインでは取得できていない**
- したがって 
eeds_research は空にできず、**status: ready にはできない**（標準どおり）

**次に必要なこと**: 公文書館の画像を月の表題から順に追う（1巻68コマ、実測1コマ数十秒で読める）、または NDL・図書館で教科書・事典・論文の現物を確認する
### オーナー判断（2026-11-11）

proto_fv_kamakura_seiritsu は、**この内容でよい**とオーナーが判断した。原文照合の未了は 
eeds_research に残したままとし、status は 
eeds_review のまま（標準のルールは緩めない）。アップロードする場合は、概要欄の出典・AI生成の明記と、YouTube の「AIの使用」を「はい」にする。
### アップロードと公開予約（2026-11-11、kamakura_seiritsu）

- 台帳キー: short_solo_kamakura_seiritsu / video id: **bi8n0NrsQAo** / 長さ PT45S
- アップロード用パック: upload/short_solo_kamakura_seiritsu/（title.txt・description.txt・tags.txt・video.mp4・subtitles_ja.srt）。scripts/yt_api.py upload <pack> は **private 固定**で上げる
- **公開予約: 2026-11-16 17:00（日本時間）= 2026-11-16T08:00:00Z**。同日 12:00 に short_solo_skytree があるので、時刻を分けた
- **AI の使用（containsSyntheticMedia）を True に設定**した（videos().update(part=status) で publishAt と同時に）。ただし **API の読み戻しでは None** が返るので、Studio の「詳細設定 → AI の使用」で「はい」になっているか目視確認が必要
- 字幕: 日本語が 2 本（asr = 自動生成、standard = アップロードした SRT）。SRT は out/short_proto_fv_kamakura_seiritsu_subtitles.srt
- 概要欄: 出典の原文照合が未了であること、AI 生成であること、出典（NDLレファレンス・朝日・Wikipedia）、クレジットを明記
- 確認: oEmbed が **403**（= 非公開のまま、予約待ち）。タイトル・タグ・概要欄の先頭は API で読み戻して一致を確認

### 同時刻の二重予約を見つけたら（2026-11-12）

- `data/youtube_ids.json` の全エントリを走査して `publishAt` の重複を確認する。2026-11-12 12:00 に `short_solo_elnino` と `short_solo_osaka_hohei` が**同じ時刻で予約**されていた（どちらも 03:00Z）
- チャンネルの通常枠は **12:00 と 17:00**。片方（osaka_hohei）を 17:00（`2026-11-12T08:00:00Z`）へ移し、`videos().update(part='status')` で `publishAt` を変更、台帳も更新した
- `videos().update` で status を更新するときは `containsSyntheticMedia` を明示する（API は読み戻さないため。地理院タイル背景の osaka_hohei は False、AI 背景の elnino は True のまま）
- 予約の重複チェックは、日付をまたぐ前に必ず行う

### koharu（小春日和）の作り直しと新版アップ（2026-11-12）

- **旧版はすでに public だった**: `data/youtube_ids.json` の `short_solo_koharu` は **NdsORT8RZH4**（2026-11-09 00:30Z 公開、91再生、タイトル「…約57秒で整理」）。アップロード前に台帳の既存キーを確認していなかったため、後から判明した。**今後はアップロード前に `short_<slug>` キーの有無を必ず見る**
- 旧版の根拠は Wikipedia のみで、画面の出典ラベルも Wikipedia だった。文化庁「平成26年度 国語に関する世論調査」報告書 p.82/86/90（n=1,942）で **51.7% / 41.7%** を確認し、台本・出典ラベル・概要欄を更新して再描画した（`scripts/gen_solo_koharu.py` を修正 → `make_short2.py solo_koharu`）
- 新版: **-TytIoEbUdE**（private）／長さ 59.82秒／1080x1920・30fps・1794フレーム／-14.14 LUFS・TP -1.47
- **公開予約: 2026-11-17 12:00（日本時間）= 2026-11-17T03:00:00Z**。同日 17:00 の short_solo_leonids と衝突しないことを台帳全件で確認
- **AI の使用（containsSyntheticMedia）を True に設定**（publishAt と同時の `videos().update(part=status)`）。API の読み戻しは None だが、**Studio（2026-11-12 08:03）で「はい、AI を使用しました」が選択済みなのを目視確認**した
- 字幕: `ja` / `standard` を SRT から `captions.insert` で投入（API で読み戻し確認）
- **タグを修正**: 旧版は長尺 43_bukka のタグ（家計・年収・消費者物価指数…）を引き継いでいた。新版は `小春日和,季語,日本語,言葉,雑学,Shorts`
- 台帳: `superseded` に旧 ID を記録。旧版は 2026-11-12 に **unlisted（限定公開）へ変更**（オーナー判断。統計と URL は保持し、削除はしない）。これで同題材の重複公開を避け、新版の公開後に旧版の統計を見て残す/消すを決められる
- **Studio 目視（2026-11-12 08:03、ログイン後）**: 寄り道ラボのチャンネルで確認。公開設定「**公開予約**」／子ども向け「いいえ」／**AI の使用「はい、AI を使用しました」選択済み**／動画の言語「日本語」／動画リンク `https://youtube.com/shorts/-TytIoEbUdE`／字幕ページに「日本語の字幕」を確認。概要欄は API の読み戻しと投稿パックが 2,221B で一致
  - 確認スクリプト: `out/check_studio_koharu.py`（CDP 9222・Playwright。チャンネルID不一致なら停止）。**自動化プロファイルは事前に `寄り道ラボ` でログインが必要**（未ログインだと accounts.google.com にリダイレクトされる）

### yoritomo_zo（伝源頼朝像＝足利直義説）の試作（2026-11-12）

題材は「学校で源頼朝の顔として覚えたあの肖像画は、いまは『伝源頼朝像』と呼ばれ、足利直義とする説がある」。
高年齢層向けの「昔の説 → いまの説」型。標準フロー（brief → result.json → check）は通したが、
原著・一次史料の照合が未了なので `status` は `needs_review`、描画は **試作 `proto_` のみ**（投稿可の判断はしていない）。

| 項目 | 値 |
| --- | --- |
| brief | `shorts/yoritomo_zo/brief.yaml`（brief-check 指摘0） |
| 台本 | `shorts/yoritomo_zo/result.json`（43秒・7シーン、check は ERROR 0 / WARN 4） |
| 試作 spec | `scripts/make_spec_yoritomo_zo.py` → `data/short_proto_yoritomo_zo.json` |
| 背景の生成 | `scripts/make_assets_yoritomo_zo.py` → `assets/yoritomo_zo/bg_0..6.png` |
| 描画 | `python scripts/make_short2.py proto_yoritomo_zo` |
| 出力 | `out/short_proto_yoritomo_zo.mp4`（git 管理外） |

**実測（確認した範囲）**: 1080x1920 / 30fps / **43.63秒** / h264 + AAC 48kHz。全編デコードでエラーなし。
loudnorm 実測 **-14.0 LUFS / True Peak -1.5 dBTP**。`silencedetect` で無音は冒頭 0.37 秒のみ（文間の音切れなし）。
字幕 SRT は 11 ブロックで、ナレーションと1対1（`out/short_proto_yoritomo_zo_subtitles.srt`）。
8時点（2/6/12/16.5/26/28/36/41秒）の静止画で、図・字幕・資料名の重なりを目視確認した。

**資料画像の扱い（重要）**

- Wikimedia Commons `File:Minamoto no Yoritomo.jpg`（1584x1974）を使用。ライセンスは `PD-Art` + `PD-old-100-expired`（deathyear=1205）
- ただし同ファイルページの `source` は **`{{unknown|source}}`＝出典・撮影者不明**。所蔵者（神護寺）撮影の画像ではないため、
  京都国立博物館の画像利用規程（インターネット 11,000円/年・申請2週間）の対象外と判断した。**この判断は法的助言ではない**
- 画面下（y>1610）に「資料：伝源頼朝像（神護寺蔵・国宝）／画像：Wikimedia Commons（PD-Art）」を焼き込む
- 画像は `assets/` 配下（`.gitignore` の `*.jpg` / `*.png` で追跡外）。再取得は
  `https://upload.wikimedia.org/wikipedia/commons/7/76/Minamoto_no_Yoritomo.jpg`

**描画で詰まった点と対処（すべて実際に踏んだもの）**

1. **`sub` パネルが肖像の顔を隠す**。`make_short2.py` は `sub` を y=800〜960 の固定パネルに描く。肖像の顔は
   その位置に来るため、**図の無い場面では `sub` を空にした**（`make_spec_yoritomo_zo.py` で機械的に処理）。
   顔を y≈1060 に置き、`big`（y=520）と字幕（1470〜1540）の間に顔が収まるように背景を作った
2. **肖像の上端が横一直線に見える**。画像をそのまま貼ると、絵の上部境界が硬い線として出る。
   `compose()` で上端を `top_feather=340px` でぼかし、左右・下端も 140px ぼかして地の色になじませた
3. **引き出し線（冠・太刀）は失敗**。線が字幕域（1240〜1540）を横切り、ラベル「太刀」が笏と袍の上に落ちて読めなかった。
   **実物への加筆はやめ**、根拠は `timeline` の図（文字の札）で示す方針に変えた
4. **`flow` 図は左右に余白が偏る**。3列の `mid` と下端の `leaf` を同時に使うと、左の箱が画面端に寄り、
   `leaf` と `src` ラベル（y≈1200）が近接した。**`timeline` に置き換えた**（項目2つの `timeline` が最も読みやすい）
5. **左端 65px が切れる**。`bg_fit=1.12` と Ken Burns で左右が切れるため、焼き込んだ資料名を x=36 から **x=92** へ移した
6. **ffmpeg が PATH に無い**（`FileNotFoundError: [WinError 2]`）。そのセッションだけ
   `$env:Path += ';C:\Users\neoen\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin'` を足す
7. **`python - <<'PY'`（ヒアドキュメント）は PowerShell では動かない**。`ParserError` になる。一時 `.py` ファイルを書いて実行する

**台本で避けたこと（根拠の都合）**

- 「足利直義で確定」と書かない。**所蔵者の神護寺が公式サイトで「表記を変更する必要はない」と明言**しており、論争は続いている
- 「全国の教科書が一斉に変わった」と書かない。確認できたのは nippon.com・テレビ朝日・帝国書院FAQ の記述のみで、
  会社別・年度別の一次比較（金沢大学『教育実践研究』41号のPDF）は取得先のメンテナンスで未取得
- **願文の年を言わない**。神護寺公式・nippon.com・Wikipedia は「康永4年＝1345年」、帝国書院FAQ だけが「1354年」で1桁違う。
  動画では「南北朝時代の願文」とだけ述べた
- 「40代以上」は nippon.com 1社の表現なので、ナレーションでは使わず `<br>` 概要欄の根拠にも入れていない

**未確認の範囲**: 米倉迪夫『源頼朝像 沈黙の肖像画』（平凡社1995）・黒田日出男・宮島新一・近藤好和の原著、
『足利直義願文』の原本、各社教科書の紙面、ナレーション全編の実聴、連続再生での動きの滑らかさ、スマホ実機表示、BGM の聴感。
**投稿可の判断はしていない**

---

## 2026-11-17: Analyticsの日付区切りと、4〜7秒離脱の実測（Ask Studio）

**1. Analyticsの「日」は太平洋時間で区切られる（今回わかった）**
- 実測: 11/15 12:00（JST）公開の2本の再生は、日別表の **「11/14」行**に入る。11/15 17:00 以降に公開した動画はまだどの行にも入らない。
- 区切りは JST 17:00（＝UTC 08:00 ＝米国太平洋時間の0時）。チャンネルのタイムゾーン設定が日本時間でない可能性（原因は未確認）。
- **日別の数字を「日本時間の公開日」と並べて比べない**。比較するときは、この17:00区切りを明記する。

**2. 離脱は0〜3秒ではなく「4〜7秒」（Ask Studio、2026-11-17）**
| 指標 | 高パフォーマンス（宝くじ218%・壊血病144%） | 低パフォーマンス（厳島32%・うめきた37%） |
|---|---:|---:|
| スワイプ率 | 72〜77% | 81〜82% |
| 視聴を継続率（ショート） | 23〜28% | 18% |
| 平均視聴時間 | 尺の1.5〜2倍（ループ再生） | 尺の3〜4割 |

- 維持率カーブでは、**0〜3秒は100%前後でほぼ横ばい**。**4〜7秒で 105%→66%（約40%の急落）**が起きる。上位動画は同じ区間で282%→253%と緩やか。
- 対策（Ask Studioの提案）: 4〜6秒目に「意外な数字や結論の断片」を置く。前提説明を先に語らない。
- 適用例: 
younkaku（明治の浅草12階）は、場面1の冒頭2文で問いと答え、直後に「1890年11月」「8階まで」の数字を置いた。

**3. 未予約のShorts在庫は「既出題材の別版」が多い**
- 未予約・非公開で40〜70秒のShortsは**94本**あるが、タイトルを見るかぎり既出題材の別版（_nl など）が多い。
- 薄い日（11/19・11/20）を埋めるとき、在庫をそのまま出すと**同じ題材の再掲**になりやすい。**新作を薄い日に置く方が安全**（11/19 19:00 に 
younkaku を置いた）。

## 2026-11-18: 年賀状の日付は年ごとに変わる／AIレビューの採否

**1. 「12月15日から受付・12月25日が締切」は、今年の案内ではない**
- 2027年（令和9年）用の年賀状は、**引受開始が2026年12月20日（日）**、**元日配達の目安が2026年12月27日（日）まで**（日本郵便FAQ「年賀状の引受は何日からですか？」 https://www.post.japanpost.jp/question/140.html 、2026-11-18確認）。
- 年賀状の受付日は**年ごとに動く**。過年度の日付を一般則として台本に書かない。公開する年の公式案内で確認する。
- 公式表現は「できるだけ12月27日まで」なので、台本では「締切」ではなく「目安」と言う。過ぎた場合は「元日に届かない可能性がある」とし、断定しない。
- 12月20日より前の扱い（「通常の郵便として年内に届く」）は、公式FAQに説明がないため**書かない**。

**2. AIレビューの指摘は、裏取りしてから採る（再確認）**
- ChatGPT（85/100「修正後に公開OK」）: 場面3の「それより前は年賀状としての取扱いにならない」は誤解を招く→「元日以降に届けてもらうには、12月20日以降に出す」に修正。場面2の「1873年で急速に広まった」という因果も弱めた。
- Gemini（「公開して問題ない」）: 「12月20日より前に出すと年内に届く」「フライング投函は年内に届く」を提案したが、**公式に説明がないため不採用**。Geminiは甘く、出典にない断言をすることがある（手順書4-3の実例）。
- 台本v2: `data/short_solo_nenga.json`。根拠: `docs/research/20261118_nenga_sources.md`。レビュー記録: `docs/research/20261118_nenga_reviews.md`。

**3. Museの添付確認は、サムネイルのblobと「添付ファイルを削除」ボタンで判定する（2026-11-18）**
- Museは添付ファイル名を本文に出さない。添付後は**サムネイルの `<img src="blob:...">`** と、**`button[aria-label="添付ファイルを削除"]`** が出る。
- 旧 `muse_review.py` は (a) `body.innerText` のファイル名、(b) `video` の blob URL だけで判定していたため、実際に添付済みでも「添付NG」で止まった（nengaで2回発生）。
- 修正: まず既存の「添付ファイルを削除」を押して下書きを空にし、添付後に同じボタンが出たか（または新しい `img/video` のblobが増えたか）で成功を判定する。ファイル名が無いときの再添付はしない（二重添付を防ぐ）。

**4. 字幕の行数は、文字数ではなく句読点の数で制限する（2026-11-18）**
- `chunks()` が「15字×2行」の文字数だけで塊を作ると、3文が1塊になり、エンドカードが3行になった（nenga）。
- 句読点の数（＝画面の行数）も `lines` 以下に制限するよう修正。SRTの1塊が2行を超えない。
- 1秒ごとの52コマを並べた確認で見つけた。Museの「サンプリング」だけでは、行数の違反は拾えないことがある。

## 2026-11-19: 同時刻の重複が5枠になった（3系統のキューが独立に予約）

**1. 症状（API実測）**
- 11/19 12:00 に単独Short 2本（`short_solo_shorui_niwatori_nl` ZUR5R9xLvmY と `short_solo_tokusei` MXSp6vn7t6A）。
- 11/19 19:00 に**長尺2本**（`27_forest` wD8rSfy5y0I と `79_hibiya` OrGGevmW-tU）＋単独Short 1本（`short_solo_ryounkaku` Y4l8Tyf15j4）。
- 同種の重複が 11/20 12:00、11/21 12:00、11/21 19:00 にもあった（11/21 19:00 も長尺2本：`28_shomi` と `32_komaki`）。

**2. 原因**
- 予約を入れる経路が3つに分かれ、**互いの枠を見ていない**。
  - ① 長尺の波：`PRODUCTION_CYCLE.md` の「19:00 長尺／20:00 同題材 Short」。
  - ② `_nl` 一括再投稿（Studio で作り直した旧作）：12:00/17:00 を 11/21 まで埋める。
  - ③ 新作の単独Short：12:00/17:00 に加え、スワイプ率検証のため 19:00 にも入れた。
- 19:00 に単独Shortを入れたのは `docs/kpi_swipe_tracking.md` と `docs/themes/20271101_hibiya/05_gates.md` が、それぞれ独立に「11/19 19:00」と決めたため。**両方とも、その枠が長尺の枠だと認識していない。**

**3. 見落とした理由（重要）**
- `data/youtube_ids.json` の `publishAt` は**予約したときにしか書かれない**。API 実測では予約がもっと入っているのに、台帳には一部しか載っていない。**台帳は予約の正ではない。**
- `scripts/check_publish.py --check` は **2026-10-21 のスナップショット**を基準にしているため、今走らせると「予約がずれた」の誤検知になる（基準の更新が必要）。
- 対策として **`scripts/check_slots.py`** を追加（`videos().list` のみ・336本で約7ユニット。重複があれば終了コード1）。予約を入れる前後で必ず走らせる。

**4. 処置（2026-11-19 09:30、`scripts/yt_api.py schedule` で4件）**
| 動画 | 変更前 | 変更後 | 理由 |
| --- | --- | --- | --- |
| `short_solo_shorui_niwatori_nl` ZUR5R9xLvmY | 11/19 12:00 | 11/22 12:00 | 新作 `tokusei` を 12:00 に残す（`_nl` は後日で損がない） |
| `27_forest` wD8rSfy5y0I | 11/19 19:00 | 11/22 19:00 | 19:00 は長尺1本に。単発在庫なので動かす損が小さい |
| `short_forest` piQdBb8SsNY | 11/20 20:00 | 11/22 20:00 | 長尺とセット（片方だけ動かすと概要欄リンクが非公開を指す） |
| `short_solo_ryounkaku` Y4l8Tyf15j4 | 11/19 19:00 | 11/19 20:00 | 19:00 長尺の直後。今日はここしか空きが無い |
- **hibiya を残した理由**：`PLV4MJdcpAGpM`「東京の低地」の1本目で、翌日の渋谷と並べる設計（サムネ・字幕・再生リストまで仕込み済み）。
- 結果（API読み戻し）：11/19 は 12:00 tokusei／17:00 sushi_two_nl／19:00 hibiya（長尺）／20:00 ryounkaku。**当日の重複はゼロ**、11/22 も 12:00/19:00/20:00 に1本ずつ。台帳の `publishAt` も4件更新した。

**5. 残り（未処置・11/20〜11/21）**
- 11/20 12:00（`short_solo_minatomirai` × `short_solo_travel_tokaido_nl`）
- 11/21 12:00（`short_solo_edo_kaji` × `short_solo_yakurei_menkyo_nl`）
- 11/21 19:00（長尺 `28_shomi` × 長尺 `32_komaki` × `short_solo_netsuden`）
- これらは**玉突き移動**になるので、`data/slot_table.json` のような枠表を1つ作ってから一括で直す。今日の公開には影響しない。
- 方針案：単独Shortは 12:00/17:00 に1本ずつ、19:00 は長尺1本、20:00 は 19:00 長尺と同題材の Short。`_nl`（再投稿）は新作より後ろへ送る。

**6. 検証コマンド**
- `python scripts/check_slots.py`（前日〜3日先。`--days 7` で拡張）
- 1件ずつ変えるときは `python scripts/yt_api.py schedule <video_id> "2026-11-22 12:00"`（JST。チャンネルID検証と `containsSyntheticMedia` の引き継ぎは実装済み）

**7. 追補（2026-11-19 15:00、上の「残り」のうち7件を移動）**
| 動画 | 変更前 | 変更後 |
| --- | --- | --- |
| `short_solo_travel_tokaido_nl` CWgTDSuyPoU | 11/20 12:00 | 12/09 12:00 |
| `short_solo_yakurei_menkyo_nl` 07bs0uqJWmc | 11/21 12:00 | 12/05 12:00 |
| `short_solo_netsuden` vOqfTUfFExM | 11/21 19:00 | 11/24 19:00 |
| `28_shomi` asBXlN_49tk | 11/21 19:00 | 11/28 19:00 |
| `short_shomi` qX1IAFU91ak | 11/22 20:00 | 11/28 20:00 |
| `27_forest` wD8rSfy5y0I | 11/22 19:00 | 12/03 19:00 |
| `short_forest` piQdBb8SsNY | 11/22 20:00 | 12/03 20:00 |

- 結果：`check_slots.py --days 21` の同時刻重複は **16 → 11**。11/20・11/21 は1枠1本、11/22 は 12:00 の3本だけが残る。移動先は実行直前に空きを確認した。
- **`netsuden` はFreeVideoのAI背景**。`yt_api.py schedule` が `containsSyntheticMedia` を False に戻すため、移動後に `videos().update(part='status', … containsSyntheticMedia=True)` をやり直した（他6件はAI映像背景ではない）。
- 残り11件の内訳：`_nl`（再投稿）が7枠に残る／新作同士の衝突が5枠（11/22・11/23・11/25・11/26・11/28の12:00）／長尺2本が2枠（11/27・11/29の19:00）。12/11以降の空き12:00は11枠、空き19:00は8枠あるが、全部は収まらないため方針の決定が必要（`_nl`を後ろへ送る／新作の一部を17:00へ／再投稿を間引く）。

**8. 追補2（2026-11-19 15:01、残り14件を移動して同時刻0に）**
| 動画 | 変更前 | 変更後 |
| --- | --- | --- |
| `short_solo_shorui_niwatori_nl` ZUR5R9xLvmY | 11/22 12:00 | 12/12 12:00 |
| `short_solo_suiban` AOkbmQp3UGU | 11/22 12:00 | 12/06 17:00 |
| `short_solo_yoriki_shizugatake` P8YEIJfbzoo | 11/23 12:00 | 12/07 17:00 |
| `short_solo_komugi_jikyu_nl` m8F9ZsgKgXo | 11/24 12:00 | 12/14 12:00 |
| `short_solo_galileo_sore_nl` Ru0b5MD-cUY | 11/24 17:00 | 12/15 12:00 |
| `short_solo_brain_origin_nl` BTjz7NZExfk | 11/25 12:00 | 12/16 12:00 |
| `short_solo_mitsuyaku_shizugatake` UGSb2LtYA6w | 11/25 12:00 | 12/08 17:00 |
| `short_solo_columbus_flat_nl` jht-JeLp0bc | 11/25 17:00 | 12/17 12:00 |
| `short_solo_moon_dark_nl` sLk85oIUQQM | 11/26 12:00 | 12/18 12:00 |
| `short_solo_yonmikata_komaki` rvpMUlhTcCI | 11/26 12:00 | 12/10 17:00 |
| `short_solo_bukka_katei_nl` k8Qm7_0EM-o | 11/26 17:00 | 12/19 12:00 |
| `20_sunrise_solstice` BeY3kMjDjzs | 11/27 19:00 | 12/06 19:00 |
| `short_solo_toji` 1vhIFZrNpdc | 11/28 12:00 | 12/22 12:00（冬至当日） |
| `62_sankin` NFzaQWPs97c | 11/29 19:00 | 12/07 19:00 |

- 結果：`check_slots.py --days 35` の同時刻重複 **0**。12/23・12/25・12/30の12:00は空けた。
- AI背景の `suiban`(AOkbmQp3UGU) と `toji`(1vhIFZrNpdc) は、`schedule` 後に `containsSyntheticMedia=True` を再設定した。
- 残る不揃い（同時刻ではない）：`20_sunrise_solstice`(12/06 19:00) の同題材Short `short_sunrise` は12/19 20:00、`62_sankin`(12/07 19:00) のShort `short_solo_sankin_tabi10` は未予約。ペアを揃えるなら 12/06 20:00 と 12/07 20:00 が空き。

**9. 予約を動かしたら、Xの紹介投稿も同じだけ動かす（2026-11-19 15:35）**
- 動画の公開時刻とX予約（`x.com/compose/post/unsent/scheduled`）を突き合わせたところ、**4件がずれていた**。Xの予約は動画の予約とは独立で、動画を移しても自動では追従しない。
- 修正した4件（Xの「編集」→ 日時を変更 → Update → Schedule。各1件のまま重複なしを確認）
  - `Y4l8Tyf15j4` 凌雲閣: 11/19 19:05 → **20:05**（動画を20:00へ移したため）
  - `vOqfTUfFExM` 発電: 11/21 19:05 → **11/24 19:05**
  - `AOkbmQp3UGU` 玉川上水: 11/22 12:05 → **12/06 17:05**
  - `1vhIFZrNpdc` 冬至: 11/28 12:05 → **12/22 12:05**
- 手順: `unsentTweet` をクリック → `scheduledTweetIndicator` をクリック → `#SELECTOR_1..5`（月・日・年・時・分）を設定 → 「Update」→ 表示が変わるのを確認 → 「Schedule」。Playwrightの通常クリックは背景divに遮られるので、JSの`.click()`を使う。
- 確認: 予約一覧を読み直し、各動画IDが1件・新しい時刻であること。

## 実測：伊能忠敬の単独Short（2026-11-19 inou）

**題材**：伊能忠敬は歩幅だけで日本地図を作った？ → 実際は縄・鉄鎖・星で測った（足掛け17年）。根拠は国土地理院「“伊能図”近代地図の原点」(PDF)と「測量・地図ミニ人物伝：伊能忠敬」（2026-11-19に取得。PDFの本文は `out/_inoh_pdf.txt` に抽出）。台本は `scripts/gen_solo_inou.py`、描画は `python scripts/make_short2.py solo_inou`。

- **背景clip1の作り直し（AI生成の文字）**：「古い手描きの地図」を頼むと、1回目は**世界地図**（日本列島でない）、2回目は日本沿岸図だが**漢字の列が写った**。通ったプロンプトは「巻物状の無地の紙＋墨の海岸線1本＋赤い細線1本、それ以外は白紙」を明示し、no writing / no characters / no calligraphy / no cartouches / no seals / no numerals を並べたもの。0.5・2.5・4.5・6.5秒の静止画で文字がないことを確認した（`out/_chk_in_c1c.png`）
- **`scripts/fv_clips.sh` のクリップ指定は `clipN`（番号だけは不可）**：`bash scripts/fv_clips.sh inou 1` は `freevideo_batch.py` の名前一致で何も作らず、**28.9秒で「ALL OK」・exit 0**（`clip1.mp4` のmtimeも不変）。正しくは `bash scripts/fv_clips.sh inou clip1`。生成は469.7秒（ComfyUI起動込み。544x960・24fps・7.30秒・690,076バイト）
- **描画はクリップ差し替えの完了後に行う**：13:14 の描画は差し替え前のclip1（世界地図）で `raw.mp4` を作っており、その生映像は捨てた
- **大テロップの読点**：`solo_spec.build()` が `big`/`sub` の `、` を削除するため、「方角は方位盤、緯度は星」は「方角は方位盤緯度は星」と連結して読めない。台本側で `／` を書く（今回は「方角は方位盤／緯度は星」「大図214枚／1821年」「足掛け17年／縄・鎖・星で測量」に修正して再描画）
- **実測（最終）**：1080x1920／30fps／60.33秒／h264+aac 48kHz stereo、全フレームのデコードでエラーなし、Integrated −13.9 LUFS、True peak −1.5 dBFS。字幕18区間（各2行以内）
- **未確認**：全編の実聴（読み・間・BGMバランス）、連続再生での背景の動き、スマホ実機、投稿可否。尺は60.33秒で、直近の単独Short（yubin_ju 56.9秒）より長い
- **Museレビュー（14:23、`out/muse_reply_solo_inou.txt`）**：判定は**このまま公開可**。返答までの時間は約150秒。書き起こしは台本とほぼ一致（「足掛け17年」の言い回しだけ語順が違う）。Museは「ナレーションは約58.5秒で終わり、最後の約2秒はBGMのみ」と書いたが、手元の字幕の最終時刻は59.38秒で、圧縮コピー(360p)での計測。音量もMuseは最大 −0.4〜−0.5 dB（360p圧縮後）、**元ファイルのTrue peakは −1.5 dBFS**（これまでどおり元ファイルを正とする）。Museの注記「第一次測量(1800年、蝦夷地)は歩測が中心という資料もある」は、台本の「『だけで』への反論」を崩さないため採用しなかった
- **Muse送信の失敗と判定の誤検知（同日）**：1回目は既存のCDP Chromeが待機中に閉じられ `TargetClosedError`（55秒で終了）。2回目は送信・添付とも成功し、返答も有効だったが、`muse_review.py` の「届いていない」判定が `0.0 dB には届いてない` と `偽文字も見当たらない` を部分一致で拾って**exit 3（不採用）にした**。判定を「動画・映像・ファイル・添付を主語にした文」に絞る修正を入れた（`動画が届いていない` などの実例と、上記2つの誤検知例で確認）
- **アップロードと予約（2026-11-19 14:33）**：`python scripts/solo_schedule.py solo_inou "…"` で非公開アップ→ `SAR6EXwQu6Q`、字幕 `ok`（ja standard と YouTube自動の asr の2トラック）、タイトル・タグ9件・概要欄をAPIで読み戻し確認。**当初 11/30 17:00 に入れたが、既存の `short_solo_vitaminc_kaze`(10a-XRaX79Q) と同時刻重複**だった（`check_slots.py` の出力を `head` で切って見落とした）。12/04 19:00（当日は12:00の1本だけの薄い日）へ移動し、重複なしを再確認
- **`yt_api.py schedule` は AI開示フラグを消す**：`containsSyntheticMedia` は `part=status` の読み戻しに出ないため、`cmd_schedule` が `cur.get('containsSyntheticMedia', False)` で **False を書き戻す**。予約を動かした後は `videos().update(part='status', … containsSyntheticMedia=True)` をやり直す（今回、移動後に再設定した）
- **Studio でのAI開示のUI確認はできなかった**：`/video/SAR6EXwQu6Q/edit` には「子ども向け」のラジオ2つ（`get_by_role('radio')` で列挙。`VIDEO_MADE_FOR_KIDS_*`）だけで、「改変」「合成」の文言と該当ボタン（`詳細設定を表示` 等）が無い。APIの200応答のみが確認で、UI上の「はい」は未確認（2026-11-19時点のStudio UI）
- **CDP 9222 の取り合い**：9222 は別プロファイル `.chrome-gemienox`（別チャンネル UCBQ8…）が使用中だった。触らず、`.chrome-automation`（寄り道ラボでログイン済み）を 9333 で起動して確認した。Muse 1回目の `TargetClosedError` も、9222 が別プロファイルだったためと推定（未検証）
- **ASR（kotoba-whisper、76秒）**：数字・日付は一致（17年・60間・108m・1尺・60本・1821年・2026年11月19日）。ずれは同音の取り違えのみ（60軒・井戸・異能体・大津・植え定・出店）。kana が正
- **無音・静止**：`silencedetect`（-45dB/0.6秒）は検出なし。`freezedetect` は32.6秒から2.2秒を静止としたが、実測で2秒間に3.6%の画素が変化（星空）。フリーズではない

## 実測：1円玉の単独Short（2026-11-19 solo_1yen）

- **題材と出典**: 「1円玉は、作るのに1円以上かかる？」→ 造幣局の公式Q&Aは「貨幣の製造原価（コスト）については…公表していません」と明記。理由は信任維持と偽造防止。1円貨はアルミニウム製・1g（造幣局「現在製造している貨幣」）。確認したURLと使わなかった数字は `docs/research/20261119_1yen_sources.md`。「3円で作れる」は一次資料で確認できないので断定しない。
- **自作背景のときの罠**: `solo_spec.build()` は全場面に `vid=assets/<slug>/fv/clipN.mp4` を入れる。AIクリップを作らない場合は、specを作った後に `sc.pop('vid', None)` しないと `make_short2.py` が ffprobe で存在しないclip1を読んで落ちる（2026-11-19に実験）。併せて `art` を自作背景に変更。
- **背景画像**: `scripts/gen_solo_1yen.py` の `make_bg()` がPILで硬貨イラストを生成（`assets/` はgit管理外なのでスクリプトから作る）。AI生成映像・AI画像は使っていない。
- **読み**: 造幣局はカタカナ辞書 `ゾウヘイキョク` だと「ぞえいきょく」と読まれた。`ゾーヘイキョク`（_long vowel）で「ぞうへいきょく」になる。`--kana` で全文を目で確認してから描画する。
- **画面**: 大テロップ「1グラムのアルミ」は右端で切れたので「重さ1グラム」に短縮。`make_short2.py` は長い大見出しを自動縮小しない。
- **Muse**: 判定「公開可」。ただし自動ゲートが「AI生成映像の不自然さは**見当たらない**」を不達と誤検知（exit 3）。`muse_review.py` の判定を「届来・確認・受取の否定」に限定するよう修正済み。9222は別プロファイルが使うため、`MUSE_CDP_PORT=9223` で実行（環境変数に対応させた）。
- **実測**: 1080x1920／30fps／48.17秒、-14.1 LUFS、全編デコードエラーなし。字幕18区間以内、代表9時点で文字の重なり・はみ出しなし。尺48.2秒は30〜45秒の標準より長い。
- **投稿**: 当初 `uqnodkk9_Qo`（非公開→11/20 20:00、X 20:05）だったが、**FV版に差し替えたため2027-01-01へ退避**。下記FV版を参照。AI背景ではないため `containsSyntheticMedia` は設定していない。
- **未確認**: 全編の実聴（Museは書き起こし一致と判定。固有名詞の読みはASRで「造兵局」と拾われたが認識側のぶれ）、スマホ実機表示。Museが受け取ったのは360x640の圧縮版で、元ファイルは1080x1920を確認済み。

## 実測：1円玉ショートのFreeVideo版と台本レビュー（2026-11-19 solo_1yen_fv）

- **差し替え理由**: 最初に自作の1枚絵背景で作ったが、動きがないため依頼でFreeVideo版に作り直した。YouTubeの動画ファイルは同じIDで差し替えられないため、**新しいIDをアップし、旧予約を2027-01-01へ退避、X予約のURLも書き換える**手順を取った（旧 `uqnodkk9_Qo` → 新 `vlnDxTPnAkA`）。`yt_api.py` の `update` は `publishAt` を省略しても予約が消えないため、退避先の日時を明示する必要がある。
- **台本レビュー**: ChatGPTとGeminiに同じ台本を渡した（最初のChatGPTは古い会話の返答を拾ったので新チャットで送り直し）。指摘と採否は `docs/research/20261119_1yen_reviews.md`。採用したのは (1) 場面3を「製造代金の**算定には**原価が勘案される」と算定基準だと明示、(2) 画面の「通説=3円かかる？」を「噂=3円は未確認」に変更、(3) 図を「量目=1g」に統一、(4) 場面4の日付の読み上げを削除（時点は場面1の図と概要欄に残す）。Geminiの「場面3の法律は出典ページに無い」は不採用: 造幣局Q&Aの本文が第4条4項を引用していることを確認済み。
- **手順の反省**: 手順書では台本レビューは**背景生成の前**。今回はFVクリップ生成後に実施してしまい、その結果として台本修正後の再描画が発生した。次回は生成前に挟む。
- **FVクリップ**: `bash scripts/fv_clips.sh 1yen_fv`。初回は既存ComfyUIと8188番/portとDBロックが競合してclip2以降が `server_down` になった。プロセスを確認して空いてから再実行し、clip2〜4を生成。後から硬貨の図柄が人物の横顔になっていたため、clip1とclip4を「若木の意匠・人物なし」で作り直した。縁の文字はAI特有の崩れが残るが、主役の図柄は1円玉になった。
- **Muse**: 修正前は「硬貨が外国のコインに見える」と指摘しつつ公開可。修正後の最終版は「図柄も直り、尺44.0秒も基準内」で**公開可**。ナレーション・字幕・事実・日付も一致。
- **実測**: 1080x1920／30fps／43.97秒、全編デコードエラーなし。最大音量 -0.9 dB（Muse）。背景はFreeVideo、図は自作。
- **最終状態**: `vlnDxTPnAkA`（非公開→2026-11-20 20:00 JST、`containsSyntheticMedia=True`）、X予約は同じ枠の20:05（予約一覧で新IDのみ1件）。`check_slots.py` で重複なしを確認。
- **未確認**: 全編の実聴、スマホ実機表示、StudioのAI開示UI（APIで設定済み）。

## 実測：根拠テーブルゲートの実装（2026-11-20）

- **背景**: 単独Short経路は `shorts/<slug>/result.json` を持たず CI の標準検査対象外だった（`SHORTS_STANDARD_INTEGRATION.md` §10）。2026-11-20 のオーナー確認で、標準を緩めずに `data/short_*.json` へ `claims` / `needs_research` / `scenes[].claim_ids` を追加し、アップ前に検査する方針に決定。[`SHORT_EVIDENCE_GATE_20261120.md`](SHORT_EVIDENCE_GATE_20261120.md)
- **検査**: `python scripts/check_short_evidence.py data/short_seijin.json` → OK（ERROR 0 / WARN 0）。`python -m unittest discover -s tests -p 'test_short_evidence.py'` → 11 tests OK。`sh -n scripts/hooks/pre-commit` → OK。
- **差し込み先**: `scripts/solo_schedule.py` は `procedure_gate.require()` の直後、キー `short_<slug>` から `data/<key>.json` を導いて検査する。`make_short2.py` は追加キーを `spec.get()` で無視するため描画系は未変更。
- **既存の扱い**: `data/short_*.json` は284本。全件遡及せず、CI は PR の変更分、pre-commit はステージ分だけを検査する（祖父化）。
- **`seijin` の根拠**: 未公開の `short_seijin` を再利用。内閣府2ページ＋名古屋大学の法令DB（e-Gov の代替、evidence_note に明記）で6主張を裏取り。`short_solo_seijin1115` は「1949〜1999年」が二次情報のため `superseded` に記録して非公開。
- **KPIの中間値**: `python scripts/yt_analytics.py videos` で旧型の平均視聴率（玉川上水 74.2%、プラニマル 97.7%）は取得。凌雲閣・発電はまだ ANALYTICS に出ておらず、スワイプ率は API に無い。判定は 11/26 に後ろ倒し（`kpi_swipe_tracking.md` 更新）。
- **未確認（当時）**: ChatGPT/Gemini の台本レビュー（当時CDPが応答せず）、凌雲閣・発電のスワイプ率（Studio 要ログイン）、`short_seijin` / `48_seijin` の連続視聴・全編実聴・スマホ実機、1/11 の公開予約。公開可否の判断はしていない。

## 実測：CDP 台本レビューの実行（2026-11-20 続き）

- **起動**: 通常プロファイルの Chrome には `--remote-debugging-port` が付いていない。自動化プロファイルを `Start-Process chrome.exe -ArgumentList '--remote-debugging-port=9222','--user-data-dir=C:\Users\neoen\.chrome-automation','--no-first-run','about:blank'` で起動すると `127.0.0.1:9222` が LISTEN した。ChatGPT / Gemini ともプロファイルにログイン済み。
- **スクリプト**: `scripts/review_short_cdp.py <slug> chatgpt|gemini`。プロンプトは spec の6シーン・根拠テーブル・未確認から自動生成（2257字）。Gemini は `div[aria-label="Gemini へのプロンプトを入力"]` に fill して Enter で送信、応答は保存できた。
- **ChatGPT のDOM変更**: 旧セレクタ `div[data-message-author-role="assistant"]` は2026-11-20時点で**0件**。現在の応答は `div[class*="DilResponseRoot"]` にあり、これをセレクタに変更して取得した。初回は旧セレクタのまま300秒待ってタイムアウトした（`--reuse` で再送信せず回収）。
- **結果**: 両方とも「公開可」。ChatGPTは軽微な改善案（シーン5の文言、シーン1の読点、シーン6のCTA）、Geminiは小テロップ提案（必須ではない）。再利用動画なので採用すれば再描画＋新ID＋予約・X差し替えが必要で、事実誤りではないため今回は不採用。採否は [`research/20261120_seijin_reviews.md`](research/20261120_seijin_reviews.md)。
- **未確認（残り）**: 連続視聴・全編実聴・スマホ実機、凌雲閣・発電のスワイプ率、1/11 の公開予約。

## 実測：Shorts優先方針への切替と1/11枠（2026-11-20）

- **方針変更**: オーナー判断で Shorts を優先し、長尺の新規公開を一旦停止。`48_seijin` の1/11 19:00予約は立てず、既存予約の `66_yakurei` も解除した（動画は削除せず private 維持）。
- **候補の差し替え**: 当初 `short_solo_magnitude_32` に根拠テーブルを追加したが、Gemini が「32倍を二回かける」の計算表現を修正必要と指摘。Aを優先して `short_solo_islands_kazu`（国土地理院の一次情報）に変更。両方の根拠テーブルは残すが、予約するのは islands のみ。
- **根拠の裏取り**: 国土地理院の報道発表（2023-02-28）を curl で取得し、6,852島・14,125島・測量技術による地図表現の詳細化・国際的な取り決めなし、の4点を本文で確認（`docs/research/20261120_islands_reviews.md`）。Python の urllib は SSL legacy renegotiation で失敗したため `curl -k` を使った。
- **ゲートと検査**: `check_short_evidence.py` は両方の spec で OK。`check_slots.py --days 60` で 1/11 12:00 の重複なしを確認。
- **予約操作**: 既存の非公開動画は再アップせず `yt_api.py schedule <video_id> "2027-01-11 12:00"` で予約。予約解除は `videos().update` の `publishAt=None`（`replace_shorts_cta.py` の実例を参考）。予約後に API から publishAt を読み戻して台帳も更新した。
- **未確認**: 元解像度・スマホ実機・人間の全編実聴。Gemini への動画添付はこの日も「ファイルを開けない」失敗が続いた。

## 実測：春分／秋分Shortの台本まで（2026-11-20）

- **手順書の再確認**: `procedure_gate` の印が24時間で切れていたため、`read_procedure.py` の全4部分と確認問題をやり直してから生成した。
- **生成器の拡張**: `solo_spec.build()` に `claims=` / `needs_research=` を追加（省略時は従来どおり）。`scenes[].claim_ids` は `dict(s, ...)` でそのまま保持される。旧ジェネレーターは無変更で動く。
- **ゲートの誤検知を修正**: `.ac.jp` をすべて「大学による再掲」と判定していたため、発行主体の国立天文台（`www.nao.ac.jp`）が「代替明記なし」で落ちた。再掲先を `web.archive.org` と `jahis.law.nagoya-u.ac.jp` の明示ホストに限定し、`.go.jp` / `.ac.jp` を一次発行主体として扱う回帰テストを追加（全12件OK）。
- **レビュー反映**: ChatGPTは公開可、Geminiは修正必要。共通指摘（2020年・東京の明示、35分8秒角が角度であること）を描画前に台本へ反映。`pron` に「三十五分八秒角」を登録。
- **未実施**: 背景生成・ビルド・Muse・予約。11/26のKPI判定待ち。

## 実測：春分／秋分Shortを投稿可まで（2026-11-20）

- **KPI判定を待たずに描画**: オーナーの「投稿可の状態まで」という指示で、11/26待ちの方針を変更して生成・ビルドを実施。
- **背景**: `& "C:\Program Files\Git\bin\bash.exe" scripts/fv_clips.sh equinox`。4本とも1回目で成功（ALL OK、約48分）。4コマを目視し、文字・人物・現代物がないことを確認。
- **ビルド**: PowerShellで `$env:PATH = 'E:\rekishikaisetu-honnoji\tools\ffmpeg\bin;' + $env:PATH` を設定してから `solo_ship.py build`。bashでの `export PATH` は子プロセスに渡らず `FileNotFoundError` になった（手順書どおりPowerShellを使う）。
- **Museの指摘**: 初回は画面下の出典行が左右に見切れていた。長い `src` と `sub` を「国立天文台FAQ（3-3）」「3月20日・東京／夜11時間52分」等に短縮して再ビルド→**公開可**。出典ラベルは画面では短く、完全なURLは概要欄に残す。
- **アップ**: `solo_schedule.py` はゲートを通してからアップする。`containsSyntheticMedia=True` はAPIで別途設定（Studioの現行UIにAI開示ラジオが出ないためUI確認不可）。タイトルの `#Shorts` 重複はAPIで修正。
- **公開状態**: `ZSRepHwe500` を2027-01-12 12:00に予約。台帳・`check_slots.py` で確認済み。
- **X予約**: `x_schedule.py --month 1 --day 12 --year 2027 --hour 12 --min 5 --ai` で12:05に予約。dry-runでアカウント・日時・URLを確認してから送信し、予約一覧で動画IDが1件だけであることを確認した。

## 実測：長尺予約の一括解除（2026-11-20）

- 対象は台帳キーが `^\d+_` の動画のうち、APIの `status.publishAt` が設定されているもの。+60日窓37件に対し全体では49件（60日超先の12件を含む）。
- `videos().update(part='status')` で `publishAt=None` を設定。`privacyStatus`・`selfDeclaredMadeForKids`・`embeddable`・`license`・`containsSyntheticMedia` は読み戻した値をそのまま渡し、他の設定は変えない。
- 49件すべて成功、失敗0。再読み取りで長尺の予約0件、Shorts 74件、重複なしを確認。
- 予約の付け替えはユーザー確認済み（「長尺動画の新規公開は一旦止めて」）。解禁時は台帳の動画IDから再予約する。

## 実測：空いた19:00枠の充填（2026-11-20）

- 台帳の `publishAt` は古いため、APIで `privacyStatus=private` かつ `publishAt` なしの在庫を洗い出した（44本。台帳だけの判定より少ない）。
- 13本を 11/21〜12/05 の19:00に予約。Tuesday〜Saturdayの連続する枠が埋まり、`check_slots.py` で同時刻の重複なし。
- 効果の判定は公開後。19:00は長尺時代の枠で、Shortsの平均視聴率が高いという小さなサンプル（4本・86%）を検証する。
- Xの紹介投稿はこの13本には入れていない（在庫の再予約のため、新作の手順をそのまま適用していない）。

## 実測：19:00枠 第2弾とX予約の大量投入（2026-11-20）

- 12/07〜12/26 に20本を予約。在庫31本のうち、根拠が二次情報に偏る2本を除外。
- X予約は `x_schedule.py` を20回連続実行。13件成功後、7件がアカウント確認不全／Confirm不在で失敗。**専用Chrome（CDP 9223）のプロセスを終了させてから再試行したところ7件すべて成功**。
- リロード再試行だけでは回復しない場合は、専用Chromeごと再起動するのが確実（メモリ節約でタブが休止した状態が残る）。
- 成功済みは再実行しないことで重複投稿を防止した（各スクリプトが予約一覧の動画ID件数=1を確認）。

## 実測：X予約の付け替え（2026-11-20）

- 予約済みX投稿の時刻変更は、予約一覧の該当ポストを開き、ダイアログ内の「Will send on …」をクリック → 月/日/年/時/分を `select_option` で設定 → 「Update」→ ダイアログの「Schedule」で保存する。Playwrightの通常クリックはオーバーレイに遮られるためJSクリックを使った。
- 保存後、予約一覧で動画IDが1件だけであることを確認（重複なし）。
- 同時にYouTube側も `yt_api.cmd_schedule` で公開時刻を変更し、台帳の `publishAt` をAPI読み戻し値で更新した。

## 実測：Google AI モードへのレビュー移行（2026-11-20）

- オーナー指示で、動画・台本のレビューを Muse から Google AI モード（https://www.google.com/ai）に変更。
- 追加指示（同日）: 台本レビューは **Google AI モード＋ChatGPT の併用**。動画レビューは Google AI モードのみ。Gemini は必須ではない。
- `scripts/google_ai_review.py` を追加。`--mode script` は spec から依頼文を自動生成、`--mode video` は動画を添付。CDP 9222 が無ければ自動起動し、送信ボタンが有効になるまで待つ。
- 実動確認: `solo_ambulance --mode script` で台本レビューを取得（`out/google_ai_review_solo_ambulance_script.txt`）。消防白書の数値・定義が一致すると判定。
- 過去の指摘で一次資料と食い違うもの（Gemini の「46.9% は軽症単体」）は不採用とし、採用判断を research に記録する運用を継続。

## ショートの作り方（2026-11-20 時点の標準手順）

1. **題材**: 既存タイトルと重複しないか確認し、一次資料（官公庁・大学・公的施設）で検証できる「身近な思い込み」を選ぶ。尺は30〜45秒。Ask Studioにも候補を聞いてよいが、数字は必ず原文照合する。
2. **根拠**: `curl -k` で一次ページ本文を取得し、使う数値・定義・日付を `evidence_note` に記録。未確認は `needs_research` に「なぜ答えが変わらないか」を添えて残す。
3. **台本**: `scripts/gen_solo_<slug>.py` を作り、`solo_spec.build(..., claims=..., needs_research=...)` を呼ぶ。`big` は12字以内、ナレーションは約150字。実行して spec と pron を生成。
4. **ゲート**: `python scripts/check_short_evidence.py data/short_solo_<slug>.json` が OK になるまで直す。
5. **背景**: FreeVideoは `& "C:\Program Files\Git\bash.exe" scripts/fv_clips.sh <slug>`（約35分）。`solo_spec.fv_prompts()` で台本に合うプロンプトを書き、生成後に各クリップのフレームを目視する。**既存クリップ流用は禁止**（救急車Shortで台風クリップを流用した事故あり）。概要欄と credit に「AI生成のイメージ」と書く。
6. **ビルド**: PowerShellで `$env:PATH = 'E:\rekishikaisetu-honnoji\tools\ffmpeg\bin;' + $env:PATH` を設定してから `python scripts/solo_ship.py build solo_<slug>`。
7. **機械検査**: `_kana.txt` 全文、loudnorm（−14 LUFS前後／TP −1.5 dBTP）、`_frames.png` の重なり・見切れ。
8. **レビュー**: 台本は **Google AI モード＋ChatGPT の併用**（`python scripts/google_ai_review.py <slug> --mode script` と `python scripts/review_short_cdp.py <slug> chatgpt`）。動画は **Google AI モードのみ**（同スクリプト `--mode video --video out/short_solo_<slug>.mp4`）。Muse・Geminiは必須ではない。AIの指摘は根拠原文と照合してから採用・不採用を決め、`docs/research/` に残す。
9. **アップ・予約**: `python scripts/solo_schedule.py solo_<slug> "YYYY-MM-DD HH:MM"`。その後 `containsSyntheticMedia=True` をAPI設定、タイトルの `#Shorts` 重複を修正、台帳の `publishAt` をAPI読み戻しで更新。
10. **X**: `python scripts/x_schedule.py --video <ID> --month M --day D --year YYYY --hour H --min M+5 --question "問い" --ai --tags "#… #寄り道ラボ"`。成功済みは再実行しない（重複防止）。Chromeが休止したら CDP 9223 のプロセスを再起動。
11. **公開後**: `check_published.py <key>` と Analytics／Ask Studio で効果を確認。台本レビュー・動画レビュー・通し再生・全編実聴・スマホ実機は別ゲートとして記録する。
12. **差し替え**: 動画ファイルは同じYouTube IDでは差し替えられない。新IDをアップし、旧IDは2027-01-01へ退避、X予約のURLも書き換えて「新ID1件・旧ID0件」を確認する（救急車Shortで実施）。


## AIレビュー指摘の照合と再描画（2026-11-22、baby_hone / baby_namida / fuji）

- **動画レビューの「字幕誤字」は実フレームで確認してから直す。** Google AI モードが「300本とゆ言い方」と指摘したのは、SRT は正しく、画面の折り返しが「300本という言い／方もありますが」だったため。該当時刻（13.5秒）の PNG と SRT を照合し、単語の途中で改行されない文に変更して再描画した。SRT だけ見て「指摘は誤り」と切り捨てると画面の読みやすさ問題を残す。
- **結論カードのタイミングはナレーションの1文目で決める。** 1文目が問いのときに `hook_card` を出すと、0:00〜0:01 で結論が先に出る。`solo_spec.build(..., hook_card=False)` を使う（`gen_solo_fuji.py` / `gen_solo_baby_namida.py` 参照）。
- **日付の読み上げは離脱要因になりうる。** 「2026年11月21日時点の情報です」を独立文で読むと不自然に間が空く。音声から削り、`scenes[].src` と概要欄に残すと情報は保てる（1yen レビューと同じ判断）。
- **Google AI モードの返答は途中で切れることがある。** スクリプトの既定は「回答が出た瞬間」に保存するので、長い回答は `stable>=4` まで待つ inline Playwright で取り直すと完全（fuji 台本レビューは1881文字→4103文字）。
- **ChatGPT（CDP 9222）が未ログインだと台本レビューは不成立。** ログイン画面のまま composer が無く、`review_short_cdp.py` は TargetClosed / fill timeout になる。その場合は「Google AI モードのみ完了、ChatGPT 未実施」と記録する（2026-11-22 実例）。
- 詳細と採否一覧は [`research/20261122_baby_fuji_reviews.md`](research/20261122_baby_fuji_reviews.md)。


## 雷と金属Shortの検証（2026-11-22、solo_thunder_metal）

- **出典の優先順位を台本で間違えない。** 気象庁は「まず安全な空間へ避難」、4mは「近くに安全な空間が無い場合」の保護範囲。台本に4mだけを出すと誤解になる（Google AIモード指摘を採用）。木は「全ての幹・枝・葉から2m以上」。
- **学会論文の結論は引用元のページまで確認する。** 「金属を外せ」は誤りで、論文p.56は「金属は身につけているほうが安全」。p.53のQ&Aだけ読むと「半分本当」と弱くなる。
- **AIの無音指摘は silencedetect で裏取りする。** 这次は「1.2秒」と言われたが実測0.398秒。レンダラの導入时长として不採用。
- **読み辞書はフルネームで登録する。** 「日本大気電気学会」は「日本気象学会」とは別語。`pron` に完全形を入れないと VOICEVOX が「にっぽん」と読む。
- 自作イラスト背景は `build()` 後に spec の `vid` を削り、`art` を差し替えて作れる（`gen_solo_thunder_metal.py` 参照）。AI映像を使わない場合でも「イメージ」と明記する。
- 詳細は [`research/20261122_thunder_metal_sources.md`](research/20261122_thunder_metal_sources.md)。


## REJECT対応：AIクリップ版への作り直し（2026-11-22、solo_thunder_metal_fv）

- オーナーREJECTの理由は「AIクリップを使っていない」。自作イラスト版（`out/short_solo_thunder_metal.mp4`）は消さず、同一台本・根拠で `scripts/gen_solo_thunder_metal_fv.py`（slug `thunder_metal_fv`）を作成。`solo_spec.build()` が各シーンに `vid=assets/<slug>/fv/clipN.mp4` を入れるので、自作版でやった `vid` 削除はしない。
- 背景プロンプトは `solo_spec.fv_prompts()` で「no people, no text, no buildings, no modern objects」を付与。5本を `bash scripts/fv_clips.sh thunder_metal_fv`（ComfyUI + FreeVideo/MiniMax H3、1本約9分）で生成し、生成直後に各クリップの代表フレームを目視して人物・文字・建造物がないことを確認した。**既存クリップの流用はしない**。
- 書き出し：`python scripts/solo_ship.py build solo_thunder_metal_fv`。出力 `out/short_solo_thunder_metal_fv.mp4` は 1080x1920 / 30fps / 60.43秒 / h264+AAC / 21.4MB。全フレームデコードはエラーなし、`silencedetect` の無音は冒頭0.398秒のみ（既知の導入）。
- AIクリップが実際に使われた証拠は、新旧動画の同じ時刻（4/15/28/40/53秒）のフレームを並べて確認した。自作版の雨のイラストに対し、FV版は積乱雲・金属球・枝と葦・撥水布の水滴・岩場と稲妻に変わっている。
- **概要欄の改行バグ**: `solo_spec.build()` が `notes + bg_note` をそのまま連結していたため、`notes` が改行で終わらないと「…と明示。・動画内の図…」と1行に結合された。`solo_spec.py` 側で不足時のみ `\n` を挿入するよう修正し（全genスクリプト共通）、generator を再実行して JSON を更新、`out/short_<slug>_description.md` と `upload/short_<slug>/description.txt` にも同じ改行を入れた（生成器だけ直しても既存パックは変わらない）。
- レビュー実行はシステム Python312（`.venv` に playwright / pip なし）。`scripts/google_ai_review.py` は回答が出た瞬間の本文を保存するため、途中経過（「AI モードが質問について考えています」）だけで終わることがある。そのため `google_ai_review.py` 本体を修正し、回答本文が3回連続で変わるまで待ってから保存するようにした（2026-11-22）。


## お試しアップロードとAPI環境（2026-11-22）

- 根拠テーブルが空のままオーナーから「お試しにアップロード」と指示されたときは、`solo_schedule.py` のゲートを迂回せず、その旨を research に記録したうえで `yt_api.py upload` → `videos().update(status.containsSyntheticMedia=True)` → `yt_api.py schedule` を手動で実行する。ゲート自体は緩めない。
- `containsSyntheticMedia` はAPI書き込み後も読み戻しが None になる（既知）。Studio の「AI を使用」ラジオは 2026-11-22 のUIでは見つからず、radio 確認は未実施と記録する。
- YouTube API 系スクリプトはシステム Python312 に `PYTHONPATH` で Python311 の site-packages を足して実行する（Python311 に python.exe が無い）。
- 予約前に `check_slots.py --days N` で実枠を確認し、アップ後にもう一度実行して重複なしを確認した。


## 説明欄から内部メモを除く（2026-11-22）

- `gen_solo_*.py` の `notes` にレビュー過程・不採用理由・未確認の調査ログを書き、そのまま `description.txt` に流れていた。公開説明欄に不要な内容（例：「Google AIモードの台本レビューで採用」「regarding 赤ちゃんの顔は不採用」「ChatGPTで直した点」）を削除した。
- 残すのは冒頭の問い、出典URL、必要な留保（二次資料・未確認の一文）、AI生成背景と図のクレジット、チャンネル紹介、ハッシュタグ。内部判断の詳細は `docs/research/` に残す。
- 投稿済み・予約済みでも、`videos().update(part='snippet')` で説明だけ差し替えられる。更新後に `status.publishAt` が変わっていないことを読み戻して確認した（3本とも維持）。


## 全動画の説明欄監査（2026-11-22）

- 公開済み・予約済みを含む全377本をAPI走査し、内部レビューメモが残っていた57本の説明欄を差し替えた。最終スキャンは該当0件。
- 共同部品 `solo_spec.public_notes()` が内部メモ行を除去する。`ChatGPT(OpenAI)による生成イラスト` などの正当なクレジット行は保持する。
- 動画IDと予約時刻は変更しない。`videos().update(part='snippet')` は `status.publishAt` を維持するが、更新後に読み戻して確認すること。


## 手順ゲートと背景生成の落とし穴（2026-11-22、water_2l）

- `scripts/read_procedure.py` の確認印は **24時間で失効**する。セッションをまたいで背景生成を始めると `fv_clips.sh` が「手順書を読み取り確認していません」で止まる。その場合は `read_procedure.py` → `--part 1..4` → `--questions` → `--answer ...` をやり直す。
- `fv_clips.sh` は `python scripts/solo_ship.py clips` を使っていたが、この環境の `python` は WindowsApps のスタブで、実際には何も生成せず「Python DONE」と出ていた。スクリプト内で `.venv/Scripts/python.exe` を優先するよう修正した。
- `fv_clips.sh` は Git Bash の `/e/...` パスを使うため、`C:\Program Files\Git\bin\bash.exe` の絶対パスで呼ぶ。

- `PYTHONPATH` がセッションから漏れていると、ComfyUI が Python311 の壊れた PIL を読んで起動失敗（`cannot import name '_imaging'`）し、`freevideo_batch.py` は `SERVER DOWN` で終わる。`fv_clips.sh` の先頭で `unset PYTHONPATH` するよう修正した（2026-11-22）。


## 味覚マップの根拠確認（2026-11-23、tongue_taste_map）

- 企画3案（味覚マップ／110番・119番／雲の重さ）のうち、冒頭の引き込みが strongest な味覚マップを先に選んだ。根拠は `shorts/tongue_taste_map/brief.yaml` と `result.json`。`brief-check` と `check` は通るが `status=needs_review` のまま（台本レビュー・音声・スマホ確認は未実施）。
- 一次資料は Spence 2022 の総説（PMC8956797）。要旨・Highlights・1節で、各基本味の受容体は舌全体に分布し「舌の地図」は長く否定されていると確認。ただし同じ総説が、場所ごとの感度差は小さいが有意だとも書く。**「地図は誤り」と「差はゼロではない」の両方を入れないと、知的な納得感が出ず誤断言にもなる**。
- 日本語の根拠として市民研通信第62号（2021年5月10日）のPDF本文も取得。`web_fetch` は PDF 非対応なので PowerShell で取得し、`Python312\python.exe` の `fitz` で UTF-8 テキストに落として読んだ。47〜48行目に「味の感覚は舌全体に広がり、差は非常にわずか」、76〜84行目に「1942年のボーリングの本だけで広まったとするのは不十分」とある。ここを単線の「誤訳で広まった」物語に単純化しない。
- この環境では `python` が WindowsApps のスタブで、PDF 抽出や `shorts_standard.py` は `C:\Users\neoen\AppData\Local\Programs\Python\Python312\python.exe` を明示して実行する。`PYTHONUTF8=1` を付けると日本語の文字化けを避けられる。
- `shorts_standard.py check` の WARN は、1秒あたり文字数（4.0〜5.5）・疑問形・模式図の明記・claim_ids で細かく出る。39秒なら全体で約160〜210文字。初稿は約305文字で全シーンが速すぎたため、約3分の1を削って PASS にした。
- 単独Short化（57.6秒・4場面）後、Google AIモードとChatGPTの両方で台本レビュー、Google AIモードで動画レビューを行い、いずれも「公開可」。動画は CDP 9222 が塞がっていたため、**9223 の automation プロファイルで Playwright の `set_input_files` を使ったら動画添付に成功**した。bsk の upload は hidden input に `Not allowed` で失敗（手順書どおり）。
- VOICEVOX はカタカナ「ヘーニッヒ」を audio_query で `エ'エ/ニッヒ'` と読む。ひらがな「へえにっひ」なら `ヘエニッ'/ヒ'` になる。**字幕はカタカナ「ヘーニッヒ」、発音辞書は `ヘーニッヒ: へえにっひ`** とすると両方を満たせる。kana ファイルで `ヘエニッ'/ヒ'ガ` を確認すること。
- `solo_spec.build` に `claims` と `needs_research` を渡しても、`needs_research` に「答えは変わらない」という語が無いと root の根拠テーブルゲートが ERROR になる。各項目にその一文を入れること。
- 予約枠の事前確認で 11/24 12:00 が空きと見落とし、既存 `short_solo_kotatsu` と重複した。**`check_slots.py` の出力は最後まで読み、予約後にもう一度実行して重複なしを確認する**。今回は今回の動画だけを 11/25 11:00 に移動（`yt_api.py schedule <id> "2026-11-25 11:00"`）。
- X の予約時刻変更は UI のクリックが `#layers` に遮られる。次の手順で保存できた: (1) 予約一覧の対象投稿をクリックして編集モーダルを開く, (2) `document.querySelector('[role=dialog] [data-testid="scheduledTweetIndicator"]').click()` を JS で実行, (3) `#SELECTOR_1..5` を 11/25 11:05 に設定して change イベント, (4) `[data-testid="scheduledConfirmationPrimaryAction"]` をクリック, (5) 最後に編集モーダルの `[data-testid="tweetButton"]` を JS click で押す。`Update` だけでは保存されない。再読み込みして予約一覧で確認すること。
- `scripts/google_ai_review.py` の動画モードを厳格化した（2026-11-23）。`VIDEO_QUESTION` で「字幕の表記そのものの違和感」を音声の読みと別に評価させ、時刻と修正候補を要求する。旧版のひらがな字幕をレビューさせて「へえにっひ」の指摘が出ることを確認済み。あわせて、動画モードが既存タブを再利用して別動画をレビューするバグを直し（常に新規タブ＋添付）、CDP ポートは `GOOGLE_AI_CDP_PORT` で指定可能にした（9222 が塞がっていても 9223 を使える）。
- 発音辞書は値を逆に書きがち（2026-11-24 `baby_taste` で `苦味: クミ / 甘味: カンミ` と登録してしまった）。味覚系の語は `甘味: アマミ / 苦味: ニガミ` が正しい。`--kana` で全文を目で確認し、動画レビューでも「読み間違いなし」と言われるまで確かめること。
- VOICEVOX はセッションをまたぐと停止していることがある。ビルド前に `http://127.0.0.1:50021/version` を確認し、止まっていれば `E:\rekishikaisetu-honnoji\tools\voicevox\windows-cpu\run.exe` を起動する。

## 既存ShortをFreeVideo背景に作り直す（2026-11-24、lightning_fv）

- 既存の `data/short_<slug>.json` は `art` に自作静止画を指定する古い形式。`scenes[].vid` に `assets/<slug>/fv/clipN.mp4` を入れると、`ytcore/make_short2.py` の `frame_at()` が `vid` を優先して動画背景にする。`art` は残していても描画されないが、混乱を避けるなら削除する。元の JSON は触らず別名の spec にコピーして作り直す。
- **同じ動画IDの映像は差し替えられない**。YouTube 公式ヘルプ（https://support.google.com/youtube/answer/55770）に明記。bsk で Studio の編集画面を開いても差し替え UI は無い。反映するなら新規IDでアップし、旧IDは残すか退避する。
- 元 spec に `claims` が無い祖父化データでも、別名の新規 spec は根拠テーブルゲートに通らない。`docs/themes/<theme>/08_fact_check.md` の原文確認結果から `claims[]` を埋め、`needs_research` の各項目に文字列「答えは変わらない」を入れる。
- `check_short_evidence.py` は `www.weather.gov`（米国立気象局の公式ドメイン）を「公式ドメイン外」として WARN にする。`.go.jp` / `.ac.jp` の誤検知と同じ種類。原文が確認できていれば WARN は内容確認済みとして不採用でよい。
- FreeVideo のプロンプトは「写したくない物の名前を書く」と逆効果になる。時計塔の文字、街の電線・アンテナ、三輪車のナンバーが実際に出た。**見せたい物だけを書き、文字が出る物は場面ごと別の物に置き換える**のが確実（時計塔→何もない平原の雨雲と稲妻）。1本約10分、作り直し3回で計6本。
- Studio の「すべて表示」ボタンは表示テキストではなく `aria-label="詳細設定を表示"` で探す。`button[aria-label="詳細設定を表示"]` をクリックすると `tp-yt-paper-radio-button[name=VIDEO_HAS_ALTERED_CONTENT_YES]` が現れる。`ai_assistant` 設定の読み戻しは `aria-checked` で確認する。
- bsk のデーモンはこの宿主では detached 起動できず、`bsk daemon start --foreground` を永続ターミナルで起動してから `BSK_AUTO_START=0` でクライアントを使う。Studio 操作はログイン済みの `.chrome-automation` プロファイル（CDP 9222）を使う。未ログインの bsk セッションで開くとチャンネル作成画面に飛ぶ。
- 予約枠は台帳ではなく `check_slots.py` の API 実測で選ぶ。11/25〜12/02 は 12:00・17:00・19:00 がほぼ毎日埋まっており、原則枠が空くまで待つより、1日6〜8本の上限内で空いている時刻（今回は 11/25 15:00）を使う。
- 音量の数値を報告するときは、**どの動画の ffprobe/loudnorm 出力か**を必ず添える。この作業で `-14.0 LUFS / -1.4 dBTP` を Short の値として報告したが、`out/codex/lightning_watch.log` の長尺 lightning（166.3秒）の値と同じで、Short 側に記録が無いと指摘された。Short 版を再実測したところ 47.133秒・`-14.0 LUFS / -1.4 dBTP / LRA 2.2 LU` で数値自体は一致した。再実測コマンド: `ffmpeg -i out/short_lightning_fv.mp4 -af loudnorm=print_format=summary -vn -f null -`。
