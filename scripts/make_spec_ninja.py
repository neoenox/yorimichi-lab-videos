"""Writes data/ninja_spec.json（忍者は、黒装束で手裏剣を投げていたのか？）。台本：docs/themes/20261016_ninja/09_script_v2.md
ポップ形式（style='pop'）。旧版は専用の合成（nj_compose.py）。画像は国立国会図書館デジタルコレクション（パブリックドメイン、権利確認済み。docs/themes/20261016_ninja/05_images_rights.md）。
at / until は台本の『行の番号』（章内の0始まり）。"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import finalize
R = Path(__file__).resolve().parents[1]


def pop(name, **kw): return dict(t='anim', name=name, **kw)
def tel(text, x, y, size, **kw): return dict(t='anim', name='pop_telop', text=text, x=x, y=y, size=size, **kw)
def rows(items, **kw): return dict(t='anim', name='pop_rows', items=items, **kw)
def card(inner, box, **kw):
    kw.setdefault('at', 0)
    return dict(t='anim', name='pop_card', inner=inner, box=box, **kw)


ND = 'assets/ndl_ninja/'
spec = dict(slug='ninja', theme_dir='20261016_ninja', pack='03_ninja_myths', header_sub='忍者の通説を、国立国会図書館の解説で確かめる',
 style='pop',
 images=dict(
   bg=dict(file=ND + 'hokusai_black_ninja.jpg', crop=[.55, .24, .95, .90]),
   shoninki=dict(file=ND + 'shoninki_ten_p1.jpg', crop=[.02, .03, .52, .93]),
   goemon=dict(file=ND + 'toyokuni_goemon_hisayoshi.jpg', crop=[.09, .075, .915, .86]),
   bar=dict(file=ND + 'hokusai_bar_shuriken.jpg', crop=[.50, .22, .97, .90]),
   colors=dict(file='assets/ninja/colors.png')),
 bgm=[['intro', 'books', 'piano36'], ['black', 'shuriken', 'piano12'], ['now', 'end', 'piano40']],
 chapters=[
 dict(key='intro', title='忍者のイメージ', chapter_title='導入：黒装束・覆面・手裏剣', scene=[
   pop('pop_bgimg', img='bg', at=0, dim=.55, blur=5),
   tel('忍者といえば\n[[黒装束]]・[[覆面]]・[[手裏剣]]', 960, 440, 112, at=0, until=2, rot=-2),
   tel('そのイメージは\n[[いつ、どこから]]来たのか？', 960, 440, 108, at=2, until=3, plate='red', rot=2),
   tel('国立国会図書館の解説で\n確かめる', 960, 440, 104, at=3, until=4, plate='blue', rot=-1.5),
   tel('分かることと\n決められないことを分ける', 960, 440, 100, at=4, plate='pink', rot=1.5)]),
 dict(key='shinobi', title='「忍び」とは？', chapter_title='「忍び」とは、何をした人たちか', scene=[
   tel('実際の「忍び」は、\nどんな人たち？', 960, 440, 112, at=0, until=2, rot=-2),
   rows([dict(at=2, tag='最古', text='『太平記』（14世紀後半）：石清水八幡宮に放火', col='orange'),
         dict(at=4, tag='戦国', text='「草」：情報収集や夜道の案内（とされる）', col='blue'),
         dict(at=5, tag='呼び名', text='忍び・忍びの者・草・乱波・透波', col='green'),
         dict(at=6, tag='「忍者」', text='定着は昭和30年代（山田雄司さんの説明）', col='purple'),
         dict(at=7, tag='1856年', text='『武用弁略』にも「忍者」の語（「しのびのもの」）', col='red')], x0=110, x1=1810, y0=190, size=44, gap=16)]),
 dict(key='books', title='忍術書', chapter_title='忍術書には、何が書かれているか', scene=[
   tel('江戸時代の\n[[忍術書]]', 960, 440, 120, at=0, until=1, rot=-2),
   rows([dict(at=1, tag='万川集海', text='1676年（延宝4）藤林保武が22巻に', col='orange'),
         dict(at=2, tag='正忍記', text='1681年（延宝9）成立。全3巻', col='blue'),
         dict(at=3, tag='忍秘伝', text='1655年とされるが、真偽ははっきりしない', col='purple'),
         dict(at=4, tag='七方出', text='『正忍記』に、七つの変装の姿', col='green'),
         dict(at=6, tag='注意', text='教えと、実際に誰が何をしたかは、分けて考える', col='red')], x0=70, x1=1130, y0=200, size=40, gap=16),
   card('img', [1170, 200, 1860, 760], img='shoninki', cap='『正忍記』（国立国会図書館）', at=2, rot=2)]),
 dict(key='black', title='黒装束と覆面', chapter_title='黒装束と覆面は、どこから来たのか', scene=[
   tel('黒装束と覆面は\nどこから？', 960, 440, 120, at=0, until=1, rot=-2),
   tel('もともと、特徴的な[[黒装束]]では\nなかった（国立国会図書館の解説）', 960, 440, 78, at=1, until=2, plate='blue', rot=1.5),
   card('img', [360, 190, 1560, 640], img='colors', at=2, until=4, rot=-1),
   tel('『正忍記』には、茶・柿・[[黒]]・紺', 960, 730, 66, at=2, until=3, plate='yellow', rot=1),
   tel('黒も、服装の選択肢のひとつ', 960, 730, 66, at=3, until=4, plate='green', rot=-1),
   tel('問題は\n[[「決まった姿」]]として描く表現', 960, 440, 92, at=4, until=5, plate='red', rot=-1.5),
   card('img', [90, 180, 740, 800], img='goemon', cap='歌舞伎の絵（豊国）', at=5, rot=-2),
   rows([dict(at=5, tag='広まり', text='歌舞伎・浄瑠璃など、演劇から', col='orange'),
         dict(at=6, tag='時期', text='18世紀の中ごろに発生・定着（吉丸雄哉さん）', col='blue'),
         dict(at=7, tag='理由', text='演劇では、「忍者です」と文字で説明できない', col='purple'),
         dict(at=8, tag='工夫', text='見ただけで分かる黒装束が、演出上の工夫に', col='green')], x0=790, x1=1850, y0=210, size=42, gap=18)]),
 dict(key='shuriken', title='手裏剣', chapter_title='手裏剣は、使われていたのか', scene=[
   tel('手裏剣は、\n[[使われていた]]？', 960, 440, 120, at=0, until=1, rot=-2),
   rows([dict(at=1, tag='実在', text='手裏剣を打つ技は、武芸の一種として伝わった', col='green', until=5),
         dict(at=2, tag='忍術書', text='見つかっている忍術書に、手裏剣の記述はない（国立国会図書館の解説）', col='red', until=5),
         dict(at=3, tag='解説', text='通常の忍者の道具とは、考えられていなかった', col='blue', until=5),
         dict(at=4, tag='注意', text='使った可能性は、否定できない', col='purple', until=5)], x0=70, x1=1130, y0=190, size=40, gap=16),
   rows([dict(at=5, tag='演劇', text='江戸時代の演劇・文芸には、手裏剣を使う忍者が登場', col='orange'),
         dict(at=6, tag='形', text='棒の形。いま思い浮かべる平らな形とは違う', col='blue'),
         dict(at=7, tag='広まり', text='娯楽の世界から定着していったと考えられる', col='green')], x0=70, x1=1130, y0=190, size=42, gap=18),
   card('img', [1170, 200, 1860, 760], img='bar', cap='『北斎漫画』の棒状の手裏剣', at=5, rot=2)]),
 dict(key='now', title='いまのイメージ', chapter_title='いまのイメージ', scene=[
   tel('江戸の演劇で広まった姿は\n形を変えながら伝わった', 960, 440, 92, at=0, until=1, rot=-2),
   tel('「忍者」の呼び名が定着した時期と\n姿が作られた時期は、[[別]]', 960, 440, 84, at=1, until=2, plate='blue', rot=1.5),
   tel('長い時間をかけて\n[[重ねられた像]]', 960, 440, 112, at=2, plate='yellow', rot=-1.5)]),
 dict(key='end', title='分かること、決められないこと', chapter_title='結論：分かること、決められないこと', scene=[
   rows([dict(at=1, tag='分かる', text='黒装束・覆面の「決まった姿」は、江戸時代の演劇から広まったと説明されている', col='green'),
         dict(at=2, tag='分かる', text='『正忍記』は茶・柿・黒・紺を挙げ、目立たない服装がふさわしいとする', col='green'),
         dict(at=3, tag='分かる', text='見つかっている忍術書に手裏剣の記述はなく、使った記録も見当たらない', col='green'),
         dict(at=4, tag='不明', text='個々の忍びが何を着て、何を使ったかは、決められない', col='red')], x0=110, x1=1810, y0=170, size=46, gap=18),
   tel('分けて見るのが、[[歴史を読む第一歩]]', 960, 800, 64, at=5, plate='yellow', rot=-1)])
 ],
 desc=dict(title_main='忍者は、黒装束で手裏剣を投げていたのか？ 国立国会図書館の解説で確かめる', title_no=1, titles=['忍者は、黒装束で手裏剣を投げていたのか？ 国立国会図書館の解説で確かめる'], intro='', points=[], refs=[], credit_lines=[], notes=[], tags='忍者', checks=[]),
 thumb=dict(bg='assets/ninja/thumb_art.png', lines=[['忍者', 150, 'white']], sub='国立国会図書館の解説で確かめる'))

finalize(spec, {})
