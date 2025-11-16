from flask import Flask, request, jsonify
import openai
import requests

app = Flask(__name__)

openai.api_key = "YOUR_OPENAI_KEY"

# -------------------------------
# 1) تحليل العملات الرقمية
# -------------------------------
@app.post("/api/analyze")
def analyze():
    data = request.json
    asset = data.get("asset")

    prompt = f"حلل حركة {asset} الآن وأعطني الاتجاه والتوقع ونسبة الثقة."

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return jsonify({
        "trend": "صعود" if "صعود" in response.choices[0].message["content"] else "هبوط",
        "analysis": response.choices[0].message["content"],
        "confidence": 87
    })

# -------------------------------
# 2) تحليل الذهب والأسهم
# -------------------------------
@app.post("/api/analyze_gold")
def analyze_gold():
    market = request.json.get("market")

    prompt = f"حلل سوق {market} الآن وأعطني الاتجاه والتوقع."

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return jsonify({
        "trend": "صعود",
        "summary": response.choices[0].message["content"]
    })

# -------------------------------
# 3) تتبع الحيتان (ضخ – بيع – بلد)
# -------------------------------
@app.post("/api/whales")
def whales():
    asset = request.json.get("asset")

    # نموذج مبدئي – عندما نربطه بالمنصة نزيد الدقة
    return jsonify({
        "buy": "1.9M USD",
        "sell": "800K USD",
        "country": "Singapore"
    })

# -------------------------------
# 4) توليد تدوينة بالذكاء الاصطناعي
# -------------------------------
@app.post("/api/blog")
def blog():
    prompt = "اكتب تدوينة قصيرة عن آخر تحركات سوق العملات الرقمية."

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return jsonify({
        "title": "تحليل جديد للسوق",
        "content": response.choices[0].message["content"]
    })

# -------------------------------
# 5) الدردشة داخل الموقع
# -------------------------------
@app.post("/api/chat")
def chat():
    msg = request.json.get("message")

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":msg}]
    )

    return jsonify({
        "reply": response.choices[0].message["content"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
