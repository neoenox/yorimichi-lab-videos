cd /e/rekishikaisetu-honnoji
export PYTHONUTF8=1
python scripts/codex_watch.py yamazaki docs/themes/20261212_yamazaki > out/codexwatch_yamazaki.log 2>&1
python scripts/codex_watch.py shizugatake docs/themes/20261219_shizugatake > out/codexwatch_shizu.log 2>&1
python scripts/codex_watch.py sekigahara docs/themes/20261205_sekigahara > out/codexwatch_seki.log 2>&1
echo ALLDONE > out/codexwatch_done.txt
