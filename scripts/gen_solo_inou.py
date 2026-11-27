"""単独Short(歴史・江戸)：伊能忠敬は歩幅だけで日本地図を作った？(solo_inou)。根拠は国土地理院「“伊能図”近代地図の原点」(PDF)と「測量・地図ミニ人物伝：伊能忠敬」(2026-11-19に原文を確認 https://www.gsi.go.jp/common/000236440.pdf 、https://www.gsi.go.jp/KIDS/MEMORI/inou.htm )。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。
Ask Studio(2026-11-17)の実測「離脱は4〜7秒」を受け、4〜6秒目に数字(17年)を置く構成。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solo_spec import build, T, fv_prompts
W = '国土地理院「“伊能図”近代地図の原点」'
pron = {'伊能忠敬': 'イノウタダタカ', '間縄': 'ケンナワ', '鉄鎖': 'テッサ', '杖先方位盤': 'ツエサキホウイバン',
        '中象限儀': 'チュウショウゲンギ', '緯度': 'イド', '緯度1度': 'イドイチド', '蝦夷地': 'エゾチ',
        '大日本沿海輿地全図': 'ダイニホンエンカイヨチゼンズ', '測量': 'ソクリョウ', '星': 'ホシ'}
scenes = [
    dict(text='伊能忠敬は、歩幅だけで、日本地図を作った？ いいえ。足掛け17年、縄と鉄の鎖、そして星で、測りました。',
         big='歩幅だけでは、ない', sub='足掛け17年／縄・鎖・星で測量', src=W,
         viz=T(2.6, [('通説', '歩幅だけで作った'), ('実際', '縄・鎖・星で測量'), ('期間', '足掛け17年')])),
    dict(text='距離は、60間、約108メートルの縄で測りました。のちに、1尺の鉄線を60本つないだ、鉄の鎖も使いました。',
         big='距離は、縄と鉄の鎖', sub='60間＝約108メートル', src=W,
         viz=T(2.8, [('間縄', '60間＝約108m'), ('鉄鎖', '1尺の鉄線×60本'), ('使い始め', '1802年')])),
    dict(text='曲がり角では、杖の先の方位盤で方角を測り、北極星などの高さから、緯度を求めました。全国規模の星の観測は、伊能隊が初めてです。',
         big='方角は方位盤／緯度は星', sub='全国規模の天測は伊能隊が初', src=W,
         viz=T(2.8, [('方角', '杖先方位盤'), ('緯度', '北極星などの高さ'), ('全国規模の天測', '伊能隊が初')])),
    dict(text='こうして、大図214枚の日本地図ができ、1821年に、幕府へ上呈されました。2026年11月19日時点の情報です。',
         big='大図214枚／1821年', sub='忠敬の没後に完成', src=W,
         viz=T(2.8, [('大図', '214枚(3万6千分の1)'), ('完成', '1821年'), ('時点', '2026年11月19日')])),
]
bg = ['畳の上に広げられた、手描きの大きな古い地図(文字なし・人物なし)',
      '麻縄を巻いた束と、鉄の輪をつないだ鎖が、木の台に置かれている映像(人物なし・手なし・文字なし)',
      '夜空に北極星が輝く、澄んだ星空(人物なし・文字なし)',
      '木の机の上に、折りたたまれた大きな地図の束(人物なし・手なし・文字なし)']
notes = ('■ 2026年11月19日に、国土地理院「“伊能図”近代地図の原点」(PDF。https://www.gsi.go.jp/common/000236440.pdf )と「測量・地図ミニ人物伝：伊能忠敬」(https://www.gsi.go.jp/KIDS/MEMORI/inou.htm )を読んで作った整理です。2026年11月19日時点の情報です。\n'
         '・使った事実(同)：伊能忠敬(1745〜1818)は、1800(寛政12)年から1816年まで、日本初の実測による全国測量を実施(足掛け17年)。測量の目的は、緯度1度の距離を測って地球の大きさを確かめることで、蝦夷地近海へのロシア船の来航で幕府も正確な地図を必要としていた。距離は間縄(60間＝約108m、1間＝約1.8mごとに目盛り)、のち1802(享和2)年から鉄鎖(内法1尺の鉄線を60本=10間つないだ、忠敬考案とされる)を使った。曲がり角の方角は杖先方位盤(忠敬が改良。測量で最も役立った器具といわれる)で測り、中象限儀で北極星をはじめとする恒星の高度を測って各観測地点の緯度を求めた(この天文測量を全国的に行ったのは伊能の測量隊が初めて)。大図(3万6千分の1)214枚・中図(21万6千分の1)8枚・小図(43万2千分の1)3枚から成る『大日本沿海輿地全図』は、忠敬の没後、1821(文政4)年に完成して幕府に上呈された。\n'
         '・言い過ぎを避けた点：「歩幅だけで作った」という通説を「いいえ」と否定するが、歩測を一切使わなかったとは言っていない(資料は、距離は間縄・鉄鎖で測ったと述べる一方、歩測そのものには触れていない)。「縄と鉄の鎖と星」は、資料が挙げる主な測量方法の言い換えで、すべての器具を網羅するわけではない。「足掛け17年」は資料の表現どおり(1800〜1816年)。\n'
         '・動画では使っていないこと：量程車・計程車(実測には使われなかった)、小象限儀(坂道の勾配)、梵天、導線法・交会法の詳細、緯度1度=28.2里、忠敬の生年(資料により1745年・1754年の表記ゆれがある)、焼失した原図、アメリカで見つかった大図。\n'
         '・未確認：原典(『大日本沿海輿地全図』、大谷亮吉『伊能忠敬』)、歩測が実際にどれほど併用されたか(静岡県立図書館の資料は「間縄と歩測の併用」と述べる)。\n'
         '・背景の映像はAI生成で、実際の伊能図や測量器具の映像ではない(イメージです)。\n')
if __name__ == '__main__':
    build('inou', '伊能忠敬は、歩幅だけで日本地図を作った？ 縄と鎖と星で測った17年', '伊能忠敬の測量', '縄・鉄の鎖・星で、足掛け17年', pron, scenes, bg, notes,
          bg_note='・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の伊能図や測量器具の映像ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の伊能図や測量器具の映像ではありません\n・図・表：自作',
          end_q='皆さんは、これまでに一番長く歩いた距離は、どのくらいですか？',
          tags=['伊能忠敬', '伊能図', '日本地図', '測量', '国土地理院', '江戸時代', '歴史', '雑学', 'Shorts'])
    fv_prompts('inou', [
        'A long unrolled scroll of aged blank paper on a tatami mat, with one thin hand-drawn ink line of a jagged coastline running its length and a single faint red line beside it, every other part of the paper left blank, absolutely no writing, no characters, no calligraphy, no letters, no labels, no numerals, no seals, no cartouches, soft window light, the camera slowly gliding along the scroll.',
        'A coiled hemp rope and a chain made of linked iron rings laid on a plain wooden platform, warm soft light, simple background, no people, no hands, no text, the camera slowly pushing in.',
        'A clear night sky full of stars with one bright star near the center above a dark ridge line, calm and quiet, no people, no text, the camera slowly tilting up.',
        'A stack of folded large paper maps on a wooden desk beside a plain brush stand, warm lamp light, only drawn lines on the paper and no writing, no people, no hands, no text, the camera slowly pushing in.'],
        allow_buildings=True)
