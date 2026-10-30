# -*- coding: utf-8 -*-
"""差し替え前の点検（API を叩かない）。

`daily_quota_run.py` が今日どの順で差し替えるかを再現し、その各本について
「アップロードで使うファイルが揃っていて、中身が最新か」をローカルだけで確かめる。

usage:
  python scripts/preflight_replace.py                 # 今日の予算(9,400)で回る分を点検
  python scripts/preflight_replace.py --budget 5000   # 予算を変えて点検
  python scripts/preflight_replace.py calendar moon   # 指定した本だけ点検

なぜ要るか: 差し替えは 1 本 2,204 ユニット。字幕・概要欄・サムネが古いまま上げると、
新しいIDに古い内容が載り、やり直しにもう 2,204 ユニットかかる。
（`replace_versions.replace()` は out の video と srt だけをパックへコピーする。
 description.txt / thumbnail.jpg はパックにあるものを使うので、パック側の鮮度を見る。）
"""
import json
import subprocess
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))

import daily_quota_run as dqr          # noqa: E402  （REPLACE_ORDER / COST / STATE を再利用）
import replace_versions as rv          # noqa: E402

OUT = R / 'out'
PACKS = R / 'upload'
REPORT = OUT / 'codex' / 'preflight_replace.txt'
_BIN = R / 'tools' / 'ffmpeg' / 'bin'
FFPROBE = str(_BIN / 'ffprobe.exe') if (_BIN / 'ffprobe.exe').exists() else 'ffprobe'

# publishAt を引くための台帳（sync_progress_sheet.py が作る）
SHEET = R / 'data' / 'progress_sheet.json'
MIN_LEAD_H = 3          # replace_versions.MIN_LEAD と同じ
WANT_W, WANT_H, WANT_FPS, WANT_AR = 1920, 1080, 30.0, 48000

_issues = []            # (slug, level, msg)


def add(slug, level, msg):
    _issues.append((slug, level, msg))


def probe(path):
    """戻り値 dict(duration, w, h, fps, ar)"""
    r = subprocess.run([FFPROBE, '-v', 'error', '-show_entries',
                        'format=duration:stream=width,height,r_frame_rate,sample_rate,codec_type',
                        '-of', 'json', str(path)], capture_output=True, text=True, encoding='utf8',
                       errors='replace')
    try:
        j = json.loads(r.stdout or '{}')
    except json.JSONDecodeError:
        return {}
    d = {}
    try:
        d['duration'] = float(j['format']['duration'])
    except (KeyError, ValueError):
        pass
    for s in j.get('streams', []):
        if s.get('codec_type') == 'video' and 'w' not in d:
            d['w'], d['h'] = int(s.get('width') or 0), int(s.get('height') or 0)
            num, _, den = (s.get('r_frame_rate') or '0/1').partition('/')
            try:
                d['fps'] = float(num) / float(den or 1)
            except (ValueError, ZeroDivisionError):
                pass
        elif s.get('codec_type') == 'audio' and 'ar' not in d:
            d['ar'] = int(s.get('sample_rate') or 0)
    return d


def mtime(p):
    return p.stat().st_mtime if p.exists() else None


def qa_of(slug):
    """out/codex/qa_lint.txt から 1 本分の判定を拾う（無ければ None）"""
    p = OUT / 'codex' / 'qa_lint.txt'
    if not p.exists():
        return None
    lines = p.read_text(encoding='utf8').splitlines()
    for i, line in enumerate(lines):
        if line.strip() in (f'[OK] {slug}', f'[WARN] {slug}', f'[NG] {slug}'):
            block = []
            for nxt in lines[i + 1:]:
                if nxt.startswith('[') or nxt.startswith('合計'):
                    break
                if nxt.strip():
                    block.append(nxt.strip())
            return line.strip()[1:line.strip().index(']')], block
    return None


def publish_at(pack, slug):
    """公開日時（JST の datetime）。snapshot の publish_at(UTC) を優先し、無ければ台帳の日付＋19:00"""
    import datetime as dt
    snap = R / 'data' / 'publish_snapshot.json'
    if snap.exists():
        try:
            rec = (json.loads(snap.read_text(encoding='utf8')).get(pack) or {})
            z = rec.get('publish_at')
            if z:
                return dt.datetime.strptime(z, '%Y-%m-%dT%H:%M:%SZ') + dt.timedelta(hours=9)
        except Exception:
            pass
    if SHEET.exists():
        d = json.loads(SHEET.read_text(encoding='utf8'))
        day = (d.get('videos', {}).get(slug) or {}).get('publishAt')
        if day:
            try:
                return dt.datetime.strptime(day[:10], '%Y-%m-%d').replace(hour=19)
            except ValueError:
                return None
    return None


def check_one(slug, pack, budget_left):
    """1 本を点検。NG が 1 つでもあれば False"""
    before = len([i for i in _issues if i[1] == 'NG'])
    out_video = OUT / f'{slug}_video.mp4'
    out_srt = OUT / f'{slug}_subtitles.srt'
    import make_upload_pack as mup
    cfg = mup.PACKS.get(pack) or {}
    out_desc = (R / cfg['desc']) if cfg.get('desc') else (OUT / f'{slug}_description.md')
    out_thumb = (R / cfg['thumb']) if cfg.get('thumb') else (OUT / f'{slug}_thumbnail.jpg')
    pk = PACKS / pack

    if not out_video.exists():
        add(slug, 'NG', f'out/{out_video.name} が無い（差し替えはスキップされます）')
        return False
    if not pk.is_dir():
        add(slug, 'NG', f'upload/{pack}/ が無い')
        return False

    # 1) replace() がコピーする2ファイルの整合（焼き込み字幕とキャプションが同じ元か）
    if not out_srt.exists():
        add(slug, 'NG', '字幕（srt）が無い')
    elif mtime(out_srt) > mtime(out_video) + 1:
        add(slug, 'NG', f'字幕が動画より新しい（字幕 {_fmt(mtime(out_srt))} / 動画 {_fmt(mtime(out_video))}）'
                        '＝字幕を直したあと再レンダリングしていない')
    if not (pk / 'video.mp4').exists():
        add(slug, 'WARN', f'upload/{pack}/video.mp4 が無い（replace() が out からコピーします）')
    if not (pk / 'subtitles_ja.srt').exists():
        add(slug, 'WARN', f'upload/{pack}/subtitles_ja.srt が無い（replace() が out からコピーします）')

    # 2) パック側だけが持つメタ情報の鮮度（replace() は作り直さない）
    #    mtime ではなく「パックを作るのと同じ抽出をして中身を比べる」（draft の見出し等で誤検知しない）
    import hashlib
    import make_upload_pack as mup
    spec_p = R / 'data' / f'{slug}_spec.json'
    title_no = cfg.get('title_no', 1)
    if spec_p.exists():
        try:
            title_no = (json.loads(spec_p.read_text(encoding='utf8')).get('desc') or {}).get('title_no', 1)
        except Exception:
            title_no = 1
    if not out_desc.exists():
        add(slug, 'NG', f'out/{out_desc.name} が無い（概要欄の元）')
    else:
        try:
            titles, body, tags = mup.sections(out_desc.read_text(encoding='utf8'))
            want = {'title.txt': (titles[title_no - 1] if len(titles) >= title_no else ''),
                    'description.txt': body.strip(),
                    'tags.txt': tags}
            for name, text in want.items():
                p = pk / name
                if not p.exists():
                    add(slug, 'NG', f'upload/{pack}/{name} が無い（`vp.py {slug} pack`）')
                elif p.read_text(encoding='utf8').strip() != text.strip():
                    add(slug, 'NG', f'{name} がパックで古い（中身が違う）＝ `vp.py {slug} pack` をやり直す')
        except Exception as e:  # noqa: BLE001  抽出できない書式なら mtime で見る
            add(slug, 'WARN', f'概要欄ドラフトを読めない（{type(e).__name__}）。mtime で判定します')
            for src, name in ((out_desc, 'description.txt'),):
                p = pk / name
                if not p.exists() or (src.exists() and mtime(src) > mtime(p) + 1):
                    add(slug, 'NG', f'{name} がパックで古い（mtime）＝ `vp.py {slug} pack`')
    if not out_thumb.exists():
        add(slug, 'NG', f'out/{out_thumb.name} が無い（サムネイル）')
    elif not (pk / 'thumbnail.jpg').exists():
        add(slug, 'NG', f'upload/{pack}/thumbnail.jpg が無い（サムネイル）')
    else:
        ha = hashlib.sha256(out_thumb.read_bytes()).hexdigest()
        hb = hashlib.sha256((pk / 'thumbnail.jpg').read_bytes()).hexdigest()
        if ha != hb:
            add(slug, 'NG', f'thumbnail.jpg がパックと違う（中身が違う）＝ `vp.py {slug} pack` をやり直す')

    # 3) 動画の素性（秒数・解像度・fps・音声）
    info = probe(out_video)
    tl = R / 'data' / f'{slug}_timeline.json'
    if tl.exists():
        want = json.loads(tl.read_text(encoding='utf8'))[-1]['end']
        got = info.get('duration')
        if got and abs(got - want) > 1.0:
            add(slug, 'NG', f'尺が timeline と違う（動画 {got:.1f}s / timeline {want:.1f}s）')
    if (info.get('w'), info.get('h')) != (WANT_W, WANT_H):
        add(slug, 'NG', f'解像度が {info.get("w")}x{info.get("h")}（{WANT_W}x{WANT_H} のはず）')
    if info.get('fps') and abs(info['fps'] - WANT_FPS) > 0.05:
        add(slug, 'NG', f'fps が {info["fps"]:.2f}（{WANT_FPS:.0f} のはず）')
    if info.get('ar') and info['ar'] != WANT_AR:
        add(slug, 'WARN', f'音声が {info["ar"]}Hz（{WANT_AR}Hz のはず）')

    # 4) 品質検査の結果（qa_lint.txt を再利用。走っていなければ未検査として警告）
    q = qa_of(slug)
    if q is None:
        add(slug, 'WARN', 'qa_lint の結果が無い（`qa_lint.py --all` を回す）')
    elif q[0] == 'NG':
        add(slug, 'NG', 'qa_lint が NG: ' + ' / '.join(q[1][:2]))
    elif q[0] == 'WARN':
        add(slug, 'WARN', 'qa_lint が WARN: ' + ' / '.join([x for x in q[1] if 'WARN' in x][:2]))

    # 5) 公開日時（今日の実行で「公開まで3時間未満」で見送られないか）
    at = publish_at(pack, slug)
    if not at:
        add(slug, 'WARN', '公開日時が台帳に無い（見送られる可能性）')
    else:
        import datetime as dt
        left = at - dt.datetime.now()
        if left < dt.timedelta(hours=MIN_LEAD_H):
            add(slug, 'NG', f'公開まで {left}（{at:%m/%d %H:%M} JST）。3時間未満なので差し替えは見送られます')

    # 6) 差し替え待ち台帳・Short 側の準備
    pend = R / 'data' / 'pending_replace.json'
    if not (pend.exists() and slug in json.loads(pend.read_text(encoding='utf8'))):
        add(slug, 'WARN', 'pending_replace.json に載っていない（パックが古いと見送られます）')
    short_slug = rv.SHORT_OF.get(slug, slug)
    if not (OUT / f'short_{short_slug}.mp4').exists():
        add(slug, 'WARN', f'Short が無い（short_{short_slug}.mp4）。リンク更新は飛ばされます')
    if not (R / 'data' / f'short_{short_slug}.json').exists():
        add(slug, 'WARN', f'data/short_{short_slug}.json が無い（long_id を書き換えられない）')
    if not (R / 'scripts' / 'fix_short_links.py').exists():
        add(slug, 'NG', 'scripts/fix_short_links.py が無い')

    # 7) 予算
    if rv.COST > budget_left:
        add(slug, 'NG', f'予算不足（残り {budget_left} / 必要 {rv.COST}）')

    return len([i for i in _issues if i[1] == 'NG']) == before


def _fmt(t):
    import datetime as dt
    return dt.datetime.fromtimestamp(t).strftime('%m/%d %H:%M') if t else '-'


def main():
    args = sys.argv[1:]
    budget = dqr.BUDGET if hasattr(dqr, 'BUDGET') else 9400
    if '--budget' in args:
        i = args.index('--budget')
        budget = int(args[i + 1])
        del args[i:i + 2]
    explicit = [a for a in args if not a.startswith('--')]

    state = dqr.load_state()
    done = state.get('done', {})
    if explicit:
        plan = [(s, budget) for s in explicit]
    else:
        plan = []
        left = budget
        for s in dqr.REPLACE_ORDER:
            if f'replace:{s}' in done:
                continue
            if rv.COST > left:
                break
            plan.append((s, left))
            left -= rv.COST

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append(f'# 差し替え事前点検（予算 {budget} ユニット）')
    if not plan:
        lines.append('今日の実行対象はありません（すべて完了、または予算不足）。')
        REPORT.write_text('\n'.join(lines) + '\n', encoding='utf8')
        print('\n'.join(lines))
        return 0

    total = 0
    ok_all = True
    for slug, left in plan:
        pack = rv.PACK.get(slug)
        if not pack:
            add(slug, 'NG', f'replace_versions.PACK に {slug} が無い')
            ok_all = False
            continue
        ok = check_one(slug, pack, left)
        total += rv.COST
        ok_all = ok_all and ok

    lines.append(f'対象: {len(plan)} 本 / 見積もり {total} ユニット')
    lines.append('')
    for slug, _left in plan:
        mine = [i for i in _issues if i[0] == slug]
        ng = [i for i in mine if i[1] == 'NG']
        wa = [i for i in mine if i[1] == 'WARN']
        mark = 'NG' if ng else ('WARN' if wa else 'OK')
        lines.append(f'[{mark}] {slug}  ({rv.PACK.get(slug)})')
        for _s, level, msg in (ng + wa):
            lines.append(f'   {level} {msg}')
    lines.append('')
    n_ng = len([i for i in _issues if i[1] == 'NG'])
    n_wa = len([i for i in _issues if i[1] == 'WARN'])
    lines.append(f'合計: NG {n_ng} 件 / WARN {n_wa} 件')
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf8')
    print('\n'.join(lines))
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main())
