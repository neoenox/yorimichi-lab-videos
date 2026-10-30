import sys; sys.path.insert(0,'scripts'); sys.argv=['vp','komaki']
import vp
vp.load_spec('komaki'); vp.stage_build(chunk=4000)
