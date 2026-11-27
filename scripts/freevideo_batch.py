"""FreeVideoの背景クリップを、1本ずつ順番に生成する。メモリ不足などで失敗したら、自動で入れ直す(最大3回)。
  python scripts/freevideo_batch.py <prompts.json> <出力フォルダ> [clip2 clip5 ...]   # 名前を指定すると、その分だけ作る
prompts.json: [{"name":"clip1","sec":7,"text":"..."}, ...]。出力: <出力フォルダ>/<name>.mp4
全部できたら 'ALL OK'、できなかったものがあれば 'FAILED: ...' を最後に表示する。サーバー(8188番)が止まっていたら 'SERVER DOWN' で終わる。"""
import json, shutil, sys, time, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import freevideo_api as F


def alive():
    try:
        F._get('/queue'); return True
    except Exception:
        return False


def wait(pid, limit=1800):
    t0 = time.time()
    while time.time() - t0 < limit:
        try:
            h = F._get('/history/' + pid)
        except Exception:
            h = {}
        if pid in h:
            return h[pid].get('status', {}).get('status_str')
        if not alive():
            return 'server_down'
        time.sleep(15)
    return 'timeout'


def main():
    p = json.loads(Path(sys.argv[1]).read_text(encoding='utf8')); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    only = set(sys.argv[3:])
    failed = []
    for it in p:
        n = it['name']
        if only and n not in only:
            continue
        ok = False
        for attempt in range(1, 4):
            if not alive():
                print('SERVER DOWN'); sys.exit(2)
            pid = F.add(it['text'], it.get('sec', 5.0))
            st = wait(pid)
            print(n, 'attempt', attempt, st, flush=True)
            if st == 'success':
                v = F.video_of(F.history(pid)[pid]); shutil.copy(v, out / f'{n}.mp4'); ok = True; break
            if st == 'server_down':
                print('SERVER DOWN'); sys.exit(2)
            time.sleep(20)   # メモリが戻るのを少し待つ
        if not ok:
            failed.append(n)
    print('ALL OK' if not failed else 'FAILED: ' + ' '.join(failed))


if __name__ == '__main__':
    main()
