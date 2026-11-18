"""単独Short(ニュース)：動物と藻類の細胞を融合(solo_planimal)。根拠はJSTの共同発表「動植物ハイブリッド細胞『プラニマル細胞』の作製に成功」(2026年11月12日発表、2026年11月16日に原文とPDFを確認 https://www.jst.go.jp/pr/announce/20261112-4/index.html)。論文は Nature Communications(2026年11月12日)。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
from solo_spec import build, T, fv_prompts
W = 'JST共同発表(2026年11月12日)'
pron = {'シゾンという藻': 'シゾントイウモ', '藻類': 'ソウルイ', '染色体': 'センショクタイ', '培養細胞': 'バイヨウサイボウ', '東京大学': 'トウキョウダイガク', '世代': 'セダイ', '光合成': 'コウゴウセイ', '組み込': 'クミコ',
        '動物': 'ドウブツ', 'シゾン': 'シゾン', '沈黙': 'チンモク', '融合': 'ユウゴウ'}
scenes = [
    dict(text='藻類と、動物の細胞を、融合させたら、どうなる？ 答えは、藻類のDNAを持つ細胞が、できました。2026年11月12日、東京大学などが発表しました。',
         big='藻類と動物の細胞を融合', sub='東京大学などが2026年11月12日に発表', src=W,
         viz=T(2.6, [('発表', '東京大学などの研究グループ'), ('発表日', '2026年11月12日'), ('論文', 'Nature Communications')])),
    dict(text='シゾンという藻の全DNAが、動物の細胞の染色体に、組み込まれました。名前は、プラニマル細胞です。',
         big='名前は、プラニマル細胞', sub='藻類(シゾン)の全DNAが染色体の一部に', src=W,
         viz=T(2.8, [('材料', '藻類(シゾン)＋動物の培養細胞'), ('結果', '藻類のDNAが染色体に組み込まれた'), ('名前', 'プラニマル細胞')])),
    dict(text='この細胞は、150世代以上、分裂しました。ただ、藻類の遺伝子の95パーセント以上は、ほとんど働いていません。',
         big='分裂は続くが、遺伝子は眠る', sub='藻類の遺伝子の95％以上は発現せず', src=W,
         viz=dict(type='compare', l_label='分裂', l_val='150世代以上', r_label='働かない藻類遺伝子', r_val='95％以上')),
    dict(text='光合成する動物の細胞は、まだ先です。今回は、その土台です。2026年11月12日時点の情報です。',
         big='光合成する細胞は、まだ先', sub='今回は土台となる成果', src=W,
         viz=T(2.8, [('期待', '光合成などの機能を動物細胞に'), ('今回', '藻類のDNAを維持できた段階'), ('注意', '光合成する細胞ではない')])),
]
bg = ['丸い動物の細胞に、緑色の藻類の細胞が近づいて溶け合う、顕微鏡のような模式的な映像(人物なし・文字なし)', '細胞の中で、緑色に光る糸状の染色体が、ほかの染色体と並んでゆっくり揺れる模式的な映像(人物なし・文字なし)',
      '分裂をくり返して、次々と数がふえていく丸い細胞の模式的な映像(人物なし・文字なし)', '明るい光の中で、丸い細胞が静かに漂う未来的な模式的な映像(人物なし・文字なし)']
notes = ('■ 2026年11月16日に、JSTの共同発表「動植物ハイブリッド細胞『プラニマル細胞』の作製に成功」(2026年11月12日発表。https://www.jst.go.jp/pr/announce/20261112-4/index.html )の原文とPDF資料を読んで作った整理です。2026年11月16日時点の情報です。\n'
         '・発表者：東京大学、東京科学大学、近畿大学、神奈川大学、静岡大学、東京理科大学の共同研究グループ。論文は Nature Communications オンライン版(2026年11月12日現地時間)、DOI 10.1038/s41467-026-78753-w。\n'
         '・主な内容(同)：藻類(シゾン)と動物培養細胞を融合させ、藻類の全DNAが動物染色体に組み込まれた「プラニマル細胞」を作製。細胞融合の48時間後にシゾン染色体が動物染色体と同じ細胞内に共存する様子を観察。150世代以上(通常の培養細胞と同じ寿命)にわたって正常に分裂し、組み込まれた藻類DNAも安定して維持された。一方、シゾン由来遺伝子の95％以上は発現せず「沈黙」していた(PDF資料で確認)。進化的に遠い藻類と動物の全DNAを同一細胞内で維持する動植物ハイブリッド細胞の作製は世界初の報告、とされている。\n'
         '・言い過ぎを避けた点：光合成をする動物細胞ができた、とは言っていない。光合成機能などの導入は「今後の期待」の段階。「動物と植物が合体した生き物」ではなく、培養細胞での成果。Geminiのレビューで「沈黙」を「ほとんど働いていませんでした」に、「シゾンという藻」と言い換え(「ワカメやミドリムシ」の例示は未確認なので不採用、冒頭と末尾の日付は年月日ルールで残した)。ChatGPTのレビュー(2026年11月16日)で、「DNAをまるごと入れた」→細胞融合、「一緒に生き続けた」→藻類のDNAを持つ細胞ができた、と直し、「95％以上が沈黙」を加えた(PDFで確認)。\n'
         '・動画では使っていないこと：エピジェネティックな仕組み(論文題名のgatekeeping)、研究者名、応用(細胞培養コスト・CO2削減)。\n'
         '・未確認：Nature Communications掲載論文そのもの(原文は共同発表とPDF資料のみ確認)。\n')
if __name__ == '__main__':
    build('planimal', '【2026年11月12日発表】動物と藻類の細胞を融合？ プラニマル細胞', '藻類と動物の細胞を融合したら？', '藻類のDNAを持つ細胞ができた', pron, scenes, bg, notes,
          bg_note='・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の細胞の映像ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の細胞の映像ではありません\n・図・表：自作', end_q='皆さんは、光合成する動物がいたら、見てみたいですか？',
          tags=['プラニマル細胞', '藻類', '動物細胞', '東京大学', 'JST', 'Nature Communications', '科学ニュース', '合成生物学', '雑学', 'Shorts'])
    fv_prompts('planimal', [
        'A round translucent animal cell and a green algae cell drifting together and merging, abstract microscope-like schematic look, the camera slowly pushing in.',
        'Glowing green thread-like chromosomes lined up among other chromosomes inside a cell nucleus, abstract schematic, the camera slowly pushing in.',
        'Round cells dividing again and again and multiplying in soft light, abstract schematic, the camera slowly gliding sideways.',
        'Round cells floating calmly in bright futuristic light with soft glow, abstract schematic, the camera slowly pushing in.'])
