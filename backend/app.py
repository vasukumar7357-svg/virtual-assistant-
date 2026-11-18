"""
HTTP Server and REST API for AI Virtual Assistant
Built using Python Standard Library (Zero external dependencies).
"""
import os
import json
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from backend.assistant import handle_chat_message
from algorithms.registry import get_all_algorithms, run_algorithm

# Base directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

class AssistantRequestHandler(BaseHTTPRequestHandler):
    """Handles HTTP requests for chat API, algorithm runner, and frontend static assets."""

    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        """Handle CORS pre-flight requests."""
        self._set_headers(200)

    def _read_json_body(self):
        """Safely parses JSON request body."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0:
                return None, "Empty request body"
            raw_body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(raw_body)
            return data, None
        except (ValueError, json.JSONDecodeError) as e:
            return None, f"Invalid JSON payload: {str(e)}"

    def do_GET(self):
        """Handles GET endpoints."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # 1. Health check endpoint
        if path == "/api/health":
            self._set_headers(200)
            response = {
                "status": "ok",
                "app": "AI Virtual Assistant",
                "version": "1.0.0"
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        # 2. List algorithms endpoint
        if path == "/api/algorithms":
            self._set_headers(200)
            catalog = get_all_algorithms()
            response = {
                "count": len(catalog),
                "algorithms": catalog
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        # 3. Serve Frontend Static Files
        self._serve_static_file(path)

    def do_POST(self):
        """Handles POST endpoints."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # 1. Chat API: POST /api/chat
        if path == "/api/chat":
            body, err = self._read_json_body()
            if err:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": err}).encode("utf-8"))
                return

            message = body.get("message", "")
            if not isinstance(message, str):
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Field 'message' must be a string."}).encode("utf-8"))
                return

            # Process through the Assistant Dialogue Engine
            assistant_response = handle_chat_message(message)
            self._set_headers(200)
            self.wfile.write(json.dumps(assistant_response).encode("utf-8"))
            return

        # 2. Algorithm Runner API: POST /api/algorithms/run
        if path == "/api/algorithms/run":
            body, err = self._read_json_body()
            if err:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": err}).encode("utf-8"))
                return

            algo_id = body.get("algorithm")
            if not algo_id or not isinstance(algo_id, str):
                self._set_headers(400)
                self.wfile.write(json.dumps({
                    "error": "Field 'algorithm' is required and must be a string."
                }).encode("utf-8"))
                return

            params = body.get("params", {})
            if not isinstance(params, dict):
                self._set_headers(400)
                self.wfile.write(json.dumps({
                    "error": "Field 'params' must be a dictionary/object if provided."
                }).encode("utf-8"))
                return

            result = run_algorithm(algo_id, params)
            if "error" in result:
                self._set_headers(400)
                self.wfile.write(json.dumps(result).encode("utf-8"))
                return

            self._set_headers(200)
            self.wfile.write(json.dumps(result).encode("utf-8"))
            return

        # Unknown route
        self._set_headers(404)
        self.wfile.write(json.dumps({"error": f"Endpoint '{path}' not found."}).encode("utf-8"))

    def _serve_static_file(self, req_path):
        """Serves HTML, CSS, JS, and asset files from the frontend directory."""
        if req_path in ["", "/"]:
            filename = "index.html"
        else:
            filename = req_path.lstrip("/")

        file_path = os.path.join(FRONTEND_DIR, filename)

        # Basic path traversal prevention
        if not os.path.abspath(file_path).startswith(FRONTEND_DIR):
            self._set_headers(403, "text/plain")
            self.wfile.write(b"403 Forbidden")
            return

        if not os.path.isfile(file_path):
            self._set_headers(404, "text/plain")
            self.wfile.write(b"404 File Not Found")
            return

        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = "application/octet-stream"
        if content_type.startswith("text/") or content_type == "application/javascript":
            content_type += "; charset=utf-8"

        self._set_headers(200, content_type)
        with open(file_path, "rb") as f:
            self.wfile.write(f.read())

    def log_message(self, format, *args):
        """Clean custom logging for academic presentation."""
        # Suppress routine 200 GET static asset spam in terminal
        if "GET /api/" in format % args or "POST /api/" in format % args:
            print(f"[API Log] {format % args}")

def run_server(port=8000, host="127.0.0.1"):
    """Starts the HTTP server."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, AssistantRequestHandler)
    print(f"==================================================")
    print(f"  AI Virtual Assistant - Academic Project")
    print(f"  Server listening on: http://{host}:{port}/")
    print(f"  Open in your browser to interact with the assistant!")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

