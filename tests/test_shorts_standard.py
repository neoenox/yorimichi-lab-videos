"""Shorts 制作標準（shorts-standard/）のゲートが緩まないことを確かめる。

方針:
  ・標準のルール値（30〜45秒、5〜7シーン、1シーン3〜9秒、caption 14文字2行）が
    変わっていないことを schema から直接読んで検査する（勝手な緩和の検知）。
  ・validate.py の形式検査と、リポジトリ固有の追加検査（scripts/shorts_standard.py）を
    実際に実行して、通る例と止まる例の両方を確かめる。
  ・レンダラ（scripts/make_short2.py）へ渡す spec への変換は、status=ready のみ許可。
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / 'shorts-standard'
SCRIPT = ROOT / 'scripts' / 'shorts_standard.py'
SAMPLE = ROOT / 'shorts' / 'sample_edo_map_compare' / 'result.json'

sys.path.insert(0, str(ROOT / 'scripts'))
import shorts_standard as S  # noqa: E402


def sample():
    return json.loads(SAMPLE.read_text(encoding='utf-8'))


def run_cli(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=ROOT,
                          text=True, encoding='utf-8', errors='replace', capture_output=True)


def errors(issues):
    return [m for lv, m in issues if lv == 'ERROR']


class RuleGuardTests(unittest.TestCase):
    """schema の固定値を直接読み、緩和されていないことを確認する。"""

    def setUp(self):
        self.schema = json.loads((STANDARD / 'output.schema.json').read_text(encoding='utf-8'))

    def test_duration_rule(self):
        d = self.schema['properties']['duration_sec']
        self.assertEqual((d['minimum'], d['maximum']), (30, 45))
        self.assertEqual((S.MIN_DURATION, S.MAX_DURATION), (30, 45))

    def test_scene_count_rule(self):
        sc = self.schema['properties']['scenes']
        self.assertEqual((sc['minItems'], sc['maxItems']), (5, 7))
        self.assertEqual((S.MIN_SCENES, S.MAX_SCENES), (5, 7))

    def test_caption_rule(self):
        cap = self.schema['properties']['scenes']['items']['properties']['caption']
        self.assertEqual(cap['maxItems'], 2)
        self.assertEqual(cap['items']['maxLength'], 14)
        self.assertEqual((S.CAPTION_LINES, S.CAPTION_CHARS), (2, 14))

    def test_status_and_required_fields(self):
        self.assertEqual(self.schema['properties']['status']['enum'], ['ready', 'needs_review'])
        for key in ('title', 'hook', 'duration_sec', 'status', 'scenes', 'claims', 'needs_research'):
            self.assertIn(key, self.schema['required'])

    def test_scene_duration_rule_in_validator(self):
        text = (STANDARD / 'validate.py').read_text(encoding='utf-8')
        self.assertIn('3 <= length <= 9', text)


class CheckTests(unittest.TestCase):
    def test_repository_sample_passes(self):
        ok, issues = S.check_data(sample())
        self.assertTrue(ok, [m for lv, m in issues if lv == 'ERROR'])
        self.assertEqual(errors(issues), [])

    def test_gap_between_scenes_is_error(self):
        data = sample()
        data['scenes'][1]['start'] += 0.5
        ok, issues = S.check_data(data)
        self.assertTrue(errors(issues))

    def test_unknown_claim_id_is_error(self):
        data = sample()
        data['scenes'][2]['claim_ids'] = ['c_missing']
        ok, issues = S.check_data(data)
        self.assertTrue(any('c_missing' in m for m in errors(issues)))

    def test_needs_research_cannot_be_ready(self):
        data = sample()
        data['status'] = 'ready'
        ok, issues = S.check_data(data)
        self.assertTrue(any('Research incomplete' in m for m in errors(issues)))

    def test_ready_requires_claims(self):
        data = sample()
        data['status'] = 'ready'
        data['needs_research'] = []
        data['claims'] = []
        for s in data['scenes']:
            s['claim_ids'] = []
        ok, issues = S.check_data(data)
        self.assertTrue(any('claims が空' in m for m in errors(issues)))

    def test_generic_visual_is_error(self):
        data = sample()
        data['scenes'][0]['visual'] = '関連画像を表示する'
        ok, issues = S.check_data(data)
        self.assertTrue(any('具体的でない' in m for m in errors(issues)))

    def test_slow_narration_is_warning(self):
        data = sample()
        data['scenes'][0]['narration'] = 'あ'
        ok, issues = S.check_data(data)
        self.assertTrue(any('文字/秒' in m for lv, m in issues if lv == 'WARN'))

    def test_caption_too_long_is_error(self):
        data = sample()
        data['scenes'][0]['caption'] = ['あ' * 15]
        ok, issues = S.check_data(data)
        self.assertTrue(any('14 文字を超える' in m for m in errors(issues)))


class BriefTests(unittest.TestCase):
    def test_sample_brief_passes(self):
        issues = S.brief_check(ROOT / 'shorts' / 'sample_edo_map_compare' / 'brief.yaml')
        self.assertEqual(errors(issues), [])


class ToSpecTests(unittest.TestCase):
    def test_cli_refuses_needs_review(self):
        p = run_cli('to-spec', str(SAMPLE))
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('needs_review', p.stdout + p.stderr)

    def test_ready_converts_to_renderer_spec(self):
        data = sample()
        data['status'] = 'ready'
        data['needs_research'] = []
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / 'ready.json'
            src.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
            out = Path(tmp) / 'spec.json'
            p = run_cli('to-spec', str(src), '--slug', 'unit_test', '--out', str(out),
                        '--art', 'assets/unit/art.png', '--pron', 'data/unit_pron.json')
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            spec = json.loads(out.read_text(encoding='utf-8'))
        self.assertEqual(len(spec['scenes']), len(data['scenes']))
        self.assertEqual(spec['scenes'][0]['text'], data['scenes'][0]['narration'])
        self.assertEqual(spec['scenes'][0]['big'], data['scenes'][0]['caption'][0])
        self.assertEqual(spec['scenes'][3]['sub'], '')  # caption が1行なら sub は空
        self.assertIs(spec['cta'], False)          # 無意味な登録誘導は付けない
        self.assertEqual(spec['pron'], 'data/unit_pron.json')
        self.assertEqual(len(spec['refs']), len(data['claims']))
        self.assertTrue(spec['notes'])
        self.assertEqual(spec['status'], 'ready')


if __name__ == '__main__':
    unittest.main()
