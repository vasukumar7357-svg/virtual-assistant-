"""
Depth-First Search (DFS) Implementation
Academic AI Demonstration Module
"""

# Default sample graph: adjacency list with node neighbors
SAMPLE_GRAPH = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E', 'G'],
    'G': ['F']
}

def dfs(graph=None, start='A', goal='G'):
    """
    Performs Depth-First Search on a graph.
    Explores as deep as possible along each branch before backtracking.
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

    # Stack stores tuples of (current_node, path_to_current)
    stack = [(start, [start])]

    while stack:
        current, path = stack.pop()  # LIFO order
        
        if current not in visited:
            visited.append(current)
            traversal_steps.append({
                "node": current,
                "current_path": path,
                "action": f"Visiting {current}"
            })

            if current == goal:
                found = True
                final_path = path
                break

            # Add unvisited neighbors to stack (reverse sorted for consistent left-to-right exploration)
            neighbors = sorted(graph.get(current, []), reverse=True)
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    output_lines = [
        "=== Depth-First Search (DFS) Demonstration ===",
        f"Graph Nodes: {', '.join(graph.keys())}",
        f"Start Node: {start} | Goal Node: {goal}",
        f"Exploration Order (Visited): {' -> '.join(visited)}",
        f"Goal Found: {'Yes' if found else 'No'}",
        f"Solution Path: {' -> '.join(final_path) if found else 'No path found'}",
        f"Path Length (edges): {len(final_path) - 1 if found else 0}",
        "",
        "How it works:",
        "- Uses a Last-In, First-Out (LIFO) stack.",
        "- Explores each branch to its deepest node before backtracking.",
        "- Space complexity is O(b * m), where b is branching factor and m is maximum depth.",
        "- Note: DFS is not guaranteed to find the shortest path."
    ]

    return {
        "algorithm": "Depth-First Search (DFS)",
        "explanation": "DFS traverses deep down each branch before backtracking. It uses a LIFO stack.",
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
    res = dfs()
    print(res["formatted_text"])

