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
# OFFER DATA (NO ML)
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


@app.route("/api/offers/predict", methods=["POST"])
def predict_offers():
    return jsonify({
        "error": "Prediction engine disabled (ML not connected yet)"
    }), 503


# =========================
# EMAIL DATA (NO ML)
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
# CAMPAIGN DATA (NO ML)
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
