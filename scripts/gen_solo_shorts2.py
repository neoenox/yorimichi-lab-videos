"""単独Short 第2弾（江戸の2食・識字率・大工・木戸・睡眠）の spec。長尺のイラストと読み辞書を流用し、新しい画像は作らない。
long_id は data/youtube_ids.json の台帳から読む（長尺をアップしてから実行。台帳にない題材は飛ばす）。
usage: python scripts/gen_solo_shorts2.py → data/short_solo_*.json。その後 make_short2.py / pack_short.py / yt_api.py upload。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
CREDIT = '・イラスト：ChatGPT(OpenAI)による生成イラスト（イメージです。実在の場面・人物・資料の再現ではありません）\n・図・表：自作'
IDS = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))


def J(n, pack, o):
    rec = IDS.get(pack)
    if not rec:
        print('skip', n, '(長尺が台帳にない)'); return
    o['long_id'] = rec['video_id']
    o.setdefault('credit', CREDIT)
    (R / 'data' / f'short_{n}.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')
    print('wrote', n)


def end():
    return dict(text='くわしくは、長い動画で、確かめています。', end=True)


J('solo_meals_region', '50_twomeals', dict(
    title='江戸の昼ごはんは、冷や飯？',
    long_title='江戸時代の人は、1日2食だった？ 農林水産省の説明と解説記事で確かめる',
    pron='data/twomeals_pronunciations.json', art='assets/twomeals/art_intro.png',
    hook='「江戸の人は、朝に一日分のご飯を炊いた」と聞いたことはありませんか。解説記事の説明を確かめます。',
    notes='■ 動画で確かめたこと\n・解説記事によると、江戸では、朝に一日分のご飯をまとめて炊き、昼は冷めたご飯で済ませるのが一般的でした。\n・京都・大坂を含む京阪神では、昼食が重視されていた、とされています。\n・原典の史料は確認していません。出典は本編の概要欄にまとめています。',
    answer='地域で違った（記事の説明）',
    scenes=[
        dict(text='江戸の人は、朝に一日分のご飯を炊いて、昼は冷や飯だった。そう聞いたことは、ありませんか。', big='江戸の昼は、冷や飯？', art='assets/twomeals/art_intro.png'),
        dict(text='解説記事によると、江戸では、朝に一日分のご飯をまとめて炊き、昼は冷めたご飯で済ませるのが、一般的でした。', big='朝にまとめて炊く', sub='昼は冷めたご飯で済ませた', src='解説記事（二次情報）', art='assets/twomeals/art_kitchen.png', col='white'),
        dict(text='一方、京都や大坂を含む京阪神では、昼食が重視されていた、とされています。', big='京阪神は、昼食が重視', src='解説記事（二次情報）', art='assets/twomeals/art_lamp.png'),
        dict(text='つまり、江戸はこう、と一つに言い切るのは、難しいようです。原典の史料は、確認していません。', big='一つには、言い切れない', sub='原典の史料は未確認', src='自作のまとめ', art='assets/twomeals/art_kitchen.png', col='white'),
        end()]))

J('solo_literacy_shiga', '51_literacy', dict(
    title='1877年の滋賀県、名前が書ける人は？',
    long_title='江戸時代の日本は、識字率が世界一だった？ 寺子屋の資料で確かめる',
    pron='data/literacy_pronunciations.json', art='assets/literacy/art_intro.png',
    hook='「江戸の人は、みんな読み書きができた」と聞いたことはありませんか。実際の調査の数字を見ます。',
    notes='■ 動画で確かめたこと\n・寺子屋の解説によると、1877年(明治10年)の滋賀県の調査で、6歳以上で自分の名前を書ける人は、男子89％、女子39％でした。\n・これは明治の初めの一つの県の数字で、江戸時代全体の数字ではありません。\n・原典の資料は確認していません。出典は本編の概要欄にまとめています。',
    answer='男子89％・女子39％',
    scenes=[
        dict(text='江戸の人は、みんな読み書きができた。そう聞いたことは、ありませんか。', big='江戸は、みんな読み書き？', art='assets/literacy/art_intro.png'),
        dict(text='実際に調べた数字として、一八七七年、明治十年の、滋賀県の調査があります。', big='1877年、滋賀県の調査', src='寺子屋の解説（二次情報）', art='assets/literacy/art_desk.png', col='white'),
        dict(text='六歳以上で、自分の名前を書ける人は、男子が八十九パーセント、女子が三十九パーセントでした。', big='男子89％　女子39％', sub='6歳以上で自分の名前を書ける人', src='寺子屋の解説（二次情報）', art='assets/literacy/art_books.png'),
        dict(text='男女で、大きな差があります。ただし、明治の初めの、一つの県の数字で、江戸時代全体の数字では、ありません。', big='男女で、大きな差', sub='明治初めの、1つの県の数字', src='自作のまとめ', art='assets/literacy/art_shop.png', col='white'),
        end()]))

J('solo_carpenter10h', '53_carpenter', dict(
    title='江戸の大工、現場に約10時間？',
    long_title='江戸の大工は、一日4時間しか働かなかった？ 解説記事の説明を比べて確かめる',
    pron='data/carpenter_pronunciations.json', art='assets/carpenter/art_intro.png',
    hook='「江戸の大工は、一日四時間しか働かなかった」と聞いたことはありませんか。別の説明も見てみます。',
    notes='■ 動画で確かめたこと\n・ある解説では、大工や左官は、朝の六ツ半(午前7時ごろ)に現場へ来て、夕方の七ツ半(午後5時ごろ)までいる習慣だったと説明されています。現場にいた時間は約10時間です(自作の計算)。\n・休憩を引いた実働は、6〜7時間ほどという説明です。\n・一方、休憩を引くと4時間ほどという説明もあります。どちらも元の史料は示されていません。',
    answer='実働は4〜7時間と幅がある',
    scenes=[
        dict(text='江戸の大工は、一日に、四時間しか働かなかった。そう聞いたことは、ありませんか。', big='大工は、一日4時間？', art='assets/carpenter/art_intro.png'),
        dict(text='別の解説では、朝の六ツ半、今の午前七時ごろに現場へ来て、夕方の七ツ半、午後五時ごろまで、いたとされます。', big='午前7時ごろ〜午後5時ごろ', src='解説記事（二次情報）', art='assets/carpenter/art_site.png', col='white'),
        dict(text='現場にいた時間だけなら、約十時間。そこから休憩を引くと、実働は、六時間から七時間ほどという計算です。', big='現場に約10時間', sub='休憩を引くと、実働6〜7時間ほど', src='自作の計算', art='assets/carpenter/art_tools.png'),
        dict(text='四時間から七時間。数字には幅があり、どの解説も、元の史料は示していません。', big='4〜7時間。出典は不明', sub='元の史料は示されていない', src='自作のまとめ', art='assets/carpenter/art_site.png', col='white'),
        end()]))

J('solo_kido_pass', '54_kido', dict(
    title='木戸が閉まったら、どう通る？',
    long_title='江戸の町は、夜になると閉鎖された？ 木戸番の解説と国会図書館の事例で確かめる',
    pron='data/kido_pronunciations.json', art='assets/kido/art_intro.png',
    hook='「江戸の町は、夜になると木戸が閉まって通れなくなった」と聞いたことはありませんか。決まりを確かめます。',
    notes='■ 動画で確かめたこと\n・Wikipedia「木戸番」によると、木戸は夜の四ツ時(午後10時ごろ)に閉められました。\n・用事のある人は、木戸番に確かめてもらったうえで、潜り戸から通りました。通るたびに拍子木を打ち、次の木戸番に知らせました(送り拍子木)。\n・医師や産婆はそのまま通れたと説明されていますが、原典は確認していません。',
    answer='潜り戸から通れた',
    scenes=[
        dict(text='江戸の町は、夜になると、木戸が閉まって、通れなくなった。そう聞いたことは、ありませんか。', big='夜の木戸は、通れない？', art='assets/kido/art_intro.png'),
        dict(text='木戸は、夜の四ツ時、午後十時ごろに閉まったとされています。', big='夜の四ツ時に閉まる', sub='午後10時ごろ', src='Wikipedia「木戸番」', art='assets/kido/art_gate.png', col='white'),
        dict(text='でも、木戸番に確かめてもらえば、左右の潜り戸から、通ることができました。', big='潜り戸から、通れた', src='Wikipedia「木戸番」', art='assets/kido/art_night.png'),
        dict(text='通るときは、拍子木を打って、次の木戸番に知らせました。医師や産婆は、そのまま通れたとされますが、原典は確認していません。', big='拍子木で、次へ知らせる', sub='医師・産婆の例外は原典未確認', src='Wikipedia「木戸番」', art='assets/kido/art_gate.png', col='white'),
        end()]))

J('solo_sleep14h', '55_sleep', dict(
    title='14時間の暗闇で、眠りはどうなった？',
    long_title='昔の人は、夜に2回に分けて眠っていた？ 英語版Wikipediaで確かめる',
    pron='data/sleep_pronunciations.json', art='assets/sleep/art_intro.png',
    hook='「昔の人は、夜に二回に分けて眠っていた」という説があります。その実験の結果を、確かめます。',
    notes='■ 動画で確かめたこと\n・英語版Wikipediaによると、1992年に、健康な男性7人が、1日14時間の暗闇で1か月過ごす実験がありました。\n・最初は11時間ほど眠り、その後は、約4時間眠り、2〜3時間起き、また約4時間眠る形が現れました。\n・一方、電気のない社会の調査では、夜の眠りが1回だった例もあります。原論文は確認していません。',
    answer='眠りが2つに分かれた',
    scenes=[
        dict(text='電気がなかった昔、人は、夜に二回に分けて眠っていた。そんな説が、あります。', big='夜に2回、眠っていた？', art='assets/sleep/art_intro.png'),
        dict(text='一九九二年、健康な男性七人が、一日十四時間の暗闇で、一か月過ごす実験が、行われました。', big='1日14時間の暗闇、1か月', src='英語版Wikipedia', art='assets/sleep/art_dark.png', col='white'),
        dict(text='すると、約四時間眠り、二、三時間起きて、また約四時間眠る形が、現れました。', big='約4時間→起きる→約4時間', sub='起きていたのは2〜3時間', src='英語版Wikipedia', art='assets/sleep/art_candle.png'),
        dict(text='ただし、電気のない社会の調査で、眠りが一回だった例もあり、普通だったかは、議論が続いています。', big='1回だった例もある', sub='普通だったかは議論が続く', src='英語版Wikipedia', art='assets/sleep/art_dark.png', col='white'),
        end()]))

J('solo_bath_hagaki', '56_bath', dict(
    title='銭湯の月ぎめ「羽書」は得？',
    long_title='江戸の銭湯は、そば一杯の半分の値段だった？ 解説記事の数字を比べて確かめる',
    pron='data/bath_pronunciations.json', art='assets/bath/art_intro.png',
    hook='江戸の銭湯には、一か月のフリーパスがあったそうです。その損得を、計算で確かめます。',
    notes='■ 動画で確かめたこと\n・「羽書」は、一か月のフリーパスです。『守貞謾稿』によると、値段は一か月で148文前後でした(解説記事・二次情報)。\n・一回6文なら、25回入ると150文で、羽書とほぼ同じです(自作の計算)。つまり、月に25回以上入る人には得、という計算です。\n・原典の史料は確認していません。出典は本編の概要欄にまとめています。',
    answer='25回以上入れば羽書が得',
    scenes=[
        dict(text='江戸の銭湯には、一か月のフリーパスが、あったそうです。', big='銭湯に、月ぎめがあった？', art='assets/bath/art_intro.png'),
        dict(text='「羽書」と呼ばれ、『守貞謾稿』によると、値段は、一か月で、百四十八文前後でした。', big='羽書：1か月で148文前後', src='解説記事（二次情報）', art='assets/bath/art_coins.png', col='white'),
        dict(text='一回六文なら、二十五回入ると、百五十文。羽書と、ほぼ同じです。', big='6文×25回＝150文', sub='1回6文として計算', src='自作の計算', art='assets/bath/art_bath.png'),
        dict(text='つまり、月に二十五回以上入る人には、羽書のほうが得、という計算です。', big='25回以上なら、羽書が得', sub='毎日のように通う人向けの仕組み', src='自作の計算', art='assets/bath/art_coins.png', col='white'),
        end()]))

J('solo_travel_tokaido', '57_travel', dict(
    title='東海道を、12日で歩くと？',
    long_title='江戸時代の旅人は、一日に40キロ歩いた？ 国会図書館のレファレンス事例で確かめる',
    pron='data/travel_pronunciations.json', art='assets/travel/art_intro.png',
    hook='東海道を、十一泊十二日で歩いた例があるそうです。一日あたりの距離を、計算で確かめます。',
    notes='■ 動画で確かめたこと\n・レファレンス事例が挙げる東海道の本には、11泊12日の旅で、一日あたり約10里半という例があります。\n・10里半×12日＝126里で、1里を約3.93kmとすると、約495kmです(自作の計算)。つまり、一日40km余りです。\n・一方、平均を8里前後(約31km)とする本もあります。原典は確認していません。出典は本編の概要欄にまとめています。',
    answer='一日40km余りの計算',
    scenes=[
        dict(text='東海道を、十一泊十二日で歩いた例が、あるそうです。', big='東海道、11泊12日？', art='assets/travel/art_intro.png'),
        dict(text='レファレンス事例が挙げる、東海道の本では、一日あたり、約十里半という例が、紹介されています。', big='一日約10里半の例', src='国会図書館レファレンス事例', art='assets/travel/art_road.png', col='white'),
        dict(text='十里半を、十二日続けると、百二十六里。一里を約三・九三キロとすると、約四百九十五キロです。', big='126里＝約495km', sub='1里は約3.93kmで計算', src='自作の計算', art='assets/travel/art_inn.png'),
        dict(text='つまり、一日四十キロ余り。急ぐ男性の旅なら、あり得る数字です。', big='一日40km余りの計算', sub='平均は8里前後（約31km）という本も', src='国会図書館レファレンス事例', art='assets/travel/art_road.png', col='white'),
        end()]))

J('solo_recycle_shinyo', '58_recycle', dict(
    title='江戸のし尿は、お金で取引？',
    long_title='江戸は、ごみが出ない完全リサイクル社会だった？ 環境省の白書で確かめる',
    pron='data/recycle_pronunciations.json', art='assets/recycle/art_intro.png',
    hook='江戸では、し尿が、肥料として取引されていたと言われます。環境省の白書の説明を、確かめます。',
    notes='■ 動画で確かめたこと\n・環境省の白書によると、農家は武家屋敷や長屋ごとに契約し、お金や品物と引き換えに、し尿を汲み取る権利を得ていました。\n・江戸の中ごろには仲買の組織も現れ、後期には値段が上がり、近郊の農民が幕府に陳情した例もあります。\n・ただし「完全なリサイクル」とまでは、今回読んだ範囲では言い切れません。原典は確認していません。出典は本編の概要欄にまとめています。',
    answer='取引されていた。ただし完全とは言い切れない',
    scenes=[
        dict(text='江戸では、し尿が、肥料として、取引されていたと言われます。', big='し尿は、取引された？', art='assets/recycle/art_intro.png'),
        dict(text='環境省の白書によると、農家は、武家屋敷や長屋ごとに契約し、お金や品物と引き換えに、汲み取る権利を得ていました。', big='契約して、汲み取る', src='環境省の白書', art='assets/recycle/art_farm.png', col='white'),
        dict(text='江戸の中ごろには、仲買の組織も現れ、後期には、値段が上がって、農民が幕府に陳情した例もあります。', big='値上がりで、陳情した例も', src='環境省の白書', art='assets/recycle/art_farm.png'),
        dict(text='ただし、「完全なリサイクル」だったとまでは、今回読んだ範囲では、言い切れません。', big='「完全」とは言い切れない', sub='原典の史料は未確認', src='自作のまとめ', art='assets/recycle/art_shop.png', col='white'),
        end()]))
