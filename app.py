from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

historical_data = {
    "offers": []
}

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/api/chat/predict", methods=["POST"])
def chat_predict():
    data = request.get_json() or {}
    message = data.get("message", "").lower()

    if not historical_data["offers"]:
        return jsonify({
            "reply": "No historical data yet. Please upload offer data.",
            "confidence": "LOW"
        })

    offers = sorted(historical_data["offers"], key=lambda x: x.get("revenue", 0))
    best = offers[-1]

    return jsonify({
        "reply": f"Best performing offer is {best.get('name')} with revenue ${best.get('revenue')}",
        "confidence": "MEDIUM"
    })
