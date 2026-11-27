# 味覚マップ：公開後の確認準備（2026-11-23）

## 目的

「誤解を覆すインパクト＋知的な納得感」型の人体科学ネタが、既存の同型動画と比べてどう伸びたかを、同じ条件で記録する。

## 比較対象

| slug | 動画ID | 公開予定（JST） | 種別 |
| --- | --- | --- | --- |
| `short_solo_tongue_taste_map` | `cO0Rhp25ue0` | 2026-11-25 11:00 | 今回（味覚マップ） |
| `short_solo_vein_aoi` | `SdalO8INdc4` | 2026-12-01 17:00 | 静脈が青い（誤解型・人体） |
| `short_solo_brain_damage` | `wGBxb4DzOKM` | 2026-12-05 19:00 | 脳の9割（誤解型・人体） |

※ 公開日時は `yt_api.videos().list(part='status')` の `publishAt`（UTC）を JST に換算した値。2026-11-23 時点では3本とも公開前で、`viewCount` / `likeCount` / `commentCount` はすべて0。

## 確認方法

公開から最低2日あけてから拾う。Analytics は1〜2日遅れるので、APIの再生数とは日を分けて記録する。

```
$env:PYTHONUTF8='1'
$env:PYTHONPATH='C:\Users\neoen\AppData\Local\Programs\Python\Python311\Lib\site-packages'
python -c "import sys; sys.path.insert(0,'scripts'); import yt_api; s=yt_api.service(); r=s.videos().list(part='snippet,statistics,status',id='cO0Rhp25ue0').execute()['items'][0]; print(r['statistics'])"
```

X の紹介投稿の効果は、Studio の Ask Studio で「X」からの外部流入を見る（APIでは取れない）。

## 記録すること

- 公開から24時間後、72時間後の `viewCount` / `likeCount` / `commentCount`
- 登録者数の増分（チャンネル単位なので、他の予約動画の影響に注意）
- コメントの内容（「ためになる」「自分でも試した」のような反応が出るか）
- X 経由の流入の有無
- 比較対象2本も同じ日数で拾い、公開直後の伸びを比べる

## 注意

- 1日の公開本数が6〜8本あるので、登録者数の増分は今回の動画単独の効果とは限らない。
- 比較は同じ経過日数でそろえる。日付が違う動画を混ぜない。
- 日が浅い動画・コメントが少ない動画の数字だけで判断しない。
