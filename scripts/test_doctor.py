"""Doctor diagnostics must not fail when optional tools or drives are missing."""
import json
from collections import namedtuple

from scripts import doctor as d


def test_missing_executable_is_reported(monkeypatch):
    def missing(*args, **kwargs):
        raise FileNotFoundError('missing tool')

    monkeypatch.setattr(d.subprocess, 'run', missing)
    result = d.command(['not-installed'])
    assert result['returncode'] != 0
    assert 'missing tool' in result['output']


def test_unavailable_drive_does_not_abort_other_disks(monkeypatch):
    Usage = namedtuple('Usage', 'total used free')

    def usage(path):
        if path == 'E:\\':
            raise FileNotFoundError('drive not mounted')
        return Usage(100, 20, 80)

    monkeypatch.setattr(d.shutil, 'disk_usage', usage)
    result = d.disk_usage(['C:\\', 'E:\\'])
    assert result['C:\\'] == {'total': 100, 'used': 20, 'free': 80}
    assert 'drive not mounted' in result['E:\\']['error']


def test_doctor_writes_diagnostics_without_optional_dependencies(tmp_path, monkeypatch):
    monkeypatch.setattr(d, 'ROOT', tmp_path)
    monkeypatch.setattr(d, 'disk_usage', lambda paths: {'C:\\': {'error': 'unavailable'}, 'E:\\': {'error': 'unavailable'}})
    monkeypatch.setattr(d, 'command', lambda args: {'returncode': 127, 'output': 'tool unavailable'})
    d.doctor()
    report = json.loads((tmp_path / 'out' / 'doctor.json').read_text(encoding='utf8'))
    assert report['disk']['E:\\']['error'] == 'unavailable'
    assert report['gpu']['returncode'] == 127
    assert report['ffmpeg'] == 'tool unavailable'
