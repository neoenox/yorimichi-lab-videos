# 画像の権利（長篠の戦い）

## 肖像（Wikimedia Commons。`scripts/fetch_portraits_nagashino.py`、記録 `data/portraits_nagashino.json`）
| 人物 | 所蔵・制作 | Commons | 備考 |
|---|---|---|---|
| 武田勝頼 | 高野山持明院蔵、16世紀後半、作者不明（部分） | File:Takeda_Katsuyori.jpg | 日本の著作権法で保護期間満了（Commonsの記載） |
| 酒井忠次 | 先求院蔵、16世紀末〜17世紀初 | File:Sakai_Tadatsugu.jpg | 同上。画像は背景の色が鮮やかに加工されて見える（Commons掲載画像の状態）。画面では「肖像（先求院蔵）」と注記 |
| 馬場信春 | 恵林寺（信玄公宝物館）蔵、江戸時代か（不確か） | File:Baba_Nobufusa.jpg | PD-Art（忠実な複製）。制作年代が不確かなので「肖像（制作年代は不確か）」と注記 |
| 山県昌景 | 浮世絵（画面に「甲陽二十四将」「国芳画」の署名と読める。歌川国芳の連作と思われる＝江戸時代後期）。Commonsの記載は「出典 Japon、16世紀」で誤り | File:Masakage_Yamagata.jpg | **肖像画ではなく、後世の浮世絵（想像図）**。画面では「浮世絵（江戸時代後期）。想像図」と注記する。Commonsの制作年の記載は採らない |
| 奥平信昌 | 久昌院蔵、1615年ごろ、絹本着色 | File:Okudaira_Nobumasa.jpg | Public Domain Mark |
| 織田信長・徳川家康 | 既存 `assets/portraits/nobunaga.jpg`・`ieyasu.jpg`（関ヶ原・桶狭間で使用） | — | 既存の権利記録を確認 |

- 肖像は**後世に描かれたものを含む**。画面には「肖像（後世の作）」などと注記し、**本人の顔の実像だと断定しない**。
- 画像の取得：Commons は回数制限（HTTP 429）をかけるので、間を空けて取得する（スクリプトに再試行を実装）。

## 地図
- 国土地理院タイル（陰影起伏図・標準地図）を加工（出典表示：「地理院タイル（陰影起伏図）を加工して作成」）。
- 位置の座標（`data/nagashino_places.json`）：Wikipedia／Wikidata の座標、OpenStreetMap（© OpenStreetMap contributors、ODbL）、国土地理院の住所検索。**鳶ノ巣山砦・信長/家康の陣・馬防柵の位置は要確認**（地図には「推定」と明記する）。

## 背景イラスト
- ChatGPT（OpenAI）による生成。地図の章には敷かない。画風は戦国の絵巻・屏風絵風を検討。

- 取得：Wikimedia の画像サーバーが回数制限（HTTP 429）で直接取得できなかったため、WebFetch 経由で取得した（ファイルは同一の upload.wikimedia.org のURL）。
- 顔の切り出し位置：`data/nagashino_crops.json`（円形の駒に使う）。
