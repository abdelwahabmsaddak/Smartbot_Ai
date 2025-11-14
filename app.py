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
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
