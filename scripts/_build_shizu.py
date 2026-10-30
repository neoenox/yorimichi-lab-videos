import sys; sys.path.insert(0,'scripts'); sys.argv=['vp','shizugatake']
import vp
vp.load_spec('shizugatake'); vp.stage_build(chunk=4000)
