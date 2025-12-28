"""
Flask web API for Prediction Engine
Deploy to Railway.app
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# =========================
# In-memory storage
# =========================
historical_data = {
    "offers": [],
    "email_creatives": [],
    "campaigns": []
}

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return jsonify({
        "message": "Prediction Engine API is LIVE 🚀",
        "version": "1.0.0",
        "status": "working"
    })


# =========================
# MODEL STATUS
# =========================
@app.route("/api/models/status", methods=["GET"])
def get_model_status():
    return jsonify({
        "data_counts": {
            "offers": len(historical_data["offers"]),
            "email_creatives": len(historical_data["email_creatives"]),
            "campaigns": len(historical_data["campaigns"])
        }
    })


# =========================
# OFFER DATA UPLOAD
# =========================
@app.route("/api/offers/upload", methods=["POST"])
def upload_offer_data():
    data = request.get_json(silent=True) or {}
    offers = data.get("data", [])

    if not isinstance(offers, list):
        return jsonify({"error": "Data must be a list"}), 400

    historical_data["offers"].extend(offers)

    return jsonify({
        "message": "Offer data uploaded",
        "total": len(historical_data["offers"])
    })


# =========================
# OFFER PREDICTION
# =========================
@app.route("/api/offers/predict", methods=["POST"])
def predict_offers():
    offers = historical_data["offers"]

    if not offers:
        return jsonify({"error": "No historical offer data available"}), 400

    total_clicks = sum(o.get("clicks", 0) for o in offers)
    total_revenue = sum(o.get("revenue", 0) for o in offers)
    count = len(offers)

    predicted_clicks = int(total_clicks / count)
    predicted_conversions = int(predicted_clicks * 0.08)
    predicted_revenue = int(total_revenue / count)

    confidence = round(min(0.95, 0.6 + count * 0.05), 2)

    return jsonify({
        "predicted_clicks": predicted_clicks,
        "predicted_conversions": predicted_conversions,
        "predicted_revenue": predicted_revenue,
        "confidence": confidence,
        "based_on_records": count
    })


# =========================
# CHAT PREDICTION (AI STYLE)
# =========================
@app.route("/api/chat/predict", methods=["POST"])
def chat_predict():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "").lower()

    offers = historical_data["offers"]

    if not offers:
        return jsonify({
            "reply": "I don’t have enough data yet. Please upload offer data first.",
            "confidence": 0
        })

    # Best offer by revenue
    best_offer = max(offers, key=lambda x: x.get("revenue", 0))
    total = len(offers)

    confidence = round(min(0.95, 0.6 + total * 0.05), 2)

    reply = (
        f"Based on {total} historical offers, "
        f"'{best_offer.get('name', 'Top Offer')}' is expected to perform best "
        f"in the next 90 days with an estimated revenue of "
        f"${best_offer.get('revenue', 0):,}. "
        f"Confidence level is {int(confidence * 100)}%."
    )

    return jsonify({
        "reply": reply,
        "top_offer": best_offer.get("name"),
        "confidence": confidence
    })

# =========================
# CHAT PREDICTION API
# =========================
@app.route("/api/chat/predict", methods=["POST"])
def chat_predict():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"reply": "Please ask a valid question."})

    offers = historical_data["offers"]

    if not offers:
        return jsonify({
            "reply": "I don’t have enough historical offer data yet. Please upload offer data first."
        })

    total_clicks = sum(o.get("clicks", 0) for o in offers)
    total_revenue = sum(o.get("revenue", 0) for o in offers)
    count = len(offers)

    predicted_clicks = int(total_clicks / count)
    predicted_revenue = int(total_revenue / count)
    confidence = round(min(0.95, 0.6 + count * 0.05), 2)

    reply = f"""
Based on analysis of {count} past offers:

• Expected clicks: {predicted_clicks}
• Expected revenue: ₹{predicted_revenue}
• Confidence level: {confidence * 100}%

This offer type is likely to perform well in the next 30–90 days.
"""

    return jsonify({"reply": reply})

# =========================
# START SERVER
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
