"""Measure a script and preview subtitle conversions: python scripts/oke_measure.py <script.md>"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hn_text import display
p = Path(sys.argv[1])
t = p.read_text(encoding='utf8')
chs = re.split(r'\n## ', t)[1:]
tot = 0
for c in chs:
    head = c.split('\n')[0]
    lines = [re.sub(r'〔[^〕]*〕', '', re.sub(r'^\d+\. ', '', l)).strip() for l in c.split('\n') if re.match(r'^\d+\. ', l)]
    txt = ''.join(lines)
    n = len([x for x in txt.split('。') if x.strip()])
    tot += len(txt)
    over = [l for l in lines if len(l) > 50]
    print(f'{head[:28]:30s} sent={n:3d} chars={len(txt):4d}' + (f'  OVER50={over}' if over else ''))
print(f'TOTAL chars={tot}  est {tot/5.0:.0f}s = {tot/5.0/60:.1f} min')
print('--- subtitle conversion samples ---')
for s in ['永禄三年五月十九日、尾張国の桶狭間で、合戦がありました。',
          '二万五千の大軍を率いた今川義元が、討ち取られたのです。',
          '十時ごろ、善照寺砦に入り、二千人から三千人ほどの軍勢を整えます。',
          '正午ごろ、織田軍の佐々政次と千秋四郎の三十人余りが、単独で今川軍の前衛に攻めかかりました。',
          '享年四十二歳でした。',
          '今川軍のうち、信長の本隊と直接向き合ったのは、五千人から六千人でした。',
          '小和田哲男さんは、豊明市の古戦場の南方の、標高六十四・七メートルの地点としています。',
          '小和田哲男さんは、義元の領地を九十万石から百万石と見て、二万五千としました。',
          '武田氏と今川氏の関係は悪化し、永禄十一年、甲相駿三国同盟は終わります。',
          '天文二十年に信秀が病死すると、織田家では家督をめぐる内紛が起こります。']:
    print(f'{s}\n  -> {display(s)}')
