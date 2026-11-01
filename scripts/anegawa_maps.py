"""姉川の戦場図（assets/anegawa/map_*.png）。gmaps.Maps を使う。下地は現代の地形。実行： python scripts/anegawa_maps.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gmaps
VIEWS = {
    'area': dict(lon0=136.19, lon1=136.41, lat0=35.37, lat1=35.48, z=14),   # 小谷城〜姉川〜横山城
    'core': dict(lon0=136.26, lon1=136.37, lat0=35.38, lat1=35.445, z=15),  # 姉川の南北岸
    'wide': dict(lon0=135.95, lon1=136.85, lat0=35.24, lat1=35.75, z=11),   # 敦賀・小谷・岐阜
    'mid': dict(lon0=136.235, lon1=136.36, lat0=35.385, lat1=35.466, z=14),   # 小谷城〜横山城（作り直し版：中心を拡大）
    'main': dict(lon0=136.282, lon1=136.352, lat0=35.393, lat1=35.445, z=15),  # 野村・三田村の主戦場（作り直し版）
}
M = gmaps.Maps('anegawa', VIEWS)
def norm(lon, lat, view): return M.norm(lon, lat, view)
if __name__ == '__main__':
    M.build(sys.argv[1] if len(sys.argv) > 1 else None)
