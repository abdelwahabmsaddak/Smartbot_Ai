# =========================================================
# SmartBot AI Trader – Main Backend
# =========================================================

from flask import Flask, request, jsonify, render_template
from ai_engine import analyze_with_ai
from trading_engine import analyze_market
from whales_tracker import get_whales_data
import os

app = Flask(__name__)


# ====================== ROUTES ===========================

@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    item = data.get("item", "")

    if item.strip() == "":
        return jsonify({"error": "يرجى إدخال اسم العملة أو السهم"}), 400

    ai_result = analyze_with_ai(item)
    market_data = analyze_market(item)

    return jsonify({
        "item": item,
        "ai_analysis": ai_result,
        "market": market_data
    })


@app.route("/whales")
def whales():
    return jsonify(get_whales_data())


@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "")
    if msg.strip() == "":
        return jsonify({"response": "لم أفهم… أعد صياغة سؤالك"}), 200

    # AI REPLY
    ai_reply = analyze_with_ai(msg)
    return jsonify({"response": ai_reply})


# ====================== RUN APP ===========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
