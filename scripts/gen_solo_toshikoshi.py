"""単独Short(一般題材・年末の風習)：年越しそばは、いつから食べられている？(solo_toshikoshi)。根拠は日本語版Wikipedia「年越し蕎麦」(2026年11月14日に原文を確認。二次資料。記事の一部の節は出典不十分と注記されている)。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
from solo_spec import build, T, fv_prompts
W = 'Wikipedia（年越し蕎麦）'
pron = {'年越しそば': 'トシコシソバ', '三十日そば': 'ミソカソバ', 'みそかそば': 'ミソカソバ', '晦日': 'ミソカ', '大みそか': 'オオミソカ', '大坂': 'オオサカ', '商家': 'ショウカ', '末日': 'マツジツ', '記述': 'キジュツ', '由来': 'ユライ', '諸説': 'ショセツ', '定着': 'テイチャク', '災厄': 'サイヤク', '長寿': 'チョウジュ', '年越しうどん': 'トシコシウドン', '香川県': 'カガワケン'}
scenes = [
    dict(text='年越しそばは、いつから、食べられているのでしょうか。答えは、少なくとも、江戸時代には、広まっていました。',
         big='年越しそばは、いつから？', sub='答え：少なくとも江戸時代には広まっていた', src=W,
         viz=T(2.6, [('よくある疑問', '年越しそばはいつから？'), ('答え', '少なくとも江戸時代には広まっていた'), ('由来', '諸説ある')])),
    dict(text='江戸時代中期の商家には、月の末日にそばを食べる、みそかそばの習慣があり、これが、大みそかだけに行われるようになったと、考えられています。',
         big='月末のみそかそばが始まり', sub='大みそかだけに転じたと考えられる', src=W,
         viz=T(2.8, [('江戸時代中期', '商家にみそかそばの習慣'), ('月の末日に', 'そばを食べていた'), ('転じて', '大みそかだけの年越しそばに')])),
    dict(text='1814年に書かれた、大坂の記録には、年末の晦日に、みんなでそばを食べる、という記述があります。由来には、細く長いから長寿、切れやすいから災厄を断つ、など、諸説あります。',
         big='1814年の大坂の記録に記述', sub='由来には諸説ある', src=W,
         viz=T(2.8, [('1814年', '大坂の記録に年末のそばの記述'), ('細く長い', '長寿を願う説'), ('切れやすい', '災厄を断つ説')])),
    dict(text='いまも、地域によって違い、香川県では、年越しうどんを食べる家庭もあります。2010年の香川県での調査では、年越しそばが43パーセント、年越しうどんが22パーセントでした。',
         big='香川では年越しうどんも', sub='2010年の香川県の調査:そば43%・うどん22%', src=W,
         viz=dict(type='compare', l_label='年越しそば', l_val='43%', r_label='年越しうどん', r_val='22%')),
]
bg = ['雪の降る夜、湯気の立つ、そばの器が、木の机に置かれている映像(人物なし・手なし・文字なし)', '江戸時代の商家の入り口で、無地の藍色の暖簾が、ゆっくり風にゆれる映像(人物なし・文字なし)',
      '粉をふった木の板の上に、切りそろえた細長いそばが、並んでいる映像(人物なし・手なし・文字なし)', 'そばの器とうどんの器が、並んで湯気を立てている映像(人物なし・手なし・文字なし)']
notes = ('■ 日本語版Wikipedia「年越し蕎麦」(2026年11月14日に原文を確認)にもとづく整理です。二次資料で、一次史料や書籍は読めていません。記事の「各地の年越し蕎麦と例外」の節は、出典が不十分と注記されています。\n'
         '・江戸時代：年越しそばは江戸時代には定着した文化とされる。江戸時代後期の1814年(文化11年)の『大坂繁花風土記』に「十二月三十一日 晦日そばとて、皆々そば切をくろふ」の記述があり、遅くとも同年には大阪で年中行事として定着していたことが窺える(同記事)。\n'
         '・起源：江戸時代中期には商家に月の末日にそばを食べる三十日蕎麦(みそかそば)の習慣があり、これが転じて大晦日だけの年越し蕎麦になったと考えられている(同)。\n'
         '・由来：細く長いから延命・長寿を願う説、切れやすいから一年の災厄や苦労・借金を断つ説など、諸説ある(同)。動画では二つだけ紹介した。\n'
         '・香川：香川県には「年越しうどん」の習慣がある。四国学院大学の調査(2010年)では、年越しそば43%に対し、年越しうどんは22%(同)。動画では「2010年の香川県での調査」と表現した(出典の記事名は「香川でも年越し蕎麦派がうどんを圧倒 四国学院大学のゼミ生が調査」)。調査の方法は確認していない。そばとうどんの両方を食べた人もいる可能性があり、43%と22%を足して全体と見ることはできない。\n'
         '・1814年の記述：Wikipediaが引く『大坂繁花風土記』の文言は旧暦の日付を含み、動画では日付を言わず「年末の晦日(みそか)」と表現した。同書には、その月の節分に年越しそばを食べる旨の記述も含まれる(Wikipediaの引用)。\n'
         '・台本は、web版ChatGPTとGeminiのレビュー(2026年11月14日)を踏まえて、「少なくとも江戸時代には広まっていた」、1814年の記述の言い方、調査の年と対象の明示に直しました。\n'
         '・言い過ぎを避けた点：由来を一つに断定していない。「江戸時代に定着」は、1814年の大坂の記述などからの推定を含む。\n'
         '・動画では使っていないこと：謝国明の世直しそば(鎌倉時代)の伝承、金銀細工師の説、年を越して食べると縁起が悪いなどの伝承、薬味のネギの意味。\n'
         '・未確認：一次史料や書籍での確認。調査の詳細。\n')
if __name__ == '__main__':
    build('toshikoshi', '年越しそばは、いつから食べられている？ 江戸の記録と由来', '年越しそばは、いつから？', '少なくとも江戸時代には広まっていた', pron, scenes, bg, notes,
          bg_note='・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の江戸時代の映像や、その時代の食事の再現ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の江戸時代の映像ではありません\n・図・表：自作', end_q='皆さんの家では、大みそかに、何を食べますか？')
    fv_prompts('toshikoshi', [
        'A steaming bowl of soba noodles with sliced green onion on a wooden table at night, soft warm light, gentle snowfall visible through a paper window behind, steam rising slowly, no people, no hands, no text, the camera slowly pushing in.',
        'The entrance of an old Edo-period wooden merchant house with a plain indigo noren curtain with no writing swaying gently in the wind, earthen floor visible inside, soft daylight, no power lines, no utility poles, no wires, no asphalt, no people, no text, the camera fixed.',
        'Thin cut buckwheat soba noodles neatly laid out on a flour-dusted wooden board, a long flat knife resting beside them, soft window light, no people, no hands, no text, the camera slowly gliding across.',
        'Two ceramic bowls side by side on a wooden table steaming gently, one with thin brown soba noodles and one with thick white udon noodles, warm light, no people, no hands, no text, the camera slowly pushing in.'],
        allow_buildings=True)
