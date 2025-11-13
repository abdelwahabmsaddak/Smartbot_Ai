import os
import aiohttp

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")  # رقمك: 21650222766 ليس هو الـ chat_id. استخدم @userinfobot لمعرفة الـ id أو حط آيدي قناة/جروب.

async def notify_telegram(text: str):
    if not (BOT_TOKEN and CHAT_ID):
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    async with aiohttp.ClientSession() as s:
        async with s.post(url, json=payload, timeout=10) as r:
            # تجاهل الأخطاء بصمت
            _ = await r.text()
  
