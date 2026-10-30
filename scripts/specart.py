"""spec に、章ごとの背景イラスト（art＋shade）を差し込む。呼び出し: inject(spec, {章key: 画像名}, alpha=0.66)"""
NOTE = 'イメージ（生成画像）。実際の場面の再現ではありません'
CREDIT = '・場面のイラスト:ChatGPT・Codex(OpenAI)による生成イラスト(イメージです。実際の場面・人物・資料の再現ではありません)'

def inject(spec, mapping, alpha=0.66):
    slug = spec['slug']
    spec['images'] = {**spec.get('images', {}), **{n: dict(file=f'assets/{slug}/art_{n}.png') for n in set(mapping.values())}}
    box = [60, 170, 1860, 850]
    for i, ch in enumerate(spec['chapters']):
        n = mapping.get(ch['key'])
        if not n:
            continue
        ch['scene'][:0] = [dict(t='art', name=n, box=box, at=0, dim=0.8, dir=1 if i % 2 == 0 else -1, note=NOTE),
                           dict(t='shade', box=box, at=0, alpha=alpha)]
    cl = spec['desc'].setdefault('credit_lines', [])
    if not any('場面のイラスト' in c for c in cl):
        for k, c in enumerate(cl):
            if c.startswith('・サムネイルの背景:Codex'):
                cl[k] = '・サムネイルの背景と場面のイラスト:ChatGPT・Codex(OpenAI)による生成イラスト(イメージです。実際の場面・人物・資料の再現ではありません)'
                break
        else:
            cl.append(CREDIT)


def inject2(spec, mapping, alpha=0.66):
    """章の途中（文 at 番目）で、2枚目の背景イラストに切り替える。mapping: {章key: (画像名, at)}。1枚目の art＋shade の直後に差し込む（後から描くので1枚目を覆う）。"""
    slug = spec['slug']
    spec['images'] = {**spec.get('images', {}), **{v[0]: dict(file=f'assets/{slug}/art_{v[0]}.png') for v in mapping.values()}}
    box = [60, 170, 1860, 850]
    for i, ch in enumerate(spec['chapters']):
        if ch['key'] not in mapping:
            continue
        n, at = mapping[ch['key']]
        pos = next((k for k, it in enumerate(ch['scene']) if it.get('t') == 'shade'), -1) + 1
        ch['scene'][pos:pos] = [dict(t='art', name=n, box=box, at=at, dim=0.8, dir=-1 if i % 2 == 0 else 1, note=NOTE),
                                dict(t='shade', box=box, at=at, alpha=alpha)]
