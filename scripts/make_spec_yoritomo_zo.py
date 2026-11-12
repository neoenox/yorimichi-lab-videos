"""「伝源頼朝像」Shorts（shorts/yoritomo_zo）の試作用 spec を作る。

shorts/yoritomo_zo/result.json は status=needs_review（原著・一次史料の照合が未了）なので、
標準の `to-spec` は正しく拒否する。このスクリプトは**試作用**に to_spec() を直接呼び、
別名 proto_ で data/short_proto_yoritomo_zo.json を出力する（ready の動画ではない）。

背景は scripts/make_assets_yoritomo_zo.py が作る assets/yoritomo_zo/bg_*.png
（Wikimedia Commons の PD 画像「伝源頼朝像」＋自作の地）。

  python scripts/make_spec_yoritomo_zo.py
  python scripts/make_short2.py proto_yoritomo_zo --kana   # 読みと長さだけ確認
  python scripts/make_short2.py proto_yoritomo_zo          # 描画（VOICEVOX 起動が必要）
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import shorts_standard as S  # noqa: E402

SLUG = 'yoritomo_zo'
PROTO = 'proto_' + SLUG

# 場面ごとの画面要素（viz は make_short2.py の draw_viz の型）。
# bg_0/bg_1/bg_6 は図なし（肖像を見せる）、bg_2/bg_3/bg_4/bg_5 は図あり。
SCENES = [
    dict(src='実物の資料（肖像画）'),   # 1: 冒頭・顔
    dict(src='実物の資料（肖像画）'),   # 2: 「伝」が付く
    dict(src='年表（模式図）',
         viz=dict(type='timeline', gap=1.2, events=[['1951年', '国宝に指定'], ['名称', '絹本著色伝源頼朝像']])),
    dict(src='模式図',
         viz=dict(type='compare', l_label='これまで', l_val='源頼朝', r_label='平成7年の新説', r_val='足利直義')),
    dict(src='根拠の整理（模式図）',
         viz=dict(type='timeline', gap=1.0, events=[['冠', '鎌倉末期以降の形式'], ['太刀', '13〜14世紀のもの'],
                                                    ['願文', '像を納めた記録']])),
    dict(src='公式サイトの記述（模式図）',
         viz=dict(type='timeline', gap=1.6, events=[['所蔵者の見解', '表記は変えない'],
                                                    ['示した理由', '時代は13世紀初頭']])),
    dict(src='実物の資料（肖像画）'),   # 7: 結論
]

CREDIT = ('・資料：伝源頼朝像（神護寺蔵・国宝）／Wikimedia Commons（PD-Art）。'
          'Commons のファイルページでは出典・撮影者が "Unknown source"（不明）とされています\n'
          '・図・表：自作の模式図（実在の資料の複製ではありません）\n'
          '・出典：文化庁 国指定文化財等データベース（登録番号00014）、文化遺産オンライン、神護寺公式サイト、'
          'nippon.com（2022-02-27）、テレビ朝日 グッド！モーニング（2025-08-13 放送）、帝国書院 FAQ、'
          '京都国立博物館 名品紹介、国立国会図書館レファレンス協同データベース（登録番号1000273133）\n'
          '・【試作】米倉迪夫氏・黒田日出男氏・宮島新一氏らの原著は未照合です（参照したのは二次資料）')


def main():
    res = ROOT / 'shorts' / SLUG / 'result.json'
    data = json.loads(res.read_text(encoding='utf-8'))
    ok, issues = S.check(str(res))
    errs = [m for lv, m in issues if lv == 'ERROR']
    if errs:
        sys.exit('標準の検査に ERROR: %s' % errs)
    art_map = ['assets/%s/bg_%d.png' % (SLUG, i) for i in range(len(data['scenes']))]
    missing = [p for p in art_map if not (ROOT / p).exists()]
    if missing:
        sys.exit('背景が足りない: %s（scripts/make_assets_yoritomo_zo.py を実行）' % missing)
    out = ROOT / 'shorts' / SLUG / 'proto_spec.json'
    _, spec = S.to_spec(data, SLUG, art=art_map[0], pron='shorts/%s/pron.json' % SLUG,
                        out=out, credit=CREDIT, art_map=art_map)
    for sc, extra in zip(spec['scenes'], SCENES):
        sc.update(extra)
        sc['dim'] = 1.0   # 背景はすでに暗く加工済み（make_short2.py の既定 dim=0.55 だと暗すぎる）
        if not sc.get('viz'):
            # 図の無い場面は、make_short2.py が sub を y=800〜960 のパネルに描く。
            # この動画は肖像の顔がその位置に来るため、2行目は出さない
            # （2026-11-12 の試作で顔が隠れることを確認）。内容はナレーション字幕で伝わる。
            sc['sub'] = ''
    # 最上部の見出しは使わない（肖像の顔と重なる）。タイトルは y=190 に出る
    spec.update(
        hook_card=False, nolink=True, cta=False, platform='youtube',
        head=data['title'], proto=True,
        notes=spec['notes'] + '\n\n【試作】原著・一次史料の照合が未了のため、この動画は公開前の確認用です。',
    )
    dest = ROOT / 'data' / f'short_{PROTO}.json'
    dest.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
    print('作成:', dest, ' シーン', len(spec['scenes']))


if __name__ == '__main__':
    main()
