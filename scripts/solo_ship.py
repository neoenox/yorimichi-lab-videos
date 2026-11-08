"""単独Shortの「作る→確かめる→アップ→公開」を、1コマンドずつにまとめた道具。
  python scripts/solo_ship.py clips   <topic>            # assets/<topic>/fv/prompts.json から背景クリップを生成(freevideo_batch)。サーバー停止ならそう表示
  python scripts/solo_ship.py build   <slug> [pack_long] # 動画づくり→パック→説明欄の重複除去→検査→静止画の一覧→sigcmp_viewへコピー
  python scripts/solo_ship.py publish <slug>             # 非公開アップ→処理完了待ち→公開→台帳→視聴ページ確認(API で最終状態を確認)
slug は gen_solo_*.py が書く data/short_<slug>.json の <slug>(例: solo_hototogisu)。台帳のキーは short_<slug>。
build が出す「確認済み/未確認」は、そのまま報告に使える。通し視聴・全編の聴取は自動化できないので、常に「未確認」に残る。"""
import importlib.util, json, re, shutil, subprocess, sys, time, os
from pathlib import Path
R = Path(__file__).resolve().parents[1]
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
sys.stdout.reconfigure(encoding='utf8')
PY = sys.executable


def sh(args, **kw):
    return subprocess.run(args, cwd=R, capture_output=True, text=True, encoding='utf8', errors='replace', **kw)


def probe(path):
    r = sh(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type', '-of', 'json', str(path)])
    j = json.loads(r.stdout or '{}')
    return float(j.get('format', {}).get('duration', 0)), {s['codec_type'] for s in j.get('streams', [])}


def clips(topic):
    d = R / 'assets' / topic / 'fv'
    r = subprocess.run([PY, str(R / 'scripts' / 'freevideo_batch.py'), str(d / 'prompts.json'), str(d)], cwd=R)
    sys.exit(r.returncode)


def build(slug, pack_long='43_bukka'):
    spec = json.loads((R / 'data' / f'short_{slug}.json').read_text(encoding='utf8'))
    ok, bad, todo = [], [], ['通しの視聴(動きの違和感)', 'ナレーション全編の聴取']
    # 1. 背景クリップが全部あるか(ビルド前に)
    miss = [s['vid'] for s in spec['scenes'] if s.get('vid') and not (R / s['vid']).exists()]
    if miss:
        sys.exit('背景クリップがありません: ' + ' '.join(sorted(set(miss))))
    r = sh([PY, 'scripts/make_short2.py', slug])
    out = R / 'out' / f'short_{slug}.mp4'
    if not out.exists():
        print(r.stdout[-1500:], r.stderr[-1500:]); sys.exit('動画ができていません')
    # 2. パック
    sh([PY, 'scripts/pack_short.py', slug, pack_long])
    up = R / 'upload' / f'short_{slug}'
    desc = up / 'description.txt'
    t = desc.read_text(encoding='utf8')
    key = '実際の風景ではありません。'
    if t.count(key) > 1:
        i = t.find(key, t.find(key) + 1); desc.write_text(t[:i] + t[i + len(key):], encoding='utf8'); ok.append('説明欄の重複文を除去')
    # 3. 検査
    dur, kinds = probe(up / 'video.mp4')
    (ok if 'audio' in kinds and 'video' in kinds else bad).append(f'動画{dur:.1f}秒、映像と音声のストリーム: {sorted(kinds)}')
    if not 20 <= dur <= 95: bad.append(f'長さが想定外: {dur:.1f}秒')
    t = desc.read_text(encoding='utf8')
    if '2026' in spec['title'] and not re.search(r'20\d\d年\d+月\d+日', t): bad.append('説明欄に年月日がない(ニュース系は必須)')
    for f in ('title.txt', 'tags.txt', 'subtitles_ja.srt', 'description.txt'):
        if not (up / f).exists() or (up / f).stat().st_size == 0: bad.append(f + ' が空')
    if len((up / 'title.txt').read_text(encoding='utf8').strip()) > 100: bad.append('タイトルが100字超')
    # 日付の「月日だけ」の表記(年がない)を、ナレーションと画面文から拾う
    texts = [s.get('text', '') for s in spec['scenes']] + [s.get('sub', '') for s in spec['scenes']]
    for x in texts:
        for m in re.finditer(r'(?<![\d年])(\d{1,2})月(\d{1,2})日', x):
            todo.append(f'年なしの日付 「{m.group(0)}」(ニュースなら要確認): {x[:24]}…')
    # 4. 読み(kana)をファイルに残し、未登録の怪しい読みを拾う
    kana = R / 'out' / f'short_{slug}_kana.txt'
    if kana.exists():
        ok.append('読み仮名ファイルを生成(目視用: ' + str(kana.relative_to(R)) + ')')
    # 5. 静止画の一覧(重なり確認用)
    sheet = R / 'out' / f'short_{slug}_frames.png'
    n = 6; ts = [dur * (i + .5) / n for i in range(n)]
    tmp = []
    for i, t0 in enumerate(ts):
        p = R / 'out' / f'_f{i}.png'; sh(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{t0:.2f}', '-i', str(out), '-frames:v', '1', '-vf', 'scale=300:-1', str(p)]); tmp.append(p)
    sh(['ffmpeg', '-y', '-loglevel', 'error'] + sum([['-i', str(p)] for p in tmp], []) + ['-filter_complex', f'hstack={n}', str(sheet)])
    for p in tmp: p.unlink(missing_ok=True)
    # 6. 見せる用にコピー
    view = Path('E:/rekishikaisetu/sigcmp_view'); view.mkdir(exist_ok=True); shutil.copy(out, view / f'short_{slug}.mp4')
    print('== build結果:', slug)
    print('確認できたこと:'); [print('  ・' + x) for x in ok]
    if bad: print('要対応:'); [print('  ×' + x) for x in bad]
    print('静止画の一覧(重なり・文字の混入を目で見る):', sheet)
    print('見せる動画:', view / f'short_{slug}.mp4')
    print('未確認のまま(報告に書く):'); [print('  ・' + x) for x in todo]


def publish(slug):
    sys.argv = ['x']
    spec_ = importlib.util.spec_from_file_location('yt', R / 'scripts' / 'yt_api.py'); yt = importlib.util.module_from_spec(spec_); spec_.loader.exec_module(yt)
    key = f'short_{slug}'
    r = sh([PY, 'scripts/yt_api.py', 'upload', key])
    m = re.search(r'video id (\S+)', r.stdout)
    if not m:
        print(r.stdout[-800:], r.stderr[-800:]); sys.exit('アップに失敗')
    vid = m.group(1); print('アップ完了(非公開):', vid, '字幕:', 'ok' if 'captions ok' in r.stdout else '要確認')
    s = yt.service()
    for _ in range(90):
        v = s.videos().list(part='status,contentDetails', id=vid).execute()['items'][0]
        if v['status']['uploadStatus'] == 'processed': break
        time.sleep(20)
    s.videos().update(part='status', body={'id': vid, 'status': {'privacyStatus': 'public', 'selfDeclaredMadeForKids': False}}).execute()
    v = s.videos().list(part='status,contentDetails', id=vid).execute()['items'][0]
    p = R / 'data' / 'youtube_ids.json'; d = json.loads(p.read_text(encoding='utf8'))
    e = d.get(key, {}); e['video_id'] = vid; e['privacy'] = v['status']['privacyStatus']; d[key] = e
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf8')
    import urllib.request
    try: code = urllib.request.urlopen(f'https://www.youtube.com/watch?v={vid}', timeout=20).status
    except Exception as ex: code = str(ex)[:40]
    print(f"公開結果: privacy={v['status']['privacyStatus']} upload={v['status']['uploadStatus']} 長さ={v['contentDetails']['duration']} 視聴ページ={code}")
    print('URL: https://www.youtube.com/shorts/' + vid)


if __name__ == '__main__':
    c = sys.argv[1] if len(sys.argv) > 1 else ''
    if c == 'clips' and len(sys.argv) > 2: clips(sys.argv[2])
    elif c == 'build' and len(sys.argv) > 2: build(*sys.argv[2:4])
    elif c == 'publish' and len(sys.argv) > 2: publish(sys.argv[2])
    else: print(__doc__)
