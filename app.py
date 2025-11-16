import os
from flask import Flask, send_from_directory

# المسار الأساسي (الفولدر فيه app.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# المسار الصحيح للفرونت
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")

app = Flask(__name__)

# ============================
# الصفحة الرئيسية index.html
# ============================
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

# ============================
# تقديم بقية الصفحات
# ============================
@app.route('/<path:page>')
def serve_page(page):
    file_path = os.path.join(FRONTEND_DIR, page)
    if os.path.exists(file_path):
        return send_from_directory(FRONTEND_DIR, page)
    else:
        return "404 - Page Not Found", 404

# ============================
# تقديم ملفات assets (css/js/img)
# ============================
@app.route('/assets/<path:path>')
def serve_assets(path):
    return send_from_directory(ASSETS_DIR, path)

# ============================
# تشغيل الخادم على Render
# ============================
from datetime import datetime
from cryptography.fernet import Fernet
import sqlite3
import os

FERNET_KEY = os.environ.get("FERNET_KEY") or Fernet.generate_key()
fernet = Fernet(FERNET_KEY)

DB_PATH = "database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            exchange TEXT,
            api_key_encrypted TEXT,
            api_secret_encrypted TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_current_user_id():
    return 1

@app.route("/api/connect-exchange", methods=["POST"])
def connect_exchange():
    data = request.get_json() or {}
    exchange = data.get("exchange")
    api_key  = data.get("api_key")
    api_secret = data.get("api_secret")

    if not exchange or not api_key or not api_secret:
        return jsonify({"status": "error", "message": "بيانات غير مكتملة."}), 400

    user_id = get_current_user_id()

    api_key_enc = fernet.encrypt(api_key.encode()).decode()
    api_secret_enc = fernet.encrypt(api_secret.encode()).decode()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("DELETE FROM user_api_keys WHERE user_id=? AND exchange=?", (user_id, exchange))

    c.execute("""
        INSERT INTO user_api_keys (user_id, exchange, api_key_encrypted, api_secret_encrypted, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, exchange, api_key_enc, api_secret_enc, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
