"""builder6: AI Mode レビューの指摘を反映した夕焼けShort v6 spec。

v5 spec を読み、次を反映する。
  - 優先度4: 「夕方は太陽が地平線に近い」を説明するシーン4の背景を
    clip5（晴天の青空）から clip6（地平線に近い夕日）へ差し替える。
    シーン5（まとめ）は clip6 から clip7（結論の夕焼け）へ差し替える。

v5 の JSON・既存 mp4・既存スクリプトは上書きしない。
v6 は data/short_solo_sunset_v6.json にだけ書き出す。
"""
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import procedure_gate
procedure_gate.require()

SRC = R / 'data' / 'short_solo_sunset_v5.json'
DST = R / 'data' / 'short_solo_sunset_v6.json'


def main():
    spec = json.loads(SRC.read_text(encoding='utf8'))
    scenes = spec['scenes']
    if len(scenes) != 7:
        raise SystemExit(f'想定と違うシーン数: {len(scenes)}')
    if scenes[4].get('big') != '通る距離が長い':
        raise SystemExit('シーン4 が想定と違います')
    if scenes[4].get('vid') != 'assets/solo_sunset/fv/clip5.mp4':
        raise SystemExit('シーン4 の背景が v5 のままではありません')
    if scenes[5].get('vid') != 'assets/solo_sunset/fv/clip6.mp4':
        raise SystemExit('シーン5 の背景が v5 のままではありません')

    scenes[4]['vid'] = 'assets/solo_sunset/fv/clip6.mp4'
    scenes[5]['vid'] = 'assets/solo_sunset/fv/clip7.mp4'

    DST.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + '\n', encoding='utf8')
    print(f'ok {DST.relative_to(R)} scene4={scenes[4]["vid"]} scene5={scenes[5]["vid"]}')


if __name__ == '__main__':
    main()
