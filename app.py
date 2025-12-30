from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ======================
# HEALTH CHECK (CRITICAL)
# ======================
@app.route("/")
def home():
    return "TLC Prediction Engine is LIVE", 200

@app.route("/health")
def health():
    return "OK", 200

# ======================
# CHAT API
# ======================
@app.route("/api/chat/predict", methods=["POST"])
def chat_predict():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "")

    return jsonify({
        "reply": f"You asked: {prompt}",
        "confidence": "MEDIUM"
    })
