"""単独Short 第6弾（第8〜9弾の長尺71〜76に付ける、1切り口のShort 6本）の spec。長尺のイラストと読み辞書を流用し、新しい画像は作らない。
long_id は data/youtube_ids.json の台帳から読む（長尺が未アップなら飛ばす）。
usage: python scripts/gen_solo_shorts5.py → data/short_solo_*.json。その後 make_short2.py / pack_short.py / yt_api.py upload。"""
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


J('solo_yoigoshi_hi', '71_yoigoshi', dict(
    title='宵越しの銭、理由は三つ？',
    long_title='江戸っ子は、宵越しの銭を持たなかった？ 解説記事の由来で確かめる',
    pron='data/yoigoshi_pronunciations.json', art=A('yoigoshi', 'intro'),
    hook='江戸っ子は、宵越しの銭は持たない。その理由として、挙げられる説明を、確かめます。',
    notes='■ 動画で確かめたこと\n・解説記事によると、由来は、火事の多さ、上方への対抗意識、仕事に困らなかったこと、の三つが挙げられています。\n・火事の説では、約260年の間に約90件の大火が記録され、3年に一度ほどだったとされます。\n・どれも推定の言い方で、庶民の収入や貯蓄の数字は、今回確認できていません。',
    answer='由来は三つの説明。どれも推定',
    scenes=[
        dict(text='江戸っ子は、宵越しの銭は持たない。その理由は、どう説明されているのでしょう。', big='宵越しの銭を持たない理由は？', art=A('yoigoshi', 'intro')),
        dict(text='一つめは、火事です。解説記事によると、約二百六十年に、約九十件の大火が記録され、三年に一度ほどでした。', big='大火：約260年で約90件', sub='三年に一度ほど', src='解説記事（二次情報）', art=A('yoigoshi', 'fire'), col='white'),
        dict(text='二つめは、上方への対抗意識。三つめは、仕事に困らなかったことです。', big='上方への対抗意識／仕事に困らなかった', src='解説記事（二次情報）', art=A('yoigoshi', 'stall')),
        dict(text='ただし、どれも推定です。庶民の収入や貯蓄の数字は、確認できていません。', big='どれも推定。数字は未確認', src='自作のまとめ', art=A('yoigoshi', 'fire'), col='white'),
        end()]))

J('solo_hanabi_kikin', '72_hanabi', dict(
    title='隅田川の花火は、慰霊の花火？',
    long_title='隅田川の花火は、飢饉の犠牲者を慰める花火から始まった？ 解説記事で確かめる',
    pron='data/hanabi_pronunciations.json', art=A('hanabi', 'intro'),
    hook='隅田川の花火は、飢饉の犠牲者の供養から始まった、と聞いたことはありませんか。確かめます。',
    notes='■ 動画で確かめたこと\n・解説記事によると、1732年の大飢饉の翌年、1733年に、慰霊と悪病退散のため、川開きと花火が行われたとされます。\n・両国橋周辺の料理屋が公許を得て花火を打ち上げたのが、由来と説明されています。\n・江戸時代の史料は、記事に示されておらず、今回確認できていません。',
    answer='慰霊と悪病退散が由来と説明されるが、史料は未確認',
    scenes=[
        dict(text='隅田川の花火は、飢饉の犠牲者を慰める、供養の花火から始まった。本当でしょうか。', big='花火は、供養から始まった？', art=A('hanabi', 'intro')),
        dict(text='解説記事によると、一七三二年に大飢饉があり、翌年、慰霊と悪病退散のため、川開きが行われました。', big='1732年 大飢饉 → 1733年 川開き', src='解説記事（二次情報）', art=A('hanabi', 'house'), col='white'),
        dict(text='このとき、両国橋周辺の料理屋が、公許を得て、花火を打ち上げた、と説明されています。', big='料理屋が、公許を得て打ち上げた', src='解説記事（二次情報）', art=A('hanabi', 'craft')),
        dict(text='ただし、江戸時代の史料は、記事に示されておらず、今回、確認できていません。', big='江戸時代の史料は、未確認', src='自作のまとめ', art=A('hanabi', 'intro'), col='white'),
        end()]))

J('solo_ooka_shirakoya', '73_ooka', dict(
    title='大岡裁き、本人が裁いたのは一件',
    long_title='大岡裁きは、大岡忠相が実際に裁いた話だった？ 解説記事で確かめる',
    pron='data/ooka_pronunciations.json', art=A('ooka', 'intro'),
    hook='大岡裁きは、名奉行が実際に裁いた話だ。そう思っていませんか。解説記事で確かめます。',
    notes='■ 動画で確かめたこと\n・解説記事によると、大岡裁きとして伝わる話は十六編で、大岡本人が担当したのは、白子屋お熊の一件だけです。\n・「実母継母詮議の事」は中国の『棠陰比事』、「石地蔵吟味の事」は『包公案』が元になっているとされます。\n・三方一両損の出典は、今回確認できていません。',
    answer='ほぼ創作。本人が裁いたのは白子屋の一件',
    scenes=[
        dict(text='大岡裁きは、名奉行の大岡忠相が、実際に裁いた話。そう思っていませんか。', big='大岡裁きは、実話？', art=A('ooka', 'intro')),
        dict(text='解説記事によると、大岡裁きとして伝わるのは、十六編。本人が担当したのは、白子屋お熊の一件だけです。', big='十六編のうち、本人の担当は一件', sub='白子屋お熊の一件', src='解説記事（二次情報）', art=A('ooka', 'scroll'), col='white'),
        dict(text='元ネタが、中国の裁判書の話もあります。たとえば、『棠陰比事』や『包公案』です。', big='元ネタは、中国の裁判書も', sub='『棠陰比事』『包公案』', src='解説記事（二次情報）', art=A('ooka', 'stone')),
        dict(text='ただし、三方一両損の出典は、今回、確認できていません。', big='三方一両損の出典は、未確認', src='自作のまとめ', art=A('ooka', 'scroll'), col='white'),
        end()]))

J('solo_hatsugatsuo_4ryo', '74_hatsugatsuo', dict(
    title='初鰹は、年収二年分？',
    long_title='江戸っ子は、女房を質に入れても初鰹を食べた？ 国立国会図書館の解説で確かめる',
    pron='data/hatsugatsuo_pronunciations.json', art=A('hatsugatsuo', 'intro'),
    hook='女房を質に入れても初鰹。その値段を、収入と比べて、確かめます。',
    notes='■ 動画で確かめたこと\n・国立国会図書館の解説によると、文政のころ、初鰹は一本四両の高値がついたといいます。町方の奉公人の年収は、男性で約二両です。\n・四両は二両の二倍で、年収の二年分になります(自作の計算)。\n・四両は伝聞の数字で、一次史料は確認できていません。質入れの実例も未確認です。',
    answer='四両は年収の二年分。ただし伝聞で一次史料は未確認',
    scenes=[
        dict(text='女房を質に入れても、初鰹。その値段は、収入と比べて、どれほどだったのでしょう。', big='初鰹の値段は？', art=A('hatsugatsuo', 'intro')),
        dict(text='解説によると、文政のころ、初鰹は一本、四両。町方の奉公人の年収は、約二両です。', big='初鰹：四両／年収：約二両', src='国立国会図書館の解説（二次情報）', art=A('hatsugatsuo', 'coin'), col='white'),
        dict(text='四両は、二両の二倍。つまり、年収の二年分です。これは、自作の計算です。', big='四両 ÷ 二両 ＝ 二倍', sub='年収の二年分', src='自作の計算', art=A('hatsugatsuo', 'fish')),
        dict(text='ただし、四両は伝聞で、一次史料は未確認です。質入れの実例も、確認できていません。', big='伝聞の数字。実例は未確認', src='自作のまとめ', art=A('hatsugatsuo', 'coin'), col='white'),
        end()]))

J('solo_jinko_suitei', '75_jinko', dict(
    title='江戸の百万人は、確定？',
    long_title='江戸は、人口100万人で世界最大の都市だった？ 博物館の解説と百科事典で確かめる',
    pron='data/jinko_pronunciations.json', art=A('jinko', 'intro'),
    hook='江戸は、人口百万人の世界最大の都市だった。この数字は、確かなのでしょうか。',
    notes='■ 動画で確かめたこと\n・江戸東京博物館の記事は、18世紀初頭に武家と町人で人口100万人を超えたと「推定されています」と述べます。\n・百科事典の説明を紹介する検索結果では、町人は1695年に35万人、1721年に50万人で、武家は同数とみた見積もりです。\n・世界最大かどうかは、資料で「世界有数」「最大という説」と言い方が分かれています。東京都の資料の原文は未確認です。',
    answer='百万人超は推定。世界最大かは言い方が分かれる',
    scenes=[
        dict(text='江戸は、人口百万人の、世界最大の都市だった。この数字は、確かなのでしょうか。', big='江戸の人口は、百万人？', art=A('jinko', 'intro')),
        dict(text='江戸東京博物館の記事は、百万人を超えたと、「推定されています」と述べます。', big='「推定されています」', sub='十八世紀初頭、武家と町人で百万人超', src='江戸東京博物館の記事（二次情報）', art=A('jinko', 'street'), col='white'),
        dict(text='町人は、一六九五年に三十五万人、一七二一年に五十万人。武家は、同数とみた見積もりです。', big='町人：35万人 → 50万人', sub='武家は同数とみた見積もり', src='百科事典の説明（検索結果の紹介）', art=A('jinko', 'scroll')),
        dict(text='世界最大かどうかは、資料で、言い方が分かれます。「有数」「最大という説」などです。', big='世界最大かは、言い方が分かれる', src='自作のまとめ', art=A('jinko', 'street'), col='white'),
        end()]))

J('solo_oyatsu_yatsu', '76_oyatsu', dict(
    title='おやつは、八つ時が語源？',
    long_title='おやつは、江戸の時刻「八つ時」が語源だった？ 解説記事で確かめる',
    pron='data/oyatsu_pronunciations.json', art=A('oyatsu', 'intro'),
    hook='おやつの語源は、江戸の時刻の八つ時。そう言われる理由を、確かめます。',
    notes='■ 動画で確かめたこと\n・解説記事によると、昼の八つ時、今の14時ごろに食べる間食を、御八つと呼んだことが語源とされています。\n・江戸中期までは一日二食、後期以降は三食になり、おやつの時間が15時ごろにずれた、と説明されています。\n・二食から三食への時期の裏付けは、今回確認できていません。',
    answer='八つ時の間食が語源とされる。三時への変化の裏付けは未確認',
    scenes=[
        dict(text='おやつの語源は、江戸の時刻の、八つ時。どういうことでしょう。', big='おやつの語源は、八つ時？', art=A('oyatsu', 'intro')),
        dict(text='昼の八つ時は、今の十四時ごろ。鐘は、八回鳴らされました。この時刻の間食が、御八つです。', big='八つ時＝十四時ごろ', sub='この時刻の間食が「御八つ」', src='解説記事（二次情報）', art=A('oyatsu', 'bell'), col='white'),
        dict(text='今が三時なのは、一日三食になり、食べる時間が、後ろにずれたため、と説明されています。', big='二食 → 三食で、三時に', src='解説記事（二次情報）', art=A('oyatsu', 'sweets')),
        dict(text='ただし、その時期の裏付けは、今回、確認できていません。', big='変化の時期は、未確認', src='自作のまとめ', art=A('oyatsu', 'bell'), col='white'),
        end()]))
