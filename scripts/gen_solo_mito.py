"""単独Short：水戸黄門は、全国を旅した？(solo_mito)。nolong, nolink。
【新しい進め方(2026-11-08〜)】まずこの台本だけをweb版ChatGPTにレビューしてもらい、通ってから背景クリップ生成・ビルドに入る。
  python scripts/gen_solo_mito.py            # data/short_solo_mito.json と、レビュー依頼用の台本テキスト out/script_solo_mito.txt を書く
根拠は日本語版Wikipedia「徳川光圀」(2026年11月8日に原文を確認)。『大日本史』などの原本は読めていない。
背景はFreeVideo(各場面の中身に合わせる。BG_PLAN参照)、図は自作。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
IDS = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))
slug = 'mito'
V = lambda n: f'assets/{slug}/fv/clip{n}.mp4'
T = lambda gap, ev: dict(type='timeline', gap=gap, events=ev)
W = 'Wikipedia（徳川光圀）'
pron = {'水戸黄門': 'ミトコウモン', '光圀': 'ミツクニ', '徳川光圀': 'トクガワミツクニ', '大日本史': 'ダイニホンシ', '勿来': 'ナコソ', '緞帳': 'ドンチョウ', '金沢八景': 'カナザワハッケイ',
        '房総': 'ボウソウ', '漫遊': 'マンユウ', '漫遊譚': 'マンユウタン', '行脚': 'アンギャ', '巡視': 'ジュンシ', '講談': 'コウダン', '歌舞伎': 'カブキ', '頭巾': 'ズキン',
        '白髭': 'シラヒゲ', '編纂': 'ヘンサン', '水戸藩': 'ミトハン', '熱海': 'アタミ', '鎌倉': 'カマクラ', '日光': 'ニッコウ', '資料': 'シリョウ', '黄門': 'コウモン'}
(R / 'data' / f'{slug}_pron.json').write_text(json.dumps(pron, ensure_ascii=False), encoding='utf8')
BG_PLAN = [
    '旅の笠と杖が、風の吹く街道の木に立てかけられている(人物なし・文字なし)',
    '杉並木の続く古い土の街道を、カメラが前に進む(建物なし・舗装なし)。場面2の位置関係は、図(関東の中／すぐ外／遠く)で示す',
    '無地の和紙の束と、筆と硯のそばで、ろうそくが揺れる(文字なし)',
    '暗い舞台に、文字のない赤い緞帳(どんちょう)がゆっくり揺れて、スポットライトが差す(人物なし・文字なし)',
]
scenes = [
    dict(text='水戸黄門といえば、全国を旅する御老公。でも、本物の光圀が訪れたと記録にあるのは、ほとんどが、関東です。', big='水戸黄門は全国を旅した？', sub='本物の光圀の話', src=W,
         viz=T(2.6, [('有名な話', '白髭と頭巾で、全国を旅する'), ('本物の光圀', '訪れた記録は、ほとんど関東'), ('問い', '全国漫遊は本当？')])),
    dict(text='記録に残る、実際の光圀の旅先は、日光、鎌倉、金沢八景、房総など。ほとんど関東の中です。記録の上で関東の外にあるのは、すぐ隣の、勿来と熱海だけです。', big='記録にある旅先', sub='日光・鎌倉・金沢八景・房総など', src=W,
         viz=T(2.8, [('関東の中', '日光・鎌倉・金沢八景（神奈川）ほか'), ('関東のすぐ外', '勿来（福島）と熱海（静岡）だけ'), ('それより遠く', '訪れた記録は残っていない')])),
    dict(text='旅のイメージの元は、いくつか考えられています。大日本史の資料集めに、家臣を各地へ送ったこと。隠居後に、水戸藩の領内を巡視した話です。', big='旅のイメージの元', sub='家臣の派遣と領内の巡視', src=W,
         viz=T(2.8, [('大日本史', '資料集めに家臣を諸国へ派遣'), ('隠居後', '水戸藩の領内を巡視した話'), ('考えられている', '漫遊のイメージの元')])),
    dict(text='白髭と頭巾で諸国を歩き、民百姓の味方をする話は、江戸時代の後期から、フィクションとして作られました。講談や歌舞伎で、人気を集めました。', big='漫遊譚はフィクション', sub='江戸後期から近代にかけて', src=W,
         viz=T(2.6, [('江戸時代後期から', '黄門漫遊譚が形づくられる'), ('広まった場', '講談・歌舞伎'), ('昭和には', '映画やテレビドラマにも')])),
]
sc = []
for i, s in enumerate(scenes):
    d = dict(s, vid=V(i + 1), dim=0.7)
    d['big'] = d['big'].replace('、', ''); d['sub'] = d['sub'].replace('、', '')
    if i: d['col'] = 'white'
    sc.append(d)
sc.append(dict(text='', end=True, vid=V(1), dim=0.7))
notes = ('■ 日本語版Wikipedia「徳川光圀」(2026年11月8日に原文を確認)にもとづく整理です。『大日本史』などの原本は読めていません。\n'
         '・黄門漫遊譚：「特に江戸時代後期から近代にかけて、白髭と頭巾姿で諸国を行脚してお上の横暴から民百姓の味方をする、フィクションとしての黄門漫遊譚が形成された。水戸黄門は講談や歌舞伎の題材として大衆的人気を獲得し、昭和時代には映画やテレビドラマなどの題材とされた」(同)。\n'
         '・実際：「『大日本史』の編纂に必要な資料収集のために家臣を諸国に派遣したことや、隠居後に水戸藩領内を巡視した話などから諸国漫遊がイメージされたと考えられるが、実際の光圀は日光、鎌倉、金沢八景、房総などしか訪れたことがなく、関東に隣接する勿来と熱海を除くと、現在の関東地方の範囲から出た記録はない」(同)。\n'
         '・「水戸黄門」の「黄門」は、官職である中納言・権中納言の唐名(同)。\n'
         '・未確認：『大日本史』『新編鎌倉志』などの原本。\n'
         '・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の風景・史実の再現ではありません。\n')
o = dict(title='水戸黄門は、本当に全国を旅した？', head='水戸黄門は全国を旅した？', pron=f'data/{slug}_pron.json', art='assets/tohoku/bg_one.png',
         hook=scenes[0]['text'], notes=notes, answer='本物の光圀が訪れた記録は、ほぼ関東だけ',
         credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の風景・史実の再現ではありません\n・図・表：自作',
         suffix='整理', nolong=True, nolink=True, long_id=IDS['43_bukka']['video_id'], long_title='43_bukka', scenes=sc)
(R / 'data' / f'short_solo_{slug}.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')

# --- 台本レビュー依頼用のテキスト(動画を作る前に、ChatGPTへ渡す) ---
L = [f"タイトル案: {o['title']} 約60秒で整理 #Shorts", f"冒頭の結論カード: {o['answer']}", '', '【場面ごとの台本(ナレーション)・画面の文字・図・背景の予定】']
for i, s in enumerate(scenes):
    v = s['viz']
    vz = ' / '.join(f'{a}={b}' for a, b in v['events']) if v['type'] == 'timeline' else json.dumps(v, ensure_ascii=False)
    L += [f'場面{i + 1}', f"  ナレーション: {s['text']}", f"  大見出し: {s['big']} / 小見出し: {s['sub']} / 出典表示: {s['src']}", f'  図: {vz}', f'  背景(AI生成映像)の予定: {BG_PLAN[i]}']
L += ['', '【終わりの画面のナレーション】出典は、説明欄にまとめています。チャンネル登録も、お願いします。', '', '【説明欄(根拠と未確認)】', notes]
out = Path('E:/rekishikaisetu/out') / f'script_solo_{slug}.txt'
out.write_text('\n'.join(L), encoding='utf8')
print('ok', len('\n'.join(L)), '字 ->', out)
