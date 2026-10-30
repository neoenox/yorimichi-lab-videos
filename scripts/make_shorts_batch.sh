#!/bin/bash
# usage: make_shorts_batch.sh slug:long_pack ...   Shortを作ってパックまで
cd /e/rekishikaisetu-honnoji; export PYTHONIOENCODING=utf-8
curl -s http://127.0.0.1:50021/version > /dev/null || { (nohup tools/voicevox/windows-cpu/run.exe --host 127.0.0.1 --port 50021 > logs/voicevox.log 2>&1 &); sleep 15; }
for p in "$@"; do s=${p%%:*}; lp=${p##*:}
  { python scripts/make_short2.py $s && python scripts/pack_short.py $s $lp; } > out/codex/short_${s}_build.log 2>&1 && echo "short_$s built $(date +%H:%M)" >> out/codex/short_progress.txt || echo "short_$s FAILED" >> out/codex/short_progress.txt
done
echo all >> out/codex/short_progress.txt
