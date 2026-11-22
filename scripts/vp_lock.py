"""二重起動を防ぐ鍵と、GPU（NVENC）の分け合い。
  ・build / audio / prep は、同じ slug で同時に1つしか動かせない（cache/<slug>.lock に PID を書く）。
    2つ目は、先に動いているものの PID を表示して止まる（部品のキャッシュを消し合う事故を防ぐ）。
  ・別の slug の build が動いているときは、並列数（VP_MAXPAR）を自動で分け合う。"""
import atexit
import contextlib
import ctypes
import os
import time
from pathlib import Path


def alive(pid):
    if pid <= 0:
        return False
    k = ctypes.windll.kernel32
    h = k.OpenProcess(0x1000, False, pid)   # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return False
    code = ctypes.c_ulong()
    ok = k.GetExitCodeProcess(h, ctypes.byref(code))
    k.CloseHandle(h)
    return bool(ok) and code.value == 259   # STILL_ACTIVE


def _read(path):
    try:
        pid, _, cmd = Path(path).read_text(encoding='utf8').partition(' ')
        return int(pid), cmd.strip()
    except Exception:
        return 0, ''


def acquire(root, slug, cmd):
    """鍵を取る。同じ slug の別プロセスが生きていれば、止まる。

    exists() してから write_text() だと、同時起動した2プロセスが両方「取得成功」に
    なる（TOCTOU）。O_CREAT|O_EXCL で原子的に作り、勝った側だけが鍵を持つ。
    """
    d = Path(root) / 'cache'
    d.mkdir(exist_ok=True)
    f = d / f'{slug}.lock'
    for _ in range(2):
        try:
            fd = os.open(f, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        except FileExistsError:
            pid, c = _read(f)
            if pid and pid != os.getpid() and alive(pid):
                raise SystemExit(f'[lock] {slug} は、すでに動いています（PID {pid}: {c}）。二重に起動しません。終わるのを待つか、そのプロセスを止めてください。') from None
            # 死んだプロセスの残骸。消してから一度だけ再挑戦する（消し合っても O_EXCL が最後に判定する）。
            with contextlib.suppress(OSError):
                f.unlink()
            continue
        with os.fdopen(fd, 'w', encoding='utf8') as fh:
            fh.write(f'{os.getpid()} {cmd} {time.strftime("%H:%M:%S")}')
        break
    else:
        raise SystemExit(f'[lock] {slug} のロックを取得できませんでした。少し待って再実行してください。')

    def release():
        try:
            if _read(f)[0] == os.getpid():
                f.unlink()
        except Exception:
            pass
    atexit.register(release)
    return f


def others(root, slug):
    """別の slug で、いま動いている build の数"""
    n = 0
    for f in (Path(root) / 'cache').glob('*.lock'):
        if f.stem == slug:
            continue
        pid, c = _read(f)
        if pid and alive(pid) and c.startswith('build'):
            n += 1
        elif pid and not alive(pid):
            try:
                f.unlink()
            except Exception:
                pass
    return n


def share_maxpar(root, slug, base=8):
    """動いている別の build があれば、並列数を分け合う（NVENC の同時セッション上限のため）"""
    return max(1, base // (others(root, slug) + 1))
