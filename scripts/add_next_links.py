"""長尺動画の概要欄に「次の動画」リンクを追加する。
youtube_ids.json のキー（01_xxx 形式）を使ってシリーズごとに順序を決める。
usage: python scripts/add_next_links.py --dry
       python scripts/add_next_links.py
"""
import sys, json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))
import yt_api  # noqa: E402

DRY = '--dry' in sys.argv

# --- シリーズ定義：youtube_ids.json のキーで順序を決める ---
SERIES = {
    # 東京の低地（再生リストあり・概要欄に既にリストURLあり）
    'tokyo_lowland': ['79_hibiya', '78_shibuya', '80_ginza'],
    # 合戦シリーズ（年代順）
    'battle': ['14_okehazama', '33_mikatagahara', '26_nagashino', '34_anegawa', '32_komaki',
               '36_tedorigawa', '28_yamazaki', '29_shizugatake', '35_tottori', '27_sekigahara'],
    # 江戸くらし（tokyo_lowland タグが付く地形ではないもの）
    'edo_life': ['60_hikeshi', '04_edo_ichikoku', '56_bath', '53_carpenter', '59_hikyaku',
                 '74_hatsugatsuo', '72_hanabi', '68_doyo', '67_chushingura'],
    # 科学・雑学（代表的なグループごとに）
    'sci_calendar': ['09_calendar_meiji5', '19_leap_second'],
    'sci_earth': ['06_drain_vortex', '10_compass_north', '31_flatearth', '17_magnitude_energy', '29_lightning'],
    'sci_bio': ['41_brain10', '12_einstein_math', '07_scurvy_lind', '08_zenzen_affirm', '13_vein_blue'],
    'sci_physics': ['25_gps', '49_frequency', '24_akashi', '14_rain_probability'],
    'sci_econ': ['05_housework_gdp', '43_bukka', '23_rice'],
    'sci_history': ['03_ninja_myths', '27_forest', '16_islands_count', '22_ocean_blue', '47_snowcrystal'],
}


def load_video_id(key):
    """youtube_ids.json から video_id を取得"""
    ids = json.load(open(R / 'data' / 'youtube_ids.json', encoding='utf8'))
    return ids.get(key, {}).get('video_id')


def build_next_map():
    """key -> next_key のマップを作る"""
    next_map = {}
    for series_name, keys in SERIES.items():
        for i, key in enumerate(keys):
            if i + 1 < len(keys):
                next_map[key] = keys[i + 1]
    return next_map


def main():
    next_map = build_next_map()
    yt = yt_api.service()

    print('対象: {} 本'.format(len(next_map)))
    for key, next_key in next_map.items():
        vid = load_video_id(key)
        next_vid = load_video_id(next_key)
        if not vid or not next_vid:
            print('  SKIP {} -> {}: video_id not found'.format(key, next_key))
            continue

        # 現在の概要欄を取得
        v = yt.videos().list(part='snippet', id=vid).execute()['items'][0]['snippet']
        desc = v['description']

        # 既に「次の動画」リンクがあればスキップ（next_vid が含まれているか）
        if '次の動画' in desc and next_vid in desc:
            print('  SKIP {}: already has next link'.format(key))
            continue

        # 次の動画のタイトルを取得
        nv = yt.videos().list(part='snippet', id=next_vid).execute()['items'][0]['snippet']
        next_title = nv['title']

        # 概要欄の末尾に追加
        addition = '\n\n▼ 次の動画\n{}\nhttps://youtu.be/{}'.format(next_title, next_vid)
        new_desc = desc.rstrip() + addition

        if DRY:
            print('  DRY {} ({}) -> {} ({})'.format(key, vid[:8], next_key, next_vid[:8]))
            print('    追加: {}...'.format(addition[:80]))
            continue

        try:
            yt.videos().update(
                part='snippet',
                body={'id': vid, 'snippet': {**v, 'description': new_desc}}
            ).execute()
            print('  OK  {} -> {}'.format(key, next_key))
        except Exception as e:
            print('  NG  {}: {}: {}'.format(key, type(e).__name__, e))


if __name__ == '__main__':
    main()