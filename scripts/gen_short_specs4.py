"""Short用の spec その4：rice・akashi・gps。台本は長尺の 09_script_v2.md の文言に合わせる（数字・限定・帰属を変えない）。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
CREDIT = '・イラスト：ChatGPT(OpenAI)による生成イラスト（イメージです。実在の資料の複製ではありません）\n・図・表：自作'


def J(n, o):
    (R / 'data' / f'short_{n}.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')


J('rice', dict(
    title='お米は、昔の半分以下になった？', long_id='lHNfr-MxXEs',
    long_title='日本人が食べるお米は、昔の半分以下になった？ 農林水産省の統計で確かめる',
    pron='data/rice_pronunciations.json', art='assets/rice/art_field.png',
    hook='「日本人が食べるお米は、昔の半分以下になった」と聞いたことはありませんか。農林水産省の統計で確かめます。',
    notes='■ 動画で確かめたこと\n・農林水産省の統計（食料需給表）では、国民1人あたりのお米の供給量は、1962年度の118.3kgから、令和7年度（概算）の52.0kgへ。ピークの約44％です（52.0÷118.3は自作の計算）。\n・この数字は、実際に食べた量ではなく、統計上の供給量です。家庭や店での廃棄や食べ残しは引かれていません。\n・令和6年度は53.3kgで、前の年より増えました。毎年同じように減ってきたわけではありません。\n・令和7年度は概算で、確定すると変わることがあります。',
    credit=CREDIT, answer='供給量は、ピークの約44％',
    scenes=[
        dict(text='日本人が食べるお米は、昔の半分以下になった。そう聞いたことはありませんか。', big='お米は、昔の半分以下？', art='assets/rice/art_field.png'),
        dict(text='農林水産省の統計では、国民一人あたりのお米の供給量は、一九六二年度に、百十八・三キログラムでした。', big='1962年度：118.3kg', src='農林水産省', art='assets/rice/art_table.png', col='white'),
        dict(text='令和七年度は、概算で、五十二キログラムです。ピークの、およそ四十四パーセントです。', big='令和7年度（概算）：52.0kg', sub='ピークの約44％（公表値から計算）', art='assets/rice/art_bowl.png'),
        dict(text='ただし、これは、実際に食べた量では、ありません。家庭や店での、廃棄や食べ残しは、引かれていません。', big='実際に食べた量ではない', src='農林水産省', art='assets/rice/art_kitchen.png', col='white'),
        dict(text='令和六年度は、五十三・三キログラムに増え、令和七年度は、再び下がっています。毎年、同じように減ってきたわけでは、ありません。', big='毎年、減り続けたわけではない', src='農林水産省', art='assets/rice/art_field.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/rice/art_bowl.png')]))

J('akashi', dict(
    title='日本の標準時は、なぜ明石の時刻？', long_id='l0KyLWbjJG0',
    long_title='日本の標準時は、なぜ明石の時刻？ 東経135度の理由を確かめる',
    pron='data/akashi_pronunciations.json', art='assets/akashi/art_seaside.png',
    hook='「日本の標準時は、明石の時刻」と聞いたことはありませんか。国立天文台や明石市立天文科学館の説明で確かめます。',
    notes='■ 動画で確かめたこと\n・1884年の国際子午線会議で、グリニッジを通る線が経度0度と決まりました。太陽を基準にした時刻は、経度15度で1時間の差になります（360÷24は自作の計算）。\n・日本は1886年、東経135度の時刻を標準時と定めました（使い始めたのは1888年1月1日）。国土のほぼ真ん中を通り、グリニッジとの時差がちょうど9時間になる線です。\n・明石市立天文科学館の学芸員は、明石があったから135度が選ばれたわけではなく、たまたま明石が線の上にあった、と説明しています（神戸新聞）。\n・今の日本標準時は、NICTが複数の原子時計をもとにつくっています。',
    credit=CREDIT, answer='明石が選ばれたのではない',
    scenes=[
        dict(text='日本の標準時は、兵庫県の明石を通る線が基準。そう聞いたことはありませんか。', big='標準時は、明石の時刻？', art='assets/akashi/art_seaside.png'),
        dict(text='太陽を基準にした時刻は、経度十五度で、一時間の差になります。', big='経度15度で、1時間の差', src='国立天文台', art='assets/akashi/art_globe.png', col='white'),
        dict(text='日本は、国土のほぼ真ん中を通り、グリニッジとの時差が、ちょうど九時間になる、東経百三十五度を、標準時の線にしました。', big='東経135度＝時差ちょうど9時間', art='assets/akashi/art_map_desk.png'),
        dict(text='明石市立天文科学館の学芸員は、こう説明しています。明石があったから、百三十五度が選ばれたわけではありません。たまたま、その線の上に明石があったのです。', big='明石は、たまたま線の上', src='明石市立天文科学館（神戸新聞）', art='assets/akashi/art_seaside.png', col='white'),
        dict(text='今の日本標準時は、NICTが、複数の原子時計をもとに、つくって、送り出しています。', big='つくっているのは、NICT', src='NICT', art='assets/akashi/art_watch.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/akashi/art_clockglobe.png')]))

J('gps', dict(
    title='GPS衛星は、居場所を知っている？', long_id='f-zfsWuPz2g',
    long_title='GPS衛星は、あなたの居場所を知っている？ GPS.govの説明で確かめる',
    pron='data/gps_pronunciations.json', art='assets/gps/art_sky.png',
    hook='「GPS衛星は、あなたの居場所を知っている」と思っていませんか。アメリカ政府のGPS公式サイト、GPS.govの説明で確かめます。',
    notes='■ 動画で確かめたこと\n・GPS.govによると、衛星は、自分の位置や状態、正確な時刻などを電波で送っています。端末は、その電波から、自分の位置を計算します。\n・GPS.govのFAQによると、GPS衛星そのものは地上のものを追跡しておらず、灯台のように一方向の信号を送るだけで、GPSを運用する政府は、スマホの位置を特定できません。携帯電話会社などが、端末に組み込まれた機能で探せる場合は別です。\n・MITの解説によると、GPSの計算そのものは居場所を外へ知らせませんが、通信機能を持つ機器やサービスが、位置情報を外へ送る場合があります。',
    credit=CREDIT, answer='衛星は、追跡していない',
    scenes=[
        dict(text='スマホの地図は、あなたの居場所を表示します。では、空の上のGPS衛星は、あなたの居場所を、知っているのでしょうか。', big='衛星は、居場所を知っている？', art='assets/gps/art_sky.png'),
        dict(text='公式サイトによると、衛星は、自分の位置や状態、そして正確な時刻などを、電波で送っています。', big='衛星が送るのは、位置・状態・時刻など', src='GPS.gov', art='assets/gps/art_orbit.png', col='white'),
        dict(text='居場所を計算するのは、その電波を受け取った、あなたの端末です。', big='位置を計算するのは、端末', src='GPS.gov', art='assets/gps/art_phone.png'),
        dict(text='GPS.govのFAQによると、GPS衛星そのものは、地上のものを追跡していません。灯台のように、一方向に、信号を送っているだけです。', big='灯台のように、一方向', src='GPS.gov FAQ', art='assets/gps/art_lighthouse.png', col='white'),
        dict(text='ただし、スマホの通信機能や、アプリを通じて、位置情報が外へ送られる場合は、あります。', big='通信やアプリから、外へ出ることはある', src='MITの解説', art='assets/gps/art_phone.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/gps/art_finale.png')]))
print('written')
