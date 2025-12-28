"""
Flask web API for Prediction Engine
Deploy to Railway.app or any cloud platform
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# In-memory storage
trained_models = {}
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
        "trained_models": list(trained_models.keys()),
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
    data = request.json.get("data", [])
    if not isinstance(data, list):
        return jsonify({"error": "Data must be a list"}), 400

    historical_data["offers"].extend(data)
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

    if len(offers) == 0:
        return jsonify({
            "error": "No historical offer data available"
        }), 400

    clicks = [o.get("clicks", 0) for o in offers]
    conversions = [o.get("conversions", 0) for o in offers]
    revenue = [o.get("revenue", 0) for o in offers]

    avg_clicks = np.mean(clicks)
    avg_conversions = np.mean(conversions)
    avg_revenue = np.mean(revenue)

    prediction = {
        "predicted_clicks": int(avg_clicks * 1.05),
        "predicted_conversions": int(avg_conversions * 1.07),
        "predicted_revenue": int(avg_revenue * 1.10),
        "confidence": round(min(0.95, 0.6 + (len(offers) * 0.05)), 2),
        "based_on_records": len(offers)
    }

    return jsonify(prediction)


# =========================
# 🧠 AI CHAT PREDICTION
# =========================
@app.route("/api/chat/predict", methods=["POST"])
def chat_predict():
    data = request.json or {}
    prompt = data.get("prompt", "").lower()

    offers = historical_data["offers"]

    if not offers:
        return jsonify({
            "reply": "I don’t have enough data yet. Please upload offer data first.",
            "confidence": 0
        })

    # Find best offer by revenue
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
# EMAIL DATA
# =========================
@app.route("/api/email/upload", methods=["POST"])
def upload_email_data():
    data = request.json.get("data", [])
    if not isinstance(data, list):
        return jsonify({"error": "Data must be a list"}), 400

    historical_data["email_creatives"].extend(data)
    return jsonify({
        "message": "Email data uploaded",
        "total": len(historical_data["email_creatives"])
    })


@app.route("/api/email/predict", methods=["POST"])
def predict_email():
    return jsonify({
        "error": "Prediction engine disabled (ML not connected yet)"
    }), 503


# =========================
# CAMPAIGN DATA
# =========================
@app.route("/api/campaigns/upload", methods=["POST"])
def upload_campaign_data():
    data = request.json.get("data", [])
    if not isinstance(data, list):
        return jsonify({"error": "Data must be a list"}), 400

    historical_data["campaigns"].extend(data)
    return jsonify({
        "message": "Campaign data uploaded",
        "total": len(historical_data["campaigns"])
    })


@app.route("/api/campaigns/predict", methods=["POST"])
def predict_campaigns():
    return jsonify({
        "error": "Prediction engine disabled (ML not connected yet)"
    }), 503


# =========================
# RAILWAY START
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
