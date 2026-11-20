"""試作：竜巻注意報は竜巻が来た意味？（solo_proto_tatsumaki）。

今日のニュース（2026-11-20 9:36 新潟県の中越・上越に竜巻注意報）をきっかけに、
全Shorts分析の戦略（30〜45秒・身近な思い込み・一次資料で検証）を試す。
根拠は気象庁「気象防災速報（竜巻注意／竜巻目撃）・竜巻ナウキャスト」
https://www.jma.go.jp/jma/kishou/know/bosai/tatsumaki.html （2026-11-20に本文確認）。
背景は既存の台風クリップを流用（試作専用・AI生成のイメージ）。"""
from solo_spec import build, T
W = '気象庁「気象防災速報（竜巻注意）」'
pron = {'竜巻': 'タツマキ', '注意報': 'チュウイホウ', '積乱雲': 'セキライウン',
        'ダウンバースト': 'ダウンバースト', '突風': 'トップウ', '新潟県': 'ニイガタケン'}
claims = [
 {'id':'jma-tatsumaki-warning','statement':'気象防災速報（竜巻注意）は、積乱雲の下で発生する竜巻やダウンバーストなどの激しい突風に対して注意を呼びかける情報である',
  'source_type':'primary','source_url':'https://www.jma.go.jp/jma/kishou/know/bosai/tatsumaki.html',
  'evidence_note':'気象庁の本文で「積乱雲の下で発生する竜巻、ダウンバーストなどの激しい突風に対して注意を呼びかける情報」を確認（2026-11-20）'},
 {'id':'jma-supplement','statement':'竜巻注意報は雷注意報を補足する情報として発表される',
  'source_type':'primary','source_url':'https://www.jma.go.jp/jma/kishou/know/bosai/tatsumaki.html',
  'evidence_note':'気象庁の本文で「雷注意報を補足する情報として発表します」を確認（2026-11-20）'},
 {'id':'jma-probability','statement':'竜巻注意報は発生確度2が現れた地域を対象に発表される',
  'source_type':'primary','source_url':'https://www.jma.go.jp/jma/kishou/know/bosai/tatsumaki.html',
  'evidence_note':'気象庁の本文で「竜巻ナウキャストで発生確度2が現れた地域を対象に発表します」を確認（2026-11-20）'},
]
needs_research = [
 '2026年11月20日の発表時刻・対象地域（新潟県中越・上越）は報道記事で確認。気象庁の発表原文は未確認だが、この試作は注意報の意味を扱うため答えに影響しない',
]
scenes = [
 dict(text='2026年11月20日、竜巻注意報。竜巻が来たという意味？',
      big='竜巻が来た？', sub='2026年11月20日', src=W, claim_ids=['jma-tatsumaki-warning'],
      viz=T(2.6, [('ニュース', '竜巻注意報'), ('思い込み', '竜巻が来た'), ('確認', '気象庁の定義')])),
 dict(text='気象庁では、積乱雲の下の竜巻やダウンバーストなど、激しい突風への注意を呼びかけています。',
      big='注意を呼びかける情報', sub='積乱雲の下の突風', src=W, claim_ids=['jma-tatsumaki-warning'],
      viz=T(2.8, [('対象', '竜巻・ダウンバースト'), ('原因', '積乱雲'), ('目的', '注意を呼びかける')])),
 dict(text='発生を知らせるものではありません。可能性が高い地域に、雷注意報を補足する形で出されます。',
      big='発生の予告ではない', sub='雷注意報を補足', src=W, claim_ids=['jma-supplement','jma-probability'],
      viz=T(2.8, [('確度2', '対象地域'), ('補足', '雷注意報'), ('意味', '可能性が高い')])),
 dict(text='空の様子に注意し、危険なら頑丈な建物へ。最新は気象庁で。2026年11月20日時点です。',
      big='最新情報を確認', sub='気象庁の発表を見る', src=W, claim_ids=['jma-tatsumaki-warning'],
      viz=T(2.8, [('空', '積乱雲に注意'), ('行動', '頑丈な建物へ'), ('情報', '気象庁で確認')])),
]
bg = ['storm clouds over dark sea', 'dramatic cloud vortex', 'storm clouds over coast', 'blue sky with thin clouds']
notes = ('■ 2026年11月20日に、気象庁「気象防災速報（竜巻注意／竜巻目撃）・竜巻ナウキャスト」'
         '(https://www.jma.go.jp/jma/kishou/know/bosai/tatsumaki.html )の本文を読んで作った試作です。\n'
         '・使った事実(同)：竜巻注意報は積乱雲の下で発生する竜巻・ダウンバーストなどの激しい突風への注意を呼びかける情報。雷注意報を補足する情報として発表。竜巻ナウキャストで発生確度2が現れた地域を対象に発表。\n'
         '・言い過ぎを避けた点：「竜巻が来る」とは言わず、「可能性が高まった」という注意喚起として説明した。発生を予告する情報ではない。\n'
         '・使っていないこと：2026年11月20日の具体的な発表時刻・対象地域の詳細（報道のみ）。竜巻発生確度の数式・運用の詳細。\n'
         '・未確認：気象庁の発表原文（時刻・対象地域）。この試作の答えには影響しない。\n'
         '・背景：試作のため既存の台風クリップを流用。実際の竜巻や当日の空の映像ではない。\n')
if __name__ == '__main__':
    build('proto_tatsumaki', '【2026年11月20日】竜巻注意報は、竜巻が来たという意味？ 約38秒で確かめる #Shorts',
          '竜巻注意報の意味', '発生の予告ではない', pron, scenes, bg, notes,
          claims=claims, needs_research=needs_research,
          bg_note='・背景は試作用に既存の台風クリップを流用したAI生成映像のイメージです。実際の竜巻や当日の空ではありません。\n',
          credit='・出典：気象庁「気象防災速報（竜巻注意／竜巻目撃）・竜巻ナウキャスト」\n・背景：既存の台風クリップを流用（AI生成・イメージ）\n・図・表：自作',
          end_q='気象警報、どれを読んだことがありますか？',
          tags=['竜巻注意報', '気象庁', '天気', '防災', 'ニュース', '雑学', '検証', 'Shorts'])
