"""
Simulated Annealing Implementation
Academic AI Demonstration Module
"""
import math
import random

# Using the same landscape from Hill Climbing to showcase escaping the local peak
DEFAULT_LANDSCAPE = [4, 7, 13, 20, 15, 8, 11, 19, 29, 24, 16, 21, 35, 28, 12]

def simulated_annealing(landscape=None, start_index=1, initial_temp=100.0, cooling_rate=0.85, max_steps=25, seed=42):
    """
    Performs Simulated Annealing on a discrete landscape.
    - Moves to better neighbors automatically.
    - Accepts worse neighbors with probability exp(delta_E / T).
    - Temperature T cools over time.
    """
    if landscape is None:
        landscape = list(DEFAULT_LANDSCAPE)
    
    if seed is not None:
        random.seed(seed)

    n = len(landscape)
    current_idx = start_index
    current_val = landscape[current_idx]
    
    best_idx = current_idx
    best_val = current_val

    temp = initial_temp
    history = []

    for step in range(1, max_steps + 1):
        # Choose a random adjacent neighbor
        possible_neighbors = []
        if current_idx - 1 >= 0:
            possible_neighbors.append(current_idx - 1)
        if current_idx + 1 < n:
            possible_neighbors.append(current_idx + 1)

        candidate_idx = random.choice(possible_neighbors)
        candidate_val = landscape[candidate_idx]
        delta_e = candidate_val - current_val

        accepted = False
        decision_reason = ""

        if delta_e > 0:
            accepted = True
            decision_reason = "Better state (Uphill move)"
        else:
            # Probability of accepting worse state
            acceptance_prob = math.exp(delta_e / max(temp, 1e-6))
            roll = random.random()
            if roll < acceptance_prob:
                accepted = True
                decision_reason = f"Worse state accepted! (P={acceptance_prob:.3f} > roll={roll:.3f})"
            else:
                decision_reason = f"Worse state rejected (P={acceptance_prob:.3f} <= roll={roll:.3f})"

        if accepted:
            current_idx = candidate_idx
            current_val = candidate_val
            if current_val > best_val:
                best_idx = current_idx
                best_val = current_val

        history.append({
            "step": step,
            "temp": round(temp, 2),
            "current_idx": current_idx,
            "current_val": current_val,
            "candidate_idx": candidate_idx,
            "candidate_val": candidate_val,
            "delta_e": delta_e,
            "accepted": accepted,
            "reason": decision_reason
        })

        # Cool down temperature
        temp *= cooling_rate

    global_max_val = max(landscape)
    global_max_idx = landscape.index(global_max_val)

    output_lines = [
        "=== Simulated Annealing Demonstration ===",
        f"Landscape: {landscape}",
        f"Start Position: Index {start_index} (Value: {landscape[start_index]})",
        f"Initial Temperature: {initial_temp} | Cooling Rate: {cooling_rate}",
        f"Global Maximum Target: Index {global_max_idx} (Value: {global_max_val})",
        "",
        "Step-by-step Annealing Log:"
    ]

    for h in history[:10]:  # Show first 10 for clean output
        acc_tag = "[ACCEPTED]" if h['accepted'] else "[REJECTED]"
        output_lines.append(
            f"  Step {h['step']:2d} | T={h['temp']:6.2f} | At idx {h['current_idx']} (val {h['current_val']}) | "
            f"Test idx {h['candidate_idx']} (val {h['candidate_val']}) -> {acc_tag} {h['reason']}"
        )

    if len(history) > 10:
        output_lines.append(f"  ... [{len(history)-10} more cooling steps completed] ...")
        last = history[-1]
        output_lines.append(
            f"  Final Step {last['step']} | T={last['temp']:6.2f} | Final Position: Index {last['current_idx']} (Value: {last['current_val']})"
        )

    output_lines.extend([
        "",
        f"Best State Discovered: Index {best_idx} with Value {best_val}",
        f"Reached Global Maximum: {'Yes!' if best_val == global_max_val else 'Near-optimal found'}",
        "",
        "Comparison with Hill Climbing:",
        "- Inspired by metallurgy (heating metal and cooling it slowly to reach a low-energy crystalline structure).",
        "- At high temperatures (early on), the algorithm frequently accepts downhill moves to explore the space.",
        "- As temperature cools, it becomes increasingly greedy, settling into the best global basin.",
        "- Successfully avoids getting trapped in local maxima where standard Hill Climbing fails."
    ])

    return {
        "algorithm": "Simulated Annealing",
        "explanation": "Probabilistic local search that accepts worse moves with probability P = exp(ΔE / T), escaping local maxima at high temperatures.",
        "start_index": start_index,
        "best_index": best_idx,
        "best_value": best_val,
        "global_max": {"index": global_max_idx, "value": global_max_val},
        "history": history,
        "formatted_text": "\n".join(output_lines)
    }

if __name__ == "__main__":
    res = simulated_annealing()
    print(res["formatted_text"])

