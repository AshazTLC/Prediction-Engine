from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://theleadsconenterprises.com/api/chat/predict"

@app.route("/")
def chat():
    return render_template("chat.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.json
    res = requests.post(API_URL, json=data)
    return jsonify(res.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

