#!/bin/bash
cd /e/rekishikaisetu-honnoji
for a in "vein 13_vein_blue 2026-10-20" "koku 04_edo_ichikoku 2026-10-21" "compass 10_compass_north 2026-10-23" "gdp 05_housework_gdp 2026-10-25" "season 11_season_distance 2026-10-27" "scurvy 07_scurvy_lind 2026-10-29" "calendar 09_calendar_meiji5 2026-10-30" "einstein 12_einstein_math 2026-11-03" "zenzen 08_zenzen_affirm 2026-11-06"; do
  set -- $a
  curl -s http://127.0.0.1:50021/version > /dev/null || { (nohup tools/voicevox/windows-cpu/run.exe --host 127.0.0.1 --port 50021 > logs/voicevox.log 2>&1 &); sleep 15; }
  bash scripts/republish.sh $1 $2 "$3 19:00"
done
echo all > out/codex/republish_done.txt
