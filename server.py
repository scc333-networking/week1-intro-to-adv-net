import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn


class _ConnectionInfoHandler(BaseHTTPRequestHandler):
    """Serves a simple HTML page describing the connection endpoints."""

    def do_GET(self) -> None:
        client_ip, client_port = self.client_address
        server_ip, server_port = self.server.server_address

        html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Connection Info</title>
  <style>
    body {{ font-family: sans-serif; margin: 2rem; }}
    h1 {{ margin-bottom: 1rem; }}
    ul {{ list-style: none; padding: 0; }}
    li {{ margin: 0.25rem 0; }}
    code {{ background: #f2f2f2; padding: 0.1rem 0.3rem; }}
  </style>
</head>
<body>
  <h1>HTTP Connection Details</h1>
  <ul>
    <li>Source: <code>{client_ip}:{client_port}</code></li>
    <li>Destination: <code>{server_ip}:{server_port}</code></li>
  </ul>
</body>
</html>"""

        encoded = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_HEAD(self) -> None:
        client_ip, client_port = self.client_address
        server_ip, server_port = self.server.server_address
        # Respond with headers only for HEAD.
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, format: str, *args) -> None:
        # Keep server output tidy by using standard print.
        print(f"{self.address_string()} - - {format % args}")


class _ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


def serve(host: str = "0.0.0.0", port: int = 80) -> None:
    server = _ThreadedHTTPServer((host, port), _ConnectionInfoHandler)
    print(f"Serving on http://{host}:{port} (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple HTTP server returning connection endpoints")
    parser.add_argument("--host", default="0.0.0.0", help="Host/interface to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=80, help="Port to bind (default: 80)")
    args = parser.parse_args()
    serve(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
