"""単独Short(一般題材・年末の風習)：除夜の鐘は、なぜ108回？(solo_joya)。根拠は日本語版Wikipedia「除夜の鐘」(2026年11月14日に原文を確認。二次資料)。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
from solo_spec import build, T, fv_prompts
W = 'Wikipedia（除夜の鐘）'
pron = {'除夜の鐘': 'ジョヤノカネ', '煩悩': 'ボンノウ', '四苦八苦': 'シクハック', '寛永寺': 'カンエイジ', '由来': 'ユライ', '諸説': 'ショセツ', '風習': 'フウシュウ', '撞く': 'ツク', '中継': 'チュウケイ', '定着': 'テイチャク', '108回': 'ヒャクハッカイ'}
scenes = [
    dict(text='除夜の鐘が、108回なのは、なぜでしょうか。答えは、はっきりした定説がなく、いくつかの説が伝えられています。',
         big='除夜の鐘が108回なのは？', sub='答え：定説はなく、複数の説がある', src=W,
         viz=T(2.6, [('よくある説明', '煩悩の数だから'), ('実は', '由来には複数の説がある'), ('どの説が正しいか', 'わかっていない')])),
    dict(text='有名なのは、煩悩の数という説です。ほかに、四苦八苦から計算する説や、1年の暦の数を足す説があります。',
         big='108の由来は、諸説ある', sub='三つの説が知られている', src=W,
         viz=T(2.8, [('煩悩の数', '人間の煩悩の数を表す説'), ('四苦八苦', '4×9と8×9を足して108'), ('1年間', '12か月+二十四節気+七十二候')])),
    dict(text='1927年に、上野の寛永寺の除夜の鐘が、史上初めて、ラジオで中継されました。これが、全国に広く定着する、きっかけになったとされています。',
         big='1927年にラジオで初中継', sub='全国に定着するきっかけに', src=W,
         viz=T(2.8, [('1927年', '寛永寺の鐘がラジオで初中継'), ('その後', '全国に広く定着した'), ('定着のきっかけ', 'ラジオ中継とされる')])),
    dict(text='いまも、鐘をつく回数は、寺によって違います。108回と決まらず、200回以上の寺もあります。',
         big='回数は、寺によって違う', sub='108回と決まらない', src=W,
         viz=dict(type='compare', l_label='多くの寺', l_val='108回', r_label='寺によっては', r_val='200回以上')),
]
bg = ['夜の雪の寺の境内で、大きな青銅の釣り鐘が、鐘楼の中にさがっている映像(人物なし・文字なし)', '鐘楼の中で、撞木(木の棒)が、ゆっくり揺れて釣り鐘に近づく映像(人物なし・手なし・文字なし)',
      '古い木のラジオが、暖かい光の中に置かれている映像(人物なし・文字なし)', '雪の降る朝の寺の境内で、釣り鐘が静かにさがっている映像(人物なし・文字なし)']
notes = ('■ 日本語版Wikipedia「除夜の鐘」(2026年11月14日に原文を確認)にもとづく整理です。二次資料で、一次史料や書籍は読めていません。\n'
         '・108回の由来：Wikipediaは、人間の煩悩の数とする説、四苦八苦(四九36と八九72を足す)とする説、1年間(月の数12、二十四節気24、七十二候72を足す)とする説を挙げ、「どれが正しいかはわかっていない」と書いている。\n'
         '・ラジオ：東京・上野の寛永寺で1927年(昭和2年)、JOAK(NHK放送センターの前身の東京放送局)のラジオによって史上初めて中継放送され、これが「除夜の鐘」という風習が日本に広く定着するきっかけになった(同)。\n'
         '・回数：寺によって撞く回数は108回と決まらず、200回以上の場合などがある(同)。\n'
         '・言い過ぎを避けた点：「煩悩の数だから108回」と断定していない。浄土真宗の本山など、除夜の鐘を行わない寺もある(動画では触れていない)。\n'
         '・動画では使っていないこと：起源(中国の宋代の禅宗寺院の習慣に由来するとされる説)、昭和初期のラジオ以前の歴史の評価、戦時の鐘、近年の変化(昼間に撞く寺)。\n'
         '・未確認：一次史料や書籍での確認。\n'
         '・台本は、web版ChatGPTとGeminiのレビュー(2026年11月14日)を踏まえて、冒頭の言い方を「定説はなく、いくつかの説が伝えられている」に、数字の説明をナレーションから画面のカードに、「撞く」を「つく」に直しました。\n')
if __name__ == '__main__':
    build('joya', '除夜の鐘は、なぜ108回？ 由来は諸説あり', '除夜の鐘は、なぜ108回？', '由来は諸説あり、正解は不明', pron, scenes, bg, notes,
          bg_note='・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の寺や鐘の映像ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の寺や鐘の映像ではありません\n・図・表：自作', end_q='皆さんは、除夜の鐘を、生で聞いたことがありますか？')
    fv_prompts('joya', [
        'A large bronze temple bell hanging inside an open wooden bell tower in a snowy temple yard at night, soft lantern light, snowflakes falling slowly, no people, no text, the camera slowly pushing in.',
        'Inside a wooden bell tower, a heavy wooden striking log hanging on ropes slowly swings toward a large bronze temple bell, warm light, no hands, no people, no text, the camera fixed.',
        'An old vintage wooden tabletop radio glowing warmly on a wooden shelf, the dial lit softly, dust floating in the light, no people, no text, no letters on the dial, the camera slowly pushing in.',
        'A quiet snowy temple yard at early morning, a large bronze temple bell hanging in a wooden bell tower, snow falling gently, pale dawn light, no people, no text, the camera slowly gliding sideways.'],
        allow_buildings=True, allow_modern=True)
