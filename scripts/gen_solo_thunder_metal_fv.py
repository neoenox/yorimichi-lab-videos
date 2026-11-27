"""単独Short：雷と金属（solo_thunder_metal_fv）。根拠は日本気象学会『天気』1995年2月号の
「落雷と人体」p.53–57 と気象庁「雷から身を守るには」。台本・根拠は自作版と同じ。
2026-11-22のオーナー判断で自作イラスト背景をAIクリップへ差し替えた版。背景はFreeVideo(MiniMax H3)、図は自作。
"""
from solo_spec import T, build, fv_prompts

W = '日本気象学会『天気』1995'
pron = {'雷雲': 'ライウン', '落雷': 'ラクライ', '金属': 'キンゾク', '絶縁': 'ゼツエン',
        '突き出る': 'ツキデル', '姿勢': 'シセイ', '避難': 'ヒナン', '気象庁': 'キショウチョウ',
        '日本気象学会': 'ニホンキショウガッカイ', '日本大気電気学会': 'ニホンタイキデンキガッカイ', '大気電気学会': 'タイキデンキガッカイ',
        '釣り竿': 'ツリザオ', '傘': 'カサ', '高く': 'タカク'}
scenes = [
    {'text': '雷が近づいたら、金属を外せ。本当でしょうか。答えは、間違いです。',
     'big': '金属を外せば安全？', 'sub': '答え：間違い', 'src': '日本気象学会『天気』1995 p.53・p.56',
     'viz': T(2.6, [('噂', '金属を外せ'), ('答え', '間違い'), ('先に', '姿勢を低く')])},
    {'text': '日本大気電気学会のQ&Aは、金属をはずしても、少しも安全にはならないと答えています。',
     'big': '外しても安全にならない', 'sub': '学会のQ&Aに明記', 'src': '日本気象学会『天気』1995 p.53',
     'viz': T(2.8, [('問い', '金属を外す？'), ('答え', '安全にならない'), ('根拠', '23年の事故調査')])},
    {'text': '問題は、傘や釣り竿が頭より高く突き出ること。金属でも非金属でも、高く突き出ると落雷を受けやすくなります。',
     'big': '高いものが危ない', 'sub': '金属・非金属は関係ない', 'src': '日本気象学会『天気』1995 p.54',
     'viz': T(2.8, [('傘・釣り竿', '頭より高い'), ('受けやすさ', '素材に限らない'), ('対策', '低く構える')])},
    {'text': 'ゴム長靴やレインコートも、雷の電圧では絶縁が破られます。金属を外すより、まず姿勢を低くしてください。',
     'big': '絶縁も効かない', 'sub': 'まず姿勢を低く', 'src': '日本気象学会『天気』p.53–54',
     'viz': T(2.8, [('ゴム長靴', '絶縁が破られる'), ('金属を外す', '後回し'), ('最初に', '姿勢を低く')])},
    {'text': '気象庁は、まず建物や車の中へ避難するよう案内しています。近くにない時は、木の幹や枝葉から2メートル以上離れ、姿勢を低く。金属より、高く突き出さないことが先です。',
     'big': '正解は高くしない', 'sub': '安全な場所へ避難', 'src': '気象庁「雷から身を守るには」・確認日11/22',
     'viz': {'type': 'compare', 'l_label': '金属', 'l_val': '外すより', 'r_label': '姿勢', 'r_val': '低く避難'}},
]
notes = '''■ 出典：日本気象学会『天気』42巻2号（1995年2月）「落雷と人体」p.53–57
https://www.metsoc.jp/tenki/pdf/1995/1995_02_0119.pdf
・同論文が引用する日本大気電気学会のQ&Aは「金属をはずしても，少しも安全にはなりません」「金属製品，金属片は，身につけたまま避難します」。高く突き出る物は金属・非金属にかかわらず落雷を受けやすく、ゴム長靴やレインコートも雷の電圧では絶縁が破られます。
・気象庁「雷から身を守るには」https://www.jma.go.jp/jma/kishou/know/toppuu/thunder4-3.html は、まず建物や車の中へ避難し、近くにない場合は木の幹・枝葉から2m以上離れて姿勢を低くするよう案内しています。
・留保：被打った後に金属周辺の熱傷・電紋が出ることがあります（同論文p.56）。これは「雷を呼ぶ」話ではありません。学会Q&Aの原本は未取得で、1995年論文の引用を根拠にしています。2026年11月22日時点の情報。'''
claims = [
 {'id':'c_metal','statement':'金属を外す必要はなく、身につけたままでよい','source_type':'primary',
  'source_url':'https://www.metsoc.jp/tenki/pdf/1995/1995_02_0119.pdf',
  'evidence_note':'日本気象学会『天気』1995年2月号p.53に「金属をはずしても，少しも安全にはなりません…金属製品，金属片は，身につけたまま避難します」、p.56に「金属は身につけているほうが安全で，ポケットの硬貨を投げ出す必要は，さらさらありません」。PDF本文を抽出して確認。'},
 {'id':'c_height','statement':'人体から高く突き出る物体は、金属・非金属にかかわらず落雷を受けやすい','source_type':'primary',
  'source_url':'https://www.metsoc.jp/tenki/pdf/1995/1995_02_0119.pdf',
  'evidence_note':'同論文p.54の問14の答えに「人体から更に高く物体が突き出ると，金属・非金属にかかわらず一層落雷を受け易くなります」と明記。PDF本文を抽出して確認。'},
 {'id':'c_insulation','statement':'ゴム長靴やレインコートは雷の高電圧では絶縁が破られ、防護にならない','source_type':'primary',
  'source_url':'https://www.metsoc.jp/tenki/pdf/1995/1995_02_0119.pdf',
  'evidence_note':'同論文p.53–54に「ゴム長靴，レインコートは雷を防ぐ役には立ちません」「落雷の電界に対しては…絶縁は破壊され」とある。PDF本文を抽出して確認。'},
 {'id':'c_jma','statement':'気象庁はまず安全な空間へ避難し、近くにない場合は高い木から2m以上離れて姿勢を低くするよう案内している','source_type':'primary',
  'source_url':'https://www.jma.go.jp/jma/kishou/know/toppuu/thunder4-3.html',
  'evidence_note':'2026-11-22に気象庁本文を取得。優先は「鉄筋コンクリート建築、自動車…の内部」への避難。「近くに安全な空間が無い場合は」高い物体から4m以上離れ、木の全ての幹・枝・葉（枝葉）から2m以上離れて姿勢を低くすると明記。'},
]
needs_research = [
    '日本大気電気学会のQ&A原本（1971年発足の研究グループによる23年調査）は未取得。1995年の学会論文が引用する答えを根拠にしており、答えは変わらない。',
    '被打った後の金属周辺の熱傷・電紋（同論文p.56）は本編で触れていない。落雷確率の説明とは別問題で、答えは変わらない。',
]
for i,cid in enumerate([['c_metal'],['c_metal'],['c_height'],['c_insulation','c_jma'],['c_jma']]):
    scenes[i]['claim_ids'] = cid

if __name__ == '__main__':
    build('thunder_metal_fv', '雷が近づいたら金属を外せ？ 実は外す必要はありません',
          '金属を外せば安全？', '間違い。先に姿勢を低く', pron, scenes,
          ['雷雲の下の暗い空（人物なし・文字なし）', '雨の中の金属のペンダント（文字なし）',
           '傘の先が頭より高くなる模式（人物なし・文字なし）', 'ゴム長靴と水滴（人物なし・文字なし）',
           '岩場と遠くの稲妻（人物なし・文字なし）'], notes,
          bg_note='',   # 背景のクレジットは credit 側に一本化
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の落雷の映像ではありません\n・図・表：自作',
          claims=claims, needs_research=needs_research,
          end_q='皆さんは、雷のとき金属を外していましたか？',
          tags=['雷','落雷','金属','安全','防災','科学','雑学','Shorts'])
    fv_prompts('thunder_metal_fv', [
        'Dramatic dark cumulonimbus clouds rolling over an open plain, a distant lightning flash glowing inside the cloud, rain streaks in the air, cinematic realistic look, slow camera push in, moody blue-grey light,',
        'Close-up of a small smooth polished metal sphere resting on wet dark stone, heavy raindrops splashing around it, soft reflections, shallow depth of field, slow camera glide, moody blue-grey light,',
        'Low angle view of a slender bare branch and tall wet reeds sticking far above a flat field, storm clouds and rain behind them, dramatic sky, slow camera tilt upward,',
        'Raindrops beading and sliding down a dark smooth waterproof fabric surface, close-up in heavy rain, soft moody light, slow camera push in,',
        'Dark rocky ground under an immense storm sky, a distant lightning bolt over the horizon, wind driven rain crossing the frame, low camera gliding slowly sideways,',
    ])
