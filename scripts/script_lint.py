"""台本の検査：python scripts/vp.py <slug> lint
台本（docs/themes/<theme>/09_script_v2.md）の、不自然な日本語になりやすい書き方を、機械で見つける。
  ・目的語が次の文に落ちた文（「…は、書きます。」のように、短くて「」も「こう」も無い文）
  ・「、」が多すぎる文／長すぎる文
  ・略称だけの呼び名（「公記」「実紀」）
  ・「…と。」で終わる文
  ・短すぎる文（読み上げが途切れる）
警告（WARN）だけで、止めない。直すかどうかは、台本を書く人が決める。"""
import re

UTTER = r'(書きます|書いています|書かれています|書いてあります|述べます|述べています|伝えます|伝えています|言います|言っています|記します|載せます)'


def run(V):
    th = V['theme_dir']() / '09_script_v2.md'
    text = th.read_text(encoding='utf8')
    out = []
    for c in re.split(r'\n## ', text)[1:]:
        head = c.split('\n')[0]
        lines = [re.sub(r'〔[^〕]*〕', '', re.sub(r'^\d+\. ', '', l)).strip() for l in c.split('\n') if re.match(r'^\d+\. ', l)]
        sents = [x.strip() + '。' for l in lines for x in l.split('。') if x.strip()]
        for i, s in enumerate(sents):
            w = f'{head.split("　")[-1]} 文{i}「{s[:22]}」'
            body = s.rstrip('。')
            if len(body) <= 26 and re.search(UTTER + r'$', body) and '「' not in body and 'こう' not in body and 'という' not in body:
                nxt = sents[i + 1] if i + 1 < len(sents) else ''
                out.append(f'{w}: 目的語が次の文に落ちている可能性（次の文「{nxt[:14]}」）。1文にまとめるか、「こう書いています」にする')
            if body.count('、') >= 4 and len(body) <= 70:
                out.append(f'{w}: 「、」が {body.count("、")}個。読点が多すぎる')
            if len(body) > 70:
                out.append(f'{w}: {len(body)}字。長すぎる（字幕と読み上げが重くなる）')
            if re.search(r'(?<!信長)公記', body):
                out.append(f'{w}: 「公記」だけの呼び方。『信長公記』と書く')
            if re.search(r'(?<!御)実紀', body):
                out.append(f'{w}: 「実紀」だけの呼び方。『東照宮御実紀』と書く')
            if re.search(r'と$', body):
                out.append(f'{w}: 「と。」で終わっている。ふつうの文末にする')
            if len(body) < 6 and body not in ('結論です',):
                out.append(f'{w}: {len(body)}字と短い。前後の文にまとめられないか')
            if body.count('は、') >= 3:
                out.append(f'{w}: 「は、」が {body.count("は、")}回。言い回しを変える')
    for m in out:
        print('WARN', m)
    print(f'lint: WARN {len(out)}')
    return 0
