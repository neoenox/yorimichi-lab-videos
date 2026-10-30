cd /e/rekishikaisetu-honnoji
export PYTHONUTF8=1
L=out/vitaminc_build.log
python scripts/vp.py vitaminc audio > $L 2>&1 && python scripts/vp.py vitaminc bgm >> $L 2>&1 && python -c "
import sys; sys.path.insert(0,'scripts'); sys.argv=['vp','vitaminc']
import vp
vp.load_spec('vitaminc'); vp.stage_build(chunk=4000)" >> $L 2>&1
echo CHAIN_DONE >> $L
