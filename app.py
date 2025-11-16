import os
from flask import Flask, send_from_directory

# مسار المشروع
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")

# نطفي static الافتراضي ونستعمل المسارات متاعنا
app = Flask(__name__, static_folder=None)

# ================== الصفحة الرئيسية ==================
@app.route("/")
def index():
    # يرجع frontend/index.html
    return send_from_directory(FRONTEND_DIR, "index.html")

# ================== الملفات الثابتة ==================
@app.route("/assets/<path:filename>")
def assets(filename):
    # يرجع CSS / JS / صور من frontend/assets
    return send_from_directory(ASSETS_DIR, filename)

# ================== باقي الصفحات ==================
@app.route("/<path:path>")
def pages(path):
    """
    يخدم:
    /pricing.html      -> frontend/pricing.html
    /pricing           -> frontend/pricing.html
    /blog.html         -> frontend/blog.html
    /blog              -> frontend/blog.html
    /whales.html       -> frontend/whales.html
    ...
    """
    # لو ما فيهاش نقطة وما تنتهيش بـ .html نزيدولها .html
    if "." not in path and not path.endswith(".html"):
        filename = path + ".html"
    else:
        filename = path

    file_path = os.path.join(FRONTEND_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(FRONTEND_DIR, filename)

    return "404 - Page Not Found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
