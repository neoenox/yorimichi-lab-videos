import sys; sys.path.insert(0,'scripts'); sys.argv=['vp','tottori']
import vp
vp.load_spec('tottori'); vp.stage_build(chunk=4000)
