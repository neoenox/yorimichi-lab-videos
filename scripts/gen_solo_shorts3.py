"""単独Short 第4弾（江戸の飛脚・火消し・一両）の spec。長尺のイラストと読み辞書を流用し、新しい画像は作らない。
long_id は data/youtube_ids.json の台帳から読む（長尺をアップしてから実行。台帳にない題材は飛ばす）。
usage: python scripts/gen_solo_shorts3.py → data/short_solo_*.json。その後 make_short2.py / pack_short.py / yt_api.py upload。"""
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


J('solo_hikyaku_40x', '59_hikyaku', dict(
    title='急ぎの飛脚は、並便の40倍？',
    long_title='江戸の手紙は、大坂まで何日で届いた？ 飛脚の日数と値段を確かめる',
    pron='data/hikyaku_pronunciations.json', art='assets/hikyaku/art_intro.png',
    hook='江戸の飛脚には、急ぎの便があったそうです。値段が、どれだけ違ったか、計算で確かめます。',
    notes='■ 動画で確かめたこと\n・解説記事によると、町飛脚の「並便」は10日以内に届ける便で、料金は30文。最短5日ほどの便は1200文です(二次情報)。\n・1200÷30＝40倍です(自作の計算)。\n・料金の原典は確認していません。出典は本編の概要欄にまとめています。',
    answer='約40倍の差（記事の数字）',
    scenes=[
        dict(text='江戸の飛脚には、急ぎの便が、あったそうです。', big='急ぎの飛脚は、いくら？', art='assets/hikyaku/art_intro.png'),
        dict(text='解説記事によると、並便は、十日以内に届けて、三十文でした。', big='並便：10日以内で30文', src='解説記事（二次情報）', art='assets/hikyaku/art_shop.png', col='white'),
        dict(text='一方、最短五日ほどの便は、千二百文です。千二百を三十で割ると、四十倍になります。', big='5日ほどの便は1200文', sub='1200÷30＝40倍', src='解説記事・自作の計算', art='assets/hikyaku/art_road.png'),
        dict(text='日数が半分になるかわりに、値段は四十倍。ただし、料金の原典は、確認していません。', big='日数は半分、値段は40倍', sub='料金の原典は未確認', src='自作のまとめ', art='assets/hikyaku/art_shop.png', col='white'),
        end()]))

J('solo_hikeshi_kowasu', '60_hikeshi', dict(
    title='燃えた家より、壊された家が多い？',
    long_title='江戸の火消しは、家を壊して火を止めた？ 東京消防庁の解説で確かめる',
    pron='data/hikeshi_pronunciations.json', art='assets/hikeshi/art_intro.png',
    hook='江戸の火消しは、家を壊して火を止めた、と聞いたことはありませんか。解説を確かめます。',
    notes='■ 動画で確かめたこと\n・東京消防庁の解説によると、火が広がらないよう、火元のまわりの家を取り壊す消し方が中心でした。\n・ある解説は、燃えた家よりも、壊された家のほうが多い火事もあった、と説明しています(原典は未確認)。\n・龍吐水という手押しポンプもありましたが、放水の力は今ほどではなかった、とされます。',
    answer='壊す消し方が中心',
    scenes=[
        dict(text='江戸の火消しは、水をかけず、家を壊して火を止めた。そう聞いたことは、ありませんか。', big='火消しは、家を壊した？', art='assets/hikeshi/art_intro.png'),
        dict(text='東京消防庁の解説では、火が広がらないよう、火元のまわりの家を、取り壊したとされています。', big='まわりの家を、取り壊す', src='東京消防庁の解説', art='assets/hikeshi/art_fire.png', col='white'),
        dict(text='ある解説は、燃えた家よりも、壊された家のほうが多い火事もあった、と説明しています。', big='壊された家のほうが多い火事も', sub='ある解説の説明（原典は未確認）', src='解説記事（二次情報）', art='assets/hikeshi/art_town.png'),
        dict(text='水の道具もありましたが、放水の力は、今ほどではなかった、とされています。', big='水の道具は、補助だった？', sub='龍吐水の放水の力は、今ほどでない', src='東京消防庁の解説', art='assets/hikeshi/art_fire.png', col='white'),
        end()]))

J('solo_ryo_soba', '61_ryo', dict(
    title='そば16文から、一両を計算すると？',
    long_title='江戸の一両は、今の十万円ほどだった？ 換算の幅を確かめる',
    pron='data/ryo_pronunciations.json', art='assets/ryo/art_intro.png',
    hook='江戸の一両は、今の十万円くらい、と聞いたことはありませんか。その計算の仕方を、確かめます。',
    notes='■ 動画で確かめたこと\n・『江戸のお勘定』を紹介する記事によると、かけそば1杯16文を約480円とみなし、1文を約30円、1両を約12万円と計算しています(検索結果で確認した要約。書籍の原文は未確認)。\n・別の記事は、1両の価値は8万〜20万円ほどの幅で動くようだと述べています。\n・国立国会図書館の案内でも、時代や地域で基準が違うため、正確な値は出せないとされています。',
    answer='約12万円。ただし8万〜20万円の幅',
    scenes=[
        dict(text='江戸の一両は、今の、十万円くらい。そう聞いたことは、ありませんか。', big='江戸の一両は、いくら？', art='assets/ryo/art_intro.png'),
        dict(text='よく使われる計算では、かけそば一杯、十六文を、今の約四百八十円とみなします。', big='そば16文＝約480円', src='解説記事（二次情報）', art='assets/ryo/art_shop.png', col='white'),
        dict(text='すると、一文は約三十円。一両は、約十二万円と、計算されています。', big='1文30円、1両は約12万円', src='解説記事（二次情報）', art='assets/ryo/art_coins.png'),
        dict(text='ただし、別の記事では、八万円から二十万円ほどの幅があります。基準しだいで、変わるようです。', big='8万〜20万円の幅がある', sub='基準によって変わる', src='解説記事（二次情報）', art='assets/ryo/art_coins.png', col='white'),
        end()]))
