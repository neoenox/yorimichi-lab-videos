"""単独Short(歴史・暮らし)：郵便ポストは最初黒かった？(solo_postbox)。根拠は郵政博物館「郵便ポストの移り変わり」(2026-11-18に原文を確認 https://www.postalmuseum.jp/column/transition/post_10.html )。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。
Ask Studio(2026-11-17)の実測「離脱は4〜7秒」を受け、4〜6秒目に数字(1901年)を置く構成。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solo_spec import build, T, fv_prompts
W = '郵政博物館「郵便ポストの移り変わり」'
pron = {'書状集箱': 'ショジョオアツメバコ', '宿場': 'シュクバ', '黒塗柱箱': 'クロヌリハシラバコ',
        '杉板': 'スギイタ', '鉄板': 'テッパン', '丸型': 'マルガタ', '回転式': 'カイテンシキ'}
scenes = [
    dict(text='郵便ポストは、最初から赤かった？ いいえ。最初は黒。赤くなったのは、1901年です。',
         big='最初は、黒だった', sub='赤くなったのは1901年', src=W,
         viz=T(2.6, [('最初', '黒'), ('赤くなった年', '1901年'), ('理由', '目立たせるため')])),
    dict(text='最初のポストは、1871年。木で作られ、東京に12、京都に5、大阪に8。東海道の宿場に、62か所。',
         big='1871年、東京に12', sub='木製の「書状集箱」', src=W,
         viz=T(2.8, [('年', '1871年'), ('東京・京都・大阪', '12・5・8'), ('東海道の宿場', '62か所')])),
    dict(text='1872年、黒い柱のポストが登場。杉板に鉄板を張って、黒く塗りました。高さ、123センチ。',
         big='黒ポスト、高さ123cm', sub='杉板に鉄板を張った', src=W,
         viz=T(2.8, [('年', '1872年'), ('作り', '杉板＋鉄板＋黒ペンキ'), ('高さ', '123cm')])),
    dict(text='1901年、鉄の赤い丸型ポストが登場。赤は、目立たせるため。1908年に正式に定められました。2026年11月18日時点の情報です。',
         big='1901年、赤い丸型', sub='1908年に正式制定', src=W,
         viz=T(2.8, [('1901年', '赤い丸型'), ('1908年', '正式に制定'), ('時点', '2026年11月18日')])),
]
bg = ['道の角に立つ、無地の黒い木のポスト(人物なし・文字なし)',
      '台の上に置かれた、無地の木の箱(人物なし・手なし・文字なし)',
      '無地の黒い柱のポストのクローズアップ(人物なし・文字なし)',
      '無地の赤い円筒形ポストのクローズアップ(人物なし・文字なし)']
notes = ('■ 2026年11月18日に、郵政博物館「郵便ポストの移り変わり 〜日本最初のポストから現在のポストまで〜」(https://www.postalmuseum.jp/column/transition/post_10.html )を読んで作った整理です。2026年11月18日時点の情報です。\n'
         '・使った事実(同)：1871(明治4)年に郵便制度が始まり、日本最初のポスト「書状集箱」が誕生。木製で、東京12か所・京都5か所・大阪8か所、東海道の宿場62か所に設置。1872(明治5)年、郵便の全国実施に伴い、杉板を四角い柱のように組み合わせ、かどに鉄板を張って黒いペンキを塗った「黒塗柱箱」(黒ポスト)が作られた(幅24.2cm・奥行24.2cm・高さ123cm)。1901(明治34)年に火事に強い鉄製の赤色丸型ポストが考案され(俵谷式・中村式を試験設置)、赤色に塗ったのはポストの位置をわかりやすくするため、かどを丸くして通行のじゃまにならないようにした。1908(明治41)年10月に鉄製赤色ポストが正式に定められた(回転式)。\n'
         '・言い過ぎを避けた点：「最初は黒」は、1871年の最初のポスト(木製・書状集箱)の色を断定しない形にし、1872年の黒塗柱箱を「黒かった」根拠にした。1901年の赤は「試験的に設置」されたもので、全国に広がったのは1908年の正式制定から。\n'
         '・動画では使っていないこと：書状集箱に付けられた太政官布告・各地時間賃銭表、俵谷高七・中村幸治の名前、1912年の庇付きへの変更、戦時中のコンクリート製・陶器製ポスト、1949年以降の規格。\n'
         '・未確認：1871年の書状集箱の塗装色、黒ポストの全国の設置数。\n'
         '・背景の映像はAI生成で、実物の写真ではない(イメージです)。\n')
if __name__ == '__main__':
    build('postbox', '郵便ポストは、最初から赤かった？ 黒から赤へ', '郵便ポストの色', '最初は黒。赤くなったのは1901年', pron, scenes, bg, notes,
          bg_note='・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実物のポストの写真ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実物のポストの写真ではありません\n・図・表：自作',
          end_q='皆さんの近所のポストは、何色ですか？',
          tags=['郵便ポスト', '郵政博物館', '郵便', '明治', '赤いポスト', '歴史', '雑学', 'インフラ', 'Shorts'])
    fv_prompts('postbox', [
        'Extreme close-up of glossy black painted metal with a gentle vertical curve, soft evening light, plain unmarked surface filling the frame, no text, no people, the camera slowly gliding sideways.',
        'A plain unmarked wooden box sitting on a simple wooden stand, weathered wood, neutral background, no text, no letters, no people, no hands, the camera slowly pushing in.',
        'A glossy black painted metal surface with a bright soft reflection sweeping across it, subtle texture, filling the frame, no text, no people, the camera slowly tilting up.',
        'Extreme close-up of glossy bright red painted metal with a gentle curve and a rounded edge at the top, soft daylight, plain unmarked surface, no text, no people, the camera slowly pushing in.'],
        allow_buildings=False)
