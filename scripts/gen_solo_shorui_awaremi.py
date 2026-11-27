"""単独Short（歴史）：生類憐みの令は本当に悪法だったのか（solo_shorui_awaremi）。
根拠は J-Stage『「生類憐みの令」の動物観』（https://www.jstage.jst.go.jp/article/seibutsugakushi/99/0/99_11/_pdf）
と NDLレファレンス（https://crd.ndl.go.jp/reference/entry/index.php?id=1000327707&page=ref_view）。
2026年11月23日にPDF本文を確認。『犬だけではなかったが、罰は厳しかった』の両保存。
nolong, nolink。背景はFreeVideoのAI映像（イメージ）、図は自作。"""
from solo_spec import build, T, fv_prompts

W = 'J-STAGE論文／NDLレファレンス'
pron = {
    '生類憐みの令': 'ショウルイアワレミノレイ', '生類': 'ショウルイ', '憐み': 'アワレミ',
    '綱吉': 'ツナヨシ', '貞享': 'ジョウキョウ', '元禄': 'ゲンロク', '遺棄': 'イキ',
    '駕籠': 'カゴ', '囚人': 'シュウジン', '獄死': 'ゴクシ', '犬小屋': 'イヌゴヤ',
    '中野': 'ナカノ', '大久保': 'オオクボ', '切腹': 'セップク', '厳罰': 'ゲンバツ',
    '評価': 'ヒョウカ', '再評価': 'サイヒョウカ', '対象': 'タイショウ', 'Law': 'ロウ',
}
scenes = [
    dict(
        text='犬ばかり大事にした悪法、生類憐みの令。でも、「犬だけ」は誤り。生類には、人も含まれていました。',
        big='犬だけの法律？', sub='答え：半分誤り・人も含まれた', src=W,
        viz=T(2.6, [('よくある印象', '犬を大事にした悪法'), ('答え', '半分誤り'), ('生類', '犬だけでなく人も')]),
        claim_ids=['c1'],
    ),
    dict(
        text='1687年の令は、病人や牛や馬を捨てないもの。捨て子や牢屋での死も防ぐ目的でした。',
        big='1687年の法令', sub='病人・病牛馬の遺棄禁止から', src='J-STAGE論文',
        viz=T(2.8, [('1687年', '病人・病牛馬の遺棄禁止'), ('人', '捨て子の禁止'), ('囚人', '獄死を防ぐ')]),
        claim_ids=['c2'],
    ),
    dict(
        text='ただ、犬小屋は実在しました。中野には10万頭といわれる犬がいて、犬を傷つけた武士が切腹した例もあります。この厳しさが、悪法と呼ばれた理由です。',
        big='犬小屋は実在', sub='10万頭といわれ、罰も厳しかった', src=W,
        viz=dict(type='compare', l_label='中野の犬小屋', l_val='約10万頭', r_label='犬を傷つけると', r_val='切腹の例も'),
        claim_ids=['c3'],
    ),
    dict(
        text='犬だけではなかった。でも、罰は厳しかった。厳しさも、悪法と呼ばれる理由の一つ。今は再評価も進んでいます。',
        big='悪法か、再評価か', sub='犬だけではないが罰は厳しかった', src=W,
        viz=T(2.8, [('当時', '犬公方と呼ばれた'), ('記録', '人も守る令だった'), ('現在', '研究で再評価も')]),
        claim_ids=['c4', 'c1'],
    ),
]
bg = [
    '江戸の町並みを遠くから見た、落ち着いた情景。瓦屋根の町家が並び、夕暮れの光が柔らかく差す（人物なし・文字なし）',
    '黒い硯の表面で墨がゆっくり磨られ、筆先がわずかに動く接写。紙は映さない（人物なし・文字なし）',
    '木柵で囲われた広い空き地に、整然と並んだ小さな木の小屋が見える。淡い光の模式的な情景（人物なし・文字なし）',
    '江戸の静かな路地に木の葉がひらひらと落ち、柔らかな光が石畳を移動する映像。看板や紙は映さない（人物なし・文字なし）',
]
notes = (
    '■ 2026年11月23日に、J-Stage掲載の研究論文「『生類憐みの令』の動物観」（https://www.jstage.jst.go.jp/article/seibutsugakushi/99/0/99_11/_pdf）'
    'のPDF本文を読んで作った整理です。\n'
    '・根拠：通説では「人命より動物を優先した悪法」と評価されてきたが、20世紀末から「単なる悪法ではない」という記述が現れた。'
    '令は1687年の病人・病牛馬の遺棄禁止令から始まり、捨て子の禁止や囚人の獄死防止など、人間を含む内容が含まれた。'
    '一方で1695年には中野・大久保に犬小屋が設けられ、10万頭におよんだといわれる。犬を傷つけて切腹した例も記録されている。\n'
    '・言い過ぎを避けた点：「世界最初の動物保護法」という評価は論文内で紹介された研究者の見解なので断定しなかった。'
    '「10万頭」も記録の伝聞表現なので「といわれる」とした。'
    '「悪法ではなかった」とだけ言うと逆の誤解になるため、「人も含まれたが罰は厳しかった」と両方伝えた。\n'
    '・使っていないこと：綱吉の出身や桂昌院・隆光僧正にまつわる逸話、犬公方という呼び名の初出。\n'
    '・未確認：法令の原文そのもの、当時の判決記録の原本。'
)
claims = [
    dict(id='c1', statement='生類憐みの令の「生類」には人間も含まれ、犬だけを対象にした法令ではない',
         source_type='primary', source_url='https://www.jstage.jst.go.jp/article/seibutsugakushi/99/0/99_11/_pdf',
         evidence_note='J-Stage論文PDF本文109〜110行目、123〜124行目で確認。'),
    dict(id='c2', statement='令は1687年の病人・病牛馬の遺棄禁止令から始まった',
         source_type='primary', source_url='https://www.jstage.jst.go.jp/article/seibutsugakushi/99/0/99_11/_pdf',
         evidence_note='J-Stage論文PDF本文147行目で確認。'),
    dict(id='c3', statement='1695年に中野・大久保に犬小屋が設けられ、10万頭といわれる犬が収容された。犬を傷つけて切腹した例もある',
         source_type='primary', source_url='https://www.jstage.jst.go.jp/article/seibutsugakushi/99/0/99_11/_pdf',
         evidence_note='J-Stage論文PDF本文329〜349行目、380行目で確認。'),
    dict(id='c4', statement='生類憐みの令の評価は、20世紀末以降「単なる悪法ではない」という論調へ変わってきた',
         source_type='primary', source_url='https://www.jstage.jst.go.jp/article/seibutsugakushi/99/0/99_11/_pdf',
         evidence_note='J-Stage論文PDF本文45〜49行目、166〜223行目で確認。'),
]
needs_research = [
    '法令の原文と判決記録の原本は未確認。ただしJ-Stage論文が原文を引用して整理しており答えは変わらない。',
    '10万頭は記録の伝聞表現。台本では「といわれる」としたため答えは変わらない。',
    '東京都公文書館のページは町触全般の解説で直接の原文ではない。出典表示には使っていないため答えは変わらない。',
]

if __name__ == '__main__':
    build(
        'shorui_awaremi',
        '生類憐みの令は本当に悪法だったのか 記録で確かめる',
        '生類憐みの令は悪法？',
        '犬だけではないが、罰は厳しかった',
        pron, scenes, bg, notes,
        bg_note='・動画内の図（比較・模式図）は自作です。背景の映像は FreeVideo（MiniMax H3）によるAI生成で、イメージです。実際の江戸の映像ではありません。\n',
        credit='・背景映像：FreeVideo（MiniMax H3）によるAI生成映像。イメージです。実際の江戸の映像ではありません\n・図・表：自作',
        end_q='皆さんは、生類憐みの令と聞いて、何を思い浮かべますか？',
        tags=['生類憐みの令', '徳川綱吉', '江戸時代', '歴史', '誤解', '一次史料', '雑学', 'Shorts'],
        claims=claims, needs_research=needs_research,
    )
    fv_prompts('shorui_awaremi', [
        'Wide cinematic view of an old Japanese town with tiled roofs and wooden houses at dusk, soft warm light, calm atmosphere, no people.',
        'Extreme macro of a dark inkstone surface with wet ink slowly being ground, the tip of a brush moving gently, no paper visible, soft even light.',
        'Wide view of a quiet open field with rows of small simple old wooden kennels, no fences, no metal mesh, no wire, soft morning light, calm minimal composition, no people.',
        'A quiet old Japanese alley with a single dry leaf drifting down onto stone paving, soft light moving across the ground, no signs, no paper, calm atmosphere.',
    ])
