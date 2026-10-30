"""公開予約のスナップショットを撮り、クォータ実行の前後で「予約・ID・リンク・削除」を突き合わせる。

usage:
  python scripts/check_publish.py --write    # いまの公開予約を data/publish_snapshot.json に保存
  python scripts/check_publish.py --check    # スナップショットと比べて合否を出す（API 2〜3ユニット）

--check で見るもの:
  1. 動画が消えていないか（403/404 は「消えた」扱い）
  2. 差し替えた回は、新しいIDになっていて、旧IDが deleted に入っていて、公開予約の時刻が変わっていないか
  3. Short の概要欄のリンクが「いまの長尺ID」を指しているか（削除済みIDを指していないか）
  4. 同じ公開時刻に2本予約されていないか（二重公開の検出）
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yt_api

R = yt_api.R
SNAP = R / 'data' / 'publish_snapshot.json'
# これから上げる Short の公開予約（日本時間 20:00 = UTC 11:00）
EXPECTED = {
    'short_oke': '2026-11-03T11:00:00Z',
    'short_oceanblue': '2026-11-10T11:00:00Z',
    'short_worldmap': '2026-11-11T11:00:00Z',
    'short_honnoji': '2026-11-12T11:00:00Z',
    'short_ninja': '2026-11-13T11:00:00Z',
}
# 公開予約が未設定だった長尺（日本時間 19:00 = UTC 10:00）
EXPECTED_LONG = {
    '01_world_map_distortion': '2026-11-11T10:00:00Z',
    '02_honnoji_incident': '2026-11-12T10:00:00Z',
    '03_ninja_myths': '2026-11-13T10:00:00Z',
}


def fetch(packs):
    """pack -> {video_id, privacy, publish_at, desc} をAPIから取る（50件ずつ）。"""
    ids = yt_api.load_ids()
    yt = yt_api.service()
    out = {}
    items = [(p, ids[p]['video_id']) for p in packs if p in ids]
    for i in range(0, len(items), 50):
        chunk = items[i:i + 50]
        try:
            res = yt.videos().list(part='status,snippet', id=','.join(v for _, v in chunk),
                                   maxResults=50).execute()
        except Exception as e:
            if 'quota' in str(e).lower():
                raise SystemExit('クォータ切れ。16:00以降に再実行してください')
            raise
        by = {it['id']: it for it in res.get('items', [])}
        for pack, vid in chunk:
            it = by.get(vid)
            if not it:
                out[pack] = dict(video_id=vid, missing=True)
                continue
            st = it['status']
            out[pack] = dict(video_id=vid, privacy=st['privacyStatus'],
                             publish_at=st.get('publishAt'), desc=it['snippet'].get('description', ''))
    return out


def write_snapshot():
    ids = yt_api.load_ids()
    state = fetch(list(ids))
    SNAP.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding='utf8')
    sched = sum(1 for v in state.values() if v.get('publish_at'))
    print(f'snapshot: {len(state)} 本（予約 {sched} 本） -> {SNAP}')
    for pack in sorted(state):
        v = state[pack]
        if v.get('publish_at'):
            print(f'  {pack:24s} {v["video_id"]:14s} {v["publish_at"]}')


def check():
    snap = json.loads(SNAP.read_text(encoding='utf8'))
    ids = yt_api.load_ids()
    now = fetch(list(set(snap) | set(EXPECTED)))

    fails = []
    notes = []
    for pack, old in snap.items():
        cur = now.get(pack)
        if not cur or cur.get('missing'):
            fails.append(f'{pack}: 動画が消えている（{old["video_id"]}）')
            continue
        if pack not in ids:
            fails.append(f'{pack}: 台帳に無い')
            continue
        new_id = ids[pack]['video_id']
        if new_id != old['video_id']:
            deleted = ids[pack].get('deleted', [])
            if old['video_id'] not in deleted:
                fails.append(f'{pack}: IDが変わったが旧IDが deleted に無い（{old["video_id"]}）')
            if old.get('publish_at') and cur.get('publish_at') != old['publish_at']:
                fails.append(f'{pack}: 公開予約がずれた {old["publish_at"]} -> {cur.get("publish_at")}')
            else:
                notes.append(f'{pack}: 差し替え済み {old["video_id"]} -> {new_id}')
        else:
            if old.get('publish_at') and cur.get('publish_at') != old['publish_at']:
                if cur.get('publish_at') is None and cur.get('privacy') == 'public':
                    # 予約時刻を過ぎて公開された（publishAt は消える）— 正常
                    notes.append(f'{pack}: 公開された（予約 {old["publish_at"]}）')
                else:
                    fails.append(f'{pack}: 予約が変わった {old.get("publish_at")} -> {cur.get("publish_at")}')
            elif not old.get('publish_at') and cur.get('publish_at'):
                notes.append(f'{pack}: 予約が入った {cur["publish_at"]}')

    # Short の概要欄リンクが、台帳の長尺の現IDを指しているか
    for pack, cur in now.items():
        if not pack.startswith('short_'):
            continue
        slug = pack[6:]
        spec_path = R / 'data' / f'short_{slug}.json'
        if not spec_path.exists():
            notes.append(f'{pack}: spec が無いのでリンク確認を飛ばした')
            continue
        long_id = json.loads(spec_path.read_text(encoding='utf8')).get('long_id')
        owners = [p for p, v in ids.items() if not p.startswith('short_') and v['video_id'] == long_id]
        if not owners:
            fails.append(f'{pack}: spec の long_id {long_id} が台帳の長尺に無い（古いID）')
            continue
        desc = cur.get('desc', '')
        if f'youtu.be/{long_id}' not in desc:
            got = [t.split('youtu.be/')[1].split()[0] for t in desc.split() if 'youtu.be/' in t]
            fails.append(f'{pack}: 概要欄リンクが長尺の現IDでない（{got} != {long_id}）')

    # これから上げる Short（スナップショットに無いもの）
    for pack, want in EXPECTED.items():
        cur = now.get(pack)
        if not cur:
            notes.append(f'{pack}: まだ上がっていない（予定 {want}）')
            continue
        if cur.get('publish_at') != want:
            fails.append(f'{pack}: 公開予約が {cur.get("publish_at")}（予定 {want}）')

    # 公開予約が未設定だった長尺
    for pack, want in EXPECTED_LONG.items():
        cur = now.get(pack)
        if not cur:
            fails.append(f'{pack}: 動画が無い')
            continue
        got = cur.get('publish_at')
        if got != want:
            notes.append(f'{pack}: 予約がまだ {got}（予定 {want}）')

    # 同じ公開時刻の重複
    slots = {}
    for pack, v in now.items():
        at = v.get('publish_at')
        if at:
            slots.setdefault(at, []).append(pack)
    for at, packs in slots.items():
        if len(packs) > 1:
            fails.append(f'同じ時刻に複数: {at} -> {", ".join(sorted(packs))}')

    for n in notes:
        print('  ' + n)
    print(f'予約 {sum(1 for v in now.values() if v.get("publish_at"))} 本 / 公開済み '
          f'{sum(1 for v in now.values() if v.get("privacy") == "public")} 本')
    for f in fails:
        print('NG ' + f)
    print('OK' if not fails else f'NG {len(fails)} 件')
    return 1 if fails else 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--write' in a:
        write_snapshot()
    elif '--check' in a:
        sys.exit(check())
    else:
        sys.exit(__doc__)
