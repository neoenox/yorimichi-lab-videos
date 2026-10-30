import sys; sys.path.insert(0,'scripts'); sys.argv=['vp','shimabara']
import vp
vp.load_spec('shimabara'); vp.stage_build(chunk=4000)
