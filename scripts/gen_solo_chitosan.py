"""単独Short(科学ニュース)：カニやエビの殻で、水素をつくれる？(solo_chitosan)。根拠は北海道大学・JST 共同発表(2026年11月16日、2026年11月16日に原文とPDFを確認 https://www.jst.go.jp/pr/announce/20261116-2/index.html )。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
from solo_spec import build, T, fv_prompts
W = '北海道大学・JST共同発表(2026年11月16日)'
pron = {'キトサン': 'キトサン', '光触媒': 'ヒカリショクバイ', '色素': 'シキソ', '水素': 'スイソ',
        '北海道大学': 'ホッカイドウダイガク', '殻': 'カラ', '集める': 'アツメル'}
scenes = [
    dict(text='カニやエビの殻から、水素をつくる技術？ 実は、殻から作るキトサンで、光触媒の性能を約10倍にできました。2026年11月16日の発表です。',
         big='カニの殻で、水素？', sub='北海道大学とJSTが2026年11月16日に発表', src=W,
         viz=T(2.6, [('発表', '北海道大学・JST'), ('発表日', '2026年11月16日'), ('材料', 'カニ・エビの殻のキトサン')])),
    dict(text='光触媒は、光で水から水素を出します。色素を多く集めると、反応に使われにくくなる。そこで、キトサンの上で、適度に集めました。',
         big='色素を、適度に集める', sub='集積を避けずに、生かす設計', src=W,
         viz=T(2.8, [('光触媒', '光で水から水素'), ('ふつう', '色素を集めると失う'), ('工夫', '適度に集める')])),
    dict(text='水素のでき方が、約10倍。色素を最も少なくした材料とくらべてです。',
         big='水素のでき方、約10倍', sub='色素が少ない材料との比較', src=W,
         viz=dict(type='compare', l_label='色素が少ない材料', l_val='3.8 mmol', r_label='最適な材料', r_val='39.2 mmol')),
    dict(text='光を水素に変える割合は、0.4％。まだ実験室の段階です。2026年11月16日時点の情報です。',
         big='効率0.4％、まだ実験室', sub='実用には、効率と耐久性が課題', src=W,
         viz=T(2.8, [('見かけの量子収率', '0.4％'), ('連続24時間', '頭打ちになる'), ('段階', '実験室レベル')])),
]
bg = ['まな板の上に置かれた、カニとエビの殻(人物なし・手なし・文字なし)',
      '白い浅い皿に盛られた、白っぽい粉(キトサン。人物なし・手なし・文字なし)',
      'ガラス容器の水中に光が差し込み、細かい泡が立ち上る映像(人物なし・文字なし)',
      '実験台に並んだガラスの器具に、青白い光が当たる映像(人物なし・文字なし)']
notes = ('■ 2026年11月16日に、北海道大学・JST 共同発表(https://www.jst.go.jp/pr/announce/20261116-2/index.html )の本文とPDF(https://www.jst.go.jp/pr/announce/20261116-2/pdf/20261116-2.pdf )を読んで作った整理です。2026年11月16日時点の情報です。\n'
         '・発表者/論文：北海道大学大学院環境科学院 博士後期課程2年 クシャル・モハン・ゴウダ氏、北海道大学電子科学研究所 高野勇太准教授ら。Journal of Materials Chemistry A に2026年11月11日(水)オンライン掲載。DOI 10.1039/d6ta07314j。\n'
         '・主な内容(同)：キトサン(カニ・エビの殻などのキチンを原料とする生物由来の高分子)に、白金ポルフィリン色素を化学結合させ、色素の固定量(キトサンの単糖ユニット当たり0.05〜0.85当量)を変えた材料を作製。従来は色素の集積を抑える設計が主流だったが、本研究は「適度に集積」させ、励起状態の寿命を延ばして、酸素へエネルギーを渡す反応を抑え、電子を移す反応を増やした。\n'
         '・数字(同)：最も活性が高い0.50当量の材料は、アスコルビン酸を電子供与体として加えた空気雰囲気下の水中で405nmの光を照射すると、色素1g当たり毎時39.2mmolの水素を生成。色素の固定量が最も少ない0.05当量(毎時3.8mmol)の約10倍。酸素濃度を低減すると毎時72.7mmol。見かけの量子収率は0.4％。0.85当量では毎時25.9mmolに低下(密着しすぎると失われる)。\n'
         '・言い過ぎを避けた点：「約10倍」は、色素の固定量が最も少ない材料(0.05当量、毎時3.8mmol)との比較であることを画面にも出した(素材全体の効率が10倍になった、ではない)。「光を水素に変える割合0.4％」は「見かけの量子収率」の言い換えで、画面のカードに正式名を出した。「まだ実験室の段階」は、発表の「実用化には効率的な光利用が必要」「耐久性の向上が今後の課題」に基づく。\n'
         '・条件の注意：水素生成は、アスコルビン酸を電子供与体として加えた水中で405nmの光を当てた実験の結果で、水そのものを分解した試験ではない。毎時72.7mmolは酸素濃度を低減した別条件の値で、約10倍の比較(39.2対3.8)とは混ぜていない。\n'
         '・論文の状態：Journal of Materials Chemistry A に2026年11月11日(水)にオンライン掲載済み(未発表ではない)。本文そのものは未確認。\n'
         '・動画では使っていないこと：励起状態の寿命777→1,209ナノ秒、白金ポルフィリンの詳細、一重項酸素、さきがけ・科研費などの支援、0.85当量・0.25当量などの細かい条件、72.7mmol(別条件)、図表。\n'
         '・未確認：論文本文(Journal of Materials Chemistry A)そのもの、図1〜4の図版。\n'
         '・背景の映像はAI生成で、実際の実験の映像ではない(イメージです)。\n')
if __name__ == '__main__':
    build('chitosan', '【2026年11月16日発表】カニやエビの殻で、水素をつくれる？ 光触媒の性能を約10倍に', '2026年11月16日発表', '殻のキトサンで、水素生成が約10倍', pron, scenes, bg, notes,
          bg_note='・動画内の図(比較・年表)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の実験・カニやエビの殻の映像ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の実験の映像ではありません\n・図・表：自作',
          end_q='カニやエビの殻、捨てるのは、もったいないと思いますか？',
          tags=['キトサン', '光触媒', '水素', '北海道大学', 'JST', 'カニ', 'エビ', '科学', '雑学', 'Shorts'])
    fv_prompts('chitosan', [
        'Fresh crab shells and shrimp shells arranged on a plain wooden board, soft natural light, detailed texture of the shells, no people, no hands, no text, the camera slowly gliding sideways.',
        'A shallow white ceramic dish holding fine pale off-white powder, soft daylight from the side, clean simple background, no people, no hands, no text, the camera slowly pushing in.',
        'A clear glass vessel filled with water, a beam of light passing through the water, tiny bubbles rising and gathering on the surface, dark background, no people, no text, the camera slowly tilting down.',
        'Glass laboratory vessels on a clean bench lit by a soft blue-white beam of light, shallow depth of field, no people, no hands, no text, the camera slowly pushing in.'],
        allow_buildings=True)
