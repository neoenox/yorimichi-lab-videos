cd /e/rekishikaisetu-honnoji
export PYTHONUTF8=1
python scripts/vp.py anegawa audio > out/anegawa_audio.log 2>&1 && python scripts/vp.py anegawa bgm >> out/anegawa_audio.log 2>&1
until [ -f assets/anegawa/art_dawn.png ] && [ -f assets/anegawa/art_castle.png ]; do sleep 10; done
python scripts/_build_anegawa.py > out/anegawa_build.log 2>&1
echo CHAIN_DONE >> out/anegawa_build.log
