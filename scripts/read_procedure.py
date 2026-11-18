"""単独Short手順書を読み、確認問題に答えて、24時間有効の「読み取り確認の印」を作る。
  python scripts/read_procedure.py                  # 全体と、部分の数を表示
  python scripts/read_procedure.py --part N         # N番目の部分を表示(全部分を表示しないと、問題に進めない)
  python scripts/read_procedure.py --questions      # 確認問題を表示
  python scripts/read_procedure.py --answer 1=… 2=… # 答える(全問正解で印ができる)
問題は E:/rekishikaisetu/docs/SOLO_SHORT_QUIZ.md から読む(書式は、その文書の冒頭)。手順書が変わると、印は無効になる。
"""
import json, re, sys, time, unicodedata
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import procedure_gate as G

sys.stdout.reconfigure(encoding='utf8')
LIM = 11000   # 1部分の最大文字数(Bashの出力上限30000字に収める)


def parts():
    t = G.DOC.read_text(encoding='utf8')
    secs = re.split(r'(?m)^(?=## )', t)
    out, cur = [], ''
    for s in secs:
        if cur and len(cur) + len(s) > LIM:
            out.append(cur); cur = ''
        if len(s) > LIM:            # 1章が長すぎる場合は行で分ける
            for ln in s.splitlines(keepends=True):
                if len(cur) + len(ln) > LIM:
                    out.append(cur); cur = ''
                cur += ln
        else:
            cur += s
    if cur:
        out.append(cur)
    return out


def load_state():
    h = G.doc_hash()
    try:
        s = json.loads(G.STATE.read_text(encoding='utf8'))
    except Exception:
        s = {}
    if s.get('hash') != h:
        s = {'hash': h, 'seen': []}
    return s


def save_state(s):
    G.STATE.parent.mkdir(parents=True, exist_ok=True)
    G.STATE.write_text(json.dumps(s), encoding='utf8')


def quiz():
    qs = []
    for ln in G.QUIZ.read_text(encoding='utf8').splitlines():
        m = re.match(r'^Q:\s*(.+?)\s*=>\s*(.+)$', ln)
        if m:
            qs.append((m.group(1), [[a.strip() for a in k.split('/') if a.strip()] for k in m.group(2).split(';') if k.strip()]))
    return qs


def norm(x):
    return unicodedata.normalize('NFKC', x).replace(' ', '').replace('\u3000', '').lower()


def all_seen(P, s):
    return all(i in s['seen'] for i in range(1, len(P) + 1))


def main():
    a = sys.argv[1:]
    P = parts()
    s = load_state()
    if not a:
        ok, msg = G.status()
        print(f'手順書: {G.DOC}\n全{len(P)}部分。1から順に `--part N` で表示して、すべて読んでください(読み飛ばすと問題に進めません)。')
        print('現在の状態: ' + ('確認済み(有効)' if ok else '未確認/期限切れ/手順書が更新された'))
        print('表示済みの部分: ' + (','.join(map(str, sorted(s['seen']))) or 'なし'))
        for i, p in enumerate(P, 1):
            heads = re.findall(r'(?m)^##+ (.+)$', p)
            print(f'  part {i}: {heads[0] if heads else "(続き)"} ほか({len(p)}字)')
        return
    if a[0] == '--part':
        n = int(a[1])
        if not 1 <= n <= len(P):
            sys.exit(f'part は 1〜{len(P)}')
        print(f'===== 手順書 part {n}/{len(P)} =====\n')
        print(P[n - 1])
        print(f'\n===== part {n}/{len(P)} ここまで =====')
        if n not in s['seen']:
            s['seen'].append(n); save_state(s)
        if n < len(P):
            print(f'次: python scripts/read_procedure.py --part {n + 1}')
        else:
            print('次: python scripts/read_procedure.py --questions (未表示の部分があれば、先にそれを表示)')
        return
    if a[0] in ('--questions', '--answer'):
        if not all_seen(P, s):
            miss = [i for i in range(1, len(P) + 1) if i not in s['seen']]
            sys.exit(f'まだ表示していない部分があります: part {miss}。`--part N` で表示して読んでから、問題に進んでください。')
        Q = quiz()
        if a[0] == '--questions':
            print('確認問題(手順書を読めば答えられます。`--answer 1=答え 2=答え …`):')
            for i, (q, _) in enumerate(Q, 1):
                print(f'  {i}. {q}')
            return
        ans = {}
        for x in a[1:]:
            m = re.match(r'^(\d+)=(.*)$', x, re.S)
            if m:
                ans[int(m.group(1))] = norm(m.group(2))
        bad = []
        for i, (q, kws) in enumerate(Q, 1):
            t = ans.get(i, '')
            if not all(any(norm(alt) in t for alt in alts) for alts in kws):
                bad.append(i)
        if bad:
            print(f'不正解または未回答: {bad}。手順書を読み直して、もう一度 `--answer` してください(正解は表示しません)。')
            sys.exit(1)
        G.ACK.parent.mkdir(parents=True, exist_ok=True)
        G.ACK.write_text(json.dumps({'hash': G.doc_hash(), 'ts': time.time(), 'when': time.strftime('%Y-%m-%d %H:%M:%S')}), encoding='utf8')
        print('全問正解。読み取り確認の印を作りました(24時間有効。手順書が更新されると無効)。')
        return
    sys.exit(__doc__)


if __name__ == '__main__':
    main()
