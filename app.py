from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

historical_data = {
    "offers": []
}

@app.route("/", methods=["GET"])
def health():
    return {"status": "TLC Prediction Engine is LIVE"}

@app.route("/api/chat/predict", methods=["POST"])
def chat_predict():
    data = request.get_json() or {}
    prompt = data.get("prompt", "").lower()

    if not historical_data["offers"]:
        return jsonify({
            "reply": "No historical data found yet.",
            "confidence": "LOW"
        })

    offers = sorted(historical_data["offers"], key=lambda x: x.get("revenue", 0))
    best = offers[-1]
    worst = offers[0]

    reply = f"Best offer: {best.get('name')} (${best.get('revenue')})"
    return jsonify({"reply": reply, "confidence": "MEDIUM"})
