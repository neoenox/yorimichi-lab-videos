# モデル比較検証（第2回：姉川の戦い・三部構成）各モデルに貼る指示文

第1回（信号の青）からの変更点
- 題材：姉川の戦い（10章・約6.6分・地図の上で武将を動かす）。台本は `docs/themes/20261104_anegawa3/09_script_v2.md`。
- **静止画（still）の確認を減らした**（build 前に最大6か所。build 後は撮らない）。
- BGMは、第1部・第2部・第3部の主題に合わせて、3曲以上を使い分ける。

使い方
1. 3モデルを、1つずつ順番に動かす（書き出しとVOICEVOXを共有するため、同時には動かさない）。
2. 下の指示文の `<SLUG>` を、次のように置き換えて貼る（`<SLUG>` のままにしない）。
   - Sonnet 5.5 → `anesonnet`／GPT-6 Luna → `aneluna`／DeepSeek V4.1 Flash → `anedeepseek`
3. 貼ったあとは、助言を出さない。質問されたら「指示文のとおりに判断して進めて」とだけ返す。
4. 終わったら最終報告をコピーして、`docs/MODEL_COMPARISON_LOG.md` に貼る。開始・終了時刻とトークン数（料金）は、あなたが記録する。

---

## 共通の指示文（ここから下を貼る）

```
あなたは、動画制作ライン scripts/vp.py を使って、解説動画を1本（約6〜7分）作る担当です。
作業フォルダは E:\rekishikaisetu-honnoji です。あなたの slug は <SLUG> です。
これは、モデルの比較検証です。ほかのモデルにも、同じ指示で同じ動画を作らせています。
人間は途中で助言しません。迷ったら、この指示文のとおりに自分で判断して進めてください。

# 0. 着手前に読むもの（全文）
1) AGENTS.md
2) docs/VIDEO_CREATION_PRECHECK.md
3) docs/VIDEO_PIPELINE_VP.md
4) docs/VIDEO_PRODUCTION_RUNBOOK.md の「ユーザーからの指摘と、動画づくりの決まり」の節と、「画面スタイル「ポップ」」の節
5) 参考にしてよい完成例（読むだけ）：data/mikatagahara_spec.json と scripts/make_spec_mikatagahara.py（戦況地図 battle_map の使い方）、scripts/vp_anim_c.py の battle_map の説明、scripts/vp_anim_pop.py の先頭の説明
6) 事実の根拠：docs/themes/20261205_anegawa/08_fact_check.md（読むだけ）
全文を読めなかったものがあれば、動画づくりに着手せず、その理由を報告して止まってください。
最初の報告で、事前確認を済ませたことと、今回適用する要点を一言で示してください。

# 1. 台本（固定）
台本は docs/themes/20261104_anegawa3/09_script_v2.md です。**1文字も変えてはいけません。このファイルは読むだけです。**
題材：姉川の戦い。三部構成。
 第1部＝開戦にいたるまでの経緯（章1〜3）
 第2部＝開戦時の各武将の動きを、地図の上で表現（章4〜8）
 第3部＝戦いの後の簡単な説明（章9〜10）
章のキーは、この順に固定します：kanegasaki / june / cast / terrain / dawn / west / east / decide / kubi / after。
出典の区別〔N〕〔軍〕〔通説〕〔説〕を、画面でも保つこと。「とされる」「伝わる」「説がある」を、断定に変えない。
研究者の名前を、画面に出さない。「圧勝」「大勝」と書かない。

# 2. 使ってよい素材（これだけ）
- 地図：assets/anegawa/map_wide.png / map_main.png / map_mid.png / map_area.png / map_core.png（どの縮尺で、どの章に使うかは、自分で決める。画像を見て、場所の座標を決めること）
- 背景イラスト：assets/anegawa/art_castle.png / art_dawn.png / art_docs.png / art_river.png
- 肖像：assets/portraits/ のうち、人物が合うもの（例：nobunaga, ieyasu, nagamasa, honda_t=本多忠勝, hideyoshi, shibata, sakai_t）。ない人物は、肖像なしの印（ラベルだけ）にする。
- BGM：assets/bgm_maou/ の曲（下の第6節を見る）。
- 画面部品：style='pop' の部品、battle_map、pop_rows、pop_telop、pop_card など既存の部品。
- 新しい画像を作ったり、外から取ってきたりしない。音声は VOICEVOX の既定のまま。サムネイルは作らない。
- 既存の姉川の動画の成果物（data/anegawa_*、scripts/make_spec_anegawa*、out/anegawa*、upload/*anegawa* など）は、**読まない・使わない**（答えの丸写しになるため）。

# 3. 作るもの（この slug の名前のファイルだけ）
1) data/<SLUG>_pronunciations.json（読みの辞書）
2) scripts/make_spec_<SLUG>.py と data/<SLUG>_spec.json（style='pop'、theme_dir は '20261104_anegawa3'、pack は 'cmp3_<SLUG>'）
3) vp.py の段階を、この順に実行：
   python scripts/vp.py <SLUG> story → kana → audio → bgm → build
   （`at` は台本の行ではなく「文」の番号。書く前に python scripts/vp.py <SLUG> sents で番号を確かめる）
4) 出来上がった動画 out/<SLUG>_video.mp4 を確認し、直す必要があれば直して再ビルドする。

# 4. 画面の決まり
- 第2部（章4〜8）は、地図の上で表現する：
  ・地名（小谷城・横山城・竜ヶ鼻・大依山・姉川・野村・三田村）を、地図の位置に置く。位置は、地図の画像を見て決める。
  ・開戦時の各武将・軍勢（徳川・朝倉・織田馬廻・美濃三人衆・浅井・磯野員昌・本多忠勝 など）の動きを、ナレーションの文に合わせて、地図の上で動かす（battle_map の units の legs。動きは文の番号で書く）。
  ・出典で割れる話（本多忠勝がどちらへ突入したか／十一段崩し／榊原康政の側面攻撃）は、軍を1つの説の動きとして断定的に動かさない。伝承として、印や吹き出しで、控えめに見せる。
- 肖像は、基本的に隠さない。ラベルや板を、肖像に重ねない。
- 画面の文字は、字幕の帯（y 836より下）に重ねない。枠や画面外にはみ出さない。1文字だけの折り返しを作らない。
- 全章に、図かテロップか背景写真がある。文字だけの章を作らない。同じ背景が長く続かないようにする。
- 表やグラフは、スマホで読める大きさにする。「≒」は使わない（「＝約」と書く）。
- 読み間違いが起きやすい語（姉川、竜ヶ鼻、野村、三田村、磯野員昌、遠藤直経、真柄十郎左衛門、横山城、大依山、卯の刻、首注文、定番 など）は、kana の結果を全文読んで確かめ、辞書で直す。
- 台本にない主張を、画面に足さない。

# 5. してはいけないこと
- scripts/ の既存ファイル（vp.py、vp_anim*.py など）、他の slug のファイル、assets/ の既存ファイル、台本を、書き換えない。新しく作るのは、第3節のファイルだけ。
- 他の比較用 slug（sigsonnet / sigluna / sigdeepseek / anesonnet / aneluna / anedeepseek のうち、自分以外）の data/・out/ を読まない。
- git の commit・push・ブランチ操作をしない。YouTube へのアップロードや予約をしない。作業フォルダの外へ書き込まない。
- 動画の書き出しは、同時に1本だけ。環境変数 VP_MAXPAR=3 を付けて実行する。

# 6. BGM（部ごとに主題に合わせる）
spec の bgm に、[開始章key, 終了章key, 曲名] を並べる（曲名は assets/bgm_maou/maou_bgm_<曲名>.mp3 の <曲名>）。
 - 第1部（kanegasaki〜cast）：緊迫を含みつつ静かな曲（例：piano 系、acoustic 系、または ethnic 系）。
 - 第2部（terrain〜decide）：戦いの高まりに合う曲。章の切れ目（terrain/dawn の静けさ→west/east/decide の戦い）で、曲を切り替えてよい（orchestra 系 ほか）。
 - 第3部（kubi〜after）：戦いのあとの余韻・静けさに合う曲（piano／ethnic／acoustic のいずれか）。
曲は全体で3曲以上、部ごとに違う曲にする。選んだ曲と、その理由を、最後の報告に一行ずつ書く。曲を聴いて選ぶことはできないので、曲名の系統（piano/orchestra/ethnic/acoustic）と章の内容から判断してよい。

# 7. 確認の方法（変更あり）
- 静止画（vp.py <SLUG> still <秒>）で見るのは、build の前に、全体で最大6か所まで。第2部の地図の場面を優先する。
- build のあとは、静止画を撮り直さない。build と qa の結果（build の成否、qa の判定）で確かめる。
- 確認の頻度は、あなたが必要だと判断した回数でよいが、1回の作業ごとに毎回撮らない。
- assert などのエラーで build が止まったときの原因調査のためだけは、still を使ってよい（回数に数えない）。

# 8. 上限
- 再ビルドは、全体で3回まで。作業時間は、3時間まで。
- 途中で止まった・直せなかったことは、隠さず、そのまま報告する（失敗の記録は、成績の一部です）。

# 9. 最後の報告（この形で書く）
- 完成したか（out/<SLUG>_video.mp4 のパス、長さ、build と qa の結果）
- 確認できたこと（どの秒の静止画で何を確かめたか）／確認できていないこと（通しで再生していない、など）
- 選んだBGM（部ごとの曲名と理由）
- 直した不具合の一覧と、再ビルドの回数
- 残っている不具合（分かっているもの）
- 台本を変えていないことの確認（字幕と台本の差分）
- 使った時間
動画の生成やデコードに成功しただけで、「視聴品質が良い」「投稿できる」とは書かないでください。
```
