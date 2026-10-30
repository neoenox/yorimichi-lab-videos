cd /e/rekishikaisetu-honnoji
export PYTHONUTF8=1
python scripts/vp.py komaki audio > out/komaki_audio.log 2>&1 && python scripts/vp.py komaki bgm >> out/komaki_audio.log 2>&1 && python scripts/_build_komaki.py > out/komaki_build.log 2>&1
echo CHAIN_DONE >> out/komaki_build.log
