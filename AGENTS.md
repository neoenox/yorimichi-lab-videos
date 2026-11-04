# エージェント共通指示

## 動画制作の事前確認は必須

動画を新規作成・作り直し・編集・合成・レンダリングする場合、または動画用のシーン、素材、台本同期、字幕、音声を制作する場合は、**作業を始める前に** `docs/VIDEO_CREATION_PRECHECK.md` を全文読んでください。全文を読めない場合は動画制作に着手せず、その理由を報告してください。動画専用の作業を別エージェントへ委任するときは、そのエージェント自身にも同じ文書を作業開始前に読ませてください。親エージェントが読んだだけでは代わりになりません。

最初の進捗報告で、事前確認を済ませたことと、今回適用する制作上の要点を一言で示してください。確認票と依頼内容に違いがあるときは、ユーザーの指示を優先し、変更する点を説明してください。

動画の生成・デコードに成功しただけで、視聴品質や投稿可能を宣言しないでください。映像の動き、全編の音声、字幕同期など、実際に確認した範囲と未確認の範囲を分けて報告してください。

## Shorts は制作標準（shorts-standard/）に従う

YouTube Shorts を新規作成・改訂するときは、作業前に `shorts-standard/README.md` と `shorts-standard/PROMPT.md` を全文読んでください。`shorts-standard/output.schema.json` が納品形式、`shorts-standard/validate.py` が形式検査です。**この標準のルールを勝手に緩めないでください。** 緩和が必要だと判断したら、変更せずに理由を報告してユーザーの判断を仰ぎます。

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

- 追記先: `docs/SHORTS_PRODUCTION_NOTES.md`（Shorts の実測ノウハウ）、`docs/SHORTS_STANDARD_INTEGRATION.md`（標準との統合・差分）、`docs/VIDEO_PRODUCTION_RUNBOOK.md`（長尺の手順）
- 書く内容: 実際に試して分かった制約、失敗した症状と原因と対処、使ったコマンド、出典URLと利用条件、確認した範囲と未確認の範囲
- 書かない内容: 推測、未検証の数値、再現できない手順
- コマンドや切り出し比率などは、後から同じ結果を再現できる粒度で書く（例: IIIF の URL 形式、画像の切り出し比率、ffprobe の確認項目）
- 知見が増えたら、次に作業するエージェントが最初に読む文書（この AGENTS.md・上記2文書）から辿れるようにする
