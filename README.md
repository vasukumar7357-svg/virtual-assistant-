# AI Virtual Assistant — Academic Project

A simple, beginner-friendly **chat virtual assistant** built as an academic computer science project. The assistant provides an interactive chat interface to learn, explain, and run step-by-step demonstrations of classical **Search Algorithms**, **AI Problems**, and **Probabilistic Models**.

> **Note on Architecture:** This assistant is built using a transparent, rule-based dialogue engine in standard Python—not a black-box large language model (LLM). This design ensures that every algorithm step, calculation, and decision path is 100% deterministic, inspectable, and easy for students to understand.

---

## 🎯 Project Goals

- Provide a clean, practical chat interface where students can ask questions or select topics.
- Demonstrate **13 fundamental AI algorithms and problems** with concise explanations and formatted step-by-step output.
- Keep the code lightweight, modular, and dependency-free: runs on standard Python 3 with **zero `pip` dependencies**.
- Separate the REST API backend from the frontend UI.

---

## 📚 Covered AI Topics & Algorithms

### 1. Search Algorithms
| Algorithm | Module | Description |
| :--- | :--- | :--- |
| **Depth-First Search (DFS)** | `algorithms/search/dfs.py` | Explores as deep as possible along each branch before backtracking using a LIFO stack. |
| **Breadth-First Search (BFS)** | `algorithms/search/bfs.py` | Explores neighbors level-by-level using a FIFO queue; optimal for unweighted graphs. |
| **Iterative Deepening (IDS)** | `algorithms/search/ids.py` | Combines BFS optimality/completeness with DFS $O(bd)$ space efficiency. |
| **A\* Search** | `algorithms/search/astar.py` | Informed heuristic search using $f(n) = g(n) + h(n)$ with priority queues. |
| **D\* (Dynamic A\*)** | `algorithms/search/dstar.py` | Dynamic replanning when unexpected obstacles appear without restarting search from scratch. |
| **Hill Climbing** | `algorithms/search/hill_climbing.py` | Greedy local search climbing towards higher elevation; illustrates local maxima trapping. |
| **Simulated Annealing** | `algorithms/search/simulated_annealing.py` | Probabilistic search accepting worse moves with probability $P = e^{\Delta E / T}$ to escape local optima. |

### 2. AI Problems
| Problem | Module | Description |
| :--- | :--- | :--- |
| **Wumpus World** | `algorithms/problems/wumpus.py` | Knowledge-based agent using propositional logic and sensory percepts (Stench, Breeze, Glitter) in a 4×4 cave. |
| **8-Puzzle** | `algorithms/problems/eight_puzzle.py` | Sliding tile puzzle solved optimally with A\* guided by the Manhattan Distance heuristic. |
| **Towers of Hanoi** | `algorithms/problems/hanoi.py` | Divide-and-conquer recursive puzzle moving $N$ disks in $2^N - 1$ optimal moves. |

### 3. Probabilistic AI
| Model | Module | Description |
| :--- | :--- | :--- |
| **Bayesian Network** | `algorithms/probabilistic/bayesian_network.py` | Exact inference via Bayes' rule on the classic Wet Grass network (Rain $\to$ Sprinkler $\to$ Wet Grass). |
| **Expectation-Maximization (EM)** | `algorithms/probabilistic/em.py` | Two-coin parameter estimation with hidden/latent coin identities across E-steps and M-steps. |
| **Hidden Markov Model (HMM)** | `algorithms/probabilistic/hmm.py` | Forward algorithm (observation sequence evaluation) and Viterbi dynamic programming (hidden state decoding). |

---

## 📁 Project Structure

```text
virtual/
├── README.md               # Documentation, setup guide, and API reference
├── server.py               # Main launcher script (starts HTTP server)
├── backend/
│   ├── __init__.py
│   ├── app.py              # HTTP server, routing, static file handler, input validation
│   └── assistant.py        # Intent recognition, dialogue manager, parameter extraction
├── algorithms/             # Modular algorithm implementations
│   ├── __init__.py
│   ├── registry.py         # Algorithm catalog, metadata, and runner dispatch
│   ├── search/
│   │   ├── dfs.py
│   │   ├── bfs.py
│   │   ├── ids.py
│   │   ├── astar.py
│   │   ├── dstar.py
│   │   ├── hill_climbing.py
│   │   └── simulated_annealing.py
│   ├── problems/
│   │   ├── wumpus.py
│   │   ├── eight_puzzle.py
│   │   └── hanoi.py
│   └── probabilistic/
│       ├── bayesian_network.py
│       ├── em.py
│       └── hmm.py
├── frontend/               # Chat virtual assistant interface
│   ├── index.html          # Clean, responsive chat layout
│   ├── style.css           # Styling, message bubbles, monospace code formatting
│   └── app.js              # Fetch client, markdown parsing, quick-action chips
└── tests/                  # Unit and integration test suite
    ├── test_algorithms.py  # Tests for all 13 algorithms
    ├── test_api.py         # Tests for all REST endpoints & static files
    └── test_assistant.py   # Tests for dialogue flows & user intents
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher.
- No third-party packages or virtual environments are required.

### Running the Application

1. Open your terminal in the project directory:
   ```bash
   cd /path/to/virtual
   ```

2. Start the server:
   ```bash
   python3 server.py
   ```
   *(Optional: You can specify a custom port, e.g., `python3 server.py 8080`)*

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

---

## 💬 Example Chat Queries

The assistant recognizes natural academic requests, including:

- **Run BFS** — executes Breadth-First Search on a sample graph.
- **Solve an 8 puzzle** — demonstrates A\* solving a 3×3 sliding tile puzzle.
- **Show Towers of Hanoi** — runs recursive solution for 3 disks (or `Show Towers of Hanoi with 4 disks`).
- **Demonstrate Wumpus World** — shows sensory percepts and logical deduction in a 4×4 cave.
- **Explain the Hidden Markov Model** — explains theory, Forward algorithm, and Viterbi decoding.
- **Run A\*** — demonstrates $f(n) = g(n) + h(n)$ search step-by-step.
- **Demonstrate D\*** — shows dynamic replanning when an obstacle is detected mid-route.
- **Run Hill Climbing** — shows greedy climbing and local maximum entrapment.
- **Run Simulated Annealing** — shows temperature cooling and escaping local peaks.
- **Demonstrate Bayesian Network** — computes exact posterior probabilities using Bayes' rule.
- **Explain Expectation-Maximization** — breaks down the E-step and M-step for the two-coin problem.
- **Help** or **Topics** — displays a list of all available topics and algorithms.

---

## 🔌 API Documentation

The backend exposes a clean REST API. All payloads and responses use standard JSON.

### 1. Health Check
- **Route:** `GET /api/health`
- **Response:**
  ```json
  {
    "status": "ok",
    "app": "AI Virtual Assistant",
    "version": "1.0.0"
  }
  ```

### 2. List All Algorithms
- **Route:** `GET /api/algorithms`
- **Response:**
  ```json
  {
    "count": 13,
    "algorithms": [
      {
        "id": "bfs",
        "name": "Breadth-First Search (BFS)",
        "category": "Search algorithms",
        "description": "Explores neighbor nodes level-by-level using a FIFO queue...",
        "sample_query": "Run BFS",
        "parameters": {
          "start": { "type": "string", "default": "A", "description": "Start node (A-G)" },
          "goal": { "type": "string", "default": "G", "description": "Goal node (A-G)" }
        }
      }
    ]
  }
  ```

### 3. Chat Message
- **Route:** `POST /api/chat`
- **Request Body:**
  ```json
  {
    "message": "Run BFS"
  }
  ```
- **Response:**
  ```json
  {
    "reply": "Here is the demonstration for **Breadth-First Search (BFS)**:\n\n```text\n=== Breadth-First Search (BFS) Demonstration ===\nGraph Nodes: A, B, C, D, E, F, G\nStart Node: A | Goal Node: G\nExploration Order (Visited): A -> B -> C -> D -> E -> F -> G\nGoal Found: Yes\nSolution Path: A -> C -> F -> G\nPath Length (edges): 3\n```",
    "intent": "run_algorithm",
    "algorithm_id": "bfs",
    "algorithm_name": "Breadth-First Search (BFS)",
    "suggestions": ["Run another algorithm", "Show topics", "Help"]
  }
  ```

### 4. Direct Algorithm Execution
- **Route:** `POST /api/algorithms/run`
- **Request Body:**
  ```json
  {
    "algorithm": "hanoi",
    "params": {
      "n_disks": 3
    }
  }
  ```
- **Response:**
  ```json
  {
    "algorithm": "Towers of Hanoi",
    "explanation": "Divide-and-conquer recursive solution requiring 2^N - 1 moves.",
    "n_disks": 3,
    "total_moves": 7,
    "formatted_text": "=== Towers of Hanoi Recursive Demonstration ===\n..."
  }
  ```

---

## 🧪 Running Unit Tests

The project includes unit and integration tests covering all 13 algorithms, the dialogue engine, and the REST API endpoints:

```bash
python3 -m unittest discover tests
```

Sample output:
```text
Ran 29 tests in 0.004s

OK
```

---

## ⚖️ Assumptions & Limitations

1. **Rule-Based Dialogue:** The assistant uses keyword and pattern matching to understand user intent. It does not use or connect to a large language model.
2. **Pedagogical Graph & Grid Sizes:** Demonstrations use clear, standardized benchmark problems (e.g., 7-node graphs, 4×4 Wumpus grid, 3-disk Hanoi, 15-point landscape) so outputs remain easy to inspect and evaluate during academic coursework.
3. **No External Network Dependencies:** All calculations and server handling run locally with Python's built-in libraries.

