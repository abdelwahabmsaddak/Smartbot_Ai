from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_crypto(symbol):
    txt = f"حلل العملة الرقمية {symbol} بالتفصيل واعطني: الاتجاه – نقاط الدخول – نقاط الخروج – توقعات 24 ساعة."
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":txt}]
    )
    return {"analysis": r.choices[0].message["content"]}

def analyze_gold():
    txt = "حلل الذهب الآن وقدم توقعات قصيرة المدى."
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":txt}]
    )
    return {"analysis": r.choices[0].message["content"]}

def analyze_stock(symbol):
    txt = f"حلل السهم {symbol} وقدم الاتجاه والتوقعات."
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":txt}]
    )
    return {"analysis": r.choices[0].message["content"]}
