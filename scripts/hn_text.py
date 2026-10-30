"""Display text for subtitles: spoken script uses kanji numerals (reads reliably in VOICEVOX); on screen, quantities become Arabic numerals."""
import re
D={'〇':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
NUM='〇一二三四五六七八九十百千'
def k2i(s):
    """kanji numeral below 10000 -> int (十百千 positional)"""
    total=0;cur=0
    for ch in s:
        if ch in D:cur=cur*10+D[ch] if False else D[ch]
        elif ch=='十':total+=(cur or 1)*10;cur=0
        elif ch=='百':total+=(cur or 1)*100;cur=0
        elif ch=='千':total+=(cur or 1)*1000;cur=0
    return total+cur
def big(s):
    """e.g. 一万三千 / 二万 / 千五百八十二 -> text"""
    if len(s)>1 and all(c in D for c in s):return ''.join(str(D[c]) for c in s)   # positional digits (年号: 一五六九 -> 1569)
    if '万' in s:
        a,b=s.split('万',1);n=(k2i(a) if a else 1)*10000+(k2i(b) if b else 0)
    else:n=k2i(s)
    if n>=10000 and n%10000==0:return f'{n//10000}万'
    if n>10000 and n%1000==0:return f'{n//10000}万{(n%10000)//1000}千'
    return str(n)
COUNTERS='年月日人時間分時歳メートルキロメートルキロ半'
# 数量・回数・順序として数字にする助数詞（ここに挙げた語が続くときだけ算用数字にする）
QTY=('つ目','つ','度目','度','騎','か所','箇所','名','個','本','枚','台','匹','頭','杯','軒','階','件','点','割','石','里','艘','隻','発','束','袋','箱','組','対','校','着','歩','羽','面','曲','折','品','周','未満','以上','以下','程度','余','弱','強')
# 助数詞が漢字の名詞（島・城など）。十百千を含む長い数に限って数量とみなす（三島・千葉は触らない）
NOUN=('島','城','戸','村','町','駅','橋','寺','社','館','家')
# 数字にすると不自然な慣用句・複合語（丸ごと保護して、あとで戻す）
KEEP=('有馬一件','一騎打ち','一騎当千','一度に','一目','一息','一礼','一見','一通り','一括','一斉','一昨年','一昨日','一問一答','一石二鳥',
      '一長一短','一生懸命','一期一会','一心不乱','一触即発','一網打尽','一喜一憂','一進一退','一溜まり','一か八か','一帯','一掃',
      '一方','一角','一緒','一般','一部','一体','一員','一国','一門','一家','一層','一変','一転','一新','一任','一存','一考','一読',
      '三国','四国','九州','三河','一宮','一山','七本槍','もう一度','二時半','当時の一時','一団','二、三百騎','五、六万騎','一人前','一仕事','一休み','三日天下',
      '明け六つ','暮れ六つ','明け五つ','暮れ五つ','明け四つ','暮れ四つ','明け七つ','暮れ七つ','明け八つ','暮れ八つ','明け九つ','暮れ九つ')
def display(t):
    keep={}
    for i,g in enumerate([g for g in KEEP if g in t]):
        k=chr(0xe100+i);keep[k]=g;t=t.replace(g,k)
    t=t.replace('不十分','不').replace('十分に','に').replace('十分な','な')  # 不十分・十分に・十分な は『10分』にしない
    t=t.replace('二十、三十人','20〜30人').replace('百五十、六十人','150〜160人').replace('二十人から三十人','20〜30人').replace('百五十人から百六十人','150〜160人')
    t=t.replace('二、三年','2〜3年')
    # decimal: 十七点五キロ / 一点五キロ
    t=re.sub(r'([%s]+)・([〇一二三四五六七八九]+)'%NUM,lambda m:f'{big(m.group(1))}.{"".join(str(D[c]) for c in m.group(2))}',t)  # 一・四倍 -> 1.4倍
    t=re.sub(r'([%s]+)点([〇一二三四五六七八九]+)'%NUM,lambda m:f'{big(m.group(1))}.{"".join(str(D[c]) for c in m.group(2))}',t)
    # maximal numeral run -> arabic when it is a quantity (followed by a counter, or containing 万)
    def conv(m):
        s=m.group(0);nxt=t_[m.end():m.end()+4]
        if m.start()>0 and (t_[m.start()-1]=='数' or t_[m.start()-1].isdigit()):return s  # 数百人・2万5千 は触らない   # 数百人・数十人 は『数100人』にしない
        if s=='万':return s   # bare 万 inside a word (万能, 数万人) is not a quantity
        if '万' in s or re.match(r'(年|月|日|人|歳|分|メートル|キロ|時間|時|度|倍|巻|世紀|兆|億|パーセ|秒|回|ポイント)',nxt):return big(s)
        # 百・千で終わる2文字以上の数は、数量とみなす（三千にも満たない -> 3000）。
        # ただし「八千代市」「三千院」のような固有名詞を壊さないよう、うしろが漢字のときは触らない。
        if any(nxt.startswith(q) for q in QTY):return big(s)
        if len(s)>=2 and s[-1] in '千百' and not ('\u4e00'<=t_[m.end():m.end()+1]<='\u9fff'):
            return big(s)
        if len(s)>=2 and any(c in s for c in '十百千') and any(nxt.startswith(q) for q in NOUN):
            return big(s)
        return s
    t_=t
    t=re.sub('[%s万]+'%NUM,conv,t)
    t=t.replace('','十分')
    t=re.sub(r'(\d+)分の([一二三四五六七八九])',lambda m:f'{m.group(1)}分の{D[m.group(2)]}',t)  # 5分の一 -> 5分の1
    for k,v in keep.items():t=t.replace(k,v)
    return t
if __name__=='__main__':
    import json,sys
    for x in ['天正十年六月二日の未明','千五百八十二年のことです。','少ない説で二十、三十人、多い説で百五十、六十人。','光秀の兵は、約一万三千ともいわれます。','約十七点五キロメートルでした。','五キロなら約三時間半、四キロなら約四時間二十分、三キロなら約五時間五十分かかります。','一つは、怨恨説。二つ目は、野望説。四国と三職推任と三男。','約百十メートルです。約二百三十メートル。約百二十メートル四方。','二万、三万とする説もあります。','千五百九十一年から翌年にかけて','十一日後、六月十三日','土佐一国と阿波の南の二郡以外を','約一点五キロメートル','約八百メートルの距離です','相手は、三千にも満たない織田信長の軍でした。','八千代市と三千院、百舌鳥。']:print(display(x))
