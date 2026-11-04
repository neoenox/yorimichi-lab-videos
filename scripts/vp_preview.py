"""場面の一覧と、重なりの自動検出：python scripts/vp.py <slug> preview
各文の少しあとの1コマを描き（3並列。NVENC は使わない）、次を自動で調べて、一覧画像にまとめる。
  ・画面の部品どうしの重なり（部品を1つずつ描いて、実際に描かれた画素どうしの交差を数える）
  ・部品が字幕の文字にかかっていないか
  ・部品が字幕の帯（y850〜）にかかっていないか
出力：out/<slug>_pv/sheet_*.png（3×3の一覧。問題のあるコマは赤枠）、report.txt、results.json
注意：背景と battle_map の中の名札どうしの重なりは、検出しない（目で見る）。"""
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

SKIP_NAMES = ('pop_bgimg',)
SKIP_T = ('shade', 'art')
STRONG = 90        # 部品が描いた画素とみなす、背景との差の大きさ（影を除く）
OVERLAP_PX = 1500  # 部品どうしの重なりとみなす画素数
SUBS_PX = 200      # 字幕の文字にかかるとみなす画素数
BAND_Y, BAND_PX = 850, 400


def jobs_of(V):
    out = []
    per = {}
    for x in V['SEGS']:
        ci = x['scene']
        si = per.get(ci, 0)
        per[ci] = si + 1
        dur = x['end'] - x['start']
        out.append(dict(ci=ci, si=si, t=round(x['start'] + min(1.2, dur * 0.8), 3)))
    return out


def run(V, k=3):
    P, slug = V['P'], V['SLUG']
    d = P(f'out/{slug}_pv')
    d.mkdir(parents=True, exist_ok=True)
    for f in d.glob('*'):
        f.unlink()
    J = jobs_of(V)
    groups = [J[i::k] for i in range(k)]
    procs = []
    t0 = time.time()
    for i, g in enumerate(groups):
        if not g:
            continue
        jf = d / f'job_{i}.json'
        jf.write_text(json.dumps(g), encoding='utf8')
        procs.append(subprocess.Popen([sys.executable, str(Path(V['__file__']).resolve()), slug, 'pvpart', str(jf)], cwd=str(V['ROOT']), env={**__import__('os').environ, 'PYTHONIOENCODING': 'utf8'}))
    rc = [p.wait() for p in procs]
    if any(rc):
        raise SystemExit(f'preview の描画に失敗（{rc}）。上のエラーを見る')
    res = []
    for f in sorted(d.glob('result_*.json')):
        res += json.loads(f.read_text(encoding='utf8'))
    res.sort(key=lambda r: (r['ci'], r['si']))
    json.dump(res, open(d / 'results.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    # 一覧
    W_, H_ = 640, 360
    keys = [c['key'] for c in V['SPEC']['chapters']]
    sheets = 0
    for s0 in range(0, len(res), 9):
        sh = Image.new('RGB', (W_ * 3, H_ * 3), (20, 20, 20))
        dr = ImageDraw.Draw(sh)
        for j, r in enumerate(res[s0:s0 + 9]):
            im = Image.open(d / r['png']).convert('RGB')
            x, y = (j % 3) * W_, (j // 3) * H_
            sh.paste(im, (x, y))
            bad = bool(r['issues'])
            dr.rectangle((x, y, x + W_ - 1, y + H_ - 1), outline=(255, 40, 40) if bad else (60, 60, 60), width=5 if bad else 1)
            dr.rectangle((x, y, x + 250, y + 22), fill=(0, 0, 0))
            dr.text((x + 4, y + 4), f'{keys[r["ci"]]} #{r["si"]}  t={r["t"]:.0f}s' + ('  !' * bad), fill=(255, 255, 0) if bad else (255, 255, 255))
        sh.save(d / f'sheet_{sheets}.png')
        sheets += 1
    lines = []
    nbad = 0
    for r in res:
        for m in r['issues']:
            lines.append(f'{keys[r["ci"]]} 文{r["si"]} (t={r["t"]:.1f}s): {m}')
        nbad += bool(r['issues'])
    (d / 'report.txt').write_text('\n'.join(lines) or '問題なし', encoding='utf8')
    for l in lines[:40]:
        print('!!', l)
    print(f'preview {slug}: {len(res)}コマ、問題のあるコマ {nbad}、一覧 {sheets}枚（{time.time() - t0:.0f}秒）→ {d}')
    return 1 if nbad else 0


def worker(V, jobfile):
    import vp_anim_pop as PP
    P, slug = V['P'], V['SLUG']
    SPEC = V['SPEC']
    d = P(f'out/{slug}_pv')
    jobs = json.loads(Path(jobfile).read_text(encoding='utf8'))
    out = []
    pop = SPEC.get('style') == 'pop'
    if pop:
        PP.bind(V)
    for j in jobs:
        ci, si, t = j['ci'], j['si'], j['t']
        full = V['render_frame'](int(t * 30)).convert('RGB')
        png = f'pv_{ci:02d}_{si:02d}.png'
        full.resize((640, 360), Image.LANCZOS).save(d / png)
        bg = PP.background(ci, t) if pop else Image.new('RGBA', (1920, 1080), V['NAVY'] + (255,))
        dr = ImageDraw.Draw(bg, 'RGBA')
        V['header'](dr, ci)
        base = np.asarray(bg.convert('RGB')).astype(int)
        cx = V['Ctx'](ci, t)
        masks = []
        issues = []
        for ii, it in enumerate(SPEC['chapters'][ci]['scene']):
            if it['t'] in SKIP_T or it.get('name') in SKIP_NAMES:
                continue
            im2 = bg.copy()
            d2 = ImageDraw.Draw(im2, 'RGBA')
            try:
                (V['it_image'] if it['t'] == 'image' else V['ITEMS'][it['t']])(im2, d2, cx, it)
            except Exception as e:   # 描画の誤りは、問題として残す
                issues.append(f'項目{ii + 1}({it.get("name") or it["t"]}) の描画で例外: {type(e).__name__}: {str(e)[:80]}')
                continue
            m = np.abs(np.asarray(im2.convert('RGB')).astype(int) - base).max(axis=2) > STRONG
            if m.sum() < 50:
                continue
            ys, xs = np.where(m)
            label = f'項目{ii + 1}:{it.get("name") or it["t"]}' + (':' + str(it['items'][0].get('text', ''))[:8] if it.get('name') == 'pop_rows' and it.get('items') else (':' + str(it.get('text', ''))[:8] if it.get('text') else ''))
            masks.append((ii, label, m, (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))))
            if m[BAND_Y:1060].sum() > BAND_PX:
                issues.append(f'{label} が字幕の帯（y{BAND_Y}〜）にかかる')
        lay = V['_subs_layer'](ci, t, 1.0)
        sm = (np.asarray(lay.split()[3]) > 140) if lay else None
        for a in range(len(masks)):
            if sm is not None:
                n = int((masks[a][2] & sm).sum())
                if n > SUBS_PX:
                    issues.append(f'{masks[a][1]} が字幕の文字にかかる（{n}画素）')
            for b in range(a + 1, len(masks)):
                n = int((masks[a][2] & masks[b][2]).sum())
                if n > OVERLAP_PX:
                    issues.append(f'{masks[a][1]} と {masks[b][1]} が重なる（{n}画素）')
        out.append(dict(ci=ci, si=si, t=t, png=png, issues=issues))
    idx = Path(jobfile).stem.split('_')[-1]
    (d / f'result_{idx}.json').write_text(json.dumps(out, ensure_ascii=False), encoding='utf8')
