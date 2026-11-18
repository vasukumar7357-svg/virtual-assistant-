"""
Hidden Markov Model (HMM) Implementation
Forward Algorithm (Evaluation) & Viterbi Algorithm (Decoding)
Academic AI Demonstration Module
"""

# Classic Weather-Activity HMM
DEFAULT_STATES = ['Rainy', 'Sunny']
DEFAULT_OBSERVATIONS = ['Walk', 'Shop', 'Clean']

DEFAULT_START_PROB = {
    'Rainy': 0.6,
    'Sunny': 0.4
}

DEFAULT_TRANSITION_PROB = {
    'Rainy': {'Rainy': 0.7, 'Sunny': 0.3},
    'Sunny': {'Rainy': 0.4, 'Sunny': 0.6}
}

DEFAULT_EMISSION_PROB = {
    'Rainy': {'Walk': 0.1, 'Shop': 0.4, 'Clean': 0.5},
    'Sunny': {'Walk': 0.6, 'Shop': 0.3, 'Clean': 0.1}
}

def forward_algorithm(obs_seq, states, start_p, trans_p, emit_p):
    """
    Computes total probability of the observation sequence using the Forward Algorithm.
    alpha_t(j) = P(o_1...o_t, state_t = j)
    """
    T = len(obs_seq)
    forward = []

    # Initialization (t = 0)
    init_alpha = {}
    for state in states:
        init_alpha[state] = start_p[state] * emit_p[state].get(obs_seq[0], 0.0)
    forward.append(init_alpha)

    # Induction (t = 1 to T-1)
    for t in range(1, T):
        alpha_t = {}
        for j in states:
            sum_prob = sum(forward[t - 1][i] * trans_p[i].get(j, 0.0) for i in states)
            alpha_t[j] = sum_prob * emit_p[j].get(obs_seq[t], 0.0)
        forward.append(alpha_t)

    # Termination: sum of final alphas
    total_prob = sum(forward[-1][state] for state in states)
    return total_prob, forward

def viterbi_algorithm(obs_seq, states, start_p, trans_p, emit_p):
    """
    Finds the most likely sequence of hidden states using the Viterbi Algorithm (Dynamic Programming).
    """
    T = len(obs_seq)
    viterbi_table = []
    backpointer = []

    # Initialization (t = 0)
    init_v = {}
    for state in states:
        init_v[state] = start_p[state] * emit_p[state].get(obs_seq[0], 0.0)
    viterbi_table.append(init_v)

    # Recursion
    for t in range(1, T):
        curr_v = {}
        curr_bp = {}
        for j in states:
            # Find max over previous states
            max_prob, best_prev_state = max(
                (viterbi_table[t - 1][i] * trans_p[i].get(j, 0.0), i) for i in states
            )
            curr_v[j] = max_prob * emit_p[j].get(obs_seq[t], 0.0)
            curr_bp[j] = best_prev_state
        viterbi_table.append(curr_v)
        backpointer.append(curr_bp)

    # Termination: find best final state
    best_final_prob, best_final_state = max((viterbi_table[-1][s], s) for s in states)

    # Path backtracking
    best_path = [best_final_state]
    for bp in reversed(backpointer):
        best_path.append(bp[best_path[-1]])
    best_path.reverse()

    return best_path, best_final_prob, viterbi_table

def run_hmm_demo(obs_seq=None):
    """Demonstrates HMM forward evaluation and Viterbi decoding."""
    if obs_seq is None:
        obs_seq = ['Walk', 'Shop', 'Clean']

    states = DEFAULT_STATES
    start_p = DEFAULT_START_PROB
    trans_p = DEFAULT_TRANSITION_PROB
    emit_p = DEFAULT_EMISSION_PROB

    # 1. Forward Algorithm
    seq_prob, alpha_steps = forward_algorithm(obs_seq, states, start_p, trans_p, emit_p)

    # 2. Viterbi Algorithm
    best_path, viterbi_prob, v_steps = viterbi_algorithm(obs_seq, states, start_p, trans_p, emit_p)

    output_lines = [
        "=== Hidden Markov Model (HMM) Demonstration ===",
        f"Hidden States: {', '.join(states)} (Weather)",
        f"Observable Tokens: {', '.join(DEFAULT_OBSERVATIONS)} (Friend's Activities)",
        f"Observed Sequence: {' -> '.join(obs_seq)}",
        "",
        "Model Parameters:",
        "  • Initial Probabilities: P(Rainy)=0.6, P(Sunny)=0.4",
        "  • Transitions: Rainy->Rainy: 0.7, Rainy->Sunny: 0.3 | Sunny->Rainy: 0.4, Sunny->Sunny: 0.6",
        "  • Emissions:",
        "      Rainy: Walk (10%), Shop (40%), Clean (50%)",
        "      Sunny: Walk (60%), Shop (30%), Clean (10%)",
        "",
        "1. Evaluation (Forward Algorithm):",
        f"  Total Probability of generating sequence {obs_seq}:",
        f"  P(Observations) = {seq_prob:.6f} (~{seq_prob*100:.4f}%)",
        "",
        "2. Decoding (Viterbi Dynamic Programming):",
        "  Trellis State Probabilities per time step:"
    ]

    for t, obs in enumerate(obs_seq):
        probs_str = ", ".join(f"{s}: {v_steps[t][s]:.5f}" for s in states)
        output_lines.append(f"    t={t+1} (Obs: '{obs:<5}'): [ {probs_str} ]")

    output_lines.extend([
        "",
        f"  Most Likely Hidden State Sequence: {' -> '.join(best_path)}",
        f"  Viterbi Path Joint Probability: {viterbi_prob:.6f}",
        "",
        "Key HMM Principles:",
        "- Hidden States: The actual weather was never directly seen.",
        "- Markov Property: The next state depends only on the current state.",
        "- Forward Algorithm calculates likelihood efficiently via dynamic programming in O(N^2 * T).",
        "- Viterbi Algorithm finds the globally optimal sequence of hidden states by backtracking."
    ])

    return {
        "algorithm": "Hidden Markov Model (HMM)",
        "explanation": "Probabilistic sequence model with hidden states and visible emissions. Solves evaluation and decoding.",
        "states": states,
        "observations": obs_seq,
        "observation_probability": round(seq_prob, 6),
        "most_likely_hidden_path": best_path,
        "viterbi_probability": round(viterbi_prob, 6),
        "formatted_text": "\n".join(output_lines)
    }

if __name__ == "__main__":
    res = run_hmm_demo()
    print(res["formatted_text"])

