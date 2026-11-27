"""builder9: 夕焼けShort v9 用 spec。v8 から BGM だけを追加する。

  - BGM: 魔王魂「ピアノ41」(maou_bgm_piano41.mp3)。scripts/bgm_plan.py の一般プールの1曲。
    選定理由: science/雑学の一般型で、入力音量が -23 LUFS と最も低く、
    mix() の volume=0.30 でナレーションの下に自然に収まる。85.1秒あり
    44秒の Short ではループ継ぎ目が出ない。静かなピアノで夕焼けの解説に合う。
  - v8 の画像2枚の重ね合わせ、3列吹き出しなし、話速0.95、171文字、
    「晴天時には」条件、hook_card=false、締め定型挨拶なし、登録誘導なし、
    v6 の背景差し替えはすべて維持。

既存 mp4・spec・スクリプトは上書きしない。v9 は data/short_solo_sunset_v9.json にだけ書き出す。
"""
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import procedure_gate
procedure_gate.require()

SRC = R / 'data' / 'short_solo_sunset_v8.json'
DST = R / 'data' / 'short_solo_sunset_v9.json'
BGM = 'piano41'
BGM_FILE = R / 'assets' / 'bgm_maou' / f'maou_bgm_{BGM}.mp3'


def main():
    spec = json.loads(SRC.read_text(encoding='utf8'))
    scenes = spec['scenes']
    if len(scenes) != 7:
        raise SystemExit(f'想定と違うシーン数: {len(scenes)}')
    if spec.get('bgm') != 'none':
        raise SystemExit('v8 の bgm=none が維持されていません')
    if spec.get('hook_card') is not False:
        raise SystemExit('hook_card=false が維持されていません')
    if scenes[4].get('vid') != 'assets/solo_sunset/fv/clip6.mp4':
        raise SystemExit('シーン4 の背景が v6 のままではありません')
    if scenes[5].get('vid') != 'assets/solo_sunset/fv/clip7.mp4':
        raise SystemExit('シーン5 の背景が v6 のままではありません')
    chars = sum(len(s.get('text', '')) for s in scenes)
    if chars != 171:
        raise SystemExit(f'ナレーション文字数が171ではありません: {chars}')
    if not BGM_FILE.is_file():
        raise SystemExit(f'BGM が見つかりません: {BGM_FILE}')

    spec['bgm'] = BGM
    spec['bgm_reason'] = (
        '一般プールから「ピアノ41」を選択。魔王魂の曲で、入力 -23 LUFS（プール内で最も低い）'
        '・85.1秒（44秒のShortでループ不要）・穏やかなピアノで解説の邪魔をしない。'
    )
    DST.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + '\n', encoding='utf8')
    print(f'ok {DST.relative_to(R)} chars={chars} bgm={BGM}')


if __name__ == '__main__':
    main()
