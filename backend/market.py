
import requests

def get_prices():
    try:
        data = requests.get("https://api.binance.com/api/v3/ticker/price").json()
        btc = next(x for x in data if x["symbol"]=="BTCUSDT")["price"]
        eth = next(x for x in data if x["symbol"]=="ETHUSDT")["price"]
        gold = "Coming soon"
        sp = "Coming soon"

        return {
            "btc": float(btc),
            "eth": float(eth),
            "gold": gold,
            "sp": sp
        }
    except:
        return {"btc":0,"eth":0,"gold":0,"sp":0}      
