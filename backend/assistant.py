"""
Virtual Assistant Intent Recognition and Chat Response Engine
Rule-based, transparent, beginner-friendly academic assistant.
"""
import re
from algorithms.registry import ALGORITHMS, run_algorithm, get_all_algorithms

GREETING_KEYWORDS = ["hi", "hello", "hey", "greetings", "good morning", "good evening", "howdy", "sup"]
HELP_KEYWORDS = ["help", "topics", "algorithms", "menu", "list", "what can you do", "options", "commands"]

def detect_algorithm_intent(message):
    """
    Identifies which algorithm the user is referring to based on keywords.
    Returns (algo_id, algo_metadata) or (None, None).
    """
    msg_clean = message.lower().strip()
    
    # Priority matching: match exact or multi-word keywords first
    for algo_id, meta in ALGORITHMS.items():
        for kw in meta["keywords"]:
            # Word boundary matching or direct substring for specific terms
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, msg_clean):
                return algo_id, meta
            # Handle special symbols like A* or D*
            if kw in ["a*", "d*"] and kw in msg_clean:
                return algo_id, meta

    return None, None

def extract_parameters(algo_id, message):
    """
    Extracts optional parameters from user message (e.g. disk count for Hanoi).
    """
    msg_clean = message.lower()
    params = {}

    if algo_id == "hanoi":
        # Look for numbers like "4 disks" or "with 5"
        match = re.search(r'(\d+)\s*(?:disks?|plates?)?', msg_clean)
        if match:
            val = int(match.group(1))
            if 1 <= val <= 7:
                params["n_disks"] = val

    elif algo_id in ["dfs", "bfs", "ids"]:
        # Look for start or goal, e.g., "from B to F"
        match_route = re.search(r'from\s+([a-g])\s+to\s+([a-g])', msg_clean)
        if match_route:
            params["start"] = match_route.group(1).upper()
            params["goal"] = match_route.group(2).upper()

    elif algo_id in ["hill_climbing", "simulated_annealing"]:
        match_idx = re.search(r'(?:index|pos|position|start)\s*(\d+)', msg_clean)
        if match_idx:
            idx = int(match_idx.group(1))
            if 0 <= idx <= 14:
                params["start_index"] = idx

    elif algo_id == "em":
        match_iter = re.search(r'(\d+)\s*iterations?', msg_clean)
        if match_iter:
            params["iterations"] = min(int(match_iter.group(1)), 10)

    return params

def handle_chat_message(user_message):
    """
    Main dialogue manager.
    Processes user input and returns structured assistant response.
    """
    if not user_message or not user_message.strip():
        return {
            "reply": "Please enter a question or choose an AI demonstration!",
            "intent": "empty_input",
            "suggestions": ["Run BFS", "Solve 8 Puzzle", "Explain HMM", "Show Towers of Hanoi"]
        }

    raw_text = user_message.strip()
    msg_lower = raw_text.lower()

    # 1. Greetings
    if any(re.search(r'\b' + re.escape(g) + r'\b', msg_lower) for g in GREETING_KEYWORDS):
        return {
            "reply": (
                "👋 Hello! I'm your student **AI Virtual Assistant**.\n\n"
                "I can demonstrate and explain 13 classical AI algorithms across three areas:\n"
                "• **Search algorithms**: DFS, BFS, IDS, A*, D*, Hill Climbing, Simulated Annealing\n"
                "• **AI problems**: Wumpus World, 8-Puzzle, Towers of Hanoi\n"
                "• **Probabilistic AI**: Bayesian Network, EM (Expectation-Maximization), HMM (Hidden Markov Model)\n\n"
                "Try clicking a prompt below or type something like `Run BFS` or `Solve 8 Puzzle`!"
            ),
            "intent": "greeting",
            "suggestions": ["Run BFS", "Solve an 8 puzzle", "Show Towers of Hanoi", "Explain the Hidden Markov Model", "Demonstrate Wumpus World"]
        }

    # 2. Help / Topics List
    if any(re.search(r'\b' + re.escape(h) + r'\b', msg_lower) for h in HELP_KEYWORDS):
        catalog = get_all_algorithms()
        categories = {}
        for item in catalog:
            categories.setdefault(item["category"], []).append(item["name"])

        reply_lines = [
            "📚 **Supported AI Algorithms & Demonstrations:**\n"
        ]
        for cat, items in categories.items():
            reply_lines.append(f"**{cat}:**")
            for name in items:
                reply_lines.append(f"  • {name}")
            reply_lines.append("")

        reply_lines.append("You can ask me to **explain** any of them or **run** a live step-by-step demonstration!")
        return {
            "reply": "\n".join(reply_lines),
            "intent": "help",
            "suggestions": ["Run A*", "Demonstrate D*", "Run Simulated Annealing", "Demonstrate Bayesian Network"]
        }

    # 3. Detect Algorithm Intent
    algo_id, algo_meta = detect_algorithm_intent(raw_text)

    if algo_id:
        # Check if the user specifically asked for an explanation vs running a demo
        is_explain_only = bool(re.search(r'\b(explain|what is|tell me about|how does|definition|theory)\b', msg_lower)) and not bool(re.search(r'\b(run|solve|show|demonstrate|demo|execute|trace|simulate)\b', msg_lower))

        if is_explain_only:
            # Return concise educational explanation and invite them to run it
            reply_text = (
                f"### 📖 {algo_meta['name']}\n\n"
                f"**Category:** {algo_meta['category']}\n\n"
                f"**Overview:** {algo_meta['description']}\n\n"
                f"Would you like to see it in action? Type **`Run {algo_meta['name']}`** or click the button below!"
            )
            return {
                "reply": reply_text,
                "intent": "explain_algorithm",
                "algorithm_id": algo_id,
                "algorithm_name": algo_meta["name"],
                "suggestions": [f"Run {algo_meta['name']}", "List other topics"]
            }
        else:
            # Run the demonstration!
            extracted_params = extract_parameters(algo_id, raw_text)
            result = run_algorithm(algo_id, extracted_params)

            if "error" in result:
                return {
                    "reply": f"⚠️ {result['error']}",
                    "intent": "algorithm_error",
                    "algorithm_id": algo_id,
                    "suggestions": ["Run BFS", "Solve 8 Puzzle", "Help"]
                }

            # Return demonstration output
            formatted = result.get("formatted_text", "")
            summary = f"Here is the demonstration for **{algo_meta['name']}**:\n\n```text\n{formatted}\n```"
            
            return {
                "reply": summary,
                "intent": "run_algorithm",
                "algorithm_id": algo_id,
                "algorithm_name": algo_meta["name"],
                "data": result,
                "suggestions": ["Run another algorithm", "Show topics", "Help"]
            }

    # 4. Fallback / Unrecognized Request
    return {
        "reply": (
            "🤔 I didn't quite understand that request.\n\n"
            "As an academic virtual assistant, I specialize in demonstrating these AI algorithms:\n"
            "• **Search**: BFS, DFS, IDS, A*, D*, Hill Climbing, Simulated Annealing\n"
            "• **Problems**: 8-Puzzle, Towers of Hanoi, Wumpus World\n"
            "• **Probabilistic**: Bayesian Network, EM, Hidden Markov Model (HMM)\n\n"
            "Please choose a topic below or type **`help`** to view all options!"
        ),
        "intent": "unknown",
        "suggestions": ["Run BFS", "Solve an 8 puzzle", "Show Towers of Hanoi", "Explain HMM", "Demonstrate Wumpus World"]
    }

