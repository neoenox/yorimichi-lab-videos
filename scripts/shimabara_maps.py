"""島原・天草の戦場図（assets/shimabara/map_*.png）。下地は現代の地形。実行： python scripts/shimabara_maps.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gmaps
VIEWS = {
    'area': dict(lon0=129.90, lon1=130.62, lat0=32.40, lat1=32.86, z=12),   # 島原半島・天草
    'wide': dict(lon0=129.70, lon1=131.00, lat0=32.30, lat1=33.65, z=10),   # 九州北西部
}
M = gmaps.Maps('shimabara', VIEWS)
def norm(lon, lat, view): return M.norm(lon, lat, view)
if __name__ == '__main__':
    M.build(sys.argv[1] if len(sys.argv) > 1 else None)
