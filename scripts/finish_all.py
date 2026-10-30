"""ブラウザで上げた動画の仕上げを一括で行う（API枠が戻ってから）。
usage: python scripts/finish_all.py [--dry] [--only vein,compass,...] [--no-delete]
  out/codex/browser_uploads.txt の各行（<pack> <pack> <id> <日付 時刻>）に対して yt_api.py の finish（概要欄・タグ・サムネ・字幕・公開予約）を実行し、
  旧版（台帳の superseded と、ブラウザで上げた途中版）を delete-superseded で消す（非公開のものだけ）。
  公開は『予約』のみ。すでに終わった行は data/youtube_ids.json の video_id と一致するので飛ばす。静脈（最初に公開される）を先頭にする。"""
import json, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
IDS = R / 'data' / 'youtube_ids.json'
# ブラウザで上げた途中版（台帳に載っていない）。pack → 消す動画ID
EXTRA_SUPERSEDED = {'13_vein_blue': ['zgTA3FHc3qs'], '04_edo_ichikoku': ['_eKAa1NUUFI', 'VSrBQ1xYXBU'],
                    '07_scurvy_lind': ['GlZ39qaS0NM', 'GeurUUmupV4', 'tIlIgvCI9yQ'], '11_season_distance': ['TZ7VvvDP4ms', 'vCEJV80_9bw'],
                    '05_housework_gdp': ['lAtP-Yd-wc0'], '09_calendar_meiji5': ['vgVLYOul7Gk'], '08_zenzen_affirm': ['ln2qz0CRCLU'], '19_leap_second': ['Xku8ppUSZKI'], '15_moon_rotation': ['nl7Bk2KK1SY'], '17_magnitude_energy': ['ZguO5obyDNg'], '14_rain_probability': ['BptkrZKjZKA'], '18_yakubusoku_meaning': ['EtiAD5-REwk'], '21_venus_day': ['oI3kenxokCw'], '22_ocean_blue': ['RUb-GWJepyg']}
PACK = {'vein': '13_vein_blue', 'koku': '04_edo_ichikoku', 'compass': '10_compass_north', 'gdp': '05_housework_gdp',
        'season': '11_season_distance', 'scurvy': '07_scurvy_lind', 'calendar': '09_calendar_meiji5',
        'einstein': '12_einstein_math', 'zenzen': '08_zenzen_affirm', 'short_vein': 'short_vein', 'short_koku': 'short_koku',
        'short_compass': 'short_compass', 'short_season': 'short_season', 'short_calendar': 'short_calendar',
        'rain30': '14_rain_probability', 'moon': '15_moon_rotation', 'islands': '16_islands_count', 'magnitude': '17_magnitude_energy', 'yakubusoku': '18_yakubusoku_meaning', 'leapsecond': '19_leap_second', 'sunrise': '20_sunrise_solstice', 'okehazama': '14_okehazama', 'short_venus': 'short_venus', 'short_oceanblue': 'short_oceanblue', 'venus': '21_venus_day', 'oceanblue': '22_ocean_blue', 'short_gdp': 'short_gdp', 'short_scurvy': 'short_scurvy', 'short_einstein': 'short_einstein', 'short_zenzen': 'short_zenzen', 'short_rain30': 'short_rain30', 'short_moon': 'short_moon', 'short_islands': 'short_islands', 'short_magnitude': 'short_magnitude', 'short_yakubusoku': 'short_yakubusoku', 'short_leapsecond': 'short_leapsecond', 'short_sunrise': 'short_sunrise'}


def run(args):
    p = subprocess.run([sys.executable, str(R / 'scripts' / 'yt_api.py')] + args, capture_output=True, text=True, encoding='utf8', errors='replace')
    print(' '.join(args), '->', (p.stdout + p.stderr).strip()[-300:])
    return p.returncode == 0


def main():
    dry = '--dry' in sys.argv
    only = None
    if '--only' in sys.argv:
        only = {PACK[k] for k in sys.argv[sys.argv.index('--only') + 1].split(',')}
    rows = []
    for ln in (R / 'out' / 'codex' / 'browser_uploads.txt').read_text(encoding='utf8').splitlines():
        if not ln.strip() or ln.startswith('#'):
            continue
        k, _pack, vid, at1, at2 = ln.split()
        rows.append((PACK[k], vid, f'{at1} {at2}'))
    rows.sort(key=lambda r: r[2])
    if only:
        rows = [r for r in rows if r[0] in only]
    ids = json.loads(IDS.read_text(encoding='utf8'))
    for pack, extra in EXTRA_SUPERSEDED.items():
        rec = ids.setdefault(pack, {})
        sup = rec.setdefault('superseded', [])
        for e in extra:
            if e not in sup and e not in rec.get('deleted', []):
                sup.append(e)
    if not dry:
        IDS.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding='utf8')
    failed = []
    for pack, vid, at in rows:
        if ids.get(pack, {}).get('video_id') == vid and ids[pack].get('finished'):
            print('skip (done)', pack); continue
        if dry:
            print('would finish', pack, vid, at); continue
        if run(['finish', pack, vid, at]):
            ids = json.loads(IDS.read_text(encoding='utf8')); ids[pack]['finished'] = True
            IDS.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding='utf8')
        else:
            failed.append(pack)
    if not dry and '--no-delete' not in sys.argv:
        run(['delete-superseded'])
    print('failed:', failed or 'none')


if __name__ == '__main__':
    main()
