"""Short の根拠テーブル（claims / needs_research）を検査する。

2026-11-20 のオーナー確認で決めたゲート:
  1. 答えを変える断定（各シーンの text / big / sub）は primary の根拠を 1 つ以上持つ。
  2. 答えを変えない未確認は needs_research に残し、「なぜ答えが変わらないか」を一行添える。
  3. 公式本文の再掲（大学DB・Wayback）は primary 可。evidence_note に「代替」と明記する。

使い方:
  python scripts/check_short_evidence.py data/short_seijin.json [data/short_solo_x.json ...]

既存の data/short_*.json は祖父化しており、このスクリプトは**渡されたファイルだけ**を検査する。
CI / pre-commit は PR ・コミットで変更された data/short_*.json を渡すこと。
"""
import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

FIRST_PARTY_SUFFIX = '.go.jp'          # 官公庁の公式ドメイン
REPRINT_HOSTS = ('web.archive.org',)   # 法定保存
REPRINT_SUFFIXES = ('.ac.jp',)         # 大学が掲載する法令・資料の再掲
VALID_SOURCE_TYPES = ('primary', 'ai_assistant')
MIN_NOTE = 8
JUSTIFY_TOKENS = ('答えは変わらない', '答えに影響しない', '影響しない', '答えに効かない')


def err(msg):
    return ('ERROR', msg)


def warn(msg):
    return ('WARN', msg)


def _host(url):
    try:
        return (urlparse(url).hostname or '').lower()
    except ValueError:
        return ''


def is_reprint(url):
    host = _host(url)
    return host in REPRINT_HOSTS or host.endswith(REPRINT_SUFFIXES)


def check_spec(path):
    """1 つの spec を検査して (level, message) のリストを返す。"""
    issues = []
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    claims = data.get('claims')
    if not isinstance(claims, list) or not claims:
        return [err(f'{path}: claims が空（根拠テーブルが無い）')]

    ids = set()
    by_id = {}
    for i, c in enumerate(claims):
        tag = f'{path}: claims[{i}]'
        if not isinstance(c, dict):
            issues.append(err(f'{tag} が辞書ではない'))
            continue
        cid = c.get('id')
        if not isinstance(cid, str) or not cid.strip():
            issues.append(err(f'{tag}: id が空'))
            continue
        if cid in ids:
            issues.append(err(f'{tag}: id が重複している ({cid})'))
        ids.add(cid)
        by_id[cid] = c
        if not (c.get('statement') or '').strip():
            issues.append(err(f'{tag}: statement が空'))
        kind = c.get('source_type')
        if kind not in VALID_SOURCE_TYPES:
            issues.append(err(f'{tag}: source_type が不正 ({kind})'))
        note = (c.get('evidence_note') or '').strip()
        if len(note) < MIN_NOTE:
            issues.append(err(f'{tag}: evidence_note が短すぎる（何を確認したか書く）'))
        if kind == 'primary':
            url = c.get('source_url') or ''
            if not (url.startswith('https://') or url.startswith('http://')):
                issues.append(err(f'{tag}: primary なのに source_url が http(s) でない'))
            elif is_reprint(url) and '代替' not in note:
                issues.append(err(f'{tag}: 再掲URLなのに evidence_note に「代替」が無い'))
            elif not is_reprint(url) and not _host(url).endswith(FIRST_PARTY_SUFFIX):
                issues.append(warn(f'{tag}: 公式ドメイン外。一次資料として妥当か人を確認 ({_host(url)})'))
        elif kind == 'ai_assistant' and '質問' not in note:
            issues.append(err(f'{tag}: ai_assistant は「何を質問し何と答えたか」を evidence_note に書く'))

    needs = data.get('needs_research')
    if needs is None:
        needs = []
    if not isinstance(needs, list):
        issues.append(err(f'{path}: needs_research が配列でない'))
    else:
        for i, item in enumerate(needs):
            if not isinstance(item, str) or len(item.strip()) < 15:
                issues.append(err(f'{path}: needs_research[{i}] が短すぎる'))
            elif not any(tok in item for tok in JUSTIFY_TOKENS):
                issues.append(err(f'{path}: needs_research[{i}] に「なぜ答えが変わらないか」が無い'))

    used = set()
    scenes = data.get('scenes') or []
    if not isinstance(scenes, list) or not scenes:
        issues.append(err(f'{path}: scenes が空'))
    for i, sc in enumerate(scenes):
        if not isinstance(sc, dict) or sc.get('end'):
            continue
        cids = sc.get('claim_ids') or []
        if not cids:
            issues.append(err(f'{path}: scenes[{i}] に断定があるのに claim_ids が無い'))
            continue
        for cid in cids:
            used.add(cid)
            if cid not in ids:
                issues.append(err(f'{path}: scenes[{i}] が存在しない claim_id を参照 ({cid})'))
            elif by_id[cid].get('source_type') != 'primary':
                issues.append(err(f'{path}: scenes[{i}] の断定が primary 以外を根拠にしている ({cid})'))
    for cid in sorted(ids - used):
        issues.append(warn(f'{path}: claim {cid} がどのシーンからも参照されていない'))
    return issues


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('specs', nargs='+', help='検査する data/short_*.json')
    args = ap.parse_args()
    all_issues = []
    for p in args.specs:
        try:
            all_issues.extend(check_spec(p))
        except (OSError, json.JSONDecodeError) as e:
            all_issues.append(err(f'{p}: 読めない ({e})'))
    for level, msg in all_issues:
        print(f'{level}: {msg}')
    errors = [m for lv, m in all_issues if lv == 'ERROR']
    if errors:
        print(f'根拠テーブル検査: ERROR {len(errors)} 件。公開準備を止めます。')
        return 1
    print(f'根拠テーブル検査: OK（{len(args.specs)} ファイル、WARN {len(all_issues)} 件）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
