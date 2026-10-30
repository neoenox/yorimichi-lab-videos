"""単独Short 第5弾（第5〜7弾の長尺に付ける、1切り口のShort 9本）の spec。長尺のイラストと読み辞書を流用し、新しい画像は作らない。
long_id は data/youtube_ids.json の台帳から読む（台帳にない題材は飛ばす）。
usage: python scripts/gen_solo_shorts4.py → data/short_solo_*.json。その後 make_short2.py / pack_short.py / yt_api.py upload。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
CREDIT = '・イラスト：ChatGPT(OpenAI)による生成イラスト（イメージです。実在の場面・人物・資料の再現ではありません）'
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


def A(slug, name): return f'assets/{slug}/art_{name}.png'


J('solo_sankin_tabi10', '62_sankin', dict(
    title='参勤交代、いちばん高いのは旅？',
    long_title='参勤交代は、大名を貧乏にする制度だった？ 解説記事の数字で確かめる',
    pron='data/sankin_pronunciations.json', art=A('sankin', 'intro'),
    hook='参勤交代は、長い旅で、大名を貧乏にした、と聞いたことはありませんか。費用の中身を、確かめます。',
    notes='■ 動画で確かめたこと\n・nippon.comの解説記事によると、加賀藩の1808年の帰国の費用は約5500両(往復で約1万1000両)です。\n・各藩の年間経費のうち、江戸での支出は約43〜78％を占めました。\n・往復の旅費は、江戸での支出の約10分の1程度とされています。費用の数字は記事の紹介で、原典は確認していません。',
    answer='旅より、江戸での暮らしが中心',
    scenes=[
        dict(text='参勤交代は、長い旅で、大名の財布を、空にした。そう聞いたことは、ありませんか。', big='いちばん高いのは、旅？', art=A('sankin', 'intro')),
        dict(text='解説記事によると、加賀藩の帰国の費用は、約五千五百両。往復で、約一万一千両です。', big='帰国の費用：約5500両', sub='往復で、約1万1000両', src='nippon.comの解説記事（二次情報）', art=A('sankin', 'river'), col='white'),
        dict(text='ところが、各藩の経費のうち、江戸での支出は、約四十三から七十八パーセントを占めました。', big='江戸での支出：43〜78％', sub='各藩の年間経費のうち', src='nippon.comの解説記事（二次情報）', art=A('sankin', 'mansion')),
        dict(text='往復の旅費は、江戸での支出の、十分の一ほどです。負担の中心は、江戸での暮らしでした。', big='旅費は、江戸の支出の約10分の1', sub='数字は記事の紹介（原典は未確認）', src='解説記事・自作のまとめ', art=A('sankin', 'mansion'), col='white'),
        end()]))

J('solo_sushi_two', '63_sushi', dict(
    title='江戸の握り2つで、そば1杯？',
    long_title='江戸の握り寿司は、屋台のファストフードだった？ 『守貞謾稿』の紹介記事で確かめる',
    pron='data/sushi_pronunciations.json', art=A('sushi', 'intro'),
    hook='江戸の握り寿司は、屋台で手軽に食べられた、と聞いたことはありませんか。値段を、比べてみます。',
    notes='■ 動画で確かめたこと\n・nippon.comの解説記事によると、握り1貫は8文、玉子焼は16文です。\n・かけそば1杯を16文とする説明と比べると、握り2つでそば1杯ほどです(自作の比較)。\n・値段は記事の紹介で、『守貞謾稿』の原文は確認していません。かけそば16文は別の解説の数字で、出典は未確認です。',
    answer='握り2つで、そば1杯ほど（自作の比較）',
    scenes=[
        dict(text='江戸の握り寿司は、屋台の軽食だった、と言われます。では、値段は、どうだったのでしょう。', big='握り寿司の値段は？', art=A('sushi', 'intro')),
        dict(text='解説記事によると、握り一貫は、八文です。玉子焼は、十六文でした。', big='握り1貫：8文', sub='玉子焼は16文', src='nippon.comの解説記事（二次情報）', art=A('sushi', 'sushi'), col='white'),
        dict(text='かけそば一杯を、十六文とする説明と比べると、握り二つで、そば一杯ほどです。', big='握り2つ＝かけそば1杯ほど', sub='そば16文は、別の説明の数字', src='解説記事・自作の比較', art=A('sushi', 'stall')),
        dict(text='ただし、これは記事の紹介で、原文は確認していません。円への換算も、扱いません。', big='原文は未確認。円換算はしない', src='自作のまとめ', art=A('sushi', 'sushi'), col='white'),
        end()]))

J('solo_shorui_niwatori', '64_shorui', dict(
    title='鶏を撃つと死罪？ 生類憐みの令の処罰',
    long_title='生類憐みの令では、犬を殺すと死刑だった？ 解説記事の処罰の例で確かめる',
    pron='data/shorui_pronunciations.json', art=A('shorui', 'intro'),
    hook='生類憐みの令では、厳しい処罰があった、と言われます。解説記事にある例を、確かめます。',
    notes='■ 動画で確かめたこと\n・解説記事によると、鶏を射殺した家来は死罪、子犬を捨てた者は市中引き回しのうえ獄門になった例があります。\n・ただし、犬を殺して死刑になった事例は、今回確認できていません。\n・処罰の例は記事の紹介で、原典の記録は確認していません。',
    answer='厳罰の例はあるが、犬殺しの死刑は未確認',
    scenes=[
        dict(text='生類憐みの令では、動物を傷つけると、重い罰を受けた。そう聞いたことは、ありませんか。', big='どんな罰があった？', art=A('shorui', 'intro')),
        dict(text='解説記事によると、鶏を射殺した家来が、死罪になった例があります。', big='鶏を射殺：死罪', src='Into JAPAN WARAKUの解説記事（二次情報）', art=A('shorui', 'board'), col='white'),
        dict(text='子犬を捨てた者が、市中引き回しのうえ、獄門になった例も、紹介されています。', big='子犬を捨てる：引き回しのうえ獄門', src='Into JAPAN WARAKUの解説記事（二次情報）', art=A('shorui', 'dogs')),
        dict(text='ただし、犬を殺して死刑になった事例は、今回、確認できていません。原典の記録も、確認していません。', big='犬殺しで死刑の事例は、確認できず', sub='処罰の例は記事の紹介', src='自作のまとめ', art=A('shorui', 'dogs'), col='white'),
        end()]))

J('solo_yachin_rokubai', '65_yachin', dict(
    title='長屋の家賃、記事で6倍も違う？',
    long_title='江戸の長屋の家賃は、月4800円ほどだった？ 解説記事の数字で確かめる',
    pron='data/yachin_pronunciations.json', art=A('yachin', 'intro'),
    hook='江戸の長屋の家賃は、今のお金でいくらだったのでしょう。記事の数字を、比べてみます。',
    notes='■ 動画で確かめたこと\n・ある解説記事は、九尺二間の長屋の家賃を、現代の感覚で月約4875円としています。\n・別の記事は、割長屋の家賃を月3万円としています。約6倍の差があり、換算の前提が違います。\n・坪あたり月100文という前提なら、3坪で月300文になります(自作の計算で、当時の記録ではありません)。',
    answer='円の金額は、記事で大きく違い、決められない',
    scenes=[
        dict(text='江戸の長屋の家賃は、今のお金で、いくらだったのでしょう。解説記事を、比べてみます。', big='長屋の家賃は、いくら？', art=A('yachin', 'intro')),
        dict(text='ある記事は、九尺二間の長屋で、月、約四千八百七十五円としています。', big='ある記事：月約4875円', src='解説記事（二次情報）', art=A('yachin', 'room'), col='white'),
        dict(text='別の記事は、割長屋で、月三万円です。同じ長屋でも、六倍ほど違います。', big='別の記事：月約3万円', sub='約6倍の差', src='解説記事（二次情報）', art=A('yachin', 'gate')),
        dict(text='換算の前提が違うので、円の数字は、一つに決められません。当時の記録も、確認していません。', big='円の数字は、決められない', sub='当時の記録は未確認', src='自作のまとめ', art=A('yachin', 'room'), col='white'),
        end()]))

J('solo_yakurei_menkyo', '66_yakurei', dict(
    title='江戸の医者に、免許はなかった？',
    long_title='江戸の医者は、名乗れば誰でも開業できた？ 解説記事で薬代まで確かめる',
    pron='data/yakurei_pronunciations.json', art=A('yakurei', 'intro'),
    hook='江戸時代の医者は、名乗れば、誰でも開業できた、と聞いたことはありませんか。解説を確かめます。',
    notes='■ 動画で確かめたこと\n・解説記事によると、当時の医者の資格は免許制ではなく、名乗れば誰でも開業できたとされます。\n・そのため質はまちまちで、実力のある藩医もいれば、評判の悪い町医者もいたと述べられています。\n・薬代にあたる薬礼は、額が決まっておらず、盆暮れにまとめて払う場合もありました。出典は二次情報です。',
    answer='免許制ではなかった、と説明されている',
    scenes=[
        dict(text='江戸時代の医者は、名乗れば、誰でも開業できた。そう聞いたことは、ありませんか。', big='医者に、免許は？', art=A('yakurei', 'intro')),
        dict(text='解説記事によると、当時の医者の資格は、免許制ではなく、名乗れば誰でも開業できたとされます。', big='免許制ではなかった', src='解説記事（二次情報）', art=A('yakurei', 'herbs'), col='white'),
        dict(text='そのため、質はまちまちで、実力のある藩医もいれば、評判の悪い町医者も、いたそうです。', big='質は、まちまち', sub='実力のある藩医もいた', src='解説記事（二次情報）', art=A('yakurei', 'kago')),
        dict(text='薬代の薬礼は、額が決まっておらず、盆暮れに、まとめて払う場合もありました。', big='薬礼：額は決まっていない', sub='盆暮れにまとめて払う場合も', src='解説記事（二次情報）', art=A('yakurei', 'herbs'), col='white'),
        end()]))

J('solo_chushingura_14_15', '67_chushingura', dict(
    title='討ち入りは、14日か15日か？',
    long_title='忠臣蔵の討ち入りは、12月14日ではなかった？ 旧暦と新暦のずれを確かめる',
    pron='data/chushingura_pronunciations.json', art=A('chushingura', 'intro'),
    hook='忠臣蔵の討ち入りは、十二月十四日、と言われます。十五日とも言える、という説明を、確かめます。',
    notes='■ 動画で確かめたこと\n・解説記事によると、討ち入りは旧暦の元禄15年12月14日の寅の上刻(午前4時ごろ)とされます。\n・一日の起点を午前0時ごろの正子とすれば12月15日、夜明けの明け六つとすれば14日とする見方も誤りではない、と述べられています。\n・新暦への換算は、記事で1日ずれており、この動画では決めていません。',
    answer='一日の起点しだいで、14日とも15日とも言える',
    scenes=[
        dict(text='忠臣蔵の討ち入りは、十二月十四日。そう習った人は、多いでしょう。', big='討ち入りは、14日？', art=A('chushingura', 'intro')),
        dict(text='解説記事によると、討ち入りは、寅の上刻、午前四時ごろです。', big='寅の上刻：午前4時ごろ', src='解説記事（二次情報）', art=A('chushingura', 'moon'), col='white'),
        dict(text='一日の起点を、午前零時ごろの正子とすれば、十五日。夜明けの明け六つとすれば、十四日です。', big='正子なら15日、明け六つなら14日', src='解説記事（二次情報）', art=A('chushingura', 'dawn')),
        dict(text='どちらも誤りではない、と記事は述べます。新暦への換算は、記事で一日ずれており、決めていません。', big='新暦は、記事で1日ずれる', sub='この動画では決めない', src='自作のまとめ', art=A('chushingura', 'dawn'), col='white'),
        end()]))

J('solo_doyo_shiryo', '68_doyo', dict(
    title='丑の日のうなぎは、源内が広めた？',
    long_title='うなぎの丑の日は、平賀源内が広めた？ 解説記事で由来を確かめる',
    pron='data/doyo_pronunciations.json', art=A('doyo', 'intro'),
    hook='土用の丑の日にうなぎを食べるのは、平賀源内が広めたから、と言われます。裏付けを、確かめます。',
    notes='■ 動画で確かめたこと\n・解説記事によると、夏のうなぎは人気がなく、うなぎ屋が平賀源内に相談した、とされます。\n・読んだ記事は、源内説に具体的な史料や出典を示していません。\n・夏にうなぎという考えは、万葉集の大伴家持の歌から、奈良時代にはあったと記事は述べます。丑の日に食べる風習の始まりは、確認できていません。',
    answer='源内説は有名だが、史料は確認できない',
    scenes=[
        dict(text='土用の丑の日に、うなぎを食べるのは、平賀源内が広めたから。そう聞いたことは、ありませんか。', big='丑の日のうなぎは、源内？', art=A('doyo', 'intro')),
        dict(text='解説記事によると、夏のうなぎは人気がなく、困ったうなぎ屋が、源内に相談したとされます。', big='うなぎ屋が、源内に相談', src='解説記事（二次情報）', art=A('doyo', 'board'), col='white'),
        dict(text='ただし、読んだ記事は、この話の史料や出典を、示していません。', big='史料や出典は、示されていない', src='解説記事（二次情報）', art=A('doyo', 'desk')),
        dict(text='夏にうなぎ、という考えは、万葉集の歌から、奈良時代には、あったと記事は述べます。', big='夏のうなぎ：奈良時代から', sub='丑の日の風習の始まりは未確認', src='解説記事・自作のまとめ', art=A('doyo', 'desk'), col='white'),
        end()]))

J('solo_nukemairi_hishaku', '69_nukemairi', dict(
    title='柄杓ひとつで、伊勢参り？',
    long_title='子どもが黙って伊勢参り？ 抜け参りは許された？ 各地の資料で確かめる',
    pron='data/nukemairi_pronunciations.json', art=A('nukemairi', 'intro'),
    hook='江戸時代には、手形もお金もなく、伊勢参りに出かけた人がいた、と言われます。資料を、確かめます。',
    notes='■ 動画で確かめたこと\n・奈良市の資料によると、許可を得ず、旅行手形も持たずに出た参宮者は、柄杓を差し出して食べ物などの施しを求めました。\n・道中の町々は、食事や宿の世話をしました。\n・静岡県の資料は、1830年に徳島の手習屋の子ども20〜30人が一緒に出発したことを紹介しています。帰ってから咎められたかは、確認できていません。',
    answer='道中は、施しで旅ができたと説明される',
    scenes=[
        dict(text='江戸時代には、手形もお金も持たずに、伊勢参りに出かけた人が、いたそうです。', big='手ぶらで、伊勢参り？', art=A('nukemairi', 'intro')),
        dict(text='奈良市の資料によると、そうした人は、柄杓を差し出して、食べ物などの施しを求めました。', big='柄杓で、施しを求めた', src='奈良市の資料（二次情報）', art=A('nukemairi', 'ladle'), col='white'),
        dict(text='道中の町々は、食事や宿の世話をした、とされます。一八三〇年には、徳島の子ども二十人から三十人が、一緒に出発した記述もあります。', big='道中の町々が、食事や宿を世話', sub='1830年、徳島の子ども20〜30人', src='奈良市・静岡県の資料（二次情報）', art=A('nukemairi', 'road')),
        dict(text='ただし、帰ってから咎められたかは、今回の資料では、確認できていません。', big='お咎めの有無は、確認できず', src='自作のまとめ', art=A('nukemairi', 'road'), col='white'),
        end()]))

J('solo_kashihon_800', '70_kashihon', dict(
    title='江戸に、貸本屋が800軒？',
    long_title='江戸の庶民は、本を借りて読んでいた？ 貸本屋800軒を確かめる',
    pron='data/kashihon_pronunciations.json', art=A('kashihon', 'intro'),
    hook='江戸には、本を背負って貸し歩く、貸本屋がいたそうです。その数を、確かめます。',
    notes='■ 動画で確かめたこと\n・解説によると、1808年の江戸には貸本屋が少なくとも656軒あり、天保のころの『江戸繁昌記』では800軒とされます。\n・1軒あたりの得意先は、170〜180軒ほどという説明です。\n・研究者の池上英子さんによると、貸す料金は買う値段の約6分の1です。数字は個人ブログの紹介で、原典は未確認です。',
    answer='800軒ほどあったとされる',
    scenes=[
        dict(text='江戸には、本を背負って、貸して歩く、貸本屋がいたそうです。その数は、どれほどでしょう。', big='貸本屋は、何軒？', art=A('kashihon', 'intro')),
        dict(text='解説によると、一八〇八年の江戸には、少なくとも六百五十六軒。天保のころは、八百軒とされます。', big='656軒（1808年）→800軒（天保）', src='解説（二次情報）', art=A('kashihon', 'shelf'), col='white'),
        dict(text='一軒あたりの得意先は、百七十から百八十軒ほど、という説明です。', big='得意先：170〜180軒ほど', src='解説（二次情報）', art=A('kashihon', 'bundle')),
        dict(text='貸す料金は、買う値段の六分の一ほどだそうです。ただし、数字の原典は、確認していません。', big='貸す料金は、買う値段の約6分の1', sub='原典は未確認', src='解説・自作のまとめ', art=A('kashihon', 'bundle'), col='white'),
        end()]))
