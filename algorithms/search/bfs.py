"""
Breadth-First Search (BFS) Implementation
Academic AI Demonstration Module
"""
from collections import deque

SAMPLE_GRAPH = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E', 'G'],
    'G': ['F']
}

def bfs(graph=None, start='A', goal='G'):
    """
    Performs Breadth-First Search on a graph.
    Explores neighbors level-by-level using a FIFO queue.
    """
    if graph is None:
        graph = SAMPLE_GRAPH

    start = start.upper()
    goal = goal.upper()

    if start not in graph:
        return {"error": f"Start node '{start}' not found in graph."}
    if goal not in graph:
        return {"error": f"Goal node '{goal}' not found in graph."}

    visited = []
    traversal_steps = []
    found = False
    final_path = []

    # Queue stores tuples of (current_node, path_to_current)
    queue = deque([(start, [start])])
    visited.append(start)

    while queue:
        current, path = queue.popleft()  # FIFO order
        traversal_steps.append({
            "node": current,
            "current_path": path,
            "action": f"Expanded {current}"
        })

        if current == goal:
            found = True
            final_path = path
            break

        # Check all neighbors
        for neighbor in sorted(graph.get(current, [])):
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append((neighbor, path + [neighbor]))

    output_lines = [
        "=== Breadth-First Search (BFS) Demonstration ===",
        f"Graph Nodes: {', '.join(graph.keys())}",
        f"Start Node: {start} | Goal Node: {goal}",
        f"Exploration Order (Visited): {' -> '.join(visited)}",
        f"Goal Found: {'Yes' if found else 'No'}",
        f"Solution Path: {' -> '.join(final_path) if found else 'No path found'}",
        f"Path Length (edges): {len(final_path) - 1 if found else 0}",
        "",
        "How it works:",
        "- Uses a First-In, First-Out (FIFO) queue.",
        "- Visits all nodes at depth d before moving to depth d+1.",
        "- Guaranteed to find the shortest path in unweighted graphs.",
        "- Time complexity: O(b^d), Space complexity: O(b^d)."
    ]

    return {
        "algorithm": "Breadth-First Search (BFS)",
        "explanation": "BFS explores level by level using a FIFO queue, guaranteeing the shortest path in unweighted graphs.",
        "start": start,
        "goal": goal,
        "visited_order": visited,
        "path": final_path,
        "path_length": len(final_path) - 1 if found else 0,
        "found": found,
        "steps": traversal_steps,
        "formatted_text": "\n".join(output_lines)
    }

if __name__ == "__main__":
    res = bfs()
    print(res["formatted_text"])

