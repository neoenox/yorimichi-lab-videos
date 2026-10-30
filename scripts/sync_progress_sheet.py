"""制作進捗シート（Claude Artifact の db）に流し込む内容を、リポジトリの実状態から作る。

Artifact へは直接書けない（OpenCode/Codex からは読み書き不可）ので、
  1. `data/progress_sheet.json`   … 「あるべき行」の正本（版管理できる）
  2. `out/codex/progress_sheet.md` … 人が読める表
  3. `out/codex/progress_batch.json` … そのまま渡せる差分（既存行の update のみ）
を出す。Claude（ArtifactData ツールを持つ）か人が 3 を適用する。

slug は `data/<slug>_spec.json` の slug。spec が無い古い3本（worldmap / honnoji / ninja）は、
Short の `long_id` から slug を引く。

usage:
  python scripts/sync_progress_sheet.py
"""

import datetime as dt
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
JST = dt.timezone(dt.timedelta(hours=9))

STAGE_MEANING = {
    0: '題材', 1: '事実確認', 2: '台本', 3: '画像・図',
    4: '動画制作', 5: 'Codex確認', 6: '非公開アップ', 7: '予約済み', 8: '公開済み',
}
# 分野の日本語（video_meta.json の field）
FIELD_JA = {
    'science': '科学', 'body': 'からだ', 'calendar': '暦', 'earth': '地球',
    'economy': '経済', 'history_sci': '科学史', 'person': '人物', 'life': 'くらし',
}


def load(name, default):
    p = R / 'data' / name
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding='utf8'))


def theme_dir(spec):
    t = spec.get('theme_dir')
    if t and (R / 'docs' / 'themes' / t).exists():
        return R / 'docs' / 'themes' / t
    slug = spec.get('slug', '')
    for d in (R / 'docs' / 'themes').glob(f'*{slug}*'):
        if d.is_dir():
            return d
    return None


def images_ready(spec):
    imgs = spec.get('images') or {}
    if not imgs:
        return False
    for meta in imgs.values():
        f = (meta or {}).get('file')
        if f and not (R / f).exists():
            return False
    return True


def parse_publish(iso):
    """'2026-11-07T10:00:00Z' -> JST datetime"""
    if not iso:
        return None
    try:
        return dt.datetime.fromisoformat(iso.replace('Z', '+00:00')).astimezone(JST)
    except ValueError:
        return None


def long_state(slug, spec, tdir, pack, ids, snap, now):
    """(stage, 根拠, publishAt, longId, deleted)"""
    e = snap.get(pack) or {}
    # 動画IDの正本は data/youtube_ids.json（差し替えのたびに更新される）。スナップショットは古いことがある。
    vid = (ids.get(pack) or {}).get('video_id') or e.get('video_id')
    pub = parse_publish(e.get('publish_at'))
    privacy = e.get('privacy') or (ids.get(pack) or {}).get('privacy')
    deleted = (ids.get(pack) or {}).get('deleted') or []

    if privacy == 'public' or (pub and pub <= now):
        stage, why = 8, '公開済み'
    elif vid and pub:
        stage, why = 7, f'{pub:%m/%d %H:%M} 公開予約'
    elif vid:
        stage, why = 6, '非公開でアップ済み'
    elif tdir and ((tdir / '13_codex_video_review.md').exists() or (tdir / '14_codex_watch.md').exists()):
        stage, why = 5, 'Codex確認あり'
    elif (R / 'out' / f'{slug}_video.mp4').exists():
        stage, why = 4, '動画あり'
    elif images_ready(spec):
        stage, why = 3, '画像あり'
    elif tdir and (tdir / '09_script_v2.md').exists():
        stage, why = 2, '台本あり'
    elif tdir and (tdir / '08_fact_check.md').exists():
        stage, why = 1, '事実確認あり'
    else:
        stage, why = 0, '題材のみ'
    return stage, why, pub, vid, deleted


def short_state(slug, ids, snap, now):
    pack = f'short_{slug}'
    e = snap.get(pack) or {}
    vid = (ids.get(pack) or {}).get('video_id') or e.get('video_id')
    pub = parse_publish(e.get('publish_at'))
    privacy = e.get('privacy') or (ids.get(pack) or {}).get('privacy')
    if privacy == 'public' or (pub and pub <= now):
        return '公開済み', vid, None
    if vid and pub:
        return '予約済み', vid, pub
    if vid:
        return 'アップ済み', vid, None
    if (R / 'out' / f'short_{slug}.mp4').exists():
        return '作成中', None, None
    return 'なし', None, None


def qa_results():
    """out/codex/qa_lint.txt から slug -> 'NG' / 'WARN' を拾う"""
    p = R / 'out' / 'codex' / 'qa_lint.txt'
    if not p.exists():
        return {}
    res = {}
    cur = None
    for ln in p.read_text(encoding='utf8').split('\n'):
        s = ln.strip()
        if s.startswith('[') and ']' in s:
            head = s[1:s.index(']')]
            cur = s[s.index(']') + 1:].strip() or None
            if cur and head in ('OK', 'NG', 'WARN'):
                res[cur] = head
        elif cur and (s.startswith('NG ') or s.startswith('NG\t')):
            res[cur] = 'NG'
        elif cur and (s.startswith('WARN ') or s.startswith('WARN\t')) and res.get(cur) != 'NG':
            res[cur] = 'WARN'
    return res


def legacy_videos(ids, snap, now):
    """spec が無い古い長尺（01〜03）を、Short の long_id から引く"""
    by_long = {}
    for p in (R / 'data').glob('short_*.json'):
        s = json.loads(p.read_text(encoding='utf8'))
        if s.get('long_id'):
            by_long[s['long_id']] = p.stem[len('short_'):]

    covered = set()
    for p in (R / 'data').glob('*_spec.json'):
        if p.name.startswith('short_'):
            continue
        covered.add(json.loads(p.read_text(encoding='utf8')).get('pack'))

    out = []
    for d in sorted((R / 'upload').iterdir()):
        if not d.is_dir() or d.name.startswith('short_') or d.name in covered:
            continue
        vid = ((ids.get(d.name) or {}).get('video_id')
               or (snap.get(d.name) or {}).get('video_id'))
        slug = by_long.get(vid)
        if not slug:
            continue
        title = ''
        sp = R / 'data' / f'short_{slug}.json'
        if sp.exists():
            title = json.loads(sp.read_text(encoding='utf8')).get('long_title') or ''
        out.append({'slug': slug, 'pack': d.name, 'title': title, 'legacy': True})
    return out


def main():
    now = dt.datetime.now(JST)
    stamp = f'{now:%Y-%m-%d %H:%M}'
    ids = load('youtube_ids.json', {})
    snap = load('publish_snapshot.json', {})
    meta = load('video_meta.json', {})
    qa = qa_results()
    pending = load('pending_replace.json', {})
    snap_time = (R / 'data' / 'publish_snapshot.json').stat().st_mtime
    snap_stamp = f'{dt.datetime.fromtimestamp(snap_time):%m/%d %H:%M}'

    specs = []
    for p in sorted((R / 'data').glob('*_spec.json')):
        if p.name.startswith('short_'):
            continue
        specs.append(json.loads(p.read_text(encoding='utf8')))

    rows = []
    for spec in specs:
        rows.append({'slug': spec.get('slug') or '', 'pack': spec.get('pack'), 'spec': spec,
                     'title': (spec.get('header_sub') or '')[:28] or spec.get('slug', '')})
    for lg in legacy_videos(ids, snap, now):
        rows.append({'slug': lg['slug'], 'pack': lg['pack'], 'spec': None, 'title': lg['title'],
                     'legacy': True})

    videos = {}
    for r in rows:
        slug, pack = r['slug'], r['pack']
        spec = r['spec'] or {}
        tdir = theme_dir(spec) if spec else None
        stage, why, pub, vid, deleted = long_state(slug, spec, tdir, pack, ids, snap, now)
        sstat, sid, _ = short_state(slug, ids, snap, now)

        note = [why]
        if deleted:
            note.append(f'旧版{len(deleted)}本削除')
        q = qa.get(slug)
        if q == 'NG':
            note.append('品質チェック NG')
        elif q == 'WARN':
            note.append('品質チェック WARN')
        if r.get('legacy'):
            note.append('旧パイプライン')
        if slug in pending:
            note.append('差し替え待ち')
        if sstat == '作成中' and (R / 'out' / f'short_{slug}.mp4').exists():
            note.append('Short は書き出し済み・未アップ')

        m = meta.get(slug) or {}
        videos[slug] = {
            'title': r['title'],
            'category': FIELD_JA.get(m.get('field'), ''),
            'type': '',
            'stage': stage,
            'shortStatus': sstat,
            'publishAt': f'{pub:%Y-%m-%d}' if pub else '',
            'longId': vid or '',
            'shortId': sid or '',
            'owner': 'Codex',
            'note': ' / '.join(dict.fromkeys(note)),
            'blocked': False,
            'blockReason': '',
            'updated': stamp,
        }

    # 要対応：公開前後で片づけるもの（事実から作れるものだけ）
    todos = {}
    n = 0
    order = sorted(videos.items(), key=lambda kv: (kv[1]['publishAt'] or '9999', kv[0]))
    for slug, v in order:
        if slug in pending:
            n += 1
            todos[f't{n:02d}'] = {
                'text': f"{slug}: 差し替え（{pending[slug].get('reason', '')}）"
                        f"・公開 {v['publishAt'] or '未定'}・約2,200ユニット",
                'who': 'Codex', 'status': 'open', 'video': slug, 'created': stamp,
            }
    for slug, v in order:
        if v['stage'] in (6, 7) and qa.get(slug) == 'NG':
            n += 1
            todos[f't{n:02d}'] = {
                'text': f"{slug}: 品質チェック NG を直す（公開 {v['publishAt'] or '未定'}・out/codex/qa_lint.txt）",
                'who': 'Claude', 'status': 'open', 'video': slug, 'created': stamp,
            }
    if (R / 'out' / 'short_oke.mp4').exists():
        n += 1
        todos[f't{n:02d}'] = {
            'text': 'short_oke は旧描画のままアップ済み（11/03 公開の予定）。差し替えるか決める（約2,100ユニット）',
            'who': '人', 'status': 'open', 'video': 'oke', 'created': stamp,
        }

    out = {'generated': stamp, 'snapshot': snap_stamp, 'videos': videos, 'todos': todos}
    (R / 'data' / 'progress_sheet.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding='utf8')

    # 人が読める表
    md = [f'# 制作進捗（{stamp} 時点 / 公開状態は {snap_stamp} のスナップショット。'
          f'クォータ切れのため更新は翌日16:00以降）', '']
    md.append('| slug | 工程 | Short | 公開日 | 長尺ID | メモ |')
    md.append('|---|---|---|---|---|---|')
    for slug, v in order:
        md.append(f"| {slug} | {v['stage']} {STAGE_MEANING[v['stage']]} | {v['shortStatus']} | "
                  f"{v['publishAt'] or '—'} | {v['longId'] or '—'} | {v['note']} |")
    md.append('')
    if todos:
        md.append('## 要対応')
        for tid, t in todos.items():
            md.append(f"- [ ] {t['text']}（{tid} / {t['who']}）")
        md.append('')
    md.append('## 適用のしかた')
    md.append('')
    md.append('このファイルは `scripts/sync_progress_sheet.py` が作る。'
              'Artifact（https://claude.ai/artifact/J4ZSSj2X5X2BLJEtXVciy8 ）へは、'
              '同じ実行で出る `out/codex/progress_batch.json` を Claude の `ArtifactData`（batch）か人に渡す。')
    md.append('')
    (R / 'out' / 'codex' / 'progress_sheet.md').write_text('\n'.join(md), encoding='utf8')

    # Artifact へ渡す差分（既存行の update のみ。category/type/owner は触らない）
    # 値が空の項目は送らない（不明な publishAt で既存の日付を消さないため）
    ops = []
    for slug, v in videos.items():
        data = {
            'stage': v['stage'], 'shortStatus': v['shortStatus'],
            'note': v['note'], 'blocked': False, 'blockReason': '', 'updated': stamp,
        }
        for k in ('publishAt', 'longId', 'shortId'):
            if v[k]:
                data[k] = v[k]
        ops.append({'op': 'update', 'collection': 'videos', 'doc_id': slug, 'data': data})
    for tid, t in todos.items():
        ops.append({'op': 'set', 'collection': 'todos', 'doc_id': tid, 'data': t})
    (R / 'out' / 'codex' / 'progress_batch.json').write_text(
        json.dumps({'url': 'https://claude.ai/artifact/J4ZSSj2X5X2BLJEtXVciy8', 'ops': ops},
                   ensure_ascii=False, indent=1), encoding='utf8')

    print(f'videos {len(videos)} 件 / todos {len(todos)} 件')
    print('  data/progress_sheet.json')
    print('  out/codex/progress_sheet.md')
    print('  out/codex/progress_batch.json')
    for slug, v in order:
        print(f"  {slug:12s} {v['stage']} {STAGE_MEANING[v['stage']]:6s} {v['shortStatus']:5s} "
              f"{v['publishAt'] or '-':10s} {v['longId'] or '-'}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
