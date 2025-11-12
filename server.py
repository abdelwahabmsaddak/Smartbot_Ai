# server/server.py
import os, csv
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN","")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID","")  # اختياري لإشعارات تلقرام

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

class ChatIn(BaseModel):
    message: str

class ProfitIn(BaseModel):
    date: str
    amount: float

@app.post("/chat")
async def chat(inb: ChatIn):
    msg = inb.message.strip()
    if not OPENAI_API_KEY:
        return JSONResponse({"reply":"⚠️ ضع OPENAI_API_KEY في .env لتفعيل الدردشة."})

    # استدعاء OpenAI Responses API (متوافق مع gpt-5)
    url = "https://api.openai.com/v1/responses"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type":"application/json"}
    payload = {
        "model": "gpt-5-turbo",
        "input": f"أنت مساعد تداول محترف. اشرح بإيجاز وبخطوات واضحة: {msg}"
    }
    async with httpx.AsyncClient(timeout=60) as cx:
        r = await cx.post(url, headers=headers, json=payload)
        if r.status_code >= 400:
            return JSONResponse({"reply": f"OpenAI error: {r.text[:200]}"},
                                status_code=500)
        data = r.json()
        reply = data.get("output_text","…")
    # إشعار تلغرام اختياري
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            await cx.post(tg_url, json={"chat_id": TELEGRAM_CHAT_ID, "text": f"User: {msg}\nAI: {reply}"})
        except Exception:
            pass
    return JSONResponse({"reply": reply})

@app.post("/profit")
async def profit(p: ProfitIn):
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", "profits.csv")
    new_file = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["date","amount"])
        w.writerow([p.date, p.amount])

    # تلغرام اختياري
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            async with httpx.AsyncClient(timeout=15) as cx:
                tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                await cx.post(tg_url, json={"chat_id": TELEGRAM_CHAT_ID,
                                            "text": f"Profit logged: {p.date} — {p.amount} USDT"})
        except Exception:
            pass

    return JSONResponse({"ok": True})

# تقديم ملفات ثابتة عند التشغيل المحلي البسيط
@app.get("/")
def root():
    return FileResponse("../index.html")
