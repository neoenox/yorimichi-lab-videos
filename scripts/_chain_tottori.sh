cd /e/rekishikaisetu-honnoji
export PYTHONUTF8=1
python scripts/vp.py tottori audio > out/tottori_audio.log 2>&1 && python scripts/vp.py tottori bgm >> out/tottori_audio.log 2>&1
until [ -f assets/tottori/art_mountain.png ] && [ -f assets/tottori/art_castle.png ]; do sleep 10; done
python scripts/_build_tottori.py > out/tottori_build.log 2>&1
echo CHAIN_DONE >> out/tottori_build.log
