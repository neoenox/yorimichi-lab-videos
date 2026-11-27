"""単独Short：救急車の軽症は半数？タクシー代わりという思い込みを消防庁の統計で検証。

根拠（2026-11-20本文確認）:
 https://www.fdma.go.jp/publication/hakusho/r7/chapter2/section5/69369.html
 https://www.fdma.go.jp/publication/hakusho/r7/document/69514.html
背景は既存クリップを流用（AI生成・イメージ）。"""
from solo_spec import build, T
W = '総務省消防庁「消防白書」'
pron = {'救急車': 'キュウキュウシャ', '搬送': 'ハンソウ', '軽症': 'ケイショウ', '入院': 'ニュウイン',
        '外来診療': 'ガイライシンリョウ', '傷病程度': 'ショウビョウテイド', '消防庁': 'ショウボウチョウ'}
claims = [
 {'id':'fdma-469','statement':'令和6年中の救急自動車による搬送人員676万9172人のうち46.9%が入院加療を必要としない軽症（外来診療）傷病者及びその他である',
  'source_type':'primary','source_url':'https://www.fdma.go.jp/publication/hakusho/r7/chapter2/section5/69369.html',
  'evidence_note':'消防白書本文「676万9,172人のうち、46.9％が入院加療を必要としない軽症（外来診療）傷病者及びその他」を確認（2026-11-20）'},
 {'id':'fdma-light-def','statement':'軽症（外来診療）とは傷病程度が入院加療を必要としないものを指す',
  'source_type':'primary','source_url':'https://www.fdma.go.jp/publication/hakusho/r7/document/69514.html',
  'evidence_note':'消防白書資料2-5-5の備考「軽症（外来診療）　傷病程度が入院加療を必要としないもの」を確認（2026-11-20）'},
 {'id':'fdma-other','statement':'その他には医師の診断がないものや傷病程度が判明しないもの等が含まれる',
  'source_type':'primary','source_url':'https://www.fdma.go.jp/publication/hakusho/r7/document/69514.html',
  'evidence_note':'消防白書資料2-5-5の備考「その他　医師の診断がないもの及び傷病程度が判明しないもの、その他の場所へ搬送したもの」を確認（2026-11-20）'},
]
needs_research = [
 '軽症のケースに不適切な利用がどれだけ含まれるかは消防白書の数字からは分からない。このShortは定義の説明しかしないため答えに影響しない',
]
scenes = [
 dict(text='救急車で運ばれた人の半分は、タクシー代わり。本当でしょうか。',
      big='半分は不要？', sub='消防庁の統計で確認', src=W, claim_ids=['fdma-469'],
      viz=T(2.6, [('思い込み', '半分は不要'), ('確認', '消防庁の統計'), ('数字', '46.9%')])),
 dict(text='令和6年の搬送は、およそ677万人。46.9%が入院不要の軽症などでした。',
      big='46.9%が軽症など', sub='2024年・搬送676万人', src=W, claim_ids=['fdma-469'],
      viz=T(2.8, [('搬送', '676万9172人'), ('軽症など', '46.9%'), ('年', '令和6年')])),
 dict(text='軽症とは入院加療が不要な傷病。医師の診断がないケースも「その他」に含まれます。',
      big='軽症＝入院不要', sub='その他も含む数字', src=W, claim_ids=['fdma-light-def','fdma-other'],
      viz=T(2.8, [('軽症', '入院が不要'), ('その他', '診断なし等'), ('意味', '不要ではない')])),
 dict(text='数字だけではタクシー代わりかは分かりません。判断は症状をもとに。令和6年のデータです。',
      big='数字だけでは分からない', sub='症状をもとに判断', src=W, claim_ids=['fdma-other'],
      viz=T(2.8, [('数字', '定義の集合'), ('分からない', '利用の動機'), ('判断', '症状をもとに')])),
]
bg = ['quiet city street at dawn', 'exterior of a modern hospital entrance without signage', 'calm emergency scene without people or text', 'empty street with soft morning light']
notes = ('■ 2026年11月20日に、総務省消防庁「令和7年版消防白書」の本文と資料2-5-5を読んで作った整理です。\n'
         '・使った事実：令和6年中の搬送人員676万9,172人。うち46.9%が入院加療を必要としない軽症（外来診療）傷病者及びその他。軽症は「傷病程度が入院加療を必要としないもの」。その他は「医師の診断がないもの及び傷病程度が判明しないもの、その他の場所へ搬送したもの」。\n'
         '・言い過ぎを避けた点：「軽症＝タクシー代わり」とは言わない。46.9%は定義上の区分の集合で、利用の動機や適切さは統計から読み取れない。\n'
         '・使っていないこと：不適切な利用の割合、救急車の利用料金、119番の運用詳細。\n'
         '・未確認：軽症ケースの利用動機。答えは定義の説明のため影響しない。\n'
         '・背景：既存クリップを流用したAI生成映像のイメージです。実際の救急現場ではありません。\n')
if __name__ == '__main__':
    build('ambulance', '救急車の軽症は半分？タクシー代わりかを消防庁の統計で確かめる #Shorts',
          '軽症は半数？', '入院が不要な人が多いだけ', pron, scenes, bg, notes,
          claims=claims, needs_research=needs_research,
          bg_note='・背景は既存クリップを流用したAI生成映像のイメージです。実際の救急現場ではありません。\n',
          credit='・出典：総務省消防庁「令和7年版消防白書」本文・資料2-5-5\n・背景：既存クリップを流用（AI生成・イメージ）\n・図・表：自作',
          end_q='救急車、ためらったことはありますか？',
          tags=['救急車', '消防庁', '統計', '軽症', '社会制度', '雑学', '検証', 'Shorts'])
