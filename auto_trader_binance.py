import os, ccxt, time, requests
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/api/trader")

BINANCE_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET = os.getenv("BINANCE_SECRET_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"

exchange = ccxt.binance({
    'apiKey': BINANCE_KEY,
    'secret': BINANCE_SECRET,
    'enableRateLimit': True,
})

def send_tg(msg):
    """إرسال رسالة تنبيه إلى تليجرام"""
    if not BOT_TOKEN or not CHAT_ID:
        print("[TG] Bot not configured")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def safe_log(msg):
    print(f"[SmartBot Trader] {msg}")
    send_tg(msg)

def get_balance():
    try:
        balance = exchange.fetch_balance()
        return round(balance['total'].get('USDT', 0), 2)
    except Exception as e:
        safe_log(f"❌ خطأ في جلب الرصيد: {e}")
        return 0

def execute_trade(symbol, side, amount):
    safe_log(f"🔁 تنفيذ {side} {symbol} بقيمة {amount}")
    if DRY_RUN:
        safe_log(f"🚧 وضع التجربة مفعل (لن يتم تنفيذ أي أمر حقيقي).")
        return {"demo": True, "symbol": symbol, "side": side, "amount": amount}
    try:
        if side == "BUY":
            order = exchange.create_market_buy_order(symbol, amount)
        else:
            order = exchange.create_market_sell_order(symbol, amount)
        safe_log(f"✅ تمت العملية بنجاح {side} {symbol}")
        return order
    except Exception as e:
        safe_log(f"❌ خطأ في التنفيذ: {e}")
        return {"error": str(e)}

def monitor_trade(symbol, entry_price, tp_percent, sl_percent):
    """مراقبة الصفقة تلقائياً"""
    safe_log(f"📈 بدء مراقبة {symbol} | TP {tp_percent}% / SL {sl_percent}%")
    while True:
        try:
            ticker = exchange.fetch_ticker(symbol)
            price = ticker['last']
            change = ((price - entry_price) / entry_price) * 100

            if change >= tp_percent:
                msg = f"🎯 Take Profit: {symbol} +{change:.2f}% — بيع الآن"
                safe_log(msg)
                execute_trade(symbol, "SELL", 0.99)
                break

            elif change <= -sl_percent:
                msg = f"🛑 Stop Loss: {symbol} {change:.2f}% — تم البيع لتقليل الخسارة"
                safe_log(msg)
                execute_trade(symbol, "SELL", 0.99)
                break

            safe_log(f"{symbol} التغير: {change:.2f}% (TP {tp_percent}% / SL {sl_percent}%)")
            time.sleep(30)

        except Exception as e:
            safe_log(f"⚠️ خطأ بالمراقبة: {e}")
            time.sleep(60)

@router.post("/run")
def run_trade(symbol: str = "BTC/USDT", action: str = "BUY", risk: float = 2.0,
              tp_percent: float = 3.0, sl_percent: float = 2.0):
    """
    تشغيل التداول الآلي مع إشعارات Telegram و TP/SL
    """
    usdt = get_balance()
    if usdt <= 10:
        msg = "🚫 رصيد USDT غير كافٍ للتداول"
        safe_log(msg)
        return {"error": msg}

    ticker = exchange.fetch_ticker(symbol)
    price = ticker['last']
    amount = round((usdt * (risk / 100)) / price, 6)

    result = execute_trade(symbol, action, amount)
    if action == "BUY":
        msg = f"🟢 شراء {symbol} بسعر {price:.2f}$، بدأ المراقبة..."
        safe_log(msg)
        monitor_trade(symbol, price, tp_percent, sl_percent)
    return {
        "trade": result,
        "symbol": symbol,
        "amount": amount,
        "TP%": tp_percent,
        "SL%": sl_percent
    }
