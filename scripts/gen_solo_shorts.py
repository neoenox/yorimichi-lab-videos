"""単独Short（長尺の要約ではなく、一つの切り口だけで完結する短い動画）の spec。
長尺のイラストと読み辞書を流用し、新しい画像は作らない。台本の数字・限定は長尺の 09_script_v2.md に合わせる。
usage: python scripts/gen_solo_shorts.py → data/short_solo_*.json。その後 make_short2.py / pack_short.py / yt_api.py upload。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
CREDIT = '・イラスト：ChatGPT(OpenAI)による生成イラスト（イメージです。実在の場面・人物・資料の再現ではありません）\n・図・表：自作'
MORE = '詳しい根拠は、長い動画にまとめています。出典は本編の概要欄にあります。'


def J(n, o):
    o.setdefault('credit', CREDIT)
    (R / 'data' / f'short_{n}.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')


def end():
    return dict(text='くわしくは、長い動画で、確かめています。', end=True)


J('solo_shinkansen24', dict(
    title='新幹線の遅れ「平均24秒」は本当？', long_id='gNGUPpg4wQM',
    long_title='新幹線の遅延は、平均で何秒？ JR東海の資料と報道で確かめる',
    pron='data/shinkansen_pronunciations.json', art='assets/shinkansen/art_intro.png',
    hook='「新幹線の遅れは、平均で24秒」と聞いたことはありませんか。その数字がいつのものか、確かめます。',
    notes='■ 動画で確かめたこと\n・「平均24秒」は、2016年度の数字として報道で紹介されています(nippon.com、二次情報)。\n・JR東海の資料では、2024年度の平均遅延時分は、運行一列車あたり1.4分(84秒)です。自然災害等による遅延も含みます。\n・集計の方法は確かめていないので、この2つの数字だけで定時運行の良し悪しは言えません。',
    answer='24秒は2016年度の数字',
    scenes=[
        dict(text='新幹線の遅れは、平均で、二十四秒。そう聞いたことは、ありませんか。', big='新幹線の遅れ、平均24秒？', art='assets/shinkansen/art_intro.png'),
        dict(text='この二十四秒は、二〇一六年度の数字として、報道で紹介されています。', big='24秒は、2016年度の数字', src='nippon.com（二次情報）', art='assets/shinkansen/art_platform.png', col='white'),
        dict(text='JR東海の資料では、二〇二四年度は、運行一列車あたり、一・四分です。', big='2024年度：1.4分', src='JR東海', art='assets/shinkansen/art_tracks.png'),
        dict(text='一・四分は、八十四秒。自然災害などによる遅れも、含まれています。', big='1.4分＝84秒', sub='自然災害等による遅延も含む', src='JR東海', art='assets/shinkansen/art_storm.png', col='white'),
        end()]))

J('solo_snow_letter', dict(
    title='「雪は天から送られた手紙」の意味は？', long_id='1vnSqLs6N_I',
    long_title='雪の結晶は、一つとして同じ形がない？ 気象台と科学館の資料で確かめる',
    pron='data/snowcrystal_pronunciations.json', art='assets/snowcrystal/art_intro.png',
    hook='「雪は天から送られた手紙である」。中谷宇吉郎のこの言葉の意味を、科学館の資料で確かめます。',
    notes='■ 動画で確かめたこと\n・中谷宇吉郎は、1936年に世界で初めて人工雪の生成に成功したとされています(大阪市立科学館)。\n・低温の実験室で条件を決めて雪を作り、どんな条件でどんな形に育つかを調べました。\n・「雪は天から送られた手紙である」は、上空の状態が結晶の形に出る、という意味です(同)。\n・大きな枝のような形は、気温がマイナス15度前後で水蒸気が多いときにできます(福岡管区気象台)。',
    answer='上空の状態が、形に出るから',
    scenes=[
        dict(text='雪は、天から送られた手紙である。この言葉を、聞いたことはありませんか。', big='雪は天からの手紙？', art='assets/snowcrystal/art_intro.png'),
        dict(text='言ったのは、中谷宇吉郎。一九三六年に、世界で初めて、人工雪の生成に成功したと、されています。', big='1936年、人工雪に成功', src='大阪市立科学館', art='assets/snowcrystal/art_lab.png', col='white'),
        dict(text='低温の実験室で、条件を決めて雪を作り、どんな条件で、どんな形に育つかを、調べました。', big='条件を変えて、雪を作った', src='大阪市立科学館', art='assets/snowcrystal/art_micro.png'),
        dict(text='たとえば、大きな枝のような形は、気温がマイナス十五度前後で、水蒸気が多いときに、できます。', big='枝の形は、マイナス15度前後', sub='水蒸気が多いときにできる', src='福岡管区気象台', art='assets/snowcrystal/art_cloud.png', col='white'),
        dict(text='だから、結晶の形から、上空の状態が、わかる。それが、手紙という意味です。', big='形を見れば、上空がわかる', art='assets/snowcrystal/art_glove.png'),
        end()]))

J('solo_snow_same', dict(
    title='雪の結晶、同じ形は本当にない？', long_id='1vnSqLs6N_I',
    long_title='雪の結晶は、一つとして同じ形がない？ 気象台と科学館の資料で確かめる',
    pron='data/snowcrystal_pronunciations.json', art='assets/snowcrystal/art_micro.png',
    hook='「雪の結晶は、一つとして同じ形がない」。気象台や科学館の資料で、どこまで言えるのかを確かめます。',
    notes='■ 動画で確かめたこと\n・福岡管区気象台の資料は「一つとして同じ形のものはなく」と書き、大阪市立科学館の資料も、全く同じ形の結晶はないと言われている、と説明しています。\n・ただし、どちらも一般向けの説明で、「絶対に同じものがない」という証明までは、今回確認した資料では見つかりませんでした。',
    answer='そっくりは、まず見つからない。証明は見つからず',
    scenes=[
        dict(text='雪の結晶は、一つとして、同じ形がない。冬の理科の、よく知られた話です。', big='同じ形は、一つもない？', art='assets/snowcrystal/art_micro.png'),
        dict(text='雲の中で成長して落ちてくる間の、気温や湿度は、結晶ごとに、少しずつ違います。', big='落ちる間の環境が、一つずつ違う', src='福岡管区気象台', art='assets/snowcrystal/art_cloud.png', col='white'),
        dict(text='気象台の資料は、一つとして同じ形のものはなく、と書いています。', big='気象台：同じ形のものはない', sub='「一つとして同じ形のものはなく」と記述', src='福岡管区気象台', art='assets/snowcrystal/art_glove.png'),
        dict(text='ただし、これは一般向けの説明です。絶対に同じものがない、という証明までは、確認できませんでした。', big='「絶対にない」の証明は、見つからず', art='assets/snowcrystal/art_lab.png', col='white'),
        end()]))

J('solo_seijin1115', dict(
    title='成人の日の1月15日、いつまで？', long_id='d-sAg63v9Mo',
    long_title='成人の日は、なぜ1月15日ではなくなった？ 内閣府の資料と法律の改正で確かめる',
    pron='data/seijin_pronunciations.json', art='assets/seijin/art_intro.png',
    hook='昔の成人の日は、1月15日でした。いつまでそうだったのか、内閣府の資料と法律の記録で確かめます。',
    notes='■ 動画で確かめたこと\n・成人の日は、今は1月の第2月曜日です(内閣府)。\n・1998年10月21日公布の改正法(法律第141号)で、「1月15日」から「1月の第2月曜日」に改められました。施行は2000年1月1日です。\n・1月15日が成人の日だったのは、1949年から1999年までとされています(二次情報)。2000年の成人の日は1月10日でした。\n・改正の目的は、連休にして余暇活動を充実させるためです(内閣府)。',
    answer='1999年まで。2000年から第2月曜日',
    scenes=[
        dict(text='昔は、成人の日と言えば、一月十五日でした。では、いつまで、そうだったのでしょうか。', big='成人の日＝1月15日、いつまで？', art='assets/seijin/art_intro.png'),
        dict(text='一九九八年の十月に、法律の改正が公布されました。成人の日は、一月十五日から、一月の第二月曜日に、改められました。', big='1998年の改正で、第2月曜日に', src='祝日法の改正法（法律第141号）', art='assets/seijin/art_desk.png', col='white'),
        dict(text='施行は、二〇〇〇年一月一日。この年の成人の日は、一月十日でした。', big='2000年から。この年は1月10日', src='国立天文台', art='assets/seijin/art_hall.png'),
        dict(text='つまり、一月十五日だったのは、一九四九年から一九九九年まで、とされています。', big='1月15日：1949年〜1999年', src='二次情報', sub='1949年から1999年まで、とされている', art='assets/seijin/art_shrine.png', col='white'),
        dict(text='目的は、連休にして、余暇活動を、充実させることだと、内閣府の資料にあります。', big='目的：連休にして、余暇を充実', src='内閣府', art='assets/seijin/art_desk.png'),
        end()]))

J('solo_freq_why', dict(
    title='電気の周波数、東と西で違うのはなぜ？', long_id='vUkgD2jioQM',
    long_title='日本の電気は、なぜ東と西で周波数が違う？ 電力会社の資料で確かめる',
    pron='data/frequency_pronunciations.json', art='assets/frequency/art_intro.png',
    hook='日本の電気は、東が50ヘルツ、西が60ヘルツです。なぜ違うのか、電力会社の資料で確かめます。',
    notes='■ 動画で確かめたこと\n・東日本は50ヘルツ、西日本は60ヘルツです(北海道電力ネットワーク)。\n・関西電力の資料では、東京にはドイツ製の発電機、大阪にはアメリカ製の発電機が輸入され、それぞれの周波数が広がったと説明しています。\n・導入した年とメーカー名は二次情報で、一次資料では確認していません。',
    answer='輸入した発電機が違ったから',
    scenes=[
        dict(text='日本の電気は、東日本が五十ヘルツ、西日本が六十ヘルツ。なぜ、違うのでしょうか。', big='東は50、西は60ヘルツ', art='assets/frequency/art_intro.png'),
        dict(text='明治時代、日本は発電機を、外国から輸入していました。東京には、ドイツ製。大阪には、アメリカ製です。', big='東京＝ドイツ製、大阪＝アメリカ製', src='関西電力', art='assets/frequency/art_plant.png', col='white'),
        dict(text='ドイツ製は五十ヘルツ、アメリカ製は六十ヘルツの電気を、つくります。', big='ドイツ製＝50、アメリカ製＝60', src='関西電力', art='assets/frequency/art_pylon.png'),
        dict(text='やがて、それぞれの周波数が、そのまま、全国に広がりました。', big='そのまま、全国に広がった', src='関西電力', art='assets/frequency/art_sub.png', col='white'),
        end()]))

J('solo_freq_move', dict(
    title='引っ越しで、家電が使えなくなる？', long_id='vUkgD2jioQM',
    long_title='日本の電気は、なぜ東と西で周波数が違う？ 電力会社の資料で確かめる',
    pron='data/frequency_pronunciations.json', art='assets/frequency/art_home.png',
    hook='東日本と西日本で、電気の周波数は違います。引っ越すと、家電は使えなくなるのでしょうか。',
    notes='■ 動画で確かめたこと\n・関西電力の資料では、五十ヘルツと六十ヘルツの両方に対応すると表示された製品は、どこでも使えます。\n・扇風機、ヘアドライヤー、掃除機は、性能が変わります。\n・洗濯機、電気時計、電子レンジは、そのままでは使えないとされています。',
    answer='製品しだい。両対応の表示を確認',
    scenes=[
        dict(text='東日本と西日本で、電気の周波数は違います。引っ越すと、家電は、使えなくなるのでしょうか。', big='引っ越すと、家電は使えない？', art='assets/frequency/art_home.png'),
        dict(text='五十ヘルツと、六十ヘルツの、両方に対応すると表示された製品は、どこでも使えます。', big='両対応の表示なら、どこでもOK', src='関西電力', art='assets/frequency/art_intro.png', col='white'),
        dict(text='扇風機、ヘアドライヤー、掃除機は、使えても、性能が変わります。', big='性能が変わる：扇風機・ドライヤー・掃除機', src='関西電力', art='assets/frequency/art_plant.png'),
        dict(text='洗濯機、電気時計、電子レンジは、そのままでは、使えないと、されています。', big='そのままでは使えない：洗濯機・時計・レンジ', src='関西電力', art='assets/frequency/art_pylon.png', col='white'),
        end()]))

J('solo_takarakuji100', dict(
    title='宝くじ百円で、当せん金は約何円分？', long_id='L2R4JsyMp8I',
    long_title='宝くじは、買ったお金の何割が当せん金になる？ 公式サイトの数字で確かめる',
    pron='data/takarakuji_pronunciations.json', art='assets/takarakuji/art_intro.png',
    hook='宝くじを百円分買うと、当せん金として払われるのは、約何円分でしょうか。公式サイトの数字で確かめます。',
    notes='■ 動画で確かめたこと\n・令和6年度の販売実績額は7,598億円。当せん金は3,529億円(46.5％)、収益金は2,750億円(36.2％)、経費は1,218億円(16.0％)、社会貢献広報費は101億円(1.3％)でした(宝くじ公式サイト)。\n・百円あたりに直すと、当せん金は約46円です(自作の換算)。\n・これは全体の割合で、一人ひとりに戻る額ではありません。商品ごとの割合は確認していません。買うことをすすめる・止める動画ではありません。',
    answer='約46円分',
    scenes=[
        dict(text='宝くじを、百円分買うと、当せん金として払われるのは、約何円分でしょうか。', big='百円分買うと、当せん金は？', art='assets/takarakuji/art_intro.png'),
        dict(text='令和六年度の販売実績額は、七千五百九十八億円。このうち、当せん金は、三千五百二十九億円です。', big='当せん金：46.5％', src='宝くじ公式サイト（令和6年度）', art='assets/takarakuji/art_counter.png', col='white'),
        dict(text='百円あたりに直すと、約四十六円です。', big='百円につき、約46円', src='自作の換算', sub='当せん金の割合46.5％を百円あたりに直した数字', art='assets/takarakuji/art_coins.png'),
        dict(text='残りは、収益金が三十六パーセント。経費などが、十七パーセントほどです。', big='収益金36.2％、経費など約17％', src='宝くじ公式サイト', art='assets/takarakuji/art_city.png', col='white'),
        dict(text='これは全体の割合です。一人ひとりに、戻る金額では、ありません。', big='全体の割合。一人に戻る額ではない', art='assets/takarakuji/art_counter.png'),
        end()]))
