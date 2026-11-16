# 単独Shortの作成・公開・宣伝の手順(2026-11-16 時点)

「寄り道ラボ」の単独Short(約50〜55秒)を、題材選びから、公開後の確認まで進める手順。2026年11月9〜16日に確立した流れ。**他のエージェントが、同じ品質の動画を作れること**を目的に、判断基準・実際の操作・失敗例まで書いてある。
作業場所は `E:\rekishikaisetu-honnoji`(scripts・data・assets・out・upload・cache)。確認用の画像と動画は `E:\rekishikaisetu\sigcmp_view` に置く。

**読み取り確認(強制の仕組み。2026-11-16 追加)**: この手順書は、`python scripts/read_procedure.py`(`E:\rekishikaisetu-honnoji` で実行)で**全部分を表示して読み、確認問題(`docs/SOLO_SHORT_QUIZ.md`)に全問正解**しないと、台本生成・ビルド・アップ・予約が止まる(`scripts/procedure_gate.py`。印は24時間有効で、この手順書を直すと無効になる)。Claude Code では、`.claude/settings.json` の PreToolUse フックが、印なしの該当コマンドを拒否する。**手順書を直したら、確認問題の答えが変わっていないか `SOLO_SHORT_QUIZ.md` も見直す**。印の偽造・`PROCEDURE_ACK_SKIP=1` での回避はしない。

**まず読む順番**: ①`AGENTS.md` ②`docs/VIDEO_CREATION_PRECHECK.md`(全文) ③この文書の 0〜0b(流れと合格基準) ④作る題材の型に近い**完成例の台本ファイル**(15章) ⑤12章の罠の一覧。
**完成例の台本は、書き写して直すのが最短**(`scripts/gen_solo_news_planimal.py`=ニュース、`gen_solo_yutanpo.py`と`gen_solo_kotatsu.py`=江戸の暮らし、`gen_solo_tokusei.py`=歴史、`gen_solo_minatomirai.py`=地図型)。

> 動画を作る前に `docs/VIDEO_CREATION_PRECHECK.md` を全文読む(AGENTS.md の決まり)。ショートには背景画像を必ず使い、AI映像は「イメージです」と明示する。

## 0. 全体の流れと、役割分担

| 段階 | 内容 | 道具 |
|---|---|---|
| 1 | 題材と根拠(一次情報) | curl、WebSearch、Wikipedia REST |
| 2 | 台本ファイル `gen_solo_<slug>.py` | `solo_spec.build` |
| 2b | 台本を ChatGPT と Gemini でレビュー → 合わせる | Chrome(Claude in Chrome) |
| 3 | 背景(地図型=国土地理院の写真、それ以外=FreeVideoのAI映像) | `gsi_clip.py`、`fv_clips.sh` |
| 4 | ビルドと機械検査 | `solo_ship.py build`、ffmpeg |
| 5 | 読みの検証(kana全文+手元ASR) | `asr_kotoba.py` |
| 6 | Muse で動画をレビュー(「公開可」が出るまで) | Chrome |
| 7 | 非公開アップ+公開予約+AI使用+台帳 | `solo_schedule.py`、YouTube API |
| 8 | Xの紹介投稿を予約 | Playwright(専用ブラウザ) |
| 9 | 公開後の確認と分析 | YouTube API、Studio の Ask Studio |
| 10 | 記録(メモリ・この手順書) | — |

**レビューの役割分担**: 台本=ChatGPT と Gemini(作る前)、動画=Muse(ビルド後)。ChatGPT・Gemini・Muse の指摘は、すべて**裏取りしてから**反映する(指摘が引く資料は、自分で読むまで根拠にしない)。

## 0b. 合格基準(すべて満たすまで、公開予約しない)

| 項目 | 基準 | 確認のしかた |
|---|---|---|
| 長さ | 50〜58秒(目標55秒)。58秒を超えたら削る。62秒は長すぎ | `solo_ship.py build` の出力 |
| ナレーション | 4場面+終わりの画面。約230字 | 台本ファイル |
| 冒頭 | 問いか数字で始め、**答えを先に出す**。結論カードも同時に出る | 台本・`_frames.png` 1コマ目 |
| 年月日 | ニュース系は、画面・図・ナレーション・説明欄・タイトルのすべてを年月日で(「2026年11月12日」)。末尾に「〇年〇月〇日時点の情報です」 | `solo_ship` が「年なしの日付」を警告する |
| 根拠 | 一次情報、または原文を読んだ二次資料。説明欄 `notes` に「確認日・URL・使った事実・使わなかった事実・言い過ぎを避けた点・未確認・レビューで直した点」 | 台本ファイル |
| 言い過ぎ | 出典の文型(「とされる」)を保つ。誤解を生む結論は書かない(「光合成する細胞ができた」と思わせない) | ChatGPTのレビュー+自分の確認 |
| 背景 | AI映像4本。文字・額・紋・刻印・電線・人物なし。「イメージです」を概要欄に。地図型は国土地理院の写真 | 4コマを並べて目で見る |
| 画面 | 重なり・はみ出し・折り返しなし。大見出し12字以内。比較カードの右値は短く(長いと枠から出る) | `_frames.png` |
| 音量 | -14 LUFS前後、ピーク -1.0〜-1.5 dBTP、0.8秒以上の無音なし(末尾を除く) | ffmpeg(6章) |
| 読み | kana全文を目で確認+ASRで数字・日付が一致 | `_kana.txt`、`asr_kotoba.py` |
| レビュー | 台本=ChatGPT+Gemini(背景生成の前)、動画=Muse「公開可」 | 4章・7章 |
| **メタデータ** | `title.txt`・`description.txt`・**`tags.txt`が題材に合っている**(前の動画のタグが入る罠。台本ファイルの `tags=[...]` で指定。2026-11-16に実際に発生) | `upload/short_solo_<slug>/` を開く、アップ後はAPIで読む |
| アップ後 | AI注記「はい」をStudioで確認、台帳に `publishAt`、Xの予約、メモリ | 8〜11章 |
| 報告 | 「確認した範囲」と「未確認」を分けて書く。生成・デコードに成功しただけで「公開品質」と言わない | AGENTS.md |

## 1. 方針(数字で確かめた決まり)

- **尺は50〜55秒、ナレーションは約230字**。登録者を多く得た動画は50〜60秒で平均視聴率100%前後。79〜82秒は58〜74%(Ask Studio、2026-11-15)。冬至72秒・みなとみらい66秒は長すぎた。長い台本は、まず削る。
- **冒頭の1文は、問いか数字。答えを先に出す**(結論カードも同時に出る)。答えを引き延ばす案は採らない。「〜でしょうか」より、短い問い。
- **終わりの問い(`end_q`)は、誰でも一言で返せるもの**(例:「皆さんの家では、こたつを、いつ出しますか？」)。ニュースの中身を問う、正解のある質問にはしない。
- **題材の優先**: 天文・科学のニュースと歴史の新発見 > 江戸の暮らし×数字で確かめる・一般の確かめる型 > 季節の風習 > 地図型(新規は優先度を下げる。同じ条件で比べると、地図型の中央値は約199回で他の型の215回と大差ない)。専門的・抽象的な題材は避ける(身近なものを優先)。
- **時事ニュースの日付は、画面・図・ナレーション・説明欄・タイトルのすべてで年月日**(「2026年11月15日時点の情報」)。ニュース以外の暦の話は、気候値などを除いて、できるだけ年も入れる。
- **1日に公開する本数は6〜8本まで**(予約と合算)。1日10本を超えると、後半の動画がほぼ再生0になる仮説がある。
- **比較は、同じ期間・同じ条件でそろえる**(伸びた時期を混ぜると、判断を誤る。2026-11-14に、地図型を「不調」と判断し、翌日に訂正した)。
- 精度より本数と速さを優先してよいが、明確な誤断言・中傷・確認できない数字の断定は避ける。確認できない点は、概要欄に「未確認」と書く。
- 新作を作る前に、**公開済みの全タイトルとの重複を照合する**(提案された題材が既出だった例がある)。

## 2. 題材と根拠

- 根拠は一次情報(内閣府、国立天文台 暦要項、気象庁、官公庁のページ)を優先。次に日本語版Wikipediaの原文(二次資料)。
- 公式ページは `curl` で直接取得する(検索ツールは「今日の発表」に弱い)。Shift-JISのページは `decode('cp932')`。取得した本文は UTF-8 のファイルに書き出して Read で読む。
- Wikipedia: `https://ja.wikipedia.org/api/rest_v1/page/html/<パーセントエンコードした記事名>`(User-Agent を付ける)。タグを落として読む。記事が短いスタブで返ったら、別の一次ページを探す。
- 国立天文台の暦: `https://eco.mtk.nao.ac.jp/koyomi/yoko/<年>/rekiyou26x.html`(東京の日出入=x4、二十四節気=x2。前年・翌年は別ページ)。表は10日ごとなので、最も早い日・遅い日を1日に特定しない。
- 内閣府「国民の祝日について」`https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html`、制定の経緯 `.../gaiyou/kaku/keii.html`。
- 国土地理院の住所検索で座標を取る(地図型): `https://msearch.gsi.go.jp/address-search/AddressSearch?q=<地名>`(経度,緯度の順)。
- 確認が難しいもの(有料書籍・論文・紙資料)は深追いしない。未確認と明記して進める。
- **言い過ぎを避ける**: 出典の文型(「とされる」「考えられる」)をそのまま使う。「最も早い」「初めて」は、記録期間を確認してから。旧暦の日付は、今の日付に単純に換算しない。

### 2b. ニュース題材の探し方(今日の題材が決まらないとき。2026-11-16 のプラニマル細胞の実例)

1. **公式の新着一覧を直接読む**: JST `https://www.jst.go.jp/pr/index.html`(日付・見出しの一覧が `get_page_text` で読める。個別ページのURLは `[...document.querySelectorAll('a')].filter(a=>/キーワード/.test(a.textContent)).map(a=>a.href)` で取る → `/pr/announce/<日付>-<n>/index.html`)。国立天文台、JAXA、理研、気象庁も同様。東北大のサイトは403で読めない。**WebSearchは新着に弱い**(国立天文台の最新が2か月前と出るなど)。
2. **決まらなければ ChatGPT に聞く**(ユーザー指示: 「題材探しはChatGPTに聞いて」)。依頼文: 「〈日付〉に公開する、60秒以内の日本語YouTube Short(雑学・科学・歴史)の題材を5つ提案してください。条件:(1)ここ数日に日本の公的機関・大学・研究機関が発表した新しい科学・天文・歴史の発見ニュース、または今週〜来週の暦・天文現象を優先。(2)冒頭を『問い+答え』にできる身近な話題。(3)各案に、根拠となる一次情報(発表機関名・発表日・URL)を必ず付ける。確実でないものは『未確認』と書く。(4)すでに扱った題材は除外:〈既出のリスト〉」。江戸の暮らしなら「テーマは〜、既出は〜、各案に一次または公的・博物館系の根拠、言い過ぎを避ける注意点」を足す。
3. **ChatGPTの候補は、裏取りしてから使う**。実績: 5案のうち、JSTの一覧で確認できたのは2案(プラニマル細胞、核の軟らかさ)。東北大の結晶(1T-TaS2)は確認できず、木津川の聖牛は検索に出なかったので使わなかった。「江戸の炭は332文」「1486年の蔗軒日録」も確認できず、後者は資料と食い違った(資料館通信は1484年)。**確認できた1案だけで進める**。
4. 個別ページ本文を読み、**PDF資料は必ず開く**。`curl -sL -o p.pdf <URL>` → `PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python -W ignore -c "import fitz; print('\n'.join(p.get_text() for p in fitz.open('p.pdf')))"`(PowerShellやcp932の画面に出すと文字化けする。`fitz`の警告は無視)。**文字が取れない画像PDF**(自治体の「資料館通信」など)は、`fitz` でページをPNGにして `Read` で目で読む(`p.get_pixmap(dpi=110).save('x.png')`)。
5. ChatGPTが引く細部(例:「藻類の遺伝子の95%以上が働いていない」)は、**PDFで原文を確かめてから**採る。確かめられた数字は動画の見どころになる。
6. 題材の選び方: 身近で絵にしやすいもの > 専門的なもの。専門語は言い換える(染色体=遺伝子の入れ物 などは、画面のカードで補う)。**誤解を生む結論は避け、「まだ先」「段階」を入れる**。
7. 暮らし・風習の題材(江戸の湯たんぽなど)は、**自治体の資料館・博物館の資料**を探す(Wikipediaの脚注から辿る。例: ふじみ野市立資料館「資料館通信」第71号)。**Wikipediaにある文でも、出典で確認できない部分は使わない**(「江戸の湯たんぽは庶民には使えなかった」はWikipediaにあるが、資料館通信には無かったので言わなかった)。
8. 確認できない題材(有料書籍・論文)は深追いせず、**確認できる範囲だけで構成**し、未確認を説明欄に書く(徳政令の「1割」は二次資料のみ → 「とされます」)。

## 3. 台本ファイル

- `scripts/gen_solo_<名前>.py`(雛形: `gen_solo_toji.py`、`gen_solo_kotatsu.py`、地図型は `gen_solo_minatomirai.py`)。`solo_spec.build(slug, title, head, answer, pron, scenes, bg_plan, notes, bg_note, credit, end_q=...)` を呼ぶ。
- scenes は4場面。各場面: `text`(ナレーション)、`big`(大見出し)、`sub`、`src`(出典表示)、`viz`(`T(間隔,[(ラベル,本文),...])` か `dict(type='compare',...)`)。
- **大見出し `big` は12字以内**(折り返して最初のカードに重なる。「江戸の人はこたつで冬を越した？」は2行になって重なった)。カードの文は14〜15字以内。年は見出しやラベルに移し、値を短くする。
- **数字・日付は画面では漢数字を算用数字に自動変換する**(「三十日そば」→「30日そば」と表示されて読めなくなる)。読みが問題になる語は、ひらがなで書く(「みそかそば」)。
- `pron`(読み辞書)に固有名詞・難読語を登録する。**ナレーションの全文を kana ファイルで読む**と、辞書の漏れが分かる。例: 勅令=チョクレイ(登録しないと「ミコトノリレイ」)、「閉鎖されました」まで登録(「ヘ→エ」の誤処理)。
- 見出し・文字から読点「、」は自動で消える。ナレーション中の読点は、間(ポーズ)になる。
- `notes`(説明欄)に、根拠のURLと確認日、使った事実、使わなかった事実、**言い過ぎを避けた点**、未確認、レビューで直した点を書く。
- 日本語は **直接書く**。`\uXXXX` で書くと、似た字に化ける(塀→塵、晦→晩、東→室、炊→烊、霜→霼)。ヒアドキュメントで文字列に `\n` を入れると本物の改行になり、構文エラーになる → 文字列の編集は **Edit ツール**で行う。
- **`tags=[...]` を必ず渡す**(2026-11-16に追加。無いと、`solo_ship` が長尺 `43_bukka`(物価)のタグを引き継ぎ、無関係なタグ「物価・家計・総務省」が付く。プラニマルで実際に発生し、アップ後にAPIで直した)。題材語・機関名・分野・`Shorts` を8〜10個。
- 図(`viz`)は4種類: `T(間隔,[(ラベル,本文),...])`(3項目の縦並び)、`dict(type='compare', l_label=, l_val=, r_label=, r_val=)`(左右比較。**値は短く**。長いと右が枠からはみ出す)、`dict(type='bars', items=[dict(label=,value=,text=,color=(r,g,b))])`(棒)、`dict(type='flow', hub=, mid=[...], leaf=)`(流れ図)。年表・比較・棒・流れ図は自作してよい(絵のイラストは作らない)。
- 実行: `PYTHONUTF8=1 python scripts/gen_solo_<名前>.py` → `data/short_solo_<slug>.json`、`data/<slug>_pron.json`、`E:\rekishikaisetu\out\script_solo_<slug>.txt`(レビュー用テキスト)、`assets/<slug>/fv/prompts.json`(AI映像の指示文)ができる。

### 3b. 台本ファイルの雛形(`scripts/gen_solo_news_planimal.py` を縮めたもの)

```python
"""単独Short：〈題材〉(solo_<slug>)。根拠は〈出典名〉(〈発表日〉、〈確認日〉に原文を確認 〈URL〉)。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
from solo_spec import build, T, fv_prompts
W = 'JST共同発表(2026年11月12日)'                       # 画面の出典表示(長すぎない)
pron = {'藻類': 'ソウルイ', '染色体': 'センショクタイ'}      # 難読語・同音語。kana全文を読んで足していく
scenes = [   # 4場面。text=ナレーション、big=大見出し(12字以内)、sub=小見出し、viz=図
    dict(text='〈問い〉？ 答えは、〈答え〉。2026年11月12日、〈発表者〉が発表しました。',
         big='〈12字以内〉', sub='〈発表者〉が2026年11月12日に発表', src=W,
         viz=T(2.6, [('発表', '〜'), ('発表日', '2026年11月12日'), ('論文', '〜')])),
    dict(text='〈中身1〉', big='〜', sub='〜', src=W, viz=T(2.8, [('材料', '〜'), ('結果', '〜'), ('名前', '〜')])),
    dict(text='〈中身2(数字)〉', big='〜', sub='〜', src=W, viz=dict(type='compare', l_label='分裂', l_val='150世代以上', r_label='働かない遺伝子', r_val='95％以上')),
    dict(text='〈限界・まだ先〉。2026年11月16日時点の情報です。', big='〜', sub='〜', src=W, viz=T(2.8, [('期待', '〜'), ('今回', '〜'), ('注意', '〜')])),
]
bg = ['場面1の映像の説明(人物なし・文字なし)', '場面2…', '場面3…', '場面4…']   # 日本語の計画メモ。実際の指示文は fv_prompts(英語)
notes = ('■ 〈確認日〉に、〈出典〉(〈URL〉)の原文とPDFを読んで作った整理です。〈確認日〉時点の情報です。\n'
         '・発表者/論文：…\n・主な内容(同)：…\n・言い過ぎを避けた点：…\n・レビューで直した点：…\n・動画では使っていないこと：…\n・未確認：…\n')
if __name__ == '__main__':
    build('<slug>', '【2026年11月12日発表】〈題名〉 〈短い副題〉', '〈画面上部の見出し〉', '〈結論カードの文〉', pron, scenes, bg, notes,
          bg_note='・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の〜の映像ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の〜の映像ではありません\n・図・表：自作',
          end_q='皆さんは、〜ですか？', tags=['題材語', '機関名', '分野', '雑学', 'Shorts'])
    fv_prompts('<slug>', ['英語の指示文1', '2', '3', '4'], allow_buildings=False)   # 江戸・建物が主役なら allow_buildings=True
```

- 題名(`title`)は `〜 約58秒で整理 #Shorts` の形で自動で整う。ニュースは先頭に【年月日】。長いときは `head`(画面上部)だけ短くする。
- `end_q` は、見た人が一言で返せる問い。`solo_spec` が「出典は、説明欄にまとめています。チャンネル登録も、お願いします。」を後ろに足す。
- 英語の指示文は、**見せたい物・動き・カメラ**だけを書く(5-2)。共通の末尾(人物・文字なし)は自動で付く。

## 4. 台本を ChatGPT と Gemini でレビューする(2b。背景生成の前)

### 4-1 依頼文(1行にまとめる)
「YouTube Shorts(約50秒)の台本をレビューしてください。題材は〈…〉です。根拠は〈出典〉で、〈確認した範囲と未確認〉。台本は次のとおりです。【場面1】…【終わりの問い】… 見てほしい点は、(1)言い過ぎ・誤解を招く断言 (2)冒頭の問いと答えの引き (3)耳で聞いて分かりにくい言い回し・読み間違えそうな語 (4)終わりの問いが適切か (5)公開してよいか。具体的な修正案つきでお願いします。」
改行入りの長文は、最初の段落だけ送信されることがあるので、1行にする。

### 4-2 Chrome(Claude in Chrome)での操作
- `tabs_context_mcp`(createIfEmpty)でタブを取る。**拡張機能が数時間つながらないことがある** → ユーザーにサイドパネルの再接続を頼む。タブがグループから外れたら、取り直す。`browser_batch` で複数操作をまとめる。
- **座標は、直前のスクリーンショットの枠(例 1568×744 や 1568×698)で指定する**。枠が変わると「outside the coordinate frame」になる。
- ChatGPT(`https://chatgpt.com/`): 入力欄をクリック → `type` → 送信。**送信ボタンは `[...document.querySelectorAll('button')].find(x=>x.getAttribute('aria-label')==='送信').click()` が確実**。ページが重く、screenshot が30秒でタイムアウトすることがある(JSの待機も45秒が限度。短く区切る)。返答は `document.querySelector('main').innerText` を「総合評価」から読む(長いので、`slice` で区切って複数回読む)。
- Gemini(`https://gemini.google.com/app`): 入力欄(スクリーンショットで位置を見る。1568×744で約(820,372))をクリック → `type` → `Return` キー。**送信されなかったら(ページが「何から始めますか？」のまま)、クリックからやり直す**。返答は `document.body.innerText` の「Gemini の回答」以降を読む。固まったらタブを閉じて開き直す。
- **背景(ComfyUI)を生成している間は、Chromeが重くなる**: `screenshot` が30秒でタイムアウト、`type` が30秒でタイムアウトすることがある。`get_page_text` やJSで読む。画面が「思考」のまま進まなければ、**再読み込みして送り直す(会話が消えていることがある。履歴は残らない前提)**。`browser_batch` で「クリック→入力→送信→待つ」を1回にまとめると、往復が減る。
- ChatGPTの返答には、広告・関連候補が混ざる。評価の本文(「修正すべき点」など)だけを読む。「思考」の表示が続くときは1〜3分かかる。
- **レビューが終わったタブは、その場で閉じる**(2026-11-16 ユーザー指示)。レビュー用に自分で開いたタブ(ChatGPT・Gemini など)を開いたままにするとメモリを食い、背景生成(ComfyUI)のRAM不足やChromeのタイムアウトの原因になる。**閉じてよいのは、自分で開いたレビュー用のタブだけ**。Gmail・カレンダー・X・YouTube Studio など、ユーザーが使っているタブは閉じない。
- **Muse はタブグループでは呼べない**(2026-11-16 実測)。拡張機能のブラウザからは `input[type=file]` にファイルを渡せず(`browser_type` は `E:\...` も `file:///E:/...` も失敗)、ページ内JSでローカル動画を `fetch` する方法も **CSP** で遮断される。DSHの公式プラグインにも添付機能は無い。Muse は `python scripts/muse_review.py <slug> --video out/short_solo_<slug>.mp4` で、専用プロファイル(`.chrome-automation`、CDP 9222)のChromeを使う。
  - **ユーザーの判断(2026-11-16)**: 別ウィンドウは許容。ただし**終わったら自動で閉じる**こと(窓を残さない)。`muse_review.py` は `close_launched()`(atexit)で、**自分が起動したChromeだけ**を閉じる(ユーザーのChromeには触らない)。X用の `scripts/x_schedule.py` にも同じ自動クローズを入れた。`--dry-run` で「起動 → 終了 → 残り0」を確認済み。

### 4-3 合わせ方
- 史実の一般化・裏取りは ChatGPT を優先。Gemini は甘く、出典にない断言をすることがある。Gemini からは、同音語の補足・テンポ・コメントを呼ぶ問いの案を取り入れる。
- **採らないもの**: 冒頭で答えを隠す案(答え先出しの方針)、出典で確認できない文言(「新たに設けられた」など)、旧暦↔新暦の単純な換算、自分で読んでいない資料にもとづく訂正。
- よく出る指摘: 断定を弱める(「〜とされています」)/同音語(祭祀→行事)/数字の羅列は耳で追えない(ナレーションから外して画面のカードへ)/「記録」の重複/年号に時代名を添える。
- **実際に反映した指摘・しなかった指摘(2026-11-16)**:

| 指摘 | 判断 | 理由 |
|---|---|---|
| 「DNAをまるごと入れた」は実験(細胞融合)と合わない | 採用 | 原文は細胞融合 |
| 「一緒に生き続けた」では何が生きたか曖昧 | 採用→「藻類のDNAを持つ細胞ができた」 | 事実に沿う |
| 「遺伝子の95%以上が沈黙」を入れよ | 採用(PDFで確認) | 見どころで、誤解も防ぐ |
| 「沈黙」は耳で擬人化に聞こえる(Gemini) | 採用→「ほとんど働いていません」 | 耳で分かる |
| 「俳諧」は「徘徊」と同音(Gemini) | 採用→「冬の季語にもなりました」 | 同音語は避ける |
| 「債権」は「財政再建」の「再建」と同音(Gemini) | 採用→「取り立て」「財政を立て直す」 | 同じ動画内の同音衝突 |
| 「出しました」は貨幣を出したように聞こえる | 採用→「設けました」 | 誤解を避ける |
| 「中国から伝わった」は断定が強い | 採用→「伝わったとされます」 | 出典の文型 |
| 湯たんぽ「1486年」(ChatGPT) | **不採用**(資料は1484年) | 自分で原文を読んだ |
| 「ワカメやミドリムシ」の例示(Gemini) | **不採用** | 確認できない例 |
| 末尾の「〇年〇月〇日時点の情報です」は余韻を削る(Gemini) | **不採用** | 年月日ルールが優先 |
| 冒頭は意外性のある言い方に(Gemini) | 軽く参考 | 方針は「問い+答え先出し」 |
| 「とされます」の連続(Gemini) | 一部採用(連続を減らす) | 断定を弱める箇所は残す |

- 直したら台本を再生成し、**ナレーションを削って50〜55秒に収める**(削ると事実を落としやすいので、レビューで確認した言い回しは残す)。

## 5. 背景

### 5-1 地図型(国土地理院の写真だけ、AI映像なし)
- `python scripts/gsi_clip.py <出力mp4> <レイヤー> <緯度> <経度> [--dx 0.0] [--zoom 16|17]` を場面ごとに1本。`assets/<slug>/fv/clip1..4.mp4` に置く。
- レイヤー: `seamlessphoto`(現在)、`ort_USA10`(1945〜50年 米軍撮影)、`ort_old10`(1961〜64年)、`gazo1`(1974〜78)、`gazo2`(1979〜83)、`gazo3`(1984〜86)、`gazo4`(1987〜90)。年代と地域で欠ける(東北は `ort_USA10` 無し、大阪は `gazo4` 無し)→ 0/35 と出たら別レイヤー。
- 垂直方向は固定。ずらせるのは経度(`--dx`)と中心の緯度。推測の座標は大きくずれる(住所検索で取る)。
- 4コマを並べて目で見る(ずれ・黒い余白・工事中)。写真は出来事の時点の写真ではないことが多い → 画面の出典に年代を入れ、説明欄に書く。
- AI使用の設定は不要(写真のみ)。

### 5-2 AI映像(FreeVideo)
- `fv_prompts(slug, [英語の指示文×4], allow_buildings=False, allow_modern=False)` が `prompts.json` を書く。人物・文字・建物・現代物は共通の末尾で禁止(建物が主役なら `allow_buildings=True`)。
- 生成: `bash scripts/fv_clips.sh <slug>`(全部)/`bash scripts/fv_clips.sh <slug> clip1 clip3`(作り直し)。ComfyUI を起動→生成→停止する。**1本約9分(4本で約36分)**。`run_in_background` で動かし、通知を待つ(ポーリングしない)。待つ間に台本レビューを進める。
  - Windows で素の `bash` は **WSL に解決されて失敗する**(WSL未導入。2026-11-16)。**`C:\Program Files\Git\bin\bash.exe` を絶対パスで呼ぶ**。`fv_clips.sh` は `/e/...` のパスを使うので Git Bash が必要。
- **指示文は、ナレーションの具体物と動きに合わせる**(雰囲気の風景で済ませない)。江戸の場面は "no power lines, no utility poles, no wires, no asphalt" を足す。
- **文字・額・紋・刻印が写ったら作り直す**(看板、額の疑似文字、暖簾の紋、包丁の刻印、掛け軸)。**写したくない物の名前を指示文に書かない**(「no hanging scroll」と書くと、かえって巨大な掛け軸が出た)。見せたい物だけを書き、構図で外す(壁の入らないアップ、"plain empty wall")。場面の中身を変えるほうが確実なこともある(暖簾→土間の台所)。
- 4コマを並べて目で見る(文字、近代的な物=吊り照明・雨どい・電線、人物)。作り直し前のクリップは `fv/old/` に退避。
- メモリ不足(RAM guard)で失敗する → Chromeのタブや並行処理を減らす。**レビューが終わったタブは、その都度閉じる(4-2)**。
- **所要時間は、1本約6〜9分**(2026-11-16は4本で約35分)。**待ち時間を遊ばせない**: その間に、台本のレビュー(ChatGPT・Gemini)、次の題材の下調べ、Xの予約、メモリの記録を進める。ユーザーは「何もやっていないように見える」ことを嫌う(2026-11-16に指摘された)。生成中だと分かる一言を、毎回の報告に入れる。
- **`Port 8188 is already in use` のログが出ても、前回のComfyUIが生きていればその上で生成が進む**(`curl http://127.0.0.1:8188/queue` で実行中のジョブが見える)。失敗ではない。止まっていれば、`tasklist` と `curl` で確かめる。
- 2本連続で作るとき(待ち行列): 1本目の `fv_<slug>.log` に `DONE` が出たら次を始める小さなシェルを `nohup` で走らせる(`for i in $(seq 1 200); do grep -q DONE log && break; sleep 20; done; bash scripts/fv_clips.sh <次のslug>`)。終了通知が欲しい待機は `run_in_background` のシェルで作る(通知が来る)。
- 生成したクリップは、4コマを並べて目で見るまで使わない。
- AI映像を使った動画は、アップ後に「AIの使用=はい」にする(7)。概要欄に「イメージです」。

## 6. ビルドと機械検査

- VOICEVOX が必要: `tools/voicevox/windows-cpu/run.exe --host 127.0.0.1 --port 50021`(**セッションをまたぐと止まる**。`curl http://127.0.0.1:50021/version` で確認して、止まっていれば起動し直す)。
- **ffmpeg / ffprobe に PATH が通っていないと、ビルドは `FileNotFoundError: [WinError 2]` で落ちる**(`make_short2.py` は 'ffmpeg' を素で呼ぶ)。同じシェルで先に `$env:PATH = "E:\rekishikaisetu-honnoji\tools\ffmpeg\bin;" + $env:PATH` を実行する(2026-11-16)。
- `python scripts/solo_ship.py build solo_<slug>` → `E:\rekishikaisetu\sigcmp_view\short_solo_<slug>.mp4`、`out\short_solo_<slug>.mp4`、`out\short_solo_<slug>_kana.txt`、`out\short_solo_<slug>_frames.png`。
- 長さを見る。**55秒を超えたら、ナレーションを削って作り直す**。
- 機械検査(すべて実行):
  - 音量: `ffmpeg -i out/short_solo_<slug>.mp4 -af loudnorm=print_format=summary -vn -f null -`(-14 LUFS前後、ピーク -1.5 dBTP前後)
  - 無音: `-af silencedetect=n=-45dB:d=0.6`(末尾1秒程度のみが正常)
  - 静止: `-vf freezedetect=n=0.003:d=2 -an -f null -`(AI映像は暗くすると差が小さく、静止と出ることがある。実際にコマの差を測る)
  - コマ一覧(`_frames.png`)を Read で見る: 文字の重なり・はみ出し・見切れ・折り返し。直した箇所は、該当コマを抜き出して目で確認する。
- **読み仮名ファイル(`_kana.txt`)の全文を読む**。数字・日付・固有名詞・難読語・同音語を確認(「ミコトノリレイ」のような誤りは、ここでしか見つからない)。誤りは `pron` に登録して再ビルド。
- **タグ**: 台本ファイルに `tags=[...]` があれば、`solo_ship` がそれを使う。**無いと、長尺 `43_bukka`(物価)のタグが入り、`solo_ship` が「tags未指定」と警告する**(警告を見逃して、無関係なタグのまま予約した例がある)。`upload/short_solo_<slug>/tags.txt`・`description.txt`・`title.txt` を開いて、題材に合っているか目で見る。
- **コマ一覧の見方**: 6コマの1枚目に結論カードがあるか、4枚目あたりの比較カードで文字が枠からはみ出していないか(右値が長いと出る)、下のテロップ(ナレーションの字幕)が読めるか、終わりの画面に「出典は説明欄に・チャンネル登録も」があるか。

## 7. 読みの検証(手元ASR)と Muse

### 7-1 手元ASR
`python scripts/asr_kotoba.py cache/short_solo_<slug> E:/rekishikaisetu/sigcmp_view/asr_<slug>.txt`(約2〜4分)。**数字・日付が台本と一致するか**を見る。稀な語・同音語のずれ(冬至→当時、亥の日→井の日)は、聞き取りのぶれ。kana が正しければ、そのまま進める。

### 7-2 Muse(動画のレビュー。「公開可」が出るまで)
1. 圧縮: `ffmpeg -y -i short_solo_<slug>.mp4 -vf scale=540:-2 -c:v libx264 -b:v 700k -c:a aac -b:a 64k muse_short_solo_<slug>.mp4`(`E:\rekishikaisetu\sigcmp_view` に置く。**`file_upload` は1回10.4MBまで**。元の16MBは弾かれた。540pで約5MB)。360p・crf30でも可。
2. Chrome で `https://muse.ai/` を開く(**読み込みに20秒ほどかかる**) → `find` で `type=file` の入力 → `file_upload` → 入力欄(枠の下部。1568×698なら (440,658)、744なら (440,706))を**2回クリック**してから `type` → スクリーンショットで文字と添付を確認 → 送信ボタン((955,658) / (955,706))をクリック。
3. 依頼文のひな形: 「この動画のレビューをお願いします。添付は、〈題材〉のYouTube Shorts(約〈秒〉秒)です。背景は〈AI生成の映像(…)/国土地理院の空中写真〉で、概要欄に〈出典〉と〈AI生成の明示〉を書きます。まず、ナレーションを文字に書き起こしてください(台本と照合します)。見てほしい点は、(1)字幕と音声の一致、(2)読み間違い・音割れ・無音(〈気になる語〉の読みを特に)、(3)文字の重なり・はみ出し・見切れ、(4)事実関係と日付・数字、(5)冒頭1〜3秒の引き、(6)AI映像の不自然さ(文字や額が映っていないか)、(7)公開してよいか。問題点は時刻つきで具体的にお願いします。」(末尾の一文は、返答を探す目印なので変えない。**日本語は直接書く**)
4. 返答は3〜10分(右パネルが「検索中」「確認中」の間は待つ。Museは題材をWeb検索して事実も確かめる)。**`get_page_text` は過去の会話が全部出て長いので、`screenshot` で返答のあたりを出して `zoom`(region 例 [360,80,880,660])で読むほうが速い**。`document.body.innerText` から読むときは、自分の依頼文の**後ろ**を読む。返答の冒頭に「結論：このまま公開可/直してから公開」が出る。
5. **送信したのに返答が来ない**とき: メッセージの下に赤字「配信が確認されていません」が出ていないか見る(配信失敗)。ページを読み込み直して記録が無ければ、動画のアップロードからやり直す。「検索中」「接続中」は待つ。
6. Muse は過去の会話を引いて「前と同じ尺」と答えることがある。書き起こしを台本と照合して使い、返答が途中(項目(2)まで)で終わっても、「公開可」と読みの確認が出ていれば、足りない項目は自分のコマ確認で補う。
7. 「公開可」が出る前にアップしない。画面の不具合は直して再ビルド、読みは 7-1 で再検証。

## 8. アップと公開予約

- `python scripts/solo_schedule.py solo_<slug> "YYYY-MM-DD HH:MM"`(日本時間)。非公開でアップし、公開予約と日本語字幕を付ける。
- **予約日時の決め方**: その日の本数を数えて薄い日へ(1日6〜8本まで。地図型は12:00、**ニュースは当日(すでに12:00・17:00が埋まっていれば19:00)**、江戸の暮らし・歴史は空いている日の12:00か19:00、季節ものは当日か直前)。台帳から日別の予約を数える: `L=json.load(open('data/youtube_ids.json',encoding='utf8'))` → 各 `publishAt`(UTC。日本時間は+9時間)を日付で集計。
- アップ直後の出力: 「アップ完了(非公開): <ID>」「公開予約(日本時間): …」「確認: privacy=private upload=processed publishAt=…」の3行が出れば成功。字幕は `字幕: ok`。
- 最後の確認行で `publishAt=None` と出ることがある(反映の遅れ)。`videos().list(part='status')` で読み直す。**台帳 `data/youtube_ids.json` に `publishAt` が入っていなければ**、`yt_api.load_ids()` / `save_ids_atomic()` で追記する。
- **AI映像の動画は**、`videos().update(part='status', body={'id':..., 'status': {'privacyStatus':'private','publishAt':'<ISO>','selfDeclaredMadeForKids':False,'containsSyntheticMedia':True}})` を設定。地図型(写真のみ)は不要。
  - **APIの読み戻し(`part=status`)には `containsSyntheticMedia` が出ない**(正常)。確認は **Studio**: `https://studio.youtube.com/video/<ID>/edit` を開き、`詳細設定を表示`(`find` で出る)をクリック → `[...document.querySelectorAll('tp-yt-paper-radio-button')].filter(e=>/^(はい|いいえ)$/.test(e.innerText.trim())).map(e=>({name:e.getAttribute('name'), checked:e.getAttribute('aria-checked')}))` で `VIDEO_HAS_ALTERED_CONTENT_YES` が `true` なら設定済み(2026-11-16 プラニマルで確認)。
  - `status` の更新で、`embeddable`/`publicStatsViewable` が他の動画と違う値になることがある。公開には影響しないので、そのままでよい。
- **アップ後のメタデータ確認(必須)**: `s.videos().list(part='snippet,status', id=ID)` で `tags`・`title`・`description` の冒頭を読み、題材に合っているか確かめる。違っていれば `videos().update(part='snippet', body={'id':ID,'snippet':{'title':..,'description':..,'categoryId':..,'tags':[..],'defaultLanguage':'ja'}})`(title・description・categoryId は読んだ値をそのまま渡す)。**読み戻しは数秒遅れる**(直後は古い値が出る)。`upload/<動画>/tags.txt` も直す。
- 地図型は、再生リスト `PLNolPNGRhWYI` に `playlistItems().insert` で追加する。
- API認証(テスト中のOAuth)は**7日で切れる**(Data API約11/17、Analytics約11/21)。切れたらユーザーが `cd E:\rekishikaisetu-honnoji` → `python scripts/yt_api.py auth` と `python scripts/yt_analytics.py auth`(kaenozu@gmail.com)。IPv4で届かないときは IPv6固定(`youtube-api-ipv6-workaround`)。
- 公開前に、削除・差し替え・公開状態の変更・予約の付け替えは、ユーザーに確認する(アップ・新規予約は、委任されている範囲で進めてよい)。

## 9. X(@yorimichi_lab1)の紹介投稿を予約する

- **新作は、アップ・予約した日のうちに、X の予約投稿も入れる**(公開時刻の5分後。抜けた日がある)。投稿は1日2〜3本まで(新作+過去動画の紹介1本=21:30)。過去動画の紹介は、日付のない題材を1日1本、21:30に。
- ブラウザは **Playwright の専用ブラウザ**(`mcp__playwright-mcp__*`)。ユーザーがその窓で @yorimichi_lab1 にログイン済み。ブラウザが途中で閉じても、`browser_navigate` し直せばログインは残っている(専用プロファイルに保存されている)。
- **Xは、拡張機能側のChromeでは投稿しない**(2026-11-16 ユーザー指示)。専用プロファイルは `C:\Users\neoen\AppData\Local\ms-playwright-mcp\mcp-chrome-666d4fb`(x.com のログインあり。Cookiesで確認)。`python scripts/x_schedule.py --video <ID> --day 21 --hour 12 --min 5 --question "問い" --ai` が、アカウント確認→予約日時の設定→本文→事前チェック→投稿→予約一覧での重複確認まで行う(`--dry-run` で送信前に止まる。2026-11-16 に x32F4QhOUSI で成功)。投稿後は予約一覧(`/compose/post/unsent/scheduled`)で同じ動画IDが1件だけか数える。
  - **理由と決まり(2026-11-13の経緯)**: Claude in Chrome がつなぐのは**ユーザーの普段のChrome**で、普段のアカウントでログインしている。寄り道ラボのXは**別アカウント**なので、**普段のChromeや内蔵ブラウザ(`mcp__Claude_Browser__*`)ではXを開かない・ログインしない**(別アカウントで投稿する事故を防ぐ。内蔵ブラウザはペインが開き直されるとログインも消えた)。Chromeのプロフィールを私が切り替えることはできないため、「別プロファイルのChromeを立ち上げる」方式は採っていない。
  - **プロファイルの場所(2026-11-16に調べた)**: `C:\Users\neoen\AppData\Local\ms-playwright-mcp\mcp-chrome-666d4fb`(Playwright MCPが作る独立したフォルダ。中のプロファイル名は `Default`。Chromeの「Profile 1」のような名前は付いていない)。**このフォルダのCookieにだけ x.com / twitter.com が入っている**(同じ場所の他の5つの `mcp-chrome-*` にはXのログインが無い)。
  - 確認のしかた: `mcp__playwright-mcp__browser_navigate https://x.com/compose/post` を開き、投稿画面が出て、予約ボタン(`[data-testid=scheduleOption]`)があればログイン済み。ログイン画面が出たら、**別のプロファイル(別のmcp-chromeフォルダ)を使っている可能性**がある(作業フォルダが変わると別のフォルダになる、と推測。未確認)。その場合はユーザーに知らせる。自分でログイン操作はしない。
  - ユーザーの普段のChromeは、`list_connected_browsers` で「Browser 1」と出る(Claude in Chrome。YouTube Studio・ChatGPT・Gemini・Museには使うが、**Xには使わない**)。
  - Playwrightの窓でログインが消えていたら、**ユーザーにその窓でログインしてもらう**(私はパスワード・認証コードを入力しない)。ログインできるまでXの投稿はしない。
- 手順(1投稿):
  1. `browser_navigate https://x.com/compose/post`
  2. `browser_evaluate`: 予約ボタン(`[data-testid=scheduleOption]`)をクリック → `#SELECTOR_1`(月)`#SELECTOR_2`(日)`#SELECTOR_3`(年)`#SELECTOR_4`(時)`#SELECTOR_5`(分)にselectの値を設定(`Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype,'value').set.call(s, v)` と change イベント)→ テキストが `Confirm` の要素をクリック。
  3. `browser_click` と `browser_type`(target は `[role=dialog] [data-testid=tweetTextarea_0]`。入力欄が2つあるので、dialog 指定が必須)で本文を入れる。
  4. `browser_evaluate`: 本文にURLが1つだけか、予約時刻が合っているかを確かめてから `[role=dialog] [data-testid=tweetButton]` をクリック。
- **複数本をまとめて予約するとき**(2026-11-16に7本を1回で成功): `mcp__playwright-mcp__browser_run_code_unsafe` の `code` に、次の関数を渡す。1件ごとに「URLが1つか」「ボタンが有効か」「日時が合っているか」を確かめ、違えば中断する。**Playwrightのブラウザが閉じていると「Target page … has been closed」で失敗する → 先に `browser_navigate https://x.com/compose/post/unsent/scheduled` で開き直し、予約一覧に入っていないことを確かめてから、もう一度実行する**(重複防止)。
```js
async (page) => {
  const items = [['<動画ID>', '<問い>', <AI背景ならtrue>, '#タグ1 #タグ2 #寄り道ラボ', <日>]];   // 月・時刻は下で固定
  const log = [];
  for (const [id, q, ai, tags, day] of items) {
    const text = q + '\n約1分でこたえを確かめました。\n' + (ai ? '※背景映像はAI生成のイメージです\n' : '') + 'https://www.youtube.com/shorts/' + id + '\n' + tags;
    await page.goto('https://x.com/compose/post');
    await page.waitForSelector('[data-testid=scheduleOption]', { timeout: 30000 });
    await page.waitForTimeout(1500);
    await page.evaluate(() => document.querySelector('[data-testid=scheduleOption]').click());
    await page.waitForSelector('#SELECTOR_1', { timeout: 15000 });
    const vals = await page.evaluate((day) => {
      const set = (id, v) => { const e = document.querySelector('#' + id); const s = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value').set; s.call(e, String(v)); e.dispatchEvent(new Event('change', { bubbles: true })); return e.value; };
      return [set('SELECTOR_1', 12), set('SELECTOR_2', day), set('SELECTOR_3', 2026), set('SELECTOR_4', 21), set('SELECTOR_5', 30)];   // 月,日,年,時,分
    }, day);
    await page.evaluate(() => { const c = [...document.querySelectorAll('button,[role=button],span')].find(e => e.textContent.trim() === 'Confirm'); c.click(); });
    await page.waitForTimeout(1500);
    const ta = page.locator('[role=dialog] [data-testid=tweetTextarea_0]');
    await ta.click(); await ta.fill(text); await page.waitForTimeout(800);
    const chk = await page.evaluate(() => { const d = document.querySelector('[role=dialog]'); const t = d.querySelector('[data-testid=tweetTextarea_0]').innerText; const b = d.querySelector('[data-testid=tweetButton]'); return { n: (t.match(/youtube\.com/g) || []).length, dis: b && b.disabled, when: (d.innerText.match(/(Dec|Nov)[^\n]{0,30}/) || [''])[0] }; });
    log.push({ id, vals, chk });
    if (chk.n !== 1 || chk.dis || !/Dec \d+, 2026 at 9:30 PM/.test(chk.when)) { log.push('ABORT ' + id); break; }
    await page.evaluate(() => document.querySelector('[role=dialog] [data-testid=tweetButton]').click());
    await page.waitForTimeout(5000);
  }
  return log;
}
```
- 予約後は、予約一覧を開いて `Will send on …` の件数と日時、同じ動画IDの重複(`shorts/<ID>` が2回)が無いかを数える。
- 過去動画の紹介に使う候補は `sigcmp_view/xassets/top.json`(視聴数順。cp932で保存されているので `decode('cp932')`)から、**日付の入った時事ニュース(【2026年…】)と、すでに予約したIDを除いて**選ぶ。AI背景かどうかは、APIで説明欄に「AI生成」があるかで判定する(無ければ「※背景映像はAI生成のイメージです」を付けない)。
- 投稿後に `/i/graduated-access` へ移るが、**投稿は通っている**(重複投稿しない)。X画面は読み込みに10秒以上かかる。
- 文字数: 全角は2文字換算(約140字)。本文: 問い→答えへの導線→「約N秒で整理しました」→AI背景なら「※背景映像はAI生成のイメージです」→URL(`https://www.youtube.com/shorts/<ID>`)→ハッシュタグ(`#雑学 #寄り道ラボ` など)。ニュースは年月日と「〇年〇月〇日時点の情報」。
- 確認: `https://x.com/compose/post/unsent/scheduled`(予約一覧。送信済みは消える)。プロフィール `https://x.com/yorimichi_lab1`(送信済みの投稿)。予約全体に重複が無いかを、動画IDで数える。
- 効果は数日後に見る(Studio の外部流入で「X」の行が出るか)。

## 10. 公開後の確認と分析

- **API**(読み取り): `yt_api.service()`(Data API。再生・高評価・コメント数、予約状況、登録者数)、`yt_analytics.svc()` と `q()`(Analytics。**1〜2日遅れ**。`maxResults` は200まで。`ageGroup` は `metrics='viewerPercentage'` が要る)。
- **Studio の Ask Studio**(API で取れない数字):
  - 手順: `tabs_context_mcp` → `https://studio.youtube.com/channel/UCN_do9fcssctmkrNsRWOO9A/analytics/tab-overview/period-default` → `find` で「Ask Studio」 → クリック → 入力欄(約1240,566)に**日本語を直接** `type` → Return → 20秒待つ → スクリーンショットで読む(パネルは `get_page_text` に出ない。長い返答はパネルを scroll して `zoom` で読む)。
  - 聞けるもの: 新規/ライト/コアの視聴者、外部流入(X)、検索語、コメントの内容、戦略案(根拠の数字つき)。**外に出る操作(コメント返信・設定変更)はしない**。
- 比較は、**同じ期間・同じ条件**で(伸びた時期を混ぜない)。公開から日が浅い動画・コメントが少ない動画は、判断しない。
- 定期確認: 毎朝8:30ごろ、読み取りだけのレポートを作る(`mcp__scheduled-tasks__create_scheduled_task`、fireAt。**自動承認の判定で止められることがある** → ユーザーに許可を頼むか、口頭で依頼してもらう)。出力は `sigcmp_view/analytics_<日付>.md`。

## 10b. ローカルの整理(アップ後。月に1回ほど)

動画ファイルは大きい(1本10〜50MB。作業用のキャッシュを含めると、数百本で数GB)。アップ済みの動画のローカルコピーは、消してよい(ユーザー許可、2026-11-15)。
- `python scripts/cleanup_uploaded.py`(dry-run。一覧と容量)→ 確認して `--apply`(削除し、記録を `sigcmp_view/cleanup_<日付>.txt` に書く)。
- **判定は、台帳の video_id が YouTube に実在するか**(API)。YouTubeに無い動画は、ローカルが唯一のコピーかもしれないので残す。台帳に無い(未アップ)動画も残す。
- 消すもの: `upload/<動画>/*.mp4`、`cache/<動画>/`、`out/<動画>.mp4`(Muse用の360p版を含む)、`sigcmp_view` の同名 mp4。
- 残すもの: 台本・data・読み辞書・字幕・説明欄・タグ(`upload/<動画>/` のテキスト)、**背景クリップ(`assets/<slug>/fv`。作り直しに9分ずつかかる)**、tools、`E:\rekishikaisetu\out` の台本テキスト(`script_solo_*.txt`)・報告書・画像・字幕(動画ファイルだけは、2026-11-16にユーザー許可で一括削除済み。新しい試作動画が `out` にたまったら、同様に確認して消す)。
- 名前は**完全一致**で拾う(前方一致だと、別の版を巻き込む)。不採用の背景クリップ(`assets/*/fv/old`)は、不要なので消してよい。
- `rm` の対象に、空になり得るシェル変数を使わない(`rm -f "$T/$pat"` は安全確認に止められる)。変数を使うなら `"${T:?}"` の形にする。
- 初回の実績(2026-11-15): 270件、約5.96GBを削除(upload 1.1GB、cache 2.08GB、out 1.08GB、sigcmp_view 1.73GB)。

- **予約の公開確認**: `python scripts/check_published.py <台帳のキー…>`(読み取りだけ。予約時刻を過ぎたのに公開されていない動画を「要確認」と出す)。公開予定の時刻の5分後に実行する。

## 11. 記録

- 動画ごとのメモを `memory`(`C:\Users\neoen\.claude\projects\E--rekishikaisetu\memory\`)に残す(題材、根拠、レビューで直した点、動画ID、予約、罠)。`MEMORY.md` に1行の索引を足す。公開済みになったら、索引の「未着手」表記を直す(古い表記で、公開済みの題材を提案した例がある)。
- 新しい罠・手順は、この文書か `docs/VIDEO_PRODUCTION_RUNBOOK.md` に追記する。

## 12. 罠の一覧(早見表)

| 場面 | 罠 | 対処 |
|---|---|---|
| 台本 | `\uXXXX` で書くと別の字に化ける(晦→晩、炊→烊、東→室) | 日本語は直接書く |
| 台本 | ヒアドキュメントの `\n` が本物の改行になる | Edit ツールで直す |
| 台本 | 大見出しが13字以上で折り返し、カードに重なる | 12字以内に |
| 台本 | 「三十日」が「30日」と表示され読めない | ひらがなで書く |
| 台本 | 「勅令」が「ミコトノリレイ」になる | `pron` に登録、kana全文を読む |
| 台本 | 長すぎる(66〜78秒) | ナレーションを約230字に削る |
| レビュー | ChatGPT/Geminiが出典にない文言を引く | 自分で原文を確認してから反映 |
| レビュー | 旧暦の日付を今の日付に換算する案 | 換算しない |
| 背景 | 文字・額・紋・刻印が写る | 場面の中身を変える。写したくない物の名前は書かない |
| 背景 | 「no 〇〇」と書くと〇〇が大きく出る | 見せたい物だけ書く |
| 背景 | メモリ不足で失敗 | Chrome・並行処理を減らす。失敗した1本だけ作り直す |
| 検査 | 静止の検出(暗い映像) | コマの差を測る。カード切替以外の差があれば問題なし |
| Muse | 返答が来ない | 赤字「配信が確認されていません」→ 読み込み直して送り直す |
| Muse | 座標が違う(枠が1568×698/744) | 直前のスクリーンショットの枠で指定 |
| Chrome | 拡張機能が切れる/タブがグループから外れる/screenshotがタイムアウト | 再接続を頼む/タブを取り直す/JSで直接操作 |
| Chrome | **レビューが終わってもタブを開いたままにする** | 自分で開いたレビュー用のタブは、終わったらその場で閉じる(4-2)。ユーザーのタブ(Gmail・X・Studio など)は閉じない |
| Chrome | **Muse・X用の専用Chromeの窓が残る** | `muse_review.py`・`x_schedule.py` は atexit の `close_launched()` で、自分が起動したChromeだけを閉じる。確認は `Get-CimInstance Win32_Process -Filter "Name='chrome.exe'"` の CommandLine を `chrome-automation` / `mcp-chrome-666d4fb` で絞って数える(2026-11-16は0件を確認) |
| アップ | tags.txt が前の動画のまま | 毎回書き直す |
| アップ | 確認行が `publishAt=None` | APIで読み直す。台帳に追記 |
| X | 投稿後に `/i/graduated-access` へ飛ぶ | 投稿は通っている(重複しない) |
| X | 入力欄が2つで指定があいまい | `[role=dialog]` 指定 |
| X | Playwright のブラウザが閉じる | navigate し直す(ログインは残る) |
| API | 認証が7日で切れる | ユーザーが `yt_api.py auth` |
| 分析 | 伸びた時期を混ぜて比較する | 同じ期間・条件で比べる |
| アップ | **前の動画のタグが付く**(`tags=` 未指定 → 物価・総務省などが付いた。2026-11-16) | 台本ファイルに `tags=[...]`。アップ後にAPIで読む |
| 題材 | ChatGPTの候補を確かめずに使う(東北大の結晶は確認できず、1486年は資料と食い違い) | 一次ページで確認できた1案だけを使う |
| 題材 | Wikipediaの文を、出典で確認せずに言う(「庶民は使えなかった」) | 出典(資料館通信など)で確認できた部分だけ |
| 資料 | PDFの文字が取れない・文字化け | 画像PDFは `fitz` でPNGにして目で読む。表示は `PYTHONUTF8=1` |
| 実行 | **Windowsでの `python - <<EOF` や置換で、日本語が文字化けして構文エラー** | 日本語の文字列編集は `Write`/`Edit` ツール。`python` の出力は `PYTHONUTF8=1` |
| 実行 | **素の `bash` が WSL に解決されて `fv_clips.sh` が動かない**(WSL未導入。2026-11-16) | `& "C:\Program Files\Git\bin\bash.exe" scripts/fv_clips.sh <slug>` と絶対パスで呼ぶ |
| ビルド | **`ffmpeg` が PATH に無く `FileNotFoundError: [WinError 2]`**(2026-11-16) | ビルドの前に `$env:PATH = "E:\rekishikaisetu-honnoji\tools\ffmpeg\bin;" + $env:PATH` |
| 読み | **「873件」が「サンゲン」と読まれる**(2026-11-16) | `pron` は文字列置換。`'873件': 'ハッピャクナナジュウサンケン'` のように登録する(字幕の表示は変わらない) |
| 背景 | `Port 8188 is already in use` | 前回のComfyUIが生きていれば、その上で進む(`/queue` で確認) |
| 背景 | 生成中にChromeが固まる(screenshot・typeが30秒でタイムアウト) | `get_page_text`・JSで操作。画面が進まなければ再読み込みして送り直す |
| 台本 | 同じ動画内の同音語(債権/再建、俳諧/徘徊)、長い比較カードの値(枠からはみ出す) | 言い換える/値を短く(右ラベルと値で分ける) |
| 台本 | 62秒になった | 読点・言い換えで削り、各場面を2〜3割短くする(58秒までは許容) |
| 読み | 「藻の」が「モノ」と読まれる | 「モ+の」で正しい。kana の `モノ` を見て誤りと決めつけない。`pron` に長めの語(「シゾンという藻」)で登録 |
| Muse | `file_upload` が10.4MBで弾かれる | 540pに圧縮(約5MB) |
| Muse | 返答まで3〜4分かかる(検索中) | 待つ。`screenshot`+`zoom` で読む |
| API | `containsSyntheticMedia` が読み戻しに出ない | Studioの詳細設定のラジオ(`VIDEO_HAS_ALTERED_CONTENT_YES`)で確認 |
| X | `browser_run_code_unsafe` で「Target page… has been closed」 | `navigate` で開き直し、予約一覧で重複を確かめてから再実行 |
| 背景 | **道路・看板・電線・書類の疑似文字・硬貨の人物の彫刻が出る**(徳政令、2026-11-16。「no power lines, no asphalt」と書いても出た) | 否定を書かず、**見せたい物を具体的に**書く。例: 「白い漆喰の壁の土蔵の重い木の扉と藁の俵、土の地面」「紐で結んだ巻いた巻物を無地の木箱に」「中央に四角い穴のある、表面が無地の銅銭を紐に通して木の盆に」。文字が出る物(開いた書類、看板、通貨の刻印)は、閉じた物・無地の物に置き換える。作り直しは `fv_clips.sh <slug> clip1 clip2 clip3`(旧版は `fv/old` へ) |
| 字幕 | 質問文の字幕の末尾に次の文の「出典は」がぶら下がる(湯たんぽ・徳政令でMuseが2回指摘) | `make_short.py` の `chunks()` を修正済み(「？」「！」の文末で必ず区切る)。**以後のビルドは自動で直る** |
| Muse | 「最大0dBに到達」「音割れの可能性」と指摘される | 圧縮した確認用コピーの特性。**元動画の `loudnorm` のTrue Peak(-1.5 dBTP前後)で判断する**。元が-1.0を超えていなければ直さない |
| ASR | 「分一銭→V1線」「季弘大叔→総の気候大宿」など珍しい語がずれる | 聞き取りのぶれ。数字・日付が一致していて、kanaが正しければ進める |

## 12b. 作業の進め方(待ち時間の使い方・報告のしかた)

**1本を作る標準の流れと所要時間**(2026-11-16 プラニマル実績。並行すると、実質2〜2.5時間):
1. 題材決め・原文確認(30〜40分)→ 台本ファイル → `python` で生成 → **すぐ背景生成を開始**(`fv_clips.sh`、約35分。バックグラウンド)。
2. 背景生成の間に: ChatGPT・Geminiの台本レビュー → 反映 → 台本を再生成(指示文が変わらなければ、生成中のクリップはそのまま使える)。次の題材の下調べ、Xの予約、メモリの記録。
3. 背景ができたら: 4コマを見る → ビルド(約3分)→ 長さ・コマ・kana・音量・ASR → Muse(圧縮して送る。返答3〜4分)→ 「公開可」→ アップ・予約 → AI注記・タグの確認 → X予約 → メモリ。
4. 長さが超えたら、ナレーションを削って再ビルド(3分ずつ)。

**報告のしかた**(ユーザーは進み具合が見えないと不安になる。2026-11-16に「なにもやってなくない？」と指摘された):
- 待っているときは、**何が動いていて、いつ終わる見込みか**、その間に何をするかを書く。
- 「終わったこと」「進行中」「このあと」「ユーザーにお願いすること」に分ける。**確認した範囲と未確認を分ける**(生成・デコードに成功しただけで、視聴品質や公開可を宣言しない)。
- 間違いは正直に書く(タグ誤りを見つけたら、直してから、そのことを報告する)。

**ユーザーの決まり(毎回守る)**: 背景・イラストはAIに依頼する(自作は図だけ)/ニュースは全て年月日/応答は日本語/削除・差し替え・予約の付け替え・公開状態の変更は確認する/不確かな確認は深追いしない(エンタメ優先、ただし明確な誤断言・中傷は避ける)/認証が切れたら、ユーザーに頼む(自分で回避しない)。

## 13. コマンド早見表

```bash
cd /e/rekishikaisetu-honnoji
python scripts/gen_solo_<名前>.py                       # 台本→JSON・レビュー用テキスト・AI映像の指示文
python scripts/gsi_clip.py <out.mp4> <layer> <lat> <lon> [--zoom 16]   # 地図型の背景
bash scripts/fv_clips.sh <slug> [clipN ...]             # AI映像(全部/作り直し)。バックグラウンドで
python scripts/solo_ship.py build solo_<slug>           # ビルド(VOICEVOXが必要)
python scripts/asr_kotoba.py cache/short_solo_<slug> E:/rekishikaisetu/sigcmp_view/asr_<slug>.txt
python scripts/solo_schedule.py solo_<slug> "YYYY-MM-DD HH:MM"   # 非公開アップ+予約+字幕
```

## 15. 完成例(書き写して直す)

| 型 | 台本ファイル | 動画ID | 見どころ |
|---|---|---|---|
| 科学ニュース | `gen_solo_news_planimal.py` | diDJcBO_ybg(2026-11-16 19:00) | JST共同発表+PDFで数字を確認。「まだ先」を明記。年月日の入れ方 |
| 江戸の暮らし | `gen_solo_yutanpo.py`、`gen_solo_kotatsu.py` | mrpfogC6t_U(2026-11-18 12:00) / AKrIQzBauTA | 自治体資料館・Wikipediaで確認。「一般的ではなかったとされる」の弱め方 |
| 歴史(制度) | `gen_solo_tokusei.py` | MXSp6vn7t6A(2026-11-19 12:00) | 二次資料のみの数字を「とされます」で書く。同音語の言い換え |
| 地図型 | `gen_solo_minatomirai.py`(QQ9rUhVqwDs) | QQ9rUhVqwDs | 国土地理院の年代別写真。AI注記なし |
| 季節の暦 | `gen_solo_toji.py`(1vhIFZrNpdc) | 1vhIFZrNpdc | 国立天文台の暦。「最も早い日」を断定しない |

関連メモリ(`C:\Users\neoen\.claude\projects\E--rekishikaisetu\memory\`): `planimal-video.md`、`x-promo-post.md`、`solo-short-procedure-doc.md`、`delegated-video-management.md`、`pipeline-speedups-20261104.md`、`visual-rules-from-user-feedback.md`、`news-dates-full.md`。
