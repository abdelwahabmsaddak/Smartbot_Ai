from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_folder="frontend/assets", template_folder="frontend")

# ================================
# ROUTES FOR MAIN PAGES
# ================================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/register.html")
def register():
    return render_template("register.html")

@app.route("/pricing.html")
def pricing():
    return render_template("pricing.html")

@app.route("/analyze.html")
def analyze():
    return render_template("analyze.html")

@app.route("/analyze_gold.html")
def analyze_gold():
    return render_template("analyze_gold.html")

@app.route("/connect_exchange.html")
def connect_exchange():
    return render_template("connect_exchange.html")

@app.route("/dashboard.html")
def dashboard():
    return render_template("dashboard.html")

@app.route("/blog.html")
def blog():
    return render_template("blog.html")

@app.route("/faq.html")
def faq():
    return render_template("faq.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/how_it_works.html")
def how_it_works():
    return render_template("how_it_works.html")

@app.route("/payment.html")
def payment():
    return render_template("payment.html")

@app.route("/whales.html")
def whales():
    return render_template("whales.html")

@app.route("/profile.html")
def profile():
    return render_template("profile.html")

@app.route("/billing.html")
def billing():
    return render_template("billing.html")

@app.route("/upgrade.html")
def upgrade():
    return render_template("upgrade.html")

# ================================
# STATIC FILES (CSS / JS / IMAGES)
# ================================
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('frontend/assets', filename)

# ================================
# RUN SERVER
# ================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
