"""焼き込み字幕を作り直した長尺を、YouTube上で「新しい動画ID」に差し替える。

YouTubeは公開後の動画ファイルを入れ替えられない（公開前でも同じIDのままは不可）ため、
新しいIDでアップロード → 同じ公開日時を予約 → Shortのリンク更新 → 旧動画を削除、の順で行う。

usage:
  python scripts/replace_versions.py --dry                # 対象と手順の確認だけ
  python scripts/replace_versions.py gdp scurvy calendar  # 指定だけ実行
  python scripts/replace_versions.py --all                # 全対象（公開が近いものは自動で見送り）
  python scripts/replace_versions.py --short --all        # Short の差し替え（数字を直した版）

1本あたり約2,200ユニット（アップロード1600＋サムネ50＋字幕400＋予約51＋概要欄更新51＋削除50）。
Short は約2,100ユニット（アップロード1600＋字幕400＋予約51＋削除50）。
1日の上限は10,000。まとめて回すときは scripts/daily_quota_run.py を使う。
"""
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yt_api

R = yt_api.R
PACK = {
    'compass': '10_compass_north',
    'gdp': '05_housework_gdp',
    'scurvy': '07_scurvy_lind',
    'calendar': '09_calendar_meiji5',
    'einstein': '12_einstein_math',
    'moon': '15_moon_rotation',
    'islands': '16_islands_count',
    'magnitude': '17_magnitude_energy',
    'yakubusoku': '18_yakubusoku_meaning',
    'leapsecond': '19_leap_second',
    'sunrise': '20_sunrise_solstice',
    'venus': '21_venus_day',
    'oke': '14_okehazama',
    # 旧系統（*_compose.py）の3本。作り直しは scripts/rebuild_old_compose.py
    'gm': '01_world_map_distortion',
    'hn': '02_honnoji_incident',
    'nj': '03_ninja_myths',
}
# 長尺slugと Short のslugが違う回（Short を後から作った3本）
SHORT_OF = {'gm': 'worldmap', 'hn': 'honnoji', 'nj': 'ninja'}
COST = 2204
COST_SHORT = 2102   # アップロード1600＋字幕400＋予約51＋削除50＋確認1
MIN_LEAD = dt.timedelta(hours=3)
# 数字を直した Short の差し替え対象（公開前のものだけ。公開済み・公開間近は見送る）
SHORT_SLUGS = ['scurvy', 'calendar', 'moon', 'islands', 'magnitude', 'leapsecond', 'venus']


class Skip(Exception):
    pass


def jst_str(utc_z):
    t = dt.datetime.strptime(utc_z, '%Y-%m-%dT%H:%M:%SZ') + dt.timedelta(hours=9)
    return t.strftime('%Y-%m-%d %H:%M')


def retry(fn, tries=3, wait=5, log=print):
    """通信が切れることがある（SSLEOFError など）ので、削除などの単発APIは数回試す。"""
    last = None
    for i in range(tries):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            last = e
            log(f'  !! 通信エラー {i + 1}/{tries}: {type(e).__name__} {str(e)[-80:]}')
            time.sleep(wait)
    raise last


def same_file(a, b):
    """中身が同じか（サイズ→sha256）。mtime は再パックで動くので当てにしない。"""
    import hashlib
    if not (a.exists() and b.exists()) or a.stat().st_size != b.stat().st_size:
        return False
    h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()  # noqa: E731
    return h(a) == h(b)


def set_long_id(slug, new_id):
    """長尺のIDが変わったら、Short の long_id を先に書き換える（data と生成器の両方）。

    fix_short_links は data/short_<slug>.json の long_id を読むので、これを先に直さないと
    古い（削除済みの）IDを概要欄に書いてしまう。
    """
    p = R / 'data' / f'short_{slug}.json'
    if not p.exists():
        return False
    d = json.loads(p.read_text(encoding='utf8'))
    old = d.get('long_id')
    if old == new_id:
        return False
    d['long_id'] = new_id
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf8')
    g = R / 'scripts' / 'gen_short_specs.py'
    if g.exists():
        src = g.read_text(encoding='utf8')
        marker = f"J('{slug}', dict("
        i = src.find(marker)
        if i >= 0:
            j = src.find("J('", i + len(marker))
            body = src[i:j] if j > 0 else src[i:]
            body = body.replace(f'long_id={old!r}', f'long_id={new_id!r}', 1)
            src = src[:i] + body + (src[j:] if j > 0 else '')
            g.write_text(src, encoding='utf8')
    return True


def clear_pending(slug, log=print):
    """data/pending_replace.json から「差し替え待ち」を消す（差し替え成功時）。"""
    p = R / 'data' / 'pending_replace.json'
    if not p.exists():
        return
    d = json.loads(p.read_text(encoding='utf8'))
    if isinstance(d, dict) and slug in d:
        d.pop(slug)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf8')
        log(f'  差し替え待ちから外した {slug}')


def _status(yt, vid):
    """動画の status（無ければ None）。1ユニット。"""
    items = yt.videos().list(part='status', id=vid).execute().get('items') or []
    return items[0]['status'] if items else None


def finish_replace(slug, log=print):
    """中断した差し替えを仕上げる（新IDはアップロード済みで、字幕か予約で落ちた状態）。

    アップロード(1,600ユニット)をやり直さず、メタ情報・サムネ・字幕・予約・旧ID削除だけを行う（約600）。
    台帳の現IDが private で予約なし、かつ superseded の末尾（旧ID）に予約が残っているときだけ動く。
    """
    pack = PACK[slug]
    ids = yt_api.load_ids()
    rec = ids[pack]
    new = rec['video_id']
    prev = list(rec.get('superseded') or [])
    if not prev:
        raise Skip('中断した差し替えが見つからない（superseded が空）')
    old = prev[-1]
    yt = yt_api.service()
    new_st = _status(yt, new)
    if not new_st:
        raise Skip(f'新ID {new} が YouTube に無い')
    if new_st['privacyStatus'] == 'public' or new_st.get('publishAt'):
        raise Skip('新IDはすでに予約/公開済み')
    old_st = _status(yt, old)
    if not old_st:
        raise Skip(f'旧ID {old} が YouTube に無い')
    publish = old_st.get('publishAt')
    if not publish:
        raise Skip('旧IDに公開予約が無い（差し替え先が分からない）')
    at = jst_str(publish)
    left = dt.datetime.strptime(publish, '%Y-%m-%dT%H:%M:%SZ') - dt.datetime.utcnow()
    if left < MIN_LEAD:
        raise Skip(f'公開まで{left}しかない（{at}）')

    # アップロード済みの映像は差し替えられないので、パックが今の書き出しと違えば中止（作り直しから）
    built = R / 'out' / f'{slug}_video.mp4'
    if not built.exists() or not same_file(built, R / 'upload' / pack / 'video.mp4'):
        raise Skip('パックの動画が今の書き出しと違う（作り直してから回す）')

    log(f'  中断した差し替えを再開 新ID {new} / 旧ID {old} / 公開 {at} JST')
    yt_api.cmd_finish(pack, new, at)
    log('  メタ情報・サムネ・字幕・予約 ok')

    short_slug = SHORT_OF.get(slug, slug)
    if set_long_id(short_slug, new):
        log(f'  Short仕様の long_id を更新 {new}')
    subprocess.run([sys.executable, str(R / 'scripts' / 'fix_short_links.py'), short_slug],
                   check=True, cwd=str(R), capture_output=True, text=True, encoding='utf8')
    short = f'short_{short_slug}'
    if short in yt_api.load_ids():
        try:
            yt_api.cmd_redesc(short)
            log(f'  Short概要欄を更新 {short}')
        except Exception as e:  # 概要欄が更新できなくても、二重公開の方が困るので削除へ進む
            log(f'  !! Short概要欄の更新に失敗 {short}: {str(e)[-120:]}')

    retry(lambda: yt.videos().delete(id=old).execute(), log=log)
    ids = yt_api.load_ids()
    rec = ids[pack]
    rec.setdefault('deleted', []).append(old)
    if old in rec.get('superseded', []):
        rec['superseded'].remove(old)
    yt_api.IDS.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding='utf8')
    log(f'  旧IDを削除 {old}')
    clear_pending(slug, log=log)
    return old, new


def replace(slug, log=print):
    """1本を差し替える。戻り値 (old_id, new_id)。見送り時は Skip を投げる。"""
    pack = PACK[slug]
    ids = yt_api.load_ids()
    if pack not in ids:
        raise Skip(f'{pack} が台帳に無い')
    old = ids[pack]['video_id']
    yt = yt_api.service()
    # 前回のアップロードが字幕や予約で落ちたまま（新IDが private・予約なし・旧IDが superseded に残る）なら、
    # アップロードをやり直さずに仕上げる。ここを見落とすと「公開予約が無い」で毎日スキップされ続ける。
    cur_st = _status(yt, old)
    if (cur_st and cur_st['privacyStatus'] != 'public' and not cur_st.get('publishAt')
            and ids[pack].get('superseded')):
        log(f'  未完成の新ID {old} を検出（前回の差し替えが途中で止まっている）')
        return finish_replace(slug, log=log)
    item = yt.videos().list(part='status,snippet', id=old).execute()['items'][0]
    st = item['status']
    if st['privacyStatus'] == 'public':
        raise Skip('公開済み（視聴数とリンクを失うため差し替えない）')
    publish = st.get('publishAt')
    if not publish:
        raise Skip('公開予約が無い')
    at = jst_str(publish)
    left = dt.datetime.strptime(publish, '%Y-%m-%dT%H:%M:%SZ') - dt.datetime.utcnow()
    if left < MIN_LEAD:
        raise Skip(f'公開まで{left}しかない（{at}）')
    log(f'  旧ID {old} / 公開 {at} JST')

    # 作り直した映像だけを差し替える（未再レンダリングなら何もしない）
    # ただし data/pending_replace.json に「差し替え待ち」として載っていれば、明示の指示なので通す
    built = R / 'out' / f'{slug}_video.mp4'
    shipped = R / 'upload' / pack / 'video.mp4'
    pending = R / 'data' / 'pending_replace.json'
    is_pending = pending.exists() and slug in json.loads(pending.read_text(encoding='utf8'))
    if not built.exists():
        raise Skip('out に作り直した動画が無い')
    if not is_pending and shipped.exists() and built.stat().st_mtime <= shipped.stat().st_mtime:
        raise Skip('動画が再レンダリングされていない（パックのまま）')

    # 字幕は2系統ある: spec から作り直す20本と、音声ステップが書いた SRT を直す3本
    spec = R / 'data' / f'{slug}_spec.json'
    if spec.exists():
        srt_cmd = [sys.executable, str(R / 'scripts' / 'regen_srt_vp.py'), slug, '--write']
    else:
        srt_cmd = [sys.executable, str(R / 'scripts' / 'fix_srt_numerals.py'),
                   str(R / 'out' / f'{slug}_subtitles.srt'), '--write']
    subprocess.run(srt_cmd, check=True, cwd=str(R), capture_output=True, text=True, encoding='utf8')
    shutil.copyfile(R / 'out' / f'{slug}_video.mp4', R / 'upload' / pack / 'video.mp4')
    shutil.copyfile(R / 'out' / f'{slug}_subtitles.srt', R / 'upload' / pack / 'subtitles_ja.srt')

    yt_api.cmd_upload(pack, new_version=True)
    new = yt_api.load_ids()[pack]['video_id']
    log(f'  新ID {new}')

    short_slug = SHORT_OF.get(slug, slug)
    if set_long_id(short_slug, new):
        log(f'  Short仕様の long_id を更新 {new}')

    yt_api.cmd_schedule(new, at)
    log(f'  予約 {at} JST')

    short = f'short_{short_slug}'
    subprocess.run([sys.executable, str(R / 'scripts' / 'fix_short_links.py'), short_slug],
                   check=True, cwd=str(R), capture_output=True, text=True, encoding='utf8')
    if short in yt_api.load_ids():
        try:
            yt_api.cmd_redesc(short)
            log(f'  Short概要欄を更新 {short}')
        except Exception as e:  # 概要欄が更新できなくても、二重公開の方が困るので削除へ進む
            log(f'  !! Short概要欄の更新に失敗 {short}: {str(e)[-120:]}')

    retry(lambda: yt.videos().delete(id=old).execute(), log=log)
    ids = yt_api.load_ids()
    rec = ids[pack]
    rec.setdefault('deleted', []).append(old)
    if old in rec.get('superseded', []):
        rec['superseded'].remove(old)
    yt_api.IDS.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding='utf8')
    log(f'  旧IDを削除 {old}')
    clear_pending(slug, log=log)
    return old, new


def replace_short(slug, log=print):
    """Short を新しいIDに差し替える（同じ公開日時を予約し、旧IDを削除する）。

    戻り値 (old_id, new_id)。見送り時は Skip。
    """
    pack = f'short_{slug}'
    ids = yt_api.load_ids()
    if pack not in ids:
        raise Skip(f'{pack} が台帳に無い')
    old = ids[pack]['video_id']
    yt = yt_api.service()
    st = yt.videos().list(part='status', id=old).execute()['items'][0]['status']
    if st['privacyStatus'] == 'public':
        raise Skip('公開済み（視聴数とリンクを失うため差し替えない）')
    publish = st.get('publishAt')
    if not publish:
        raise Skip('公開予約が無い')
    at = jst_str(publish)
    left = dt.datetime.strptime(publish, '%Y-%m-%dT%H:%M:%SZ') - dt.datetime.utcnow()
    if left < MIN_LEAD:
        raise Skip(f'公開まで{left}しかない（{at}）')

    built = R / 'out' / f'short_{slug}.mp4'
    shipped = R / 'upload' / pack / 'video.mp4'
    if not built.exists():
        raise Skip('out に作り直した Short が無い')
    # パックの中身が今の書き出しと同じなら「再レンダリング済み・未アップロード」＝差し替え対象。
    # mtime で見ると、再レンダリングの直後にパックを作り直した回（まさにその状態）を誤って見送る。
    pending = R / 'data' / 'pending_replace.json'
    is_pending = pending.exists() and f'short:{slug}' in json.loads(pending.read_text(encoding='utf8'))
    if not is_pending and not same_file(built, shipped):
        raise Skip('パックの Short が今の書き出しと違う（作り直してから回す）')
    log(f'  旧ID {old} / 公開 {at} JST')

    # 長尺のIDが変わっていれば、先に Short の long_id と概要欄を新しいIDへ
    spec = json.loads((R / 'data' / f'short_{slug}.json').read_text(encoding='utf8'))
    if slug in PACK and PACK[slug] in ids:
        set_long_id(slug, ids[PACK[slug]]['video_id'])
    subprocess.run([sys.executable, str(R / 'scripts' / 'fix_short_links.py'), slug],
                   check=True, cwd=str(R), capture_output=True, text=True, encoding='utf8')

    # 尺が変わったときに備えてタイトルの秒数も作り直す
    desc = (R / 'out' / f'short_{slug}_description.md').read_text(encoding='utf8')
    m = re.search(r'約(\d+)秒', desc)
    sec = int(m.group(1)) if m else spec.get('sec', 45)
    (R / 'upload' / pack / 'title.txt').write_text(f"{spec['title']} 約{sec}秒で確かめる #Shorts\n", encoding='utf8')

    shutil.copyfile(built, shipped)
    shutil.copyfile(R / 'out' / f'short_{slug}_subtitles.srt', R / 'upload' / pack / 'subtitles_ja.srt')

    yt_api.cmd_upload(pack, new_version=True)
    new = yt_api.load_ids()[pack]['video_id']
    log(f'  新ID {new}')
    yt_api.cmd_schedule(new, at)
    log(f'  予約 {at} JST')

    retry(lambda: yt.videos().delete(id=old).execute(), log=log)
    ids = yt_api.load_ids()
    rec = ids[pack]
    rec.setdefault('deleted', []).append(old)
    yt_api.IDS.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding='utf8')
    log(f'  旧IDを削除 {old}')
    return old, new


def main():
    a = sys.argv[1:]
    dry = '--dry' in a
    short_mode = '--short' in a
    names = [x for x in a if not x.startswith('--')]
    if short_mode:
        if '--all' in a or (dry and not names):
            names = list(SHORT_SLUGS)
        if not names:
            sys.exit(__doc__)
        for slug in names:
            print(f'--- short_{slug}')
            if dry:
                print(f'  再アップ → 同時刻に予約 → 旧ID削除（約{COST_SHORT}ユニット）')
                continue
            try:
                replace_short(slug)
            except Skip as e:
                print('  見送り:', e)
        return
    if '--all' in a:
        names = list(PACK)
    if not names:
        sys.exit(__doc__)
    for slug in names:
        print(f'--- {slug} ({PACK.get(slug, "?")})')
        if slug not in PACK:
            print('  対象外')
            continue
        if dry:
            if PACK[slug] in yt_api.load_ids():
                print(f'  旧ID {yt_api.load_ids()[PACK[slug]]["video_id"]} → 新IDで再アップ → 同時刻に予約 → Shortリンク更新 → 旧ID削除（約{COST}ユニット）')
            continue
        try:
            replace(slug)
        except Skip as e:
            print('  見送り:', e)


if __name__ == '__main__':
    main()
