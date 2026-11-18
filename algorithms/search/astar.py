"""
A* (A-Star) Search Algorithm Implementation
Academic AI Demonstration Module
"""
import heapq

# Weighted graph: node -> list of (neighbor, edge_cost)
SAMPLE_WEIGHTED_GRAPH = {
    'S': [('A', 1), ('B', 4)],
    'A': [('B', 2), ('C', 5), ('D', 12)],
    'B': [('C', 2)],
    'C': [('D', 3), ('G', 10)],
    'D': [('G', 1)],
    'G': []
}

# Admissible heuristic: estimated distance h(n) to goal 'G'
SAMPLE_HEURISTICS = {
    'S': 7,
    'A': 6,
    'B': 4,
    'C': 2,
    'D': 1,
    'G': 0
}

def astar(graph=None, heuristics=None, start='S', goal='G'):
    """
    Performs A* Search using f(n) = g(n) + h(n).
    g(n): exact cost from start to n.
    h(n): heuristic estimated cost from n to goal.
    """
    if graph is None:
        graph = SAMPLE_WEIGHTED_GRAPH
    if heuristics is None:
        heuristics = SAMPLE_HEURISTICS

    start = start.upper()
    goal = goal.upper()

    if start not in graph:
        return {"error": f"Start node '{start}' not found in graph."}
    if goal not in graph:
        return {"error": f"Goal node '{goal}' not found in graph."}

    # Priority queue stores tuples: (f_score, g_score, current_node, path)
    initial_h = heuristics.get(start, 0)
    pq = [(initial_h, 0, start, [start])]
    
    # Track lowest g_score found to each node
    best_g = {start: 0}
    expansion_steps = []
    found = False
    final_path = []
    total_cost = 0

    while pq:
        f, g, current, path = heapq.heappop(pq)

        # Skip if we already reached this node with a strictly lower g cost
        if g > best_g.get(current, float('inf')):
            continue

        expansion_steps.append({
            "node": current,
            "g": g,
            "h": heuristics.get(current, 0),
            "f": f,
            "path": path
        })

        if current == goal:
            found = True
            final_path = path
            total_cost = g
            break

        for neighbor, weight in graph.get(current, []):
            new_g = g + weight
            if new_g < best_g.get(neighbor, float('inf')):
                best_g[neighbor] = new_g
                h = heuristics.get(neighbor, 0)
                new_f = new_g + h
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [neighbor]))

    output_lines = [
        "=== A* (A-Star) Search Demonstration ===",
        f"Start: {start} | Goal: {goal}",
        "Evaluation Function: f(n) = g(n) + h(n)",
        "--------------------------------------------------",
        "Step-by-step Node Expansions:"
    ]

    for idx, step in enumerate(expansion_steps, start=1):
        output_lines.append(
            f"  Step {idx}: Expand Node '{step['node']}' | "
            f"g={step['g']}, h={step['h']} => f={step['f']} | Path: {' -> '.join(step['path'])}"
        )

    output_lines.extend([
        "--------------------------------------------------",
        f"Goal Reached: {'Yes' if found else 'No'}",
        f"Optimal Path: {' -> '.join(final_path) if found else 'None'}",
        f"Total Path Cost (g): {total_cost}",
        "",
        "Key Concepts:",
        "- g(n) is the exact accumulated cost from the start node.",
        "- h(n) is an admissible heuristic (it never overestimates the true remaining cost).",
        "- When h(n) is admissible, A* is guaranteed to find an optimal (least cost) path.",
        "- A* expands the fewest nodes possible among all equally informed optimal algorithms."
    ])

    return {
        "algorithm": "A* Search",
        "explanation": "A* finds the shortest path using f(n) = g(n) + h(n), balancing actual cost so far with estimated remaining cost.",
        "start": start,
        "goal": goal,
        "path": final_path,
        "total_cost": total_cost,
        "steps": expansion_steps,
        "formatted_text": "\n".join(output_lines)
    }

if __name__ == "__main__":
    res = astar()
    print(res["formatted_text"])

