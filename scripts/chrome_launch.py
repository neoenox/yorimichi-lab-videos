"""専用プロファイルのChromeを、最小化した状態で起動する共通部品(2026-11-19 ユーザー指示:「chromeを立ち上げるときは最小化して開いて」)。

使い方:
    from chrome_launch import launch_minimized
    proc = launch_minimized(CHROME, port, profile, url)      # Popen を返す
    # 呼び出し側は、これまでどおり port_open() で待ち、atexit で taskkill する

やっていること:
  1. --start-minimized で起動する(Windowsでは効かないことがある)
  2. 起動したプロセスのウィンドウを、Win32 の ShowWindow(SW_SHOWMINNOACTIVE) で最小化する
     (フォーカスを奪わない。あなたの作業中の窓の前に出ない)
  3. 最小化に失敗しても、動画の確認・投稿そのものは続けられる(警告を出すだけ)

注意: 最小化したウィンドウは、実クリック/実キー入力が効かない場合がある(Playwrightが
DOMへ直接送る操作は通る)。ログインなど手で操作してもらうときは、restore_window() で戻す。
"""
import ctypes
import subprocess
import sys
import time

SW_SHOWMINNOACTIVE = 7
SW_RESTORE = 9


def _windows_of_pid(pid):
    """pid(とその子孫)が所有する可視トップレベルウィンドウのハンドルを返す。"""
    user32 = ctypes.windll.user32
    pids = {pid}
    # 子プロセス(ChromeはGPU/レンダラ等を分ける)も対象にする
    try:
        out = subprocess.run(
            ['powershell', '-NoProfile', '-Command',
             f'Get-CimInstance Win32_Process | Where-Object {{ $_.ParentProcessId -eq {pid} }} | Select-Object -ExpandProperty ProcessId'],
            capture_output=True, text=True, timeout=10).stdout.split()
        pids |= {int(x) for x in out if x.isdigit()}
    except Exception:
        pass
    found = []
    EnumProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

    def cb(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        p = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
        if p.value in pids:
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:   # タイトルのある本体ウィンドウだけ
                found.append(hwnd)
        return True

    user32.EnumWindows(EnumProc(cb), 0)
    return found


def minimize_pid(pid, wait=12):
    """起動直後のウィンドウが現れるのを待って最小化する。最小化できた数を返す。"""
    user32 = ctypes.windll.user32
    t0 = time.time()
    done = set()
    while time.time() - t0 < wait:
        for h in _windows_of_pid(pid):
            if h not in done:
                user32.ShowWindow(h, SW_SHOWMINNOACTIVE)
                done.add(h)
        if done:
            time.sleep(1.0)   # 遅れて現れる窓(復元ダイアログ等)も拾う
            for h in _windows_of_pid(pid):
                if h not in done:
                    user32.ShowWindow(h, SW_SHOWMINNOACTIVE)
                    done.add(h)
            break
        time.sleep(0.4)
    return len(done)


def launch_minimized(chrome, port, profile, url, extra_args=None):
    """最小化して起動し、Popen を返す。待機(port_open)は呼び出し側で行う。"""
    args = [chrome, f'--remote-debugging-port={port}', f'--user-data-dir={profile}',
            '--start-minimized', '--no-first-run', '--no-default-browser-check']
    args += list(extra_args or [])
    args.append(url)
    # STARTUPINFO でも最小化(SW_SHOWMINNOACTIVE)を指定する
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = SW_SHOWMINNOACTIVE
    proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=si)
    try:
        n = minimize_pid(proc.pid)
        if not n:
            print('警告: Chromeのウィンドウを最小化できなかった(起動は成功)', file=sys.stderr)
    except Exception as e:   # 最小化の失敗で本来の作業を止めない
        print('警告: 最小化に失敗:', e, file=sys.stderr)
    return proc


def restore_window(pid):
    """ログインなど手操作が要るとき、窓を元に戻して前面に出す。"""
    user32 = ctypes.windll.user32
    n = 0
    for h in _windows_of_pid(pid):
        user32.ShowWindow(h, SW_RESTORE)
        user32.SetForegroundWindow(h)
        n += 1
    return n


if __name__ == '__main__':
    # 動作確認: python scripts/chrome_launch.py <port> <profile> <url>
    import os
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    port, profile, url = int(sys.argv[1]), sys.argv[2], sys.argv[3]
    p = launch_minimized(chrome, port, profile, url)
    print('pid', p.pid, '| 窓:', len(_windows_of_pid(p.pid)))
    time.sleep(3)
    print('終了します')
    subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True)
