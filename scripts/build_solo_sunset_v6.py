"""builder6: Google AI レビュー反映版夕焼けShort(v5)を描画する。

v4 の描画設定を維持しつつ、slug だけ solo_sunset_v6 に変える。
既存の out/short_solo_sunset*.mp4 は上書きしない。
"""
import inspect
import json
import os
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
os.environ.setdefault('YT_PROJECT_ROOT', str(R))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import procedure_gate
procedure_gate.require()

import ytcore.make_short as base
base.SPEED = 1.45
import ytcore.make_short2 as ms2


def patch_end_card():
    """nolong の末尾カードから登録誘導の1行だけを除く（この process 内のみ）。"""
    src = inspect.getsource(ms2.draw_scene)
    target = "d.text((540, top + 165), 'チャンネル登録', font=font(92, True), fill=GOLD + (A,), anchor='mm')"
    if src.count(target) != 1:
        raise SystemExit(f'想定した登録カード行が見つかりません (count={src.count(target)})')
    patched = src.replace(target, 'pass  # builder6: nolong 末尾の登録誘導カードを削除')
    ns = dict(ms2.__dict__)
    exec(compile(patched, '<builder6_draw_scene>', 'exec'), ns)
    ms2.draw_scene = ns['draw_scene']


def main_v5(slug):
    spec_path = ms2.ROOT / 'data' / f'short_{slug}.json'
    spec = json.loads(spec_path.read_text(encoding='utf8'))
    plain = spec.get('end_text_plain')
    if not plain or 'チャンネル登録' in plain or 'お願いします' in plain:
        raise SystemExit('end_text_plain が無い、または登録誘導が残っています')
    if spec.get('hook_card') is not False:
        raise SystemExit('hook_card=false が維持されていません')
    for sc in spec['scenes']:
        if sc.get('sub') or sc.get('src'):
            raise SystemExit('v5 では sub/src を空にする必要があります')

    patch_end_card()

    work = ms2.ROOT / 'cache' / f'short_{slug}'
    work.mkdir(parents=True, exist_ok=True)
    texts = [s['text'] for s in spec['scenes']]
    texts[-1] = plain
    segs, total = ms2.synth(dict(pron=spec['pron'], scenes=[dict(text=t, kind='') for t in texts]), work)
    (ms2.ROOT / 'out' / f'short_{slug}_kana.txt').write_text(
        '\n'.join(f"{s['text']}\n    {s['kana']}" for s in segs), encoding='utf8')
    print('narration', round(total, 1), 's')
    if '--kana' in sys.argv:
        return
    raw = work / 'raw.mp4'
    ms2.render(spec, segs, total, raw, slug)
    ms2.mix(spec, work, total, raw, ms2.ROOT / 'out' / f'short_{slug}.mp4')
    spec['sec'] = round(total)
    text = ms2.description(spec)
    (ms2.ROOT / 'out' / f'short_{slug}_description.md').write_text(text, encoding='utf8')
    print('done -> out/short_%s.mp4' % slug)


if __name__ == '__main__':
    sys.argv = ['make_short2', 'solo_sunset_v6'] + sys.argv[1:]
    main_v5(sys.argv[1])
