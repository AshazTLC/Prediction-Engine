const API_URL = "https://thelewadsconenterprises.com/api/chat/predict";

const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = `msg ${type}`;
  chatMessages.appendChild(div);

  if (type === "ai") {
    typeEffect(div, text);
  } else {
    div.textContent = text;
  }

  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function typeEffect(element, text) {
  let i = 0;
  element.textContent = "";

  const interval = setInterval(() => {
    element.textContent += text.charAt(i);
    i++;
    chatMessages.scrollTop = chatMessages.scrollHeight;
    if (i >= text.length) clearInterval(interval);
  }, 18);
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  userInput.value = "";

  const thinking = document.createElement("div");
  thinking.className = "msg ai";
  thinking.textContent = "Thinking...";
  chatMessages.appendChild(thinking);

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: text })
    });

    const data = await res.json();
    chatMessages.removeChild(thinking);
    addMessage(data.reply || "No response.", "ai");

  } catch (err) {
    thinking.textContent = "Server error. Try again.";
  }
}

sendBtn.onclick = sendMessage;
userInput.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});
