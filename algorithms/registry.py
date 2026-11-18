"""
Central Registry for all AI Algorithms and Problems
Provides metadata, descriptions, parameter specifications, and execution functions.
"""
from algorithms.search.dfs import dfs
from algorithms.search.bfs import bfs
from algorithms.search.ids import ids
from algorithms.search.astar import astar
from algorithms.search.dstar import dstar
from algorithms.search.hill_climbing import hill_climbing
from algorithms.search.simulated_annealing import simulated_annealing
from algorithms.problems.wumpus import wumpus
from algorithms.problems.eight_puzzle import solve_8_puzzle
from algorithms.problems.hanoi import solve_hanoi
from algorithms.probabilistic.bayesian_network import bayesian_network_demo
from algorithms.probabilistic.em import expectation_maximization
from algorithms.probabilistic.hmm import run_hmm_demo

ALGORITHMS = {
    "dfs": {
        "id": "dfs",
        "name": "Depth-First Search (DFS)",
        "category": "Search algorithms",
        "keywords": ["dfs", "depth first", "depth-first search"],
        "description": "Explores as deep as possible along each branch before backtracking using a LIFO stack.",
        "sample_query": "Run DFS",
        "parameters": {
            "start": {"type": "string", "default": "A", "description": "Start node (A-G)"},
            "goal": {"type": "string", "default": "G", "description": "Goal node (A-G)"}
        },
        "runner": lambda params: dfs(
            start=params.get("start", "A"),
            goal=params.get("goal", "G")
        )
    },
    "bfs": {
        "id": "bfs",
        "name": "Breadth-First Search (BFS)",
        "category": "Search algorithms",
        "keywords": ["bfs", "breadth first", "breadth-first search"],
        "description": "Explores neighbor nodes level-by-level using a FIFO queue. Finds shortest path in unweighted graphs.",
        "sample_query": "Run BFS",
        "parameters": {
            "start": {"type": "string", "default": "A", "description": "Start node (A-G)"},
            "goal": {"type": "string", "default": "G", "description": "Goal node (A-G)"}
        },
        "runner": lambda params: bfs(
            start=params.get("start", "A"),
            goal=params.get("goal", "G")
        )
    },
    "ids": {
        "id": "ids",
        "name": "Iterative Deepening Search (IDS)",
        "category": "Search algorithms",
        "keywords": ["ids", "iddfs", "iterative deepening", "iterative deepening search"],
        "description": "Repeatedly executes depth-limited search with increasing depth limits. Combines BFS optimality with DFS space efficiency.",
        "sample_query": "Run Iterative Deepening Search",
        "parameters": {
            "start": {"type": "string", "default": "A", "description": "Start node (A-G)"},
            "goal": {"type": "string", "default": "G", "description": "Goal node (A-G)"},
            "max_depth": {"type": "int", "default": 5, "description": "Maximum depth limit"}
        },
        "runner": lambda params: ids(
            start=params.get("start", "A"),
            goal=params.get("goal", "G"),
            max_depth=int(params.get("max_depth", 5))
        )
    },
    "astar": {
        "id": "astar",
        "name": "A* (A-Star) Search",
        "category": "Search algorithms",
        "keywords": ["a*", "astar", "a star", "a-star"],
        "description": "Informed heuristic search using f(n) = g(n) + h(n) to find the lowest-cost path.",
        "sample_query": "Run A*",
        "parameters": {
            "start": {"type": "string", "default": "S", "description": "Start node (S, A, B, C, D)"},
            "goal": {"type": "string", "default": "G", "description": "Goal node (G)"}
        },
        "runner": lambda params: astar(
            start=params.get("start", "S"),
            goal=params.get("goal", "G")
        )
    },
    "dstar": {
        "id": "dstar",
        "name": "D* (Dynamic A*)",
        "category": "Search algorithms",
        "keywords": ["d*", "dstar", "d star", "d-star", "dynamic a*"],
        "description": "Dynamic replanning algorithm that repairs paths when obstacles or edge costs change at runtime without restarting search.",
        "sample_query": "Demonstrate D*",
        "parameters": {
            "start": {"type": "string", "default": "S", "description": "Start node"},
            "goal": {"type": "string", "default": "G", "description": "Goal node"}
        },
        "runner": lambda params: dstar(
            start=params.get("start", "S"),
            goal=params.get("goal", "G")
        )
    },
    "hill_climbing": {
        "id": "hill_climbing",
        "name": "Hill Climbing",
        "category": "Search algorithms",
        "keywords": ["hill climbing", "hill-climbing", "hill climb", "local search"],
        "description": "Greedy local search moving towards higher elevation. Fast and simple, but vulnerable to local maxima and ridges.",
        "sample_query": "Run Hill Climbing",
        "parameters": {
            "start_index": {"type": "int", "default": 1, "description": "Start index in landscape (0 to 14)"}
        },
        "runner": lambda params: hill_climbing(
            start_index=int(params.get("start_index", 1))
        )
    },
    "simulated_annealing": {
        "id": "simulated_annealing",
        "name": "Simulated Annealing",
        "category": "Search algorithms",
        "keywords": ["simulated annealing", "annealing", "temperature cooling"],
        "description": "Probabilistic local search that accepts downhill moves with probability P = exp(ΔE/T) to escape local optima.",
        "sample_query": "Run Simulated Annealing",
        "parameters": {
            "start_index": {"type": "int", "default": 1, "description": "Start index in landscape (0 to 14)"},
            "initial_temp": {"type": "float", "default": 100.0, "description": "Starting temperature"},
            "cooling_rate": {"type": "float", "default": 0.85, "description": "Cooling factor alpha"}
        },
        "runner": lambda params: simulated_annealing(
            start_index=int(params.get("start_index", 1)),
            initial_temp=float(params.get("initial_temp", 100.0)),
            cooling_rate=float(params.get("cooling_rate", 0.85))
        )
    },
    "wumpus": {
        "id": "wumpus",
        "name": "Wumpus World",
        "category": "AI problems",
        "keywords": ["wumpus", "wumpus world", "hunt the wumpus", "stench", "breeze"],
        "description": "Knowledge-based agent reasoning with propositional logic in a partially observable cave with pits, a monster, and gold.",
        "sample_query": "Demonstrate Wumpus World",
        "parameters": {},
        "runner": lambda params: wumpus()
    },
    "eight_puzzle": {
        "id": "eight_puzzle",
        "name": "8-Puzzle",
        "category": "AI problems",
        "keywords": ["8 puzzle", "8-puzzle", "eight puzzle", "sliding puzzle", "tile puzzle"],
        "description": "Sliding tile puzzle solved optimally using A* search guided by the Manhattan Distance heuristic.",
        "sample_query": "Solve an 8 puzzle",
        "parameters": {},
        "runner": lambda params: solve_8_puzzle()
    },
    "hanoi": {
        "id": "hanoi",
        "name": "Towers of Hanoi",
        "category": "AI problems",
        "keywords": ["hanoi", "towers of hanoi", "tower of hanoi"],
        "description": "Classic divide-and-conquer recursive puzzle moving N disks across pegs in 2^N - 1 moves.",
        "sample_query": "Show Towers of Hanoi",
        "parameters": {
            "n_disks": {"type": "int", "default": 3, "description": "Number of disks (1 to 7)"}
        },
        "runner": lambda params: solve_hanoi(
            n_disks=int(params.get("n_disks", 3))
        )
    },
    "bayesian_network": {
        "id": "bayesian_network",
        "name": "Bayesian Network",
        "category": "Probabilistic AI",
        "keywords": ["bayesian", "bayes network", "bayesian network", "belief network", "cpt", "wet grass"],
        "description": "Directed acyclic probabilistic graphical model showing exact inference and Bayes' rule with conditional probability tables.",
        "sample_query": "Demonstrate Bayesian Network",
        "parameters": {
            "evidence_grass_wet": {"type": "bool", "default": True, "description": "Observed evidence: grass is wet"}
        },
        "runner": lambda params: bayesian_network_demo(
            evidence_grass_wet=bool(params.get("evidence_grass_wet", True))
        )
    },
    "em": {
        "id": "em",
        "name": "Expectation-Maximization (EM)",
        "category": "Probabilistic AI",
        "keywords": ["em", "expectation maximization", "expectation-maximization", "latent variable", "two coin"],
        "description": "Iterative optimization finding maximum likelihood parameter estimates in models with hidden/latent variables.",
        "sample_query": "Explain Expectation-Maximization",
        "parameters": {
            "iterations": {"type": "int", "default": 4, "description": "Number of EM iterations"}
        },
        "runner": lambda params: expectation_maximization(
            num_iterations=int(params.get("iterations", 4))
        )
    },
    "hmm": {
        "id": "hmm",
        "name": "Hidden Markov Model (HMM)",
        "category": "Probabilistic AI",
        "keywords": ["hmm", "hidden markov", "hidden markov model", "viterbi", "forward algorithm"],
        "description": "Probabilistic sequence model with hidden states. Demonstrates Forward evaluation and Viterbi dynamic programming decoding.",
        "sample_query": "Explain the Hidden Markov Model",
        "parameters": {},
        "runner": lambda params: run_hmm_demo()
    }
}

def get_all_algorithms():
    """Returns a simplified list of all algorithms for API catalog."""
    return [
        {
            "id": meta["id"],
            "name": meta["name"],
            "category": meta["category"],
            "description": meta["description"],
            "sample_query": meta["sample_query"],
            "parameters": meta["parameters"]
        }
        for meta in ALGORITHMS.values()
    ]

def run_algorithm(algo_id, params=None):
    """Executes the specified algorithm by ID with parameters."""
    if params is None:
        params = {}
    
    algo_key = algo_id.lower().replace("-", "_").replace(" ", "_")
    if algo_key not in ALGORITHMS:
        # Try matching by id
        found_key = None
        for k, v in ALGORITHMS.items():
            if v["id"] == algo_key:
                found_key = k
                break
        if not found_key:
            return {
                "error": f"Algorithm '{algo_id}' not found. Supported algorithms: {', '.join(ALGORITHMS.keys())}"
            }
        algo_key = found_key

    try:
        result = ALGORITHMS[algo_key]["runner"](params)
        return result
    except Exception as e:
        return {"error": f"Execution error in {algo_key}: {str(e)}"}

