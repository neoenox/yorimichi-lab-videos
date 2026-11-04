"""字幕・画面の文字の読点（、）を減らす。音声は元の文のまま（読点＝息継ぎ）なので、音は変わらない。
規則：読点を残すのは、①文頭の接続語の後ろ（ところが、ただし、…）②手前の区切りが8字以上で、後ろに5字以上続くとき。
それ以外は外す。usage: from thin_commas import thin"""
import re
CONJ = ('ところが', 'ただし', 'つまり', 'また', 'そして', 'しかし', 'だから', 'そのため', 'さらに', 'ですから', 'なお', '一方', 'では', 'たとえば', 'まず', '次に', 'そこで', 'けれども', 'ですが')


def thin(t):
    if '、' not in t: return t
    out = []
    for sent in re.split(r'(?<=[。！？\n])', t):
        parts = sent.split('、')
        if len(parts) <= 1: out.append(sent); continue
        res = parts[0]
        for i in range(1, len(parts)):
            prev = res.split('、')[-1]
            rest = ''.join(parts[i:]).rstrip('。！？\n')
            keep = (i == 1 and prev in CONJ) or (len(prev) >= 8 and len(rest) >= 5)
            res += ('、' if keep else '') + parts[i]
        out.append(res)
    return ''.join(out)


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    for s in ['家康は、なぜ、浜松城から出て、信玄と戦ったのでしょうか。', '元亀3年、12月22日、遠江の三方ヶ原で、武田信玄の軍と、徳川家康の軍が、ぶつかりました。', 'その夜の、「犀ヶ崖の夜襲」や、「空城の計」は、有名です。',
              'ところが、同時代に近い『信長公記』には、どちらも、書かれていません。', 'それが、軍を出して、武田軍を、追ったのです。']:
        print(s, '\n  ->', thin(s))
