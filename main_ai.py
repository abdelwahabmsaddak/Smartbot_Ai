from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_engine import router as ai_router
from telegram_bot import router as telegram_router
from trading import router as trader_router

app = FastAPI(title="SmartBot AI Trader API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True
)

app.include_router(ai_router)
app.include_router(telegram_router)
app.include_router(trader_router)

@app.get("/")
def root():
    return {"msg": "SmartBot AI Trader API Running ✅"}
