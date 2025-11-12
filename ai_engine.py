import os, httpx
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/api/ai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","")

@router.get("/analyze/{symbol}")
async def analyze(symbol: str):
    if not OPENAI_API_KEY:
        return {"error":"API key missing"}
    headers={"Authorization":f"Bearer {OPENAI_API_KEY}","Content-Type":"application/json"}
    payload={"model":"gpt-5-turbo","input":f"حلل العملة {symbol} وأعطني توصية مختصرة."}
    async with httpx.AsyncClient(timeout=60) as cx:
        r=await cx.post("https://api.openai.com/v1/responses",headers=headers,json=payload)
    data=r.json()
    return {"symbol":symbol.upper(),"ai":data.get("output_text","لا توجد بيانات حالياً.")}
