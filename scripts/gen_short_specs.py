"""Short用の spec（data/short_<slug>.json）を作る。台本は長尺の 09_script_v2.md の文言に合わせる。

data/short_*.json を正として同期している（2026-10-20）。新しい回はここに J() を足す。
"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]


def J(n, o):
    (R / 'data' / f'short_{n}.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')

J('vein', dict(
    title='静脈の血は、青い？',
    long_id='vtGdSrEnQjI',
    long_title='静脈の血は、体の中では青いのか？ アリゾナ州立大学とハーバード・ヘルスで確かめる',
    pron='data/vein_pronunciations.json',
    art='assets/vein/art_arm.png',
    hook='「静脈の血は、体の中では青い」と聞いたことはありませんか。アリゾナ州立大学とハーバード・ヘルスの解説から、血の色を確かめます。',
    notes='■ 動画で確かめたこと\n・人間の血液は常に赤色で、酸素が多いと明るい赤色、少ないと暗い赤色になります（アリゾナ州立大学）。\n・手の甲の静脈が青く見えるのは、皮膚による光の吸収の仕方による錯覚だとされています（ハーバード・ヘルス）。\n・教科書の図で静脈が青いのは、動脈と区別するためです（ハーバード・ヘルス）。\n・色から体の状態を判断することは、扱っていません。',
    scenes=[
        dict(text='「静脈の血は、体の中では青い」。そう聞いたことはありませんか。', big='静脈の血は、青い？', art='assets/vein/art_arm.png'),
        dict(text='アリゾナ州立大学の解説によると、人間の血液は、常に赤色です。', big='血は、常に赤色', sub='酸素が多いと明るい赤、少ないと暗い赤', src='アリゾナ州立大学', art='assets/vein/art_cells.png', col='white'),
        dict(text='酸素が多く結びついていると、明るい赤色に、少ないと、暗い赤色になります。', big='明るい赤 と 暗い赤', art='assets/vein/art_drop.png'),
        dict(text='ハーバード・ヘルスの解説は、静脈は、実際には青くない、と述べています。', big='実際には青くない', sub='皮膚による、光の吸収の仕方による、錯覚', src='ハーバード・ヘルス', art='assets/vein/art_sunlight.png'),
        dict(text='教科書の図で、静脈が青く描かれるのは、動脈と区別するためだと説明されています。', big='図の青は、区別の色', art='assets/vein/art_book.png', col='white'),
        dict(text='光の通り方など、くわしいことは、長い動画で、確かめています。', end=True, art='assets/vein/art_heart.png'),
    ]))

J('koku', dict(
    title='江戸の一刻は、いつも2時間？',
    long_id='AcW0KC8O7FY',
    long_title='江戸の「一刻」は、いつも同じ長さだったのか？ 夏と冬で何分違うのか確かめる',
    pron='data/koku_pronunciations.json',
    art='assets/koku/art_edo.png',
    hook='「一刻は、およそ二時間」と言われます。でも、夏でも冬でも同じだったのでしょうか。大阪工業大学の論文の計算例で確かめます。',
    notes='■ 動画で確かめたこと\n・江戸時代の暮らしでは、昼と夜をそれぞれ六つに分ける不定時法が使われていました（国立天文台）。\n・計算例（北緯35度・東経135度）では、昼の一刻は夏至のころ約2時間36分、冬至のころ約1時間49分です（大阪工業大学・真貝寿明氏の論文）。\n・この数字は計算例で、江戸で実際に鳴った鐘の記録ではありません。',
    scenes=[
        dict(text='時代劇でおなじみの「一刻」。「一刻は、およそ二時間」と説明されることがあります。', big='一刻は、約2時間？', art='assets/koku/art_edo.png'),
        dict(text='江戸時代の暮らしでは、昼と夜を、それぞれ六つに等分する、不定時法が使われていました。', big='昼と夜を、六つに分ける', art='assets/koku/art_sunrise.png', col='white'),
        dict(text='計算例では、昼の一刻は、夏至のころ約二時間三十六分です。', big='夏至：約2時間36分', sub='北緯35度・東経135度の計算例', src='大阪工業大学の論文', art='assets/koku/art_sundial.png'),
        dict(text='冬至のころは、約一時間四十九分まで、短くなります。', big='冬至：約1時間49分', art='assets/koku/art_bell.png'),
        dict(text='昼と夜をならすと、ちょうど二時間。一刻は約二時間という目安は、成り立ちます。', big='ならすと、ちょうど2時間', sub='数字は計算例で、実際の鐘の時刻とは、ずれる場合があります', art='assets/koku/art_wadokei.png', col='white'),
        dict(text='くわしい計算は、長い動画で、確かめています。', end=True, art='assets/koku/art_meiji.png'),
    ]))

J('compass', dict(
    title='方位磁針は、北極点を指す？',
    long_id='zqHvAQwYC2I',
    long_title='方位磁針は、北極点を指している？ NOAAと国土地理院の解説で確かめる',
    pron='data/compass_pronunciations.json',
    art='assets/compass/art_desk.png',
    hook='「方位磁針は、北極点を指している」と思っていませんか。NOAAと国土地理院の解説から、磁針が何を指しているのかを確かめます。',
    notes='■ 動画で確かめたこと\n・方位磁石が指す北を磁北と呼びます（国土地理院）。磁針は、その場所の磁場の水平な成分の向きを指します（NOAA）。\n・北の磁極は、2025年のモデルで北緯約85.8度、東経約139度です（NOAA）。北極点（北緯90度）から緯度で約4.2度、距離にすると約470kmの計算です（自作の計算）。\n・磁北と真北のずれ（偏角）は、場所と時間で変わります。あなたが使う場所と日時での正確な偏角は確認していません。',
    scenes=[
        dict(text='「方位磁針は、北極点を指している」。そう思っていませんか。', big='磁針は、北極点を指す？', art='assets/compass/art_desk.png'),
        dict(text='国土地理院の解説では、方位磁石が指す北を、磁北と呼びます。', big='磁北', sub='方位磁石が指す北', src='国土地理院', art='assets/compass/art_hiker.png'),
        dict(text='真北は、地理上の北極点へ向かう方向です。磁北は、この真北と、必ずしも一致しません。', big='真北 と 磁北は、ちがう', art='assets/compass/art_globe.png', col='white'),
        dict(text='二〇二五年のモデルでは、北の磁極は、北極点から、約四百七十キロメートル離れています。', big='北極点から、約470km', sub='自作の計算（緯度で約4.2度）', src='NOAAのモデルから', art='assets/compass/art_arctic.png'),
        dict(text='磁北と真北のずれ、偏角は、場所と時間で変わります。', big='ずれは、場所と時間で変わる', art='assets/compass/art_closeup.png', col='white'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/compass/art_ship.png'),
    ]))

J('season', dict(
    title='夏が暑いのは、太陽に近いから？',
    long_id='SrpCtfIcU4Y',
    long_title='夏が暑いのは、地球が太陽に近いから？ NASAの解説と簡単な計算で確かめる',
    pron='data/season_pronunciations.json',
    art='assets/season/art_summer.png',
    hook='「夏が暑いのは、地球が太陽に近づくから」と思っていませんか。NASAの解説と簡単な計算で、季節の原因を確かめます。',
    notes='■ 動画で確かめたこと\n・近日点は1月、遠日点は7月です。北半球が夏の7月に、地球は太陽から最も遠くなります（NASA）。\n・季節の主な原因は、地軸の傾き（約23.4度）です（NASA）。\n・近日点と遠日点の光の強さの差は約7%の計算です。距離を同じとして北緯35度の正午を比べると、夏至は冬至の約1.9倍です（自作の計算。大気は無視）。\n・距離の差が各地の気温を何度変えるのかは、確認していません。',
    scenes=[
        dict(text='「夏が暑いのは、地球が太陽に近づくから」。そう思っていませんか。', big='夏は、太陽に近いから？', art='assets/season/art_summer.png'),
        dict(text='近日点は一月、遠日点は七月に、訪れます。', big='近いのは1月、遠いのは7月', art='assets/season/art_space.png', col='white'),
        dict(text='つまり、北半球が夏の七月に、地球は、太陽から最も遠くなります。', big='夏の7月に、一番遠い', sub='距離が原因なら、説明がつかない', src='NASAの解説', art='assets/season/art_sun.png'),
        dict(text='NASAの解説では、季節は、地球の、傾いた地軸によって、生じます。', big='季節の原因は、地軸の傾き', art='assets/season/art_tilt.png', col='white'),
        dict(text='光の強さの差は、距離では約七パーセント。正午の太陽の高さによる差のほうが、上回る計算です。', big='距離：約7%の差', sub='自作の計算（北緯35度・正午・大気は無視）', art='assets/season/art_winter.png'),
        dict(text='くわしい計算は、長い動画で、確かめています。', end=True, art='assets/season/art_seasons.png'),
    ]))

J('calendar', dict(
    title='明治5年は、12月が2日だけ？',
    long_id='xBrcDEN8tmk',
    long_title='明治5年は、12月が2日で終わった？ 国立国会図書館と国立天文台で確かめる',
    pron='data/calendar_pronunciations.json',
    art='assets/calendar/art_flip.png',
    hook='日本には、十二月が二日で終わった年があります。国立国会図書館と国立天文台の解説から、何が起きたのかを確かめます。',
    notes='■ 動画で確かめたこと\n・旧暦の明治5年12月3日が、明治6年1月1日になりました。12月は1日と2日の2日間だけでした（国立天文台・国立国会図書館）。\n・日が消えたのではなく、日付の数え方が切り替わりました。\n・改暦の背景として、欧米との統一のほか、閏月と月給にまつわる財政の事情が挙げられています。どちらが決め手だったのかは、決められません。',
    scenes=[
        dict(text='日本には、十二月が、二日で終わった年があります。', big='12月が、2日で終わった年', art='assets/calendar/art_flip.png'),
        dict(text='明治五年の十二月二日の、次の日は、明治六年の、一月一日でした。', big='12月2日の次は、翌年1月1日', art='assets/calendar/art_diary.png', col='white'),
        dict(text='十一月九日の布告で、旧暦の明治五年十二月三日を、明治六年一月一日とする、と定めています。', big='12月3日 が 1月1日に', sub='十一月九日の布告', src='国立国会図書館・国立天文台', art='assets/calendar/art_meiji.png'),
        dict(text='日が、消えたわけではありません。続いている日の、数え方が、切り替わったのです。', big='日は消えていない', art='assets/calendar/art_moon.png', col='white'),
        dict(text='どちらが決め手だったのかは、これらの解説だけでは、決められません。', big='理由は、決められない', sub='欧米との統一／閏月と月給の財政', art='assets/calendar/art_ledger.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/calendar/art_desk.png'),
    ]))

J('gdp', dict(
    title='家事を外注すると、GDPは増える？',
    long_id='NMTirenWL9M',
    long_title='家事を外注すると、GDPは増える？ 内閣府の資料で、数字を確かめる',
    pron='data/gdp_pronunciations.json',
    art='assets/gdp/art_house.png',
    hook='「家事を外注すると、GDPが増える」と聞いたことはありませんか。内閣府の資料から、記録の扱いと推計額を確かめます。',
    notes='■ 動画で確かめたこと\n・国民経済計算では、有償の家事サービスは生産として記録され、市場を介さない自分の家事は、中心となる勘定には記録されません（内閣府）。\n・二〇二一年の無償労働の評価額は、機会費用法で約百四十六兆円、名目GDPの二十六点六パーセントです（内閣府）。\n・評価額は賃金の取り方で変わり、名目GDPの十九点二から二十六点六パーセントまでの幅があります（内閣府）。\n・この推計は中心の勘定とは別のサテライト勘定で、GDPに足して、経済が大きくなったとは言えません（内閣府）。',
    scenes=[
        dict(text='「家事を外注すると、GDPが増える」と聞いたことはありませんか。', big='外注すると、GDPは増える？', art='assets/gdp/art_house.png'),
        dict(text='同じ掃除でも、自分ですると、お金は動きません。業者に頼むと、料金は業者の売上になります。', big='同じ掃除、2つの場合', art='assets/gdp/art_tools.png', col='white'),
        dict(text='内閣府の資料では、有償の家事は生産として記録されます。自分の家事は、中心の勘定には記録されません。', big='有償は記録、無償は記録外', sub='中心となる勘定での扱い', src='内閣府', art='assets/gdp/art_ledger.png'),
        dict(text='二〇二一年の無償労働の推計は、機会費用法で約百四十六兆円。名目GDPの二十六点六パーセントです。', big='2021年 約146兆円', sub='名目GDPの26.6%（機会費用法）', src='内閣府', art='assets/gdp/art_y2021.png', col='white'),
        dict(text='ただし、この額をGDPに足すことはできません。評価額は賃金の取り方で、十九点二から二十六点六パーセントまで変わります。', big='GDPに足すことはできない', sub='評価額は19.2〜26.6%（名目GDP比）', src='内閣府', art='assets/gdp/art_city.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/gdp/art_end.png'),
    ]))

J('scurvy', dict(
    title='壊血病は、レモンで解決した？',
    long_id='c9vR4yp4U0A',
    long_title='壊血病は、「レモンが効く」と分かったら解決したのか？ リンドの試験を確かめる',
    pron='data/scurvy_pronunciations.json',
    art='assets/scurvy/art_deck.png',
    hook='「リンドがレモンの効果を発見したのに、海軍が採用せず、対策が遅れた」。この話を、ミルンさんの論文から確かめます。',
    notes='■ 動画で確かめたこと\n・一七四七年五月、軍艦ソールズベリーの上で、壊血病の水兵十二人を二人ずつ六組に分け、十四日間、別々の処置を試した記録があります（リンド『壊血病論』、ミルン二〇一二年）。\n・最も早く、はっきりした効果が見られたのは、オレンジとレモンでした。与えられたのは六日間だけです（ミルン二〇一二年）。\n・ミルンさんは、リンドの本で、柑橘の果汁が治療になると明確に述べられていない、と指摘しています（ミルン二〇一二年）。\n・柑橘が効く話はリンド以前から記録され、広まらなかった要因として、値段と傷みやすさ、ビタミンの概念の不在が挙げられています（ミルン二〇一二年）。',
    scenes=[
        dict(text='昔の船乗りを苦しめた、壊血病。「レモンが効くと分かっていたのに、対策が遅れた」と語られます。', big='レモンで、解決した？', art='assets/scurvy/art_deck.png'),
        dict(text='一七四七年、軍艦ソールズベリーで、水兵十二人を二人ずつ六組に分け、十四日間、別々の処置を試しました。', big='1747年、12人を6組に', sub='軍艦ソールズベリーの上で', src='リンドの記録', art='assets/scurvy/art_sickbay.png', col='white'),
        dict(text='最も早く効果が見られたのは、オレンジとレモン。ただし、与えられたのは六日間だけでした。', big='効果は、オレンジとレモン', sub='ただし、与えられたのは6日間', src='リンドの記録', art='assets/scurvy/art_why.png'),
        dict(text='ミルンさんの指摘では、リンドの本に、柑橘が治療になるとは、明確に書かれていません。', big='本には、明確に書いていない', src='ミルン（2012）', art='assets/scurvy/art_book.png', col='white'),
        dict(text='柑橘が効く話は、リンド以前から記録されています。広まらなかった理由には、値段と傷みやすさ、ビタミンの概念の不在が挙げられます。', big='広まらなかった理由', sub='値段・傷みやすさ・ビタミン未発見', art='assets/scurvy/art_harbor.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/scurvy/art_end.png'),
    ]))

J('einstein', dict(
    title='アインシュタインは、数学で落第した？',
    long_id='sVMwrN1fomA',
    long_title='アインシュタインは、数学が苦手な落第生だった？ 入学試験の記録で確かめる',
    pron='data/einstein_pronunciations.json',
    art='assets/einstein/art_study.png',
    hook='「天才アインシュタインは、数学が苦手で、落第した」。ETH図書館とスイス歴史事典の記録から、入学試験の実際を確かめます。',
    notes='■ 動画で確かめたこと\n・一八九五年十月、アインシュタインはチューリヒの連邦工科大学の入学試験を受け、不合格でした（ETH図書館・スイス歴史事典）。\n・数学と自然科学は優れた成績で、不十分だったのは語学と歴史でした（ETH図書館）。\n・不合格の理由として挙げられているのは、数学ではなく、数学以外の科目です（ETH図書館・スイス歴史事典）。\n・「数学で落第」という話は、新聞のコラム、リプリーズに載ったとされ、本人は否定したと報じられています（TIME誌）。\n・具体的な点数や成績表の数値は、確認していません。',
    scenes=[
        dict(text='「天才アインシュタインは、数学が苦手で、落第した」。そんな話を、聞いたことはありませんか。', big='数学で、落第した？', art='assets/einstein/art_study.png'),
        dict(text='入学試験に落ちたのは、本当のようです。一八九五年、チューリヒの連邦工科大学を受験しました。', big='1895年、入学試験', sub='チューリヒの連邦工科大学', src='ETH図書館', art='assets/einstein/art_exam.png', col='white'),
        dict(text='数学と自然科学は、優れた成績。不十分だったのは、語学と歴史でした。', big='数学は、優れていた', sub='不十分だったのは、語学と歴史', src='ETH図書館', art='assets/einstein/art_result.png'),
        dict(text='総合では不合格。理由として挙げられているのは、数学ではなく、数学以外の科目です。', big='不合格の理由は、数学ではない', art='assets/einstein/art_board.png', col='white'),
        dict(text='「数学で落第」という話は、新聞のコラム、リプリーズに載ったとされています。本人は、数学で落第したことはない、と答えたとされています。', big='話のもとは、リプリーズ', sub='本人は「落第したことはない」', src='TIME誌', art='assets/einstein/art_paper.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/einstein/art_study.png'),
    ]))

J('zenzen', dict(
    title='「全然おいしい」は、間違い？',
    long_id='T2b_wiN9xow',
    long_title='「全然おいしい」は最近の間違い？ 昔の文章と研究で、「全然」の歴史を確かめる',
    pron='data/zenzen_pronunciations.json',
    art='assets/zenzen/art_cafe.png',
    hook='「全然おいしい」は、最近生まれた間違いなのでしょうか。青空文庫の小説と国立国語研究所の記事から、「全然」の使われ方を確かめます。',
    notes='■ 動画で確かめたこと\n・「ない」などの打ち消しを伴わない「全然」は、明治から昭和はじめの文章にも用例があります（青空文庫・国立国語研究所）。\n・ただし「悪い」「不同意」「支配」など、意味が否定的な言葉との組み合わせが多く、いまの「全然おいしい」と同じ使い方とは限りません（青空文庫）。\n・「否定と呼応するのが正しい」とされたのは戦後だ、という指摘があります（国立国語研究所）。\n・いまの「全然おいしい」が昔の使い方の続きなのか、別の使い方なのかは、決められません（国立国語研究所）。\n・現代の使われ方の数字や、辞書の記述は、確認していません。',
    scenes=[
        dict(text='「全然おいしい」「全然大丈夫」。最近の間違いだと、言われることがあります。', big='「全然おいしい」は、間違い？', art='assets/zenzen/art_cafe.png'),
        dict(text='夏目漱石の『坊っちゃん』には、「一体生徒が全然悪るいです」。芥川龍之介の『羅生門』にも、「全然、自分の意志に支配されている」とあります。', big='昔の小説にも、用例がある', sub='『坊っちゃん』『羅生門』', src='青空文庫', art='assets/zenzen/art_novel.png', col='white'),
        dict(text='ただし、いずれも「悪い」「支配」と、意味が否定的な言葉との組み合わせです。いまの「全然おいしい」と同じ使い方とは、限りません。', big='同じ使い方とは、限らない', sub='否定的な意味の言葉との組み合わせ', src='青空文庫', art='assets/zenzen/art_dict.png'),
        dict(text='国立国語研究所の記事によると、「否定と呼応するのが正しい」とされたのは、戦後です。', big='正しいとされたのは、戦後', sub='否定と呼応する、という規範', src='国立国語研究所', art='assets/zenzen/art_study.png', col='white'),
        dict(text='では、「全然おいしい」は、最近生まれた間違いなのでしょうか。この資料だけでは、決められません。', big='間違いと、言い切れる？', sub='昔の用法の続きかは、決められない', art='assets/zenzen/art_cafe.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/zenzen/art_study.png'),
    ]))

J('rain30', dict(
    title='降水確率30％は、地域の30％で雨？',
    long_id='SwT2kd1obFg',
    long_title='降水確率30％は、地域の30％で雨が降る？ 気象庁の解説で確かめる',
    pron='data/rain30_pronunciations.json',
    art='assets/rain30/art_intro.png',
    hook='「降水確率30％は、地域の30％で雨が降る」と思っていませんか。気象庁の解説から、降水確率の意味を確かめます。',
    notes='■ 動画で確かめたこと\n・降水確率は、指定された時間帯の間に、1ミリ以上の降水がある確率です（気象庁）。\n・予報が出される地域内の、どの点でも同じ確率として定義されます。地域の30％の面積で降る、という意味ではありません（気象庁）。\n・降水量の多少は示していません（気象庁）。\n・実際に雨が降るかどうか、降水量の多少までは、この数字だけでは決められません。',
    scenes=[
        dict(text='「降水確率が三十パーセントなら、その地域の三十パーセントで、雨が降る」。そう思っていませんか。', big='30％は、地域の30％？', art='assets/rain30/art_intro.png'),
        dict(text='気象庁の解説によると、降水確率は、指定された時間帯の間に、一ミリ以上の降水がある確率です。', big='1ミリ以上の降水がある確率', src='気象庁', art='assets/rain30/art_def.png', col='white'),
        dict(text='予報が出される地域内の、どの点でも、同じ確率として定義されます。', big='どの点でも、同じ確率', art='assets/rain30/art_meaning.png'),
        dict(text='つまり、地域の三十パーセントの面積で、雨が降る、という意味ではありません。', big='面積の30％、ではない', art='assets/rain30/art_amount.png', col='white'),
        dict(text='また、降水量の多少は、この数字では示されていません。', big='雨の強さは、示さない', sub='強い雨か、弱い雨かは、この数字だけでは決められない', src='気象庁', art='assets/rain30/art_verify.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/rain30/art_end.png'),
    ]))

J('islands', dict(
    title='日本の島は、2倍に増えた？',
    long_id='UIDRLw9UOXg',
    long_title='日本の島は、本当に2倍に増えた？ 国土地理院の解説で確かめる',
    pron='data/islands_pronunciations.json',
    art='assets/islands/art_intro.png',
    hook='日本の島の数として公表された数字が、6,852島から14,125島に変わりました。本当に島は増えたのでしょうか。国土地理院の解説で確かめます。',
    notes='■ 動画で確かめたこと\n・6,852島は海上保安庁が昭和62年に公表した数字、14,125島は国土地理院が2023年2月に公表した数字です。\n・国土地理院は、大きく異なるのは測量技術の進歩による地図表現の詳細化が大きく影響していると考えられる、と説明しています。\n・新しい島が見つかったわけではなく、電子国土基本図に描かれた陸地を、一定の条件で数えた結果です。\n・昭和62年の調査の詳しい数え方、都道府県別の島の数は、この動画の資料だけでは分かりません。',
    scenes=[
        dict(text='日本の島の数として公表された数字が、六千八百五十二島から、一万四千百二十五島に、変わりました。', big='6,852島 → 14,125島', art='assets/islands/art_intro.png'),
        dict(text='六千八百五十二島は、海上保安庁が、昭和六十二年に公表した数字です。', big='昭和62年：6,852島', src='海上保安庁の公表', art='assets/islands/art_nums.png', col='white'),
        dict(text='一万四千百二十五島は、国土地理院が、二千二十三年二月に公表した数字です。', big='2023年2月：14,125島', src='国土地理院の公表', art='assets/islands/art_count.png'),
        dict(text='国土地理院によると、測量技術の進歩による、地図表現の詳細化が、大きく影響していると、考えられます。', big='地図の表現が、細かくなった', src='国土地理院', art='assets/islands/art_new.png', col='white'),
        dict(text='新しい島が、見つかったわけでは、ありません。', big='新しい島が見つかったわけではない', sub='地図に描かれた陸地を、一定の条件で数えた結果', src='国土地理院', art='assets/islands/art_land.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/islands/art_end.png'),
    ]))

J('magnitude', dict(
    title='マグニチュード+1で、10倍強い？',
    long_id='q18--lhsm_8',
    long_title='マグニチュードが1増えると地震は10倍強い？ 気象庁の解説で確かめる',
    pron='data/magnitude_pronunciations.json',
    art='assets/magnitude/art_intro.png',
    hook='「マグニチュードが1大きいと、地震のエネルギーは10倍強」と思っていませんか。気象庁の解説から、確かめます。',
    notes='■ 動画で確かめたこと\n・マグニチュードは地震そのものの大きさ（規模）、震度はある場所での揺れの強さを表します（気象庁）。\n・マグニチュードの値が1大きくなると、エネルギーは約32倍、2大きくなると約1,000倍になります（気象庁）。\n・マグニチュードの数字だけでは、あなたのいる場所の震度は決められません。',
    scenes=[
        dict(text='「マグニチュードが一つ大きくなると、地震のエネルギーは、十倍強になる」。そう思っていませんか。', big='M+1で、10倍強？', art='assets/magnitude/art_intro.png'),
        dict(text='気象庁によると、マグニチュードは、地震そのものの大きさを表します。震度は、ある場所での、揺れの強さです。', big='M＝地震の大きさ\u3000震度＝揺れの強さ', src='気象庁', art='assets/magnitude/art_diff.png', col='white'),
        dict(text='マグニチュードの値が、一大きくなると、エネルギーは、約三十二倍になります。', big='+1で、約32倍', src='気象庁', art='assets/magnitude/art_energy.png'),
        dict(text='二大きくなると、約千倍です。十倍強では、ありません。', big='+2で、約1,000倍', sub='約32倍を2回かけると約1,000（自作の計算）', art='assets/magnitude/art_dist.png', col='white'),
        dict(text='ただし、マグニチュードの数字だけでは、あなたのいる場所の震度は、決められません。', big='場所の揺れは、M だけでは決まらない', art='assets/magnitude/art_end.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/magnitude/art_end.png'),
    ]))

J('yakubusoku', dict(
    title='「役不足」の本当の意味は？',
    long_id='h6C7OPst0zg',
    long_title='「役不足」は、能力が足りない意味？ 文化庁の調査で確かめる',
    pron='data/yakubusoku_pronunciations.json',
    art='assets/yakubusoku/art_intro.png',
    hook='「彼には役不足の仕事だ」。この言葉は、能力が足りない、という意味でしょうか。文化庁の調査の結果から確かめます。',
    notes='■ 動画で確かめたこと\n・文化庁の調査では、「本人の力量に対して、役目が軽すぎること」が本来の意味とされています（文化庁「国語に関する世論調査」平成14年度・平成18年度）。\n・平成14年度は「重すぎる」が62.8％、「軽すぎる」が27.6％。平成18年度は50.3％と40.3％でした。\n・この数字は、調査年度のものです。いまの割合を示すものではありません。',
    scenes=[
        dict(text='「彼には役不足の仕事だ」。この「役不足」は、彼の力量に対して、仕事が重すぎる、という意味でしょうか。', big='「役不足」の意味は？', art='assets/yakubusoku/art_intro.png'),
        dict(text='文化庁は、本来の意味を、本人の力量に対して、役目が軽すぎること、としています。', big='本来は「役目が軽すぎる」', src='文化庁', art='assets/yakubusoku/art_ask.png', col='white'),
        dict(text='平成十四年度の調査では、重すぎる、と答えた人が、六十二・八パーセント。軽すぎる、は二十七・六パーセントでした。', big='62.8％\u3000対\u300027.6％', sub='平成14年度の調査', src='文化庁', art='assets/yakubusoku/art_result.png'),
        dict(text='平成十八年度は、五十・三パーセントと、四十・三パーセント。差は、縮まりました。', big='50.3％\u3000対\u300040.3％', sub='平成18年度の調査', src='文化庁', art='assets/yakubusoku/art_meaning.png', col='white'),
        dict(text='ただし、これは、調査に答えた人が選んだ意味の割合です。いまの割合では、ありません。', big='いまの割合では、ない', art='assets/yakubusoku/art_end.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/yakubusoku/art_end.png'),
    ]))

J('leapsecond', dict(
    title='うるう秒は、なぜやめる？',
    long_id='JkPCUodEGfE',
    long_title='うるう秒は、なぜやめる？ 国際度量衡総会の決議を確かめる',
    pron='data/leapsecond_pronunciations.json',
    art='assets/leapsecond/art_intro.png',
    hook='日本時間の2017年1月1日、「8時59分60秒」が入りました。うるう秒です。このうるう秒をやめる決議が、2026年に出されました。なぜなのか、資料で確かめます。',
    notes='■ 動画で確かめたこと\n・うるう秒は、原子時計をもとにした協定世界時と、地球の自転に基づく時刻のずれを、0.9秒以内に保つために、1秒を入れる仕組みです（総務省）。\n・2026年の国際度量衡総会の決議5は、2027年5月20日から、うるう秒による調整をしない連続した協定世界時とします。ずれの許容上限は3,600秒（1時間）で、実際のずれが1時間になるという意味ではありません（BIPM）。\n・前文は、負のうるう秒は一度も使われておらず、重要な設備には高いリスクがある、2035年までに必要になる確率は30％という見積もりがある、としています（BIPM）。',
    scenes=[
        dict(text='二千十七年の元日、日本時間の午前八時五十九分五十九秒。その次に、「八時五十九分六十秒」が入りました。', big='8時59分60秒', art='assets/leapsecond/art_intro.png'),
        dict(text='うるう秒は、協定世界時と、地球の自転に基づく時刻の、ずれを、小さく保つための仕組みです。', big='ずれを、0.9秒以内に', src='総務省', art='assets/leapsecond/art_in.png', col='white'),
        dict(text='そのうるう秒を、やめる決議が、二千二十六年の、国際度量衡総会で出されました。', big='うるう秒を、やめる決議', src='BIPM（国際度量衡総会）', art='assets/leapsecond/art_out.png'),
        dict(text='理由の一つは、一秒を抜く、負のうるう秒が、これまで一度も使われていないことです。', big='負のうるう秒は、一度も使われていない', sub='決議：重要な設備には、高いリスク', art='assets/leapsecond/art_change.png', col='white'),
        dict(text='ずれの許容上限は、一時間に広がります。ただし、実際のずれが、すぐ一時間になる、という意味では、ありません。', big='上限が1時間。実際のずれ、ではない', art='assets/leapsecond/art_end.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/leapsecond/art_end.png'),
    ]))

J('moon', dict(
    title='月は自転していない？',
    long_id='q8-ufW5IuA0',
    long_title='月はいつも同じ面を見せる。自転していない？ NASAの解説で確かめる',
    pron='data/moon_pronunciations.json',
    art='assets/moon/art_intro.png',
    hook='「月はいつも同じ面を地球に見せているから、自転していない」と思っていませんか。NASAの解説から、月の動きを確かめます。',
    notes='■ 動画で確かめたこと\n・月は、地球のまわりを一周するあいだに、一回、自転します（NASA）。この状態を潮汐ロックと呼びます。\n・同じ面が見え続けるのは、自転と公転の時間が同じだからです（NASA）。\n・地球から見えない側を「暗い側」と呼ぶのは誤解を招く、とNASAは説明しています。\n・自転と公転の周期の、細かい日数は、この動画の資料だけでは決められません。',
    scenes=[
        dict(text='「月は、いつも同じ面を、地球に見せている。だから、自転していない」。そう思っていませんか。', big='月は、自転していない？', art='assets/moon/art_intro.png'),
        dict(text='NASAの解説によると、月は、地球のまわりを一周するあいだに、一回、自転します。', big='一周で、一回、自転', src='NASA', art='assets/moon/art_motion.png', col='white'),
        dict(text='同じ面が見え続けるのは、自転と公転の時間が、同じだからです。', big='自転と公転の時間が、同じ', art='assets/moon/art_sync.png'),
        dict(text='自転しない月なら、地球からは、月のさまざまな面が、順に見えるはずです。', big='自転しなければ、いろいろな面が見える', sub='自作の模式図で比べています', art='assets/moon/art_why.png', col='white'),
        dict(text='見えない側にも、昼と夜があります。NASAは、暗い側という呼び方は、誤解を招く、としています。', big='見えない側にも、昼がある', src='NASA', art='assets/moon/art_dark.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/moon/art_end.png'),
    ]))

J('sunrise', dict(
    title='日の出が一番早いのは夏至の日？',
    long_id='BeY3kMjDjzs',
    long_title='日の出が一番早いのは、夏至の日？ 国立天文台の暦で確かめる',
    pron='data/sunrise_pronunciations.json',
    art='assets/sunrise/art_intro.png',
    hook='昼が一番長い夏至の日に、日の出も一番早いのでしょうか。国立天文台の説明と、東京の暦で確かめます。',
    notes='■ 動画で確かめたこと\n・国立天文台の説明では、日の出が最も早い日は夏至の約1週間前、日の入りが最も遅い日は約1週間後です。\n・東京の2027年の暦（国立天文台暦計算室）では、日の出は6月6日〜21日が毎日4時25分で、夏至（6月21日）も同じです。日の入りは、夏至の日が19時00分、6月24日〜7月5日が19時01分でした。\n・暦は分単位なので、東京の暦だけでは、一番早い一日は決められません。',
    scenes=[
        dict(text='昼が一番長い日は、夏至です。では、日の出が一番早い日も、夏至でしょうか。', big='日の出が一番早いのは、夏至の日？', art='assets/sunrise/art_intro.png'),
        dict(text='国立天文台は、日の出が最も早い日は、夏至の約一週間前、と説明しています。', big='夏至の、約1週間前', src='国立天文台', art='assets/sunrise/art_rise.png', col='white'),
        dict(text='東京の二千二十七年の暦では、六月六日から夏至の日まで、日の出は毎日、四時二十五分です。', big='6月6日〜21日：毎日、4時25分', src='国立天文台 暦計算室', art='assets/sunrise/art_set.png'),
        dict(text='日の入りは、夏至のあとも遅くなり、六月二十四日から、十九時一分になります。', big='夏至のあとも、日の入りは遅くなる', sub='6月24日〜7月5日：19時01分', art='assets/sunrise/art_why.png', col='white'),
        dict(text='理由は、南中の時刻が、毎日、少しずつ遅くなるためです。ただし、暦は分単位で、一番早い一日は、決められません。', big='理由は、南中の時刻の変化', art='assets/sunrise/art_end.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/sunrise/art_end.png'),
    ]))

J('venus', dict(
    title='金星では、1日が1年より長い？',
    long_id='qZBtCpOCa6o',
    long_title='金星では、1日が1年より長い？ NASAの表で確かめる',
    pron='data/venus_pronunciations.json',
    art='assets/venus/art_intro.png',
    hook='「金星では、一日が一年より長い」と聞いたことはありませんか。NASAの表の数字で確かめます。',
    notes='■ 動画で確かめたこと\n・NASAの表では、金星の自転周期（星を基準）は5,832.6時間で約243日、公転周期は224.701日です。自転一回のほうが長くなります。\n・同じ表の「Length of day」（太陽が正午の位置に戻るまでの平均の時間）は2,802.0時間＝116.75日で、公転周期より短くなります。\n・自転が公転と反対向きなので、太陽が戻るのが早くなります（日数への換算と検算は自作の計算）。',
    scenes=[
        dict(text='金星では、一日が、一年より長い。そう聞いたことはありませんか。', big='金星：一日 ＞ 一年？', art='assets/venus/art_intro.png'),
        dict(text='NASAの表では、金星が自転で一回転する時間は、約二百四十三日です。', big='自転一回：約243日', src='NASA', art='assets/venus/art_nums.png', col='white'),
        dict(text='公転で、太陽のまわりを一周する時間は、二百二十四・七日です。', big='公転一周：224.7日', src='NASA', art='assets/venus/art_sun.png'),
        dict(text='つまり、自転一回のほうが、長いのです。ただし、太陽が空の同じ位置に戻る周期は、百十六・七五日です。', big='太陽が戻る周期：116.75日', sub='自転が公転と反対向きだから', art='assets/venus/art_why.png', col='white'),
        dict(text='一日の意味が違えば、答えも変わります。', big='一日の意味で、答えが変わる', art='assets/venus/art_end.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/venus/art_end.png'),
    ]))

J('oceanblue', dict(
    title='海が青いのは、空が映っているから？',
    long_id='31mlleqtpsM',
    long_title='海が青いのは、空が映っているから？ NOAAの解説で確かめる',
    pron='data/oceanblue_pronunciations.json',
    art='assets/oceanblue/art_intro.png',
    hook='「海が青いのは、空が映っているから」と思っていませんか。NOAAとウッズホール海洋研究所の解説で確かめます。',
    notes='■ 動画で確かめたこと\n・空は水面では映りますが、水面の下に潜っても青は残ります（WHOI）。\n・海が青い主な理由は、水が光の赤い側の色を吸収し、青い側の色が残るからです（NOAA）。\n・赤やオレンジは数メートルでほとんど消え、青と紫が最も深くまで届きます（WHOI）。\n・吸収と散乱が色にどのくらい影響するかの割合は、この動画の資料だけでは分かりません。',
    scenes=[
        dict(text='海が青いのは、空が青くて、その空が、水面に映っているから。そう思っていませんか。', big='海が青いのは、空が映るから？', art='assets/oceanblue/art_intro.png'),
        dict(text='空が映るのは、本当です。でも、水面の下に潜っても、青い色は、残ります。', big='水の下でも、青は残る', src='ウッズホール海洋研究所', art='assets/oceanblue/art_sky.png', col='white'),
        dict(text='NOAAによると、海が青いのは、水が、光の赤い側の色を、吸収するからです。', big='水が、赤い側の色を吸収', src='NOAA', art='assets/oceanblue/art_light.png'),
        dict(text='赤やオレンジは、数メートルでほとんど消え、青と紫が、最も深くまで届きます。', big='青い光が、最後まで残る', src='ウッズホール海洋研究所', art='assets/oceanblue/art_colors.png', col='white'),
        dict(text='海は、空を映すだけの、鏡ではありません。水が、光の色を選んで吸収するのです。', big='海は、空を映すだけの鏡ではない', art='assets/oceanblue/art_end.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/oceanblue/art_end.png'),
    ]))

J('oke', dict(
    title='2万5千の大軍は、なぜ敗れた？',
    long_id='id1hjqjrztY',
    long_title='2万5千の大軍は、なぜ敗れたのか？ 桶狭間の戦いを史料の数字から確かめる',
    pron='data/oke_pronunciations.json',
    art='assets/okehazama/art_field_dusk.png',
    hook='「2万5千の大軍が、3千にも満たない軍に敗れた」。桶狭間の戦いを、公開されている史料の数字から確かめます。',
    notes='■ 動画で確かめたこと\\n・永禄3年5月19日、尾張国の桶狭間で、織田信長の軍が今川義元を討ち取りました（ウィキペディア日本語版「桶狭間の戦い」）。\\n・今川軍の兵力は2万5千とされますが、『信長公記』は4万5千、『甲陽軍鑑』は2万余、『武功夜話』は3万有余、『徳川実紀』などは4万余、『絵本太閤記』は5万余と、史料で違います。\\n・戦前に広く使われた2万5千は、陸軍参謀本部『日本戦史 桶狭間役』の数字です。小和田哲男さんは、義元の領地を90万石から100万石と見て2万5千としました。\\n・織田方が今川本陣を攻撃したのは約2千人、直接向き合った今川軍は5千人から6千人とされます。\\n・奇襲だったのか正面攻撃だったのか、桶狭間山の位置も、決まっていません。\\n・原史料は公開されている翻刻の範囲で確かめました。原本・影印本・専門書は未確認です。',
    scenes=[
        dict(text='永禄三年五月十九日、尾張国の桶狭間で、合戦がありました。二万五千の大軍を率いた今川義元が、討たれたのです。', big='2万5千 対 3千', art='assets/okehazama/art_field_dusk.png'),
        dict(text='相手は、三千にも満たない、織田信長の軍でした。', big='織田軍は、3千未満', sub='永禄3年5月19日・尾張国桶狭間', art='assets/okehazama/art_quiet_field.png', col='white'),
        dict(text='今川軍の兵力は、史料によって違います。『信長公記』は四万五千、『甲陽軍鑑』は二万余、『武功夜話』は三万有余と書きます。', big='史料で、数字が違う', sub='4万5千／2万余／3万有余', src='『信長公記』ほか', art='assets/okehazama/art_old_records.png'),
        dict(text='戦前に広く使われたのは、陸軍参謀本部の『日本戦史 桶狭間役』にある、二万五千です。', big='広まったのは、2万5千', sub='陸軍参謀本部『日本戦史 桶狭間役』', art='assets/okehazama/art_old_book.png', col='white'),
        dict(text='合戦の行われ方も、戦場の場所も、いまも議論が続いています。', big='奇襲か、正面か。場所も、議論', sub='桶狭間山の位置は、決まっていない', art='assets/okehazama/art_war_council.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/okehazama/art_downpour.png'),
    ]))

J('honnoji', dict(
    title='「敵は本能寺にあり」は、本当か？',
    long_id='84DQbeXhwfA',
    long_title='【経緯から丁寧に解説】本能寺の変 ― 光秀はどんな立場で、どの道を通って京都へ来たのか',
    pron='data/hn_pronunciations.json',
    art='assets/imagen/img_09_honnoji_night.webp',
    hook='「「敵は本能寺にあり」。この言葉は、同時代の史料には、見えません」。本能寺の変の経緯と、動機をめぐる諸説を確かめます。',
    notes='■ 動画で確かめたこと\n・天正10年（1582年）6月2日の未明、京都の本能寺で、織田信長が明智光秀の軍勢に取り囲まれ、亡くなりました。\n・光秀の兵は約1万3千ともいわれ、2万・3万とする説もあります。信長の側近は20〜30人とも150〜160人ともいわれ、確定していません。\n・「敵は本能寺にあり」は同時代の史料になく、江戸時代の書物で広まった俗説とされます。\n・動機には定説がありません。怨恨説・野望説・突発説・朝廷関与説・足利義昭説・四国説などがあり、どれも決め手を欠きます。\n・信長の遺体は確認されておらず、最期の様子も分かっていません。\n・出典は本編の概要欄にまとめています。',
    scenes=[
        dict(text='天正十年六月二日の未明、京都の本能寺で、織田信長が、明智光秀の軍勢に取り囲まれました。', big='1582年6月2日、本能寺', art='assets/imagen/img_09_honnoji_night.webp'),
        dict(text='光秀の兵は約一万三千。信長の側近は、二十人から三十人とも、百五十人から百六十人ともいわれます。', big='約1万3千 対 側近数十人', sub='側近の人数は、説が分かれる', art='assets/army_hn/akechi_00.png', col='white'),
        dict(text='「敵は本能寺にあり」。この言葉は、同時代の史料には、見えません。江戸時代の書物で広まった俗説とされます。', big='そのセリフは、史料にない', sub='同時代の記録には、残っていない', art='assets/imagen/img_05_kyoto_morning.webp'),
        dict(text='光秀がなぜ主君を討ったのか。実は、定説がありません。', big='動機に、定説はない', art='assets/portraits/mitsuhide.jpg', col='white'),
        dict(text='怨恨、野望、突発、朝廷、足利義昭、四国。どの説にも、決め手がありません。', big='6つの説、決め手なし', sub='怨恨／野望／突発／朝廷／義昭／四国', art='assets/imagen/img_11_renga.webp'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/imagen/img_03_honnoji_fire.webp'),
    ]))

J('ninja', dict(
    title='忍者は、黒装束だったのか？',
    long_id='flajM3xInYE',
    long_title='忍者は、黒装束で手裏剣を投げていたのか？ 国立国会図書館の解説で確かめる',
    pron='data/nj_pronunciations.json',
    art='assets/ndl_ninja/hokusai_black_ninja.jpg',
    hook='「忍者といえば、黒い装束に覆面、そして手裏剣」。そのイメージは、どこから来たのか。国立国会図書館の解説から確かめます。',
    notes='■ 動画で確かめたこと\n・国立国会図書館の解説は、忍者はもともと想像されるような特徴的な黒装束ではなかった、としています。\n・『正忍記』には、茶色・柿色・黒色・紺色を着ると書かれています。\n・黒装束と覆面を忍者の姿として描く表現は、18世紀の中ごろの歌舞伎や浄瑠璃から広まったと考えられています。\n・手裏剣そのものは実在しましたが、見つかっている忍術書に記述はなく、忍者が使った記録も見当たりません。\n・「忍者」という呼び名が広く定着したのは昭和30年代とされますが、二文字自体は1856年の『武用弁略』にも見えます。\n・個々の忍びが何をしたかは、資料だけでは決められません。\n・出典は本編の概要欄にまとめています。',
    scenes=[
        dict(text='忍者といえば、黒い装束に覆面、そして手裏剣。映画や漫画で、おなじみの姿です。', big='黒装束に、手裏剣？', art='assets/ndl_ninja/hokusai_black_ninja.jpg'),
        dict(text='国立国会図書館の解説では、忍者はもともと、特徴的な黒装束ではなかった、としています。', big='黒装束は、定番ではなかった', sub='国立国会図書館の解説', src='国立国会図書館', art='assets/ndl_ninja/shoninki_chi_p12.jpg', col='white'),
        dict(text='『正忍記』には、茶色、柿色、黒色、紺色を着る、と書かれています。', big='茶・柿・黒・紺', sub='目立たない色を、選んだ', art='assets/ndl_ninja/shoninki_chi_p13.jpg'),
        dict(text='黒装束と覆面の姿は、十八世紀の中ごろの、歌舞伎や浄瑠璃から広まった、と考えられています。', big='演劇から、広まった', art='assets/ndl_ninja/ehon_taikoki_kimura.jpg'),
        dict(text='手裏剣は実在しましたが、忍術書に記述はなく、忍者が使った記録も見当たりません。', big='忍術書に、手裏剣なし', sub='見つかっている忍術書に、記述はない', art='assets/ndl_ninja/hokusai_bar_shuriken.jpg', col='white'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/ndl_ninja/fujita_flat_shuriken.jpg'),
    ]))

J('worldmap', dict(
    title='世界地図は、大きさを間違えている？',
    long_id='HtZmfkJy9Eo',
    long_title='グリーンランドはアフリカに何個入る？ 地図の「大きさ」を計算で検証',
    pron='data/gm_pronunciations.json',
    art='assets/earth/overview.png',
    hook='「メルカトル図法の世界地図では、アフリカとグリーンランドが、同じくらいの大きさに見えます」。実際の面積と、地図の歪みを確かめます。',
    notes='■ 動画で確かめたこと\n・アフリカは約3,000万平方キロメートル、グリーンランドは約217万平方キロメートルで、その差は約14倍です。\n・メルカトル図法は1569年、航海のために作られました。狭い範囲では角度が正しく表される一方、緯度が高いほど面積が大きく見えます。\n・地球を球体とみなすと、緯度60度では面積が約4倍、緯度80度では約33倍に見えます。\n・面積を保つ図法（ガル・ピーターズ図法、イコール・アース図法など）もありますが、形は歪みます。\n・図法に絶対の正解はなく、目的によって選ぶものが変わります。\n・出典は本編の概要欄にまとめています。',
    scenes=[
        dict(text='アフリカと、グリーンランド。世界地図では、同じくらいの大きさに見えます。', big='同じくらいに、見える', art='assets/imagen/gm_thumb_globe_peel.webp'),
        dict(text='アフリカは約三千万平方キロメートル、グリーンランドは約二百十七万平方キロメートル。差は、約十四倍です。', big='実際は、約14倍', sub='アフリカ 約3,000万km²\nグリーンランド 約217万km²', art='assets/gm_short/map_portrait.png', col='white'),
        dict(text='地球は球体で、地図は平らです。球面を、伸び縮みなしで平面にすることは、できません。', big='球体は、平らにできない', art='assets/imagen/gm_thumb_globe_peel.webp'),
        dict(text='メルカトル図法は角度を保つ代わりに、緯度が高いほど面積が大きく見えます。緯度六十度で約四倍、八十度で約三十三倍。', big='緯度60°で4倍、80°で33倍', sub='面積の拡大率（地球を球体とみなす）', art='assets/gm_short/map_greenland_zoom.png', col='white'),
        dict(text='面積を保つ図法もありますが、形は歪みます。図法に、絶対の正解はありません。', big='正解は、目的で変わる', sub='面積を取るか、形を取るか', art='assets/imagen/gm_thumb_globe_peel.webp'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/imagen/gm_thumb_globe_peel.webp'),
    ]))
