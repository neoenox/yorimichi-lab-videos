cd /e/rekishikaisetu-honnoji
export PYTHONUTF8=1
for s in shizugatake sekigahara yamazaki; do
  L=out/${s}_rebuild3.log
  python scripts/vp.py $s story > $L 2>&1
  python scripts/vp.py $s kana >> $L 2>&1
  python scripts/vp.py $s audio >> $L 2>&1 && python scripts/vp.py $s bgm >> $L 2>&1 && python -c "
import sys; sys.path.insert(0,'scripts'); sys.argv=['vp','$s']
import vp
vp.load_spec('$s'); vp.stage_build(chunk=4000)" >> $L 2>&1
  python scripts/vp.py $s desc >> $L 2>&1
  python scripts/vp.py $s pack >> $L 2>&1
  echo DONE_$s >> out/chain3_done.txt
done
echo ALL >> out/chain3_done.txt
