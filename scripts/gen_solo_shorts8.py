"""単独Short 第9弾（2026-11-04）＝「Shorts先行・頻度アップ」の新作12本。脳10%2・ガリレオ・物価・コロンブス・賞味期限・桶狭間・月・鳥取城・手取川前史・島原の乱・食料輸入先。
台本は長尺の検証メモ（docs/themes/*/09_script_v2.md、08_fact_check.md）にある記述だけを使う。新しい調査・画像生成はしない。
usage: python scripts/gen_solo_shorts8.py → data/short_solo_*.json。その後 make_short2.py / pack_short.py / yt_api.py upload（非公開）。"""
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
NOTE = '・解説や報道の要約による内容で、原典(原本)そのものの照合は、今回は行っていません。'

# 桶狭間は、読み辞書がないので、三方ヶ原の辞書に足したものを使う
ok = json.loads((R / 'data' / 'mikatagahara_pronunciations.json').read_text(encoding='utf8'))
ok.update({'桶狭間': 'オケハザマ', '小瀬甫庵': 'オゼホアン', '信長記': 'シンチョウキ', '迂回': 'ウカイ', '義元': 'ヨシモト', '今川': 'イマガワ'})
(R / 'data' / 'okehazama_pron_short.json').write_text(json.dumps(ok, ensure_ascii=False, indent=1), encoding='utf8')


def J(n, pack, o):
    vid = IDS[pack]['video_id']
    o['long_id'] = vid
    o["long_title"] = o.get("long_title") or LONG_TITLE.get(vid) or pack
    o.setdefault('credit', CREDIT)
    (R / 'data' / f'short_{n}.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')
    print('wrote', n, vid, o['long_title'][:26])


def end():
    return dict(text='くわしくは、長い動画で、確かめています。', end=True)


def A(slug, name): return f'assets/{slug}/art_{name}.png'


# 1. 脳10%の出どころ
J('solo_brain_origin', '41_brain10', dict(
    title='「脳の10％」は、誰の言葉？', pron='data/brain10_pronunciations.json', art=A('brain10', 'intro'),
    hook='「人は、脳の十パーセントしか使っていない」。この数字の出どころを、確かめます。',
    notes='■ 動画で確かめたこと\n・発端としてよく挙げられるのは、心理学者ウィリアム・ジェームズの1907年の論文「人間のエネルギー」です。\n・原文には、「十パーセント」という数字は出てきません(Wikisourceの原文で確認)。\n・1936年、ローウェル・トーマスがデール・カーネギーの本の序文で、この考えを紹介したことが、広まるきっかけの一つだったとされます。\n・序文で語られたのは「能力の十パーセント」だとされ、「脳の十パーセント」という言い方は、その後に広まった、と説明されています。\n' + NOTE,
    answer='数字は、原文にない',
    scenes=[
        dict(text='人は、脳の十パーセントしか使っていない。この話の発端として、よく挙げられるのは、心理学者のジェームズです。', big='発端は、ジェームズの論文？', sub='1907年「人間のエネルギー」', art=A('brain10', 'intro')),
        dict(text='ところが、その論文の原文に、「十パーセント」という数字は、出てきません。', big='原文に「10％」はない', src='ジェームズの原文（Wikisource）', art=A('brain10', 'study'), col='white'),
        dict(text='一九三六年、ローウェル・トーマスが、カーネギーの本の序文で、この考えを紹介しました。広まるきっかけの一つだった、とされます。', big='1936年、カーネギーの本の序文', src='研究者の解説（二次情報）', art=A('brain10', 'lamp')),
        dict(text='語られたのは、「能力の十パーセント」だとされます。能力の話が、脳の話に、すり替わっていきました。', big='能力の話が、脳の話にすり替わった', src='研究者の解説（二次情報）', art=A('brain10', 'crowd'), col='white'),
        end()]))

# 2. 脳10%：損傷
J('solo_brain_damage', '41_brain10', dict(
    title='脳の9割は、使われていない？', pron='data/brain10_pronunciations.json', art=A('brain10', 'scan'),
    hook='脳の九割が使われていないのなら、そこが傷ついても、影響は出ないはずです。確かめます。',
    notes='■ 動画で確かめたこと\n・もし九割が使われていないなら、そこが傷ついても影響は出ないはずです。\n・ところが、脳の十パーセントよりずっと小さい範囲が傷つくだけでも、重い影響が出ることがあります(Beyerstein 2004の紹介による)。\n・どの部分の損傷でも、何らかの影響が出うるとされ、「何も担当していない場所」は見つかっていません。\n・「沈黙の皮質」と呼ばれた領域は、働きが分かりにくく、「何もしていない」と誤解された可能性がある、とされます。\n' + NOTE,
    answer='何も担当しない場所は、見つかっていない',
    scenes=[
        dict(text='脳の九割が、使われていないなら、そこが傷ついても、影響は、出ないはずです。', big='九割が未使用なら、傷ついても平気？', art=A('brain10', 'scan')),
        dict(text='ところが、十パーセントよりずっと小さい範囲が、傷つくだけでも、重い影響が出ることがあります。', big='小さな傷でも、重い影響', src='解説（二次情報）', art=A('brain10', 'clinic'), col='white'),
        dict(text='どの部分でも、損傷すれば、何らかの影響が出うる。「何も担当していない場所」は、見つかっていません。', big='「担当のない場所」は、見つかっていない', src='解説（二次情報）', art=A('brain10', 'study')),
        dict(text='「沈黙の皮質」と呼ばれた領域は、働きが分かりにくく、「何もしていない」と、誤解された可能性がある、とされます。', big='「沈黙の皮質」は、誤解だった？', src='解説（二次情報）', art=A('brain10', 'lamp'), col='white'),
        end()]))

# 3. ガリレオ
J('solo_galileo_sore', '44_galileo', dict(
    title='「それでも地球は動く」は本当？', pron='data/galileo_pronunciations.json', art=A('galileo', 'hall'),
    hook='ガリレオが裁判のあとにつぶやいた、「それでも地球は動く」。この言葉の最も古い記録を、確かめます。',
    notes='■ 動画で確かめたこと\n・この言葉が、印刷物で確認されている最も古い例は、1757年とされます(Wikipedia「And yet it moves」)。\n・ジュゼッペ・バレッティが、ロンドンで出した、英語の本『イタリアン・ライブラリー』です。\n・ガリレオの弟子ヴィヴィアーニが書いた最初の伝記には、この言葉は出てきません。裁判の記録にも、引用されていないとされます。\n・ガリレオが異端の疑いで裁判にかけられ、地動説を撤回させられたことは、歴史の解説で述べられています(Scientific American)。\n' + NOTE,
    answer='最古の印刷は1757年とされる',
    scenes=[
        dict(text='ガリレオは、裁判のあとに、「それでも地球は動く」と、つぶやいた。有名な話です。', big='「それでも地球は動く」', art=A('galileo', 'hall')),
        dict(text='この言葉が、印刷物で確認されている、最も古い例は、一七五七年とされます。ロンドンで出た、英語の本です。', big='最古の印刷物は、1757年', src='Wikipedia「And yet it moves」', art=A('galileo', 'books'), col='white'),
        dict(text='ガリレオの弟子が書いた、最初の伝記に、この言葉は、出てきません。裁判の記録にも、引用されていないとされます。', big='最初の伝記にも、裁判の記録にもない', src='Wikipedia（二次情報）', art=A('galileo', 'gallery')),
        dict(text='ただし、地動説を撤回させられたことは、歴史の解説で、述べられています。', big='撤回させられたこと自体は、述べられている', src='Scientific American', art=A('galileo', 'sky'), col='white'),
        end()]))

# 4. 物価：家庭で違う
J('solo_bukka_katei', '43_bukka', dict(
    title='物価の上昇、家庭で違う？', pron='data/bukka_pronunciations.json', art=A('bukka', 'shop'),
    hook='物価の上がり方は、どの家庭も同じなのか。総務省の指数で、確かめます。',
    notes='■ 動画で確かめたこと\n・2025年の全国の消費者物価は、前の年より3.2%上がりました(総務省)。\n・総務省は、勤労者世帯を年収の低い順に五つに分けた指数も作っています。2025年は、最も低い五分の一が3.3%、次が3.1%、真ん中が3.0%です。\n・最も低い層と最も高い層の差は、0.6ポイントです(自作の計算)。\n・全国の数字と、勤労者世帯の数字は、対象が違います。\n',
    answer='差はあるが、1ポイント未満',
    scenes=[
        dict(text='二〇二五年、全国の消費者物価は、前の年より、三・二パーセント上がりました。', big='全国の物価：3.2％上昇', src='総務省', art=A('bukka', 'shop')),
        dict(text='総務省は、勤労者世帯を、年収の低い五つに分けた、指数も作っています。', big='年収で五つに分けた指数', src='総務省', art=A('bukka', 'home'), col='white'),
        dict(text='最も低い五分の一が、三・三パーセント。次が三・一パーセント。真ん中は、三・〇パーセントです。', big='低い層3.3％／真ん中3.0％', src='総務省（2025年）', art=A('bukka', 'wallet')),
        dict(text='最も低い層と、最も高い層の差は、〇・六ポイント。どの家庭も同じではありませんが、差は、一ポイント未満でした。', big='差は、0.6ポイント', src='総務省・自作の計算', art=A('bukka', 'office'), col='white'),
        end()]))

# 5. コロンブス
J('solo_columbus_flat', '31_flatearth', dict(
    title='コロンブスと学者は、何でもめた？', pron='data/flatearth_pronunciations.json', art=A('flatearth', 'ship'),
    hook='コロンブスは、地球は丸いと説いて、平らだと信じる人たちと戦った。この話の出どころを、確かめます。',
    notes='■ 動画で確かめたこと\n・1828年に、アメリカの作家ワシントン・アーヴィングが書いたコロンブスの伝記に、スペインのサラマンカで学者たちがコロンブスに反対する場面があります(原文の抜粋で確認)。\n・ドレイパーとホワイトが、「科学と宗教は戦ってきた」という見方で、この話を広めた、とされます(二次情報)。\n・もめたのは、地球の大きさです。コロンブスは、地球の大きさを実際より小さく見積もっていました(二次情報)。\n' + NOTE,
    answer='もめたのは、地球の大きさ',
    scenes=[
        dict(text='コロンブスは、地球は丸いと説いて、平らだと信じる人たちと、戦った。よく聞く話です。', big='丸い地球 vs 平らな地球？', art=A('flatearth', 'ship')),
        dict(text='一八二八年に、アメリカの作家アーヴィングが書いた、コロンブスの伝記に、学者たちが反対する場面があります。', big='1828年、アーヴィングの伝記', src='アーヴィング『コロンブスの生涯と航海』', art=A('flatearth', 'book'), col='white'),
        dict(text='ドレイパーとホワイトが、「科学と宗教は戦ってきた」という見方で、この話を広めた、とされます。', big='「科学と宗教の戦い」で広まった', src='研究者の解説（二次情報）', art=A('flatearth', 'press')),
        dict(text='実際にもめたのは、地球の大きさです。コロンブスは、実際より小さく、見積もっていました。', big='もめたのは、地球の大きさ', src='研究者の解説（二次情報）', art=A('flatearth', 'map'), col='white'),
        end()]))

# 6. 賞味期限
J('solo_shomi_sugitara', '28_shomi', dict(
    title='賞味期限を過ぎたら、食べられない？', pron='data/shomi_pronunciations.json', art='assets/shomi/gen_open.png',
    hook='賞味期限を一日過ぎた。もう食べられないのでしょうか。表示の決まりで、確かめます。',
    notes='■ 動画で確かめたこと\n・消費期限は、定められた方法で保存した場合に、安全性を欠くおそれがないと認められる期限です。\n・賞味期限は、定められた方法で保存した場合に、期待される品質が十分に保てると認められる期限です。\n・未開封で、表示どおりに保存していた食品の賞味期限は、「過ぎたら食べられない」という期限ではありません。\n・開封後まで保証する期限ではありません。\n・消費者庁の期限表示のガイドラインの説明をもとにしています。\n',
    answer='「過ぎたら食べられない」期限ではない',
    scenes=[
        dict(text='賞味期限を、一日過ぎた。この食品は、もう、食べられないのでしょうか。', big='賞味期限を、一日過ぎた', art='assets/shomi/gen_open.png'),
        dict(text='賞味期限は、定められた方法で保存した場合に、期待される品質が、十分に保てると認められる期限です。', big='賞味期限＝品質が保てる期限', src='消費者庁のガイドライン', art='assets/shomi/gen_shelf.png', col='white'),
        dict(text='消費期限は、安全性を欠くおそれがないと、認められる期限です。', big='消費期限＝安全性の期限', src='消費者庁のガイドライン', art='assets/shomi/gen_cold.png'),
        dict(text='未開封で、表示どおりに保存していた食品の、賞味期限は、「過ぎたら食べられない」という期限では、ありません。', big='「過ぎたら食べられない」ではない', src='消費者庁のガイドライン', art='assets/shomi/gen_pack.png', col='white'),
        end()]))

# 7. 桶狭間：迂回奇襲
J('solo_okehazama_ukai', '14_okehazama', dict(
    title='桶狭間は、迂回奇襲だった？', pron='data/okehazama_pron_short.json', art=A('okehazama', 'downpour'),
    hook='桶狭間の戦いは、信長が迂回して奇襲した。その説が、いまどう見られているかを確かめます。',
    notes='■ 動画で確かめたこと\n・信長は義元の居場所を知り、ひそかに迂回し、豪雨に乗じて丘の上から奇襲した、という迂回攻撃説があります。\n・これは、江戸時代の小瀬甫庵の『信長記』で取り上げられ、長く定説とされてきました。\n・現在は、迂回攻撃説には、否定的な見解が多いとされています。\n・織田方が今川本陣を攻撃したのは、約二千人とされます。\n' + NOTE,
    answer='今は、否定的な見解が多い',
    scenes=[
        dict(text='信長は、義元の居場所を知り、ひそかに迂回し、豪雨に乗じて、丘の上から奇襲した。桶狭間の、有名な説です。', big='迂回して、豪雨の中で奇襲？', art=A('okehazama', 'downpour')),
        dict(text='この説は、江戸時代の小瀬甫庵の『信長記』で取り上げられ、長く、定説とされてきました。', big='江戸時代の『信長記』から、定説に', src='解説（二次情報）', art=A('okehazama', 'old_book'), col='white'),
        dict(text='ところが、現在は、迂回攻撃説には、否定的な見解が多いとされています。', big='今は、否定的な見解が多い', src='解説（二次情報）', art=A('okehazama', 'war_council')),
        dict(text='織田方が、今川本陣を攻撃したのは、約二千人とされます。', big='今川本陣を攻めたのは、約2千人', src='解説（二次情報）', art=A('okehazama', 'field_dusk'), col='white'),
        end()]))

# 8. 月の裏側
J('solo_moon_dark', '15_moon_rotation', dict(
    title='月の裏側は、ずっと暗い？', pron='data/moon_pronunciations.json', art=A('moon', 'dark'),
    hook='地球から見えない月の裏側を、「暗い側」と呼ぶ人がいます。本当に、ずっと暗いのでしょうか。',
    notes='■ 動画で確かめたこと\n・地球から見えない側を、「暗い側」と呼ぶ人もいます。\n・月では、時間とともに、日光が当たる場所と、暗くなる場所が入れ替わります。地球から見えない側も、ずっと暗いわけではありません(NASA Science『Moon Facts』)。\n・同じ面が地球に見え続けるのは、自転と公転の時間が同じだからです。\n',
    answer='裏側にも、昼と夜がある',
    scenes=[
        dict(text='地球から見えない月の裏側を、「暗い側」と呼ぶ人がいます。', big='月の裏側は、「暗い側」？', art=A('moon', 'dark')),
        dict(text='ところが、月では、時間とともに、日光が当たる場所と、暗くなる場所が、入れ替わります。', big='日光が当たる場所は、入れ替わる', src='NASA Science', art=A('moon', 'motion'), col='white'),
        dict(text='地球から見えない側も、ずっと暗いわけでは、ありません。', big='裏側にも、昼と夜がある', src='NASA Science', art=A('moon', 'why')),
        dict(text='同じ面が見え続けるのは、自転と公転の時間が、同じだからです。', big='同じ面が見えるのは、周期が同じだから', src='NASA Science', art=A('moon', 'sync'), col='white'),
        end()]))

# 9. 鳥取城：兵糧
J('solo_tottori_hyoro', '35_tottori', dict(
    title='鳥取城、兵糧不足はいつから？', long_title='【鳥取の渇え殺しは計画どおり？】鳥取城の戦い 米の買い占めは本当か｜地図と『信長公記』で検証', pron='data/tottori_pronunciations.json', art=A('tottori', 'castle'),
    hook='鳥取城の飢えは、秀吉の包囲で始まった。そう思われがちですが、記録を確かめます。',
    notes='■ 動画で確かめたこと\n・天正9年の3月、吉川経家が鳥取城に入りました(研究者の説)。\n・経家は、入城した時点で、すでに兵糧が足りないと書き送っていた、といわれます(研究者の説)。\n・『信長公記』は、霜や露に打たれて、弱い者は際限なく餓死した、と書きます。\n・餓死した人の数は、書かれていません。\n' + NOTE,
    answer='入城時すでに、兵糧不足と書き送っていた',
    scenes=[
        dict(text='天正九年の三月、吉川経家が、鳥取城に入りました。', big='吉川経家、鳥取城へ', src='研究者の説', art=A('tottori', 'castle')),
        dict(text='ところが、経家は、入城した時点で、すでに、兵糧が足りないと、書き送っていた、といわれます。', big='入城時から、兵糧不足', src='研究者の説', art=A('tottori', 'docs'), col='white'),
        dict(text='『信長公記』は、霜や露に打たれて、弱い者は、際限なく餓死した、と書きます。', big='『信長公記』：際限なく餓死', src='『信長公記』', art=A('tottori', 'mountain')),
        dict(text='ただし、餓死した人の数は、書かれていません。', big='餓死した人数は、書かれていない', src='『信長公記』', art=A('tottori', 'castle'), col='white'),
        end()]))

# 10. 手取川の前：七尾城
J('solo_nanao_tedorigawa', '36_tedorigawa', dict(
    title='手取川の前に、七尾城で何が？', long_title='【手取川は大敗だった？】手取川の戦い 謙信の書状と『信長公記』で検証｜地図で解説', pron='data/tedorigawa_pronunciations.json', art=A('tedorigawa', 'castle'),
    hook='手取川の戦いの前、能登の七尾城で何があったのか。研究者の説明を、確かめます。',
    notes='■ 動画で確かめたこと\n・七尾城は、能登の守護、畠山氏の城でした。重臣の長続連らが実権を握り、織田信長に救援を求めました(研究者の説)。\n・天正5年9月15日、城の中で、上杉に味方する家臣が内応した、とされます(研究者の説)。\n・長続連ら長一族のほとんどが殺され、三男の長連龍は生き延びた、とされます(研究者の説)。\n' + NOTE,
    answer='七尾城は、内応で落ちたとされる',
    scenes=[
        dict(text='能登の七尾城は、守護、畠山氏の城でした。重臣の長続連らが、実権を握っていました。', big='七尾城の実権は、長続連', src='研究者の説', art=A('tedorigawa', 'castle')),
        dict(text='長続連は、織田信長に、救援を求めました。', big='信長に、救援を求めた', src='研究者の説', art=A('tedorigawa', 'docs'), col='white'),
        dict(text='九月十五日、城の中で、上杉に味方する家臣が、内応したとされます。', big='9月15日、城内で内応', src='研究者の説', art=A('tedorigawa', 'castle')),
        dict(text='長続連ら長一族のほとんどが、殺されました。三男の長連龍は、生き延びたとされます。', big='長一族は、ほとんどが殺された', src='研究者の説', art=A('tedorigawa', 'flood'), col='white'),
        end()]))

# 11. 島原の乱：数字
J('solo_shimabara_kazu', '37_shimabara', dict(
    title='島原の乱 討伐軍の死者は何人？', pron='data/shimabara_pronunciations.json', art=A('shimabara', 'castle'),
    hook='島原の乱で、討伐軍の死者は何人だったのか。記録によって数字が違うことを、確かめます。',
    notes='■ 動画で確かめたこと\n・討伐軍の死傷者の数は、記録によって違います。\n・紹介される数字の一つは、死者1,130人、負傷者6,960人です(研究者の紹介)。\n・『有馬一件』は、死者2,800人、負傷者7,700人と記す、とされます。\n・『オランダ商館長日記』は、八万の兵のうち、死者5,712人と記す、とされます。\n・『有馬一件』と『オランダ商館長日記』の数字は、原典で確かめていません。\n',
    answer='記録によって、数字が違う',
    scenes=[
        dict(text='島原の乱で、討伐軍の死傷者の数は、記録によって、違います。', big='死傷者の数は、記録で違う', art=A('shimabara', 'castle')),
        dict(text='紹介される数字の一つは、死者千百三十人、負傷者六千九百六十人です。', big='死者1,130人／負傷者6,960人', src='研究者の紹介（二次情報）', art=A('shimabara', 'docs'), col='white'),
        dict(text='『有馬一件』は、死者二千八百人、負傷者七千七百人と、記すとされます。', big='『有馬一件』：死者2,800人', src='研究者の紹介（二次情報）', art=A('shimabara', 'sea')),
        dict(text='『オランダ商館長日記』は、八万の兵のうち、死者五千七百十二人と、記すとされます。ただし、原典では、確かめていません。', big='『日記』：死者5,712人（原典は未確認）', src='研究者の紹介（二次情報）', art=A('shimabara', 'castle'), col='white'),
        end()]))

# 12. 食料自給率：輸入先
J('solo_jikyu_yunyusaki', '42_jikyu', dict(
    title='食料の輸入先、1位はどこ？', pron='data/jikyu_pronunciations.json', art=A('jikyu', 'ship'),
    hook='日本の食料は、どこから輸入されているのか。農林水産省の試算で、確かめます。',
    notes='■ 動画で確かめたこと\n・農林水産省の試算では、供給熱量のうち、国産が37%、米国が26%、カナダが11%、豪州が10%です(令和7年度・概算)。\n・これは、国別の輸入量をもとにした試算で、実際の数字そのものではありません。\n',
    answer='米国が26％で1位（試算）',
    scenes=[
        dict(text='日本の食料の、供給熱量のうち、国産は、三十七パーセントです。', big='国産は、37％', src='農林水産省（令和7年度・試算）', art=A('jikyu', 'harbor')),
        dict(text='輸入では、米国が、二十六パーセント。いちばん多い国です。', big='米国が、26％', src='農林水産省（令和7年度・試算）', art=A('jikyu', 'ship'), col='white'),
        dict(text='カナダが、十一パーセント。豪州が、十パーセントです。', big='カナダ11％／豪州10％', src='農林水産省（令和7年度・試算）', art=A('jikyu', 'market')),
        dict(text='ただし、これは、国別の輸入量をもとにした、試算です。実際の数字そのものでは、ありません。', big='国別の輸入量をもとにした試算', src='農林水産省', art=A('jikyu', 'harbor'), col='white'),
        end()]))
