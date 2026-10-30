cd /e/rekishikaisetu-honnoji
export PYTHONUTF8=1
python scripts/vp.py mikatagahara audio > out/mikatagahara_audio.log 2>&1 && python scripts/vp.py mikatagahara bgm >> out/mikatagahara_audio.log 2>&1 && python scripts/_build_mikatagahara.py > out/mikatagahara_build.log 2>&1
echo CHAIN_DONE >> out/mikatagahara_build.log
