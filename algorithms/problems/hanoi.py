"""
Towers of Hanoi Recursive Solver
Academic AI Demonstration Module
"""

def render_pegs(pegs, n_disks):
    """Generates a clean text display of the 3 pegs [A, B, C]."""
    lines = []
    lines.append(f"    Peg A: {pegs['A']}")
    lines.append(f"    Peg B: {pegs['B']}")
    lines.append(f"    Peg C: {pegs['C']}")
    return "\n".join(lines)

def solve_hanoi(n_disks=3, source='A', target='C', auxiliary='B'):
    """
    Solves the Towers of Hanoi puzzle recursively.
    Returns step-by-step moves and state of pegs after each move.
    """
    try:
        n_disks = int(n_disks)
    except (ValueError, TypeError):
        return {"error": "Number of disks must be an integer."}

    if n_disks < 1 or n_disks > 7:
        return {"error": "Please choose between 1 and 7 disks for a clear demonstration."}

    # Initialize pegs: larger numbers represent larger disks
    # Disk 1 is smallest, disk N is largest
    pegs = {
        source: list(range(n_disks, 0, -1)),
        auxiliary: [],
        target: []
    }

    moves_history = [{
        "step": 0,
        "action": "Initial Configuration",
        "pegs": {k: list(v) for k, v in pegs.items()}
    }]

    def hanoi_recursive(k, src, tgt, aux):
        if k == 1:
            disk = pegs[src].pop()
            pegs[tgt].append(disk)
            moves_history.append({
                "step": len(moves_history),
                "disk": disk,
                "from": src,
                "to": tgt,
                "action": f"Move disk {disk} from Peg {src} -> Peg {tgt}",
                "pegs": {p: list(v) for p, v in pegs.items()}
            })
            return

        # Move k-1 disks from src to aux using tgt
        hanoi_recursive(k - 1, src, aux, tgt)

        # Move kth disk from src to tgt
        disk = pegs[src].pop()
        pegs[tgt].append(disk)
        moves_history.append({
            "step": len(moves_history),
            "disk": disk,
            "from": src,
            "to": tgt,
            "action": f"Move disk {disk} from Peg {src} -> Peg {tgt}",
            "pegs": {p: list(v) for p, v in pegs.items()}
        })

        # Move k-1 disks from aux to tgt using src
        hanoi_recursive(k - 1, aux, tgt, src)

    hanoi_recursive(n_disks, source, target, auxiliary)

    output_lines = [
        "=== Towers of Hanoi Recursive Demonstration ===",
        f"Number of Disks: {n_disks} (Disks 1 to {n_disks}, where 1 is smallest)",
        f"Start Peg: {source} | Target Peg: {target} | Auxiliary Peg: {auxiliary}",
        f"Theoretical Minimum Moves: 2^{n_disks} - 1 = {2**n_disks - 1} moves",
        "--------------------------------------------------",
        f"Initial Peg State:\n{render_pegs(moves_history[0]['pegs'], n_disks)}\n"
    ]

    for item in moves_history[1:]:
        output_lines.append(
            f"Step {item['step']:2d}: {item['action']}\n"
            f"{render_pegs(item['pegs'], n_disks)}\n"
        )

    output_lines.extend([
        "--------------------------------------------------",
        f"Completed in {len(moves_history) - 1} moves.",
        "",
        "Key Algorithmic Concepts:",
        "- Divide and Conquer Recursion: To move N disks from A to C:",
        "  1. Move top N-1 disks from A to B (auxiliary).",
        "  2. Move the largest disk N directly from A to C.",
        "  3. Move the N-1 disks from B to C.",
        "- Recurrence relation: T(N) = 2*T(N-1) + 1 => T(N) = 2^N - 1.",
        "- Time complexity: O(2^N), Space complexity: O(N) call stack."
    ])

    return {
        "algorithm": "Towers of Hanoi",
        "explanation": "Divide-and-conquer recursive solution requiring 2^N - 1 moves.",
        "n_disks": n_disks,
        "total_moves": len(moves_history) - 1,
        "moves": moves_history,
        "formatted_text": "\n".join(output_lines)
    }

if __name__ == "__main__":
    res = solve_hanoi(3)
    print(res["formatted_text"])

