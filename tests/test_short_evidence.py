"""Short の根拠テーブルゲートが緩まないことを確かめる。

通る例と止まる例の両方を実行する。既存 spec の全件検査ではなく、ゲートに
渡したファイルだけを検査する設計（既存は祖父化）も確認する。
"""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'check_short_evidence.py'
sys.path.insert(0, str(ROOT / 'scripts'))
import check_short_evidence as E  # noqa: E402


def valid_spec():
    return {
        'title': 'テスト',
        'claims': [
            {
                'id': 'c1',
                'statement': '成人の日は1月の第2月曜日',
                'source_type': 'primary',
                'source_url': 'https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html',
                'evidence_note': '内閣府の本文を2026-11-20に確認した',
            },
        ],
        'needs_research': [],
        'scenes': [
            {'text': '今は第二月曜日です', 'big': '第2月曜日', 'claim_ids': ['c1']},
            {'text': 'くわしくは本編で', 'end': True},
        ],
    }


def errors(issues):
    return [m for lv, m in issues if lv == 'ERROR']


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'short_test.json'
        self.data = valid_spec()

    def check(self, data=None):
        self.path.write_text(json.dumps(self.data if data is None else data, ensure_ascii=False),
                             encoding='utf-8')
        return E.check_spec(str(self.path))

    def test_valid_spec_passes(self):
        self.assertEqual(errors(self.check()), [])

    def test_missing_claims_fails(self):
        d = copy.deepcopy(self.data)
        del d['claims']
        self.assertTrue(any('claims が空' in m for m in errors(self.check(d))))

    def test_scene_without_claim_ids_fails(self):
        d = copy.deepcopy(self.data)
        del d['scenes'][0]['claim_ids']
        self.assertTrue(any('claim_ids が無い' in m for m in errors(self.check(d))))

    def test_primary_without_url_fails(self):
        d = copy.deepcopy(self.data)
        del d['claims'][0]['source_url']
        self.assertTrue(any('http(s) でない' in m for m in errors(self.check(d))))

    def test_duplicate_id_fails(self):
        d = copy.deepcopy(self.data)
        d['claims'].append(copy.deepcopy(d['claims'][0]))
        self.assertTrue(any('重複' in m for m in errors(self.check(d))))

    def test_unverified_research_without_reason_fails(self):
        d = copy.deepcopy(self.data)
        d['needs_research'] = ['自治体ごとの成人式の対象年齢は、このShortでは扱っていないため未確認のまま']
        self.assertTrue(any('答えが変わらないか' in m for m in errors(self.check(d))))

    def test_verified_research_with_reason_passes(self):
        d = copy.deepcopy(self.data)
        d['needs_research'] = ['自治体ごとの対象年齢はこのShortでは言及しないため答えに影響しない']
        self.assertEqual(errors(self.check(d)), [])

    def test_reprint_needs_substitution_note(self):
        d = copy.deepcopy(self.data)
        d['claims'][0]['source_url'] = 'https://jahis.law.nagoya-u.ac.jp/lawdb/l/410a0141'
        self.assertTrue(any('「代替」が無い' in m for m in errors(self.check(d))))
        d['claims'][0]['evidence_note'] += '。e-Govから取得できず大学DBの条文を代替として確認'
        self.assertEqual(errors(self.check(d)), [])

    def test_ai_assistant_cannot_back_assertion(self):
        d = copy.deepcopy(self.data)
        d['claims'][0]['source_type'] = 'ai_assistant'
        self.assertTrue(any('primary 以外' in m for m in errors(self.check(d))))

    def test_unknown_claim_reference_fails(self):
        d = copy.deepcopy(self.data)
        d['scenes'][0]['claim_ids'] = ['missing']
        self.assertTrue(any('存在しない claim_id' in m for m in errors(self.check(d))))

    def test_cli_exit_code(self):
        self.path.write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8')
        ok = subprocess.run([sys.executable, str(SCRIPT), str(self.path)], cwd=ROOT,
                            text=True, encoding='utf-8', errors='replace', capture_output=True)
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        bad = copy.deepcopy(self.data)
        del bad['claims']
        self.path.write_text(json.dumps(bad, ensure_ascii=False), encoding='utf-8')
        ng = subprocess.run([sys.executable, str(SCRIPT), str(self.path)], cwd=ROOT,
                            text=True, encoding='utf-8', errors='replace', capture_output=True)
        self.assertEqual(ng.returncode, 1, ng.stdout + ng.stderr)


if __name__ == '__main__':
    unittest.main()
