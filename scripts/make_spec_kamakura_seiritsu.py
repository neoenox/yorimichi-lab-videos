"""鎌倉幕府の成立年 Short の試作 spec を作る（shorts/kamakura_seiritsu/result.json → data/short_proto_kamakura_seiritsu.json）。

標準 JSON は status=needs_review（出典の原文照合が未了）なので、`shorts_standard.py to-spec` は拒否する。
このスクリプトは**試作用**に to_spec() を直接呼び、別名 proto_ で出力する（ready の動画ではない）。
背景は既定では自作の暗色グラデーション（assets/ の png は git 管理外なので、このスクリプトで再生成できる）。
--fv を付けると、FreeVideo の AI 生成クリップ（assets/kamakura_seiritsu/fv/clip1..7.mp4）を背景にした別名 proto_fv_ を出力する。
既存の単独 Shorts と同じ方式（場面の vid、dim=0.7、クレジットに『AI生成・イメージ』を明記）。クリップは scripts/gen_fv_prompts_kamakura_seiritsu.py → solo_ship.py clips で作る。

  python scripts/make_spec_kamakura_seiritsu.py            # 単色背景版 → data/short_proto_kamakura_seiritsu.json
  python scripts/make_spec_kamakura_seiritsu.py --fv       # FreeVideo 背景版 → data/short_proto_fv_kamakura_seiritsu.json
  python scripts/make_short2.py proto_fv_kamakura_seiritsu   # VOICEVOX 起動が必要（--kana で読みだけ確認）
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import shorts_standard as S  # noqa: E402

SLUG = 'kamakura_seiritsu'
FV = '--fv' in sys.argv
PROTO = ('proto_fv_' if FV else 'proto_') + SLUG
W, H = 1080, 1920

# 場面ごとの背景の色味（暗い紺を基調に、場面の話題で少し変える）
TINTS = [(18, 30, 52), (16, 34, 50), (30, 32, 52), (44, 30, 44), (22, 38, 44), (26, 36, 40), (30, 30, 56)]

# 場面ごとの画面要素（データだけ書く）。viz は make_short2.py の draw_viz の型
SCENES = [
    dict(src='模式図', viz=dict(type='count', label='鎌倉幕府の成立', value=1192, fmt='{:.0f}', unit='年？', note='いい国つくろう、で覚えた年')),
    dict(src='模式図（諸説の例）', viz=dict(type='timeline', gap=0.9, events=[
        ['1180年', '東国独立国家の成立'], ['1183年', '東国の支配権を公認'], ['1185年', '守護・地頭の設置を許可'],
        ['1190年', '諸国の守護権を付与'], ['1192年', '征夷大将軍に就任']])),
    dict(src='模式図', viz=dict(type='timeline', gap=1.6, events=[['1185年', '守護・地頭の任命権'], ['得た人', '源頼朝']])),
    dict(src='模式図', viz=dict(type='timeline', gap=1.6, events=[['1192年', '征夷大将軍に任命'], ['任じた側', '朝廷']])),
    dict(src='模式図（東京書籍・中学歴史の年表）', viz=dict(type='compare', l_label='〜2011年度版', l_val='1192年から', r_label='2012年度版〜', r_val='1185年から')),
    dict(src='模式図（東京書籍・中学歴史）', viz=dict(type='timeline', gap=1.8, events=[['本文', '1192年の将軍任命も記載'], ['欄外', '成立時期には諸説がある']])),
    dict(src='模式図', viz=dict(type='compare', l_label='1185年', l_val='実質', r_label='1192年', r_val='名実とも')),
]

CREDIT_FV = ('・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の風景・史実の再現ではありません\n'
             '・図・表：自作の模式図（実在の資料の複製ではありません）\n'
             '・出典：国立国会図書館レファレンス協同データベース（登録番号 1000197449・1000344905）、朝日新聞 asahi.com（2008-02-28）、Wikipedia「鎌倉幕府」\n'
             '・【試作】出典の原文照合は未了です（吾妻鏡・山槐記・教科書の実物など）')
CREDIT = ('・図・表：自作の模式図（実在の資料の複製ではありません）\n'
          '・背景：自作の単色グラデーション（画像素材は使用していません）\n'
          '・出典：国立国会図書館レファレンス協同データベース（登録番号 1000197449・1000344905）、朝日新聞 asahi.com（2008-02-28）、Wikipedia「鎌倉幕府」\n'
          '・【試作】出典の原文照合は未了です（吾妻鏡・山槐記・教科書の実物など）')


def make_bg(i, tint):
    im = Image.new('RGB', (W, H))
    px = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H
        c = tuple(int(v * (1.25 - 0.55 * k)) for v in tint)
        px.line([(0, y), (W, y)], fill=c)
    d = ImageDraw.Draw(im, 'RGBA')
    for x in range(-H, W, 90):   # ごく淡い斜線で単調さを減らす
        d.line([(x, H), (x + H // 2, 0)], fill=(255, 255, 255, 7), width=2)
    out = ROOT / 'assets' / SLUG
    out.mkdir(parents=True, exist_ok=True)
    p = out / f'bg_{i}.png'
    im.save(p)
    return f'assets/{SLUG}/bg_{i}.png'


def main():
    res = ROOT / 'shorts' / SLUG / 'result.json'
    data = json.loads(res.read_text(encoding='utf-8'))
    ok, issues = S.check(str(res))
    errs = [m for lv, m in issues if lv == 'ERROR']
    if errs:
        sys.exit('標準の検査に ERROR: %s' % errs)
    art_map = [make_bg(i, TINTS[i]) for i in range(len(data['scenes']))]   # FV 版でも、クリップが無い場面の予備として作る
    if FV:
        miss = [i + 1 for i in range(len(data['scenes'])) if not (ROOT / 'assets' / SLUG / 'fv' / f'clip{i + 1}.mp4').exists()]
        if miss:
            sys.exit('FreeVideo のクリップが足りない: clip%s（scripts/solo_ship.py clips %s で生成）' % (miss, SLUG))
    out = ROOT / 'shorts' / SLUG / 'proto_spec.json'
    _, spec = S.to_spec(data, SLUG, art=art_map[0], pron='shorts/%s/pron.json' % SLUG, out=out, credit=CREDIT_FV if FV else CREDIT, art_map=art_map)
    for i, (sc, extra) in enumerate(zip(spec['scenes'], SCENES)):
        sc.update(extra)
        if FV:   # 既存の単独 Shorts と同じ：場面ごとの動画背景。図が読めるよう暗めにする(dim=0.7)
            sc['vid'] = f'assets/{SLUG}/fv/clip{i + 1}.mp4'
            sc['dim'] = 0.7
        else:
            sc['dim'] = 0.95
    # nolong は付けない（付けると make_short2.py が最後の場面のナレーションを登録誘導に差し替える）。概要欄の本編リンクは nolink で消す
    spec.update(
        hook_card=False, nolink=True, cta=False, platform='youtube', head='鎌倉幕府は1192年？',
        proto=True,
        notes=spec['notes'] + '\n\n【試作】出典の原文照合が未了のため、この動画は公開前の確認用です。' + ('\n背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の風景・史実の再現ではありません。' if FV else ''))
    # 最後の場面（end）は付けない（登録誘導なし。標準：無意味な登録誘導は禁止）
    dest = ROOT / 'data' / f'short_{PROTO}.json'
    dest.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
    print('作成:', dest, ' シーン', len(spec['scenes']))


if __name__ == '__main__':
    main()
