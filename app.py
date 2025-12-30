from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# =========================
# In-memory storage
# =========================
historical_data = {
    "offers": []
}

# =========================
# UI ROUTES
# =========================
@app.route("/")
def chat():
    return render_template("chat.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/reports")
def reports():
    return render_template("reports.html")

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
# CHAT AI PREDICTION
# =========================
@app.route("/api/chat/predict", methods=["POST"])
def chat_predict():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "").lower()

    offers = historical_data["offers"]

    if not offers:
        return jsonify({
            "reply": "I don’t have enough historical data yet. Please upload offer data first.",
            "confidence": "LOW"
        })

    sorted_offers = sorted(offers, key=lambda x: x.get("revenue", 0))
    best_offer = sorted_offers[-1]
    worst_offer = sorted_offers[0]

    total = len(offers)

    confidence = "HIGH" if total >= 6 else "MEDIUM" if total >= 3 else "LOW"

    if "dead" in prompt or "low" in prompt:
        reply = f"""
⚠️ Offer likely to go dead:
{worst_offer.get('name')}

Revenue: ${worst_offer.get('revenue', 0):,}
Confidence: {confidence}
"""
        return jsonify({"reply": reply, "confidence": confidence})

    reply = f"""
🚀 Best performing offer (next 90 days):
{best_offer.get('name')}

Estimated Revenue: ${best_offer.get('revenue', 0):,}
Confidence: {confidence}
"""
    return jsonify({"reply": reply, "confidence": confidence})

# =========================
# ENTRYPOINT
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
