"""単独Short(江戸の暮らし)：江戸の人は、こたつで冬を越した？(solo_kotatsu)。根拠は日本語版Wikipedia「炬燵」(2026年11月15日に原文を確認。二次資料。記事は出典不十分と注記されている)。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
from solo_spec import build, T, fv_prompts
W = 'Wikipedia（炬燵）'
pron = {'こたつ': 'コタツ', 'こたつ弁慶': 'コタツベンケイ', '置きごたつ': 'オキゴタツ', '火鉢': 'ヒバチ', '亥の日': 'イノヒ', '町家': 'マチヤ', '武家': 'ブケ', '蔭凉軒日録': 'インリョウケンニチロク', '炭火': 'スミビ', '弁慶': 'ベンケイ'}
scenes = [
    dict(text='江戸の人は、こたつで冬を越した？ 答えは、はい。江戸時代には、炭火を使うこたつが、広まっていたとされています。',
         big='江戸にこたつはあった？', sub='答え：はい。江戸時代に広まっていたとされる', src=W,
         viz=T(2.6, [('よくある疑問', '江戸にこたつはあった？'), ('答え', 'はい、江戸時代に広まっていた'), ('熱源は', '炭火')])),
    dict(text='こたつの最古の記述は、室町時代の1490年ごろの、京都の記録にあります。江戸時代には、綿の布団が広まり、こたつも発達しました。',
         big='記述は1490年、普及は江戸', sub='綿の布団の普及は16世紀とされる', src=W,
         viz=T(2.8, [('1490年ごろ', '京都の記録にこたつの記述'), ('16世紀', '綿の布団が輸入された'), ('江戸時代以降', 'こたつが発達・普及した')])),
    dict(text='こたつは、家の中で使う、内向きの暖房でした。家では威張るのに、外では弱い人を、こたつ弁慶と呼びました。',
         big='家の中の暖房、こたつ弁慶', sub='家では強気で外では弱い人', src=W,
         viz=T(2.8, [('こたつは', '家の中で使う内向きの暖房'), ('家では威張る', '外では弱い人'), ('その呼び名', 'こたつ弁慶')])),
    dict(text='旧暦の10月の亥の日に、こたつを使い始める風習も、ありました。',
         big='亥の日にこたつ開き', sub='こたつ開きの風習', src=W,
         viz=T(2.8, [('いつ', '旧暦10月の亥の日'), ('何を', 'こたつを使い始める'), ('その風習', 'こたつ開き')])),
]
bg = ['江戸時代の畳の部屋で、布団をかけたこたつが、下からほんのり赤く光っている映像(人物なし・文字なし)', '古い陶器の火鉢で、灰の中の炭が赤く光り、鉄瓶から湯気が立っている映像(人物なし・手なし・文字なし)',
      '商家の畳の部屋で、引き出しのついた木の長火鉢の上で、鉄瓶が湯気を立てている映像(人物なし・手なし・文字なし)', '夕暮れの雪の中、古い木造の家の紙の窓から、暖かい明かりがもれている映像(人物なし・文字なし)']
notes = ('■ 日本語版Wikipedia「炬燵」(2026年11月15日に原文を確認)にもとづく整理です。二次資料で、記事自体も「出典が不十分」と注記されています。一次史料や書籍は読めていません。\n'
         '・こたつの歴史：1490年(延徳2年)10月の『蔭凉軒日録』の記述が最初で、15世紀末以降の京都での使用例が史料で確認できる。綿布や綿が輸入されたのは16世紀なので、今に伝わるこたつの普及は17世紀の江戸時代以降とする説(新穂栄蔵)がある。江戸時代中期には、熱源に火鉢を用いた置きごたつが広まった(同記事)。\n'
         '・こたつ弁慶：外では意気地がないが家庭の中では威張る人を「こたつ弁慶」と言う(同記事。越谷吾山『物類称呼』の記述にも触れている)。同記事は「寺院や武家では火鉢が客向け、こたつは家庭用」とも書くが、ChatGPTのレビューで裏付けが弱いとされたため、動画では「家の中で使う内向きの暖房」とだけ言った。\n'
         '・こたつ開き：同記事は、武家は亥の月亥の日に暖房具を出し、町家は第二の亥の日から火鉢やこたつを使い始めた、と書く。ChatGPTのレビューで、「2回目」の裏付けが弱く、旧暦10月を今の11月に単純には換算できないとされたため、動画では「旧暦10月の亥の日にこたつを使い始める風習があった」とだけ言った(福岡市博物館、国立国会図書館のレファレンス事例などが、旧暦10月の亥の日の炬燵開きを紹介しているとのこと。こちらでは未確認)。\n'
         '・言い過ぎを避けた点：「江戸時代の人はみなこたつを使った」とは言っていない。普及の時期は説による。\n'
         '・動画では使っていないこと：海外の類似の暖房器具(イランのコルシなど)、近代のこたつ(電気こたつ)、事故の危険、置きごたつの登場時期。\n'
         '・台本は、web版ChatGPTとGeminiのレビュー(2026年11月15日)を踏まえて、断定を弱め(「広まっていたとされる」)、1490年に「室町時代」を添え、火鉢との対比と「2回目の亥の日」を外しました。\n'
         '・未確認：一次史料や書籍での確認。\n')
if __name__ == '__main__':
    build('kotatsu', '江戸の人は、こたつで冬を越した？ 広まった時期と使い始めの日', '江戸の人は、こたつで冬を越した？', 'はい。江戸時代に広まっていた', pron, scenes, bg, notes,
          bg_note='・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の江戸時代の映像や、その時代の暖房器具の再現ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の江戸時代の映像ではありません\n・図・表：自作', end_q='皆さんの家では、こたつを、いつ出しますか？')
    fv_prompts('kotatsu', [
        'Interior of an old Edo-period Japanese room with tatami floor, a low wooden frame covered with a thick quilted futon (kotatsu) glowing faintly warm orange from underneath, a paper shoji window with snow falling outside, no people, no hands, no text, the camera slowly pushing in.',
        'Close-up of an old ceramic hibachi brazier filled with ash and glowing red charcoal, a black iron kettle steaming on a trivet beside it, warm dim light, steam rising slowly, no people, no hands, no text, the camera slowly pushing in.',
        'A wooden long brazier with small drawers in a plain Edo-period merchant house room with tatami, an iron kettle steaming on top, warm lamp light, no signboard, no writing, no people, no hands, no text, the camera slowly gliding sideways.',
        'Snow falling at dusk onto an old wooden Japanese house, warm light glowing through a paper window, quiet atmosphere, no power lines, no utility poles, no wires, no asphalt, no people, no text, the camera fixed.'],
        allow_buildings=True)
