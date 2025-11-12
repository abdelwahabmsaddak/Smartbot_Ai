import os, requests
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/api/telegram")
BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID=os.getenv("TELEGRAM_CHAT_ID")

@router.post("/notify")
def notify(msg:str="📈 تحديث جديد من SmartBot AI Trader"):
    if not (BOT_TOKEN and CHAT_ID):
        return {"error":"Telegram not configured"}
    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r=requests.post(url,data={"chat_id":CHAT_ID,"text":msg})
    return {"sent":r.ok}
