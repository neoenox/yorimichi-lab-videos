"""コードが、プロジェクトの外の絶対パス(E:/rekishikaisetu)を直接指していないことの回帰テスト。

以前は、台本レビュー用のテキスト(out/)、レビュー用の動画(sigcmp_view/)、Remotion の Chrome(node_modules/)を、
`E:/rekishikaisetu/...` と決め打ちしていた。そのため、そのフォルダーを消せなかった。
プロジェクトのルート(Path(__file__).parents[1] など)からの相対で指す。標準ライブラリだけで動く。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# 「E:/rekishikaisetu」または「E:\rekishikaisetu」で、直後が「-honnoji」でないもの
PATTERN = re.compile(r'E:[/\\]+rekishikaisetu(?!-)')
SUFFIXES = {'.py', '.mjs', '.js', '.sh'}
SKIP_PARTS = {'__pycache__', 'node_modules', '.venv', 'tools'}


def _code_files():
    for base in ('scripts', 'tests'):
        for p in (ROOT / base).rglob('*'):
            if p.suffix in SUFFIXES and p.is_file() and not (SKIP_PARTS & set(p.relative_to(ROOT).parts)):
                yield p


def test_no_code_points_at_the_old_e_root():
    hits = []
    for p in _code_files():
        if p.name == Path(__file__).name:
            continue
        for i, line in enumerate(p.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
            if PATTERN.search(line):
                hits.append(f'{p.relative_to(ROOT).as_posix()}:{i}: {line.strip()[:100]}')
    assert not hits, 'E:/rekishikaisetu を直接指している:\n' + '\n'.join(hits)
