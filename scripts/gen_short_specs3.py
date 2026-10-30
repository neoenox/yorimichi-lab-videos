"""Short用の spec その3：venus・oceanblue。台本は長尺の 09_script_v2.md の文言に合わせる。"""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]


def J(n, o):
    (R / 'data' / f'short_{n}.json').write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding='utf8')


J('venus', dict(
    title='金星では、1日が1年より長い？', long_id='rj1bDRBWHsY',
    long_title='金星では、1日が1年より長い？ NASAの表で確かめる',
    pron='data/venus_pronunciations.json', art='assets/venus/art_intro.png',
    hook='「金星では、一日が一年より長い」と聞いたことはありませんか。NASAの表の数字で確かめます。',
    notes='■ 動画で確かめたこと\n・NASAの表では、金星の自転周期（星を基準）は5,832.6時間で約243日、公転周期は224.701日です。自転一回のほうが長くなります。\n・同じ表の「Length of day」（太陽が正午の位置に戻るまでの平均の時間）は2,802.0時間＝116.75日で、公転周期より短くなります。\n・自転が公転と反対向きなので、太陽が戻るのが早くなります（日数への換算と検算は自作の計算）。',
    scenes=[
        dict(text='金星では、一日が、一年より長い。そう聞いたことはありませんか。', big='金星：一日 ＞ 一年？', art='assets/venus/art_intro.png'),
        dict(text='NASAの表では、金星が自転で一回転する時間は、約二百四十三日です。', big='自転一回：約243日', src='NASA', art='assets/venus/art_nums.png', col='white'),
        dict(text='公転で、太陽のまわりを一周する時間は、二百二十四・七日です。', big='公転一周：224.7日', src='NASA', art='assets/venus/art_sun.png'),
        dict(text='つまり、自転一回のほうが、長いのです。ただし、太陽が空の同じ位置に戻る周期は、百十六・七五日です。', big='太陽が戻る周期：116.75日', sub='自転が公転と反対向きだから', art='assets/venus/art_why.png', col='white'),
        dict(text='一日の意味が違えば、答えも変わります。', big='一日の意味で、答えが変わる', art='assets/venus/art_end.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/venus/art_end.png')]))

J('oceanblue', dict(
    title='海が青いのは、空が映っているから？', long_id='31mlleqtpsM',
    long_title='海が青いのは、空が映っているから？ NOAAの解説で確かめる',
    pron='data/oceanblue_pronunciations.json', art='assets/oceanblue/art_intro.png',
    hook='「海が青いのは、空が映っているから」と思っていませんか。NOAAとウッズホール海洋研究所の解説で確かめます。',
    notes='■ 動画で確かめたこと\n・空は水面では映りますが、水面の下に潜っても青は残ります（WHOI）。\n・海が青い主な理由は、水が光の赤い側の色を吸収し、青い側の色が残るからです（NOAA）。\n・赤やオレンジは数メートルでほとんど消え、青と紫が最も深くまで届きます（WHOI）。\n・吸収と散乱が色にどのくらい影響するかの割合は、この動画の資料だけでは分かりません。',
    scenes=[
        dict(text='海が青いのは、空が青くて、その空が、水面に映っているから。そう思っていませんか。', big='海が青いのは、空が映るから？', art='assets/oceanblue/art_intro.png'),
        dict(text='空が映るのは、本当です。でも、水面の下に潜っても、青い色は、残ります。', big='水の下でも、青は残る', src='ウッズホール海洋研究所', art='assets/oceanblue/art_sky.png', col='white'),
        dict(text='NOAAによると、海が青いのは、水が、光の赤い側の色を、吸収するからです。', big='水が、赤い側の色を吸収', src='NOAA', art='assets/oceanblue/art_light.png'),
        dict(text='赤やオレンジは、数メートルでほとんど消え、青と紫が、最も深くまで届きます。', big='青い光が、最後まで残る', src='ウッズホール海洋研究所', art='assets/oceanblue/art_colors.png', col='white'),
        dict(text='海は、空を映すだけの、鏡ではありません。水が、光の色を選んで吸収するのです。', big='海は、空を映すだけの鏡ではない', art='assets/oceanblue/art_end.png'),
        dict(text='くわしくは、長い動画で、確かめています。', end=True, art='assets/oceanblue/art_end.png')]))
print('written')
