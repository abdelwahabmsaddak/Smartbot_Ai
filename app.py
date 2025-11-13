
import os
from flask import Flask, send_from_directory

# حساب المسارات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../smartbot_ai/frontend")
ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route('/<path:path>')
def serve_page(path):
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.exists(file_path):
        return send_from_directory(FRONTEND_DIR, path)
    else:
        return "404 - Page Not Found", 404

@app.route('/assets/<path:path>')
def serve_assets(path):
    return send_from_directory(ASSETS_DIR, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
