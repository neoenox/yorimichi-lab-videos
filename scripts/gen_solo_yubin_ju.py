"""単独Short(歴史・明治)：明治の郵便屋さんはピストルを持っていた？(solo_yubin_ju)。根拠は郵政博物館「明治期の郵便と熊害」(2026年2月5日、2026-11-19に原文を確認 https://www.postalmuseum.jp/column/transition/postandbear.html )。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。
Ask Studio(2026-11-17)の実測「離脱は4〜7秒」を受け、4〜6秒目に数字(1873年)を置く構成。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solo_spec import build, T, fv_prompts
W = '郵政博物館「明治期の郵便と熊害」'
pron = {'逓送人': 'テイソウニン', '短銃': 'タンジュウ', '喇叭': 'ラッパ', '鐸鈴': 'タクレイ',
        '雷電山': 'ライデンヤマ', '郵便物保護銃': 'ユウビンブツホゴジュウ', '岩内': 'イワナイ',
        '猛獣': 'モウジュウ', '慰労': 'イロウ', '行嚢': 'コウノウ'}
scenes = [
    dict(text='明治の郵便屋さんは、ピストルを持っていた？ はい。1873年から、危ない地域の郵便局に、短銃が配られました。',
         big='郵便屋さんに、短銃', sub='1873年から危険地域の局へ', src=W,
         viz=T(2.6, [('1873年', '危険地域の局に短銃'), ('目的', '強盗から郵便物を守る'), ('名前', '郵便物保護銃')])),
    dict(text='最初は、強盗への備えでした。1887年からは、猛獣に襲われた時にも、撃ってよいことになりました。',
         big='1887年、猛獣にも', sub='山道は熊や猪が出た', src=W,
         viz=T(2.8, [('最初', '強盗への備え'), ('1887年', '猛獣にも発射可'), ('山道', '熊・猪・毒蛇')])),
    dict(text='さらに、ラッパや大きな鈴も配られました。鳴らしながら山道を進み、獣を遠ざけたのです。',
         big='ラッパと鈴も', sub='鳴らして獣を遠ざける', src=W,
         viz=T(2.8, [('1891年', 'ラッパを支給'), ('1895年', '猛獣よけと明記'), ('鈴', '今の熊鈴の一種')])),
    dict(text='1897年、北海道で19歳の逓送人が、熊に襲われます。死んだふりで助かり、それでも郵便を届けようと歩き続けました。2026年11月19日時点の情報です。',
         big='熊に襲われても', sub='1897年、北海道・雷電山', src=W,
         viz=T(2.8, [('1897年', '北海道・雷電山'), ('逓送人', '19歳'), ('その後', '慰労手当20円')])),
]
bg = ['明治の山道を進む、郵便かばんの映像(人物なし・文字なし)',
      '霧の深い山林と、細い山道(人物なし・文字なし)',
      '木の机に置かれた、真ちゅうのラッパと大きな鈴(人物なし・手なし・文字なし)',
      '夜明けの北海道の山と、竹やぶ(人物なし・文字なし)']
notes = ('■ 2026年11月19日に、郵政博物館「明治期の郵便と熊害」(2026年2月5日公開、学芸員 倉地伸枝。https://www.postalmuseum.jp/column/transition/postandbear.html )を読んで作った整理です。2026年11月19日時点の情報です。\n'
         '・使った事実(同)：近代郵便は1871(明治4)年に創業。逓送人や集配人は、整備の不十分な山林原野を通ることが多く、熊・猪・狂犬・毒蛇などの危険があった。短銃は1873(明治6)年から、賊徒対策として危険地域の各局に支給された。1887(明治20)年に使用条件が緩和され、「強盗ノ脅迫」のほか「猛獣ノ危難ニ遭遇」した場合にも発射できるようになり、「郵便物保護銃」という名称もこの時に定められた。喇叭は1891(明治24)年から本省交付品に加わり、1895(明治28)年の公達で「猛獣予防」と「舟子召呼」に使うことが明文化された。鐸鈴(大ぶりのハンドベル)も同じ公達で使用が認められ、今日の熊鈴の一種といえる。1897(明治30)年11月1日、北海道の岩内郵便電信局の逓送人 吉村市太郎(19才)が雷電山で熊に襲われ、死んだふりをして一命をとりとめ、負傷を顧みず目的地へ進んだが、傷の痛みで完遂できず帰局・入院。札幌監督局長から慰労手当20円が給与された。\n'
         '・言い過ぎを避けた点：短銃は「危険地域の各局に支給」で、郵便屋さん全員が持っていたわけではない(画面とナレーションで「危ない地域の郵便局に」と限定)。「届けた」とは言わず「届けようと歩き続けた」とした(資料では完遂できずに帰局)。熊の被害の描写は控えめにした。\n'
         '・動画では使っていないこと：同年9月22日の別の逓送人の熊被害、合羽と火道具で追い払った話、舟子召呼、短銃の規則の公達番号、出典の『交通』誌。\n'
         '・未確認：原典の『駅逓局類聚摘要録』『交通』第171号、短銃の実際の支給数。\n'
         '・背景の映像はAI生成で、実際の明治の郵便の映像ではない(イメージです)。\n')
if __name__ == '__main__':
    build('yubin_ju', '明治の郵便屋さんは、ピストルを持っていた？ 郵便物保護銃と熊', '明治の郵便と熊', '1873年から、危険地域の局に短銃', pron, scenes, bg, notes,
          bg_note='・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の明治の郵便の映像ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の明治の郵便の映像ではありません\n・図・表：自作',
          end_q='山道を歩くとき、熊鈴を付けたことはありますか？',
          tags=['郵便', '明治', '郵政博物館', '郵便物保護銃', '熊', '熊鈴', '歴史', '雑学', 'Shorts'])
    fv_prompts('yubin_ju', [
        'A plain worn leather satchel resting on a mossy stone beside a narrow mountain path in an old Japanese forest, soft morning light, no people, no text, the camera slowly pushing in.',
        'A narrow dirt path winding through a deep misty mountain forest, tall cedar trees, quiet atmosphere, no people, no text, the camera slowly moving forward along the path.',
        'A plain brass bugle and a large plain bronze hand bell lying on an old wooden table, warm window light, smooth unmarked metal surfaces, no people, no hands, no text, the camera slowly gliding sideways.',
        'A dense bamboo thicket at the edge of a mountain pass at dawn, mist drifting between stalks, no people, no animals, no text, the camera slowly tilting up.'],
        allow_buildings=False)
