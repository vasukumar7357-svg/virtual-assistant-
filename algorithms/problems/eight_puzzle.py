"""
8-Puzzle Solver using A* Search with Manhattan Distance Heuristic
Academic AI Demonstration Module
"""
import heapq

# Target Goal State:
# 1  2  3
# 4  5  6
# 7  8  0 (0 represents the blank space)
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Default starting state (solvable in 4 moves for a clean, fast demonstration)
DEFAULT_START_STATE = (1, 2, 3, 4, 0, 6, 7, 5, 8)

def manhattan_distance(state):
    """Calculates sum of Manhattan distances of all tiles from their goal positions."""
    dist = 0
    for idx, val in enumerate(state):
        if val != 0:
            target_idx = val - 1  # val 1 belongs at idx 0, etc.
            curr_r, curr_c = divmod(idx, 3)
            goal_r, goal_c = divmod(target_idx, 3)
            dist += abs(curr_r - goal_r) + abs(curr_c - goal_c)
    return dist

def get_neighbors(state):
    """Generates valid next states by sliding adjacent tiles into the blank (0)."""
    blank_idx = state.index(0)
    r, c = divmod(blank_idx, 3)
    neighbors = []

    moves = [
        ('UP', r - 1, c),
        ('DOWN', r + 1, c),
        ('LEFT', r, c - 1),
        ('RIGHT', r, c + 1)
    ]

    for move_name, nr, nc in moves:
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_blank = nr * 3 + nc
            new_state = list(state)
            new_state[blank_idx], new_state[new_blank] = new_state[new_blank], new_state[blank_idx]
            neighbors.append((move_name, tuple(new_state)))

    return neighbors

def format_grid(state):
    """Renders 3x3 board string."""
    rows = []
    for r in range(3):
        row_tiles = [str(x) if x != 0 else "_" for x in state[r*3:(r+1)*3]]
        rows.append("  [ " + "  ".join(row_tiles) + " ]")
    return "\n".join(rows)

def solve_8_puzzle(start_state=None):
    """
    Solves the 8-puzzle from start_state to GOAL_STATE using A* Search.
    """
    if start_state is None:
        start_state = DEFAULT_START_STATE
    else:
        start_state = tuple(start_state)

    if len(start_state) != 9 or set(start_state) != set(range(9)):
        return {"error": "Invalid board state. Must contain digits 0 through 8 exactly once."}

    # Priority queue stores (f, g, state, path_of_actions, states_trace)
    h0 = manhattan_distance(start_state)
    pq = [(h0, 0, start_state, [], [start_state])]
    visited_costs = {start_state: 0}

    nodes_expanded = 0
    solution_moves = []
    solution_states = []

    while pq:
        f, g, curr_state, actions, state_history = heapq.heappop(pq)
        nodes_expanded += 1

        if curr_state == GOAL_STATE:
            solution_moves = actions
            solution_states = state_history
            break

        if g > visited_costs.get(curr_state, float('inf')):
            continue

        for move_dir, next_state in get_neighbors(curr_state):
            new_g = g + 1
            if new_g < visited_costs.get(next_state, float('inf')):
                visited_costs[next_state] = new_g
                h = manhattan_distance(next_state)
                new_f = new_g + h
                heapq.heappush(pq, (
                    new_f,
                    new_g,
                    next_state,
                    actions + [move_dir],
                    state_history + [next_state]
                ))

    output_lines = [
        "=== 8-Puzzle Solver (A* with Manhattan Heuristic) ===",
        f"Initial Board State:\n{format_grid(start_state)}",
        "",
        f"Goal Board State:\n{format_grid(GOAL_STATE)}",
        "",
        f"Solution Found in {len(solution_moves)} moves (Nodes Expanded: {nodes_expanded}):",
        "--------------------------------------------------"
    ]

    for idx, (move, st) in enumerate(zip(["START"] + solution_moves, solution_states)):
        step_title = "Initial State:" if idx == 0 else f"Step {idx}: Move {move}"
        output_lines.append(f"{step_title}\n{format_grid(st)}\n")

    output_lines.extend([
        "--------------------------------------------------",
        f"Move Sequence: {' -> '.join(solution_moves) if solution_moves else 'Already at goal'}",
        "",
        "Algorithm Breakdown:",
        "- Search algorithm: A* with Priority Queue.",
        "- Evaluation function: f(n) = g(n) + h(n).",
        "- g(n) = number of moves taken from the initial configuration.",
        "- h(n) = Manhattan Distance (sum of vertical + horizontal distances for each tile to target position).",
        "- Manhattan distance is an admissible and consistent heuristic, guaranteeing the shortest solution path."
    ])

    return {
        "algorithm": "8-Puzzle Solver",
        "explanation": "A* search on a sliding tile puzzle using the Manhattan Distance admissible heuristic.",
        "start_state": list(start_state),
        "goal_state": list(GOAL_STATE),
        "total_moves": len(solution_moves),
        "move_sequence": solution_moves,
        "nodes_expanded": nodes_expanded,
        "formatted_text": "\n".join(output_lines)
    }

if __name__ == "__main__":
    res = solve_8_puzzle()
    print(res["formatted_text"])

