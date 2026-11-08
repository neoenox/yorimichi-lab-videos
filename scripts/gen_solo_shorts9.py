"""単独Short 第10弾（2026-11-05）＝「本編に触れない版」(nolong) の新作12本。海の色2・日の出と日の入り2・お米2・マグニチュード2・島の数・ビタミンC・静脈・森林率。
台本は、長尺の検証メモ（docs/themes/*/09_script_v2.md、08_fact_check.md）にある記述だけを使う。新しい調査・画像生成はしない。
usage: python scripts/gen_solo_shorts9.py → data/short_solo_*.json（nolong:true）。その後 make_short2.py / pack_short.py / Studioまたはyt_api.pyでアップ（非公開）。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
IDS = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))
CREDIT = '・イラスト：ChatGPT(OpenAI)による生成イラスト（イメージです。実在の場面・人物・資料の再現ではありません）\n・図・表：自作'
NOTE = '・公的機関・研究者の解説の要約による内容で、原典(原本)そのものの照合は、今回は行っていません。\n'


def J(n, pack, o):
    o['long_id'] = IDS[pack]['video_id']
    o['long_title'] = o.get('long_title', pack)
    o['nolong'] = True
    o.setdefault('credit', CREDIT)
    (R / 'data' / f'short_{n}.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')
    print('wrote', n)


def end():
    return dict(text='', end=True)


def A(slug, name): return f'assets/{slug}/art_{name}.png'


J('solo_oceanblue_sora', '22_ocean_blue', dict(
    title='海が青いのは、空が映るから？', pron='data/oceanblue_pronunciations.json', art=A('oceanblue', 'sky'),
    hook='海が青いのは、空の青さが映っているから。この説明で、海の青さは、説明できるのでしょうか。',
    notes='■ 動画で確かめたこと\n・ウッズホール海洋研究所の解説は、水面では空を映す、と認めています。しかし、水面の下に潜っても、青い色は残ります。\n・NOAAの解説によると、海が青いのは、水が、光の赤い側の色を吸収するからです。\n・つまり、空の映り込みだけでは、海が青い理由を説明できません。\n' + NOTE,
    answer='空の映り込みだけでは、説明できない',
    scenes=[
        dict(text='海が青いのは、空が青くて、その空が、水面に映っているから。そう思っていませんか。', big='海が青い＝空の映り込み？', art=A('oceanblue', 'sky')),
        dict(text='ウッズホール海洋研究所の解説でも、水面では、空を映す、と認めています。', big='水面では、空を映す', src='ウッズホール海洋研究所', art=A('oceanblue', 'intro'), col='white'),
        dict(text='しかし、水面の下に、潜っても、青い色は、残ります。', big='潜っても、青は残る', src='ウッズホール海洋研究所', art=A('oceanblue', 'light')),
        dict(text='NOAAの解説では、海が青いのは、水が、光の赤い側の色を、吸収するからです。', big='水が、赤い側の色を吸収', src='NOAA', art=A('oceanblue', 'colors'), col='white'),
        end()]))

J('solo_oceanblue_iro', '22_ocean_blue', dict(
    title='海は、いつも青い？', pron='data/oceanblue_pronunciations.json', art=A('oceanblue', 'colors'),
    hook='海は、いつも青いのでしょうか。海の色が変わる条件を、NOAAとウッズホール海洋研究所の解説で確かめます。',
    notes='■ 動画で確かめたこと\n・堆積物が多いと、水は茶色に見える、とされます(ウッズホール海洋研究所)。\n・植物プランクトンが多い場所では、水は緑や赤に見えることがあります。\n・浅くて砂の底の場所では、光が底で跳ね返り、水は鮮やかな青に見えることがあります。\n' + NOTE,
    answer='条件で、色は変わる',
    scenes=[
        dict(text='海は、いつも、青いのでしょうか。', big='海は、いつも青い？', art=A('oceanblue', 'colors')),
        dict(text='堆積物が多いと、水は、茶色に見える、とされます。', big='堆積物が多いと、茶色', src='ウッズホール海洋研究所', art=A('oceanblue', 'intro'), col='white'),
        dict(text='植物プランクトンが多い場所では、水は、緑や赤に見えることがあります。', big='プランクトンで、緑や赤に', src='ウッズホール海洋研究所', art=A('oceanblue', 'light')),
        dict(text='浅くて砂の底の場所では、光が底で跳ね返り、水は、鮮やかな青に見えることがあります。', big='浅い砂地は、鮮やかな青', src='ウッズホール海洋研究所', art=A('oceanblue', 'sky'), col='white'),
        end()]))

J('solo_sunrise_hayai', '20_sunrise_solstice', dict(
    title='日の出が一番早いのは、夏至？', pron='data/sunrise_pronunciations.json', art=A('sunrise', 'rise'),
    hook='一年で昼が一番長い日は、夏至です。では、日の出が一番早い日も、夏至でしょうか。暦で確かめます。',
    notes='■ 動画で確かめたこと\n・国立天文台は、日の出が最も早い日は、夏至の約一週間前、と説明しています。\n・東京の2027年の暦では、6月6日から6月21日まで、毎日、日の出は4時25分です(国立天文台 暦計算室)。\n・暦は分単位なので、一番早い一日は、この表だけでは、一つに絞れません。\n' + NOTE,
    answer='夏至の約1週間前',
    scenes=[
        dict(text='一年で、昼が一番長い日は、夏至です。では、日の出が一番早い日も、夏至でしょうか。', big='日の出が一番早いのは、夏至？', art=A('sunrise', 'rise')),
        dict(text='国立天文台は、日の出が最も早い日は、夏至の約一週間前、と説明しています。', big='夏至の、約一週間前', src='国立天文台', art=A('sunrise', 'why'), col='white'),
        dict(text='東京の二〇二七年の暦では、六月六日から六月二十一日まで、毎日、日の出は、四時二十五分です。', big='6/6〜6/21：4時25分', src='国立天文台 暦計算室（東京・2027年）', art=A('sunrise', 'end')),
        dict(text='暦は、分単位なので、一番早い一日は、この表だけでは、一つに絞れません。', big='一番早い一日は、絞れない', src='国立天文台 暦計算室', art=A('sunrise', 'rise'), col='white'),
        end()]))

J('solo_sunrise_osoi', '20_sunrise_solstice', dict(
    title='日の入りが一番遅いのは、夏至？', pron='data/sunrise_pronunciations.json', art=A('sunrise', 'set'),
    hook='日の入りが一番遅い日も、夏至なのでしょうか。東京の暦の数字で、確かめます。',
    notes='■ 動画で確かめたこと\n・東京の2027年の暦では、夏至の日の入りは19時ちょうどです。6月24日から7月5日までは、毎日19時1分です(国立天文台 暦計算室)。\n・国立天文台は、日の入りが最も遅い日は、夏至の約一週間後、と説明しています。\n・昼の長さは、夏至の前後で、ほとんど変わりません(暦から自作の計算)。\n' + NOTE,
    answer='夏至の約1週間後',
    scenes=[
        dict(text='夏至の日の、日の入りは、十九時ちょうどです。', big='夏至の日の入り：19時0分', src='国立天文台 暦計算室（東京・2027年）', art=A('sunrise', 'set')),
        dict(text='ところが、そのあとも、日の入りは、遅くなります。六月二十四日から七月五日までは、毎日、十九時一分です。', big='6/24〜7/5：19時1分', src='国立天文台 暦計算室（東京・2027年）', art=A('sunrise', 'why'), col='white'),
        dict(text='国立天文台は、日の入りが最も遅い日は、夏至の約一週間後、と説明しています。', big='夏至の、約一週間後', src='国立天文台', art=A('sunrise', 'end')),
        dict(text='昼の長さは、夏至の前後で、ほとんど変わりません。', big='昼の長さは、ほぼ同じ', src='暦から自作の計算', art=A('sunrise', 'set'), col='white'),
        end()]))

J('solo_rice_hanbun', '23_rice', dict(
    title='お米は、昔の半分以下に？', pron='data/rice_pronunciations.json', art=A('rice', 'bowl'),
    hook='日本人が食べるお米は、昔の半分以下になった。この話を、農林水産省の統計で確かめます。',
    notes='■ 動画で確かめたこと\n・農林水産省によると、国民一人あたりのお米の量のピークは、1962年度で、1年間に118.3kgです。\n・令和7年度は、概算で52kgです。ピークの約44%にあたります(自作の計算)。\n・ただし、これは、実際に食べた量ではなく、「食料需給表」という統計の、一人あたりの供給量です。家庭や店での廃棄や食べ残しは、引かれていません。\n・令和7年度は概算の数字で、確定すると変わることがあります。\n',
    answer='供給量の統計で、約44％',
    scenes=[
        dict(text='日本人が食べるお米は、昔の半分以下になった。そう聞いたことは、ありませんか。', big='お米は、半分以下に？', art=A('rice', 'bowl')),
        dict(text='農林水産省によると、国民一人あたりの量は、一九六二年度が、ピーク。一年で、百十八・三キログラムです。', big='1962年度：118.3kg', src='農林水産省', art=A('rice', 'field'), col='white'),
        dict(text='令和七年度は、概算で、五十二キログラム。ピークの、約四十四パーセントです。', big='令和7年度：約52kg（概算）', src='農林水産省・自作の計算', art=A('rice', 'table')),
        dict(text='ただし、これは、実際に食べた量ではなく、食料需給表の、供給量です。廃棄や食べ残しは、引かれていません。', big='食べた量ではなく、供給量', src='農林水産省（食料需給表）', art=A('rice', 'kitchen'), col='white'),
        end()]))

J('solo_rice_nenn', '23_rice', dict(
    title='お米の量、毎年減り続けた？', pron='data/rice_pronunciations.json', art=A('rice', 'table'),
    hook='国民一人あたりのお米の量は、毎年、減り続けたのでしょうか。直近の数字で、確かめます。',
    notes='■ 動画で確かめたこと\n・農林水産省の食料需給表によると、国民一人あたりのお米の量は、令和5年度が50.3kg、令和6年度が53.3kgです。\n・令和7年度は、概算で52kgに下がっています。\n・長い目で見ると大きく減っていますが、年によって増えることもあります。\n・令和7年度は概算の数字です。\n',
    answer='年によって、増えることもある',
    scenes=[
        dict(text='国民一人あたりのお米は、毎年、減り続けたのでしょうか。', big='お米は、毎年減り続けた？', art=A('rice', 'table')),
        dict(text='令和五年度は、五十・三キログラムです。', big='令和5年度：50.3kg', src='農林水産省（食料需給表）', art=A('rice', 'field'), col='white'),
        dict(text='令和六年度は、五十三・三キログラム。増えています。', big='令和6年度：53.3kg', src='農林水産省（食料需給表）', art=A('rice', 'bowl')),
        dict(text='令和七年度は、概算で、五十二キログラム。長い目で見ると減っていますが、年によっては、増えることもあります。', big='年によって、増えることもある', src='農林水産省（食料需給表・概算）', art=A('rice', 'kitchen'), col='white'),
        end()]))

J('solo_magnitude_32', '17_magnitude_energy', dict(
    title='地震のエネルギー、10倍ずつ？', pron='data/magnitude_pronunciations.json', art=A('magnitude', 'energy'),
    hook='マグニチュードが一つ大きくなると、地震のエネルギーは、十倍強になる。気象庁の解説で、確かめます。',
    notes='■ 動画で確かめたこと\n・気象庁の解説では、マグニチュードの値が1大きくなると、エネルギーは約32倍になります。2大きくなると、約1000倍です。\n・約32倍を2回かけると、約1000です(自作の計算)。\n・つまり、エネルギーは「10倍強」ではなく、1大きくなるごとに、約32倍です。\n',
    answer='1で約32倍、2で約1000倍',
    scenes=[
        dict(text='マグニチュードが一つ大きくなると、地震のエネルギーは、十倍強になる。そう思っていませんか。', big='エネルギーは、10倍強？', art=A('magnitude', 'intro')),
        dict(text='気象庁の解説では、マグニチュードが一つ大きくなると、エネルギーは、約三十二倍です。', big='1大きいと、約32倍', src='気象庁', art=A('magnitude', 'energy'), col='white'),
        dict(text='二つ大きくなると、約千倍になります。', big='2大きいと、約1000倍', src='気象庁', art=A('magnitude', 'diff')),
        dict(text='約三十二倍を、二回かけると、約千です。「十倍強」では、ありません。', big='「10倍強」ではない', src='自作の計算', art=A('magnitude', 'energy'), col='white'),
        end()]))

J('solo_magnitude_shindo', '17_magnitude_energy', dict(
    title='マグニチュードと震度は、同じ？', pron='data/magnitude_pronunciations.json', art=A('magnitude', 'dist'),
    hook='マグニチュードと震度は、何が違うのか。気象庁のたとえで、確かめます。',
    notes='■ 動画で確かめたこと\n・気象庁の解説によると、マグニチュードは地震そのものの大きさ(規模)を表し、震度はある場所での揺れの強さを表します。\n・気象庁は、電球にたとえています。マグニチュードは電球の明るさ、震度は離れた場所での明るさにあたります。\n・日本の震度は、全部で十階級です。同じ地震でも、場所によって震度は異なることがあります。\n',
    answer='Mは規模、震度は場所ごとの揺れ',
    scenes=[
        dict(text='気象庁の解説によると、マグニチュードは、地震そのものの、大きさ、規模を表します。', big='マグニチュード＝地震の規模', src='気象庁', art=A('magnitude', 'dist')),
        dict(text='一方、震度は、ある場所での、揺れの強さを表します。', big='震度＝その場所の揺れの強さ', src='気象庁', art=A('magnitude', 'diff'), col='white'),
        dict(text='気象庁は、電球にたとえています。マグニチュードは、電球の明るさ。震度は、離れた場所での、明るさにあたります。', big='電球のたとえ', src='気象庁', art=A('magnitude', 'energy')),
        dict(text='日本の震度は、全部で十階級です。同じ地震でも、場所によって、震度は異なることがあります。', big='同じ地震でも、場所で違う', src='気象庁', art=A('magnitude', 'dist'), col='white'),
        end()]))

J('solo_islands_kazu', '16_islands_count', dict(
    title='日本の島の数、どちらが本当？', pron='data/islands_pronunciations.json', art=A('islands', 'count'),
    hook='日本の島の数として公表された数字が、変わりました。何が違うのか、国土地理院の説明で確かめます。',
    notes='■ 動画で確かめたこと\n・6,852島は、海上保安庁が昭和62年に公表した数字です。\n・14,125島は、国土地理院が2023年2月に公表した数字です。\n・国土地理院は、測量技術の進歩による地図表現の詳細化が、大きく影響していると考えられる、と説明しています。\n・島を数える方法には、国際的な取り決めがありません。\n',
    answer='数え方に、国際ルールはない',
    scenes=[
        dict(text='日本の島の数として公表された数字が、六千八百五十二島から、一万四千百二十五島に、変わりました。', big='6,852島 → 14,125島', art=A('islands', 'count')),
        dict(text='六千八百五十二島は、海上保安庁が、昭和六十二年に公表した数字です。', big='6,852島：海上保安庁（昭和62年）', src='国土地理院の説明', art=A('islands', 'nums'), col='white'),
        dict(text='一万四千百二十五島は、国土地理院が、二〇二三年二月に公表した数字です。', big='14,125島：国土地理院（2023年2月）', src='国土地理院', art=A('islands', 'new')),
        dict(text='国土地理院は、測量技術の進歩による、地図表現の詳細化が、大きく影響していると、説明しています。', big='地図表現の詳細化が、影響', src='国土地理院', art=A('islands', 'land'), col='white'),
        dict(text='島を数える方法には、国際的な取り決めが、ありません。', big='国際的な取り決めは、ない', src='国土地理院', art=A('islands', 'count')),
        end()]))

J('solo_vitaminc_kaze', '30_vitaminc', dict(
    title='ビタミンCで、風邪は短くなる？', pron='data/vitaminc_pronunciations.json', art=A('vitaminc', 'intro'),
    hook='ビタミンCを毎日とると、風邪の期間は、短くなるのか。コクランのレビューの数字で、確かめます。',
    notes='■ 動画で確かめたこと\n・毎日、サプリメントなどで追加でとり続けた一般の人、1万700人あまりを調べた結果です(コクランのレビュー、2013年)。\n・風邪の期間は、平均して、成人で8%、子どもで14%短くなりました。\n・一週間の風邪が8%短くなると、半日ほどです(自作の計算)。\n・この差を大きいと見るか、小さいと見るかは、人によって分かれます。\n・このレビューは2013年のもので、それ以後の研究は確認していません。\n',
    answer='成人8％、子ども14％短く（平均）',
    scenes=[
        dict(text='毎日、サプリメントなどで、ビタミンCを追加でとり続けた、一般の人。一万七百人あまりを、調べた結果があります。', big='約1万700人を調べた結果', src='コクランのレビュー（2013年）', art=A('vitaminc', 'intro')),
        dict(text='風邪の期間は、平均して、成人で八パーセント、子どもで十四パーセント、短くなりました。', big='成人8％・子ども14％短縮', src='コクランのレビュー（2013年）', art=A('vitaminc', 'review'), col='white'),
        dict(text='一週間の風邪が、八パーセント短くなると、半日ほどです。', big='一週間の風邪で、半日ほど', src='自作の計算', art=A('vitaminc', 'snow')),
        dict(text='この差を、大きいと見るか、小さいと見るかは、人によって、分かれます。', big='大きいか小さいかは、人による', art=A('vitaminc', 'book'), col='white'),
        end()]))

J('solo_vein_aoi', '13_vein_blue', dict(
    title='静脈が青く見えるのは、なぜ？', pron='data/vein_pronunciations.json', art=A('vein', 'arm'),
    hook='手の甲の静脈は、青っぽく見えます。血が青いから、なのでしょうか。解説で確かめます。',
    notes='■ 動画で確かめたこと\n・静脈は、実際には青くありません。図解などで、動脈と区別するために、青で描かれることが多いとされます。\n・静脈が青っぽく見えるのは、皮膚と光の見え方によるもので、血が青いからではありません。\n・光の色によって、皮膚への入り方が違います。\n' + NOTE,
    answer='血が青いからではない',
    scenes=[
        dict(text='手の甲の静脈は、青っぽく見えます。血が青いから、でしょうか。', big='静脈の血は、青い？', art=A('vein', 'arm')),
        dict(text='静脈は、実際には、青くありません。', big='静脈は、実際には青くない', src='解説（二次情報）', art=A('vein', 'cells'), col='white'),
        dict(text='青っぽく見えるのは、皮膚と光の、見え方によるものです。', big='皮膚と光の、見え方', src='解説（二次情報）', art=A('vein', 'sunlight')),
        dict(text='光の色によって、皮膚への入り方が、違います。', big='光の色で、入り方が違う', src='解説（二次情報）', art=A('vein', 'drop'), col='white'),
        end()]))

J('solo_forest_oecd', '27_forest', dict(
    title='日本の森林率は、世界3位？', pron='data/forest_pronunciations.json', art=A('forest', 'hills'),
    hook='日本の森林率は、約六八パーセント。これは、世界で何番目なのか。FAOと林野庁の数字で、確かめます。',
    notes='■ 動画で確かめたこと\n・FAOの2020年の評価では、日本の森林率は68.4%です。\n・国全体で見ると、スリナムが約97%、ガイアナが約94%、ガボンが約91%で、日本より高い国はいくつもあります。\n・OECD加盟国に限ると、日本は68.4%で、3番目です(FAOの2020年の統計をもとに、林野庁が比べた表)。\n・つまり、「世界三位」ではなく、「2020年の統計で、OECD加盟国の中で三位」が正確です。\n',
    answer='OECD加盟国の中で3位（2020年）',
    scenes=[
        dict(text='日本の森林率は、約六八パーセント。これは、世界で、何番目でしょうか。', big='森林率68％は、世界で何位？', art=A('forest', 'hills')),
        dict(text='国全体で見ると、スリナムが約九七パーセント。ガイアナが約九四、ガボンが約九一パーセントです。日本より高い国は、いくつもあります。', big='日本より高い国は、いくつもある', src='FAO（2020年）', art=A('forest', 'dark'), col='white'),
        dict(text='OECD加盟国に限ると、日本は、六八・四パーセントで、三番目です。', big='OECD加盟国では、3位', src='FAO・林野庁', art=A('forest', 'dawn')),
        dict(text='つまり、「世界三位」ではなく、「二〇二〇年の統計で、OECD加盟国の中で三位」が、正確です。', big='「世界3位」は、不正確', src='FAO・林野庁', art=A('forest', 'hills'), col='white'),
        end()]))
