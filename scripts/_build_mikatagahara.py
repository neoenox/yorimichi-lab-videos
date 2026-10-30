import sys; sys.path.insert(0,'scripts'); sys.argv=['vp','mikatagahara']
import vp
vp.load_spec('mikatagahara'); vp.stage_build(chunk=4000)
