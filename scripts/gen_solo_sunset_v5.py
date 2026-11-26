"""builder5: 夕焼けShort v5 の spec を作る（Google AI レビュー反映）。

v4 の spec を読み、Gemini の指摘のうち次を反映する。
  [優先度1] 画面上の情報重複を減らす: 中央の小さい sub 帯を空にする。
  [優先度2] 小文字要素を減らす: 吹き出しイベントを3→2に絞り、短い語にする。
  [優先度4] 冒頭の核心を早める: 最初の字幕文を短くして「通る距離」を最初に置く。

v4 の JSON・既存 mp4・既存スクリプトは上書きしない。
v5 は data/short_solo_sunset_v5.json にだけ書き出す。
"""
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import procedure_gate
procedure_gate.require()

SRC = R / 'data' / 'short_solo_sunset_v4.json'
DST = R / 'data' / 'short_solo_sunset_v5.json'


def main():
    spec = json.loads(SRC.read_text(encoding='utf8'))
    if spec.get('hook_card') is not False:
        raise SystemExit('v4 の hook_card=false が維持されていません')
    scenes = spec['scenes']
    if len(scenes) != 7:
        raise SystemExit(f'想定と違うシーン数: {len(scenes)}')
    if 'チャンネル登録' in spec.get('end_text_plain', ''):
        raise SystemExit('v4 の登録誘導削除が維持されていません')

    # 優先度4: 冒頭で「通る距離」を先に出す。内容は v4 の主張を変えない。
    scenes[0]['text'] = '夕焼けが赤いのは、光が大気を通る距離が違うから。空が青いのと同じ仕組みです。'

    # 優先度1: 中央の sub 帯を空にして、見出し・吹き出し・字幕の役割を分ける。
    # 出典は credit / notes（概要欄）に集約済み。
    for sc in scenes:
        if 'sub' in sc:
            sc['sub'] = ''
        if 'src' in sc:
            sc['src'] = ''

    # 優先度2: 吹き出しイベントを2つに絞り、短い語にする。
    new_events = [
        [('短い波長', '強く散乱'), ('紫', '高い所で')],
        [('届く色', '青が多い'), ('空', '青く見える')],
        [('夕方', '距離が長い'), ('届く色', '赤が残る')],
        [('昼', '距離が短い'), ('夕', '距離が長い')],
    ]
    # シーン順: 0=導入, 1=色, 2=散乱, 3=青, 4=夕方, 5=まとめ, 6=end
    for idx, ev in zip((2, 3, 4, 5), new_events):
        viz = scenes[idx].get('viz', {})
        if viz.get('type') != 'timeline':
            raise SystemExit(f'scene {idx} が timeline ではありません')
        viz['events'] = [[a, b] for a, b in ev]
        viz['gap'] = 3.2
        scenes[idx]['viz'] = viz

    DST.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + '\n', encoding='utf8')
    print(f'ok {DST.relative_to(R)} scenes={len(scenes)} sub_cleared=True')
    print('opening=' + scenes[0]['text'])


if __name__ == '__main__':
    main()
