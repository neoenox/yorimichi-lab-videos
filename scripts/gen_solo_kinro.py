"""単独Short(一般題材・季節の祝日)：勤労感謝の日は、もともと何の日？(solo_kinro)。根拠は内閣府「国民の祝日について」(2026年11月15日に原文を確認:勤労感謝の日=11月23日、趣旨「勤労をたっとび、生産を祝い、国民たがいに感謝しあう」、祝日法=昭和23年法律第178号)と、新嘗祭を起源とする複数の解説(國學院大學の研究者の解説記事ほか。二次資料)。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
from solo_spec import build, T, fv_prompts
W = '内閣府(国民の祝日について)ほか'
pron = {'勅令': 'チョクレイ', '勤労感謝の日': 'キンロウカンシャノヒ', '新嘗祭': 'ニイナメサイ', '宮中': 'キュウチュウ', '祭祀': 'サイシ', '穀物': 'コクモツ', '戦前': 'センゼン', '趣旨': 'シュシ', '勤労': 'キンロウ', '祝日': 'シュクジツ', '供え': 'ソナエ', 'たっとび': 'タットビ'}
scenes = [
    dict(text='勤労感謝の日は、もともと、何の日？ 答えは、新嘗祭という、皇室の祭典の日です。',
         big='勤労感謝の日は、もともと？', sub='答え：新嘗祭という皇室の祭典の日', src=W,
         viz=T(2.6, [('11月23日は', '勤労感謝の日'), ('もともとは', '新嘗祭という皇室の祭典の日'), ('いまは', '国民の祝日')])),
    dict(text='新嘗祭は、その年の新しい穀物を、神々に供え、天皇自らも食べる、宮中の行事です。祝日法ができる前、11月23日は、勅令で休日とされた、この祭日でした。',
         big='祝日法の前の11月23日は祭日', sub='勅令で休日とされた新嘗祭の日', src=W,
         viz=T(2.8, [('新嘗祭とは', '新穀を神々に供える宮中の行事'), ('天皇が', '自らも食べて収穫に感謝する'), ('祝日法の前の11月23日', '勅令で休日とされた祭日')])),
    dict(text='1948年の7月に、国民の祝日に関する法律ができ、11月23日は、勤労感謝の日という、国民の祝日の一つになりました。',
         big='1948年7月に祝日法ができる', sub='11月23日は勤労感謝の日に', src=W,
         viz=T(2.8, [('1948年7月', '国民の祝日に関する法律ができる'), ('11月23日が', '勤労感謝の日になる'), ('制定時の祝日', '全部で九つだった')])),
    dict(text='その趣旨は、勤労をたっとび、生産を祝い、国民たがいに感謝しあうこと、と定められています。',
         big='趣旨は、勤労と生産への感謝', sub='内閣府が示す趣旨', src=W,
         viz=T(2.8, [('勤労を', 'たっとぶ'), ('生産を', '祝う'), ('国民たがいに', '感謝しあう')])),
]
bg = ['実りの季節の、黄金色の稲穂が、風にゆれる田んぼの映像(人物なし・文字なし)', '白い布の上に、稲穂とお米をのせた木の台が、静かな社殿の中に置かれている映像(人物なし・手なし・文字なし)',
      '刈り取った稲が、夕日の中で、稲架に干されている映像(人物なし・文字なし)', '湯気の立つ、炊きたての白いごはんが、木の机に置かれている映像(人物なし・手なし・文字なし)']
notes = ('■ 2026年11月15日に、内閣府「国民の祝日について」(https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html )の原文を確認し、新嘗祭を起源とする複数の解説記事(國學院大學の研究者の解説記事ほか。二次資料)で補った整理です。一次史料や書籍は読めていません。\n'
         '・内閣府：勤労感謝の日は11月23日。趣旨は「勤労をたっとび、生産を祝い、国民たがいに感謝しあう」。国民の祝日に関する法律は昭和23年(1948年)法律第178号。\n'
         '・内閣府「(参考情報)祝日法制定の経緯」(https://www8.cao.go.jp/chosei/shukujitsu/gaiyou/kaku/keii.html ):祝日法の制定前は、皇室の祭典の行われる日である「祭日」のうち、新嘗祭(11月23日)などが勅令で休日とされていた。祝日法は昭和23年(1948年)7月5日に成立し、7月20日に公布・施行された。制定時の「国民の祝日」は九つで、勤労感謝の日(11月23日)はその一つ。\n'
         '・新嘗祭の説明：天皇が新穀を神々に供え、自らも食する宮中の行事、という説明は、複数の解説記事(二次資料)による。\n'
         '・台本は、web版ChatGPTとGeminiのレビュー(2026年11月15日)を踏まえて、「祭祀」を「行事」に、「戦前」を「祝日法ができる前」に、祝日法の制定を「1948年の7月」に直しました。新嘗祭が名前を変えただけではない点は、動画では断定せず、「国民の祝日の一つになった」とだけ言っています。\n'
         '・言い過ぎを避けた点：11月23日に定まった経緯(旧暦の「二の卯の日」から明治期の改暦を経た)は、資料によって年などの細部が異なるため、動画では触れていない。GHQの政策との関係も、資料の確認が足りないため言っていない。\n'
         '・動画では使っていないこと：新嘗祭の古代からの歴史、各地の収穫祭、戦後の祝日制定の議論。\n'
         '・未確認：一次史料や書籍での確認。新嘗祭の説明は二次資料による。\n')
if __name__ == '__main__':
    build('kinro', '勤労感謝の日は、もともと何の日？ 内閣府の趣旨と由来', '勤労感謝の日は、もともと？', '新嘗祭という皇室の祭典の日', pron, scenes, bg, notes,
          bg_note='・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の祭祀や行事の映像ではありません。\n',
          credit='・出典：内閣府「国民の祝日について」ほか\n・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の祭祀や行事の映像ではありません\n・図・表：自作', end_q='皆さんは、今年、誰に感謝を伝えたいですか？')
    fv_prompts('kinro', [
        'A golden rice field at harvest time, heavy ripe rice ears swaying gently in the autumn wind under soft afternoon light, no people, no text, the camera slowly gliding forward.',
        'Inside a quiet Shinto shrine hall, a plain wooden offering stand holding rice ears and a small mound of rice on a white cloth, soft warm light, no people, no hands, no text, no inscription, no signboard, the camera slowly pushing in.',
        'Harvested rice sheaves hanging to dry on wooden poles in a field at sunset, warm orange light, no power lines, no utility poles, no wires, no people, no text, the camera fixed.',
        'A bowl of freshly cooked white rice steaming gently on a wooden table, warm soft light, steam rising slowly, no people, no hands, no text, the camera slowly pushing in.'],
        allow_buildings=True)
