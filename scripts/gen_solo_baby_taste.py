"""単独Short（科学の誤解）：赤ちゃんは味を感じないのか（solo_baby_taste）。
根拠は Beauchamp & Mennella の総説（https://pmc.ncbi.nlm.nih.gov/articles/PMC3202923/）
と乳児の顔表情と食品受容の研究（https://pmc.ncbi.nlm.nih.gov/articles/PMC5492973/）。
2026年11月23日にPMC本文を確認。『感じるが、好みは経験で形作られる』の両保存。
nolong, nolink。背景はFreeVideoのAI映像（イメージ）、図は自作。"""
from solo_spec import build, T, fv_prompts

W = 'Beauchamp & Mennella 2011'
pron = {
    '新生児': 'シンセイジ', '羊水': 'ヨウスイ', '母乳': 'ボニュウ', '粉ミルク': 'コナミルク',
    '加水分解': 'カスイブンカイ', 'タンパク質': 'タンパクシツ', '好み': 'コノミ',
    '生得的': 'セイトクテキ', '苦味': 'ニガミ', '甘味': 'アマミ', '塩味': 'エンミ',
    'うま味': 'ウマミ', '味覚': 'ミカク', '経験': 'ケイケン',
    '授乳': 'ジュニュウ', '胎児': 'タイジ', '拒否': 'キョヒ', '受容': 'ジュヨウ',
}
scenes = [
    dict(
        text='生まれたばかりの赤ちゃんに、味は分かる？ 答えは、感じています。甘味が好きで、苦味は嫌う。',
        big='赤ちゃんに味は分かる？', sub='答え：感じている・甘味が好き', src=W,
        viz=T(2.6, [('よくある思い込み', '味はまだ分からない'), ('答え', '感じている'), ('好み', '甘味が好き・苦味は嫌う')]),
        claim_ids=['c1'],
    ),
    dict(
        text='甘味やうま味が好きで、苦味を嫌う傾向は、生まれつきと研究で分かっています。味を判断する仕組みを持って生まれるのです。',
        big='味の好みは生まれつき？', sub='甘味が好き・苦味は嫌う傾向', src=W,
        viz=T(2.8, [('甘味', '好む傾向'), ('うま味', '好む傾向'), ('苦味', '避ける傾向')]),
        claim_ids=['c2'],
    ),
    dict(
        text='ただ、3〜4か月ごろの赤ちゃんは、苦味や酸味の強い特殊なミルクも受け入れます。5〜6か月ごろになると、拒否する傾向が強まります。',
        big='生後半年ごろから変化', sub='生後数か月で受け止め方が変化', src=W,
        viz=dict(type='compare', l_label='3〜4か月', l_val='受け入れる', r_label='5〜6か月', r_val='拒否傾向'),
        claim_ids=['c3'],
    ),
    dict(
        text='味の経験は、お腹の中の羊水から始まり、母乳や粉ミルクで続きます。味を感じるだけでなく、経験で好みが形作られるのです。',
        big='経験が好みを作る', sub='羊水から母乳・粉ミルクへ', src=W,
        viz=T(2.8, [('胎児期', '羊水で風味を経験'), ('出生後', '母乳・粉ミルクで経験'), ('その先', '好みが形作られる')]),
        claim_ids=['c4'],
    ),
]
bg = [
    '柔らかな光に包まれた空のベビーベッドのマクロ映像。白いガーゼが静かに揺れ、人の顔は映さない（人物なし・文字なし）',
    '小さな透明な水滴が光を含んでゆっくり落ちるマクロ映像。柔らかく清らかな印象（人物なし・文字なし）',
    '二つの薄い色の光がゆっくり近づき、やがて一つの色に溶け合う抽象的な映像（人物なし・文字なし）',
    '淡い色の液体が静かに波打つマクロ映像。光が水面をゆっくり移動する（人物なし・文字なし）',
]
notes = (
    '■ 2026年11月23日に、Beauchamp & Mennella の総説「Flavor Perception in Human Infants」（'
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC3202923/）のPMC本文を読んで作った整理です。\n'
    '・根拠：甘味・うま味の好みと苦味の嫌悪は生得的な傾向がある。塩味への感受性と好みは生後4か月ごろに発達する。乳児は大人より甘味への好みが強い。'
    '3〜4か月未満の乳児は苦味・酸味の強い加水分解タンパク質ミルクを拒否せず受け入れるが、5〜6か月の乳児は拒否する。'
    '胎児期の羊水、出生後の母乳・粉ミルクを通じた風味の経験が、後の好みを形作る。\n'
    '・言い過ぎを避けた点：「味を感じない」を単純に否定するだけでなく、好みが経験で形作られる点も入れた。'
    '「生得的」は総説の表現に沿い、「生まれつき完全に決まっている」とは言わなかった。'
    '月齢には「ごろ」を付けて留保した。\n'
    '・使っていないこと：「大人より甘味への好みが強い」の具体的な比較値、苦味受容体の数、'
    '母乳に含まれる風味成分の詳細。\n'
    '・未確認：月齢による反応の個体差に関する一次データ。総説の知見を一般的な傾向として紹介している。'
)
claims = [
    dict(id='c1', statement='新生児は味を感じ、甘味を好み苦味を避ける傾向がある',
         source_type='primary', source_url='https://pmc.ncbi.nlm.nih.gov/articles/PMC3202923/',
         evidence_note='PMC総説2011の要旨・Origin of Flavor Preferences 節で確認。'),
    dict(id='c2', statement='甘味・塩味・うま味の好みと苦味の嫌悪には生得的な傾向がある',
         source_type='primary', source_url='https://pmc.ncbi.nlm.nih.gov/articles/PMC3202923/',
         evidence_note='PMC総説2011の要旨で確認。'),
    dict(id='c3', statement='3〜4か月ごろと5〜6か月ごろでは、苦味・酸味の強いミルクへの反応が異なる',
         source_type='primary', source_url='https://pmc.ncbi.nlm.nih.gov/articles/PMC3202923/',
         evidence_note='PMC総説2011の Postnatal Flavor Learning via Infant Formula 節で確認。'),
    dict(id='c4', statement='胎児期・出生後の風味の経験が、後の味の好みを形作る',
         source_type='primary', source_url='https://pmc.ncbi.nlm.nih.gov/articles/PMC3202923/',
         evidence_note='PMC総説2011の Prenatal/Postnatal Flavor Learning 節で確認。'),
]
needs_research = [
    '月齢による反応の差は総説が紹介する研究の結果。個体差の詳細は未確認だが、台本では「ごろ」と留保しており答えは変わらない。',
    '乳児の顔表情と味覚の関係は PMC5492973 の要旨のみ確認。台本では表情を断定材料にしていないため答えは変わらない。',
    '日本語の小児科・新生児科の一次資料は未確認。ただし英語の査読総説で骨格は確認できているため答えは変わらない。',
]

if __name__ == '__main__':
    build(
        'baby_taste',
        '赤ちゃんは味を感じないのか 新生児の味覚を論文で確かめる',
        '赤ちゃんに味は分かる？',
        '感じている。でも好みは経験で変わる',
        pron, scenes, bg, notes,
        bg_note='・動画内の図（模式図・比較）は自作です。背景の映像は FreeVideo（MiniMax H3）によるAI生成で、イメージです。実際の赤ちゃんの映像ではありません。\n',
        credit='・背景映像：FreeVideo（MiniMax H3）によるAI生成映像。イメージです。実際の赤ちゃんの映像ではありません\n・図・表：自作',
        end_q='皆さんは、赤ちゃんはどんな味が好きだと思いますか？',
        tags=['赤ちゃん', '新生児', '味覚', '科学', '誤解', '論文', '雑学', 'Shorts'],
        claims=claims, needs_research=needs_research,
    )
    fv_prompts('baby_taste', [
        'Soft macro view of an empty white baby bassinet with clean gauze fabric gently swaying, warm diffuse light, no people, no text, calm and tender.',
        'Macro view of a single clear water droplet slowly falling and catching soft light, pure clean atmosphere, shallow depth of field.',
        'Abstract soft light in two pale tints slowly drifting together and merging into one gentle tint, minimal calm motion, no text.',
        'Macro view of pale liquid gently rippling with soft light moving across the surface, clean tender atmosphere, no text.',
    ])
