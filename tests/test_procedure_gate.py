"""手順書の読み取り確認の門番(scripts/procedure_gate.py)の回帰テスト。

門番は、手順書(docs/SOLO_SHORT_PROCEDURE.md)を「自分のスクリプトと同じプロジェクト」から読む。
以前は E:/rekishikaisetu の絶対パスで、作業の場で手順書を直しても、古いコピーを見続けていた。
隔離した一時プロジェクトにゲートと手順書をコピーして、フック(PreToolUse)の終了コードを確かめる。標準ライブラリだけで動く。
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATED = 'python scripts/solo_ship.py build x'
FREE = 'ls -la'


def _project(tmp_path, doc_text='手順書 v1\n'):
    (tmp_path / 'scripts').mkdir()
    (tmp_path / 'data').mkdir()
    (tmp_path / 'docs').mkdir()
    shutil.copy(ROOT / 'scripts' / 'procedure_gate.py', tmp_path / 'scripts' / 'procedure_gate.py')
    (tmp_path / 'docs' / 'SOLO_SHORT_PROCEDURE.md').write_text(doc_text, encoding='utf-8')
    (tmp_path / 'docs' / 'SOLO_SHORT_QUIZ.md').write_text('Q: x => y\n', encoding='utf-8')
    return tmp_path


def _hook(project, command):
    env = {**os.environ, 'PYTHONUTF8': '1'}
    env.pop('PROCEDURE_ACK_SKIP', None)
    r = subprocess.run([sys.executable, 'scripts/procedure_gate.py', 'hook'], cwd=project, input=json.dumps({'tool_input': {'command': command}}),
                       capture_output=True, text=True, encoding='utf-8', env=env)
    return r.returncode


def _ack(project, ts=None):
    h = hashlib.sha256((project / 'docs' / 'SOLO_SHORT_PROCEDURE.md').read_bytes()).hexdigest()[:16]
    (project / 'data' / '.procedure_ack.json').write_text(json.dumps({'hash': h, 'ts': ts or time.time()}), encoding='utf-8')


def test_gate_reads_the_docs_of_its_own_project_not_a_fixed_path():
    src = (ROOT / 'scripts' / 'procedure_gate.py').read_text(encoding='utf-8')
    assert "DOC = R / 'docs' / 'SOLO_SHORT_PROCEDURE.md'" in src and "QUIZ = R / 'docs' / 'SOLO_SHORT_QUIZ.md'" in src
    assert "Path('E:/" not in src


def test_gated_command_is_blocked_without_ack_and_allowed_with_a_valid_one(tmp_path):
    p = _project(tmp_path)
    assert _hook(p, GATED) == 2          # 印なし
    assert _hook(p, FREE) == 0           # 関係のないコマンドは通る
    _ack(p)
    assert _hook(p, GATED) == 0          # 有効な印


def test_changing_the_projects_own_procedure_doc_invalidates_the_ack(tmp_path):
    p = _project(tmp_path)
    _ack(p)
    assert _hook(p, GATED) == 0
    (p / 'docs' / 'SOLO_SHORT_PROCEDURE.md').write_text('手順書 v2(更新された)\n', encoding='utf-8')
    assert _hook(p, GATED) == 2          # 自分の docs/ を読んでいる証拠(固定パスなら、変わらず通ってしまう)


def test_expired_ack_is_blocked(tmp_path):
    p = _project(tmp_path)
    _ack(p, ts=time.time() - 25 * 3600)
    assert _hook(p, GATED) == 2
