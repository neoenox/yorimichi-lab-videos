"""単独Short(身近な科学)：冬に息が白くなるのは寒さだけじゃない(solo_white_breath)。
根拠は気象庁「はれるんランド」、豊川市の白煙の説明、JST「高校生のための科学」(2026年11月25日に確認)。
nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
from solo_spec import build, T, fv_prompts

W = '気象庁・自治体の解説'
pron = {
    '息が白く': 'イキガシロク',
    '水蒸気': 'スイジョウキ',
    '結露': 'ケツロ',
    '湿度': 'シツド',
    '露点': 'ロテン',
    'こもり': 'コモリ',
    'ひこうき雲': 'ヒコウキグモ',
}
scenes = [
    dict(text='冬に息が白くなる。寒いからだと思っていませんか。実は、寒さだけじゃありません。湿度も関係します。',
         big='寒さだけじゃない', sub='息が白くなるには湿度も関係する', src=W,
         viz=T(2.6, [('思い込み', '寒さだけ'), ('実際は', '寒さ＋湿度'), ('白い正体', '小さな水滴')])),
    dict(text='吐いた息は、体温に近い約36度。その中には、目に見えない水蒸気が含まれています。',
         big='息は約36度', sub='水蒸気を含んだ暖かい空気', src=W,
         viz=T(2.8, [('息の温度', '約36度'), ('中身', '目に見えない水蒸気'), ('外の空気', '冷たい')])),
    dict(text='暖かい息が冷たい外気に触れると、水蒸気が小さな水滴になって、白く見えます。結露と同じ仕組みです。',
         big='白いのは水滴', sub='水蒸気が冷えて結露する', src=W,
         viz=T(2.8, [('水蒸気', '目に見えない'), ('冷えると', '小さな水滴'), ('見え方', '白く見える')])),
    dict(text='気象庁によると、同じ仕組みのひこうき雲も、温度や湿度ででき方が変わるそうです。息も仕組みは同じ。晴れの日より雨の日は、気温が高くても白く見えます。',
         big='湿度でも変わる', sub='雨の日は白く見えやすい', src=W,
         viz=T(2.8, [('気象庁', '温度と湿度の両方'), ('雨の日', '湿度が高い'), ('息', '白く見えやすい')])),
]
bg = [
    '寒い冬の朝の空気に、小さな白い息の粒がふわりと広がる接写、暗い青灰色の背景、人物の顔は映さない、文字なし、ゆっくりした動き',
    '透明なガラスのコップの表面に、小さな水滴が結露して光る接写、柔らかい光、文字なし、ゆっくりカメラが寄る',
    '冷たい空気の中を通る一筋の白い水蒸気が、小さな水滴の粒に変わって広がる模式的な映像、文字なし、ゆっくりした動き',
    '雨の日の窓辺に付いた水滴と、しんしんと降る雨、冷たい青い光、人物なし、文字なし、カメラはゆっくり横に動く',
]
notes = (
    '■ 2026年11月25日に確認した一次資料にもとづく整理です。\n'
    '・気象庁「はれるんランド」(https://www.jma.go.jp/jma/kids/kids/faq/a2_01.html )：ひこうき雲は「冬の寒い日に人間がはく息が白く見えるのと同じこと」で、「上空の温度や湿度、ジェット機のはい気ガスの温度などにより、できるときとできないときがある」と明記。温度だけでなく湿度も条件。\n'
    '・豊川市清掃工場の白煙について(https://warp.ndl.go.jp/info:ndljp/pid/10299136/www.city.toyokawa.lg.jp/shisetsu/sonota/seisokojo/hakuen.html )：白煙は水蒸気が冷えて水滴になる結露で、「吐く息が白くなる寒い季節とほぼ同じ」「特に湿度の高い雨天時に目立つ」と明記。\n'
    '・JST「高校生のための科学」(https://koushien.jst.go.jp/koushien/pastexam/2016/files/1-1.pdf )：やかんの湯気を題材に、温度だけでなく空気に含まれる水蒸気の量も関係すると解説。\n'
    '・数字：息の温度「約36度」と「13度以下が目安」は JAL の天気情報(http://weather.jal.co.jp/seasonal/12/seasonal_12f.html )の記述。気象庁の値ではないため、13度は台本で使っていない。36度は体温とほぼ同じという一般的な数値として使った。\n'
    '・言い過ぎを避けた点：「寒さだけで決まる」とは言わず、気象庁の記述に沿って温度と湿度の両方に触れた。「息が白い＝体温が低い」という断定はしていない。\n'
    '・動画では使っていないこと：露点の数値、絶対湿度、口の開け方による違い。\n'
    '・背景は FreeVideo(MiniMax H3)によるAI生成映像で、イメージです。図は自作です。\n'
)
if __name__ == '__main__':
    build('white_breath', '冬に息が白くなるのは寒さだけじゃない？', '息が白くなる理由', '寒さだけじゃない。湿度も関係', pron, scenes, bg, notes,
          bg_note='・動画内の図(並び)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の息や結露の映像ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の息や結露の映像ではありません\n・図・表：自作',
          end_q='皆さんは、寒い日に息が白くなるのを見たことがありますか？',
          tags=['息が白くなる', '冬', '気象', '湿度', '結露', '気象庁', '科学', '雑学', 'Shorts'])
    fv_prompts('white_breath', [
        'Extreme close-up of a tiny cloud of white breath mist spreading in cold blue-grey winter air, backlit by soft pale daylight, no face, no people, no text, no buildings, the camera slowly pushing in.',
        'Close-up of a clear glass surface with tiny water droplets forming and glistening, condensation visible, soft cool light, no text, no people, no fingers, the camera slowly gliding sideways.',
        'A thin stream of transparent vapor moving through dark cold air and turning into a fine cloud of small glowing water droplets, abstract schematic look, no text, no people, no buildings, the camera slowly pushing in.',
        'Raindrops running down a window pane on a cold grey day, wet outdoor light, soft blue tones, no people, no text, no buildings close up, the camera slowly gliding sideways.',
    ])
