cd /e/rekishikaisetu-honnoji
export PYTHONUTF8=1
python scripts/vp.py tedorigawa audio > out/tedorigawa_audio.log 2>&1 && python scripts/vp.py tedorigawa bgm >> out/tedorigawa_audio.log 2>&1
until [ -f assets/tedorigawa/art_flood.png ] && [ -f assets/tedorigawa/art_castle.png ]; do sleep 10; done
python scripts/_build_tedorigawa.py > out/tedorigawa_build.log 2>&1
echo CHAIN_DONE >> out/tedorigawa_build.log
