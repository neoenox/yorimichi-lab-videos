import sys; sys.path.insert(0,'scripts'); sys.argv=['vp','tedorigawa']
import vp
vp.load_spec('tedorigawa'); vp.stage_build(chunk=4000)
