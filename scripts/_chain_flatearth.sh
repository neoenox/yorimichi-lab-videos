cd /e/rekishikaisetu-honnoji
export PYTHONUTF8=1
L=out/flatearth_build3.log
python scripts/vp.py flatearth kana > $L 2>&1 && python scripts/vp.py flatearth audio >> $L 2>&1 && python scripts/vp.py flatearth bgm >> $L 2>&1 && python -c "
import sys; sys.path.insert(0,'scripts'); sys.argv=['vp','flatearth']
import vp
vp.load_spec('flatearth'); vp.stage_build(chunk=4000)" >> $L 2>&1 && python scripts/vp.py flatearth desc >> $L 2>&1 && python scripts/vp.py flatearth thumb >> $L 2>&1 && python scripts/vp.py flatearth pack >> $L 2>&1 && python scripts/make_short2.py flatearth >> $L 2>&1 && python scripts/pack_short.py flatearth 31_flatearth >> $L 2>&1
echo CHAIN_DONE >> $L
