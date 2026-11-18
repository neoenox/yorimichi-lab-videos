"""単独Short(科学ニュース)：捨てる熱で発電(ZnSb)(solo_netsuden)。根拠はNIMS・JST共同発表(2026年11月16日、同日に原文を確認 https://www.jst.go.jp/pr/announce/20261116-3/index.html )。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。
Ask Studio(2026-11-17)の実測「離脱は4〜7秒」を受け、4〜6秒目に数字(8%)を置く構成。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solo_spec import build, T, fv_prompts
W = 'NIMS・JST共同発表(2026年11月16日)'
pron = {'アンチモン化亜鉛': 'アンチモンカアエン', '亜鉛': 'アエン', '熱電': 'ネツデン',
        '変換効率': 'ヘンカンコオリツ', 'ケルビン': 'ケルビン', '排熱': 'ハイネツ',
        'ゲルマニウム': 'ゲルマニウム', '耐久性': 'タイキュウセイ'}
scenes = [
    dict(text='工場や車が、捨てている熱。それで電気は、つくれる？ 答えは、つくれます。温度差400ケルビンで、変換効率は最大8％。',
         big='捨てる熱で、発電', sub='温度差400Kで、変換効率8％', src=W,
         viz=T(2.6, [('変換効率', '最大8％'), ('温度差', '400K'), ('使い道', '工場・車の排熱')])),
    dict(text='材料は、アンチモン化亜鉛。安い元素だけで、できています。原料のコストは、1キロ、約38ドル。',
         big='1キロ、約38ドル', sub='安い元素だけで作れる', src=W,
         viz=T(2.8, [('材料', 'ZnSb'), ('原料コスト', '37.9ドル/kg'), ('元素', '安い元素で')])),
    dict(text='高性能な材料と比べると、コストは40分の1。値段あたりの性能では、負けません。',
         big='コストは、40分の1', sub='値段あたりの性能で見る', src=W,
         viz=T(2.8, [('GeTe比', 'コスト約1/40'), ('MgAgSb比', 'コスト約1/14'), ('コスト当たり効率', '1.7倍')])),
    dict(text='ただし、まだ研究の段階。実用化には、耐久性や、大量に作る方法の確認が要ります。2026年11月16日時点の情報です。',
         big='まだ、研究の段階', sub='耐久性・量産が課題', src=W,
         viz=T(2.8, [('段階', '研究レベル'), ('課題', '耐久性・量産'), ('時点', '2026年11月16日')])),
]
bg = ['夜の工場の屋根から、湯気と熱が立ち上る映像(人物なし・文字なし)',
      '金属の板と、銀色のインゴットが並ぶ映像(人物なし・手なし・文字なし)',
      '発電モジュールらしい、金属の板と配線のクローズアップ(人物なし・手なし・文字なし)',
      '実験室の測定装置と、金属の試料(人物なし・文字なし)']
notes = ('■ 2026年11月16日に、NIMS・JST共同発表(https://www.jst.go.jp/pr/announce/20261116-3/index.html )の本文を読んで作った整理です。2026年11月16日時点の情報です。\n'
         '・発表者/論文：物質・材料研究機構(NIMS)ナノアーキテクトニクス材料研究センター 熱エネルギー変換材料グループ 森孝雄副センター長ら。Nature Sustainability に2026年11月16日(ロンドン時間)オンライン掲載。DOI 10.1038/s41893-026-01986-6。\n'
         '・主な内容(同)：熱を電気に変える熱電材料を「低い材料コストでどれだけ高い発電性能を得られるか」で評価。比較的安価な元素から成るp型ZnSb(アンチモン化亜鉛)に着目。原料コストは約37.9米ドル/kgで、最大のzTを示すGeTeの約40分の1、MgAgSbの約14分の1。ZnSbと電極を低抵抗でつなぐSb界面層を開発し、p型ZnSbとn型材料を組み合わせた発電モジュールを作製。温度差400Kで最大約8％の変換効率を実測。原料コスト当たりの変換効率は代表的な熱電デバイスの中で高く、Mg3Sb1.5Bi0.5系デバイスの約1.7倍。\n'
         '・言い過ぎを避けた点：「最高性能の材料ではない」ことを前提に、「値段あたりの性能」で見る話として構成した。8％は温度差400Kでの最大値で、どの温度差でも8％ではない。材料名(ZnSb)はナレーションでは言わず、画面のカードに置いた(専門語を耳で追わせない)。\n'
         '・動画では使っていないこと：zTの具体的な数値、p型/n型の詳細、界面層の作製法、Mg3Sb1.5Bi0.5の組成、論文の図表。\n'
         '・未確認：論文本文、図表。\n'
         '・背景の映像はAI生成で、実際の研究設備の映像ではない(イメージです)。\n')
if __name__ == '__main__':
    build('netsuden', '捨てている熱で、電気はつくれる？ 変換効率8％の材料', '捨てる熱で発電', '温度差400Kで、変換効率は最大8％', pron, scenes, bg, notes,
          bg_note='・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の研究設備の映像ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の研究設備の映像ではありません\n・図・表：自作',
          end_q='皆さんの家や職場で、捨てている熱はありますか？',
          tags=['熱電発電', '廃熱', 'ZnSb', 'NIMS', 'JST', '省エネ', '科学', '雑学', 'Shorts'])
    fv_prompts('netsuden', [
        'Steam and heat shimmer rising from the roof of a large factory at night, warm orange light from vents against a dark blue sky, no people, no text, the camera slowly tilting up.',
        'Plain metal plates and a stack of silver-grey metal ingots on a workbench, cool industrial lighting, no people, no hands, no text, the camera slowly gliding sideways.',
        'Close view of a metal plate module with rows of small elements and thin wires, heat haze above it, shallow depth of field, no people, no hands, no text, the camera slowly pushing in.',
        'A plain smooth metal cylinder and a metal ring on a clean matte grey surface, soft studio light, featureless polished surfaces filling the frame, no people, no hands, no text, the camera slowly gliding forward.'],
        allow_modern=True)
