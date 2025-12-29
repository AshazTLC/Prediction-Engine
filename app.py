from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

historical_data = {
    "offers": []
}

# =========================
# DASHBOARD UI
# =========================
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# =========================
# UPLOAD OFFER DATA
# =========================
@app.route("/api/offers/upload", methods=["POST"])
def upload_offer_data():
    data = request.get_json(silent=True) or {}
    offers = data.get("data", [])

    if not isinstance(offers, list):
        return jsonify({"error": "Data must be a list"}), 400

    historical_data["offers"].extend(offers)

    return jsonify({
        "message": "Offer data uploaded successfully",
        "total_records": len(historical_data["offers"])
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
            "reply": "No historical data found. Upload offer data first.",
            "confidence": "LOW"
        })

    sorted_offers = sorted(offers, key=lambda x: x.get("revenue", 0))
    best = sorted_offers[-1]
    worst = sorted_offers[0]
    mid = sorted_offers[len(sorted_offers)//2]
    total = len(offers)

    if total >= 6:
        confidence = "HIGH"
    elif total >= 3:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    if "dead" in prompt or "stop" in prompt:
        reply = (
            f"🚨 DEAD OFFER ALERT\n\n"
            f"Offer: {worst['name']}\n"
            f"Revenue: ${worst['revenue']:,}\n"
            f"Confidence: {confidence}"
        )
        return jsonify({"reply": reply})

    if "best" in prompt or "perform" in prompt:
        reply = (
            f"🚀 TOP PERFORMER\n\n"
            f"Offer: {best['name']}\n"
            f"Expected Revenue (90 days): ${best['revenue']:,}\n"
            f"Confidence: {confidence}"
        )
        return jsonify({"reply": reply})

    reply = (
        f"📊 PERFORMANCE SUMMARY\n\n"
        f"Best: {best['name']} (${best['revenue']:,})\n"
        f"Average: {mid['name']} (${mid['revenue']:,})\n"
        f"Weak: {worst['name']} (${worst['revenue']:,})\n\n"
        f"Confidence: {confidence}"
    )

    return jsonify({"reply": reply})

# =========================
# START SERVER
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
