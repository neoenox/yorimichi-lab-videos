# 事実確認：GPS衛星は、あなたの居場所を知っている？（確認日 2026-10-21）

型の候補：C 仕組み（段階的な図解）。答え先出し「知らない。衛星は自分の位置と時刻を流しているだけ」。

| ID | 資料 | 確認できたこと |
|---|---|---|
| G1 | GPS.gov「How GPS Works」ポスター http://archive.gps.gov/multimedia/poster/poster.txt | 「GPS satellites broadcast radio signals providing their locations, status, and precise time (t1) from on-board atomic clocks.」受信機は到着時刻（t2）を記録し、distance = rate x time（rate は光速）で距離を出す。「Once a GPS device knows its distance from at least four satellites, it can use geometry to determine its location on Earth in three dimensions.」衛星へのデータ送信は地上のアンテナが行う（受信機は含まれない） |
| G2 | GPS.gov「GPS and Telling Time」https://www.gps.gov/gps-and-telling-time | 「Each GPS satellite contains multiple atomic clocks...」「GPS receivers decode these signals, effectively synchronizing each receiver to the atomic clocks.」「provides a critical fourth dimension – time」 |
| G3 | GPS.gov 衛星の説明（archive）https://archive.gps.gov/systems/gps/space/ | 「The GPS space segment consists of a constellation of satellites transmitting radio signals to users.」運用の衛星は2023年7月3日時点で31基、高度は約20,200km（中軌道）、運用は米国宇宙軍 |
| G4 | NASA Space Place「How Does GPS Work?」https://spaceplace.nasa.gov/gps/en | 衛星は常に信号を送り出し、受信機は聞き取り、4基以上との距離を計算して位置を決める。30基以上 |
| G5 | GPS.gov（SPS性能規格等）| 民生の基本のGPSサービスは、95%の時間で約8m以内（検索で得た要約。**原典で再確認**）|
| G6 | MIT Engineering Ask an Engineer（二次）https://engineering.mit.edu/ask-an-engineer/could-a-gps-device-reveal-my-location-to-others | 位置の計算は受信機の中で行われる。ただし位置履歴の記録や、通信機能（スマホの電波）が位置を外へ送ることはある |

## 骨格（台本に使える範囲）
- 衛星は、自分の位置・状態・正確な時刻を、全方向へ流している（G1）。
- 受信機は、信号が届くまでの時間×光速で、衛星までの距離を出す。4基以上の距離があれば、3次元の位置が決まる（G1）。4つ目の衛星は時刻のずれの分（G2のfourth dimension＝時刻。「4つの未知数＝緯度・経度・高度・受信機の時計のずれ」は別の公式説明にもある。公開前に原文で確認）。
- 受信機から衛星へ信号を返す説明はない。衛星は、誰が聞いているかを知らない（G1/G4。「返さない」ことを明記した公的な文は未確認＝ナレーションは「そう設計されている」ではなく「公式の説明では、衛星が送るのは位置と時刻」まで）。
- 位置を外に知らせるのは、スマホの通信やアプリの側（G6、二次資料）。
- 衛星は約20,200km上空に31基（2023年7月時点）、米国宇宙軍が運用（G3）。

## 要確認（台本の前に）
- 「受信機は衛星に何も送らない」の断言根拠：GPS.govの規格（IS-GPS-200等）か、GPS.govの説明の一次文。見つからなければ弱める。
- 衛星の基数は「今」の数。動画では「2023年時点で31基」と日付つきで言うか、「30基ほど」にとどめる。
- 「約8m」は原典（GPS.govのaccuracyページ。URLが変わった可能性）で確認。
- 「GPSは位置を知らせてくれる＝衛星が探してくれる」と誤解されやすい点の出どころ（アンケートがあれば）。なければ「よくある誤解」とは言わず、「そう思いがち」と柔らかく。
- 相対性理論の補正（時計のずれ）は面白いが、本題から外れる。入れるなら一次資料を別に確認。

## 見せ場（自作）
- 衛星4基から円が広がり、交点で位置が決まる図。受信機の側が計算していることを矢印で示す（矢印は衛星→受信機の一方向のみ）。

## 追記 2026-10-21（ChatGPT査読の裏取り）
- **GPS.gov FAQ・位置情報のプライバシーのページ（検索結果で確認）**：「The GPS satellites themselves do not track anything on the ground. They are simply beacons, like lighthouses, broadcasting one-way reference signals. Therefore, the government operators of GPS cannot locate your phone/device.」プライバシーのページ：政府の衛星は、人や地上のものを追跡できない一方向の灯台のようなもの。ただし、通信や記録の機能を持つ市販のGPS機器は、追跡に使える。→ 「受信機は何も返さない」と書いた文を探す必要はなくなった。
- 衛星数：GPS.govのSpace Segmentは2023-07-03で31基、同じ日付のFAQでは25基（ChatGPT指摘）。**衛星数は言わない**。
- 時間差×光速は擬似距離（受信機の時計のずれ等を含む）。未知数は、東西・南北・高さ・時計のずれの4つ（米国沿岸警備隊Navcen資料。URL未確認）。

## 追記2 2026-10-21（原文で確認）
- **GPS.gov FAQ（https://www.gps.gov/faq 、原文を取得して確認）**：質問「I lost my mobile phone/device. Can GPS help me find it?」への回答。「Please be aware that the GPS satellites themselves do not track anything on the ground. They are simply beacons, like lighthouses, broadcasting one-way reference signals. Therefore, the government operators of GPS cannot locate your phone/device.」＋「We recommend you contact your wireless carrier. They may be able to track down your phone/device using the location technology built into it.」→ 台本の「衛星は追跡していない／灯台のように一方向／運用する政府は位置を特定できない」と一致。携帯会社など、端末側の技術なら探せる場合があるという文脈も同じFAQにある。
- **Navcen「NAVSTAR GPS User Equipment Introduction」(1996) https://navcen.uscg.gov/sites/default/files/pubs/gps/gpsuser/gpsuser.pdf（PDF本文を取得して確認）**：p.13「a minimum of four satellites are normally required to be simultaneously "in view" of the receiver, thus providing four range measurements. This enables the receiver to calculate the three unknown parameters representing its (3-D) position, as well as a fourth pa[rameter...]」、p.17「the user position coordinates and the user clock offset are calculated using simultaneous equations. Four satellites are normally required」、p.23「pseudorange measurement, rather than a range measurement, because the receiver's clock bias has not been removed」。→ 「4つ（東西・南北・高さ＋時計のずれ）を求める」「おおよその距離」の根拠として確認済み。
- GPS.gov「How GPS Works」ポスターの文面（http://archive.gps.gov/multimedia/poster/poster.txt）は、前回、原文で確認済み。
