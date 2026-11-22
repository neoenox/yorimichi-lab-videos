# エージェント共通指示

## 動画制作の事前確認は必須

動画を新規作成・作り直し・編集・合成・レンダリングする場合、または動画用のシーン、素材、台本同期、字幕、音声を制作する場合は、**作業を始める前に** `docs/VIDEO_CREATION_PRECHECK.md` を全文読んでください。全文を読めない場合は動画制作に着手せず、その理由を報告してください。動画専用の作業を別エージェントへ委任するときは、そのエージェント自身にも同じ文書を作業開始前に読ませてください。親エージェントが読んだだけでは代わりになりません。

最初の進捗報告で、事前確認を済ませたことと、今回適用する制作上の要点を一言で示してください。確認票と依頼内容に違いがあるときは、ユーザーの指示を優先し、変更する点を説明してください。

## 単独Short（YouTube Short）を作る・公開するときは、手順書の読み取り確認が必須

単独Shortの台本生成・背景生成・ビルド・アップ・公開予約・X予約の前に、`E:\rekishikaisetu-honnoji\docs\SOLO_SHORT_PROCEDURE.md` を**全文**読み、確認問題に答えてください。読んだことの証明は、次の操作でしか作れません（`E:\rekishikaisetu-honnoji` で実行）。

1. `python scripts/read_procedure.py`（全体と部分の数）
2. `python scripts/read_procedure.py --part 1` … 最後の部分まで、すべて表示して読む（未表示だと問題に進めない）
3. `python scripts/read_procedure.py --questions` → `python scripts/read_procedure.py --answer 1=… 2=…`（全問正解で、24時間有効の印ができる）

印が無い・期限切れ・手順書が更新された場合、`gen_solo_*.py`（`solo_spec.build`）、`solo_ship.py`、`solo_schedule.py` は止まり、Claude Code では該当コマンドがフックで拒否されます。**印を偽造したり、`PROCEDURE_ACK_SKIP=1` で回避したりしないでください**（非常時に使った場合は、理由をユーザーに報告する）。確認問題の答えを `docs/SOLO_SHORT_QUIZ.md` から写して通すことも、読んだことになりません。動画制作を別のエージェントに任せるときは、そのエージェント自身にこの確認をさせてください。

## イラスト・背景画像は必ずChatGPTに依頼する（毎回守ること）

動画（ニュースShortを含む）の背景・場面イラスト・サムネイルの絵は、**コードで描いて済ませず、最初からweb版ChatGPT（chatgpt.com、Claude in Chromeで操作）に依頼して生成する**。ユーザーが毎回指示している決まりです（2026-11-05に記録）。自作してよいのは、データ由来の図（年表・棒グラフ・比較・流れ図などのviz、地図）だけです。依頼文では、画像に文字を入れさせず、文字を載せる余白を指定します。生成画像は「イメージです」と概要欄に明記します。手順・保存方法は `docs/VIDEO_PRODUCTION_RUNBOOK.md` と、メモリの image-generation-chatgpt / codex-evaluation-only を参照。

動画の生成・デコードに成功しただけで、視聴品質や投稿可能を宣言しないでください。映像の動き、全編の音声、字幕同期など、実際に確認した範囲と未確認の範囲を分けて報告してください。

## ニュース系の動画は、必ず年月日を入れる（毎回守ること）

時事ニュースを扱う動画・Short・説明欄・タイトルでは、**日付をすべて年月日で書く**（例：2026年11月5日。「11月5日」「12日頃」だけにしない）。来年見たときに意味が変わってしまうため。画面の図・年表・ナレーション・説明欄・タイトル（「【2026年11月5日】…」）のすべてに入れ、「2026年11月5日時点の情報」と、過去の動画だと分かる表示も置く。ユーザーの指示（2026-11-05に再度）。長いタイトルは spec の `head` で画面上部の見出しだけ短くできる。

## レビューは Google AI モードを使う（2026-11-20 オーナー指示）

動画レビューは **Google AI モード**（https://www.google.com/ai）のみを使い、`python scripts/google_ai_review.py <slug> --mode video --video out/...mp4` で行う。**台本レビューは Google AI モードと ChatGPT を併用**し、Google AI モードは `python scripts/google_ai_review.py <slug> --mode script`、ChatGPT は `python scripts/review_short_cdp.py <slug> chatgpt` で実行する。Gemini は必須ではない。AIの指摘は必ず根拠の原文と照合してから採用・不採用を決め、`docs/research/` に記録する。Muse は起動しない。

## Shorts は制作標準（shorts-standard/）に従う

YouTube Shorts を新規作成・改訂するときは、作業前に `shorts-standard/README.md` と `shorts-standard/PROMPT.md` を全文読んでください。`shorts-standard/output.schema.json` が納品形式、`shorts-standard/validate.py` が形式検査です。**この標準のルールを勝手に緩めないでください。** 緩和が必要だと判断したら、変更せずに理由を報告してユーザーの判断を仰ぎます。

> 2026-11-04 のオーナー判断で **v1.1** に改訂済み: `claims.source_type` に `ai_assistant` を許す（AI アシスタントの回答を根拠にしてよい）。詳細は `shorts-standard/CHANGELOG.md`。`primary` は従来どおり一次資料の URL が必要。

手順:

1. `python scripts/shorts_standard.py new <slug> --topic "題材"` で `shorts/<slug>/brief.yaml` を作る。
2. brief の `source_urls` は実際に開いて確認した URL だけを書き、`verified_facts` には確認できた事実だけを書く。推測で埋めない。
3. `python scripts/shorts_standard.py brief-check shorts/<slug>/brief.yaml` を通す。
4. `PROMPT.md` の指示に従い、`shorts/<slug>/result.json` を作る（JSON のみ。疑問→結論の方向性→理由・根拠→結論回収、30〜45秒、5〜7シーン）。
5. `python scripts/shorts_standard.py check shorts/<slug>/result.json` が ERROR 無しになるまで直す（WARN は内容を確認して判断）。
6. 出典の原文照合が済むまで `status` は `needs_review`。未確認の事項は `needs_research` に書く。`needs_research` が空でない JSON は `ready` にできない。
7. `ready` の JSON だけを `python scripts/shorts_standard.py to-spec ...` でレンダラ用 spec に変換する。`needs_review` は変換されない（試作が必要なら、その旨と未確認範囲を報告する）。
8. 根拠資料が足りない題材は制作を止め、何の資料が必要かを報告する。確認していない数字・発言・因果関係を台本に書かない。
9. 既存の動画・台本・素材・レンダラ（`scripts/make_short2.py` など）を勝手に削除・上書きしない。試作は別名で作る。

CI（`.github/workflows/shorts-standard.yml`）が `shorts/**/result.json` を検査し、`tests/test_shorts_standard.py` が標準ルールの緩和を検知します。

## ノウハウは必ず git に残す

制作・検証で分かったことは、**その場で文書に書いてコミット**してください。チャットや記憶に残さない。

- **入口**: [`docs/KNOWHOW.md`](docs/KNOWHOW.md)（何がどこに書いてあるかの索引。まずこれを更新する）
- 追記先: `docs/SHORTS_PRODUCTION_NOTES.md`（Shorts の実測ノウハウ）、`docs/SHORTS_STANDARD_INTEGRATION.md`（標準との統合・差分）、`docs/VIDEO_PRODUCTION_RUNBOOK.md`（長尺の手順）
- 書く内容: 実際に試して分かった制約、失敗した症状と原因と対処、使ったコマンド、出典URLと利用条件、確認した範囲と未確認の範囲
- 書かない内容: 推測、未検証の数値、再現できない手順
- コマンドや切り出し比率などは、後から同じ結果を再現できる粒度で書く（例: IIIF の URL 形式、画像の切り出し比率、ffprobe の確認項目）
- 知見が増えたら、次に作業するエージェントが最初に読む文書（この AGENTS.md・上記2文書）から辿れるようにする
