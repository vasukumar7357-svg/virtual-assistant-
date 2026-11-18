"""
API Tests for AI Virtual Assistant HTTP endpoints.
"""
import unittest
import json
import io
from backend.app import AssistantRequestHandler

class DummyRequest:
    def __init__(self, body_bytes=b""):
        self._body = io.BytesIO(body_bytes)

    def makefile(self, *args, **kwargs):
        return self._body

class TestAssistantAPI(unittest.TestCase):

    def _simulate_request(self, method, path, body=None):
        """Helper to simulate HTTP request and capture response."""
        body_bytes = json.dumps(body).encode("utf-8") if body is not None else b""
        
        # Create a mock socket-like object
        mock_rfile = io.BytesIO(body_bytes)
        mock_wfile = io.BytesIO()

        # Initialize mock handler
        handler = AssistantRequestHandler.__new__(AssistantRequestHandler)
        handler.rfile = mock_rfile
        handler.wfile = mock_wfile
        handler.path = path
        handler.command = method
        handler.headers = {
            "Content-Length": str(len(body_bytes)),
            "Content-Type": "application/json"
        }
        handler.close_connection = True

        status_code = [200]
        headers_sent = {}

        def mock_send_response(code, message=None):
            status_code[0] = code
        def mock_send_header(k, v):
            headers_sent[k] = v
        def mock_end_headers():
            pass

        handler.send_response = mock_send_response
        handler.send_header = mock_send_header
        handler.end_headers = mock_end_headers

        if method == "GET":
            handler.do_GET()
        elif method == "POST":
            handler.do_POST()

        raw_output = mock_wfile.getvalue().decode("utf-8")
        try:
            parsed_json = json.loads(raw_output)
        except json.JSONDecodeError:
            parsed_json = raw_output

        return status_code[0], headers_sent, parsed_json

    def test_health_endpoint(self):
        code, headers, data = self._simulate_request("GET", "/api/health")
        self.assertEqual(code, 200)
        self.assertEqual(data.get("status"), "ok")

    def test_algorithms_catalog(self):
        code, headers, data = self._simulate_request("GET", "/api/algorithms")
        self.assertEqual(code, 200)
        self.assertEqual(data.get("count"), 13)
        self.assertEqual(len(data.get("algorithms")), 13)

    def test_chat_greeting(self):
        code, headers, data = self._simulate_request("POST", "/api/chat", {"message": "Hello!"})
        self.assertEqual(code, 200)
        self.assertEqual(data.get("intent"), "greeting")
        self.assertIn("AI Virtual Assistant", data.get("reply"))

    def test_chat_run_bfs(self):
        code, headers, data = self._simulate_request("POST", "/api/chat", {"message": "Run BFS"})
        self.assertEqual(code, 200)
        self.assertEqual(data.get("intent"), "run_algorithm")
        self.assertEqual(data.get("algorithm_id"), "bfs")
        self.assertIn("Breadth-First Search", data.get("reply"))

    def test_chat_explain_hmm(self):
        code, headers, data = self._simulate_request("POST", "/api/chat", {"message": "Explain the Hidden Markov Model"})
        self.assertEqual(code, 200)
        self.assertEqual(data.get("intent"), "explain_algorithm")
        self.assertEqual(data.get("algorithm_id"), "hmm")

    def test_chat_unknown_input(self):
        code, headers, data = self._simulate_request("POST", "/api/chat", {"message": "Can you order pizza?"})
        self.assertEqual(code, 200)
        self.assertEqual(data.get("intent"), "unknown")
        self.assertIn("didn't quite understand", data.get("reply"))

    def test_direct_algorithm_run(self):
        code, headers, data = self._simulate_request("POST", "/api/algorithms/run", {
            "algorithm": "eight_puzzle",
            "params": {}
        })
        self.assertEqual(code, 200)
        self.assertEqual(data.get("algorithm"), "8-Puzzle Solver")

    def test_invalid_algorithm_run(self):
        code, headers, data = self._simulate_request("POST", "/api/algorithms/run", {
            "algorithm": "non_existent"
        })
        self.assertEqual(code, 400)
        self.assertIn("error", data)

    def test_static_file_serving(self):
        code, headers, data = self._simulate_request("GET", "/")
        self.assertEqual(code, 200)
        self.assertIn("text/html", headers.get("Content-Type", ""))
        self.assertIn("AI Virtual Assistant", data)

    def test_static_css_serving(self):
        code, headers, data = self._simulate_request("GET", "/style.css")
        self.assertEqual(code, 200)
        self.assertIn("text/css", headers.get("Content-Type", ""))
        self.assertIn("chat-container", data)

    def test_static_js_serving(self):
        code, headers, data = self._simulate_request("GET", "/app.js")
        self.assertEqual(code, 200)
        self.assertIn("javascript", headers.get("Content-Type", ""))
        self.assertIn("DOMContentLoaded", data)


if __name__ == "__main__":
    unittest.main()
