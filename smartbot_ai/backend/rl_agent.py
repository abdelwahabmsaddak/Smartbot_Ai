import pandas as pd

class SimpleRLAgent:
    """وكيل مبدئي: يختبر حدود RSI ويختار أفضل زوج (buy_rsi, sell_rsi) على بيانات تاريخية."""
    def __init__(self):
        self.buy_rsi = 52.0
        self.sell_rsi = 45.0

    def fit(self, df: pd.DataFrame):
        best_buy = self.buy_rsi
        best_sell = self.sell_rsi
        best_score = -1e9
        for b in range(48, 60):
            for s in range(40, 50):
                if s >= b:
                    continue
                score = 0.0
                pos = None
                entry = 0.0
                for _, r in df.iterrows():
                    rsi = r.get("rsi", 50)
                    price = r["close"]
                    if pos is None and rsi >= b:
                        pos = price; entry = price
                    elif pos is not None and rsi <= s:
                        score += (price - entry)
                        pos = None
                if score > best_score:
                    best_score = score
                    best_buy = float(b)
                    best_sell = float(s)
        self.buy_rsi = best_buy
        self.sell_rsi = best_sell

    def act(self, last_row) -> str:
        rsi = last_row.get("rsi", 50)
        if rsi >= self.buy_rsi:
            return "BUY"
        if rsi <= self.sell_rsi:
            return "SELL"
        return "HOLD"
              
