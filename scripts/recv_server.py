"""ブラウザ（ChatGPTのweb）で作った画像を、ローカルに受け取る小さなサーバー（127.0.0.1:8766）。
POST /<slug>/<name>  本文=画像のバイト列 → assets/<slug>/art_<name>.png に保存（slug・nameは英数字と_のみ）。"""
import http.server, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class H(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*'); self.send_header('Access-Control-Allow-Private-Network', 'true')
        self.send_header('Access-Control-Allow-Methods', 'POST'); self.send_header('Access-Control-Allow-Headers', '*')
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_POST(self):
        m = re.fullmatch(r'/([a-z0-9_]+)/([a-z0-9_]+)', self.path)
        if not m:
            self.send_response(400); self._cors(); self.end_headers(); return
        n = int(self.headers.get('Content-Length', 0)); b = self.rfile.read(n)
        p = ROOT / 'assets' / m.group(1) / f'art_{m.group(2)}.png'
        p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b)
        self.send_response(200); self._cors(); self.end_headers(); self.wfile.write(str(len(b)).encode())
http.server.ThreadingHTTPServer(('127.0.0.1', 8766), H).serve_forever()
