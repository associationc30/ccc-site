#!/usr/bin/env python3
"""預覽用靜態伺服器：關閉快取，避免重建後瀏覽器仍抓舊的 fingerprint 檔名。"""
import functools
import http.server
import os
import socketserver
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 1319
ROOT = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else ".")


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        pass


socketserver.TCPServer.allow_reuse_address = True
handler = functools.partial(Handler, directory=ROOT)
with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
    print(f"serving {ROOT} on http://127.0.0.1:{PORT}/ (no-cache)", flush=True)
    httpd.serve_forever()
