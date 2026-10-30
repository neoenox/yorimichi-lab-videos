#!/bin/bash
# 全動画の作り直し（アップ前まで）。usage: build_all.sh slug ...
cd /e/rekishikaisetu-honnoji; export PYTHONIOENCODING=utf-8
for s in "$@"; do
  curl -s http://127.0.0.1:50021/version > /dev/null || { (nohup tools/voicevox/windows-cpu/run.exe --host 127.0.0.1 --port 50021 > logs/voicevox.log 2>&1 &); sleep 15; }
  { python scripts/vp.py $s audio && python scripts/vp.py $s ends && python scripts/vp.py $s build && python scripts/vp.py $s desc && python scripts/vp.py $s pack; } > out/codex/${s}_build_all.log 2>&1 && echo "$s built $(date +%H:%M)" >> out/codex/build_all_progress.txt || echo "$s BUILD FAILED" >> out/codex/build_all_progress.txt
done
echo all > out/codex/build_all_done.txt
