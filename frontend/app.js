/**
 * AI Virtual Assistant - Frontend Client
 * Handles chat messaging, UI updates, and communication with the backend API.
 */

document.addEventListener("DOMContentLoaded", () => {
  const messagesContainer = document.getElementById("messagesContainer");
  const chatForm = document.getElementById("chatForm");
  const messageInput = document.getElementById("messageInput");
  const sendBtn = document.getElementById("sendBtn");
  const chipsContainer = document.getElementById("chipsContainer");

  // Initial welcome greeting
  renderWelcomeMessage();

  // Handle form submission
  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = messageInput.value.trim();
    if (!query) return;

    // Append user message
    appendMessage("user", query);
    messageInput.value = "";
    messageInput.focus();

    // Disable input while awaiting response
    setInputDisabled(true);

    // Show temporary typing indicator
    const typingIndicator = showTypingIndicator();

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: query })
      });

      if (!response.ok) {
        throw new Error(`Server returned HTTP ${response.status}`);
      }

      const data = await response.json();
      removeTypingIndicator(typingIndicator);
      appendMessage("assistant", data.reply, data.suggestions);
    } catch (err) {
      removeTypingIndicator(typingIndicator);
      appendMessage(
        "assistant",
        `⚠️ **Error connecting to assistant:** ${err.message}. Please verify the Python server is running.`
      );
    } finally {
      setInputDisabled(false);
    }
  });

  // Handle quick prompt chips click
  chipsContainer.addEventListener("click", (e) => {
    const chip = e.target.closest(".prompt-chip");
    if (!chip) return;
    const query = chip.getAttribute("data-query");
    if (query) {
      sendMessageDirectly(query);
    }
  });

  // Handle in-bubble suggestion clicks
  messagesContainer.addEventListener("click", (e) => {
    const btn = e.target.closest(".suggestion-btn");
    if (!btn) return;
    const query = btn.getAttribute("data-query");
    if (query) {
      sendMessageDirectly(query);
    }
  });

  function sendMessageDirectly(text) {
    messageInput.value = text;
    chatForm.dispatchEvent(new Event("submit"));
  }

  function renderWelcomeMessage() {
    const welcomeText = 
      "👋 **Welcome to the AI Virtual Assistant!**\n\n" +
      "I am a student-built academic project created to demonstrate 13 classical AI algorithms:\n" +
      "• **Search algorithms**: Depth-First Search (DFS), Breadth-First Search (BFS), Iterative Deepening (IDS), A*, D*, Hill Climbing, Simulated Annealing\n" +
      "• **AI problems**: Wumpus World, 8-Puzzle, Towers of Hanoi\n" +
      "• **Probabilistic AI**: Bayesian Network, Expectation-Maximization (EM), Hidden Markov Model (HMM)\n\n" +
      "You can ask questions like `\"Run BFS\"`, `\"Solve an 8 puzzle\"`, `\"Explain HMM\"`, or click any of the example prompts above.";

    const initialSuggestions = [
      "Run BFS",
      "Solve an 8 puzzle",
      "Show Towers of Hanoi",
      "Explain the Hidden Markov Model",
      "Demonstrate Wumpus World"
    ];

    appendMessage("assistant", welcomeText, initialSuggestions);
  }

  function appendMessage(sender, text, suggestions = []) {
    const row = document.createElement("div");
    row.className = `message-row ${sender}`;

    const avatar = document.createElement("div");
    avatar.className = `avatar ${sender === "user" ? "user-avatar" : "bot-avatar"}`;
    avatar.textContent = sender === "user" ? "You" : "AI";

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    if (sender === "user") {
      bubble.textContent = text;
    } else {
      bubble.innerHTML = formatAssistantMarkdown(text);

      if (suggestions && suggestions.length > 0) {
        const suggContainer = document.createElement("div");
        suggContainer.className = "bubble-suggestions";
        suggestions.forEach((sug) => {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "suggestion-btn";
          btn.setAttribute("data-query", sug);
          btn.textContent = sug;
          suggContainer.appendChild(btn);
        });
        bubble.appendChild(suggContainer);
      }
    }

    row.appendChild(avatar);
    row.appendChild(bubble);
    messagesContainer.appendChild(row);
    scrollToBottom();
  }

  function showTypingIndicator() {
    const row = document.createElement("div");
    row.className = "message-row assistant typing-row";

    const avatar = document.createElement("div");
    avatar.className = "avatar bot-avatar";
    avatar.textContent = "AI";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerHTML = "<em>Thinking & computing demonstration...</em>";

    row.appendChild(avatar);
    row.appendChild(bubble);
    messagesContainer.appendChild(row);
    scrollToBottom();
    return row;
  }

  function removeTypingIndicator(el) {
    if (el && el.parentNode) {
      el.parentNode.removeChild(el);
    }
  }

  function setInputDisabled(disabled) {
    messageInput.disabled = disabled;
    sendBtn.disabled = disabled;
    if (!disabled) {
      messageInput.focus();
    }
  }

  function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  /**
   * Safe and simple markdown-to-HTML formatter for academic chat
   */
  function formatAssistantMarkdown(text) {
    // Escape HTML tags first
    let escaped = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    // Replace code blocks: ```lang ... ```
    escaped = escaped.replace(/```(?:[a-zA-Z0-9]+)?\n([\s\S]*?)```/g, (match, code) => {
      return `<pre><code>${code.trim()}</code></pre>`;
    });

    // Replace inline code: `code`
    escaped = escaped.replace(/`([^`]+)`/g, "<code>$1</code>");

    // Replace bold: **text**
    escaped = escaped.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

    // Replace headers: ### Header
    escaped = escaped.replace(/^### (.*$)/gim, "<h3>$1</h3>");

    // Bullet points: • item
    escaped = escaped.replace(/^[•*] (.*$)/gim, "<li>$1</li>");
    escaped = escaped.replace(/(<li>.*<\/li>)/gms, "<ul>$1</ul>");

    // Convert newlines to paragraphs/linebreaks
    const paragraphs = escaped
      .split(/\n\n+/)
      .map((p) => {
        p = p.trim();
        if (p.startsWith("<pre>") || p.startsWith("<h3>") || p.startsWith("<ul>")) {
          return p;
        }
        return `<p>${p.replace(/\n/g, "<br>")}</p>`;
      })
      .join("");

    return paragraphs;
  }
});

