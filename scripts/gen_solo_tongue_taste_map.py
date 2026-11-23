"""単独Short（科学の誤解）：舌の味覚マップは本当に存在しないのか（solo_tongue_taste_map）。
根拠は Spence 2022 の総説（https://pmc.ncbi.nlm.nih.gov/articles/PMC8956797/）と
市民研通信第62号（2021年5月10日、https://www.shiminkagaku.org/wp/wp-content/uploads/csijnewsletter_062_202105_seno.pdf）。
2026年11月23日に原文を確認。地図は誤りだが、場所による感度の小さな差はある、と両方伝える。
nolong, nolink。背景はFreeVideoのAI映像（イメージ）、図は自作。"""
from solo_spec import build, T, fv_prompts

W = 'Spence2022／市民研通信2021'
pron = {
    '味覚マップ': 'ミカクマップ', 'ボーリング': 'ボーリング',
    '味覚': 'ミカク', '感度': 'カンド', '受容体': 'ジュヨウタイ', '専用区域': 'センヨウクイキ',
    '心理物理': 'シンリブツリ', '誇張': 'コチョウ', 'わずか': 'ワズカ', '舌先': 'シタサキ',
    '四つ': 'ヨッツ', '五つ': 'イツツ', 'ゼロ': 'ゼロ',
    '甘味': 'アマミ', '苦味': 'ニガミ', '酸味': 'スミ', '塩味': 'エンミ',
}
scenes = [
    dict(
        text='舌の先は甘味、奥は苦味。覚えた人は多い味覚マップ。答えは、この地図は誤り。甘味も苦味も、舌の広い範囲で感じます。',
        big='味覚マップは本当？', sub='答え：地図は誤り・広い範囲で感じる', src=W,
        viz=T(2.6, [('覚えている地図', '先は甘味・奥は苦味'), ('答え', '地図は誤り'), ('現在', '広い範囲で感じる')]),
        claim_ids=['c1'],
    ),
    dict(
        text='1901年、へえにっひが味の感度を測りました。感覚は舌全体に広がり、場所による差は、非常にわずかでした。',
        big='1901年の測定', sub='感覚は舌全体・差はわずか', src=W,
        viz=T(2.8, [('1901年', 'ヘーニッヒが感度を測定'), ('原論文', '感覚は舌全体に広がる'), ('差', '非常にわずか')]),
        claim_ids=['c2'],
    ),
    dict(
        text='この小さな差が、図の描き方や引用を通じて誇張されました。甘味は舌先、苦味は奥。地図が、教科書に広がったのです。',
        big='差が誇張された', sub='誇張された地図が広まった', src=W,
        viz=dict(type='compare', l_label='1901年', l_val='差はわずか', r_label='地図', r_val='先＝甘／奥＝苦'),
        claim_ids=['c3'],
    ),
    dict(
        text='ただ、差がゼロというわけではありません。場所による小さな差は報告されています。専用区域はないが、まったく同じでもない。境界線で分かれた地図ではないのです。',
        big='差はゼロではない', sub='専用区域はないが小さな差はある', src=W,
        viz=T(2.8, [('受容体', '五つの味が舌全体に'), ('感度', '場所で小さな差'), ('結論', '地図ではない')]),
        claim_ids=['c4', 'c1'],
    ),
]
bg = [
    '舌の表面を模式的にした、ピンク色の柔らかい曲面のマクロ映像。丸い小さな突起が規則的に並び、その上を薄い光がゆっくり移動する（文字なし・人物なし）',
    '古い紙の上に、手描きの曲線グラフが薄いインクで描かれているマクロ映像。なめらかな波がわずかに起伏し、紙の繊維が見える（文字なし・人物なし）',
    '四つの色に分かれた舌の模式図が、ゆっくり一つの色に溶けていくアニメーション風の映像。境界線が消え、均等な点在に変わる（文字なし・人物なし）',
    '暗い背景に、五つの小さな光点が舌の形に沿って均一に並び、それぞれがゆっくり脈動する映像。一部の光点だけがわずかに明るい（文字なし・人物なし）',
]
notes = (
    '■ 2026年11月23日に、Spence 2022 の総説（https://pmc.ncbi.nlm.nih.gov/articles/PMC8956797/）'
    'と市民研通信第62号（https://www.shiminkagaku.org/wp/wp-content/uploads/csijnewsletter_062_202105_seno.pdf）'
    'の原文を読んで作った整理です。\n'
    '・根拠：舌の味蕾が存在する広い範囲で、各基本味に対応する受容体が分布し、甘味・苦味の専用区域はない。1901年のHänigの原論文では、'
    '味の感覚は舌全体に広がり、基本味ごとの感度差は非常にわずかだった。小さな差が引用の過程で誇張され、'
    '甘味は先・苦味は奥という地図になった。現在の心理物理の研究では、場所による小さな感度差も報告されている。\n'
    '・言い過ぎを避けた点：「感度の差がない」とは言っていない。「舌の裏まで味を感じる」と言わず、'
    '「舌の広い範囲」とした。1942年のボーリングの本だけで地図が広まったという単線の説明も避けた。\n'
    '・使っていないこと：うま味の詳しい話、味蕾の数、Hänigの原グラフの数値。\n'
    '・未確認：J-Stageの大学生の味覚閾値研究は詳細未読。1912年の新聞掲載の原文も未確認。'
)
claims = [
    dict(id='c1', statement='舌のどの場所でも五つの基本味の受容体が見つかり、甘味や苦味の専用区域はない',
         source_type='primary', source_url='https://pmc.ncbi.nlm.nih.gov/articles/PMC8956797/',
         evidence_note='Spence 2022の要旨・Highlights・1節で確認。'),
    dict(id='c2', statement='1901年のヘーニッヒの原論文では、味の感覚は舌全体に広がり、基本味ごとの感度差は非常にわずかだった',
         source_type='primary', source_url='https://www.shiminkagaku.org/wp/wp-content/uploads/csijnewsletter_062_202105_seno.pdf',
         evidence_note='市民研通信第62号PDF本文47〜48行目で確認。'),
    dict(id='c3', statement='小さな感度差が引用の過程で誇張され、甘味は先・苦味は奥という地図になった',
         source_type='primary', source_url='https://pmc.ncbi.nlm.nih.gov/articles/PMC8956797/',
         evidence_note='Spence 2022の1節Fig.1と本文で確認。'),
    dict(id='c4', statement='舌の場所による味覚感度の小さな差は心理物理の研究で報告されているが、地図のような専用区域を意味しない',
         source_type='primary', source_url='https://pmc.ncbi.nlm.nih.gov/articles/PMC8956797/',
         evidence_note='Spence 2022の要旨・3節で確認。'),
]
needs_research = [
    '1912年の新聞掲載の原文は未確認。ただしSpence 2022と市民研通信で誇張の経緯は確認済みなので答えは変わらない。',
    'J-Stageの大学生の味覚閾値研究は詳細未読。ただし台本に数値は入れておらず、Spence 2022で感度差の存在は確認済みなので答えは変わらない。',
    'Hänigの原グラフの数値は未確認。図は模式図で数値を載せていないため、答えは変わらない。',
]

if __name__ == '__main__':
    build(
        'tongue_taste_map',
        '舌の味覚マップは本当に存在しないのか 論文で確かめる',
        '味覚マップは本当？',
        '地図は誤り。広い範囲で感じる',
        pron, scenes, bg, notes,
        bg_note='・動画内の図（模式図・比較）は自作です。背景の映像は FreeVideo（MiniMax H3）によるAI生成で、イメージです。実際の舌の映像ではありません。\n',
        credit='・背景映像：FreeVideo（MiniMax H3）によるAI生成映像。イメージです。実際の舌の映像ではありません\n・図・表：自作',
        end_q='皆さんは、舌のどの部分で甘味を感じていると思いますか？',
        tags=['味覚', '舌', '味覚マップ', '科学', '誤解', '論文', '雑学', 'Shorts'],
        claims=claims, needs_research=needs_research,
    )
    fv_prompts('tongue_taste_map', [
        'Extreme macro view of a soft pink biological surface with regular tiny rounded bumps, a thin soft light slowly traveling across it, shallow depth of field, calm scientific atmosphere.',
        'Macro view of an old cream paper surface with faint hand-drawn curve lines in pale ink, gentle waves with very small rises, visible paper fibers, soft even light.',
        'Abstract morphing shapes: four differently tinted soft regions on a curved pink surface slowly dissolving into one even tint, boundary lines fading out, even small dots remaining, calm minimal motion.',
        'Dark background with five clusters of tiny soft glowing dots arranged along a curved tongue-like arc, each dot pulsing slowly, a few dots slightly brighter than the others, minimal calm motion.',
    ])
