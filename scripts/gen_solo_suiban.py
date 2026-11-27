"""単独Short(江戸の暮らし／インフラ)：玉川上水は誰が守った？(solo_suiban)。根拠は東京都水道局「玉川上水の歴史」(2026年11月16日に原文を確認 https://www.waterworks.metro.tokyo.lg.jp/kouhou/pr/tamagawa/rekishishiritai/rekishi )。nolong, nolink。背景はFreeVideoのAI映像(イメージ)、図は自作。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solo_spec import build, T, fv_prompts
W = '東京都水道局「玉川上水の歴史」'
pron = {'玉川上水': 'タマガワジョウスイ', '水番屋': 'ミズバンヤ', '水番人': 'ミズバンニン',
        '持場村': 'モチバムラ', '上水記': 'ジョウスイキ', '入札': 'ニュウサツ', '普請': 'フシン'}
scenes = [
    dict(text='玉川上水は、誰が掃除していた？ 答えは、村人や水番人、工事を請け負う町人です。役割を分担して守っていました。',
         big='守ったのは、村々', sub='役割を分担して守った', src=W,
         viz=T(2.6, [('問い', '誰が掃除した？'), ('答え', '村人・水番人・町人'), ('分担', '役割を分けて守る')])),
    dict(text='上水沿いには、水番屋が置かれました。水番人は、水量を見て、ゴミを取り除きました。',
         big='水番屋と、水番人', sub='水量の確認と、ゴミ除け', src=W,
         viz=T(2.8, [('施設', '水番屋'), ('人', '水番人'), ('仕事', '水量・ゴミ除け')])),
    dict(text='村々は「持場村」と呼ばれ、草刈りや堀の掃除を担当。工事は、町人が入札し、落札した人が請け負いました。',
         big='持場村が、草刈り', sub='工事は入札→落札者が請負', src=W,
         viz=T(2.8, [('呼び名', '持場村'), ('仕事', '草刈り・堀掃除'), ('工事', '入札→落札者が請負')])),
    dict(text='こうした管理体制は、1791年の「上水記」全10巻にまとめられています。2026年11月16日時点の情報です。',
         big='上水記に、記録', sub='1791年、全10巻', src=W,
         viz=T(2.8, [('1791年', '上水記 全10巻'), ('内容', '管理体制・絵図'), ('時点', '2026年11月16日')])),
]
bg = ['水路のほとりに建つ、板張りの小さな小屋(人物なし・文字なし)',
      '浅い水路の中に置かれた木の枠と、水面に浮かぶ落ち葉(人物なし・手なし・文字なし)',
      '土の土手に生えた草と、水をたたえた堀(人物なし・文字なし)',
      '無地の木箱に納められた、紐で結ばれた巻物(人物なし・手なし・文字なし)']
notes = ('■ 2026年11月16日に、東京都水道局「玉川上水の歴史」(https://www.waterworks.metro.tokyo.lg.jp/kouhou/pr/tamagawa/rekishishiritai/rekishi )を読んで作った整理です。2026年11月16日時点の情報です。\n'
         '・使った事実(同)：玉川上水沿いには「水番屋」(水番所)が置かれ、水番人と呼ばれる町人(農民)が水の量の確認や、芥留(ゴミを留めるスクリーン)の清掃などを行った。沿線の村々はそれぞれ持ち場を割り当てられ「持場村」と呼ばれ、注意書きの高札の管理、土手の草刈り、堀の掃除、役人の通行の補助などを担った。普請(工事)や修復は、工事内容を記した触書を見た町人が入札し、落札した町人が請け負った。管理の内容は、寛政3(1791)年に普請奉行 石野広通が作成した『上水記』(全10巻)にまとめられている。\n'
         '・言い過ぎを避けた点：水番人は「町人(農民)」と資料にあるが、動画では「水番人」とだけ言い、身分の区別は持ち込んでいない。入札は「工事は入札で請け負う人を決めました」と、対象を普請・修復に限って述べた。\n'
         '・レビューで直した点(ChatGPT、2026年11月16日。裏取りして採用)：管理主体を村々だけに限定せず「村人や水番人、工事を請け負う町人たち」と分担を示した、「ゴミを留める網」→「ゴミを取り除きました」(資料の芥留は「ゴミを留めるスクリーン」で、網という構造ではない)、「工事は入札で請け負う人を決めました」→「工事や修理は、町人が入札し、落札した人が請け負いました」、「記録されています」→「まとめられています」。\n'
         '・Geminiのレビューは、この日は利用上限の画面が出て実施できなかった(ChatGPTのみ)。\n'
         '・動画では使っていないこと：分水33か所(1791年頃)、野火止用水、青山・三田・千川の3上水、通船、桜や松の伐採、玉川兄弟の子孫による管理、普請奉行 石野広通の名前。\n'
         '・未確認：『上水記』原文、水番屋の具体的な数と場所。\n'
         '・背景の映像はAI生成で、実際の玉川上水の映像ではない(イメージです)。\n')
if __name__ == '__main__':
    build('suiban', '玉川上水は、誰が掃除していた？ 水番人と持場村', '上水を守った人たち', '村人・水番人・町人が分担して守った', pron, scenes, bg, notes,
          bg_note='・動画内の図(年表・比較)は自作です。背景の映像は FreeVideo(MiniMax H3)によるAI生成で、イメージです。実際の玉川上水の映像ではありません。\n',
          credit='・背景映像：FreeVideo(MiniMax H3)によるAI生成映像。イメージです。実際の玉川上水の映像ではありません\n・図・表：自作',
          end_q='皆さんの町の用水路や川は、誰が掃除しているか、知っていますか？',
          tags=['玉川上水', '水番', '持場村', '江戸時代', '上水', '東京都水道局', '歴史', '雑学', 'Shorts'])
    fv_prompts('suiban', [
        'A small simple wooden plank hut standing beside a water channel in the countryside, plain walls, no signboard, no text, no people, soft morning light, the camera slowly gliding sideways.',
        'A simple wooden grate made of vertical slats set across a narrow earth water channel, leaves and twigs caught against the slats, clear water flowing through, stones and grass on both banks, no people, no hands, no text, the camera slowly pushing in.',
        'A grassy earthen embankment beside a water channel filled with calm water, tall grass moving in a light breeze, no people, no text, the camera slowly drifting forward.',
        'Several rolled paper scrolls tied with cord, laid in a plain wooden box, soft warm light, no writing visible, no text, no people, no hands, the camera slowly pushing in.'],
        allow_buildings=True)
