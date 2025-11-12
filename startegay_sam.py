import pandas as pd

def compute_indicators(df: pd.DataFrame, rsi_window=14, sma_fast=20, sma_slow=50):
    df = df.copy()
    df["sma_fast"] = df["close"].rolling(sma_fast).mean()
    df["sma_slow"] = df["close"].rolling(sma_slow).mean()

    delta = df["close"].diff()
    up = (delta.clip(lower=0)).rolling(rsi_window).mean()
    down = (-delta.clip(upper=0)).rolling(rsi_window).mean()
    rs = up / (down.replace(0, 1e-9))
    df["rsi"] = 100 - (100 / (1 + rs))

    return df

def signal_from_row(row) -> str:
    if pd.isna(row.get("sma_fast")) or pd.isna(row.get("sma_slow")):
        return "HOLD"
    try:
        if row["sma_fast"] > row["sma_slow"] and (row.get("rsi", 50) > 50):
            return "BUY"
        if row["sma_fast"] < row["sma_slow"] or (row.get("rsi", 50) < 45):
            return "SELL"
        return "HOLD"
    except Exception:
        return "HOLD"
