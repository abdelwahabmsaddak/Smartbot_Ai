import random, time
from fastapi import APIRouter
router = APIRouter(prefix="/api/trader")

balance = 1000
profit_today = 0
coins = ["BTC","ETH","BNB","FLOKI","PEPE"]

@router.get("/run")
def auto_trade():
    global profit_today
    coin=random.choice(coins)
    signal=random.choice(["BUY","SELL"])
    change=random.uniform(-2,3)
    profit_today+=change
    return {
        "coin":coin,
        "signal":signal,
        "change":round(change,2),
        "profit_today":round(profit_today,2)
  }
  
