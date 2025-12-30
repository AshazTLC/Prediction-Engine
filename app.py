from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

historical_data = {
    "offers": []
}

@app.route("/")
def chat():
    return render_template("chat.html")

@app.route("/dashboard")
def dashboard():
    return "Dashboard coming soon"

@app.route("/reports")
def reports():
    return "Reports coming soon"

@app.route("/api/chat/predict", methods=["POST"])
def chat_predict():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "").lower()

    if not historical_data["offers"]:
        return jsonify({
            "reply": "No historical data found. Please upload data first.",
            "confidence": "LOW"
        })

    offers = sorted(historical_data["offers"], key=lambda x: x.get("revenue", 0))
    best = offers[-1]
    worst = offers[0]

    reply = f"Best offer: {best.get('name')} (${best.get('revenue')})"
    return jsonify({"reply": reply, "confidence": "MEDIUM"})

# ❌ DO NOT use app.run() in Railway
