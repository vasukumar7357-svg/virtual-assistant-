"""
Bayesian Network (Probabilistic Reasoning & Exact Inference) Implementation
Academic AI Demonstration Module
"""

def bayesian_network_demo(evidence_grass_wet=True):
    """
    Demonstrates exact inference on the classic 'Wet Grass' Bayesian Network.
    Variables:
      - Rain (R)
      - Sprinkler (S)
      - Grass Wet (W)
    
    DAG Structure:
      R ---> S
      |      |
      v      v
      +--> W <--+
    """
    # 1. Prior Probabilities
    # P(Rain)
    P_R = {True: 0.20, False: 0.80}

    # 2. Conditional Probability Table (CPT): P(Sprinkler | Rain)
    # If it rains, the sprinkler is rarely turned on.
    P_S_given_R = {
        (True, True): 0.01,    # P(S=T | R=T)
        (False, True): 0.99,   # P(S=F | R=T)
        (True, False): 0.40,   # P(S=T | R=F)
        (False, False): 0.60    # P(S=F | R=F)
    }

    # 3. CPT: P(GrassWet | Sprinkler, Rain)
    # Both: 0.99, Sprinkler only: 0.90, Rain only: 0.80, Neither: 0.00
    P_W_given_SR = {
        (True, True, True): 0.99,
        (False, True, True): 0.01,
        (True, True, False): 0.90,
        (False, True, False): 0.10,
        (True, False, True): 0.80,
        (False, False, True): 0.20,
        (True, False, False): 0.00,
        (False, False, False): 1.00
    }

    # Compute complete Joint Distribution Table:
    # P(R, S, W) = P(R) * P(S | R) * P(W | S, R)
    joint_distribution = []
    for r in [True, False]:
        for s in [True, False]:
            for w in [True, False]:
                p_r = P_R[r]
                p_s_given_r = P_S_given_R[(s, r)]
                p_w_given_sr = P_W_given_SR[(w, s, r)]
                prob = p_r * p_s_given_r * p_w_given_sr
                joint_distribution.append({
                    "Rain": r,
                    "Sprinkler": s,
                    "GrassWet": w,
                    "probability": round(prob, 5)
                })

    # Exact Inference: Given W = True (Grass is Wet), find P(Rain = True | GrassWet = True)
    # P(W=T) = sum_{R, S} P(R, S, W=T)
    p_w_true = sum(
        row["probability"] for row in joint_distribution if row["GrassWet"] == evidence_grass_wet
    )

    # P(R=T, W=T) = sum_{S} P(R=T, S, W=T)
    p_r_true_and_w = sum(
        row["probability"] for row in joint_distribution 
        if row["Rain"] is True and row["GrassWet"] == evidence_grass_wet
    )

    # P(S=T, W=T) = sum_{R} P(R, S=T, W=T)
    p_s_true_and_w = sum(
        row["probability"] for row in joint_distribution 
        if row["Sprinkler"] is True and row["GrassWet"] == evidence_grass_wet
    )

    # By Bayes' rule: P(A | B) = P(A, B) / P(B)
    posterior_rain = p_r_true_and_w / p_w_true if p_w_true > 0 else 0
    posterior_sprinkler = p_s_true_and_w / p_w_true if p_w_true > 0 else 0

    output_lines = [
        "=== Bayesian Network Exact Inference Demonstration ===",
        "Network Topology: Rain (R) -> Sprinkler (S) -> Wet Grass (W)",
        "                    \\------------------------>",
        "",
        "Defined Conditional Probability Tables (CPTs):",
        "  • Prior P(Rain=True) = 20%, P(Rain=False) = 80%",
        "  • P(Sprinkler=True | Rain=True) = 1%, P(Sprinkler=True | Rain=False) = 40%",
        "  • P(Wet | Sprinkler, Rain): [T, T: 99%], [T, F: 90%], [F, T: 80%], [F, F: 0%]",
        "",
        "Observed Evidence: Grass is Wet (GrassWet = True)",
        "--------------------------------------------------",
        "Joint Probability Breakdown (where GrassWet = True):"
    ]

    for row in joint_distribution:
        if row["GrassWet"] == evidence_grass_wet:
            output_lines.append(
                f"  P(R={str(row['Rain']):<5}, S={str(row['Sprinkler']):<5}, W={str(evidence_grass_wet):<5}) = {row['probability']:.5f}"
            )

    output_lines.extend([
        "--------------------------------------------------",
        f"Total Probability of Evidence P(W=True) = {p_w_true:.5f}",
        "",
        "Posterior Probabilities (Inference by Bayes' Rule):",
        f"  • P(Rain = True | Grass is Wet)      = {p_r_true_and_w:.5f} / {p_w_true:.5f} = {posterior_rain:.4f} ({posterior_rain*100:.1f}%)",
        f"  • P(Sprinkler = True | Grass is Wet) = {p_s_true_and_w:.5f} / {p_w_true:.5f} = {posterior_sprinkler:.4f} ({posterior_sprinkler*100:.1f}%)",
        "",
        "Key Bayesian Concepts:",
        "- Prior probability of Rain was only 20%.",
        "- After observing that the grass is wet, our belief in Rain updates to 35.8% (Explaining Away / Diagnostic Reasoning).",
        "- The joint distribution factorizes as: P(R,S,W) = P(R) * P(S|R) * P(W|S,R).",
        "- Exact inference uses enumeration and Bayes' conditioning."
    ])

    return {
        "algorithm": "Bayesian Network",
        "explanation": "Exact probabilistic inference on a directed acyclic graphical model using Bayes' Theorem.",
        "evidence": {"GrassWet": evidence_grass_wet},
        "joint_distribution": joint_distribution,
        "marginal_evidence_p": round(p_w_true, 5),
        "posteriors": {
            "P(Rain=True|Wet)": round(posterior_rain, 4),
            "P(Sprinkler=True|Wet)": round(posterior_sprinkler, 4)
        },
        "formatted_text": "\n".join(output_lines)
    }

if __name__ == "__main__":
    res = bayesian_network_demo()
    print(res["formatted_text"])

