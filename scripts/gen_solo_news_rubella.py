"""単独Short(ニュース)：風疹ウイルスの主要な侵入受容体Nectin-4(solo_rubella)。根拠は横浜市立大学のプレスリリース(2026年11月9日発表、2026年11月12日に原文を確認)。論文は2026年11月5日にNatureに公表。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
from solo_spec import build, T, fv_prompts
W = '横浜市立大学ほか(2026年11月9日発表)'
pron = {'風疹': 'フウシン', '麻疹': 'ハシカ', '受容体': 'ジュヨウタイ', '呼吸上皮': 'コキュウジョウヒ', '基底側': 'キテイソク', '気道': 'キドウ', '胎盤': 'タイバン', '母子感染': 'ボシカンセン',
        '国立健康危機管理研究機構': 'コクリツケンコウキキカンリケンキュウキコウ', '英国': 'エイコク', '科学誌': 'カガクシ', 'ネイチャー': 'ネイチャー', '感染しました': 'カンセンシマシタ', '感染せず': 'カンセンセズ', '感染': 'カンセン', '研究グループ': 'ケンキュウグルウプ', '開発': 'カイハツ'}
scenes = [
    dict(text='風疹と麻疹は、別のウイルスなのに、同じ入口を使う？ 研究グループが、2026年11月5日に、英国の科学誌ネイチャーに発表しました。',
         big='風疹と麻疹は、同じ入口？', sub='2026年11月5日にNatureで発表', src=W,
         viz=T(2.6, [('Nature掲載', '2026年11月5日'), ('大学の発表', '2026年11月9日'), ('時点', '2026年11月12日')])),
    dict(text='その入口は、ネクチンフォーという分子です。風疹ウイルスは、これを持たない細胞には感染せず、持たせると感染しました。',
         big='入口は、Nectin-4', sub='持たない細胞は感染せず、持たせると感染', src=W,
         viz=dict(type='compare', l_label='Nectin-4なし', l_val='感染せず', r_label='Nectin-4あり', r_val='感染した')),
    dict(text='呼吸の細胞では、基底側から入ります。胎盤の細胞にも多く、母子感染に関わる可能性が示されました。',
         big='呼吸の細胞と、胎盤の細胞', sub='胎盤は培養した細胞での結果', src=W,
         viz=T(2.8, [('呼吸の細胞', '基底側から入る'), ('胎盤の細胞', 'Nectin-4が豊富'), ('注意', '培養細胞での結果')])),
    dict(text='麻疹ウイルスも、同じネクチンフォーを使うことが知られています。治療薬や予防法は、まだ将来への期待です。2026年11月12日時点の情報です。',
         big='麻疹も同じNectin-4を使う', sub='薬や予防法は、まだ将来への期待', src=W,
         viz=dict(type='compare', l_label='風疹ウイルス', l_val='Nectin-4', r_label='麻疹ウイルス', r_val='Nectin-4')),
]
bg = ['暗い青の液体の中を、半透明の丸い粒がゆっくり漂う顕微鏡のような映像(人物なし・文字なし)', '石畳のように並んだ細胞の層に、小さな光の扉がいくつも並ぶ模式的な映像(人物なし・文字なし)',
      'ピンク色の半透明の組織のひだを、粒がゆっくり流れる模式的な映像(人物なし・文字なし)', '色の違う2つの球が、同じ小さな光の門へゆっくり近づく模式的な映像(人物なし・文字なし)']
notes = ('■ 2026年11月12日に、横浜市立大学のプレスリリース「風疹ウイルスの主要侵入受容体Nectin-4を同定」(2026年11月9日発表。https://digitalpr.jp/r/147664 に掲載された原文)を読んで作った整理です。2026年11月12日時点の情報です。\n'
         '・発表者：国立健康危機管理研究機構(JIHS)、国立医薬品食品衛生研究所、東京科学大学、横浜市立大学、東北大学、大阪大学、群馬大学などの研究グループ。論文は2026年11月5日、英国科学誌「Nature」に公表(題名：Nectin-4 mediates rubella virus entry in airway and placental cells)。\n'
         '・主な内容(同)：風疹ウイルスが細胞に侵入する際の主要な受容体として、細胞間接着因子Nectin-4を同定した。Nectin-4を持たないRaji細胞は風疹ウイルスに感染せず、Nectin-4を強制発現させると感染が成立した。培養した呼吸上皮細胞では、基底面から感染し、子孫ウイルスは頂端面から放出された。胎盤の合胞体性栄養膜細胞にはNectin-4が豊富に発現し、母体から胎児への感染の初期段階に関与する可能性が示された。Nectin-4は麻疹ウイルスの受容体としても知られている。\n'
         '・言い過ぎを避けた点：「感染の仕組みがすべて分かった」「治療薬ができた」とは言っていない。原文は、予防法や治療法の開発につながることが「将来的に期待される」としている。胎盤は培養した細胞(オルガノイド)での結果で、人での母子感染の経路を確定したものではない。\n'
         '・動画では使っていないこと：先天性風疹症候群の患者数、ワクチンの効果や接種の推奨、麻疹の流行状況。\n'
         '・未確認：Nature掲載論文そのもの(原文はプレスリリースのみ確認)、論文の掲載ページのURL。\n'
         '・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際のウイルスや細胞の映像ではありません。\n')
if __name__ == '__main__':
    build('rubella', '【2026年11月9日】風疹と麻疹は、同じ細胞の入口を使う？ Nature論文', '風疹と麻疹、同じ入口？', '同じNectin-4を使う', pron, scenes, bg, notes,
          end_q='皆さんは、風疹のワクチンを、受けた記憶がありますか？')
    fv_prompts('rubella', [
        'Translucent round particles drifting slowly in dark blue liquid like a microscope view, soft glow, the camera slowly pushing in.',
        'A layer of rounded cells arranged like cobblestones with small glowing doorways on the surface, abstract and schematic, the camera slowly gliding sideways.',
        'Soft pink translucent tissue folds with tiny particles flowing slowly along them, abstract and schematic, the camera slowly pushing in.',
        'Two spheres of different colors slowly moving toward the same small glowing gate in darkness, abstract and schematic, the camera slowly pulling back.'])
