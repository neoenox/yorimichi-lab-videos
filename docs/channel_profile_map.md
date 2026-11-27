# channel_profile の対応表（2026-11-19）

各slugの実績をどの動画から取ったかの表。**slug完全一致キー（`short_<slug>` → `short_solo_<slug>`）を最優先**し、その動画が未公開なら「同じslugを含むキーのShortで、タイトル類似度0.3以上の公開済み・最多再生」に切り替える。Shortが無いslugは長尺キー（`14_okehazama`等）を使う。
再生数はData APIの`statistics.viewCount`、平均視聴率はAnalytics API（`yt_analytics.py videos`）。未公開しか無いslugは0（公開後に再取得）。

| slug | 動画ID | 台帳キー | 公開 | 再生数 | 平均視聴率 | 変更前views | 備考 |
|---|---|---|---|---:|---:|---:|---|
| drain | `60hEGrmryiY` | short_drain | public | 1213 | 79.4 | 1208 | - |
| vein | `MI4uSQhWuTE` | short_vein | public | 1238 | 73.6 | 1238 | - |
| koku | `ku6FuXKerlI` | short_koku | public | 1226 | 123.1 | 1226 | - |
| compass | `RlCfl7JxMsk` | short_compass | public | 1221 | 73.5 | 1207 | - |
| gdp | `Y7hBNfHyxcQ` | short_gdp | public | 1175 | 53.7 | 1174 | - |
| season | `X0gVeS9KdNw` | short_season | public | 1260 | 72.1 | 1257 | - |
| scurvy | `holp8pd66r8` | short_scurvy | public | 1210 | 143.6 | 1209 | - |
| calendar | `2waqm6-Kqg4` | short_calendar | public | 1255 | 54.6 | 1177 | - |
| einstein | `5LTjdjdQDR4` | short_einstein | public | 1031 | 74.7 | 1026 | - |
| zenzen | `1zdEPEveReY` | short_zenzen | private | 0 | - | - | - |
| ninja | `BpZ7pce2htQ` | short_ninja | public | 98 | 39.7 | - | - |
| gm | - | - | - | - | - | - | 候補なし |
| honnoji | `bsbf0T-RslY` | short_honnoji | public | 2 | 74.9 | - | - |
| okehazama | `id1hjqjrztY` | 14_okehazama | public | 7 | 0.0 | - | 長尺のみ |
| nagashino | `kAfQ6KNRwf8` | short_solo_sandan_nagashino | public | 2 | 85.6 | - | Shortキー無し |
| sekigahara | `HVdstpUra9E` | short_sekigahara | public | 1027 | 81.8 | 291 | - |
| sunrise | `bbaSqiNWZeY` | short_sunrise | private | 0 | - | - | - |
| akashi | `LgePZBLaOTk` | short_akashi | public | 173 | 51.4 | - | - |
| leapsecond | `HFqz24ruHQM` | short_leapsecond | private | 0 | - | - | - |
| oceanblue | `dYAFL198wT4` | short_oceanblue | public | 172 | 52.3 | - | - |
| islands | `UIDRLw9UOXg` | 16_islands_count | public | 2 | 21.1 | - | 長尺のみ |
| rain30 | `myjfHXMUQ-4` | short_rain30 | public | 994 | 47.1 | - | - |
| gps | `j1WZYf-TXqU` | short_gps | public | 672 | 53.1 | - | - |
| shomi | `qX1IAFU91ak` | short_shomi | private | 0 | - | - | - |
| rice | `i6uM3eAXmlM` | short_rice | public | 378 | 103.2 | - | - |
| yakubusoku | `YdOyg6W-954` | short_yakubusoku | public | 330 | 54.7 | - | - |
| coldvirus | - | - | - | - | - | - | 候補なし |
| magnitude | `3dU7_-zVeQ0` | short_magnitude | private | 0 | - | - | - |
| moon | - | - | - | - | - | - | 候補なし |
| venus | `mCTDtQPfdbg` | short_venus | public | 2 | 18.9 | - | - |
| forest | `piQdBb8SsNY` | short_forest | private | 0 | - | - | - |
| lightning | `smfBjHIV_zA` | short_lightning | private | 0 | - | - | - |
| yamazaki | `_iQG1kUdoTc` | short_yamazaki | public | 1184 | 106.7 | - | - |
| shizugatake | `y1E14uWhmgg` | short_shizugatake | public | 967 | 62.3 | - | - |
| brain10 | `lwsPMoWRaDU` | short_brain10 | private | 0 | - | - | - |
| jikyu | `UEw9NhQ3EJk` | short_jikyu | private | 0 | - | - | - |
| bukka | `3QfMB3NnOzQ` | short_bukka | private | 0 | - | - | - |
| galileo | `MDUddXa0gos` | short_galileo | private | 0 | - | - | - |
| takarakuji | `xd1r2JzphLI` | short_takarakuji | private | 0 | - | - | - |
| flatearth | `PhT8Bjmx3Tw` | short_flatearth | private | 0 | - | - | - |
| vitaminc | `wJyBVJRvdeE` | short_vitaminc | private | 0 | - | - | - |
| komaki | `T9dn5K9Rgvg` | short_komaki | private | 0 | - | - | - |
| mikatagahara | `WJjnokAn-W4` | 33_mikatagahara | public | 7 | 13.8 | - | 長尺のみ |
| anegawa | `Y9f2PwDPBY0` | short_anegawa | public | 931 | 57.9 | - | - |
| tottori | `o_eahLXJpl0` | short_tottori | public | 261 | 81.0 | - | - |
| tedorigawa | `fOclvHna2bg` | short_tedorigawa | public | 201 | - | - | - |
| shimabara | `SJsfLzzAq1c` | short_shimabara | public | 143 | - | - | - |
