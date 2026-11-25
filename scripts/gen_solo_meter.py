"""単独Short：メートルの定義が三度替わった話(solo_meter_light)。
根拠は Wikipedia「History of the metre」と BIPM「metre」
(https://www.bipm.org/en/history-si/metre )。BIPM 本文は 2026年11月25日に bsk で確認済み。
1799年の測量と 0.197mm は二次資料のみで needs_research に残す。
nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
from solo_spec import build, T, fv_prompts

W = 'BIPM・メートルの歴史'
pron = {
    'ダンケルク': 'ダンケルク',
    'バルセロナ': 'バルセロナ',
    'イリジウム': 'イリジウム',
    '白金': 'ハッキン',
    '0.2ミリ': 'レイテンニミリ',
    '1ミリ': 'イチミリ',
}
scenes = [
    dict(text='定規の1ミリは、地球を測って決めました。でも、その決め方は、もう使われていません。基準は三度、替わりました。',
         big='地球から光へ', sub='一メートルの定義は三度替わった', src=W,
         viz=T(2.6, [('最初', '地球'), ('次', '金属'), ('今', '光')])),
    dict(text='一七九九年、ダンケルクからバルセロナまでを測り、白金の棒に刻みました。一八八九年、白金とイリジウムの国際原器ができました。',
         big='地球を棒に', sub='一七九九年に白金の棒／一八八九年に国際原器', src=W,
         viz=T(2.8, [('1799年', '白金の棒'), ('1889年', '国際原器'), ('材質', '白金＋イリジウム')])),
    dict(text='一九六〇年、基準は光の波に替わりました。一九八三年からは、光の速さで決めています。いまの定規は、ここに由来します。',
         big='光の波と速さ', sub='一九六〇年は波／一九八三年は光の速さ', src=W,
         viz=dict(type='compare', l_label='1960年', l_val='波の数', r_label='1983年', r_val='光の速さ')),
    dict(text='いまは、最初より約0.2ミリ短いとされます。基準は、間違いではなく、測り方で替わってきました。',
         big='替えたのは測り方', sub='より正確に測れる方法が出た', src=W,
         viz=T(2.8, [('最初', '地球'), ('途中', '金属'), ('今', '光')])),
]
bg = [
    '暗い背景で、青い地球がゆっくり回り、極から赤道へ向かう細い光の線が浮かぶ模式的な映像(人物なし・文字なし・建物なし)',
    '灰色の台の上に、角張った金属の棒が置かれ、横から冷たい光が当たってゆっくり輝く模式的な映像(人物なし・文字なし・刻印なし)',
    '暗い空間を一本の温かい色の光がまっすぐ進み、淡い縞模様が広がる模式的な映像(人物なし・文字なし・機械の表示なし)',
    '白い半透明の細長い板が静かに浮かび、その横を青い光が通り過ぎる模式的な映像(人物なし・文字なし・目盛りなし)',
]
notes = (
    '■ 2026年11月24日に Wikipedia「History of the metre」(https://en.wikipedia.org/wiki/History_of_the_metre )の本文を確認して作った整理です。\n'
    '・使った事実(同記事)：フランス革命期に、北極から赤道までの距離を一千万分の一とする長さとしてメートルが導入された。1799年にダンケルクからバルセロナまでの子午線の測量が完了し、白金の棒(メートル・デ・ザルシヴ)がprimary standardとされた。1889年に白金90パーセント・イリジウム10パーセントの国際原器が第1回CGPMで定められ、29本の写しが各国に配られた。1960年に第11回CGPMがクリプトン86の特定の遷移による光の波、1,650,763.73個分の長さで定義し直した。1983年に第17回CGPMが光の速さ299792458メートル毎秒と、その1/299792458秒で進む距離として定義した。現在のメートルは当初の定義より約0.197ミリ短いと同記事に記載がある。\n'
    '・言い過ぎを避けた点：「基準が間違っていた」とは言わず、より正確に測れる方法が出た、とした。この先メートルが替わるかどうかは断定していない。\n'
    '・動画では使っていないこと：一七九一年という年号(確認できた本文にないため)、研究者名、クリプトン86の波の正確な個数、光の速さの正確な数値。\n'
    '・一次確認(2026年11月24日)：BIPM「metre」(https://www.bipm.org/en/history-si/metre )で、1889年に第1回CGPMが白金とイリジウムの国際原器を認定したこと、1960年の第11回CGPMがクリプトン86の波の定義に替えたこと、1983年の第17回CGPM決議1が光の速さによる定義に替えたことを確認。決議原文は https://www.bipm.org/en/committees/cg/cgpm/11-1960/resolution-6 と https://www.bipm.org/en/committees/cg/cgpm/17-1983/resolution-1 。\n'
    '・未確認(続き)：1799年のダンケルク〜バルセロナの測量と、現在の定義が当初より約0.197ミリ短いという数値は、Wikipediaの記事で確認しただけで一次史料での照合は未実施で、公開前に照合する。\n'
    '・レビューで直した点：未実施。\n'
)
if __name__ == '__main__':
    build('meter_light', '一メートルは地球の長さで決まっていた？', '一メートルは地球の長さ?', '基準は三度、替わった',
          pron, scenes, bg, notes,
          bg_note='・動画内の図(比較・並び)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の地球・原器・光の映像ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の地球・原器・光の映像ではありません\n・図・表：自作',
          end_q='一メートルで、まず測りたいものは何ですか？',
          tags=['メートル', '計量', '単位', '科学', 'BIPM', '地球', '光の速さ', '雑学', 'Shorts'])
    fv_prompts('meter_light', [
        'A dark blue globe turning slowly, a thin glowing line running from the pole toward the equator, abstract schematic look, the camera slowly pushing in.',
        'A polished angular metal bar resting on a plain grey surface, cold light sliding along it, abstract schematic look, the camera slowly gliding sideways.',
        'A single warm colored beam travelling straight through a dark empty space, faint soft interference fringes spreading behind it, abstract schematic look, the camera slowly pushing in.',
        'A plain translucent white strip floating quietly, a cool blue light passing beside it, abstract schematic look, the camera slowly pushing in.',
    ])
