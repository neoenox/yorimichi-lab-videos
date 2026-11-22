"""単独Short(身近な科学・連作「赤ちゃんの思い込み」①)：赤ちゃんは、泣いても涙が出ない？(solo_baby_namida)。根拠は日本語版Wikipedia「涙腺」(二次資料。2026年11月21日に原文を取得して確認 https://ja.wikipedia.org/wiki/涙腺)。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
from solo_spec import T, build, fv_prompts

W = '日本語版Wikipedia「涙腺」(二次資料)'
pron = {'涙腺': 'ルイセン', '分泌': 'ブンピツ', '涙液': 'ルイエキ', '未熟': 'ミジュク', '乾燥': 'カンソウ',
        '生後': 'セイゴ', '個人差': 'コジンサ'}
scenes = [
    {'text': '赤ちゃんは、泣いても涙が出ない？ 答えは、ほぼ本当。ただし、生まれたばかりの赤ちゃんの目を守る涙は、出ています。',
         'big': '泣いても涙は出ない', 'sub': '答え：ほぼ本当。目を守る涙は出ている', 'src': W,
         'viz': T(2.6, [('疑問', '泣いても涙が出ない？'), ('答え', 'ほぼ本当'), ('ただし', '目を守る涙は出ている')])},
    {'text': '生まれたばかりの赤ちゃん。涙腺の形はできていますが、働きはまだ未熟です。泣いても、涙が流れることは少ないのです。目を乾燥から守る涙は、少しずつ出ています。',
         'big': '涙腺は生まれつきある', 'sub': '形はできるが、働きはまだ未熟', 'src': W,
         'viz': T(2.8, [('生まれたとき', '涙腺の形はできている'), ('働き', 'まだ未熟'), ('出ている涙', '目を守る分だけ')])},
    {'text': '泣きながら涙を流せるようになるのは、生後2週間から2ヶ月ごろ。涙腺が育つまでには、数ヶ月かかることもあります。',
         'big': '涙を流して泣けるように', 'sub': '生後2週間〜2ヶ月ごろから', 'src': W,
         'viz': T(2.8, [('涙を流して泣く', '生後2週間〜2ヶ月ごろ'), ('育つまで', '数ヶ月かかることも'), ('それまで', '目を守る涙だけ')])},
    {'text': '3歳から5歳ごろには、大人と同じくらいになるとされています。',
         'big': '3〜5歳で大人に近づく', 'sub': '大人に近い量になるとされる', 'src': W + '・2026/11/21時点',
         'viz': T(2.8, [('3〜5歳ごろ', '大人に近い分泌量'), ('大人', '感情でも涙が出る'), ('時点', '2026年11月21日')])},
]
bg = ['ベビーベッドの中の、白い毛布と小さなまくら。朝の光が差し込む(人物なし・文字なし)',
      'やわらかなガーゼの布が、光を受けてしっとりと濡れているアップ(人物なし・文字なし)',
      '白い陶器の皿の上を、一滴の水滴が転がるマクロ。光を反射する(人物なし・文字なし)',
      '明るい部屋の窓辺。カーテン越しの光と、白い毛布の質感(人物なし・文字なし)']
notes = '''■ 出典：日本語版Wikipedia「涙腺」(https://ja.wikipedia.org/wiki/涙腺 )。2026年11月21日に原文を確認した二次資料です。
・涙腺は出生時までに形はできているものの、分泌能はまだ未熟です。生後2週間〜2ヶ月ごろに感情に伴う流涙が可能になり、3〜5歳ごろまでに大人と同等の分泌能力に達するとされています。目を乾燥から守る涙は、生まれたばかりの時期にも出ています。
・出典が二次資料のため、小児科・眼科の一次資料での直接確認はできていません。数値は「ごろ」「とされています」としています。2026年11月21日時点の情報です。'''
if __name__ == '__main__':
    build('baby_namida', '赤ちゃんは、泣いても涙が出ない？ 涙腺が育つまでの話', '泣いても涙が出ない？', 'ほぼ本当。ただし目を守る涙は出ている', pron, scenes, bg, notes,
          bg_note='',   # 背景のクレジットは credit 側に一本化
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の赤ちゃんの映像ではありません\n・図・表：自作',
          hook_card=False,   # 0:00〜0:01の結論カードが問いかけより先に出るのを防ぐ(2026-11-22 Google AIモード指摘)
          end_q='皆さんは、赤ちゃんが泣くとき、涙は出ていましたか？',
          tags=['赤ちゃん', '涙', '涙腺', '新生児', '育児', '雑学', '科学', 'Shorts'])
    fv_prompts('baby_namida', [
        'A white soft blanket and a small pillow inside a simple wooden baby crib, quiet morning light falling across the fabric, calm and empty, no people, no text, the camera slowly pushing in.',
        'Close-up of a soft white gauze cloth lying in a pool of light, the fibers glistening and slightly damp, very shallow depth of field, no people, no text, the camera slowly gliding sideways.',
        'Macro shot of a single clear water droplet rolling across a plain white ceramic saucer, catching the light, soft blurred background, no people, no text, the camera slowly pushing in.',
        'A bright window with a sheer white curtain, soft daylight falling on a folded white blanket, quiet and calm, no people, no text, the camera slowly gliding sideways.'],
        allow_modern=True)
