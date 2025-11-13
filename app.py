import os
from flask import Flask, send_from_directory

# حساب مسار المشروع
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ⚠️ المسار الصحيح إلى الفرونت داخل GitHub
FRONTEND_DIR = os.path.join(BASE_DIR, "../Smartbot_Ai/frontend")
ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")

app = Flask(__name__)

# ============================
# صفحة الهوم index.html
# ============================
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

# ============================
# تقديم صفحات HTML الأخرى
# ============================
@app.route('/<path:path>')
def serve_page(path):
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.exists(file_path):
        return send_from_directory(FRONTEND_DIR, path)
    else:
        return "404 - Page Not Found", 404

# ============================
# تقديم ملفات assets (css/js/images)
# ============================
@app.route('/assets/<path:path>')
def serve_assets(path):
    return send_from_directory(ASSETS_DIR, path)

# ============================
# تشغيل السيرفر
# ============================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
