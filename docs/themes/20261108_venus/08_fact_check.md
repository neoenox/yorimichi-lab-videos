# 事実確認：金星では、1日が1年より長い？（確認日 2026-10-20）

| ID | 資料 | 確認できたこと |
|---|---|---|
| V1 | NASA(NSSDC) Venus Fact Sheet https://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html | 表（金星／地球／比）：Sidereal rotation period (hrs) −5832.6／23.9345／243.690。Length of day (hrs) 2802.0／24.0000／116.750。Sidereal orbit period (days) 224.701／365.256／0.615。Tropical orbit period (days) 224.695／365.242／0.615。Obliquity to orbit 177.36° |
| V2 | NASA(NSSDC) Notes on the Fact Sheets https://nssdc.gsfc.nasa.gov/planetary/factsheet/planetfact_notes.html | 「Negative numbers indicate retrograde (backwards relative to the Earth) rotation.」「Venus rotates in a retrograde direction, opposite the other planets」。Rotation Period：「the time it takes for the planet to complete one rotation relative to the fixed background stars」。Length of day の定義：「The average time in hours for the Sun to move from the noon position in the sky at a point on the equator back to the same position.」（2026-10-20に再取得して全文を確認） |

## 自作の計算（V1の数字から）
- 自転周期 5,832.6時間 ÷ 24 ＝ 243.025日（24時間を1日とした換算）。
- 公転周期 224.701日。自転 − 公転 ＝ 18.3日（自転のほうが長い）。
- Length of day 2,802.0時間 ÷ 24 ＝ 116.75日。
- 検算：自転と公転が逆向きのとき、1／自転＋1／公転＝1／昼夜の周期。1／243.025 ＋ 1／224.701 ＝ 0.008565、逆数は116.75日で、V1の値と一致（自作の計算）。
- 地球での検算：自転23.9345時間、公転365.256日、同じ向き：1／(1/0.99727 − 1/365.256) ＝ 24.00時間、V1の地球の値24.0000と一致。

## 骨格（台本に使える範囲）
- NASAの表では、金星の自転周期は5,832.6時間（日数にして約243日。符号がマイナスで逆向きの自転）、公転周期は224.701日。自転一回のほうが、公転一周より長い（V1・V2、自作の換算）。
- 同じ表の「Length of day」（太陽が空の同じ位置に戻る周期）は2,802.0時間＝116.75日で、公転周期より短い（V1）。
- 自転と公転が逆向きなので、太陽が戻るまでの時間は、自転周期より短くなる（V2＋自作の説明）。検算も一致。

## 確認していないこと（台本に入れない／限定する）
- 金星の自転周期の測定方法、時期による変化：未確認。
- 金星の地表から実際に太陽がどう見えるか（厚い雲）：未確認。
- 「1日」の一般的な意味は定義による、という整理は自作のまとめ。

## 見せ場（自作）
- 公転しながら自転する金星を、上から見た動く図。自転が1回転する間に、公転は1周を少し超える。太陽が空の同じ位置に戻る回数も数える。
- 周期の比較（自転243.0日／公転224.7日／昼夜の周期116.75日）の棒グラフ。
- 逆向きだと昼夜の周期が短くなることの検算（1/243.0＋1/224.7＝1/116.75）。

## 追加確認（2026-10-20）
- 天王星の表（https://nssdc.gsfc.nasa.gov/planetary/factsheet/uranusfact.html）：Sidereal rotation period −17.24（符号はマイナス）、Obliquity 97.77°。→「金星だけが逆向き」とは言わない。
