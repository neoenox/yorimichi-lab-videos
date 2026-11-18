"""単独Short(一般題材)：江戸の長屋は本当に鍵をかけなかった？(solo_nagaya_kagi)。根拠はSUUMOジャーナル「落語に多い泥棒噺 江戸のセキュリティは『人力オートロック』が守っていた」(2013年6月20日、2026年11月12日に原文確認。深川江戸資料館の展示解説書などを参考資料に挙げる二次資料)。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
from solo_spec import build, T, fv_prompts
W = 'SUUMOジャーナル(2013年6月20日)'
pron = {'心張り棒': 'シンバリボウ', '木戸': 'キド', '夜四つ': 'ヨツ', '戸締まり': 'トジマリ', '見張り役': 'ミハリヤク'}
scenes = [
    dict(text='江戸の長屋は、本当に、鍵をかけなかったのでしょうか？ 答えは、心張り棒と、木戸の、二重の守りでした。',
         big='長屋は、鍵なし？', sub='答え：心張り棒と木戸の二重の守り', src=W,
         viz=T(2.6, [('よくある話', '長屋は鍵をかけない'), ('実際の戸締まり', '心張り棒'), ('夜の守り', '木戸')])),
    dict(text='戸締まりの基本は、心張り棒です。戸の内側にあてがう、つっかい棒で、家の中に人がいないと、使えません。',
         big='心張り棒は、内側から', sub='家に人がいないと使えない', src=W,
         viz=dict(type='compare', l_label='在宅のとき', l_val='棒で戸締まり', r_label='留守のとき', r_val='棒は使えない')),
    dict(text='昼間は、残る住人たちの目も、防犯の役割を果たしていました。夜は、町の入り口の、木戸が、夜四つ、今の夜10時ごろに閉まりました。',
         big='昼は住人、夜は木戸', sub='夜四つ(今の夜10時ごろ)に木戸が閉まる', src=W,
         viz=T(2.8, [('昼間', '残った住人の目'), ('夜', '夜四つに木戸を閉める'), ('夜四つ', '今の夜10時ごろ')])),
    dict(text='鍵だけに頼らず、近所の目と、木戸でも守る。それが、長屋の防犯でした。ただし、これは、解説記事をもとにした整理で、時代や長屋によって、違いはあったはずです。',
         big='鍵ではなく、仕組みで守る', sub='時代や長屋で違いはあったはず', src=W,
         viz=T(2.8, [('守っていたもの', '鍵ではなく近所と木戸'), ('この動画は', '解説記事をもとにした整理'), ('注意', '時代・長屋で差があった')])),
]
bg = ['鍵のない長屋の木の引き戸の戸口を、正面からゆっくり映す映像(人物なし・文字なし)', '戸の内側に、心張り棒の細い木の棒が斜めに立てかけられている映像(人物なし・手なし・文字なし)',
      '夕暮れの長屋の路地口で、木戸の扉がゆっくり閉まる映像(人物なし・手なし・文字なし)', '昼の長屋の路地で、向かい合う戸口と、干された洗濯物が風にゆれる映像(人物なし・文字なし)']
notes = ('■ 2026年11月12日に、SUUMOジャーナルの記事「落語に多い泥棒噺 江戸のセキュリティは『人力オートロック』が守っていた」(2013年6月20日、筆者：山本久美子。https://suumo.jp/journal/2013/06/20/45336/ )の原文を読んで作った整理です。記事は、深川江戸資料館の展示解説書などを参考資料に挙げている二次資料で、一次史料や学術書までは確認していません。\n'
         '・動画で使った内容(同記事)：落語に出てくる長屋の家には鍵がなく、戸の内側にあてがうつっかい棒の「心張り棒」で戸締まりをした。心張り棒は鍵と違い、家の中に人がいないと使えず、外出時は戸を開けたままになる(記事は落語「締め込み」の長屋を例にした説明。動画では「戸を開けたまま」とは言わず、「留守のときは棒で戸を押さえられない」と言い換えた)。昼間の防犯は、長屋に残っている人たちの目。夜間は、日の出(明六つ)から夜10時ごろ(夜四つ)までは開けている木戸を閉めて、不審者が入れないようにした。\n'
         '・言い過ぎを避けた点：「長屋では誰も鍵を使わなかった」「泥棒はいなかった」とは言っていない。時代、地域、長屋の種類や住人の暮らしぶりによって違いはあったはずです。\n'
         '・動画では使っていないこと：南京錠などが普及した時期、蔵や商家の錠前、町ごとの木戸番の細かい運用。\n'
         '・未確認：一次史料や、江戸の長屋の戸締まりを扱った学術書での確認。\n')
if __name__ == '__main__':
    build('nagaya_kagi', '江戸の長屋は、本当に鍵をかけなかった？ 心張り棒と木戸の戸締まり', '長屋は、鍵なし？', '心張り棒と木戸の二重の守り', pron, scenes, bg, notes,
          bg_note='・動画内の図(比較・表)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の江戸の長屋の映像ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の江戸の長屋の映像ではありません\n・図・表：自作', end_q='皆さんは、もし江戸の長屋に住んだら、この戸締まりで、安心して眠れますか？')
    fv_prompts('nagaya_kagi', [
        'The humble entrance of an Edo-period Japanese row house: a single plain wooden lattice sliding door with white paper panels in the upper half, a dirt-floor step in front, no lock, seen straight on in soft daylight, no people, no text, the camera slowly pushing in.',
        'Close-up inside an old Japanese wooden sliding door: a thin wooden bar leaning diagonally against the door to hold it shut, soft light, no hands, no people, no text, the camera slowly pushing in.',
        'Edo-period scene at dusk: a simple wooden gate with two plank doors at the mouth of a narrow earthen-floor alley between low wooden row houses, the doors slowly swing shut by themselves, no power lines, no utility poles, no wires, no asphalt, no tile-roofed modern houses, no people, no hands, no text, the camera fixed.',
        'Edo-period narrow earthen alley between low wooden row houses in daylight, plain wooden sliding doors facing each other across the dirt path, a communal well, cloth hanging on a bamboo pole swaying in the wind, no power lines, no utility poles, no wires, no asphalt, no manhole covers, no people, no text, the camera slowly gliding forward.'], allow_buildings=True)
