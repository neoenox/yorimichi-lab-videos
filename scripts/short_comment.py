"""公開済みの Short に、対応する長尺への案内コメントを投稿する。

「固定」は API 非対応なので、投稿だけを自動化する（固定は Studio で1本ずつ押す）。

  python scripts/short_comment.py --dry            # 本文を out/_f2_text.txt に書き出すだけ
  python scripts/short_comment.py --limit 3        # 先頭3本だけ投稿
  python scripts/short_comment.py                  # 未投稿のすべて

対応（Short → 長尺）は data/short_*.json の long_id を使う。
投稿済みは data/short_comment_done.json に残し、二重投稿しない
（自分のチャンネルが同じ長尺IDを案内しているコメントがあれば skip）。
quota: commentThreads.insert 50ユニット/本、list 1ユニット/本。
"""
import io
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))
import yt_api  # noqa: E402

STATE = R / 'data/short_comment_done.json'
STATUS = R / 'out/youtube_status.json'
AM = 'https://youtu.be/'
DRY = '--dry' in sys.argv
LIMIT = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else None


def secs(d):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d or '')
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def trim_sentences(s, limit=100):
    """文の切れ目で切る（途中でぶった切ると読めなくなるため）。"""
    out = ''
    for part in re.findall(r'[^。]*。|[^。]+$', s or ''):
        if len(out) + len(part) > limit:
            break
        out += part
    return out.strip()


def build_text(title, hook, long_id):
    text = f'くわしくは本編で →「{title}」\n{AM}{long_id}'
    h = trim_sentences(hook)
    if h:
        text += f'\n{h}'
    return text


def collect():
    """公開済み Short のうち、まだ投稿していないもの。"""
    S = json.loads(STATUS.read_text(encoding='utf8'))
    ids = json.loads((R / 'data/youtube_ids.json').read_text(encoding='utf8'))
    state = json.loads(STATE.read_text(encoding='utf8')) if STATE.exists() else {}
    pub = {r['id']: r for r in S['public_with_views']}
    jobs = []
    for f in sorted((R / 'data').glob('short_*.json')):
        slug = f.stem
        try:
            d = json.loads(f.read_text(encoding='utf8'))
        except Exception:
            continue
        if not isinstance(d, dict) or not d.get('long_id'):
            continue
        sh = (ids.get(slug) or {}).get('video_id')
        if not sh or sh not in pub:
            continue
        if (state.get(slug) or {}).get('short') == sh:
            continue
        jobs.append(dict(slug=slug, short=sh, long=d['long_id'], hook=d.get('hook', ''),
                         views=pub[sh]['views']))
    jobs.sort(key=lambda r: -r['views'])
    return jobs[:LIMIT] if LIMIT else jobs


def main():
    jobs = collect()
    if not jobs:
        print('no jobs (すべて投稿済み、または公開済みの Short がない)')
        return

    yt = yt_api.service()
    if DRY:
        lines = []
        for j in jobs:
            v = yt.videos().list(part='snippet', id=j['long']).execute()['items'][0]['snippet']
            lines.append(f"== {j['slug']:<20} {j['short']} -> {j['long']}  ({j['views']}v)\n"
                         + build_text(v['title'], j['hook'], j['long']))
        (R / 'out').mkdir(exist_ok=True)
        io.open(R / 'out/_f2_text.txt', 'w', encoding='utf-8').write('\n\n'.join(lines) + '\n')
        print(f'dry {len(jobs)} 本  推定 {len(jobs) * 50} ユニット → out/_f2_text.txt')
        return

    me = yt.channels().list(part='id', mine=True).execute()['items'][0]['id']
    state = json.loads(STATE.read_text(encoding='utf8')) if STATE.exists() else {}
    for j in jobs:
        v = yt.videos().list(part='snippet', id=j['long']).execute()['items'][0]['snippet']
        text = build_text(v['title'], j['hook'], j['long'])

        exists = False
        try:
            ct = yt.commentThreads().list(part='snippet', videoId=j['short'], maxResults=100,
                                          textFormat='plainText').execute()
            for it in ct.get('items', []):
                c = it['snippet']['topLevelComment']['snippet']
                if c['authorChannelId']['value'] == me and j['long'] in c['textDisplay']:
                    exists = True
                    break
        except Exception as e:
            print('  (list failed)', j['slug'], type(e).__name__)
        if exists:
            print(f'skip  {j["slug"]:<20} 既に案内コメントあり')
            state[j['slug']] = dict(short=j['short'], long=j['long'], comment_id='(existing)')
            continue

        try:
            r = yt.commentThreads().insert(
                part='snippet',
                body=dict(snippet=dict(videoId=j['short'],
                                       topLevelComment=dict(snippet=dict(textOriginal=text))))).execute()
        except Exception as e:
            print(f'NG    {j["slug"]:<20} {type(e).__name__}: {e}')
            continue
        st = r['snippet']['topLevelComment']['snippet'].get('moderationStatus', 'published')
        state[j['slug']] = dict(short=j['short'], long=j['long'],
                                comment_id=r['id'], status=st)
        print(f'ok    {j["slug"]:<20} {r["id"]} [{st}]')
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1) + '\n', encoding='utf8')

    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1) + '\n', encoding='utf8')


if __name__ == '__main__':
    main()
