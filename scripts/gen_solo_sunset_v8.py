"""builder8: 夕焼けShort v8 用 spec。v7 から上部3列吹き出し(timeline viz)を消し、
AI生成のプレゼン画像2枚を重ねるための指定だけを足す。

  - シーン2〜4 (index 1..3): diagram_presentation_day_v2.png  (a)(b)(c)
  - シーン5〜6 (index 4..5): diagram_presentation_compare.png (d)
  - シーン1 (index 0) と末尾カード (index 6) は図なしのまま。
  - 話速0.95(171文字)、「晴天時には」条件、hook_card=false、v6背景(clip6/clip7)、
    end_text_plain は v7 から維持。

既存 mp4・spec・スクリプトは上書きしない。v8 は data/short_solo_sunset_v8.json にだけ書き出す。
"""
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import procedure_gate
procedure_gate.require()

SRC = R / 'data' / 'short_solo_sunset_v7.json'
DST = R / 'data' / 'short_solo_sunset_v8.json'

DAY = 'assets/solo_sunset/diagram/diagram_presentation_day_v2.png'
COMPARE = 'assets/solo_sunset/diagram/diagram_presentation_compare.png'

# index -> 画像。シーン番号は 1 始まりで 2,3,4 と 5,6 に対応。
OVERLAY = {1: DAY, 2: DAY, 3: DAY, 4: COMPARE, 5: COMPARE}


def main():
    spec = json.loads(SRC.read_text(encoding='utf8'))
    scenes = spec['scenes']
    if len(scenes) != 7:
        raise SystemExit(f'想定と違うシーン数: {len(scenes)}')
    if spec.get('hook_card') is not False:
        raise SystemExit('hook_card=false が維持されていません')
    if scenes[4].get('vid') != 'assets/solo_sunset/fv/clip6.mp4':
        raise SystemExit('シーン4 の背景が v6 のままではありません')
    if scenes[5].get('vid') != 'assets/solo_sunset/fv/clip7.mp4':
        raise SystemExit('シーン5 の背景が v6 のままではありません')
    chars = sum(len(s.get('text', '')) for s in scenes)
    if chars != 171:
        raise SystemExit(f'ナレーション文字数が171ではありません: {chars}')

    for i, sc in enumerate(scenes):
        sc.pop('viz', None)   # 上部3列吹き出しを全シーンから削除する
    for i, rel in OVERLAY.items():
        p = R / rel
        if not p.is_file():
            raise SystemExit(f'採用画像が見つかりません: {p}')
        scenes[i]['overlay'] = rel

    # credit / notes は AI生成画像の模式図であることを明記する。
    spec['credit'] = spec['credit'].replace(
        '・図・表：自作（模式図）',
        '・図：AI生成の模式図（文字なし。気象庁FAQの本文どおりの内容を採用）')
    spec['notes'] = spec['notes'].replace(
        '・動画内の図(光の通り道の模式図)は自作です。',
        '・動画内の図はAI生成の模式図です。文字・署名なしのものを選び、気象庁FAQの本文と照合しました。')

    spec['sec'] = 45
    DST.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + '\n', encoding='utf8')
    print(f'ok {DST.relative_to(R)} chars={chars} overlays={len(OVERLAY)}')


if __name__ == '__main__':
    main()
