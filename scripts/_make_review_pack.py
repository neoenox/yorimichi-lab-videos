"""5本のShortを、ChatGPT査読用に: 960px/mono の確認用コピー + 台本・画面文・説明欄をまとめた依頼文を out(master側) に書く"""
import json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf8')
R = Path(__file__).resolve().parents[1]
DST = R / 'out'
for slug in sys.argv[1:]:
    spec = json.loads((R / 'data' / f'short_{slug}.json').read_text(encoding='utf8'))
    up = R / 'upload' / f'short_{slug}'
    title = (up / 'title.txt').read_text(encoding='utf8').strip()
    desc = (up / 'description.txt').read_text(encoding='utf8').strip()
    L = [f'タイトル(投稿時): {title}', '', '【場面ごとの台本(ナレーション)と画面の文字】']
    n = 0
    for s in spec['scenes']:
        if s.get('end'): continue
        n += 1
        v = s.get('viz')
        vz = ''
        if v:
            if v['type'] == 'timeline': vz = ' / '.join(f'{a}={b}' for a, b in v['events'])
            elif v['type'] == 'compare': vz = f"{v['l_label']}:{v['l_val']} vs {v['r_label']}:{v['r_val']}"
            elif v['type'] == 'bars': vz = ' / '.join(f"{i['label']}:{i['text']}" for i in v['items'])
            else: vz = json.dumps(v, ensure_ascii=False)
        L += [f'場面{n}', f"  ナレーション: {s['text']}", f"  大見出し: {s.get('big','')} / 小見出し: {s.get('sub','')} / 出典表示: {s.get('src','')}", f'  図: {vz}']
    L += ['', '【説明欄】', desc]
    (DST / f'review_{slug}.txt').write_text('\n'.join(L), encoding='utf8')
    out = DST / f'review_{slug}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(R / 'out' / f'short_{slug}.mp4'), '-vf', 'scale=-2:960,fps=6', '-ac', '1', '-b:a', '48k', '-crf', '30', str(out)])
    print(slug, out.stat().st_size // 1024, 'KB', len('\n'.join(L)), '字')
