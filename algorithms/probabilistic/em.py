"""
Expectation-Maximization (EM) Algorithm Implementation
Academic AI Demonstration Module
Pedagogical Model: Two-Coin Problem with Hidden Coin Identity
(Do & Batzoglou, Nature Biotechnology / Stanford CS229)
"""
import math

def binom_likelihood(heads, tails, theta):
    """Computes likelihood theta^heads * (1 - theta)^tails (binomial proportionality)."""
    return (theta ** heads) * ((1.0 - theta) ** tails)

def expectation_maximization(theta_A_init=0.60, theta_B_init=0.50, num_iterations=4):
    """
    Demonstrates the Expectation-Maximization (EM) algorithm on a 2-coin model.
    5 rounds of 10 coin flips, but coin identities are hidden (latent).
    """
    # Observed data: list of (heads, tails) for 5 experiments of 10 tosses each
    experiments = [
        {"round": 1, "heads": 5, "tails": 5},
        {"round": 2, "heads": 9, "tails": 1},
        {"round": 3, "heads": 8, "tails": 2},
        {"round": 4, "heads": 4, "tails": 6},
        {"round": 5, "heads": 7, "tails": 3}
    ]

    theta_A = float(theta_A_init)
    theta_B = float(theta_B_init)

    iterations_trace = []

    for it in range(1, num_iterations + 1):
        # E-Step: Calculate expected counts of Heads and Tails for Coin A and Coin B
        total_expected_heads_A = 0.0
        total_expected_tails_A = 0.0
        total_expected_heads_B = 0.0
        total_expected_tails_B = 0.0

        round_details = []

        for exp in experiments:
            h, t = exp["heads"], exp["tails"]
            
            # Likelihood under Coin A and Coin B
            lh_A = binom_likelihood(h, t, theta_A)
            lh_B = binom_likelihood(h, t, theta_B)
            
            # Posterior weights (assuming equal prior P(Coin A) = P(Coin B) = 0.5)
            weight_A = lh_A / (lh_A + lh_B) if (lh_A + lh_B) > 0 else 0.5
            weight_B = 1.0 - weight_A

            exp_h_A = weight_A * h
            exp_t_A = weight_A * t
            exp_h_B = weight_B * h
            exp_t_B = weight_B * t

            total_expected_heads_A += exp_h_A
            total_expected_tails_A += exp_t_A
            total_expected_heads_B += exp_h_B
            total_expected_tails_B += exp_t_B

            round_details.append({
                "round": exp["round"],
                "heads": h,
                "tails": t,
                "weight_A": round(weight_A, 3),
                "weight_B": round(weight_B, 3)
            })

        # M-Step: Maximize parameters theta_A and theta_B from expected counts
        new_theta_A = total_expected_heads_A / (total_expected_heads_A + total_expected_tails_A)
        new_theta_B = total_expected_heads_B / (total_expected_heads_B + total_expected_tails_B)

        iterations_trace.append({
            "iteration": it,
            "theta_A_before": round(theta_A, 4),
            "theta_B_before": round(theta_B, 4),
            "expected_heads_A": round(total_expected_heads_A, 2),
            "expected_tails_A": round(total_expected_tails_A, 2),
            "expected_heads_B": round(total_expected_heads_B, 2),
            "expected_tails_B": round(total_expected_tails_B, 2),
            "theta_A_after": round(new_theta_A, 4),
            "theta_B_after": round(new_theta_B, 4),
            "round_details": round_details
        })

        theta_A, theta_B = new_theta_A, new_theta_B

    output_lines = [
        "=== Expectation-Maximization (EM) Demonstration ===",
        "Problem: Estimate bias (probability of Heads) of 2 coins (Coin A and Coin B)",
        "Latent Variable: Which coin was flipped in each round is UNKNOWN.",
        f"Initial Parameter Guesses: θ_A = {theta_A_init:.2f}, θ_B = {theta_B_init:.2f}",
        "",
        "Observed Flips (5 sets of 10 tosses):",
        "  Round 1: 5 Heads, 5 Tails | Round 2: 9 Heads, 1 Tails | Round 3: 8 Heads, 2 Tails",
        "  Round 4: 4 Heads, 6 Tails | Round 5: 7 Heads, 3 Tails",
        "--------------------------------------------------"
    ]

    for item in iterations_trace:
        output_lines.append(f"Iteration {item['iteration']}:")
        output_lines.append(
            f"  [E-Step] Weighting flips: Coin A expected {item['expected_heads_A']}H / {item['expected_tails_A']}T, "
            f"Coin B expected {item['expected_heads_B']}H / {item['expected_tails_B']}T"
        )
        output_lines.append(
            f"  [M-Step] Re-estimate biases: θ_A: {item['theta_A_before']} -> {item['theta_A_after']} | "
            f"θ_B: {item['theta_B_before']} -> {item['theta_B_after']}\n"
        )

    output_lines.extend([
        "--------------------------------------------------",
        f"Final Parameter Estimates after {num_iterations} iterations:",
        f"  • Estimated Bias of Coin A (θ_A): {theta_A:.4f} (~{theta_A*100:.1f}% heads)",
        f"  • Estimated Bias of Coin B (θ_B): {theta_B:.4f} (~{theta_B*100:.1f}% heads)",
        "",
        "How Expectation-Maximization Works:",
        "- Used when datasets have missing or hidden (latent) variables.",
        "- E-Step (Expectation): Evaluates responsibilities (probabilities of each coin generating the data) using current parameters.",
        "- M-Step (Maximization): Computes maximum likelihood parameters using the expected counts from the E-step.",
        "- Guaranteed to monotonically increase the log-likelihood of the observed data until convergence."
    ])

    return {
        "algorithm": "Expectation-Maximization (EM)",
        "explanation": "Iterative optimization algorithm for estimating parameters in models with latent variables.",
        "initial_parameters": {"theta_A": theta_A_init, "theta_B": theta_B_init},
        "final_parameters": {"theta_A": round(theta_A, 4), "theta_B": round(theta_B, 4)},
        "iterations": iterations_trace,
        "formatted_text": "\n".join(output_lines)
    }

if __name__ == "__main__":
    res = expectation_maximization()
    print(res["formatted_text"])

