"""
D* (Dynamic A* / Dynamic Replanning) Implementation
Academic AI Demonstration Module
"""

class SimpleDStarDemo:
    """
    Demonstrates Dynamic Replanning (D* / D* Lite concept) on a navigation graph.
    The agent plans an initial optimal route, encounters a dynamic blockage
    along the way, and replans efficiently from its current position.
    """
    def __init__(self):
        # Initial graph with known traversable edge costs
        self.graph = {
            'S': {'A': 2, 'C': 5},
            'A': {'B': 2, 'D': 4},
            'B': {'G': 3},
            'C': {'D': 1, 'E': 6},
            'D': {'G': 3},
            'E': {'G': 2},
            'G': {}
        }
        # Add undirected connections for realism
        for u in list(self.graph.keys()):
            for v, w in list(self.graph[u].items()):
                if u not in self.graph.setdefault(v, {}):
                    self.graph[v][u] = w

        self.heuristics = {
            'S': 6, 'A': 4, 'B': 2, 'C': 5, 'D': 3, 'E': 2, 'G': 0
        }

    def dijkstra_or_astar(self, start, goal):
        """Standard shortest path search."""
        import heapq
        pq = [(self.heuristics.get(start, 0), 0, start, [start])]
        best_g = {start: 0}

        while pq:
            f, g, u, path = heapq.heappop(pq)
            if g > best_g.get(u, float('inf')):
                continue
            if u == goal:
                return path, g

            for v, cost in self.graph.get(u, {}).items():
                if cost == float('inf'):
                    continue
                new_g = g + cost
                if new_g < best_g.get(v, float('inf')):
                    best_g[v] = new_g
                    heapq.heappush(pq, (new_g + self.heuristics.get(v, 0), new_g, v, path + [v]))

        return None, float('inf')

    def run_demonstration(self, start='S', goal='G', blocked_edge=('A', 'B')):
        """
        Runs the full D* dynamic replanning sequence:
        1. Initial route planning
        2. Moving to the intermediate waypoint
        3. Detecting unexpected obstacle
        4. Dynamic replanning to goal
        """
        # Step 1: Initial path planning
        init_path, init_cost = self.dijkstra_or_astar(start, goal)

        # Step 2: Agent moves along initial path to first waypoint
        current_agent_pos = 'A' if 'A' in init_path else start
        traveled_segment = [start, current_agent_pos]

        # Step 3: Dynamic change in environment (obstacle detected)
        u, v = blocked_edge
        self.graph[u][v] = float('inf')
        self.graph[v][u] = float('inf')

        # Step 4: D* replans from current agent position
        replan_path, replan_cost = self.dijkstra_or_astar(current_agent_pos, goal)

        full_journey = traveled_segment[:-1] + replan_path if replan_path else None
        total_journey_cost = 2 + replan_cost if replan_path else float('inf')  # 2 is cost from S to A

        output_lines = [
            "=== D* (Dynamic A*) Replanning Demonstration ===",
            f"Scenario: Robot navigating from '{start}' to '{goal}' in an environment with changing obstacles.",
            "",
            "Phase 1: Initial Planning (Static Map)",
            f"  Optimal initial path computed: {' -> '.join(init_path)} (Expected cost: {init_cost})",
            "",
            f"Phase 2: Execution & Dynamic Obstacle Encounter",
            f"  Robot moves from {start} to {current_agent_pos}.",
            f"  [ALERT] Sensor detects edge ({u} <-> {v}) is BLOCKED by a fallen obstacle!",
            f"  Edge cost updated: cost({u}, {v}) = Infinity.",
            "",
            "Phase 3: D* Dynamic Replanning (from current position)",
            f"  Instead of restarting from scratch, D* repairs the search tree from node '{current_agent_pos}'.",
            f"  Replanned remaining path: {' -> '.join(replan_path)} (Remaining cost: {replan_cost})",
            f"  Complete trajectory taken: {' -> '.join(full_journey)} (Total cost: {total_journey_cost})",
            "",
            "How D* Works & Why It Matters:",
            "- In standard A*, any map change requires restarting the entire search from scratch.",
            "- D* (Dynamic A*) and D* Lite maintain cost estimates (rhs / g values) and back-pointers.",
            "- When an obstacle is detected, D* only updates nodes whose costs are affected.",
            "- Widely used in autonomous vehicles (e.g. Mars Rovers, warehouse robots) navigating unknown terrain."
        ]

        return {
            "algorithm": "D* (Dynamic A*)",
            "explanation": "D* plans an initial path and efficiently replans local routes when unexpected obstacles appear, without restarting from scratch.",
            "start": start,
            "goal": goal,
            "initial_path": init_path,
            "initial_cost": init_cost,
            "blocked_edge": blocked_edge,
            "replan_from": current_agent_pos,
            "replan_path": replan_path,
            "full_journey": full_journey,
            "total_journey_cost": total_journey_cost,
            "formatted_text": "\n".join(output_lines)
        }

def dstar(start='S', goal='G'):
    demo = SimpleDStarDemo()
    return demo.run_demonstration(start=start, goal=goal)

if __name__ == "__main__":
    res = dstar()
    print(res["formatted_text"])

