import csv
from datetime import datetime

def log_profit(symbol, profit):
    with open("profits.csv","a",newline="") as file:
        writer=csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),symbol,profit])
    print(f"💰 {symbol} Profit: {profit}$ logged.")
