"""単独Short(身近な科学・連作「赤ちゃんの思い込み」②)：赤ちゃんの骨は、大人より100本多い？(solo_baby_hone)。根拠は英語版Wikipedia「Human skeleton」(2026年11月21日に原文を取得して確認 https://en.wikipedia.org/wiki/Human_skeleton)と、Cleveland Clinic「Skeletal System」(同 https://my.clevelandclinic.org/health/body/21048-skeletal-system )。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
from solo_spec import T, build, fv_prompts

W = 'Wikipedia「Human skeleton」／Cleveland Clinic'
pron = {'骨格': 'コッカク', '軟骨': 'ナンコツ', '仙骨': 'センコツ', '骨盤': 'コツバン', '癒合': 'ユゴウ',
        '頭蓋骨': 'ズガイコツ', '約': 'ヤク', '個人差': 'コジンサ', '付属骨': 'フゾクコツ', '206本': 'ニヒャクロッポン'}
scenes = [
    {'text': '赤ちゃんの骨は、大人より100本多い？ 答えは、ほぼ本当。数え方で変わります。',
         'big': '骨は大人より100本多い', 'sub': '答え：ほぼ本当。数え方で変わる', 'src': W,
         'viz': T(2.6, [('よくある話', '赤ちゃんは骨が300本'), ('大人', '約206本'), ('差', '約100本')])},
    {'text': '生まれたときの骨は、約270本。大人は、約206本です。300本という言い方も、数え方で変わります。',
         'big': '生まれた時は約270本', 'sub': '300本という言い方も', 'src': W,
         'viz': {'type': 'compare', 'l_label': '生まれたとき', 'l_val': '270本', 'r_label': '大人', 'r_val': '206本'}},
    {'text': '減るのは、壊れるからではありません。成長で、いくつかの骨がくっついて、1つになるからです。頭蓋骨の一部、骨盤の左右の骨は3つ、お尻の真ん中の仙骨は5つが、1つになります。',
     'big': '骨はくっついて減る', 'sub': '成長すると、いくつかの骨が1つになる', 'src': W,
     'viz': T(2.8, [('頭蓋骨', '一部が融合する'), ('骨盤の左右', '3つが1つに'), ('仙骨', '5つが1つに')])},
    {'text': '大人の骨も、人によって206本から213本と、違います。2026年11月21日時点の情報です。',
         'big': '大人の数も人それぞれ', 'sub': '206本から213本と違う', 'src': W,
         'viz': T(2.8, [('大人の骨', '206〜213本'), ('理由', '個人差がある'), ('時点', '2026年11月21日')])},
]
bg = ['白い骨格模型の胸郭（肋骨）のアップ。無地の背景、柔らかな光(人物なし・手なし・文字なし)',
      '白い骨格模型の頭と背骨が、無地の背景に立っている(人物なし・文字なし)',
      '机の上で、二つの白い木の立方体が、ゆっくり寄って1つになる(人物なし・文字なし)',
      '窓からの光が当たる、白い骨格模型の骨盤のアップ(人物なし・文字なし)']
notes = '''■ 出典：英語版Wikipedia「Human skeleton」(https://en.wikipedia.org/wiki/Human_skeleton ) と Cleveland Clinic「Skeletal System」(https://my.clevelandclinic.org/health/body/21048-skeletal-system )。2026年11月21日に原文を確認した二次資料です。
・出生時は約270本、成長に伴っていくつかの骨が癒合し、成人では約206本になるとされています。成人の骨の数は206〜213本と個人差があります。
・「赤ちゃんは300本」は軟骨も含めた数え方として広く言われますが、一次資料では確認できていません。減る理由は骨が壊れることではなく癒合です。2026年11月21日時点の情報です。'''
if __name__ == '__main__':
    build('baby_hone', '赤ちゃんの骨は、大人より100本多い？ 減る理由は、くっつくから', '骨は大人より100本多い？', 'ほぼ本当。数え方で変わる', pron, scenes, bg, notes,
          bg_note='',   # 背景のクレジットは credit 側に一本化
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の骨格標本の映像ではありません\n・図・表：自作',
          end_q='皆さんは、骨の数が変わることを知っていましたか？',
          tags=['赤ちゃん', '骨', '骨格', '軟骨', '解剖学', '人体', '雑学', '科学', 'Shorts'])
    fv_prompts('baby_hone', [
        'Close-up of the ribcage of a white anatomical skeleton model against a plain light background, soft diffuse light, clean bone-white surfaces, the camera slowly pushing in, no people, no hands, no text, no labels,',
        'A white anatomical model of a human skull and spine standing against a plain light background, soft studio light, no people, no text, no labels, the camera slowly gliding sideways.',
        'Two smooth white wooden cubes on a plain table slowly moving together and meeting into one shape, soft light, minimal composition, no people, no text, the camera slowly pushing in.',
        'Close-up of the pelvis part of a white anatomical skeleton model in soft window light, plain background, no people, no text, no labels, the camera slowly gliding sideways.'],
        allow_modern=True)
