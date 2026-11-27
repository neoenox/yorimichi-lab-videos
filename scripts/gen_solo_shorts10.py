"""単独Short 当日ニュース版（2026-11-04）：関東の大雨予報を、背景から説明する。nolong。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
IDS = json.loads((R / 'data' / 'youtube_ids.json').read_text(encoding='utf8'))
CREDIT = '・イラスト：ChatGPT(OpenAI)による生成イラスト（イメージです）\n・図・表：自作'
o = dict(
    title='関東の大雨、130ミリは多い？', pron='data/drain_pronunciations.json', art='assets/rain30/art_amount.png',
    hook='明日の朝、関東は大雨のピーク。24時間で130ミリと聞いて、多いのか少ないのか、ピンときますか。',
    notes='■ 2026年11月4日夜時点の予報にもとづく解説です。予報は変わります。最新は気象庁・お住まいの自治体の情報で確認してください。\n・日本気象協会 tenki.jp(11/4 18:12)：関東南部の24時間予想雨量(4日18時〜5日18時)は130ミリ、多い所で1時間50ミリ。ピークは5日未明から朝。\n・同記事：11月の平年降水量は、東京都心や千葉市で100ミリ未満。「1日で11月ひと月分に匹敵」。\n・気象庁の雨の強さの表：1時間50ミリ以上80ミリ未満は「非常に激しい雨」、傘は全く役に立たなくなる。\n・公的機関・報道の要約による内容で、原典の照合は軽く行いました。\n',
    answer='1日でひと月分に匹敵', credit=CREDIT, nolong=True, nolink=True,
    long_id=IDS['14_rain_probability']['video_id'], long_title='14_rain_probability',
    scenes=[
        dict(text='明日の朝、関東は、大雨のピークを迎えます。24時間で、130ミリと聞いて、多いのか、ピンときますか。', big='24時間で130ミリ、多い？', art='assets/rain30/art_amount.png'),
        dict(text='日本気象協会によると、関東南部の、4日夕方からの24時間の予想雨量は、130ミリ。ピークは、5日の未明から朝です。', big='関東南部：24時間130ミリ予想', src='日本気象協会 tenki.jp（11/4 18:12）', art='assets/rain30/art_intro.png', col='white'),
        dict(text='11月の、ひと月の平年の雨量は、東京都心などで、100ミリ未満。つまり、一日で、ひと月分に、匹敵します。', big='1日で、11月ひと月分', src='日本気象協会 tenki.jp', art='assets/rain30/art_def.png'),
        dict(text='多い所では、一時間に50ミリ。気象庁では、非常に激しい雨で、傘は全く役に立たなくなる、とされます。', big='1時間50ミリ＝傘は役に立たない', src='気象庁（雨の強さと降り方）', art='assets/rain30/art_amount.png', col='white'),
        dict(text='', end=True)])
(R / 'data' / 'short_solo_news_kanto_rain.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')
print('ok')
