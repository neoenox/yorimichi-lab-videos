"""単独Short 第8弾（2026-11-04）＝「Shorts先行」の新作10本。戦国の「通説の出どころ」9本＋食料自給率1本。
台本は、長尺の検証メモ（docs/themes/*/09_script_v2.md）にある記述だけを使う。新しい調査・画像生成はしない。
usage: python scripts/gen_solo_shorts7.py → data/short_solo_*.json。その後 make_short2.py / pack_short.py / yt_api.py upload（非公開）。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
IDS = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))
CREDIT = '・イラスト：ChatGPT(OpenAI)による生成イラスト（イメージです。実在の場面・人物・資料の再現ではありません）'
LONG_TITLE = {}
for l in (R / 'out' / 'stats_1104.txt').read_text(encoding='utf8').splitlines():
    p = [x.strip() for x in l.split('|')]
    if len(p) >= 7:
        LONG_TITLE[p[5]] = p[6]


def J(n, pack, o):
    vid = IDS[pack]['video_id']
    o['long_id'] = vid
    o['long_title'] = LONG_TITLE.get(vid) or o.get('long_title') or pack
    o.setdefault('credit', CREDIT)
    (R / 'data' / f'short_{n}.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')
    print('wrote', n, vid, o['long_title'][:30])


def end():
    return dict(text='くわしくは、長い動画で、確かめています。', end=True)


def A(slug, name): return f'assets/{slug}/art_{name}.png'


NOTE = '・研究者の解説や報道の要約による内容で、原典(原本)そのものの照合は、今回は行っていません。'

# 1. 山崎「洞ヶ峠」
J('solo_horagatoge_yamazaki', '28_yamazaki', dict(
    title='洞ヶ峠の日和見は本当？', pron='data/yamazaki_pronunciations.json', art=A('yamazaki', 'dusk'),
    hook='山崎の戦いの前、筒井順慶が洞ヶ峠で日和見をした、という逸話があります。その話を確かめます。',
    notes='■ 動画で確かめたこと\n・筒井順慶が洞ヶ峠で日和見をした、という逸話は、確かめられません。\n・順慶は、居城の郡山城で軍議を重ねた、と説明されます。\n・「天王山」と同じく、「洞ヶ峠」も言葉として残りました。\n' + NOTE,
    answer='逸話は、確かめられない',
    scenes=[
        dict(text='山崎の戦いの前、筒井順慶は、洞ヶ峠で、日和見をした。そう伝わる逸話があります。', big='筒井順慶の「洞ヶ峠」', art=A('yamazaki', 'dusk')),
        dict(text='ところが、この逸話は、確かめられません。', big='逸話は、確かめられない', art=A('yamazaki', 'docs'), col='white'),
        dict(text='順慶は、居城の郡山城で、軍議を重ねた、と説明されます。', big='郡山城で、軍議を重ねた', src='山崎の戦いの解説（二次情報）', art=A('yamazaki', 'march')),
        dict(text='「天王山」と並ぶ言葉になりましたが、中身は、確かめられていないのです。', big='言葉は残ったが、中身は不明', art=A('yamazaki', 'rain'), col='white'),
        end()]))

# 3. 賤ヶ岳「与力」
J('solo_yoriki_shizugatake', '29_shizugatake', dict(
    title='前田利家は、勝家の家臣？', pron='data/shizugatake_pronunciations.json', art=A('shizugatake', 'dusk'),
    hook='賤ヶ岳で柴田勝家を裏切った、と言われる前田利家。利家は、勝家の家臣だったのでしょうか。',
    notes='■ 動画で確かめたこと\n・利家は、勝家の家臣ではなく、与力だったと説明されます(研究者の説)。\n・与力とは、大将の指揮のもとで一緒に戦う、協力者のような立場です。\n' + NOTE,
    answer='家臣ではなく、与力と説明される',
    scenes=[
        dict(text='賤ヶ岳の戦いで、前田利家は、柴田勝家を、裏切って退いた。そう語られます。', big='前田利家は、裏切った？', art=A('shizugatake', 'dusk')),
        dict(text='ところが、利家は、勝家の家臣では、なく、与力だったと、説明されます。', big='家臣ではなく、与力', src='研究者の説', art=A('shizugatake', 'docs'), col='white'),
        dict(text='与力とは、大将の指揮のもとで、一緒に戦う、協力者のような立場です。', big='与力＝一緒に戦う協力者', art=A('shizugatake', 'lake')),
        dict(text='ただし、これは研究者の説明です。立場をどう呼ぶかで、この話の見え方は、変わります。', big='立場で、見え方が変わる', art=A('shizugatake', 'dusk'), col='white'),
        end()]))

# 4. 賤ヶ岳「密約」
J('solo_mitsuyaku_shizugatake', '29_shizugatake', dict(
    title='利家の裏切りに、密約はあった？', pron='data/shizugatake_pronunciations.json', art=A('shizugatake', 'docs'),
    hook='前田利家は、戦いの前に、秀吉と密約を結んでいた。その話を、同時代の記録で確かめます。',
    notes='■ 動画で確かめたこと\n・『柴田退治記』(秀吉の側がその年のうちにまとめた記録)は、戦場での離脱には触れません。二十二日に利家らが越前府中で降参した、と記すだけです。\n・事前の密約を裏付ける同時代の史料は、確認されていない、との指摘があります。\n・動機の説明の多くは、江戸時代初めの『甫庵太閤記』など、後世の記述に由来する、との見方もあります。\n' + NOTE,
    answer='密約の同時代の史料は、確認されていない',
    scenes=[
        dict(text='前田利家は、戦いの最中に、退いたと、語られます。事前に、秀吉と、密約があった、という話もあります。', big='利家と秀吉の「密約」？', art=A('shizugatake', 'dusk')),
        dict(text='秀吉の側が、その年のうちにまとめた、『柴田退治記』は、戦場での離脱には、触れません。', big='『柴田退治記』は、離脱に触れない', src='『柴田退治記』', art=A('shizugatake', 'docs'), col='white'),
        dict(text='事前の密約を、裏付ける、同時代の史料は、確認されていない、との指摘があります。', big='密約の史料は、確認されていない', src='研究者の指摘', art=A('shizugatake', 'lake')),
        dict(text='動機の説明の多くは、江戸時代初めの、『甫庵太閤記』など、後世の記述に、由来するとの見方もあります。', big='説明の多くは、後世の記述', src='研究者の説', art=A('shizugatake', 'docs'), col='white'),
        end()]))

# 5. 小牧・長久手「朱印状」
J('solo_shuinjo_komaki', '32_komaki', dict(
    title='小牧・長久手 和議を求めたのは？', pron='data/komaki_pronunciations.json', art=A('komaki', 'docs'),
    hook='小牧・長久手の戦いで、和議を申し入れたのは、どちらだったのか。新しく見つかった朱印状から確かめます。',
    notes='■ 動画で確かめたこと\n・2026年5月、兵庫県たつの市の旧家で、秀吉の朱印状が二通見つかったと報じられました。\n・朱印状には、信雄と家康から人質を出すので和議を、と申し入れがあった、と書かれています(報道で紹介された範囲)。\n・東京大学史料編纂所の村井祐樹准教授は、和議を申し入れたのが家康の側だったことが、はっきりした、と話します(報道)。\n・朱印状は、長久手の局地戦と戦争全体を分けて考える材料の一つです。\n・朱印状の原文は、今回は確認していません。\n' + NOTE,
    answer='申し入れたのは、家康の側と報じられた',
    scenes=[
        dict(text='二〇二六年五月、兵庫県たつの市の旧家で、秀吉の朱印状が、二通、見つかったと、報じられました。', big='秀吉の朱印状が、二通', src='報道', art=A('komaki', 'docs')),
        dict(text='朱印状には、信雄と家康から、人質を出すので和議を、と、申し入れがあった、とあります。', big='「人質を出すので、和議を」', src='報道で紹介された範囲', art=A('komaki', 'dusk'), col='white'),
        dict(text='東京大学史料編纂所の、村井祐樹准教授は、和議を申し入れたのが、家康の側だったことが、はっきりした、と話します。', big='申し入れたのは、家康の側', src='報道（研究者の説）', art=A('komaki', 'hill')),
        dict(text='ただし、朱印状は、長久手の局地戦と、戦争全体を、分けて考える、材料の一つです。', big='局地戦と、戦争全体は、別', art=A('komaki', 'docs'), col='white'),
        end()]))

# 6. 小牧・長久手「勝ち？」
J('solo_yonmikata_komaki', '32_komaki', dict(
    title='長久手は勝ち、でも戦争は？', pron='data/komaki_pronunciations.json', art=A('komaki', 'hill'),
    hook='長久手の戦いだけを見れば、徳川方の勝ちです。では、戦争全体では、どうだったのでしょうか。',
    notes='■ 動画で確かめたこと\n・長久手の戦いだけを見れば、徳川方の勝ちです(通説)。\n・戦争の全体では、信雄が秀吉と和睦し、家康は戦う大義を失いました(通説)。\n・家康がいつ服従したかは、1584年の講和、1586年の上洛、1586年の天正地震のあと、1590年の小田原征伐、など、研究者の見方が分かれます。\n' + NOTE,
    answer='服従の時期は、研究者の見方が分かれる',
    scenes=[
        dict(text='長久手の戦いだけを見れば、徳川方の勝ちです。', big='長久手だけなら、徳川の勝ち', src='通説', art=A('komaki', 'hill')),
        dict(text='しかし、戦争の全体では、信雄が、秀吉と和睦し、家康は、戦う大義を、失いました。', big='全体では、大義を失った', src='通説', art=A('komaki', 'dusk'), col='white'),
        dict(text='では、家康は、いつ服従したのか。一五八四年の講和、一五八六年の上洛、天正地震のあと、一五九〇年の小田原征伐。', big='いつ服従した？ 見方は四つ', src='研究者の説', art=A('komaki', 'docs')),
        dict(text='どの時点を、服従とみるかで、小牧・長久手の見え方は、変わります。', big='どの時点で見るかで、変わる', art=A('komaki', 'hill'), col='white'),
        end()]))

# 9. 三方ヶ原「酒井の太鼓」
J('solo_taiko_mikata', '33_mikatagahara', dict(
    title='「酒井の太鼓」は本当？', pron='data/mikatagahara_pronunciations.json', art=A('mikatagahara', 'castle'),
    hook='三方ヶ原の夜、酒井忠次が櫓で太鼓を打ち、武田軍に伏兵を疑わせた。その話を確かめます。',
    notes='■ 動画で確かめたこと\n・酒井忠次が櫓で太鼓を打ち、武田軍に伏兵を疑わせた、という話は有名です(通説)。\n・この話は、1873年(明治6年)に初演された歌舞伎で広まった、とされます(研究者の解説)。\n・『三河後風土記』にも、その記述はないとされます。\n・『信長公記』(Wikisourceの翻刻で確認)にも、この話は書かれていません。\n' + NOTE,
    answer='広めたのは、明治の歌舞伎とされる',
    scenes=[
        dict(text='酒井忠次が、櫓で太鼓を打ち、武田軍に、伏兵を疑わせた。三方ヶ原の、有名な話です。', big='酒井忠次の、太鼓の話', art=A('mikatagahara', 'castle')),
        dict(text='この話は、一八七三年、明治六年に初演された、歌舞伎で、広まったとされます。', big='広めたのは、明治の歌舞伎', src='研究者の解説（二次情報）', art=A('mikatagahara', 'docs'), col='white'),
        dict(text='『三河後風土記』にも、その記述は、ないとされます。', big='『三河後風土記』にも、ない', src='研究者の解説（二次情報）', art=A('mikatagahara', 'plateau')),
        dict(text='同時代に近い『信長公記』にも、この話は、書かれていません。', big='『信長公記』にも、ない', src='『信長公記』', art=A('mikatagahara', 'ravine'), col='white'),
        end()]))

# 10. 三方ヶ原「小山田信茂の投石隊」
J('solo_oyamada_mikata', '33_mikatagahara', dict(
    title='「小山田信茂の投石隊」は本当？', pron='data/mikatagahara_pronunciations.json', art=A('mikatagahara', 'plateau'),
    hook='三方ヶ原で、武田軍の先頭に立って石を投げた、小山田信茂の投石隊。この話を確かめます。',
    notes='■ 動画で確かめたこと\n・『信長公記』は、投石隊を「水股之者」と名づけた三百人ほど、と書きますが、小山田信茂の名はありません(Wikisourceの翻刻で確認)。\n・江戸時代の『総見記』の書き方が誤読され、明治の参謀本部の本で、信茂が率いたと書かれて広まった、とされます(研究者の解説)。\n' + NOTE,
    answer='『信長公記』に、信茂の名はない',
    scenes=[
        dict(text='三方ヶ原で、武田軍の先頭には、小山田信茂の、投石隊がいた。有名な話です。', big='小山田信茂の、投石隊', art=A('mikatagahara', 'plateau')),
        dict(text='『信長公記』は、投石隊を、「水股之者」と名づけた、三百人ほどだと、書いています。', big='「水股之者」三百人ほど', src='『信長公記』', art=A('mikatagahara', 'docs'), col='white'),
        dict(text='ところが、そこに、小山田信茂の名は、ありません。', big='信茂の名は、ない', src='『信長公記』', art=A('mikatagahara', 'ravine')),
        dict(text='江戸時代の『総見記』の書き方が、誤読され、明治の参謀本部の本で、信茂が率いたと書かれて、広まった、とされます。', big='誤読が、広まった', src='研究者の解説（二次情報）', art=A('mikatagahara', 'docs'), col='white'),
        end()]))

# 11. 関ヶ原「毛利の起請文」
J('solo_kishomon_sekigahara', '27_sekigahara', dict(
    title='南宮山の毛利は、なぜ動かなかった？', pron='data/sekigahara_pronunciations.json', art=A('sekigahara', 'council'),
    hook='関ヶ原で、南宮山の毛利勢は、主戦場の戦いに加わりませんでした。その背景にある起請文を、確かめます。',
    notes='■ 動画で確かめたこと\n・南宮山には、毛利秀元や吉川広家らの軍勢がいました。毛利関係の兵は、およそ一万六千とする記録があります。\n・吉川広家は、東軍と通じていました。\n・9月14日、徳川方の本多忠勝と井伊直政は、広家らに起請文を送りました。忠節を尽くせば毛利家を粗略にせず、領地も現状のままにする、という内容です。\n・南宮山の毛利勢は、主戦場での戦いに加わりませんでした。\n・起請文の原本は、今回は確認していません(研究者の要約による)。\n' + NOTE,
    answer='東軍との約束があった、とされる',
    scenes=[
        dict(text='関ヶ原で、西軍の有力な軍勢だった毛利勢は、南宮山にいました。毛利関係の兵は、およそ一万六千と、する記録があります。', big='南宮山の毛利勢', src='研究者の解説（二次情報）', art=A('sekigahara', 'council')),
        dict(text='ところが、吉川広家は、東軍と、通じていました。', big='吉川広家は、東軍と通じていた', art=A('sekigahara', 'old_docs'), col='white'),
        dict(text='九月十四日、徳川方の本多忠勝と井伊直政は、広家らに、起請文を送りました。忠節を尽くせば、毛利家を粗略にせず、領地も現状のままにする、という内容です。', big='起請文：毛利家を粗略にしない', src='研究者の要約（二次情報）', art=A('sekigahara', 'old_docs')),
        dict(text='南宮山の毛利勢は、主戦場での戦いに、加わりませんでした。', big='主戦場に、加わらなかった', art=A('sekigahara', 'fog'), col='white'),
        end()]))

# 12. 姉川「陣替え」
J('solo_jinkae_anegawa', '34_anegawa', dict(
    title='姉川、信長と家康は陣を替えた？', pron='data/anegawa_pronunciations.json', art=A('anegawa', 'dawn'),
    hook='姉川の戦いで、信長と家康は、陣を入れ替えた。そう書く本があります。その話を確かめます。',
    notes='■ 動画で確かめたこと\n・『東照宮御実紀』は、信長はもともと朝倉に向かい、家康は浅井に向かう予定だったが、暁に信長が朝倉の大軍を見て陣を替えた、と書きます(後世の編纂物)。\n・『信長公記』(Wikisourceの翻刻で確認)は、西の三田村口に、一番合戦として家康が向かった、と書きます。\n' + NOTE,
    answer='陣替えは、後世の編纂物の話',
    scenes=[
        dict(text='姉川の戦いで、信長と家康は、陣を入れ替えた。そう書く本があります。', big='信長と家康が、陣を入れ替えた？', art=A('anegawa', 'dawn')),
        dict(text='『東照宮御実紀』は、書きます。信長は、もともと、朝倉に向かい、家康は、浅井に向かう予定でした。', big='予定：信長は朝倉、家康は浅井', src='『東照宮御実紀』（後世の編纂物）', art=A('anegawa', 'docs'), col='white'),
        dict(text='ところが、暁に、信長は、朝倉の大軍を見て、陣を替えた、というのです。', big='朝倉の大軍を見て、陣を替えた', src='『東照宮御実紀』（後世の編纂物）', art=A('anegawa', 'castle')),
        dict(text='同時代に近い『信長公記』が伝えるのは、西の三田村口へ、家康が、一番合戦として、向かった、ということです。', big='『信長公記』：西の三田村口へ家康', src='『信長公記』', art=A('anegawa', 'river'), col='white'),
        end()]))

# 14. 食料自給率「小麦」
J('solo_komugi_jikyu', '42_jikyu', dict(
    title='小麦の自給率は、約16％？', pron='data/jikyu_pronunciations.json', art=A('jikyu', 'market'),
    hook='日本の小麦は、どのくらい国内で作られているのか。農林水産省の資料の数字で、確かめます。',
    notes='■ 動画で確かめたこと\n・小麦は、国内で作られた量が約103万トン、国内で消費に向けられた量が約659万トンです(農林水産省の資料。令和7年度の概算)。\n・割ると、約16％です。\n・数字は概算です。\n',
    answer='約16％',
    scenes=[
        dict(text='日本の小麦は、どのくらい、国内で作られているのでしょうか。', big='小麦の自給率は？', art=A('jikyu', 'market')),
        dict(text='国内で作られた量は、約百三万トンです。', big='国内で作られた量：約103万トン', src='農林水産省（令和7年度・概算）', art=A('jikyu', 'farm'), col='white'),
        dict(text='国内で消費に向けられた量は、約六百五十九万トンです。', big='消費に向けた量：約659万トン', src='農林水産省（令和7年度・概算）', art=A('jikyu', 'harbor')),
        dict(text='割ると、国産は、約十六パーセント。足りない分は、輸入などで、まかなわれています。', big='国産は、約16％', src='農林水産省（令和7年度・概算）', art=A('jikyu', 'market'), col='white'),
        end()]))
