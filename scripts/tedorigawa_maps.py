"""手取川の戦場図（assets/tedorigawa/map_*.png）。下地は現代の地形。実行： python scripts/tedorigawa_maps.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gmaps
VIEWS = {
    'area': dict(lon0=136.40, lon1=137.02, lat0=36.34, lat1=36.72, z=13),   # 小松〜手取川〜津幡
    'wide': dict(lon0=136.15, lon1=137.35, lat0=36.30, lat1=37.20, z=11),   # 加賀・能登
}
M = gmaps.Maps('tedorigawa', VIEWS)
def norm(lon, lat, view): return M.norm(lon, lat, view)
if __name__ == '__main__':
    M.build(sys.argv[1] if len(sys.argv) > 1 else None)
