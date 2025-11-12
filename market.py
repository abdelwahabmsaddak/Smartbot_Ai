# =========================
# 📂 FILE: api/services/market.py
# =========================
import os, httpx

COINGECKO = os.getenv("COINGECKO_BASE", "https://api.coingecko.com/api/v3")

async def fetch_trending():
    url = f"{COINGECKO}/search/trending"
    async with httpx.AsyncClient(timeout=20) as c:
        r = await c.get(url)
        r.raise_for_status()
        raw = r.json().get("coins", [])
    out = []
    for item in raw:
        i = item.get("item", {})
        out.append({"id": i.get("id"),
                    "symbol": i.get("symbol","").upper(),
                    "name": i.get("name")})
    return out

async def market_history(coin_id: str, vs: str="usd", days: int=7):
    url = f"{COINGECKO}/coins/{coin_id}/market_chart"
    params = {"vs_currency": vs, "days": days}
    async with httpx.AsyncClient(timeout=20) as c:
        r = await c.get(url, params=params)
        r.raise_for_status()
        prices = r.json().get("prices", [])
    return [p[1] for p in prices]

def _sma(data, w):
    return sum(data[-w:]) / w if len(data) >= w else None

def _momentum(data, n=12):
    return (data[-1] - data[-n]) / data[-n] if len(data) > n else 0

def analyze_signals(series):
    if len(series) < 30: return "HOLD", 0.0
    s10, s30 = _sma(series, 10), _sma(series, 30)
    m = _momentum(series, 12)
    score = 0.0
    score += 0.6 if s10 and s30 and s10 > s30 else -0.6
    score += 0.4 if m > 0 else -0.4
    if score > 0.4: return "BUY", score
    if score < -0.4: return "SELL", score
    return "HOLD", score
      
