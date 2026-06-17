#!/usr/bin/env python3
"""Todo UI Probe — development static server.

Serves static files from src/ and provides a /healthz endpoint.
"""

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

HOST = "127.0.0.1"
PORT = 19003
SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))


class TodoHandler(SimpleHTTPRequestHandler):
    """Custom handler: serve static files from src/ + /healthz endpoint."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SRC_DIR, **kwargs)

    def end_headers(self):
        """Add Cache-Control: no-cache for HTML files."""
        if self.path.endswith(".html") or self.path == "/" or not os.path.splitext(self.path)[1]:
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_GET(self):
        """Handle GET: /healthz returns JSON, everything else is static files."""
        if self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))
            return
        super().do_GET()

    def log_message(self, format, *args):
        """Log to stderr with a friendlier format."""
        print(f"[server] {args[0]}", file=sys.stderr)


if __name__ == "__main__":
    print(f"Serving static files from: {SRC_DIR}")
    print(f"Listening on http://{HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), TodoHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()
