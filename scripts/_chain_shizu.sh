cd /e/rekishikaisetu-honnoji
export PYTHONUTF8=1
python scripts/vp.py shizugatake kana > out/shizugatake_audio.log 2>&1
python scripts/vp.py shizugatake audio >> out/shizugatake_audio.log 2>&1 && python scripts/vp.py shizugatake bgm >> out/shizugatake_audio.log 2>&1 && python scripts/_build_shizu.py > out/shizugatake_build.log 2>&1
echo CHAIN_DONE >> out/shizugatake_build.log
