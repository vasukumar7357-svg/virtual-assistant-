"""
Iterative Deepening Search (IDS / IDDFS) Implementation
Academic AI Demonstration Module
"""

SAMPLE_GRAPH = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E', 'G'],
    'G': ['F']
}

def dls(graph, node, goal, depth_limit, current_path, visited_in_iteration):
    """Depth-Limited Search helper function."""
    visited_in_iteration.append(node)
    
    if node == goal:
        return True, current_path
    
    if depth_limit <= 0:
        return False, None

    for neighbor in sorted(graph.get(node, [])):
        if neighbor not in current_path:  # Avoid cycle in current path
            found, path = dls(graph, neighbor, goal, depth_limit - 1, current_path + [neighbor], visited_in_iteration)
            if found:
                return True, path

    return False, None

def ids(graph=None, start='A', goal='G', max_depth=5):
    """
    Performs Iterative Deepening Search (IDS).
    Combines BFS's optimality/completeness with DFS's low memory requirements.
    """
    if graph is None:
        graph = SAMPLE_GRAPH

    start = start.upper()
    goal = goal.upper()

    if start not in graph:
        return {"error": f"Start node '{start}' not found in graph."}
    if goal not in graph:
        return {"error": f"Goal node '{goal}' not found in graph."}

    iterations = []
    found = False
    final_path = []

    for depth in range(max_depth + 1):
        visited_in_iteration = []
        found, path = dls(graph, start, goal, depth, [start], visited_in_iteration)
        
        iterations.append({
            "depth_limit": depth,
            "visited": list(visited_in_iteration),
            "found": found,
            "path": path if found else None
        })

        if found:
            final_path = path
            break

    output_lines = [
        "=== Iterative Deepening Search (IDS) Demonstration ===",
        f"Graph Nodes: {', '.join(graph.keys())}",
        f"Start Node: {start} | Goal Node: {goal} | Max Depth Allowed: {max_depth}",
        "",
        "Iteration by Iteration Breakdown:"
    ]

    for it in iterations:
        status = f"FOUND! Path: {' -> '.join(it['path'])}" if it["found"] else "Goal not reached"
        output_lines.append(f"• Depth Limit {it['depth_limit']}: Visited [{ ' -> '.join(it['visited']) }] => {status}")

    output_lines.extend([
        "",
        f"Goal Found: {'Yes' if found else 'No'}",
        f"Final Solution Path: {' -> '.join(final_path) if found else 'No path found'}",
        f"Optimal Depth: {len(final_path) - 1 if found else 'N/A'}",
        "",
        "How it works:",
        "- Iteratively runs Depth-Limited Search (DLS), incrementing the limit by 1 each round.",
        "- Has the memory benefit of DFS: O(b * d) space complexity.",
        "- Has the completeness and optimality of BFS: O(b^d) time complexity.",
        "- Re-visiting shallower nodes adds only a small overhead (~b/(b-1) factor)."
    ] )

    return {
        "algorithm": "Iterative Deepening Search (IDS)",
        "explanation": "IDS combines DFS space efficiency O(bd) with BFS optimality by running depth-limited DFS with increasing depth limits.",
        "start": start,
        "goal": goal,
        "iterations": iterations,
        "found": found,
        "path": final_path,
        "formatted_text": "\n".join(output_lines)
    }

if __name__ == "__main__":
    res = ids()
    print(res["formatted_text"])

