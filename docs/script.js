const API_URL = "https://theleadsconenterprises.com/api/chat/predict";

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

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: text })
    });

    const data = await res.json();
    typing.remove();
    addMessage(data.reply || "No response.", "bot");

  } catch (err) {
    typing.innerText = "Server error. Try again.";
  }
}

userInput.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});
