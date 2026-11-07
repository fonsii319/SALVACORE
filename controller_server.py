import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

PORT = 8000
ACTIONS = ("left", "right", "jump")
_lock = threading.Lock()
_held = {"1": set(), "2": set()}
_opened = {"1": False, "2": False}

PAGE = """<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>Mando SALVACORE</title>
<style>
 body{margin:0;background:#0b0b1e;color:#fff;font-family:sans-serif;height:100vh;
      display:flex;flex-direction:column;user-select:none;-webkit-user-select:none;touch-action:none}
 h1{font-size:20px;text-align:center;margin:12px 0;color:#ffd23c}
 .row{flex:1;display:flex;gap:10px;padding:10px}
 button{flex:1;border:none;border-radius:18px;font-size:40px;color:#fff;background:#2a2a55;box-shadow:0 6px 0 #111}
 button.on{background:#ffb020;transform:translateY(4px);box-shadow:0 2px 0 #111}
 .jump{background:#2f6fd6}
 .jump.on{background:#5ea0ff}
</style></head><body>
<h1 id="t"></h1>
<div class="row">
 <button data-a="left">&#9664;</button>
 <button data-a="jump" class="jump">&#9650;</button>
 <button data-a="right">&#9654;</button>
</div>
<script>
const p = location.pathname === "/p2" ? "2" : "1";
document.getElementById("t").textContent = p === "1" ? "Blanqui (jugador 1)" : "Darky (jugador 2)";
function send(a, s) {
  fetch("/input?p=" + p + "&a=" + a + "&s=" + s, {method: "POST", keepalive: true}).catch(function(){});
}
document.querySelectorAll("button").forEach(function(b) {
  const a = b.dataset.a;
  const down = function(e) { e.preventDefault(); b.classList.add("on"); send(a, 1); };
  const up = function(e) { e.preventDefault(); b.classList.remove("on"); send(a, 0); };
  b.addEventListener("pointerdown", down);
  b.addEventListener("pointerup", up);
  b.addEventListener("pointercancel", up);
  b.addEventListener("pointerleave", up);
});
</script></body></html>
"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/p1", "/p2"):
            with _lock:
                _opened[path[-1]] = True
            body = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        url = urlparse(self.path)
        if url.path == "/input":
            q = parse_qs(url.query)
            p = q.get("p", [""])[0]
            a = q.get("a", [""])[0]
            pressed = q.get("s", ["0"])[0] == "1"
            if p in _held and a in ACTIONS:
                with _lock:
                    if pressed:
                        _held[p].add(a)
                    else:
                        _held[p].discard(a)
        self.send_response(204)
        self.end_headers()


def start_server(port=PORT):
    srv = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def get_input(p):
    with _lock:
        return set(_held[p])


def connected(p):
    with _lock:
        return _opened[p]


def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()
        