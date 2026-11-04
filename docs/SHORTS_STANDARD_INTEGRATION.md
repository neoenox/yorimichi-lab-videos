# Shorts 制作標準の統合（調査・差分・使い方）

更新日: 2026-11-04。`shorts-standard/`（v1.0、原本を byte 一致で配置）を既存の動画制作へ接続した記録。

## 1. 既存の制作方式（調査結果）

| 工程 | 実装 | 入力 | 出力 |
| --- | --- | --- | --- |
| 長尺の台本・絵コンテ | `scripts/vp.py <slug> story` | `data/<slug>_spec.json` ＋ `docs/themes/<theme>/09_script_v2.md` | `data/<slug>_scenes.json` / `_timeline.json` |
| 音声 | `scripts/vp.py <slug> audio` → VOICEVOX（`http://127.0.0.1:50021`、`SPEED=0.95`） | 台本＋`data/<slug>_pronunciations.json`（読み） | `out/<slug>_audio.wav` ほか |
| 描画 | `scripts/vp.py <slug> build`（PIL でカード合成）→ FFmpeg（libx264） | timeline＋`assets/<slug>/` の画像 | `out/<slug>_video.mp4` |
| Shorts | `scripts/make_short2.py <slug>` | `data/short_<slug>.json`（`title`/`hook`/`pron`/`art`/`scenes[{text,big,sub,src,art,col}]`/`answer`/`credit`） | `out/short_<slug>.mp4` / `_subtitles.srt` / `_description.md` |
| Shorts の spec 生成 | `scripts/gen_solo_shorts*.py`（人手で書き分け） | 長尺の台本・`08_fact_check.md`・統計 | `data/short_<slug>.json` |
| 公開 | `scripts/pack_short.py`、`scripts/yt_api.py upload`（非公開で登録） | `out/` と `upload/` | YouTube（private） |
| 検査 | `scripts/qa_lint.py`、`scripts/script_lint.py`、`scripts/vp_check.py` | `out/` の完成品、台本 md | 警告一覧 |

素材は `assets/<slug>/` に置き、画像・音声は `.gitignore` でリポジトリへ入れない（1.1GB のため）。

## 2. 制作標準との差分

| 観点 | 制作標準（shorts-standard v1.0） | 既存の Shorts | 統合での扱い |
| --- | --- | --- | --- |
| 入力 | `brief.yaml`（題材・視聴者の疑問・出典URL・確認済み事実・留保） | 台本 md と人手の spec 生成 | `shorts/<slug>/brief.yaml` を必須の入口にした |
| 形式 | `output.schema.json`（title/hook/duration_sec/status/scenes/claims/needs_research） | `data/short_<slug>.json`（text/big/sub/src/art） | 標準 JSON を先に作り、`to-spec` で既存形式へ変換 |
| 時間 | 作者が start/end を設計（1シーン3〜9秒、計30〜45秒） | VOICEVOX の音声長から自動決定 | 標準側は目標値。実測で再計算されるのは従来どおり（標準も「実測音声で最終調整」と明記） |
| 根拠 | `claims[{id,statement,source_url,evidence_note}]`、シーンが `claim_ids` で参照 | `src`（画面の小さな出典ラベル）と `notes` の文章 | `claims` を `notes`/`refs` へ変換し、`src` は任意 |
| 公開可否 | `status` と `needs_research` | 無し（人の判断のみ） | `needs_review` では変換（レンダラ入力生成）を拒否 |
| 誘導 | 「無意味な登録誘導は禁止」 | `make_short2.py` が既定で CTA を付加 | `to-spec` は `cta: false` を出力（既存レンダラは未変更） |
| 画面テキスト | 1行14文字・2行以内 | `big`/`sub` に自由文 | 標準側で機械検査し、`caption[0]→big`、`caption[1]→sub` に写像 |
| 検査 | `validate.py`（形式）＋人の照合 | `qa_lint.py` 等（完成品向け） | `validate.py` をそのまま実行し、追加規則を重ねる |

## 3. 追加・変更したファイル

| ファイル | 内容 |
| --- | --- |
| `shorts-standard/`（5ファイル） | 原本を byte 一致で配置（README / PROMPT / brief.yaml / output.schema.json / validate.py）。**内容は変更していない** |
| `scripts/shorts_standard.py`（新規） | `new` / `brief-check` / `check` / `to-spec` / `list`。形式検査は標準の `validate.py` を subprocess 実行 |
| `tests/test_shorts_standard.py`（新規） | 16テスト。ルール値の緩和検知、PASS/FAIL の両例、`to-spec` の入出力 |
| `.github/workflows/shorts-standard.yml`（新規） | PR でユニットテスト＋`shorts/*/result.json` の全件検査 |
| `scripts/hooks/pre-commit`（新規）＋`install_git_hooks.py` | `shorts/<slug>/result.json` をコミット前に検査 |
| `shorts/sample_edo_map_compare/`（新規） | サンプル企画（brief.yaml ＋ result.json） |
| `AGENTS.md` | Shorts 制作は標準に従う、の節を追加 |
| `requirements.txt` | `jsonschema` / `pyyaml` を追加 |

既存の `scripts/make_short2.py`・`scripts/vp.py`・`data/short_*.json`・素材は変更していない。

## 4. 使い方

```bash
# 1. 企画の雛形
python scripts/shorts_standard.py new my_topic --topic "題材"

# 2. brief を実際の出典で埋めて検査
python scripts/shorts_standard.py brief-check shorts/my_topic/brief.yaml

# 3. PROMPT.md に従って shorts/my_topic/result.json を作り、検査
python scripts/shorts_standard.py check shorts/my_topic/result.json

# 4. ready になったらレンダラ用 spec へ変換（既定は shorts/<slug>/short_spec.json）
python scripts/shorts_standard.py to-spec shorts/my_topic/result.json \
  --art assets/my_topic/art_intro.png --pron data/my_topic_pronunciations.json

# 5. 従来どおり描画（VOICEVOX を起動しておく）
cp shorts/my_topic/short_spec.json data/short_my_topic.json
python scripts/make_short2.py my_topic

# 一覧
python scripts/shorts_standard.py list
```

`to-spec` は `data/` へ直接書かない（誤って公開バッチへ載らないようにするため）。

## 5. 検査の階層

1. `shorts-standard/validate.py` — 標準の形式（シーン数・尺・隙間/重複・claim 参照・needs_research と status）
2. `scripts/shorts_standard.py` の追加規則
   - ERROR: caption 14文字超・空行、`status=ready` なのに claims が空、claim の URL が http(s) でない、`evidence_note` が空、claim id の重複、`visual` が「関連画像を表示」等の禁止表現
   - WARN: 4〜5.5文字/秒の目安から外れる、0〜3秒に疑問が無い、8秒以内に根拠付きシーンが無い、映像種別（模式図/イメージ/資料）の明記漏れ、claim_ids の無いシーン
3. 人 — 出典の原文照合、読み、スマホ可読性、映像の誤認

## 6. サンプル企画の実行結果（`shorts/sample_edo_map_compare`）

題材は「江戸の古地図は、今の地図と重ねられる？」。出典は NDL の IIIF マニフェスト2点と NDLサーチ1点で、
2026-11-04 に metadata を実際に取得して確認した（`evidence_note` に確認内容を記載）。

| 実行 | 結果 |
| --- | --- |
| `brief-check` | ERROR 0（exit 0） |
| `check` | `validate.py PASS`、WARN 2（Scene 1 は claim_ids 無し＝フックのため／形式 PASS でも人の確認が必要） |
| `to-spec` | **中止**（`status=needs_review`）。未確認2件を表示 — 仕様どおりの拒否 |
| `python -m unittest tests.test_shorts_standard` | 16 tests OK |

`needs_research` に残した未確認事項:

- 2点の地図画像を実際に並べ、位置合わせの可否を人が目視で確認する
- 「慶長年間江戸図考」巻頭図と奥書の年を原本画像で確認する

→ このため `status` は `needs_review` のまま。`ready` にするには人が原文照合する。

## 7. 実レンダリング（edo_map_date）で分かった制約

制作標準に沿って1本を実際に描画した結果、既存レンダラ側の前提が3点見つかった。

| 制約 | 内容 | 対応 |
| --- | --- | --- |
| タイトルは1行・折り返し無し | `make_short2.py` は 58px で中央に1行描く。全角18文字程度を超えると左右が切れる | タイトルを13文字に短縮（レンダラは未変更） |
| `long_id` 必須 | 単独Shorts（対応する長尺が無い）では概要欄の生成で落ちる | `long_id` が無いときは案内行を出さないよう最小修正 |
| BGMのクレジット | 既定で魔王魂 piano12 を重ねる。素材の実態と合わない場合は概要欄が不正確になる | `to-spec --credit` で実際の素材を明記 |

実測（`out/short_edo_map_date.mp4`、git 管理外）:

- 1080x1920 / 30fps / h264 + AAC 48kHz ステレオ / **32.17秒**（設計36秒。音声長で決まる）
- 全編デコード: エラーなし
- loudnorm 実測: **-14.1 LUFS / True Peak -1.5 dBTP**（YouTube の目安に一致）
- 字幕 SRT はナレーションと1対1（`out/short_edo_map_date_subtitles.srt`）

## 8. 未対応・残課題

- **実測音声による時間調整**: 標準は作者が start/end を書くが、既存レンダラは音声長で再計算する。変換時に目標値を保持し、実測との差は従来どおり描画側に任せている。
- **読み（pron）の生成**: `to-spec` は `--pron` で既存の pronunciations JSON を指すだけ。新規題材の読み辞書づくりは従来どおり手作業。
- **素材画像の生成**: `visual` の指示から画像を作る工程は未接続（既存の `scripts/codex_art.py` などを利用）。
- **レンダリング確認**: サンプルは JSON と検証まで。VOICEVOX を起動した描画・全編の聴取・スマホ確認は行っていない。
- **既存 Shorts の移行**: `data/short_*.json`（旧形式）は変換していない。移行は別作業。
- **標準の更新**: `shorts-standard/` は原本コピー。上流が更新されたら差分を確認して置き換える（ルールを独断で変えない）。
