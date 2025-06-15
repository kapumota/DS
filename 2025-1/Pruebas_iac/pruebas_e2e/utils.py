"""
Utilidades para simular despliegue y servidor HTTP local.
"""
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

_service = None
_thread = None
_service_url = None

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Esta corriendo!")
    def log_message(self, format, *args):
        pass
        
def initialize() -> int:
    # No se requiere inicialización externa
    return 0

def apply() -> tuple[int, str, bytes]:
    global _service, _thread, _service_url
    # Selecciona puerto libre
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    _service = HTTPServer(('localhost', port), Handler)
    _thread = threading.Thread(target=_service.serve_forever, daemon=True)
    _thread.start()
    _service_url = f"http://localhost:{port}"
    # Simula salida de despliegue con URL
    return 0, _service_url, b''

def output(var_name: str) -> tuple[bytes, bytes]:
    if var_name == 'url' and _service_url:
        return _service_url.encode(), b''
    return b'', b'Variable no encontrada'

def destroy() -> int:
    global _service
    if _service:
        _service.shutdown()
        _service = None
    return 0
