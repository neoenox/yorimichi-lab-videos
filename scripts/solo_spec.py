"""台本先行の進め方(2026-11-08〜)用の共通部品。gen_solo_<slug>.py から build() を呼ぶと、
  ① data/short_solo_<slug>.json と data/<slug>_pron.json(動画づくり用)
  ② E:/rekishikaisetu/out/script_solo_<slug>.txt (台本レビュー用のテキスト。ChatGPTに渡す)
を書く。動画の背景生成・ビルドは、台本がChatGPTのレビューを通ってから始める。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
IDS = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))
BG_NOTE = '・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の風景・史実の再現ではありません。\n'
CREDIT = '・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の風景・史実の再現ではありません\n・図・表：自作'
T = lambda gap, ev: dict(type='timeline', gap=gap, events=ev)


def build(slug, title, head, answer, pron, scenes, bg_plan, notes, bg_note=None, credit=None, end_vid=None, hook_text=None, hook_label=None, end_q=None):
    (R / 'data' / f'{slug}_pron.json').write_text(json.dumps(pron, ensure_ascii=False), encoding='utf8')
    V = lambda n: f'assets/{slug}/fv/clip{n}.mp4'
    sc = []
    for i, s in enumerate(scenes):
        d = dict(s, vid=V(i + 1), dim=0.7)
        d['big'] = d['big'].replace('、', ''); d['sub'] = d['sub'].replace('、', '')
        if i: d['col'] = 'white'
        sc.append(d)
    sc.append(dict(text='', end=True, vid=(end_vid or V(1)), dim=0.7))
    o = dict(title=title, head=head, pron=f'data/{slug}_pron.json', art='assets/tohoku/bg_one.png', hook=scenes[0]['text'], notes=notes + (bg_note or BG_NOTE), answer=answer, hook_text=hook_text, hook_label=hook_label, end_q=end_q,
             credit=(credit or CREDIT), suffix='整理', nolong=True, nolink=True, long_id=IDS['43_bukka']['video_id'], long_title='43_bukka', scenes=sc)
    (R / 'data' / f'short_solo_{slug}.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')
    L = [f'タイトル案: {title} 約60秒で整理 #Shorts', f'冒頭の結論カード: {answer}', '', '【場面ごとの台本(ナレーション)・画面の文字・図・背景の予定】']
    for i, s in enumerate(scenes):
        v = s['viz']
        vz = ' / '.join(f'{a}={b}' for a, b in v['events']) if v['type'] == 'timeline' else json.dumps(v, ensure_ascii=False)
        L += [f'場面{i + 1}', f"  ナレーション: {s['text']}", f"  大見出し: {s['big']} / 小見出し: {s['sub']} / 出典表示: {s['src']}", f'  図: {vz}', f'  背景(AI生成映像)の予定: {bg_plan[i]}']
    L += ['', '【終わりの画面のナレーション】' + (end_q or '') + '出典は、説明欄にまとめています。チャンネル登録も、お願いします。', '', '【説明欄(根拠と未確認)】', notes + (bg_note or BG_NOTE)]
    out = Path('E:/rekishikaisetu/out') / f'script_solo_{slug}.txt'
    out.write_text('\n'.join(L), encoding='utf8')
    print('ok', slug, len('\n'.join(L)), '字')


def fv_prompts(slug, prompts):
    """背景クリップの指示文(英語)を assets/<slug>/fv/prompts.json に書く。文字・人物・建物・現代物は入れない。"""
    T_ = ' Cinematic realistic look, no people, no hands, no text, no letters, no characters, no labels, no markings, no logos, no buildings, no modern objects.'
    d = R / 'assets' / slug / 'fv'; d.mkdir(parents=True, exist_ok=True)
    (d / 'prompts.json').write_text(json.dumps([dict(name=f'clip{i + 1}', sec=7, text=t + T_) for i, t in enumerate(prompts)], ensure_ascii=False, indent=1), encoding='utf8')
