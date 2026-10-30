#!/bin/bash
# 字幕の数字表記だけを直して作り直す。usage: rebuild_subs.sh slug ...
cd /e/rekishikaisetu-honnoji; export PYTHONIOENCODING=utf-8
for s in "$@"; do
  { for st in audio bgm ends build desc pack; do python scripts/vp.py $s $st || exit 1; done; } > out/codex/${s}_rebuild.log 2>&1 && echo "$s rebuilt $(date +%H:%M)" >> out/codex/rebuild_progress.txt || echo "$s REBUILD FAILED" >> out/codex/rebuild_progress.txt
done
echo all >> out/codex/rebuild_progress.txt
