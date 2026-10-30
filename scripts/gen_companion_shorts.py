"""長尺の要約Short（江戸の2食・識字率・ナポレオン）の spec。long_id は data/youtube_ids.json の台帳から読む（長尺をアップしてから実行）。
usage: python scripts/gen_companion_shorts.py → data/short_<slug>.json"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
CREDIT = '・イラスト：ChatGPT(OpenAI)による生成イラスト（イメージです。実在の場面・人物・資料の再現ではありません）\n・図・表：自作'
IDS = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))


def J(n, pack, o):
    o['long_id'] = IDS[pack]['video_id']
    o.setdefault('credit', CREDIT)
    (R / 'data' / f'short_{n}.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')


def end():
    return dict(text='くわしくは、長い動画で、確かめています。', end=True)


J('twomeals', '50_twomeals', dict(
    title='江戸の人は、1日2食だった？', long_title='江戸時代の人は、1日2食だった？ 農林水産省の説明と解説記事で確かめる',
    pron='data/twomeals_pronunciations.json', art='assets/twomeals/art_intro.png',
    hook='「江戸時代の人は、1日2食だった」と聞いたことはありませんか。農林水産省の説明と解説記事で確かめます。',
    notes='■ 動画で確かめたこと\n・農林水産省の子ども向けページは、江戸時代の中ごろから、朝・昼・夕の1日3食になったといわれている、と説明しています。理由は、あんどんが使われて夜の活動時間が長くなったためとされています。\n・解説記事の多くは、3食の定着を元禄期(1688〜1704年)以降としています。時期には説明の幅があり、地域でも違いました。\n・原典の史料は確認していません。出典は本編の概要欄にまとめています。',
    credit=CREDIT, answer='江戸の中ごろから3食に',
    scenes=[
        dict(text='江戸時代の人は、一日二食だった。そう聞いたことは、ありませんか。', big='江戸の人は、1日2食？', art='assets/twomeals/art_intro.png'),
        dict(text='農林水産省は、江戸時代の中ごろから、朝、昼、夕の、一日三食になったといわれている、と説明しています。', big='江戸の中ごろから、1日3食に', src='農林水産省', art='assets/twomeals/art_lamp.png', col='white'),
        dict(text='理由は、あんどんが使われて、夜の活動時間が長くなったため、とされています。', big='理由：あんどんで夜が長くなった', src='農林水産省', art='assets/twomeals/art_lamp.png'),
        dict(text='解説記事は、元禄期以降に定着し、それより前は、二食が中心だったと述べています。', big='定着は、元禄期以降', sub='解説記事の説明。時期には幅がある。原典は未確認', src='二次情報', art='assets/twomeals/art_kitchen.png', col='white'),
        end()]))

J('literacy', '51_literacy', dict(
    title='江戸の識字率は、世界一？', long_title='江戸時代の日本は、識字率が世界一だった？ 寺子屋の資料で確かめる',
    pron='data/literacy_pronunciations.json', art='assets/literacy/art_intro.png',
    hook='「江戸時代の日本は、識字率が世界一だった」と聞いたことはありませんか。寺子屋の資料で確かめます。',
    notes='■ 動画で確かめたこと\n・寺子屋の解説によると、1883年の文部省の全国調査で、寺子屋は16,560軒あったとされます。\n・識字率の「50〜60％」「江戸70％超」は推定で、地域差が大きく、正確な統計はないとされています。\n・1877年の滋賀県の調査では、自分の名前を書ける人は、男子89％、女子39％でした。\n・「世界一」を、同じ基準で比べた資料は確認できませんでした。出典は本編の概要欄にまとめています。',
    credit=CREDIT, answer='「世界一」の根拠は確認できず',
    scenes=[
        dict(text='江戸時代の日本は、識字率が世界一だった。そう聞いたことは、ありませんか。', big='江戸の識字率は、世界一？', art='assets/literacy/art_intro.png'),
        dict(text='寺子屋は、一八八三年の文部省の調査で、全国に一万六千五百六十軒あったとされています。', big='寺子屋は、全国に16,560軒', src='寺子屋の解説（二次情報）', art='assets/literacy/art_desk.png', col='white'),
        dict(text='ただし、識字率の七十パーセントなどの数字は、推定で、地域差も大きいとされています。', big='70％などの数字は、推定', src='二次情報', art='assets/literacy/art_books.png'),
        dict(text='世界一を、同じ基準で比べた根拠は、今回の資料では、確認できませんでした。', big='「世界一」の根拠は、確認できず', art='assets/literacy/art_shop.png', col='white'),
        end()]))

J('napoleon', '52_napoleon', dict(
    title='ナポレオンは、背が低かった？', long_title='ナポレオンは、背が低かった？ 英語版Wikipediaと単位の計算で確かめる',
    pron='data/napoleon_pronunciations.json', art='assets/napoleon/art_intro.png',
    hook='「ナポレオンは背が低かった」「身長は157センチ」と聞いたことはありませんか。英語版Wikipediaと自分の計算で確かめます。',
    notes='■ 動画で確かめたこと\n・英語版Wikipediaによると、ナポレオンの身長は約1.67メートルで、当時の成人男性の平均くらいです。\n・157センチは、フランスと英国の単位の違いによる読み違いと説明されています。自作の計算では、5ピエ2プースは約168センチ、英国の5フィート2インチは約157センチです。\n・小柄なイメージは、英国の風刺画で広まったとされています。\n・身長の記録の原典は確認していません。出典は本編の概要欄にまとめています。',
    credit=CREDIT, answer='当時の平均くらい。157cmは単位の違い',
    scenes=[
        dict(text='ナポレオンは、背が低かった。身長は、百五十七センチ、とも言われます。', big='ナポレオンは、背が低かった？', art='assets/napoleon/art_intro.png'),
        dict(text='英語版Wikipediaでは、身長は約一メートル六十七センチで、当時の成人男性の平均くらいと、述べています。', big='身長は、約1.67メートル', sub='当時の成人男性の平均くらい', src='英語版Wikipedia', art='assets/napoleon/art_ruler.png', col='white'),
        dict(text='五ピエ二プースを、フランスの単位で計算すると、約百六十八センチ。英国の単位で読むと、約百五十七センチです。', big='168cmか、157cmか', sub='5ピエ2プース＝約168cm、5フィート2インチ＝約157cm', src='自作の計算', art='assets/napoleon/art_ruler.png'),
        dict(text='小柄なイメージは、英国の風刺画で、広まったとされています。', big='小柄なイメージは、風刺画から', src='英語版Wikipedia', art='assets/napoleon/art_print.png', col='white'),
        end()]))
