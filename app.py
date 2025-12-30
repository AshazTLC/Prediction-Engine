from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# IMPORTANT: explicitly define folders
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

CORS(app)

# =========================
# In-memory data
# =========================
historical_data = {
    "offers": []
}

# =========================
# HEALTH CHECK (REQUIRED)
# =========================
@app.route("/health")
def health():
    return "OK", 200

# =========================
# UI ROUTES
# =========================
@app.route("/")
def chat():
    return render_template("chat.html")

@app.route("/dashboard")
def dashboard():
    return "Dashboard coming soon"

@app.route("/reports")
def reports():
    return "Reports coming soon"

# =========================
# CHAT AI API
# =========================
@app.route("/api/chat/predict", methods=["POST"])
def chat_predict():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "")

    if not historical_data["offers"]:
        return jsonify({
            "reply": "No historical data found. Please upload data first.",
            "confidence": "LOW"
        })

    offers = sorted(historical_data["offers"], key=lambda x: x.get("revenue", 0))
    best = offers[-1]

    reply = (
        f"🚀 Best performing offer:\n\n"
        f"{best.get('name')} → ${best.get('revenue', 0)}\n\n"
        f"Confidence: MEDIUM"
    )

    return jsonify({
        "reply": reply,
        "confidence": "MEDIUM"
    })
