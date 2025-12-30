from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
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

    # Sort offers by revenue
    sorted_offers = sorted(offers, key=lambda x: x.get("revenue", 0))
    best_offer = sorted_offers[-1]
    worst_offer = sorted_offers[0]
    mid_offer = sorted_offers[len(sorted_offers)//2]

    total = len(offers)

    def confidence_level(count):
        if count >= 6:
            return "HIGH"
        elif count >= 3:
            return "MEDIUM"
        else:
            return "LOW"

    confidence = confidence_level(total)

    # Dead offer logic
    if "dead" in prompt or "low" in prompt:
        reply = (
            f"⚠️ '{worst_offer.get('name')}' is likely to go dead in the next 30 days.\n\n"
            f"Revenue: ${worst_offer.get('revenue', 0):,}\n"
            f"Confidence: {confidence}"
        )
        return jsonify({"reply": reply, "confidence": confidence})

    # Best offer logic
    if "best" in prompt or "90" in prompt:
        reply = (
            f"🚀 '{best_offer.get('name')}' is expected to perform best in the next 90 days.\n\n"
            f"Estimated Revenue: ${best_offer.get('revenue', 0):,}\n"
            f"Confidence: {confidence}"
        )
        return jsonify({"reply": reply, "confidence": confidence})

    # Default response
    reply = (
        f"📊 Performance Overview:\n\n"
        f"Best: {best_offer.get('name')} (${best_offer.get('revenue', 0):,})\n"
        f"Average: {mid_offer.get('name')} (${mid_offer.get('revenue', 0):,})\n"
        f"Weak: {worst_offer.get('name')} (${worst_offer.get('revenue', 0):,})\n\n"
        f"Confidence: {confidence}"
    )

    return jsonify({"reply": reply, "confidence": confidence})

# =========================
# START SERVER (RAILWAY)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
