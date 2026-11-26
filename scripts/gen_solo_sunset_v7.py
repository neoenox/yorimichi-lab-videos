"""lead: 話速 0.95 と「晴天時には」条件を反映した夕焼けShort v7 spec。

v6 spec を読み、次を反映する。
  - 話速を 1.45 → 0.95 に戻すため、ナレーションを約178文字まで短縮する
    （v6 は255文字・40.13秒）。
  - シーン3 に気象庁FAQ原文どおり「晴天時には」の条件を入れる。
  - v6 の背景差し替え（シーン4=clip6／シーン5=clip7）と hook_card=false を維持。

既存 mp4・spec・スクリプトは上書きしない。v7 は data/short_solo_sunset_v7.json にだけ書き出す。
"""
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import procedure_gate
procedure_gate.require()

SRC = R / 'data' / 'short_solo_sunset_v6.json'
DST = R / 'data' / 'short_solo_sunset_v7.json'

# 話速 0.95 で 30〜45 秒に収める短縮文。原文の事実は変えない。
NARRATION = [
    '夕焼けが赤いのは、なぜでしょう。空が青いのと同じ仕組みです。',
    '太陽光には、紫から赤まで様々な色が含まれます。',
    '晴天時には、空気分子は波長の短い光を強く散乱します。紫は届きにくくなります。',
    '届く量の多い青が強調され、空は青く見えます。',
    '夕方は太陽が地平線に近く、光が大気を通る距離が長くなります。短い光は散乱され、赤が多く届きます。',
    'だから夕焼けは赤い。',
]


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

    for i, text in enumerate(NARRATION):
        scenes[i]['text'] = text

    spec['sec'] = 45
    spec['end_text_plain'] = '夕焼けが赤い理由、どこで聞いた話でしたか？出典は、説明欄にまとめています。'
    DST.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + '\n', encoding='utf8')
    print(f'ok {DST.relative_to(R)} chars={sum(len(t) for t in NARRATION)}')


if __name__ == '__main__':
    main()
