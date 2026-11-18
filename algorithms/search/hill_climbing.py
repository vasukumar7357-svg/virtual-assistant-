"""
Hill Climbing (Local Search) Implementation
Academic AI Demonstration Module
"""

# Discrete 1D landscape representing elevation/fitness at discrete positions
# Demonstrates local maximum vs global maximum
DEFAULT_LANDSCAPE = [4, 7, 13, 20, 15, 8, 11, 19, 29, 24, 16, 21, 35, 28, 12]

def hill_climbing(landscape=None, start_index=1):
    """
    Performs Simple Hill Climbing on an elevation landscape.
    Continually moves to the best neighboring state with higher elevation.
    Terminates when no neighbor has a strictly higher value (local maximum).
    """
    if landscape is None:
        landscape = list(DEFAULT_LANDSCAPE)

    n = len(landscape)
    if not (0 <= start_index < n):
        return {"error": f"start_index must be between 0 and {n-1}."}

    current_idx = start_index
    current_val = landscape[current_idx]
    
    trajectory = [{
        "step": 0,
        "index": current_idx,
        "value": current_val,
        "action": f"Started at position {current_idx} with value {current_val}"
    }]

    step = 0
    while True:
        step += 1
        # Evaluate left and right neighbors
        neighbors = []
        if current_idx - 1 >= 0:
            neighbors.append((current_idx - 1, landscape[current_idx - 1]))
        if current_idx + 1 < n:
            neighbors.append((current_idx + 1, landscape[current_idx + 1]))

        # Find the neighbor with highest elevation
        best_neighbor = max(neighbors, key=lambda x: x[1])
        best_idx, best_val = best_neighbor

        # If best neighbor is higher, climb to it
        if best_val > current_val:
            current_idx, current_val = best_idx, best_val
            trajectory.append({
                "step": step,
                "index": current_idx,
                "value": current_val,
                "action": f"Climbed to position {current_idx} (value {current_val})"
            })
        else:
            # Reached a peak (no neighbor is higher)
            trajectory.append({
                "step": step,
                "index": current_idx,
                "value": current_val,
                "action": f"No neighbor is higher. Trapped at peak at position {current_idx} (value {current_val})"
            })
            break

    global_max_val = max(landscape)
    global_max_idx = landscape.index(global_max_val)
    is_global = (current_val == global_max_val)

    output_lines = [
        "=== Hill Climbing (Local Search) Demonstration ===",
        f"State Landscape Elevation: {landscape}",
        f"Start Position: Index {start_index} (Value: {landscape[start_index]})",
        f"Global Maximum: Index {global_max_idx} (Value: {global_max_val})",
        "",
        "Climbing Trace:"
    ]

    for item in trajectory:
        output_lines.append(f"  Step {item['step']}: {item['action']}")

    output_lines.extend([
        "",
        f"Final Terminating State: Index {current_idx} with Value {current_val}",
        f"Reached Global Maximum: {'Yes (Global Peak)' if is_global else 'No (Stuck in a Local Maximum!)'}",
        "",
        "How Hill Climbing Works & Limitations:",
        "- Greedy local search: always takes the best step immediately available.",
        "- Very memory-efficient (only stores current state and immediate neighbors).",
        "- Key weaknesses:",
        "  1. Local Maxima: Stops when neighboring states are worse, missing higher distant peaks.",
        "  2. Plateaus: Flat areas with identical neighbor values where slope gives no direction.",
        "  3. Ridges: Navigating diagonal ridges can require zig-zagging."
    ])

    return {
        "algorithm": "Hill Climbing",
        "explanation": "Greedy local search that iteratively moves towards higher neighbor values. Highly susceptible to local maxima.",
        "landscape": landscape,
        "start_index": start_index,
        "final_index": current_idx,
        "final_value": current_val,
        "global_max": {"index": global_max_idx, "value": global_max_val},
        "is_global": is_global,
        "trajectory": trajectory,
        "formatted_text": "\n".join(output_lines)
    }

if __name__ == "__main__":
    res = hill_climbing()
    print(res["formatted_text"])

