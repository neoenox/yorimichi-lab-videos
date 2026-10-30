"""Short用の spec その5：brain10。台本は長尺の 09_script_v2.md の文言に合わせる（数字・限定・帰属を変えない）。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
CREDIT = '・イラスト：ChatGPT(OpenAI)による生成イラスト（イメージです。実在の場面・人物・資料の再現ではありません）\n・図・表：自作'


def J(n, o):
    (R / 'data' / f'short_{n}.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')


J('brain10', dict(
    title='人は、脳の10%しか使っていない？', long_id='c_pVVpkjHh4',
    long_title='人は、脳の10%しか使っていない？ 原文と脳の研究で確かめる',
    pron='data/brain10_pronunciations.json', art='assets/brain10/art_intro.png',
    hook='「人は、脳の10%しか使っていない」と聞いたことはありませんか。ジェームズの原文と、脳の研究で確かめます。',
    notes='■ 動画で確かめたこと\n・ジェームズ『人間のエネルギー』(1907年)の原文に、「10%」という数字は出てきません。書かれているのは、人の力や能力の話です(Wikisource版で確認)。\n・脳の損傷では、10%よりずっと小さい範囲でも、重い影響が出ることがあります(Beyerstein, 2004)。\n・脳画像でも、新しい役割を待つ静かな領域は見つかっていません。\n・脳は体重の約2%で、体の酸素とカロリーの約20%を使います(Raichle & Gusnard, 2002)。\n・1936年のカーネギーの本の序文の原文は、確認していません。出典は本編の概要欄にまとめています。',
    credit=CREDIT, answer='「10%」は、原文にない',
    scenes=[
        dict(text='人は、脳の十パーセントしか使っていない。残りを使えたら、天才になれる。そう聞いたことはありませんか。', big='脳の10%しか使ってない？', art='assets/brain10/art_intro.png'),
        dict(text='発端としてよく挙げられるのが、心理学者ジェームズの、一九〇七年の論文です。原文を確認すると、そこに、十パーセントという数字は、出てきません。', big='原文に「10%」はない', src='ジェームズ「人間のエネルギー」(1907)', art='assets/brain10/art_study.png', col='white'),
        dict(text='脳の、十パーセントよりずっと小さい範囲が傷つくだけでも、重い影響が出ることがあります。', big='小さな損傷でも、重い影響', src='Beyerstein (2004)', art='assets/brain10/art_clinic.png'),
        dict(text='脳の画像でも、新しい役割を待っている、静かな領域は、見つかっていません。', big='眠っている領域は、見つかっていない', src='Beyerstein (2004)', art='assets/brain10/art_scan.png', col='white'),
        dict(text='脳は、体重の約二パーセントで、体が使う酸素と、カロリーの、約二十パーセントを使います。', big='体重2％、エネルギー20％', sub='どちらも約。体の酸素とカロリーのうち', src='Raichle & Gusnard (2002)', art='assets/brain10/art_lamp.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/brain10/art_intro.png')]))

J('jikyu', dict(
    title='食料自給率37％、残り63％は輸入？', long_id='JJ7XlklBau0',
    long_title='日本の食料自給率37％なら、食べ物の63％は輸入？ 農林水産省の資料で確かめる',
    pron='data/jikyu_pronunciations.json', art='assets/jikyu/art_intro.png',
    hook='「食料自給率は37％。食べ物の63％は輸入」と聞いたことはありませんか。農林水産省の資料で確かめます。',
    notes='■ 動画で確かめたこと\n・農林水産省は、令和7年度（概算）の供給熱量を、国産37％・輸入63％と示しています。\n・輸入した飼料で国内で育てた畜産物は、自給率では国産に数えません。卵は、自給率11％、食料国産率97％です。\n・国産率(1,040kcal)と自給率(830kcal)の差210kcalは、輸入飼料の畜産物の分で、総供給熱量2,237kcalの約9％です(自作の計算)。国内で作られていない輸入の食料は、約54％です(自作の計算)。\n・令和7年度の数字は概算です。出典は本編の概要欄にまとめています。',
    credit=CREDIT, answer='63％＝輸入の食料 約54％＋輸入飼料の畜産物 約9％',
    scenes=[
        dict(text='食料自給率は、三十七パーセント。では、食べ物の六十三パーセントは、輸入なのでしょうか。', big='63％は、輸入？', art='assets/jikyu/art_intro.png'),
        dict(text='農林水産省も、国産三十七、輸入六十三、と示しています。', big='農水省も「輸入63％」と表示', src='農林水産省（令和7年度・概算）', art='assets/jikyu/art_desk.png', col='white'),
        dict(text='ただし、輸入した飼料で、国内で育てた畜産物は、自給率では、国産に数えません。', big='輸入飼料の畜産物は、国産に入れない', src='農林水産省', art='assets/jikyu/art_farm.png'),
        dict(text='たとえば卵は、自給率が十一パーセント。ところが、食料国産率は、九十七パーセントです。', big='卵：自給率11％、国産率97％', src='農林水産省', art='assets/jikyu/art_kitchen.png', col='white'),
        dict(text='六十三パーセントの内訳は、二つです。輸入された食料が、全体の約五十四パーセント。輸入飼料で育てた畜産物が、全体の約九パーセントです。', big='63％＝約54％＋約9％', sub='公表値からの自作の計算', art='assets/jikyu/art_ship.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/jikyu/art_harbor.png')]))

J('bukka', dict(
    title='物価2％上昇、どの家庭も2％増える？', long_id='qzxzekd5j-I',
    long_title='物価が2％上がったら、どの家庭の生活費も2％増える？ 総務省の統計で確かめる',
    pron='data/bukka_pronunciations.json', art='assets/bukka/art_intro.png',
    hook='「物価が2％上がった」と聞いたことはありませんか。どの家庭でも、生活費が2％増えるのでしょうか。総務省の統計で確かめます。',
    notes='■ 動画で確かめたこと\n・2025年の全国の消費者物価は、前年より3.2％上昇でした(総務省)。\n・二人以上の世帯のうち勤労者世帯を、年収の低い順に5つに分けると、2025年の上昇率は、最も低い層3.3％、最も高い層2.7％でした(差0.6ポイント)。\n・差の理由として、食料などの買い物かごの中身の違いが考えられます。食料の寄与の差は約0.36ポイントと近似できます(自作の近似計算)。\n・内閣府の試算では、2021年からの5年間で3％程度の差があります。総務省の指数とは、方法や期間が違い、そのまま比べられません。出典は本編の概要欄にまとめています。',
    credit=CREDIT, answer='どの家庭も同じではない。ただし、差は小さい',
    scenes=[
        dict(text='物価が二パーセント上がった。そう聞くと、どの家庭でも、生活費が二パーセント増える、と思うかもしれません。', big='物価2％上昇＝生活費も2％増？', art='assets/bukka/art_intro.png'),
        dict(text='二〇二五年の全国の消費者物価は、前の年より、三・二パーセント上がりました。', big='2025年：全国で3.2％上昇', src='総務省', art='assets/bukka/art_office.png', col='white'),
        dict(text='二人以上の勤労者世帯を、年収の低い順に五つに分けて見ます。最も低い五分の一の世帯は、三・三パーセント。', big='年収が最も低い層：3.3％', src='総務省（2025年・勤労者世帯）', art='assets/bukka/art_shop.png'),
        dict(text='最も高い五分の一の世帯は、二・七パーセントです。差は、〇・六ポイントです。', big='最も高い層：2.7％（差0.6ポイント）', src='総務省（2025年・勤労者世帯）', art='assets/bukka/art_home.png', col='white'),
        dict(text='差の理由として、食料など、買い物かごの中身の違いが、考えられます。ただし、差は、思ったより小さいものでした。', big='差は、かごの中身の違い。ただし小さい', art='assets/bukka/art_wallet.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/bukka/art_intro.png')]))

J('galileo', dict(
    title='「それでも地球は動く」は本当？', long_id='nVHHuD3khZ8',
    long_title='ガリレオは「それでも地球は動く」と言った？ 最古の記録を確かめる',
    pron='data/galileo_pronunciations.json', art='assets/galileo/art_intro.png',
    hook='「それでも地球は動く」。ガリレオが裁判のあとにつぶやいた、という有名な言葉を、確かめます。',
    notes='■ 動画で確かめたこと\n・ガリレオが、1633年に異端の疑いで裁判にかけられ、地動説を撤回させられたことは、歴史の解説で述べられています。\n・「それでも地球は動く」が、印刷物で確認されている最も古い例は、1757年のバレッティ『The Italian Library』で、ガリレオの死(1642年)から100年以上あとです。\n・弟子ヴィヴィアーニの最初の伝記や、裁判の記録には、この言葉はないとされます。\n・天文学者リビオは、後の時代の作り話の可能性が高いとしつつ、実際に言ったかどうかは確実ではない、と述べています。\n・原典(バレッティの本文など)は確認していません。出典は本編の概要欄にまとめています。',
    credit=CREDIT, answer='同時代の証拠は見つかっていない',
    scenes=[
        dict(text='「それでも地球は動く」。ガリレオが、裁判のあとに、そうつぶやいた。そんな話を、聞いたことはありませんか。', big='「それでも地球は動く」', art='assets/galileo/art_intro.png'),
        dict(text='ガリレオが、異端の疑いで裁判にかけられ、地動説を撤回させられたことは、歴史の解説で述べられています。', big='裁判で、地動説を撤回させられた', src='Scientific American / Wikipedia', art='assets/galileo/art_hall.png', col='white'),
        dict(text='ところが、このつぶやきを、ガリレオの時代の記録として示すものは、見つかっていません。', big='同時代の証拠は、見つかっていない', art='assets/galileo/art_books.png'),
        dict(text='印刷物で確認されている最も古い例は、一七五七年。ガリレオの死から、百年以上あとの本です。', big='最古の例は、1757年（死後100年以上）', src='Wikipedia', art='assets/galileo/art_sky.png', col='white'),
        dict(text='言った証拠がないことと、言わなかった証拠があることは、別です。確実なことは、分かっていません。', big='「証拠がない」≠「言わなかった」', art='assets/galileo/art_gallery.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/galileo/art_intro.png')]))

J('takarakuji', dict(
    title='宝くじ、何割が当せん金？', long_id='L2R4JsyMp8I',
    long_title='宝くじは、買ったお金の何割が当せん金になる？ 公式サイトの数字で確かめる',
    pron='data/takarakuji_pronunciations.json', art='assets/takarakuji/art_intro.png',
    hook='宝くじを買うとき、買ったお金の何割が、当せん金として払われているのでしょうか。公式サイトの数字で確かめます。',
    notes='■ 動画で確かめたこと\n・令和6年度の販売実績額は7,598億円。当せん金は3,529億円(46.5％)、収益金は2,750億円(36.2％)、経費は1,218億円(16.0％)、社会貢献広報費は101億円(1.3％)でした(宝くじ公式サイト)。\n・百円あたりに直すと、当せん金は約46円です(自作の換算)。\n・これは全体の割合で、一人ひとりに戻る額ではありません。商品ごとの割合は確認していません。買うことをすすめる・止める動画ではありません。出典は本編の概要欄にまとめています。',
    credit=CREDIT, answer='全体で46.5％。百円につき約46円',
    scenes=[
        dict(text='宝くじを買うとき、買ったお金の、何割が、当せん金として、払われているのでしょうか。', big='買ったお金の何割が、当せん金？', art='assets/takarakuji/art_intro.png'),
        dict(text='宝くじ公式サイトによると、令和六年度の販売実績額は、七千五百九十八億円です。', big='令和6年度：販売実績額 7,598億円', src='宝くじ公式サイト', art='assets/takarakuji/art_counter.png', col='white'),
        dict(text='このうち、当せん金は、三千五百二十九億円。公式の表記で、四十六・五パーセントです。', big='当せん金：46.5％', src='宝くじ公式サイト（令和6年度）', art='assets/takarakuji/art_coins.png'),
        dict(text='収益金は三十六・二パーセント、経費は十六・〇パーセントです。百円につき、当せん金は、約四十六円です。', big='百円につき、当せん金は約46円', src='宝くじ公式サイト（令和6年度）', art='assets/takarakuji/art_city.png', col='white'),
        dict(text='ただし、これは全体の割合です。一人ひとりに、いくら戻るかは、運で決まります。', big='全体の割合。一人ひとりの結果は別', art='assets/takarakuji/art_coins.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/takarakuji/art_intro.png')]))

J('shinkansen', dict(
    title='新幹線の遅れ、平均で何秒？', long_id='gNGUPpg4wQM',
    long_title='新幹線の遅延は、平均で何秒？ JR東海の資料と記事で確かめる',
    pron='data/shinkansen_pronunciations.json', art='assets/shinkansen/art_intro.png',
    hook='新幹線の遅れは、平均で、何秒なのでしょうか。JR東海の資料と、記事の数字で確かめます。',
    notes='■ 動画で確かめたこと\n・JR東海は、東海道新幹線の2024年度の平均遅延時分を、運行1列車あたり1.4分(84秒)と示しています。自然災害等による遅延も含みます(JR東海)。\n・2016年度は24秒と、報道記事で紹介されています(二次情報。原本は未確認)。\n・年度で数字は動きます。2つの数字だけで、3.5倍悪くなったとは言えません。\n・平均は、一本ごとの遅れを示すものではありません。遅延の定義や途中の年度は確かめきれていません。出典は本編の概要欄にまとめています。',
    credit=CREDIT, answer='年度で違う。2016年度は24秒、2024年度は84秒',
    scenes=[
        dict(text='新幹線の遅れは、平均で、何秒なのでしょうか。「数十秒」と聞いたことは、ありませんか。', big='新幹線の遅れは、平均で何秒？', art='assets/shinkansen/art_intro.png'),
        dict(text='JR東海の資料では、二〇二四年度の平均遅延時分は、運行一列車あたり、一・四分です。', big='2024年度：1.4分（84秒）', src='JR東海（自然災害等による遅延も含む）', art='assets/shinkansen/art_platform.png', col='white'),
        dict(text='一方、二〇一六年度は、二十四秒と、記事で紹介されています。', big='2016年度：24秒', src='nippon.com（二次情報）', art='assets/shinkansen/art_tracks.png'),
        dict(text='年度で数字が動くので、二つだけで、悪くなった、とは言えません。', big='年度で動く。2つだけでは言えない', art='assets/shinkansen/art_storm.png', col='white'),
        dict(text='平均は、一本ごとの遅れを示す数字では、ありません。見るときは、年度と、何を含むかを確かめましょう。', big='年度と、含むものを確かめる', art='assets/shinkansen/art_platform.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/shinkansen/art_intro.png')]))

J('snowcrystal', dict(
    title='雪の結晶、同じ形はない？', long_id='1vnSqLs6N_I',
    long_title='雪の結晶は、一つとして同じ形がない？ 気象台・科学館の資料で確かめる',
    pron='data/snowcrystal_pronunciations.json', art='assets/snowcrystal/art_intro.png',
    hook='「雪の結晶は、一つとして同じ形がない」。冬の理科でよく聞く言葉を、気象台や科学館の資料で確かめます。',
    notes='■ 動画で確かめたこと\n・雪の結晶は、水蒸気が直接氷になってできます。形は、成長するときの温度と水蒸気の量で大きく変わります(福岡管区気象台・大阪市立科学館)。\n・気象台や科学館の資料は「同じ形はない(言われている)」と書いていますが、一般向けの説明で、証明の書き方ではありません。\n・1988年に、とてもよく似た二つの結晶の報告があります。完全な同一を示したものではないとされます(二次情報。原著は未確認)。\n・「絶対に同じものがない」という証明は、今回確認した資料では見つかりませんでした。出典は本編の概要欄にまとめています。',
    credit=CREDIT, answer='完全一致は考えにくい。ただし証明は未確認',
    scenes=[
        dict(text='「雪の結晶は、一つとして、同じ形がない」。聞いたことは、ありませんか。', big='雪の結晶は、同じ形がない？', art='assets/snowcrystal/art_intro.png'),
        dict(text='雪の結晶は、水蒸気が直接、氷になってできます。形は、温度と水蒸気の量で、大きく変わります。', big='形は、温度と水蒸気の量で変わる', src='福岡管区気象台・大阪市立科学館', art='assets/snowcrystal/art_cloud.png', col='white'),
        dict(text='気象台や科学館の資料は、同じ形はない、と書いています。ただし、一般向けの説明です。', big='資料は「同じ形はない」と説明', art='assets/snowcrystal/art_micro.png'),
        dict(text='一九八八年には、とてもよく似た二つの結晶が、報告されました。完全な同一を示したものでは、ありません。', big='1988年：とてもよく似た二つの報告', src='二次情報（原著は未確認）', art='assets/snowcrystal/art_lab.png', col='white'),
        dict(text='「絶対に同じものがない」という証明は、今回の資料では、見つかりませんでした。「同じ」の意味でも、答えは変わります。', big='「絶対にない」の証明は、確認できず', art='assets/snowcrystal/art_micro.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/snowcrystal/art_intro.png')]))

J('seijin', dict(
    title='成人の日、なぜ1月15日じゃない？', long_id='d-sAg63v9Mo',
    long_title='成人の日は、なぜ1月15日ではなくなった？ 内閣府の資料と法改正で確かめる',
    pron='data/seijin_pronunciations.json', art='assets/seijin/art_intro.png',
    hook='成人の日は、昔は一月十五日でした。なぜ、変わったのでしょうか。内閣府の資料で確かめます。',
    notes='■ 動画で確かめたこと\n・成人の日は、祝日法で「1月の第2月曜日」と決められています(内閣府)。\n・1998年(平成10年)10月21日公布の祝日法の改正(法律第141号)で、「1月15日」から変わりました。施行は2000年1月1日です。\n・改正の理由は、連休にして余暇活動を充実させ、ゆとりある国民生活を実現するため(内閣府)。\n・1月15日は、元服の日取りを避けて、松の内にあたる15日が選ばれた、と内閣府の資料にあります(昭和23年の報告書)。出典は本編の概要欄にまとめています。',
    credit=CREDIT, answer='1998年の法改正。施行は2000年1月1日',
    scenes=[
        dict(text='成人の日は、昔は、一月十五日でした。なぜ、一月十五日では、なくなったのでしょうか。', big='成人の日は、なぜ1月15日じゃない？', art='assets/seijin/art_intro.png'),
        dict(text='今の成人の日は、祝日法で、一月の第二月曜日と、決められています。', big='今：1月の第2月曜日', src='内閣府', art='assets/seijin/art_hall.png', col='white'),
        dict(text='変わったのは、一九九八年の、祝日法の改正です。施行は、二〇〇〇年一月一日からです。', big='1998年の改正。施行は2000年1月1日', src='国民の祝日に関する法律の一部を改正する法律', art='assets/seijin/art_desk.png'),
        dict(text='目的は、連休にして、余暇活動を充実させ、ゆとりのある国民生活を、実現することでした。', big='目的：連休にして、余暇を充実', src='内閣府', art='assets/seijin/art_shrine.png', col='white'),
        dict(text='もとの一月十五日は、元服の日取りを避けて、松の内から、選ばれたと説明されています。', big='1月15日は、元服の日を避けて選ばれた', src='内閣府（昭和23年の報告書）', art='assets/seijin/art_shrine.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/seijin/art_intro.png')]))

J('frequency', dict(
    title='電気の周波数、なぜ東西で違う？', long_id='vUkgD2jioQM',
    long_title='日本の電気は、なぜ東と西で周波数が違う？ 電力会社の資料で確かめる',
    pron='data/frequency_pronunciations.json', art='assets/frequency/art_intro.png',
    hook='日本の電気は、東日本が五十ヘルツ、西日本が六十ヘルツ。なぜ違うのか、電力会社の資料で確かめます。',
    notes='■ 動画で確かめたこと\n・東日本は50ヘルツ、西日本は60ヘルツです。境目は、新潟県の糸魚川と静岡県の富士川を結ぶ線とされます(関西電力・北海道電力ネットワーク)。\n・明治時代に、東京にはドイツ製(50ヘルツ)、大阪にはアメリカ製(60ヘルツ)の発電機が輸入され、それぞれが全国に広がりました(関西電力)。\n・約100年前から統一が何度も話し合われましたが、うまくいきませんでした(関西電力)。詳しい理由は確認できていません。\n・周波数変換設備の合計容量は、2021年に120万kWから210万kWに拡大しました(送配電事業者9社の発表)。導入年やメーカー名は二次情報で、未確認です。出典は本編の概要欄にまとめています。',
    credit=CREDIT, answer='明治の輸入発電機が、東京と大阪で違ったから',
    scenes=[
        dict(text='日本の電気は、東日本が五十ヘルツ、西日本が六十ヘルツ。同じ国で、なぜ、違うのでしょうか。', big='電気の周波数は、なぜ東西で違う？', art='assets/frequency/art_intro.png'),
        dict(text='明治時代、日本は、発電機を外国から輸入していました。', big='明治：発電機は、輸入していた', src='関西電力', art='assets/frequency/art_plant.png', col='white'),
        dict(text='東京には、ドイツ製の発電機。五十ヘルツの電気をつくります。', big='東京：ドイツ製 → 50ヘルツ', src='関西電力', art='assets/frequency/art_plant.png'),
        dict(text='大阪には、アメリカ製の発電機。六十ヘルツの電気をつくります。', big='大阪：アメリカ製 → 60ヘルツ', src='関西電力', art='assets/frequency/art_pylon.png', col='white'),
        dict(text='それぞれが全国に広がり、統一の話し合いも、うまくいきませんでした。今は、周波数変換設備で、東西をつないでいます。', big='統一はうまくいかず、変換設備でつなぐ', src='関西電力・送配電事業者', art='assets/frequency/art_sub.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/frequency/art_intro.png')]))
