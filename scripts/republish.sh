#!/bin/bash
# usage: republish.sh <slug> <pack> <publishAt "YYYY-MM-DD HH:MM">
# 音声(字幕SRT)→ends→build→desc→pack→新版アップ→旧版削除→公開予約。失敗したらそこで止まる。
cd /e/rekishikaisetu-honnoji; export PYTHONIOENCODING=utf-8
s=$1; pack=$2; at=$3; L=out/codex/${s}_republish.log
{ python scripts/vp.py $s audio && python scripts/vp.py $s ends && python scripts/vp.py $s build && python scripts/vp.py $s desc && python scripts/vp.py $s pack; } > $L 2>&1 || { echo "$s BUILD FAILED" >> out/codex/republish_progress.txt; exit 1; }
id=$(python scripts/yt_api.py upload $pack --new-version 2>&1 | tee -a $L | grep "video id" | awk '{print $3}')
[ -n "$id" ] || { echo "$s UPLOAD FAILED" >> out/codex/republish_progress.txt; exit 1; }
python scripts/yt_api.py delete-superseded >> $L 2>&1
python scripts/yt_api.py schedule $id "$at" >> $L 2>&1
echo "$s OK $id $at" >> out/codex/republish_progress.txt
