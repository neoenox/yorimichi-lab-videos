"""旧形式（紺の背景に枠つきのパネル）の spec を、ポップ形式に自動で作り直す。台本・音声は変えない（画面だけ）。
usage: python scripts/to_pop.py <slug> [--keep-text]   data/<slug>_spec.json を読み、style='pop' にして書き戻す（元は <slug>_spec_before_pop.json）
変換の規則：
  art → pop_bgimg（ぼかした写真の背景）／shade → 消す／big・大きな panel → pop_telop／panel → pop_rows（白いカード）
  cols2・chips → pop_rows／地図の章（battle_map）→ 大きな地図（左）＋右にカード、文字・ピンは1.5倍
  table・bars・stack・timeline・flow・line・daybar・swirl・image・anim（図）は、そのまま（背景だけポップ）"""
import json, sys, shutil, copy
from pathlib import Path
R = Path(__file__).resolve().parents[1]
MAPBOX = [30, 120, 1000, 880]
GOLDCOL = {'gold': 'orange', 'org': 'orange', 'blue': 'blue', 'red': 'red', 'green': 'green'}


def pop(name, **kw): return dict(t='anim', name=name, **kw)


def big(k):
    for pl in k.get('places', []):
        if not pl.get('_note'): pl['lsize'] = int(pl.get('lsize', 24) * 1.5)
        pl.pop('_note', None)
    for u in k.get('units', []):
        u['lsize'] = int(u.get('lsize', 26) * 1.5); u['head'] = int(u.get('head', 26) * 1.3)
        if 'lab_off' in u: u['lab_off'] = [int(u['lab_off'][0] * 1.6), int(u['lab_off'][1] * 1.6)]
    for ln in k.get('lines', []): ln['lsize'] = int(ln.get('lsize', 26) * 1.5)
    for mk in k.get('marks', []): mk['lsize'] = int(mk.get('lsize', 24) * 1.5)


def rows_from_panel(e, x0=None, x1=None, y0=None, size=None):
    box = e['box']
    item = dict(at=e.get('at'), text=e['text'], col=GOLDCOL.get(e.get('col'), 'orange'))
    if e.get('until') is not None: item['until'] = e['until']
    if e.get('title'): item['tag'] = e['title']
    sz = size or max(46, min(e.get('size', 40) + 6, 56))
    return pop('pop_rows', items=[item], x0=x0 if x0 is not None else box[0] + 50, x1=x1 if x1 is not None else box[2] - 50, y0=y0 if y0 is not None else box[1], size=sz, gap=0)


def convert_chapter(ch, slug, images, art_cycle, ci):
    sc = ch['scene']; out = []
    has_map = any(e.get('t') == 'anim' and e.get('name') == 'battle_map' for e in sc)
    GRAPH = ('bars', 'table', 'timeline', 'flow', 'line', 'daybar', 'stack', 'image', 'swirl', 'cols2', 'chips')
    has_graph = any(e.get('t') in GRAPH or (e.get('t') == 'anim' and e.get('name') != 'battle_map') for e in sc)
    text_only = not has_map and not has_graph
    has_big = any(e.get('t') == 'big' for e in sc)
    plates = ['yellow', 'blue', 'pink', 'green', 'orange']; pn_ = 0
    bg_added = False
    for e in sc:
        t = e.get('t')
        if t == 'shade':
            continue
        if t == 'art':
            nm = e['name']
            if nm not in images:
                p = R / 'assets' / slug / f'art_{nm}.png'
                images[nm] = dict(file=f'assets/{slug}/art_{nm}.png') if p.exists() else None
            if images.get(nm) is None:
                images.pop(nm, None); continue
            out.append(pop('pop_bgimg', img=nm, at=e.get('at', 0), dim=.5 if not has_map else .6, blur=4 if not has_map else 9))
            if e.get('until') is not None: out[-1]['until'] = e['until']
            bg_added = True
            continue
        if t == 'big':
            out.append(pop('pop_telop', text=e['text'], x=960, y=e.get('y', 400), size=int(min(e.get('size', 60) * 1.6, 120)), at=e.get('at', 0), plate='yellow' if e.get('col') != 'red' else 'red', rot=-1.5))
            continue
        if t == 'panel':
            sz = e.get('size', 40)
            if has_map:
                out.append(rows_from_panel(e, x0=1010, x1=1880, y0=170, size=44))
            elif text_only and e.get('text') and e['box'][1] < 800:
                txt = (f"【{e['title']}】" if e.get('title') else '') + e['text']
                n = len(txt)
                tsz = 84 if n <= 16 else 72 if n <= 26 else 62 if n <= 40 else 52
                ty = (e['box'][1] + e['box'][3]) // 2 if has_big else 470
                tel = pop('pop_telop', text=txt, x=960, y=ty, size=tsz, at=e.get('at', 0), plate=plates[pn_ % len(plates)], rot=(-1.5 if pn_ % 2 == 0 else 1.5), maxw=1560)
                if e.get('until') is not None: tel['until'] = e['until']
                out.append(tel); pn_ += 1
            elif sz >= 62 and e.get('text'):
                bx = e['box']
                out.append(pop('pop_telop', text=e['text'], x=(bx[0] + bx[2]) // 2, y=(bx[1] + bx[3]) // 2, size=min(sz + 20, 110), at=e.get('at', 0), until=e.get('until'), plate='yellow', rot=-1.2))
                if out[-1].get('until') is None: out[-1].pop('until')
            else:
                out.append(rows_from_panel(e))
            continue
        if t == 'cols2':
            items = []
            for side, key in (('left', 'left'), ('right', 'right')):
                sd = e.get(key) or {}
                title = sd.get('title') or ''
                col = 'green' if '分か' in title else 'red' if '決め' in title or '不明' in title else 'blue' if side == 'left' else 'orange'
                for it in sd.get('items', []):
                    d = dict(at=it.get('at'), text=it['text'], col=col)
                    if title:
                        if len(title) <= 9: d['tag'] = title
                        else: d['text'] = f'【{title}】' + it['text']
                    if e.get('until') is not None: d['until'] = e['until']
                    elif e.get('at') is not None and False: pass
                    items.append(d)
            items.sort(key=lambda d: (d['at'] if d['at'] is not None else -1))
            n = len(items)
            sz = 54 if n <= 3 else 50 if n <= 4 else 44 if n <= 6 else 36
            out.append(pop('pop_rows', items=items, x0=110, x1=1810, y0=200 if n <= 6 else 170, size=sz, gap=22 if n <= 6 else 10))
            continue
        if t == 'chips':
            its = [dict(at=c.get('at'), text=c['text'], col='orange') for c in e.get('items', [])]
            out.append(pop('pop_rows', items=its, x0=300, x1=1620, y0=e.get('y', 250), size=54, gap=20))
            continue
        if t == 'anim' and e.get('name') == 'battle_map':
            e = copy.deepcopy(e); big(e)
            e['box'] = MAPBOX
            out.append(e)
            continue
        out.append(e)
    # 地図の章に、ぼかした背景が無ければ足す
    if has_map and not bg_added and art_cycle:
        nm = art_cycle[ci % len(art_cycle)]
        out.insert(0, pop('pop_bgimg', img=nm, at=0, dim=.6, blur=9))
    if has_map:
        out.append(pop('pop_telop', text='※位置・経路は概略の推定（資料の推定図と軍記による）', x=1440, y=835, size=28, at=0))
    ch['scene'] = out


def main(slug):
    p = R / 'data' / f'{slug}_spec.json'
    bk = R / 'data' / f'{slug}_spec_before_pop.json'
    if not bk.exists(): shutil.copy(p, bk)
    spec = json.loads(bk.read_text(encoding='utf8'))
    images = spec.setdefault('images', {})
    arts = [nm for nm, v in images.items() if v and str(v.get('file', '')).find('/art_') >= 0]
    for ci, ch in enumerate(spec['chapters']):
        convert_chapter(ch, slug, images, arts, ci)
    spec['style'] = 'pop'
    p.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf8')
    print('pop spec written', slug, len(spec['chapters']), 'chapters')


if __name__ == '__main__':
    main(sys.argv[1])
