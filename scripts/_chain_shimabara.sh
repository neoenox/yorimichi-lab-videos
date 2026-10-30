cd /e/rekishikaisetu-honnoji
export PYTHONUTF8=1
python scripts/vp.py shimabara audio > out/shimabara_audio.log 2>&1 && python scripts/vp.py shimabara bgm >> out/shimabara_audio.log 2>&1
until [ -f assets/shimabara/art_sea.png ] && [ -f assets/shimabara/art_castle.png ]; do sleep 10; done
python scripts/_build_shimabara.py > out/shimabara_build.log 2>&1
echo CHAIN_DONE >> out/shimabara_build.log
