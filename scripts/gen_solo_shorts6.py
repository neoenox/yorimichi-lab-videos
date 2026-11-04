"""単独Short 第7弾（2026-11-04）＝「Shorts寄せ」実験の試作5本。戦況解説の「通説の出どころ」3本＋姉川1本＋食料自給率1本。
長尺のイラスト・読み辞書・検証メモ（docs/themes/*/08_fact_check.md）を流用し、新しい画像は作らない。
usage: python scripts/gen_solo_shorts6.py → data/short_solo_*.json。その後 make_short2.py <slug> / pack_short.py / yt_api.py upload（非公開）。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
IDS = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))
CREDIT_ART = '・イラスト：ChatGPT(OpenAI)による生成イラスト（イメージです。実在の場面・人物・資料の再現ではありません）'
CREDIT_MAP = '・図：自作（国土地理院タイル(陰影起伏図・標準地図)を加工。現代の地形で、当時の川筋や道ではありません。位置は概略の推定です）'


def J(n, pack, o):
    o['long_id'] = IDS[pack]['video_id']
    o.setdefault('credit', CREDIT_ART)
    (R / 'data' / f'short_{n}.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')
    print('wrote', n, o['long_id'])


def end():
    return dict(text='くわしくは、長い動画で、確かめています。', end=True)


def A(slug, name): return f'assets/{slug}/art_{name}.png'


# 1. 三方ヶ原「味噌」（検証メモ 20261128_mikatagahara/08_fact_check.md：出典が判明していない。類似は『三河後風土記』の一言坂の後）
J('solo_miso_mikata', '33_mikatagahara', dict(
    title='家康の「これは味噌だ」は本当？',
    long_title='【家康はなぜ出陣した？】三方ヶ原の戦い 犀ヶ崖の夜襲は本当か｜地図と『信長公記』で検証',
    pron='data/mikatagahara_pronunciations.json', art=A('mikatagahara', 'ravine'),
    hook='三方ヶ原で敗れた家康が、「これは味噌だ」と言い張った。この有名な話の出どころを、確かめます。',
    notes='■ 動画で確かめたこと\n・三方ヶ原で敗れた家康が、恐怖で失禁し、「これは味噌だ」と言い張った、という話は有名です。\n・この話は、出典が判明していない、とされています(研究者の解説。二次情報)。\n・類似の話は『三河後風土記』にありますが、そこでは一言坂の戦いの後の話です(同)。\n・『信長公記』(Wikisourceの翻刻で確認)の三方ヶ原の場面には、この話は書かれていません。\n・『三河後風土記』の原文は、今回は確認していません。',
    answer='出典は、判明していない',
    scenes=[
        dict(text='三方ヶ原で敗れた家康は、恐怖で漏らし、「これは味噌だ」と言い張った。有名な話です。', big='家康「これは味噌だ」', art=A('mikatagahara', 'ravine')),
        dict(text='ところが、この話は、出典が、判明していません。', big='出典は、判明していない', src='研究者の解説（二次情報）', art=A('mikatagahara', 'docs'), col='white'),
        dict(text='似た話は、『三河後風土記』にあります。ただし、そこでは、一言坂の戦いのあとの話です。', big='似た話は、別の戦いのあと', sub='一言坂の戦い', src='『三河後風土記』（二次情報による）', art=A('mikatagahara', 'castle')),
        dict(text='同時代に近い『信長公記』にも、この話は、書かれていません。', big='『信長公記』にも、ない', src='『信長公記』', art=A('mikatagahara', 'plateau'), col='white'),
        end()]))

# 2. 関ヶ原「問鉄砲」（検証メモ 20261205_sekigahara/09_script_v3.md 章7・11_source_check.md）
J('solo_toiteppo_sekigahara', '27_sekigahara', dict(
    title='関ヶ原「問鉄砲」は本当にあった？',
    long_title='関ヶ原の戦い 開戦は何時？ 小早川秀秋はいつ寝返った？ 史料で確かめる',
    pron='data/sekigahara_pronunciations.json', art=A('sekigahara', 'fog'),
    hook='小早川秀秋は、家康の鉄砲に脅されて寝返った。「問鉄砲」と呼ばれる話を、確かめます。',
    notes='■ 動画で確かめたこと\n・通説では、家康が松尾山へ鉄砲を撃たせ、迷う小早川秀秋を動かした、と語られます(問鉄砲)。\n・この話は、戦いから六十年以上あとの『慶長軍記』など、江戸時代の軍記に見えます(研究者の要約。原本の照合は未了)。\n・同時代の史料で、実際に撃ったと確かめられたものは、見つかっていません。\n・藤本正行氏、白峰旬氏は、後世の創作とみます。笠谷和比古氏は、撃ちかけはあったが、秀秋に決断を迫る話ではない、と考えます(いずれも研究者の紹介による)。\n・『慶長軍記』『備前老人物語』などの原文は、今回は確認していません。',
    answer='同時代の確認はなく、説は割れる',
    scenes=[
        dict(text='戦いが長引くなか、家康は、松尾山へ鉄砲を撃たせ、迷う小早川秀秋を、動かした。「問鉄砲」と呼ばれる話です。', big='家康が鉄砲で脅した？', art=A('sekigahara', 'fog')),
        dict(text='この話は、戦いから、六十年以上あとの、『慶長軍記』など、江戸時代の軍記に、見えます。', big='60年以上あとの軍記に見える', src='研究者の解説（二次情報）', art=A('sekigahara', 'old_docs'), col='white'),
        dict(text='同時代の史料で、実際に撃ったと、確かめられたものは、見つかっていません。', big='同時代の史料では、確認できず', art=A('sekigahara', 'council')),
        dict(text='藤本氏や白峰氏は、後世の創作とみます。笠谷氏は、撃ちかけはあったが、決断を迫る話ではない、と考えます。', big='研究者の説は、割れている', sub='創作説／撃ちかけはあった説', src='研究者の解説（二次情報）', art=A('sekigahara', 'aftermath'), col='white'),
        end()]))

# 3. 長篠「三段撃ち」（検証メモ 20261127_nagashino/08_fact_check.md）
J('solo_sandan_nagashino', '26_nagashino', dict(
    title='長篠「三段撃ち」は作り話？',
    long_title='【三段撃ちは作り話？】長篠の戦い 武田軍はなぜ壊滅したのか｜地図と『信長公記』で検証',
    pron='data/nagashino_pron_short.json', art='assets/nagashino/map_wide.png',
    hook='長篠の戦いで、信長は、鉄砲を三列に入れ替えて撃たせた。この話を、『信長公記』で確かめます。',
    notes='■ 動画で確かめたこと\n・鉄砲を三列に並べ、交代で撃たせた、という「三段撃ち」が、長篠の戦いの通説として知られます。\n・『信長公記』(Wikisourceの翻刻で確認)には、鉄砲を千挺ほど、五人の奉行のもとで足軽に懸けさせた、とあります。三列で入れ替えて撃つ、という説明は見当たりません。\n・交代して撃つ描写は、江戸時代の軍記(甫庵『信長記』など)に現れる、とされます(二次情報)。\n・ただし、何らかの交代射撃がなかったとまでは言い切れない、という見方もあります。\n・鉄砲の数は、写本によって千挺とも三千挺とも読める、と説明されます。',
    answer='『信長公記』には、説明がない',
    credit=CREDIT_MAP,
    scenes=[
        dict(text='鉄砲を三列に並べ、交代で撃たせた。長篠の戦いの、有名な、「三段撃ち」です。', big='鉄砲を、三列で交代？', art='assets/nagashino/map_wide.png'),
        dict(text='ところが、『信長公記』の翻刻に、三列で入れ替えて撃った、という説明は、見当たりません。', big='『信長公記』に、説明はない', src='『信長公記』', art='assets/nagashino/map_area.png', col='white'),
        dict(text='書かれているのは、鉄砲を千挺ほど、五人の奉行のもとで、足軽に懸けさせた、ということです。', big='五人の奉行に、鉄砲を預けた', src='『信長公記』', art='assets/nagashino/map_area.png'),
        dict(text='交代して撃つ描写は、江戸時代の軍記に、現れるとされます。', big='交代射撃は、後世の軍記に', src='二次情報', art='assets/nagashino/map_wide.png', col='white'),
        dict(text='ただし、何らかの交代射撃が、なかったとまでは、言い切れない、という見方もあります。', big='「なかった」とも、言い切れない', art='assets/nagashino/map_area.png'),
        end()]))

# 4. 食料自給率「卵」（検証メモ 20270130_jikyu/08_fact_check.md：鶏卵 自給率11→国産率97、牛肉13→50、豚肉5→49。令和7年度の概算）
J('solo_tamago_jikyu', '42_jikyu', dict(
    title='卵の自給率11％、なのに国産97％？',
    long_title='日本の食料自給率37％なら、食べ物の63％は輸入？ 農林水産省の資料で確かめる',
    pron='data/jikyu_pronunciations.json', art=A('jikyu', 'kitchen'),
    hook='日本の卵の自給率は、十一パーセント。ところが、国産率は九十七パーセント。この差の理由を、確かめます。',
    notes='■ 動画で確かめたこと\n・令和7年度(概算)の鶏卵は、カロリーベースの自給率が11％、食料国産率が97％です(農林水産省の資料)。\n・畜産物は、輸入した飼料で育てた分を、自給率では国産に数えません。国産率は、その分を国産に数えます。\n・牛肉は、自給率13％・国産率50％。豚肉は、5％・49％です(同)。\n・数字は概算です。',
    answer='えさが輸入だと、国産に数えない',
    scenes=[
        dict(text='日本の卵の自給率は、カロリーベースで、十一パーセントです。', big='卵の自給率は、11％', src='農林水産省（令和7年度・概算）', art=A('jikyu', 'kitchen')),
        dict(text='ところが、食料国産率では、九十七パーセント。同じ卵なのに、数字が、大きく違います。', big='国産率は、97％', src='農林水産省（令和7年度・概算）', art=A('jikyu', 'market'), col='white'),
        dict(text='理由は、決まりです。日本で育てた鶏でも、えさが輸入なら、その分は、自給率では、国産に数えません。', big='えさが輸入だと、国産に数えない', src='農林水産省', art=A('jikyu', 'farm')),
        dict(text='牛肉は、十三パーセントと、五十パーセント。豚肉は、五パーセントと、四十九パーセントです。', big='牛肉 13％→50％／豚肉 5％→49％', sub='自給率→国産率', src='農林水産省（令和7年度・概算）', art=A('jikyu', 'harbor'), col='white'),
        end()]))

# 5. 姉川「戦いの描写は数行」（『信長公記』巻三（八）あね川合戦之事 Wikisource翻刻で確認：20261205_anegawa/_ws_shinchokoki_gaji.txt）
J('solo_anegawa_suugyou', '34_anegawa', dict(
    title='姉川の戦い『信長公記』は何行？',
    long_title='【姉川は圧勝だった？】姉川の戦い 家康の活躍と十一段崩しは本当か｜地図と『信長公記』で検証',
    pron='data/anegawa_pronunciations.json', art=A('anegawa', 'river'),
    hook='姉川の戦いは、有名な戦いです。では、同時代に近い『信長公記』は、この戦いを、どれくらい書いているでしょうか。',
    notes='■ 動画で確かめたこと\n・『信長公記』は、朝倉の軍を八千ほど、浅井の軍を五千ほど、あわせて一万三千と書きます。\n・戦いそのものは、「推しつ返しつ、散々に入り乱れ」「ついに追い崩し」と、ほんの数行です(Wikisourceの翻刻で確認)。\n・織田・徳川の兵数は書かれていません。\n・磯野員昌の「十一段崩し」は『東照宮御実紀』『浅井三代記』にあり、『信長公記』にはありません。',
    answer='戦いの描写は、ほんの数行',
    scenes=[
        dict(text='姉川の戦いは、有名な戦いです。では、『信長公記』は、この戦いを、どれくらい書いているでしょうか。', big='『信長公記』は、何行書いた？', art=A('anegawa', 'river')),
        dict(text='朝倉の軍は、八千ほど。浅井の軍は、五千ほど。あわせて、一万三千と、書いています。', big='朝倉8千＋浅井5千＝1万3千', src='『信長公記』', art=A('anegawa', 'castle'), col='white'),
        dict(text='ところが、戦いそのものは、「推しつ返しつ、散々に入り乱れ」「ついに追い崩し」と、ほんの数行です。', big='戦いそのものは、ほんの数行', src='『信長公記』', art=A('anegawa', 'dawn')),
        dict(text='織田・徳川の兵数は、書かれていません。', big='織田・徳川の兵数は、ない', src='『信長公記』', art=A('anegawa', 'docs'), col='white'),
        dict(text='「十一段崩し」のような話は、『信長公記』ではなく、後世の軍記に出てきます。', big='十一段崩しは、後世の軍記', src='『東照宮御実紀』『浅井三代記』', art=A('anegawa', 'docs')),
        end()]))
