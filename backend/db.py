import sqlite3

def init_db():
    conn = sqlite3.connect('smartbot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        plan TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    c.execute('''CREATE TABLE IF NOT EXISTS daily_profits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        pnl REAL,
        user_id INTEGER)''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
