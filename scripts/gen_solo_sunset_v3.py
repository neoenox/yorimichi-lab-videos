"""builder3: 夕焼けShort v3 の spec を作る。

v2 の spec を読み、次の2点だけを変える。
  1. 冒頭の結論カードを消す (hook_card=false)。オーナー指示「動画の最初のドデカフリップは不要」。
  2. 最終シーンのナレーションから締めの挨拶「寄り道ラボ、また寄り道、続けます。」を消す。
     オーナー指示「サムいからやめてほしい」。shorts-standard/PROMPT.md 項目4は
     不要な挨拶・登録誘導を禁止しており、この文に根拠は無い。
v2 の JSON・既存 mp4・既存スクリプトは上書きしない。
v3 は data/short_solo_sunset_v3.json にだけ書き出す。
"""
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import procedure_gate
procedure_gate.require()

SRC = R / 'data' / 'short_solo_sunset_v2.json'
DST = R / 'data' / 'short_solo_sunset_v3.json'


def main():
    spec = json.loads(SRC.read_text(encoding='utf8'))
    # 冒頭0〜1.9秒(ytcore の hook_on は t<3.2)の結論カードを消す。
    # answer 自体は末尾の結論カードと概要欄で使うため残す。
    spec['hook_card'] = False
    # 最終シーンの締めの挨拶を削り、結論だけの文にする。
    last = spec['scenes'][-2]           # 末尾の end シーンの手前
    old = '波長の短い光は散乱され、赤が届く。だから夕焼けは赤い。寄り道ラボ、また寄り道、続けます。'
    new = '波長の短い光は散乱され、赤が届く。だから夕焼けは赤い。'
    if last['text'] != old:
        raise SystemExit(f'想定と違う最終ナレーション: {last["text"]!r}')
    last['text'] = new
    DST.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + '\n', encoding='utf8')
    print(f'ok {DST.relative_to(R)} hook_card={spec["hook_card"]} scenes={len(spec["scenes"])}')


if __name__ == '__main__':
    main()
