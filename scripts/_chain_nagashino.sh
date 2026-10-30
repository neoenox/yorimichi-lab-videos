cd /e/rekishikaisetu-honnoji
export PYTHONUTF8=1
python scripts/vp.py nagashino story > out/nagashino_rebuild.log 2>&1
python scripts/vp.py nagashino kana >> out/nagashino_rebuild.log 2>&1
python scripts/vp.py nagashino audio >> out/nagashino_rebuild.log 2>&1 && python scripts/vp.py nagashino bgm >> out/nagashino_rebuild.log 2>&1 && python -c "
import sys; sys.path.insert(0,'scripts'); sys.argv=['vp','nagashino']
import vp
vp.load_spec('nagashino'); vp.stage_build(chunk=4000)" >> out/nagashino_rebuild.log 2>&1
echo CHAIN_DONE >> out/nagashino_rebuild.log
