"""Short用の spec（data/short_<slug>.json）その2：rain30・moon・islands・magnitude・yakubusoku・leapsecond・sunrise。台本は長尺の 09_script_v2.md の文言に合わせる。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]


def J(n, o):
    (R / 'data' / f'short_{n}.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')


J('rain30', dict(
    title='降水確率30％は、地域の30％で雨？', long_id='SwT2kd1obFg',
    long_title='降水確率30％は、地域の30％で雨が降る？ 気象庁の解説で確かめる',
    pron='data/rain30_pronunciations.json', art='assets/rain30/art_intro.png',
    hook='「降水確率30％は、地域の30％で雨が降る」と思っていませんか。気象庁の解説から、降水確率の意味を確かめます。',
    notes='■ 動画で確かめたこと\n・降水確率は、指定された時間帯の間に、1ミリ以上の降水がある確率です（気象庁）。\n・予報が出される地域内の、どの点でも同じ確率として定義されます。地域の30％の面積で降る、という意味ではありません（気象庁）。\n・降水量の多少は示していません（気象庁）。\n・実際に雨が降るかどうか、降水量の多少までは、この数字だけでは決められません。',
    scenes=[
        dict(text='「降水確率が三十パーセントなら、その地域の三十パーセントで、雨が降る」。そう思っていませんか。', big='30％は、地域の30％？', art='assets/rain30/art_intro.png'),
        dict(text='気象庁の解説によると、降水確率は、指定された時間帯の間に、一ミリ以上の降水がある確率です。', big='1ミリ以上の降水がある確率', src='気象庁', art='assets/rain30/art_def.png', col='white'),
        dict(text='予報が出される地域内の、どの点でも、同じ確率として定義されます。', big='どの点でも、同じ確率', art='assets/rain30/art_meaning.png'),
        dict(text='つまり、地域の三十パーセントの面積で、雨が降る、という意味ではありません。', big='面積の30％、ではない', art='assets/rain30/art_amount.png', col='white'),
        dict(text='また、降水量の多少は、この数字では示されていません。', big='雨の強さは、示さない', sub='強い雨か、弱い雨かは、この数字だけでは決められない', src='気象庁', art='assets/rain30/art_verify.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/rain30/art_end.png')]))

J('moon', dict(
    title='月は自転していない？', long_id='97mj1dw20ec',
    long_title='月はいつも同じ面を見せる。自転していない？ NASAの解説で確かめる',
    pron='data/moon_pronunciations.json', art='assets/moon/art_intro.png',
    hook='「月はいつも同じ面を地球に見せているから、自転していない」と思っていませんか。NASAの解説から、月の動きを確かめます。',
    notes='■ 動画で確かめたこと\n・月は、地球のまわりを一周するあいだに、一回、自転します（NASA）。この状態を潮汐ロックと呼びます。\n・同じ面が見え続けるのは、自転と公転の時間が同じだからです（NASA）。\n・地球から見えない側を「暗い側」と呼ぶのは誤解を招く、とNASAは説明しています。\n・自転と公転の周期の、細かい日数は、この動画の資料だけでは決められません。',
    scenes=[
        dict(text='「月は、いつも同じ面を、地球に見せている。だから、自転していない」。そう思っていませんか。', big='月は、自転していない？', art='assets/moon/art_intro.png'),
        dict(text='NASAの解説によると、月は、地球のまわりを一周するあいだに、一回、自転します。', big='一周で、一回、自転', src='NASA', art='assets/moon/art_motion.png', col='white'),
        dict(text='同じ面が見え続けるのは、自転と公転の時間が、同じだからです。', big='自転と公転の時間が、同じ', art='assets/moon/art_sync.png'),
        dict(text='自転しない月なら、地球からは、月のさまざまな面が、順に見えるはずです。', big='自転しなければ、いろいろな面が見える', sub='自作の模式図で比べています', art='assets/moon/art_why.png', col='white'),
        dict(text='見えない側にも、昼と夜があります。NASAは、暗い側という呼び方は、誤解を招く、としています。', big='見えない側にも、昼がある', src='NASA', art='assets/moon/art_dark.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/moon/art_end.png')]))

J('islands', dict(
    title='日本の島は、2倍に増えた？', long_id='4xXMeRX8OfA',
    long_title='日本の島は、本当に2倍に増えた？ 国土地理院の解説で確かめる',
    pron='data/islands_pronunciations.json', art='assets/islands/art_intro.png',
    hook='日本の島の数として公表された数字が、6,852島から14,125島に変わりました。本当に島は増えたのでしょうか。国土地理院の解説で確かめます。',
    notes='■ 動画で確かめたこと\n・6,852島は海上保安庁が昭和62年に公表した数字、14,125島は国土地理院が2023年2月に公表した数字です。\n・国土地理院は、大きく異なるのは測量技術の進歩による地図表現の詳細化が大きく影響していると考えられる、と説明しています。\n・新しい島が見つかったわけではなく、電子国土基本図に描かれた陸地を、一定の条件で数えた結果です。\n・昭和62年の調査の詳しい数え方、都道府県別の島の数は、この動画の資料だけでは分かりません。',
    scenes=[
        dict(text='日本の島の数として公表された数字が、六千八百五十二島から、一万四千百二十五島に、変わりました。', big='6,852島 → 14,125島', art='assets/islands/art_intro.png'),
        dict(text='六千八百五十二島は、海上保安庁が、昭和六十二年に公表した数字です。', big='昭和62年：6,852島', src='海上保安庁の公表', art='assets/islands/art_nums.png', col='white'),
        dict(text='一万四千百二十五島は、国土地理院が、二千二十三年二月に公表した数字です。', big='2023年2月：14,125島', src='国土地理院の公表', art='assets/islands/art_count.png'),
        dict(text='国土地理院によると、測量技術の進歩による、地図表現の詳細化が、大きく影響していると、考えられます。', big='地図の表現が、細かくなった', src='国土地理院', art='assets/islands/art_new.png', col='white'),
        dict(text='新しい島が、見つかったわけでは、ありません。', big='新しい島が見つかったわけではない', sub='地図に描かれた陸地を、一定の条件で数えた結果', src='国土地理院', art='assets/islands/art_land.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/islands/art_end.png')]))

J('magnitude', dict(
    title='マグニチュード+1で、10倍強い？', long_id='RXJrW4QwXdE',
    long_title='マグニチュードが1増えると地震は10倍強い？ 気象庁の解説で確かめる',
    pron='data/magnitude_pronunciations.json', art='assets/magnitude/art_intro.png',
    hook='「マグニチュードが1大きいと、地震のエネルギーは10倍強」と思っていませんか。気象庁の解説から、確かめます。',
    notes='■ 動画で確かめたこと\n・マグニチュードは地震そのものの大きさ（規模）、震度はある場所での揺れの強さを表します（気象庁）。\n・マグニチュードの値が1大きくなると、エネルギーは約32倍、2大きくなると約1,000倍になります（気象庁）。\n・マグニチュードの数字だけでは、あなたのいる場所の震度は決められません。',
    scenes=[
        dict(text='「マグニチュードが一つ大きくなると、地震のエネルギーは、十倍強になる」。そう思っていませんか。', big='M+1で、10倍強？', art='assets/magnitude/art_intro.png'),
        dict(text='気象庁によると、マグニチュードは、地震そのものの大きさを表します。震度は、ある場所での、揺れの強さです。', big='M＝地震の大きさ　震度＝揺れの強さ', src='気象庁', art='assets/magnitude/art_diff.png', col='white'),
        dict(text='マグニチュードの値が、一大きくなると、エネルギーは、約三十二倍になります。', big='+1で、約32倍', src='気象庁', art='assets/magnitude/art_energy.png'),
        dict(text='二大きくなると、約千倍です。十倍強では、ありません。', big='+2で、約1,000倍', sub='約32倍を2回かけると約1,000（自作の計算）', art='assets/magnitude/art_dist.png', col='white'),
        dict(text='ただし、マグニチュードの数字だけでは、あなたのいる場所の震度は、決められません。', big='場所の揺れは、M だけでは決まらない', art='assets/magnitude/art_end.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/magnitude/art_end.png')]))

J('yakubusoku', dict(
    title='「役不足」の本当の意味は？', long_id='Cx9DgjZ2TAM',
    long_title='「役不足」は、能力が足りない意味？ 文化庁の調査で確かめる',
    pron='data/yakubusoku_pronunciations.json', art='assets/yakubusoku/art_intro.png',
    hook='「彼には役不足の仕事だ」。この言葉は、能力が足りない、という意味でしょうか。文化庁の調査の結果から確かめます。',
    notes='■ 動画で確かめたこと\n・文化庁の調査では、「本人の力量に対して、役目が軽すぎること」が本来の意味とされています（文化庁「国語に関する世論調査」平成14年度・平成18年度）。\n・平成14年度は「重すぎる」が62.8％、「軽すぎる」が27.6％。平成18年度は50.3％と40.3％でした。\n・この数字は、調査年度のものです。いまの割合を示すものではありません。',
    scenes=[
        dict(text='「彼には役不足の仕事だ」。この「役不足」は、彼の力量に対して、仕事が重すぎる、という意味でしょうか。', big='「役不足」の意味は？', art='assets/yakubusoku/art_intro.png'),
        dict(text='文化庁は、本来の意味を、本人の力量に対して、役目が軽すぎること、としています。', big='本来は「役目が軽すぎる」', src='文化庁', art='assets/yakubusoku/art_ask.png', col='white'),
        dict(text='平成十四年度の調査では、重すぎる、と答えた人が、六十二・八パーセント。軽すぎる、は二十七・六パーセントでした。', big='62.8％　対　27.6％', sub='平成14年度の調査', src='文化庁', art='assets/yakubusoku/art_result.png'),
        dict(text='平成十八年度は、五十・三パーセントと、四十・三パーセント。差は、縮まりました。', big='50.3％　対　40.3％', sub='平成18年度の調査', src='文化庁', art='assets/yakubusoku/art_meaning.png', col='white'),
        dict(text='ただし、これは、調査に答えた人が選んだ意味の割合です。いまの割合では、ありません。', big='いまの割合では、ない', art='assets/yakubusoku/art_end.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/yakubusoku/art_end.png')]))

J('leapsecond', dict(
    title='うるう秒は、なぜやめる？', long_id='dO_fY0jaTh4',
    long_title='うるう秒は、なぜやめる？ 国際度量衡総会の決議を確かめる',
    pron='data/leapsecond_pronunciations.json', art='assets/leapsecond/art_intro.png',
    hook='日本時間の2017年1月1日、「8時59分60秒」が入りました。うるう秒です。このうるう秒をやめる決議が、2026年に出されました。なぜなのか、資料で確かめます。',
    notes='■ 動画で確かめたこと\n・うるう秒は、原子時計をもとにした協定世界時と、地球の自転に基づく時刻のずれを、0.9秒以内に保つために、1秒を入れる仕組みです（総務省）。\n・2026年の国際度量衡総会の決議5は、2027年5月20日から、うるう秒による調整をしない連続した協定世界時とします。ずれの許容上限は3,600秒（1時間）で、実際のずれが1時間になるという意味ではありません（BIPM）。\n・前文は、負のうるう秒は一度も使われておらず、重要な設備には高いリスクがある、2035年までに必要になる確率は30％という見積もりがある、としています（BIPM）。',
    scenes=[
        dict(text='二千十七年の元日、日本時間の午前八時五十九分五十九秒。その次に、「八時五十九分六十秒」が入りました。', big='8時59分60秒', art='assets/leapsecond/art_intro.png'),
        dict(text='うるう秒は、協定世界時と、地球の自転に基づく時刻の、ずれを、小さく保つための仕組みです。', big='ずれを、0.9秒以内に', src='総務省', art='assets/leapsecond/art_in.png', col='white'),
        dict(text='そのうるう秒を、やめる決議が、二千二十六年の、国際度量衡総会で出されました。', big='うるう秒を、やめる決議', src='BIPM（国際度量衡総会）', art='assets/leapsecond/art_out.png'),
        dict(text='理由の一つは、一秒を抜く、負のうるう秒が、これまで一度も使われていないことです。', big='負のうるう秒は、一度も使われていない', sub='決議：重要な設備には、高いリスク', art='assets/leapsecond/art_change.png', col='white'),
        dict(text='ずれの許容上限は、一時間に広がります。ただし、実際のずれが、すぐ一時間になる、という意味では、ありません。', big='上限が1時間。実際のずれ、ではない', art='assets/leapsecond/art_end.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/leapsecond/art_end.png')]))

J('sunrise', dict(
    title='日の出が一番早いのは夏至の日？', long_id='mk5x-Yu9cC4',
    long_title='日の出が一番早いのは、夏至の日？ 国立天文台の暦で確かめる',
    pron='data/sunrise_pronunciations.json', art='assets/sunrise/art_intro.png',
    hook='昼が一番長い夏至の日に、日の出も一番早いのでしょうか。国立天文台の説明と、東京の暦で確かめます。',
    notes='■ 動画で確かめたこと\n・国立天文台の説明では、日の出が最も早い日は夏至の約1週間前、日の入りが最も遅い日は約1週間後です。\n・東京の2027年の暦（国立天文台暦計算室）では、日の出は6月6日〜21日が毎日4時25分で、夏至（6月21日）も同じです。日の入りは、夏至の日が19時00分、6月24日〜7月5日が19時01分でした。\n・暦は分単位なので、東京の暦だけでは、一番早い一日は決められません。',
    scenes=[
        dict(text='昼が一番長い日は、夏至です。では、日の出が一番早い日も、夏至でしょうか。', big='日の出が一番早いのは、夏至の日？', art='assets/sunrise/art_intro.png'),
        dict(text='国立天文台は、日の出が最も早い日は、夏至の約一週間前、と説明しています。', big='夏至の、約1週間前', src='国立天文台', art='assets/sunrise/art_rise.png', col='white'),
        dict(text='東京の二千二十七年の暦では、六月六日から夏至の日まで、日の出は毎日、四時二十五分です。', big='6月6日〜21日：毎日、4時25分', src='国立天文台 暦計算室', art='assets/sunrise/art_set.png'),
        dict(text='日の入りは、夏至のあとも遅くなり、六月二十四日から、十九時一分になります。', big='夏至のあとも、日の入りは遅くなる', sub='6月24日〜7月5日：19時01分', art='assets/sunrise/art_why.png', col='white'),
        dict(text='理由は、南中の時刻が、毎日、少しずつ遅くなるためです。ただし、暦は分単位で、一番早い一日は、決められません。', big='理由は、南中の時刻の変化', art='assets/sunrise/art_end.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/sunrise/art_end.png')]))

print('written')
