"""冬至の動画の一次資料を取得し、数字を抜き出す（再実行できるようにする）。
- 国立天文台 暦要項 2026（二十四節気）: 冬至・夏至の日時
- 国立天文台 暦計算室 東京 2026年12月・6月（日の出・南中・南中高度・日の入り）
- 気象庁 東京 平年値（1991-2020）: 月平均気温・日照時間
出力: docs/themes/20261219_toji/sources/*.csv, *.txt
usage: python scripts/toji_sources.py
"""
import re, sys, json, datetime
from pathlib import Path
import requests

R = Path(__file__).resolve().parents[1]
OUT = R / 'docs' / 'themes' / '20261219_toji' / 'sources'
OUT.mkdir(parents=True, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (research; rekishikaisetu)'}


def get(url, enc):
    r = requests.get(url, headers=UA, timeout=40)
    r.raise_for_status()
    return r.content.decode(enc, errors='replace')


def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s.replace('&nbsp;', ' '))).strip()


def naoj_solar_terms():
    t = get('https://eco.mtk.nao.ac.jp/koyomi/yoko/2026/rekiyou262.html', 'shift_jis')
    p = strip_tags(t)
    out = {}
    for name in ('夏至', '冬至'):
        m = re.search(name + r'\s*(\d+)度\s*(\d+)月(\d+)日\s*(\d+)時(\d+)分', p)
        assert m, name
        out[name] = dict(degree=int(m.group(1)), month=int(m.group(2)), day=int(m.group(3)),
                         hour=int(m.group(4)), minute=int(m.group(5)))
    (OUT / 'naoj_solar_terms_2026.txt').write_text(
        'source: https://eco.mtk.nao.ac.jp/koyomi/yoko/2026/rekiyou262.html\n'
        '国立天文台 暦要項 令和8年(2026) 二十四節気および雑節（中央標準時）\n'
        + '\n'.join(f'{k}: {v["month"]}月{v["day"]}日 {v["hour"]}時{v["minute"]:02d}分' for k, v in out.items()) + '\n',
        encoding='utf8')
    return out


def naoj_tokyo(month):
    url = f'https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s13{month:02d}.html'
    t = get(url, 'euc-jp')
    rows = []
    for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S):
        cells = [strip_tags(c) for c in re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)]
        if len(cells) >= 7 and re.fullmatch(r'\d+', cells[0]):
            rows.append(dict(day=int(cells[0]), sunrise=cells[1], sunrise_dir=cells[2],
                             noon=cells[3], noon_alt=cells[4], sunset=cells[5], sunset_dir=cells[6]))
    assert len(rows) >= 28, (month, len(rows))
    with (OUT / f'naoj_tokyo_2026_{month:02d}.csv').open('w', encoding='utf8') as f:
        f.write('day,sunrise,sunrise_dir,noon,noon_alt,sunset,sunset_dir\n')
        for r in rows:
            f.write(','.join(str(r[k]) for k in r) + '\n')
    return rows


def minutes(hhmm):
    h, m = hhmm.split(':')
    return int(h) * 60 + int(m)


def jma_normals():
    url = ('https://www.data.jma.go.jp/stats/etrn/view/nml_sfc_ym.php'
           '?prec_no=44&block_no=47662&year=&month=&day=&view=')
    t = get(url, 'utf-8')
    rows = {}
    for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S):
        cells = [strip_tags(c) for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', tr, re.S)]
        if cells and re.fullmatch(r'\d+月', cells[0]) and len(cells) > 14:
            rows[int(cells[0][:-1])] = dict(temp_mean=float(cells[4]), temp_max=float(cells[5]),
                                            temp_min=float(cells[6]), sunshine=float(cells[11]))
    assert len(rows) == 12, rows
    with (OUT / 'jma_tokyo_normals_1991_2020.csv').open('w', encoding='utf8') as f:
        f.write('month,temp_mean_C,temp_max_C,temp_min_C,sunshine_h\n')
        for m in range(1, 13):
            r = rows[m]
            f.write(f'{m},{r["temp_mean"]},{r["temp_max"]},{r["temp_min"]},{r["sunshine"]}\n')
    (OUT / 'jma_tokyo_normals_source.txt').write_text(
        'source: ' + url + '\n'
        '気象庁 過去の気象データ検索 東京（47662）平年値（年・月ごとの値）統計期間1991〜2020\n', encoding='utf8')
    return rows


def main():
    terms = naoj_solar_terms()
    dec = naoj_tokyo(12)
    jun = naoj_tokyo(6)
    jma = jma_normals()
    d22 = next(r for r in dec if r['day'] == 22)
    j21 = next(r for r in jun if r['day'] == 21)
    day_dec = minutes(d22['sunset']) - minutes(d22['sunrise'])
    day_jun = minutes(j21['sunset']) - minutes(j21['sunrise'])
    summary = dict(
        solstice=terms,
        tokyo_winter=dict(day=22, sunrise=d22['sunrise'], sunset=d22['sunset'], noon_alt=d22['noon_alt'],
                          day_minutes=day_dec, day_hhmm=f'{day_dec//60}時間{day_dec%60}分'),
        tokyo_summer=dict(day=21, sunrise=j21['sunrise'], sunset=j21['sunset'], noon_alt=j21['noon_alt'],
                          day_minutes=day_jun, day_hhmm=f'{day_jun//60}時間{day_jun%60}分'),
        day_diff_minutes=day_jun - day_dec,
        alt_diff=float(j21['noon_alt']) - float(d22['noon_alt']),
        coldest_month=min(jma, key=lambda m: jma[m]['temp_mean']),
        shortest_sunshine_month=min(jma, key=lambda m: jma[m]['sunshine']),
        jma={m: jma[m] for m in (11, 12, 1, 2, 6)},
        fetched=datetime.datetime.now().isoformat(timespec='seconds'),
    )
    (OUT / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding='utf8')
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
