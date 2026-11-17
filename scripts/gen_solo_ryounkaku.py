"""単独Short(歴史／明治)：明治の浅草に12階建てはあった？(solo_ryounkaku)。根拠は国立科学博物館「理工電子資料館 大日本凌雲閣之圖」(2026年11月17日に原文を確認 https://www.kahaku.go.jp/exhibitions/vm/past_parmanent/rikou/other/ryounkaku.html )。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。
Ask Studio(2026-11-17)の実測「離脱は0〜3秒ではなく4〜7秒」を受け、4〜6秒目に数字(1890年・12階)を置く構成にした。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solo_spec import build, T, fv_prompts
W = '国立科学博物館「大日本凌雲閣之圖」'
pron = {'凌雲閣': 'リョウウンカク', '浅草': 'アサクサ', 'バルトン': 'バルトン', 'アーク灯': 'アークトウ',
        '関東大震災': 'カントウダイシンサイ', '爆破': 'バクハ', '展望台': 'テンボウダイ'}
scenes = [
    dict(text='明治の浅草に、12階建てはあった？ ありました。1890年11月、凌雲閣が開業。エレベーターは、8階まで。',
         big='1890年、12階建て', sub='浅草に凌雲閣が開業', src=W,
         viz=T(2.6, [('年', '1890年11月'), ('階数', '12階建て'), ('エレベーター', '8階まで')])),
    dict(text='設計は英国人バルトン。工事は、日本人の手で行われました。',
         big='設計は英国人、施工は日本', sub='ウィリアム・K・バルトン', src=W,
         viz=T(2.8, [('設計', 'ウィリアム・K・バルトン'), ('施工', '日本人の手で'), ('呼び名', '浅草十二階')])),
    dict(text='外にはアーク灯、中には電灯。電気の明かりが珍しかった時代です。屋上の展望台からの眺めで、東京の名所になりました。',
         big='電気の灯りに、展望台', sub='屋外はアーク灯、室内は電灯', src=W,
         viz=T(2.8, [('屋外', 'アーク灯'), ('室内', '電灯'), ('屋上', '展望台で名所に')])),
    dict(text='1923年の関東大震災で上部が倒壊。その後、爆破解体され、今は残っていません。2026年11月17日時点の情報です。',
         big='震災で倒れ、解体', sub='1923年、関東大震災', src=W,
         viz=T(2.8, [('1923年', '関東大震災'), ('上部', '倒壊'), ('その後', '爆破解体')])),
]
bg = ['明治の低い町並みの上に、12階建ての高い塔がそびえる映像(人物なし・文字なし)',
      '高い塔の中の、鉄の籠のエレベーター(人物なし・手なし・文字なし)',
      '夜の塔に、窓の電気の明かりと、外のアーク灯が輝く映像(人物なし・文字なし)',
      '上部が崩れ、瓦礫が積もった塔の映像(人物なし・文字なし)']
notes = ('■ 2026年11月17日に、国立科学博物館「理工電子資料館 大日本凌雲閣之圖」(https://www.kahaku.go.jp/exhibitions/vm/past_parmanent/rikou/other/ryounkaku.html )を読んで作った整理です。2026年11月17日時点の情報です。\n'
         '・使った事実(同)：1890(明治23)年11月、東京の浅草に12階建ての「凌雲閣」がオープン。設計者は英国人ウィリアム・K・バルトンで、工事は日本人の手で行なわれた。開館当初は東京電燈株式会社によるエレベーターが8階まで設置され、屋外にアーク灯が、室内に電灯が灯され、その賑やかな様子や展望台からの眺望で東京名所の一つとなった。凌雲閣は1923年の関東大震災により上部が倒壊したため、その後爆破解体された。\n'
         '・言い過ぎを避けた点：「8階まで」はエレベーターの設置階であって、12階まで昇れたわけではない。高さ(約52mとされることがある)は資料に記載がないため使っていない。「富士山が見えた」も資料に無いため使っていない。「浅草十二階」の通称は資料の表題と「12階建て」から補った呼び名で、動画では小見出しに置いた。\n'
         '・Ask Studio(2026-11-17)の実測メモ：離脱は0〜3秒ではなく4〜7秒に集中(例:105%→66%)。高パフォーマンス動画はスワイプ72〜77%、低は81〜82%。対策として、4〜6秒目に数字や結論の断片を置く。この台本は、場面1の冒頭2文で問いと答え、その直後(おおよそ4〜6秒)に「1890年11月」「8階まで」の数字を置いた。\n'
         '・未確認：凌雲閣の正確な高さ、入場料、エレベーターのメーカー、倒壊後の解体時期の詳細。\n'
         '・背景の映像はAI生成で、実際の凌雲閣の写真ではない(イメージです)。\n')
if __name__ == '__main__':
    build('ryounkaku', '明治の浅草に、12階建てはあった？ 凌雲閣とエレベーター', '浅草十二階', '1890年、浅草に12階建ての凌雲閣', pron, scenes, bg, notes,
          bg_note='・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の凌雲閣の写真ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の凌雲閣の写真ではありません\n・図・表：自作',
          end_q='初めてエレベーターに乗ったとき、覚えていますか？',
          tags=['凌雲閣', '浅草十二階', '明治', '浅草', 'エレベーター', '国立科学博物館', '歴史', '雑学', 'Shorts'])
    fv_prompts('ryounkaku', [
        'A tall octagonal brick tower, twelve tiers of western-style balconies with brickwork, rising above low tiled wooden rooftops of a Meiji-era Japanese town, seen from a distance in late afternoon light, no people, no text, the camera slowly moving sideways.',
        'Inside an old iron elevator cage with lattice doors in a tall brick tower, brass fittings, warm dim light from above, no people, hands, or text, the camera slowly pushing in.',
        'Close view of arched windows on the upper facade of a tall brick tower at night, warm electric light glowing inside the windows, dark blue sky, brick texture filling the frame, no people, no text, the camera slowly tilting up.',
        'A tall brick tower whose upper tiers have collapsed, broken bricks and rubble at the base, pale overcast sky, no people, no text, the camera slowly moving forward.'],
        allow_buildings=True)
