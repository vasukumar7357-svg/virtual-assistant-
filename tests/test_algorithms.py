"""
Unit tests for AI Virtual Assistant Algorithms
Validates search algorithms, AI problems, and probabilistic models.
"""
import unittest
from algorithms.registry import ALGORITHMS, run_algorithm, get_all_algorithms

class TestAIAlgorithms(unittest.TestCase):

    def test_all_13_algorithms_registered(self):
        self.assertEqual(len(ALGORITHMS), 13)
        expected_keys = [
            "dfs", "bfs", "ids", "astar", "dstar", "hill_climbing", "simulated_annealing",
            "wumpus", "eight_puzzle", "hanoi",
            "bayesian_network", "em", "hmm"
        ]
        for key in expected_keys:
            self.assertIn(key, ALGORITHMS)

    def test_dfs(self):
        res = run_algorithm("dfs", {"start": "A", "goal": "G"})
        self.assertTrue(res.get("found"))
        self.assertIn("G", res.get("path"))
        self.assertIn("Depth-First Search", res.get("formatted_text"))

    def test_bfs(self):
        res = run_algorithm("bfs", {"start": "A", "goal": "G"})
        self.assertTrue(res.get("found"))
        self.assertEqual(res.get("path")[0], "A")
        self.assertEqual(res.get("path")[-1], "G")

    def test_ids(self):
        res = run_algorithm("ids", {"start": "A", "goal": "G", "max_depth": 4})
        self.assertTrue(res.get("found"))
        self.assertGreater(len(res.get("iterations")), 0)

    def test_astar(self):
        res = run_algorithm("astar", {"start": "S", "goal": "G"})
        self.assertEqual(res.get("path")[0], "S")
        self.assertEqual(res.get("path")[-1], "G")
        self.assertGreater(res.get("total_cost"), 0)

    def test_dstar(self):
        res = run_algorithm("dstar", {"start": "S", "goal": "G"})
        self.assertIsNotNone(res.get("initial_path"))
        self.assertIsNotNone(res.get("replan_path"))

    def test_hill_climbing(self):
        res = run_algorithm("hill_climbing", {"start_index": 1})
        self.assertIn("final_index", res)
        self.assertIn("trajectory", res)

    def test_simulated_annealing(self):
        res = run_algorithm("simulated_annealing", {"start_index": 1})
        self.assertIn("best_value", res)
        self.assertIn("history", res)

    def test_wumpus(self):
        res = run_algorithm("wumpus")
        self.assertIn("log", res)
        self.assertGreater(len(res.get("log")), 0)

    def test_eight_puzzle(self):
        res = run_algorithm("eight_puzzle")
        self.assertIn("move_sequence", res)
        self.assertGreater(res.get("total_moves"), 0)

    def test_hanoi(self):
        res = run_algorithm("hanoi", {"n_disks": 3})
        self.assertEqual(res.get("total_moves"), 7)
        self.assertEqual(len(res.get("moves")), 8)  # initial state + 7 moves

    def test_bayesian_network(self):
        res = run_algorithm("bayesian_network")
        self.assertIn("posteriors", res)
        self.assertIn("P(Rain=True|Wet)", res.get("posteriors"))

    def test_em(self):
        res = run_algorithm("em", {"iterations": 3})
        self.assertIn("final_parameters", res)
        self.assertIn("theta_A", res.get("final_parameters"))

    def test_hmm(self):
        res = run_algorithm("hmm")
        self.assertIn("most_likely_hidden_path", res)
        self.assertGreater(res.get("observation_probability"), 0.0)

    def test_invalid_algorithm_error_handling(self):
        res = run_algorithm("non_existent_algo")
        self.assertIn("error", res)

if __name__ == "__main__":
    unittest.main()

