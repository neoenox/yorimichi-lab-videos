"""make_spec_<slug>.py の共通部分。台本（09_script_v2.md）の行番号 at/until を文の番号に直し、画面の枠を調整し、背景イラストを差し込んで spec を書く。
usage（各 make_spec_*.py の末尾）: from spec_common import finalize; finalize(spec, ART)"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from specart import inject, inject2
R = Path(__file__).resolve().parents[1]
TOP = [60, 170, 1860, 235]


def _fit(o):
    if isinstance(o, dict):
        if o.get('t') == 'panel' and o.get('title'):
            h = o['box'][3] - o['box'][1]
            if h < 112:
                tx = o['title'] + '：' + o['text']; sz = min(o.get('size', 40), 40, int((o['box'][2] - o['box'][0] - 70) / len(tx)))
                if sz >= 26: o['title'] = None; o['text'] = tx; o['size'] = sz
                else: o['size'] = min(o.get('size', 40), 30)
            else: o['size'] = min(o.get('size', 40), 40 if h < 125 else 46)
        for v in o.values(): _fit(v)
    elif isinstance(o, list):
        for v in o: _fit(v)


def _starts(theme_dir):
    t = (R / 'docs' / 'themes' / theme_dir / '09_script_v2.md').read_text(encoding='utf8')
    out = []
    for c in re.split('\n## ', t)[1:]:
        if not re.match('章(\\d+)　', c.split('\n')[0]): continue
        starts, n = [], 0
        for l in c.split('\n'):
            if re.match('^\\d+\\. ', l):
                body = re.sub('〔[^〕]*〕', '', re.sub('^\\d+\\. ', '', l)).strip()
                starts.append(n); n += len([x for x in body.split('。') if x.strip()])
        starts.append(n)
        out.append(starts)
    return out


def _remap(o, st):
    f = lambda i: None if i is None else st[min(i, len(st) - 1)]
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if k in ('at', 'until', 'title_at', 'at2') and isinstance(v, int): o[k] = f(v)
            else: _remap(v, st)
    elif isinstance(o, list):
        for v in o: _remap(v, st)


def finalize(spec, art, art2=None):
    S = _starts(spec['theme_dir'])
    assert len(S) == len(spec['chapters']), (len(S), len(spec['chapters']))
    for ch, st in zip(spec['chapters'], S):
        _remap(ch['scene'], st)
        if 'opener_until' in ch: ch['opener_until'] = st[min(ch['opener_until'], len(st) - 1)]
    _fit(spec)
    if all((R / 'assets' / spec['slug'] / f'art_{v}.png').exists() for v in set(art.values())):
        inject(spec, art)
        if art2:   # {章key: (画像名, 章内の行番号)}。行番号は文の番号に直して差し込む
            keys = [c['key'] for c in spec['chapters']]
            inject2(spec, {k: (n, S[keys.index(k)][min(a, len(S[keys.index(k)]) - 1)]) for k, (n, a) in art2.items()})
    else:
        print('背景イラストが未そろい：art は差し込まない')
    (R / 'data' / f"{spec['slug']}_spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8')
    print('spec written', spec['slug'])
