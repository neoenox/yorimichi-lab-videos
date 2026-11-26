"""単独Short(科学)：満月のたびに月食が起きる？(solo_eclipse)。
根拠は国立天文台 暦Wiki「月食／なぜ毎月(望)に月食がおこらないのですか」
(https://eco.mtk.nao.ac.jp/koyomi/wiki/B7EEBFA92FBEF2B7EF.html 、2026年11月26日にEUC-JPで本文確認)。
nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
from solo_spec import build, T, fv_prompts

W = '国立天文台 暦Wiki'
pron = {
    '白道': 'ハクドウ',
    '黄道': 'コウドウ',
    '交点': 'コウテン',
    '月食': 'ゲッショク',
    '満月': 'マンゲツ',
    '公転軌道': 'コウテンキドウ',
    '5.1°': 'ゴテンイチド',
}
scenes = [
    dict(text='満月のたびに、月食が起きる？ 起きません。満月と、二つの通り道が交わる場所。両方そろって、はじめて月食になります。',
         big='満月でも月食は稀', sub='満月だけでは足りません', src=W,
         viz=dict(type='compare', l_label='満月', l_val='毎月', r_label='月食', r_val='約半年に1回')),
    dict(text='月の通り道は、地球の通り道に対して、約5.1度傾いています。この傾きが、月を地球の影の上下に外します。',
         big='通り道が約5.1度傾く', sub='白道と黄道は約5.1度違う', src=W,
         viz=dict(type='flow', hub='満月', mid=['白道は5.1度傾く', '影の上下を通る'], leaf='月食にならない')),
    dict(text='ところが、二つの通り道が交わる、交点の付近。そこで満月になると、地球の影に入って月食になります。',
         big='交点の付近だけ', sub='昇交点・降交点の付近', src=W,
         viz=T(2.8, [('必要条件1', '満月'), ('必要条件2', '交点付近'), ('両方で', '月食')])),
    dict(text='交点付近で満月になるのは、約半年に1回。だから、月食も約半年に1回程度。満月は毎月あっても、月食はめずらしいのです。',
         big='月食は半年に1回ほど', sub='満月＋交点付近', src=W,
         viz=dict(type='compare', l_label='満月', l_val='毎月', r_label='月食', r_val='約半年に1回')),
]
bg = [
    '夜空に浮かぶ満月が、雲の間からゆっくり顔を出す接写、冷たい青い光、文字なし・人物なし・建造物なし、ゆっくりカメラが寄る',
    '暗い宇宙空間に、二つの細い楕円の軌道が角度を違えて重なっている模式的な映像、光の線だけ、文字なし・数字なし・人物なし、ゆっくり回る',
    '地球の丸い影に、小さな月が静かに入っていく模式的な映像、暗い赤みのある光、文字なし・人物なし・建造物なし、ゆっくりカメラが寄る',
    '夜空に小さな星がまたたき、満月がゆっくりと地平線へ沈む映像、静かな青い光、文字なし・人物なし・建造物なし、カメラは固定',
]
notes = (
    '■ 2026年11月26日に国立天文台 暦Wiki「月食／なぜ毎月(望)に月食がおこらないのですか」'
    '(https://eco.mtk.nao.ac.jp/koyomi/wiki/B7EEBFA92FBEF2B7EF.html )の本文を確認して作った整理です。'
    'web_fetch では EUC-JP が文字化けしたため、Python で取得して decode("euc_jp") して読みました。\n'
    '・月の公転軌道面は、地球の公転軌道面である黄道面に対して5.1°程度傾いている(原文)。\n'
    '・この傾きのため、軌道の交点付近で満月(望)となるときにしか月食は起こらない(原文)。\n'
    '・交点付近に来るのは約半年に1回で、月食も約半年に1回程度(原文)。\n'
    '・地球と月の動きは連動していないので、必ずしも毎回交点ぴったりで満月になるわけではない(原文)。\n'
    '・言い過ぎを避けた点：「満月なら月食」とは言わず、交点付近という条件を必ず併記した。年ごとの回数の変動は台本に入れていない。\n'
    '・動画では使っていないこと：皆既・部分・半影の区別、交点からの角度による分類、日食とのセット関係、NASAの図の転載。\n'
    '・図は自作の模式図です。実際の轨道や天体の写真ではありません。背景は FreeVideo(MiniMax H3)によるAI生成で、イメージです。\n'
)
if __name__ == '__main__':
    build('eclipse', '満月のたびに、月食が起きる？', '満月と月食', '起きません。満月＋交点付近', pron, scenes, bg, notes,
          bg_note='・動画内の図(比較・流れ・並び)は自作の模式図です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の月や地球の映像ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の月や地球の映像ではありません\n・図・表：自作の模式図',
          end_q='皆さんは、今夜の月が満月かどうか、確かめますか？',
          tags=['月食', '満月', '白道', '黄道', '交点', '国立天文台', '天文', '雑学', 'Shorts'])
    fv_prompts('eclipse', [
        'A full moon slowly emerging from thin clouds in a dark blue night sky, cold pale light, no text, no people, no buildings, no modern objects, the camera slowly pushing in.',
        'Two thin elliptical orbital rings crossing at a slight angle in dark empty space, glowing lines only, abstract schematic look, no text, no numbers, no people, no buildings, the camera slowly rotating.',
        'A small moon quietly entering the round shadow of the earth in dark space, faint reddish light, abstract schematic look, no text, no people, no buildings, no modern objects, the camera slowly pushing in.',
        'A full moon slowly sinking toward the horizon in a calm night sky with tiny stars, quiet blue light, no text, no people, no buildings, no modern objects, the camera fixed.',
    ])
