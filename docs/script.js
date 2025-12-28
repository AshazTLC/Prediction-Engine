from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# In-memory storage
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
    data = request.json.get("data", [])

    if not isinstance(data, list):
        return jsonify({"error": "Data must be a list"}), 400

    historical_data["offers"].extend(data)

    return jsonify({
        "message": "Offer data uploaded",
        "total": len(historical_data["offers"])
    })


# =========================
# OFFER PREDICTION (WORKING)
# =========================
@app.route("/api/offers/predict", methods=["POST"])
def predict_offers():

    offers = historical_data["offers"]

    if not offers:
        return jsonify({
            "error": "No historical offer data available"
        }), 400

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


# =========================
# START SERVER
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
