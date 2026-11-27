"""単独Short(一般題材・季節)：日の入りが一番早いのは冬至？(solo_toji)。根拠は国立天文台 暦計算室の暦要項(令和8年(2026)・令和9年(2027)「東京の日出入」「二十四節気および雑節」。2026年11月14日に原文を取得して確認)。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
from solo_spec import build, T, fv_prompts
W = '国立天文台 暦要項(東京の日出入)'
pron = {'冬至': 'トウジ', '国立天文台': 'コクリツテンモンダイ', '日の入り': 'ヒノイリ', '日の出': 'ヒノデ', '東京': 'トウキョウ'}
scenes = [
    dict(text='東京で、日の入りがいちばん早い日は、冬至でしょうか？ 答えは、いいえ。冬至より前の、12月上旬です。',
         big='日の入り最早は、冬至？', sub='答え：冬至より前の12月上旬', src=W,
         viz=T(2.6, [('よくある思い込み', '冬至に日の入りが最も早い'), ('東京の表では', '12月上旬が最も早い'), ('冬至', '2026年12月22日')])),
    dict(text='国立天文台の、東京の表です。2026年11月27日は、午後4時29分。12月7日は、午後4時28分。12月17日は、午後4時30分。この表では、12月7日が、いちばん早い日の入りです。',
         big='日の入りは12月7日が最も早い', sub='2026年の表(10日ごと)', src=W,
         viz=T(2.8, [('2026年11月27日', '日の入り16時29分'), ('2026年12月7日', '16時28分(表で最も早い)'), ('2026年12月17日', '日の入り16時30分')])),
    dict(text='冬至は、2026年12月22日。その5日後の12月27日には、日の入りは、午後4時35分まで、遅くなっています。',
         big='冬至のころは、もう遅くなる', sub='日の入りは冬至より前が最も早い', src=W,
         viz=dict(type='compare', l_label='2026年12月7日', l_val='16時28分', r_label='2026年12月27日', r_val='16時35分')),
    dict(text='逆に、日の出がいちばん遅いのは、冬至の後。2027年の表では、1月11日の、午前6時51分です。夕方が暗くなる時期と、朝が明るくなる時期は、ずれているのです。',
         big='日の出最遅は、冬至の後', sub='2027年の表では1月11日が6時51分', src=W,
         viz=T(2.8, [('日の入りが最も早い', '冬至より前(12月上旬)'), ('日の出が最も遅い', '冬至より後(1月)'), ('2027年1月11日', '日の出6時51分')])),
]
bg = ['冬の澄んだ空の水平線に、夕日がゆっくり沈んでいく映像(人物なし・文字なし)', '冬の野原の向こうの山並みに、太陽がゆっくり沈んでいく映像(人物なし・文字なし)',
      '夕方の低い日差しで、霜の降りた野原に、長い影がのびている映像(人物なし・文字なし)', '冬の朝、うす暗い水平線から、太陽がゆっくりのぼってくる映像(人物なし・文字なし)']
notes = ('■ 2026年11月14日に、国立天文台 暦計算室の暦要項の原文を取得して確認した整理です(日付と時刻は同ページの表のとおり)。\n'
         '・令和8年(2026)暦要項「東京の日出入」(https://eco.mtk.nao.ac.jp/koyomi/yoko/2026/rekiyou264.html ):日入は 2026年11月27日16時29分、12月7日16時28分、12月17日16時30分、12月27日16時35分(中央標準時、10日ごとの表)。\n'
         '・同「二十四節気および雑節」(https://eco.mtk.nao.ac.jp/koyomi/yoko/2026/rekiyou262.html ):冬至は2026年12月22日5時50分。\n'
         '・令和9年(2027)暦要項「東京の日出入」(https://eco.mtk.nao.ac.jp/koyomi/yoko/2027/rekiyou274.html ):日出は 2027年1月1日6時50分、1月11日6時51分、1月21日6時48分(10日ごとの表では1月11日が最も遅い)。\n'
         '・言い過ぎを避けた点:表は10日おきなので、「日の入りが最も早い日」を1日に特定してはいません(「表では12月7日が最も早い」と表現)。場所によって日付や時刻は少し違います。動画の数字は東京のものです。\n'
         '・動画では使っていないこと:この現象の理由(太陽が真南に来る時刻が日ごとにずれる「均時差」と説明される)、冬至当日の日の入りの時刻、東京以外の都市。\n'
         '・未確認:「最も早い日」を1日単位で示す資料での確認。\n')
if __name__ == '__main__':
    build('toji', '日の入りが一番早い日は、冬至？ 国立天文台の東京の表で確かめる', '日の入りが最も早い日は？', '冬至より前の12月上旬', pron, scenes, bg, notes,
          bg_note='・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の風景ではありません。\n',
          credit='・出典：国立天文台 暦計算室「暦要項」(令和8年・令和9年)\n・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の風景ではありません\n・図・表：自作', end_q='皆さんは、冬至が、いちばん早く日が沈む日だと、思っていましたか？')
    fv_prompts('toji', [
        'A calm winter horizon at sunset, a large orange sun slowly sinking toward a still sea, clear pale sky, gentle reflections on the water, no people, no text, the camera fixed.',
        'A winter landscape of bare fields and a distant mountain ridge, the sun slowly sinking behind the ridge with a warm orange glow, thin clouds, no people, no text, the camera fixed.',
        'Late afternoon winter light over a frosty open field, long shadows of grass stretching across the white frost, the low sun glowing near the horizon, no people, no text, the camera slowly gliding forward.',
        'A cold winter morning, a pale sun slowly rising above a misty horizon, soft pink and gold sky, quiet scene, no people, no text, the camera fixed.'])
