"""単独Short手順書の「読み取り確認」の門番。

  ・印(確認済み)は data/.procedure_ack.json。`python scripts/read_procedure.py` を最後まで進め、確認問題に全問正解した人だけが作れる。
  ・印は、手順書(E:/rekishikaisetu/docs/SOLO_SHORT_PROCEDURE.md)の内容(ハッシュ)が変わると無効になる。24時間で期限切れ。
  ・台本生成(solo_spec.build / fv_prompts)、solo_ship.py、solo_schedule.py が require() を呼び、印が無ければ止まる。
  ・`python scripts/procedure_gate.py hook` は Claude Code の PreToolUse フック用(標準入力のJSONを読み、対象コマンドを印なしで呼ぶと exit 2 で止める)。
  ・非常用: 環境変数 PROCEDURE_ACK_SKIP=1 で通せる(警告を出す)。使ったら、理由をユーザーに報告すること。
"""
import hashlib, json, os, re, sys, time
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf8')
    except Exception:
        pass
R = Path(__file__).resolve().parents[1]
DOC = Path('E:/rekishikaisetu/docs/SOLO_SHORT_PROCEDURE.md')
QUIZ = Path('E:/rekishikaisetu/docs/SOLO_SHORT_QUIZ.md')
ACK = R / 'data' / '.procedure_ack.json'
STATE = R / 'data' / '.procedure_read.json'
TTL = 24 * 3600

HOW = ('手順書を読み取り確認していません。次の順に進めてください:\n'
       '  1) python scripts/read_procedure.py            (全体の流れと、読む部分の数を表示)\n'
       '  2) python scripts/read_procedure.py --part 1   (…最後の部分まで、すべて表示して読む)\n'
       '  3) python scripts/read_procedure.py --questions (確認問題を表示)\n'
       '  4) python scripts/read_procedure.py --answer 1=... 2=... (全問正解で、24時間有効の印ができる)\n'
       '手順書: ' + str(DOC))


def doc_hash():
    return hashlib.sha256(DOC.read_bytes()).hexdigest()[:16]


def status():
    """(ok, message)"""
    try:
        h = doc_hash()
    except Exception as e:
        return False, f'手順書を読めません: {DOC} ({e})'
    if not ACK.exists():
        return False, HOW
    try:
        a = json.loads(ACK.read_text(encoding='utf8'))
    except Exception:
        return False, HOW
    if a.get('hash') != h:
        return False, '手順書が更新されています。もう一度、読み取り確認をしてください。\n' + HOW
    if time.time() - a.get('ts', 0) > TTL:
        return False, '読み取り確認の期限(24時間)が切れています。もう一度、確認してください。\n' + HOW
    return True, 'ok'


def require():
    if os.environ.get('PROCEDURE_ACK_SKIP') == '1':
        print('警告: PROCEDURE_ACK_SKIP=1 で手順書の読み取り確認を省略しています(理由をユーザーに報告すること)', file=sys.stderr)
        return
    ok, msg = status()
    if not ok:
        print('【止めました】' + msg, file=sys.stderr)
        sys.exit(3)


PATTERN = re.compile(r'(python[0-9.]*(\.exe)?\s+[^|;&\n]*?(gen_solo_\w+|solo_ship|solo_schedule|freevideo_batch|pack_short|make_short2)\.py)|(bash\s+[^|;&\n]*fv_clips\.sh)')


def hook():
    try:
        d = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    cmd = (d.get('tool_input') or {}).get('command', '') or ''
    if 'read_procedure.py' in cmd or 'procedure_gate.py' in cmd:
        sys.exit(0)
    if not PATTERN.search(cmd):
        sys.exit(0)
    if os.environ.get('PROCEDURE_ACK_SKIP') == '1':
        sys.exit(0)
    ok, msg = status()
    if ok:
        sys.exit(0)
    print('【止めました】単独Shortの作成・公開に関わる操作です。先に手順書の読み取り確認が必要です。\n' + msg, file=sys.stderr)
    sys.exit(2)


if __name__ == '__main__':
    c = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if c == 'hook':
        hook()
    else:
        ok, msg = status()
        print(msg)
        sys.exit(0 if ok else 3)
