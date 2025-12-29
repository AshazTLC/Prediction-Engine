const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");

function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = type === "user" ? "user-msg" : "bot-msg";
  div.innerText = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  userInput.value = "";

  const typing = document.createElement("div");
  typing.className = "bot-msg typing";
  typing.innerText = "AI is thinking...";
  chatBox.appendChild(typing);

  const res = await fetch("/api/predict", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ prompt: text })
  });

  const data = await res.json();
  chatBox.removeChild(typing);

  addMessage(data.answer || "No response", "bot");
}

