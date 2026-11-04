"""寄り道ラボ Shorts 制作標準（shorts-standard/）を既存パイプラインへ繋ぐ橋渡し。

制作標準のルールは shorts-standard/README.md と PROMPT.md が正で、このスクリプトは
その規則を変更しない。形式検査は標準の validate.py をそのまま実行し、その上に
リポジトリ固有の追加検査（文字数/秒・断定の禁止表現・claim の実在確認など）を重ねる。

usage:
  python scripts/shorts_standard.py new <slug> --topic "題材"
       shorts/<slug>/brief.yaml の雛形を作る（事実は空。推測で埋めない）

  python scripts/shorts_standard.py brief-check <brief.yaml>
       brief に題材・視聴者の疑問・出典URL・確認済み事実が揃っているか検査

  python scripts/shorts_standard.py check <result.json>
       validate.py（形式）＋追加規則で検査。ERROR があれば終了コード 1

  python scripts/shorts_standard.py to-spec <result.json> [--slug s] [--art PATH]
       [--pron PATH] [--out PATH]
       合格した JSON を、既存レンダラ（scripts/make_short2.py）が読む
       data/short_<slug>.json 形式へ変換する。status が ready でなければ中止。

  python scripts/shorts_standard.py list
       shorts/*/result.json を列挙して状態を表示

既存のレンダラ・台本・素材は変更しない。to-spec の出力先は既定で
shorts/<slug>/short_spec.json（data/ へは自動で置かない＝誤公開を防ぐ）。
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / 'shorts-standard'
SCHEMA = STANDARD / 'output.schema.json'
VALIDATE = STANDARD / 'validate.py'

# 制作標準の固定値（README.md「固定ルール」）。ここを書き換えて緩和しないこと。
MIN_DURATION, MAX_DURATION = 30, 45
MIN_SCENES, MAX_SCENES = 5, 7
MIN_SCENE_SEC, MAX_SCENE_SEC = 3, 9
CHARS_PER_SEC = (4.0, 5.5)
CAPTION_LINES, CAPTION_CHARS = 2, 14
HOOK_SEC = 3.0
DIRECTION_SEC = 8.0

# PROMPT.md 5: 単なる「関連画像を表示」は禁止
BANNED_VISUAL = ('関連画像を表示', 'イメージ画像を表示', '適当な画像', 'フリー素材を表示')


def err(msg):
    return ('ERROR', msg)


def warn(msg):
    return ('WARN', msg)


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def load_brief(path):
    if yaml is None:
        raise SystemExit('PyYAML が必要です: pip install pyyaml')
    return yaml.safe_load(Path(path).read_text(encoding='utf-8'))


def run_official(path):
    """標準の validate.py をそのまま実行する（規則を複製しない）。"""
    p = subprocess.run([sys.executable, str(VALIDATE), str(path)],
                       text=True, encoding='utf-8', errors='replace', capture_output=True)
    out = (p.stdout + p.stderr).strip()
    return p.returncode == 0, out


def extra_checks(data, path=None):
    """validate.py が見ない規則を検査する。"""
    issues = []
    scenes = data.get('scenes') or []
    claims = data.get('claims') or []
    claim_ids = [c.get('id') for c in claims]

    # 1. 日本語の文字数/秒（README: 1秒あたり約4〜5.5文字。実測音声で最終調整）
    lo, hi = CHARS_PER_SEC
    for i, s in enumerate(scenes, 1):
        dur = (s.get('end') or 0) - (s.get('start') or 0)
        n = len(re.sub(r'\s', '', s.get('narration') or ''))
        if dur > 0:
            cps = n / dur
            if not lo <= cps <= hi:
                issues.append(warn('Scene %d: ナレーション %.1f 文字/秒（目安 %.1f〜%.1f、%d秒に%d文字）'
                                   % (i, cps, lo, hi, dur, n)))
        if not (s.get('narration') or '').strip():
            issues.append(err('Scene %d: narration が空' % i))

    # 2. 冒頭 0〜3秒に疑問・違和感（最初のシーンで問いを出す）
    if scenes:
        first = scenes[0]
        if (first.get('end') or 0) > HOOK_SEC + 0.5:
            issues.append(warn('Scene 1: 疑問の提示が %.1f 秒まで続く（0〜3秒に収める）' % (first.get('end') or 0)))
        if not re.search(r'[?？]', first.get('narration') or ''):
            issues.append(warn('Scene 1: ナレーションに疑問形（?／？）が無い'))

    # 3. 8秒以内に結論の方向性（claim 付きのシーンがあるか）
    if scenes and claims:
        has_dir = any((s.get('start') or 0) < DIRECTION_SEC and s.get('claim_ids') for s in scenes)
        if not has_dir:
            issues.append(warn('8秒以内に事実根拠（claim_ids）付きのシーンが無い（結論の方向性を示す）'))

    # 4. 画面テキスト（1行14文字・2行以内は schema が見る。空行と全角の詰め込みを追加で見る）
    for i, s in enumerate(scenes, 1):
        for line in s.get('caption') or []:
            if not str(line).strip():
                issues.append(err('Scene %d: caption に空の行がある' % i))
            if len(str(line)) > CAPTION_CHARS:
                issues.append(err('Scene %d: caption が %d 文字を超える: %s' % (i, CAPTION_CHARS, line)))

    # 5. 映像指示が具体的か（禁止表現）
    for i, s in enumerate(scenes, 1):
        visual = s.get('visual') or ''
        for banned in BANNED_VISUAL:
            if banned in visual:
                issues.append(err('Scene %d: visual が具体的でない（「%s」は禁止）' % (i, banned)))
        if '模式図' not in visual and 'イメージ' not in visual and '資料' not in visual and '実写' not in visual:
            issues.append(warn('Scene %d: 映像の種別（模式図／イメージ／資料）が visual に書かれていない' % i))

    # 6. 事実の主張と出典（status=ready は claims 必須）
    if data.get('status') == 'ready' and not claims:
        issues.append(err('status=ready なのに claims が空（根拠の無い断定は禁止）'))
    if len(claim_ids) != len(set(claim_ids)):
        issues.append(err('claims の id が重複している'))
    for c in claims:
        url = (c.get('source_url') or '').strip()
        if not re.match(r'https?://', url):
            issues.append(err('claim %s: source_url が http(s) ではない' % c.get('id')))
        if len((c.get('evidence_note') or '').strip()) < 5:
            issues.append(err('claim %s: evidence_note が短すぎる（何を確認したか書く）' % c.get('id')))
        if not (c.get('statement') or '').strip():
            issues.append(err('claim %s: statement が空' % c.get('id')))

    # 7. claims があるのに根拠IDを持たないシーン（断定の出所が不明）
    if claims:
        for i, s in enumerate(scenes, 1):
            if not s.get('claim_ids'):
                issues.append(warn('Scene %d: claim_ids が空（事実を述べる場面なら根拠IDを付ける）' % i))

    # 8. 合計時間と文字数の整合
    total = data.get('duration_sec') or 0
    if total:
        chars = sum(len(re.sub(r'\s', '', s.get('narration') or '')) for s in scenes)
        cps = chars / total
        if not CHARS_PER_SEC[0] <= cps <= CHARS_PER_SEC[1]:
            issues.append(warn('全体: %.1f 文字/秒（目安 %.1f〜%.1f）' % (cps, *CHARS_PER_SEC)))

    # 9. 常に人の確認が要る（機械検査は形式だけ）
    issues.append(warn('形式検査は PASS でも、出典の原文照合・読み・スマホ可読性は人が確認する'))
    return issues


def check(path):
    """validate.py（形式）＋追加規則で検査する。"""
    data = load_json(path)
    ok, out = run_official(path)
    official_errors = [] if ok else [err(line) for line in out.splitlines() if line and not line.startswith('PASS')]
    issues = official_errors + extra_checks(data, path)
    return ok, issues


def check_data(data):
    """メモリ上の JSON を検査する（validate.py に渡すため一時ファイルへ書く）。"""
    import tempfile
    with tempfile.TemporaryDirectory(prefix='shorts-check-') as d:
        p = Path(d) / 'result.json'
        p.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        return check(p)


def brief_check(path):
    b = load_brief(path)
    issues = []
    for key in ('topic', 'viewer_question', 'audience', 'visual_assets'):
        if not str((b or {}).get(key) or '').strip():
            issues.append(err('brief: %s が空' % key))
    urls = (b or {}).get('source_urls') or []
    if not urls:
        issues.append(err('brief: source_urls が空（出典の無い題材は制作しない）'))
    for u in urls:
        if not re.match(r'https?://', str(u)):
            issues.append(err('brief: source_urls に URL でない値: %s' % u))
    facts = (b or {}).get('verified_facts') or []
    if not facts:
        issues.append(err('brief: verified_facts が空（確認済みの事実を先に書く）'))
    if not (b or {}).get('caveats'):
        issues.append(warn('brief: caveats が空（留保・複数説を書く）'))
    return issues


def to_spec(data, slug, art=None, pron=None, out=None, long_id=None, long_title=None):
    """標準 JSON → 既存レンダラ（scripts/make_short2.py）の spec。"""
    src = ' '.join(s.get('narration') or '' for s in data['scenes'])
    for line in src.splitlines():
        if len(line) > 0 and not line.strip():
            raise SystemExit('narration に空行')
    claims = data.get('claims') or []
    notes = '\n'.join('・%s' % c['statement'] for c in claims)
    refs = ['%s — %s' % (c['statement'], c['source_url']) for c in claims]
    spec = {
        'title': data['title'],
        'hook': data['hook'],
        'notes': notes,
        'refs': refs,
        'pron': pron or 'shorts/%s/pron.json' % slug,
        'art': art or 'assets/%s/art.png' % slug,
        'scenes': [{
            'text': s['narration'],
            'big': (s.get('caption') or [''])[0],
            'sub': (s.get('caption') or ['', ''])[1] if len(s.get('caption') or []) > 1 else '',
            'art': art or 'assets/%s/art.png' % slug,
        } for s in data['scenes']],
        # 制作標準: 無意味な登録誘導は禁止 → 既定でCTAを付けない
        'cta': False,
        'status': data.get('status'),
        'claims': claims,
        'needs_research': data.get('needs_research') or [],
    }
    if long_id:
        spec['long_id'] = long_id
    if long_title:
        spec['long_title'] = long_title
    dest = Path(out) if out else ROOT / 'shorts' / slug / 'short_spec.json'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
    return dest, spec


def cmd_new(args):
    slug = args.slug
    d = ROOT / 'shorts' / slug
    if (d / 'brief.yaml').exists():
        raise SystemExit('既に存在します: %s' % (d / 'brief.yaml'))
    d.mkdir(parents=True, exist_ok=True)
    brief = {
        'topic': args.topic or '',
        'viewer_question': '',
        'audience': '一般視聴者・予備知識なし',
        'source_urls': [],
        'verified_facts': [],
        'caveats': [],
        'visual_assets': '',
    }
    (d / 'brief.yaml').write_text(
        yaml.safe_dump(brief, allow_unicode=True, sort_keys=False), encoding='utf-8')
    print('作成:', d / 'brief.yaml')
    print('次: source_urls と verified_facts を実際に確認してから埋める（推測で書かない）')
    print('    python scripts/shorts_standard.py brief-check %s' % (d / 'brief.yaml'))
    return 0


def cmd_brief_check(args):
    issues = brief_check(args.brief)
    print_issues(issues)
    return 0 if not any(lv == 'ERROR' for lv, _ in issues) else 1


def cmd_check(args):
    ok, issues = check(args.result)
    print('meta: %s (%s)' % (args.result, 'validate.py PASS' if ok else 'validate.py FAIL'))
    print_issues(issues)
    return 0 if not any(lv == 'ERROR' for lv, _ in issues) else 1


def cmd_to_spec(args):
    data = load_json(args.result)
    ok, issues = check(args.result)
    print_issues(issues)
    errors = [m for lv, m in issues if lv == 'ERROR']
    if errors:
        print('中止: 形式検査/追加検査に ERROR がある（レンダラへ渡さない）')
        return 1
    if data.get('status') != 'ready':
        print('中止: status=%s。出典の原文照合を終えて ready にしてから変換する'
              % data.get('status'))
        print('  未確認: %s' % ', '.join(data.get('needs_research') or ['(needs_research が空)']))
        return 1
    slug = args.slug or Path(args.result).resolve().parent.name
    dest, spec = to_spec(data, slug, args.art, args.pron, args.out, args.long_id, args.long_title)
    print('作成:', dest)
    print('  シーン %d / caption・art を確認し、python scripts/make_short2.py %s で描画（VOICEVOX 起動が必要）'
          % (len(spec['scenes']), slug))
    return 0


def cmd_list(args):
    rows = sorted((ROOT / 'shorts').glob('*/result.json'))
    if not rows:
        print('shorts/*/result.json はまだありません')
        return 0
    for r in rows:
        try:
            d = load_json(r)
            print('%-28s %-12s %5.1fs %2d scenes  needs_research=%d'
                  % (r.parent.name, d.get('status'), d.get('duration_sec') or 0,
                     len(d.get('scenes') or []), len(d.get('needs_research') or [])))
        except Exception as e:  # 壊れた JSON も一覧では見せる
            print('%-28s 読み込み失敗: %s' % (r.parent.name, e))
    return 0


def print_issues(issues):
    for lv, msg in issues:
        print('%-5s %s' % (lv, msg))


def main():
    ap = argparse.ArgumentParser(description='Shorts 制作標準の検査・変換')
    sub = ap.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('new', help='brief.yaml の雛形を作る')
    p.add_argument('slug')
    p.add_argument('--topic', default='')
    p.set_defaults(func=cmd_new)

    p = sub.add_parser('brief-check', help='brief の必須項目を検査')
    p.add_argument('brief')
    p.set_defaults(func=cmd_brief_check)

    p = sub.add_parser('check', help='result.json を検査（validate.py + 追加規則）')
    p.add_argument('result')
    p.set_defaults(func=cmd_check)

    p = sub.add_parser('to-spec', help='合格 JSON をレンダラ用 spec へ変換')
    p.add_argument('result')
    p.add_argument('--slug')
    p.add_argument('--art')
    p.add_argument('--pron')
    p.add_argument('--out')
    p.add_argument('--long-id')
    p.add_argument('--long-title')
    p.set_defaults(func=cmd_to_spec)

    p = sub.add_parser('list', help='shorts/ の制作状況')
    p.set_defaults(func=cmd_list)

    a = ap.parse_args()
    return a.func(a)


if __name__ == '__main__':
    sys.exit(main())
