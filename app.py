from flask import Flask, render_template, request, jsonify
import os
from market import get_prices
from ai_engine import analyze_crypto, analyze_gold, analyze_stock
from whales import get_whale_data
from chatbot_engine import chat_ai
from telegram_bot import telegram_send_message

app = Flask(__name__, static_folder="assets", template_folder=".")

# ========================= ROUTES ========================= #

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/payment")
def payment():
    return render_template("payment.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/notifications")
def notifications():
    return render_template("notifications.html")

@app.route("/support")
def support():
    return render_template("support.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/analyze")
def analyze_page():
    return render_template("analyze.html")

@app.route("/analyze_gold")
def analyze_gold_page():
    return render_template("analyze_gold.html")

@app.route("/whales")
def whales_page():
    return render_template("whales.html")

@app.route("/how_it_works")
def how_page():
    return render_template("how_it_works.html")

@app.route("/connect_exchange")
def connect_exchange():
    return render_template("connect_exchange.html")

# ========================= API ENDPOINTS ========================= #

@app.route("/api/chat", methods=["POST"])
def api_chat():
    msg = request.json.get("message")
    reply = chat_ai(msg)
    return jsonify({"reply": reply})

@app.route("/api/prices")
def api_prices():
    return jsonify(get_prices())

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    coin = request.json.get("symbol")
    result = analyze_crypto(coin)
    return jsonify(result)

@app.route("/api/analyze_gold", methods=["POST"])
def api_analyze_gold():
    result = analyze_gold()
    return jsonify(result)

@app.route("/api/analyze_stock", methods=["POST"])
def api_analyze_stock():
    stock = request.json.get("symbol")
    result = analyze_stock(stock)
    return jsonify(result)

@app.route("/api/whales")
def api_whales():
    return jsonify(get_whale_data())

@app.route("/api/telegram", methods=["POST"])
def api_telegram():
    msg = request.json.get("message")
    telegram_send_message(msg)
    return jsonify({"status": "sent"})

# ========================= RUN SERVER ========================= #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
