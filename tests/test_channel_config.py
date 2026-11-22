"""チャンネル設定(channel.toml)が、Short の描画に実際に効いていることの回帰テスト。

共通部品 ytkit が無い環境(CI など)では飛ばす。描画そのものは Windows のフォントが要るので、ここでは概要欄・キャプションと
設定の読み込みだけを確かめる(画素の一致は、設定化の前後で全コマ比較して確認済み)。
"""
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip('ytkit')

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
sys.path.insert(0, str(SCRIPTS))

REQUIRED = ('channel.name', 'channel.tagline', 'channel.tagline_tiktok', 'channel.about',
            'voice.speaker', 'voice.style', 'voice.credit', 'bgm.file', 'bgm.credit',
            'fonts.dir', 'fonts.sans', 'fonts.serif', 'hashtags.shorts', 'hashtags.tiktok')


def test_channel_toml_has_every_required_key():
    from ytkit.project import load_config, require
    cfg = load_config(ROOT)
    for k in REQUIRED:
        assert require(cfg, k), k


def test_description_and_caption_follow_the_config(monkeypatch):
    import make_short2 as M2
    spec = {'title': 'T', 'hook': 'H', 'notes': 'N', 'sec': 45}
    original = M2.description(spec)
    assert M2.CH['about'] in original and M2.VOICE['credit'] in original and M2.BGM['credit'] in original
    monkeypatch.setitem(M2.CH, 'about', 'ABOUT-X')
    monkeypatch.setitem(M2.VOICE, 'credit', 'VOICE-X')
    monkeypatch.setitem(M2.BGM, 'credit', 'BGM-X')
    monkeypatch.setitem(M2.TAGS, 'shorts', '#TAG-S')
    monkeypatch.setitem(M2.TAGS, 'tiktok', '#TAG-T')
    d = M2.description(spec)
    for s in ('ABOUT-X', 'VOICE-X', 'BGM-X', '#TAG-S'):
        assert s in d
    assert M2.description(spec) != original
    c = M2.tiktok_caption(spec)
    assert 'VOICE-X' in c and '#TAG-T' in c
    own = M2.tiktok_caption({**spec, 'hashtags': '#MINE'})   # spec の hashtags があれば、設定の既定より優先
    assert '#MINE' in own and '#TAG-T' not in own


def test_project_root_env_switches_the_channel(tmp_path):
    (tmp_path / 'channel.toml').write_text(
        '[channel]\nname = "別チャンネル"\ntagline = "t"\ntagline_tiktok = "tt"\nabout = "a"\n'
        '[voice]\nspeaker = "s"\nstyle = "st"\ncredit = "c"\n[bgm]\nfile = "b.mp3"\ncredit = "bc"\n'
        '[fonts]\ndir = "D:/f/"\nsans = "a.ttf"\nserif = "b.ttf"\n[hashtags]\nshorts = "#s"\ntiktok = "#t"\n', encoding='utf-8')
    code = 'import make_short as M; print(M.CH["name"], M.ROOT, M.FONTS["dir"], M.BGM["file"])'
    r = subprocess.run([sys.executable, '-c', code], cwd=SCRIPTS, capture_output=True, text=True, encoding='utf-8',
                       env={**__import__('os').environ, 'YT_PROJECT_ROOT': str(tmp_path), 'PYTHONUTF8': '1'})
    assert r.returncode == 0, r.stderr[-400:]
    assert r.stdout.split()[0] == '別チャンネル'
    assert str(tmp_path) in r.stdout and 'D:/f/' in r.stdout and 'b.mp3' in r.stdout


def test_missing_key_stops_with_the_key_name(tmp_path):
    (tmp_path / 'channel.toml').write_text('[channel]\nname = "x"\n', encoding='utf-8')
    code = 'import make_short'
    r = subprocess.run([sys.executable, '-c', code], cwd=SCRIPTS, capture_output=True, text=True, encoding='utf-8',
                       env={**__import__('os').environ, 'YT_PROJECT_ROOT': str(tmp_path), 'PYTHONUTF8': '1'})
    assert r.returncode != 0 and 'channel.tagline' in r.stderr


# ---- 長尺 vp.py

def _run_vp(code, root=None):
    import os
    env = {**os.environ, 'PYTHONUTF8': '1'}
    if root:
        env['YT_PROJECT_ROOT'] = str(root)
    return subprocess.run([sys.executable, '-c', code], cwd=SCRIPTS, capture_output=True, text=True, encoding='utf-8', env=env)


def test_vp_reads_the_default_config():
    r = _run_vp('import vp; print(vp.SPEED, vp.MAOU["piano36"], vp.BGM["pattern"].format(name="x"), vp.FONTS["sans"])')
    assert r.returncode == 0, r.stderr[-400:]
    assert r.stdout.split() == ['0.95', 'ピアノ36', 'maou_bgm_x.mp3', 'NotoSansJP-VF.ttf']


def test_vp_follows_another_channels_config(tmp_path):
    (tmp_path / 'channel.toml').write_text(
        '[channel]\nname = "N"\ntagline = "t"\ntagline_tiktok = "tt"\nabout = "ABOUT-L"\nterms_check = "TERMS-L"\n'
        '[voice]\nspeaker = "SPK"\nstyle = "STY"\ncredit = "c"\nspeed = 1.1\nlabel = "LBL"\ncredit_long = "VC-L"\n'
        '[bgm]\nfile = "b.mp3"\ncredit = "bc"\ndir = "x/bgm"\npattern = "song_{name}.wav"\ncredit_long = "MUSIC {tracks}"\n'
        '[bgm.names]\npiano = "Piano"\n'
        '[fonts]\ndir = "D:/f/"\nsans = "a.ttf"\nserif = "b.ttf"\n[hashtags]\nshorts = "#s"\ntiktok = "#t"\n', encoding='utf-8')
    r = _run_vp('import vp; print(vp.SPEED, vp.VOICE["speaker"], vp.VOICE["label"], vp.MAOU["piano7"], vp.BGM["dir"], '
                'vp.BGM["credit_long"].format(tracks="T"), vp.CH["terms_check"], vp.SPEC_F["serif"][0], vp.FONTS["dir"])', tmp_path)
    assert r.returncode == 0, r.stderr[-400:]
    assert r.stdout.split() == ['1.1', 'SPK', 'LBL', 'Piano7', 'x/bgm', 'MUSIC', 'T', 'TERMS-L', 'b.ttf', 'D:/f/']


def test_vp_stops_with_the_missing_long_form_key(tmp_path):
    (tmp_path / 'channel.toml').write_text('[channel]\nabout = "a"\nterms_check = "t"\n', encoding='utf-8')
    r = _run_vp('import vp', tmp_path)
    assert r.returncode != 0 and 'voice.' in r.stderr
