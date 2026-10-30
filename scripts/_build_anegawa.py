import sys; sys.path.insert(0,'scripts'); sys.argv=['vp','anegawa']
import vp
vp.load_spec('anegawa'); vp.stage_build(chunk=4000)
