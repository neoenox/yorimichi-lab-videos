"""usage: python scripts/_mkreview_gen.py <theme_dir> <out.md> "<固有の確認点>" ["<方針メモ>"]  台本v2があればv2、なければv1"""
import sys, os
theme, out, focus = sys.argv[1:4]
note = sys.argv[4] if len(sys.argv) > 4 else '確認が難しい事項（有料書籍・論文・紙資料、原本）は諦め、「未確認」と明記して公開する方針です。'
d = f'docs/themes/{theme}/'
sc = d + ('09_script_v2.md' if os.path.exists(d + '09_script_v2.md') else '09_script_v1.md')
head = f'''あなたは解説動画の台本の査読者です。以下の「事実確認メモ」と「台本」を読み、評価だけをしてください（書き直しは禁止）。

観点：
A. 事実の誤り・取り違え（Web検索で照合してください。新しい事実を挙げる場合は出典のURLか書名を必ず付けること）。特に：{focus}
B. 台本が、メモで確認できた範囲を超えて断定していないか。
C. 音声で聞いたとき誤解されやすい言い方。計算の誤り。
D. 「分かること」と「分からないこと」の線引きは適切か。
E. 構成・分量（約7〜9分、8〜10章。ナレーションの文字数は2,000〜3,000字を目安）。

注意：一般題材。{note} 指摘する場合は出典つきで。

出力形式：総評（3行）／指摘の表（No・重大度 高中低・該当箇所・理由・出典）／問題なしと判断した主張／自信の低い判断。

=== 事実確認メモ ===
'''
open(out, 'w', encoding='utf8').write(head + open(d + '08_fact_check.md', encoding='utf8').read() + '\n\n=== 台本 ===\n' + open(sc, encoding='utf8').read())
print(out)
