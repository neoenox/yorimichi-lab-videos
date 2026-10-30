"""鳥取城の戦場図（assets/tottori/map_*.png）。下地は現代の地形。実行： python scripts/tottori_maps.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gmaps
VIEWS = {
    'area': dict(lon0=134.12, lon1=134.32, lat0=35.46, lat1=35.56, z=14),   # 鳥取城・太閤ヶ平・賀露
    'wide': dict(lon0=133.75, lon1=134.45, lat0=35.30, lat1=35.62, z=11),   # 羽衣石〜鳥取
}
M = gmaps.Maps('tottori', VIEWS)
def norm(lon, lat, view): return M.norm(lon, lat, view)
if __name__ == '__main__':
    M.build(sys.argv[1] if len(sys.argv) > 1 else None)
