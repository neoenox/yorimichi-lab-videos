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
- 適用例: younkaku（明治の浅草12階）は、場面1の冒頭2文で問いと答え、直後に「1890年11月」「8階まで」の数字を置いた。

**3. 未予約のShorts在庫は「既出題材の別版」が多い**
- 未予約・非公開で40〜70秒のShortsは**94本**あるが、タイトルを見るかぎり既出題材の別版（_nl など）が多い。
- 薄い日（11/19・11/20）を埋めるとき、在庫をそのまま出すと**同じ題材の再掲**になりやすい。**新作を薄い日に置く方が安全**（11/19 19:00 に younkaku を置いた）。

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

**3. Museの添付確認は、ファイル名ではなく動画のblobで判定する（2026-11-18）**
- Museは添付ファイル名を本文に出さず、サムネイル（`<video src="blob:...">`）だけを出す。
- 旧 `muse_review.py` は `body.innerText` にファイル名が含まれるかで判定していたため、実際に添付済みでも「添付NG」で止まった（nengaで発生）。
- 添付前後の `video` の `currentSrc` を比べ、新しいblobが増えたら成功とする。ファイル名が無いときの再添付はしない（二重添付を防ぐ）。
