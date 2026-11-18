"""
Dialogue and Intent Flow Tests for Virtual Assistant
"""
import unittest
from backend.assistant import handle_chat_message

class TestAssistantDialogue(unittest.TestCase):

    def test_sample_requests(self):
        prompts = [
            ("Run BFS", "run_algorithm", "bfs"),
            ("Solve an 8 puzzle", "run_algorithm", "eight_puzzle"),
            ("Show Towers of Hanoi", "run_algorithm", "hanoi"),
            ("Explain the Hidden Markov Model", "explain_algorithm", "hmm"),
            ("Demonstrate Wumpus World", "run_algorithm", "wumpus"),
            ("Run DFS", "run_algorithm", "dfs"),
            ("Run IDS", "run_algorithm", "ids"),
            ("Run A*", "run_algorithm", "astar"),
            ("Demonstrate D*", "run_algorithm", "dstar"),
            ("Run Hill Climbing", "run_algorithm", "hill_climbing"),
            ("Run Simulated Annealing", "run_algorithm", "simulated_annealing"),
            ("Demonstrate Bayesian Network", "run_algorithm", "bayesian_network"),
            ("Explain Expectation-Maximization", "explain_algorithm", "em")
        ]

        for text, expected_intent, expected_id in prompts:
            res = handle_chat_message(text)
            self.assertEqual(res.get("intent"), expected_intent, f"Failed on '{text}'")
            self.assertEqual(res.get("algorithm_id"), expected_id, f"Failed on '{text}'")

    def test_parameter_extraction(self):
        # Hanoi with custom disks
        res = handle_chat_message("Show Towers of Hanoi with 4 disks")
        self.assertEqual(res.get("intent"), "run_algorithm")
        self.assertEqual(res.get("data", {}).get("n_disks"), 4)

        # Hill climbing starting from index 3
        res = handle_chat_message("Run Hill Climbing from index 3")
        self.assertEqual(res.get("intent"), "run_algorithm")
        self.assertEqual(res.get("data", {}).get("start_index"), 3)

    def test_fallback_polite_response(self):
        res = handle_chat_message("What is the meaning of life?")
        self.assertEqual(res.get("intent"), "unknown")
        self.assertIn("didn't quite understand", res.get("reply"))
        self.assertTrue(len(res.get("suggestions")) > 0)

if __name__ == "__main__":
    unittest.main()

