# 全ソース到達性レビュー（2026-11-19）

## 範囲と方法

- 対象: `docs/themes/` 96テーマ・Markdown 454ファイルに書かれた URL。重複を除き **206件**。
- 方法: MarkdownからURLを抽出し（`）` や日本語の注釈を除けて正規化）、`curl -L` でHTTPステータスを取得。2026-11-19に実施。
- **このレビューは到達性のみ**。各テーマの記述と原文の内容が一致するか（事実照合）は全件では実施していない。

## 結果

| 区分 | 件数 |
|---|---:|
| 200（到達） | 178 |
| 202 / 203（受付・非標準） | 3 |
| 302（リダイレクト） | 1 |
| 実質的に死んだリンク（404×3, 410×1） | **4** |
| 403（Bot遮断の可能性） | 5 |
| 429（レート制限） | 6 |
| 接続不可（TLS/タイムアウト） | 4 |
| 500（Amazon） | 1 |

## 死んだリンク（要対応）

| ステータス | URL | 使われている場所 |
|---|---|---|
| 404 | `https://digital.library.adelaide.edu.au/items/39c638be-140c-4c34-a71a-bd17f5234c8a` | `docs/themes/20261017_batch2/03_candidates_codex.md:138` |
| 404 | `https://www.chuko.co.jp/shinsho/portal/128511.html` | `docs/themes/20261212_yamazaki/08_fact_check.md:7` |
| 404 | `https://www.city.komaki.aichi.jp/admin/soshiki/kyoiku/bunkazai/1_1/2/bunkazai/9161.html` | `docs/themes/20261226_komaki_nagakute/08_fact_check.md:8` |
| 410 | `https://www.nssl.noaa.gov/education/svrwx101/lightning/faq/` | `docs/themes/20261018_batch3/03_candidates_codex.md:161` |

内容は別の一次資料で確認済みの可能性があるが、**このレビューではURLの到達性だけを確認した**。参照先を差し替えるか、古い候補なら削除する。

## 自動検査では到達できなかったリンク（要手動確認）

| 区分 | URL（代表） | 使われている場所 |
|---|---|---|
| 403 | `https://www.city.fukuoka.lg.jp/shishi/kankou01.html` | `20261205_sekigahara/11_source_check.md:74` |
| 403 | `https://doi.org/10.1175/1520-0469...`（JASMSの論文） | `20261017_drain/12_codex_script_review.md:5` |
| 403 | `https://hls-dhs-dss.ch/de/articles/028814` | `20261018_einstein/08_fact_check.md:8` |
| 403 | `https://navcen.uscg.gov/.../gpsuser.pdf` | `20261114_gps/08_fact_check.md:38` |
| 403 | `https://www.moma.org/calendar/exhibitions/3639?locale=en` | `20261018_batch3/03_candidates_codex.md:65` |
| 429 | Wikipedia / Wikisource 6件（銀座・築地・信長公記・甲陽軍鑑ほか）、Met Museum 2件 | `20271101_ginza`, `20261019_okehazama`, `20261018_batch3` |
| TLS/timeout | `www.aoml.noaa.gov/hrd/tcfaq/D3.html` ほか3件、`dhayton.haverford.edu` | `20261017_drain`, `20261017_batch2`, `20270213_galileo` |
| 500 | `https://www.amazon.co.jp/dp/4584121672` | `20261019_okehazama/08e_source_check_researchers.md:29` |

403/429はBot遮断・レート制限の可能性が高く、リンク切れと即断しない（ブラウザで開ける場合は問題なし）。`www.aoml.noaa.gov` はWindowsのSchannelでTLSハンドシェイクが失敗するだけで、ブラウザからは開ける例がある。

## 出典の種類（参考）

- 非常に多いドメイン: `dl.ndl.go.jp` 14件、`ja.wikipedia.org` 10件、`commons.wikimedia.org` 9件、`www.maff.go.jp` 9件、`eco.mtk.nao.ac.jp` 8件、`www.mlit.go.jp` 6件、`www.gsi.go.jp` 5件、`www.jma.go.jp` 5件。
- 行政・大学・研究機関（`.go.jp` `.ac.jp` `.or.jp` 等）が多数を占める。Wikipediaは10件だが、一次資料の補助や比較として使われている文脈が多く、**このレビューでは各記述が一次資料で裏取られているかは判定していない**。
- 詳細は `out/_url_check_v4.json`（git管理外）にURL・ステータス・最終URL・エラーを保存した。

## 未実施

- 206URLすべての本文取得と、台本・事実確認メモの記述との突き合わせ。
- YouTube / SNS の動画内で使った出典の表示の監査。
- 有料書籍・紙の資料の現物照合。
