"""builder4: 夕焼けShort v4 の spec を作る。

v3 の spec を読み、最後のナレーションから登録誘導だけを消す。
  - ytcore/make_short2.py の main() は nolong のとき、末尾のナレーションを
    end_q + '出典は、説明欄にまとめています。チャンネル登録も、お願いします。' に
    差し替える。spec 側にその文を書いても main() に上書きされるため、
    v4 用ビルド側で end_text_plain を使う契約にする。
  - hook_card=false、締めの挨拶なし、修正済み台本は v3 から維持する。
v3 の JSON・既存 mp4・既存スクリプトは上書きしない。
v4 は data/short_solo_sunset_v4.json にだけ書き出す。
"""
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import procedure_gate
procedure_gate.require()

SRC = R / 'data' / 'short_solo_sunset_v3.json'
DST = R / 'data' / 'short_solo_sunset_v4.json'
OLD_END = '夕焼けが赤い理由、どこで聞いた話でしたか？出典は、説明欄にまとめています。チャンネル登録も、お願いします。'


def main():
    spec = json.loads(SRC.read_text(encoding='utf8'))
    if spec.get('hook_card') is not False:
        raise SystemExit('v3 の hook_card=false が維持されていません')
    scenes = spec['scenes']
    if scenes[-2]['text'] != '波長の短い光は散乱され、赤が届く。だから夕焼けは赤い。':
        raise SystemExit('修正済みの最終ナレーションが維持されていません')
    if '寄り道ラボ' in scenes[-2]['text'] or 'また寄り道' in scenes[-2]['text']:
        raise SystemExit('締めの挨拶が残っています')
    if spec.get('end_q') != '夕焼けが赤い理由、どこで聞いた話でしたか？':
        raise SystemExit(f'想定と違う end_q: {spec.get("end_q")!r}')

    # make_short2.main() の nolong 分岐が足す定型文を、このフィールドで置き換える。
    # v4 用ビルド側だけが参照する。共通パッケージは書き換えない。
    spec['end_text_plain'] = '夕焼けが赤い理由、どこで聞いた話でしたか？出典は、説明欄にまとめています。'
    if 'チャンネル登録' in spec['end_text_plain'] or 'お願いします' in spec['end_text_plain']:
        raise SystemExit('置換後の文に登録誘導が残っています')

    DST.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + '\n', encoding='utf8')
    print(f'ok {DST.relative_to(R)} hook_card={spec["hook_card"]} scenes={len(scenes)}')
    print('end_text_plain=' + spec['end_text_plain'])


if __name__ == '__main__':
    main()
