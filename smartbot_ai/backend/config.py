import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")
    BINANCE_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_SECRET = os.getenv("BINANCE_SECRET_KEY")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    PAYPAL_ID = os.getenv("PAYPAL_CLIENT_ID")
    PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
  
