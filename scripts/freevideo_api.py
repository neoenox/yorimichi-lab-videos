"""FreeVideo(ローカルComfyUI, 127.0.0.1:8188)をHTTP APIで操作する。画面操作は不要。
  python scripts/freevideo_api.py status                      # 実行中・待ち行列
  python scripts/freevideo_api.py add "prompt" [--sec 5] [--w 544] [--h 960]   # 生成を待ち行列に追加→prompt_idを表示
  python scripts/freevideo_api.py add-file prompts.json        # [{"name":"clip1","text":"..."},…] をまとめて追加。name→prompt_idを assets側の jobs.json に保存
  python scripts/freevideo_api.py outputs                      # 完了した出力mp4（新しい順）
  python scripts/freevideo_api.py fetch <prompt_id> <dest.mp4>  # 完了した動画を取り出す
  python scripts/freevideo_api.py cancel <prompt_id>           # 待ち行列から外す
サーバーはFreeVideoのランチャーで「Launch FreeVideo」を押して起動しておく（8188番が応答すること）。
グラフは画面と同じ2ノード(FreeVideoGenerate + FreeVideoMedia)。設定の既定は縦544x960・5秒・two_pass・8+3ステップ（画面の「Light」相当）。"""
import json, random, shutil, sys, time, urllib.request, uuid
from pathlib import Path
BASE = 'http://127.0.0.1:8188'
OUTROOT = Path('E:/FreeVideo/runtime/ComfyUI/output')


def _get(path):
    return json.load(urllib.request.urlopen(BASE + path, timeout=10))


def _post(path, body):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
    raw = urllib.request.urlopen(req, timeout=30).read()
    return json.loads(raw) if raw.strip() else {}


def graph(text, sec=5.0, w=544, h=960, seed=None):
    return {'1': {'class_type': 'FreeVideoGenerate', 'inputs': dict(
        text=text, width=w, height=h, seconds=float(sec), seed=seed if seed is not None else random.randint(1, 2 ** 48), two_pass=True, base_steps=8, refine_steps=3,
        force_regenerate=False, preview=False, refine_from='', continue_from='', frames=0, first_frame_reference=False, voice_reference=False, hide_tail=False,
        step_cache='none', upscale_factor='2', allow_empty_prompt=False, media=['2', 0])},
        '2': {'class_type': 'FreeVideoMedia', 'inputs': {'assets': '[]', 'audio_use': 'reference'}}}


def add(text, sec=5.0, w=544, h=960, seed=None):
    r = _post('/prompt', {'prompt': graph(text, sec, w, h, seed), 'client_id': str(uuid.uuid4())})
    return r['prompt_id']


def status():
    q = _get('/queue')
    return q['queue_running'], q['queue_pending']


def history(pid=None):
    return _get('/history' + (f'/{pid}' if pid else '?max_items=50'))


def video_of(entry):
    for n in entry.get('outputs', {}).values():
        for i in n.get('images', []):
            return OUTROOT / i['subfolder'] / i['filename']
    return None


def main():
    a = sys.argv[1:]
    if not a: print(__doc__); return
    c = a[0]
    if c == 'status':
        run, pend = status(); print('running', len(run), 'pending', len(pend))
        for p in run + pend: print(' ', p[1][:8], json.dumps(p[2]['1']['inputs']['text'], ensure_ascii=False)[:70])
    elif c == 'add':
        opt = {k: a[i + 1] for i, k in enumerate(a) if k in ('--sec', '--w', '--h')}
        print(add(a[1], float(opt.get('--sec', 5)), int(opt.get('--w', 544)), int(opt.get('--h', 960))))
    elif c == 'add-file':
        items = json.loads(Path(a[1]).read_text(encoding='utf8')); jobs = {}
        for it in items: jobs[it['name']] = add(it['text'], it.get('sec', 5.0)); print(it['name'], jobs[it['name']])
        Path(a[1]).with_suffix('.jobs.json').write_text(json.dumps(jobs, ensure_ascii=False, indent=1), encoding='utf8')
    elif c == 'outputs':
        for k, v in history().items():
            p = video_of(v); print(k[:8], v.get('status', {}).get('status_str'), p)
    elif c == 'fetch':
        p = video_of(history(a[1])[a[1]]); assert p and p.exists(), '未完了か出力なし'; shutil.copy(p, a[2]); print('saved', a[2])
    elif c == 'cancel':
        print(_post('/queue', {'delete': [a[1]]}))


if __name__ == '__main__':
    main()
