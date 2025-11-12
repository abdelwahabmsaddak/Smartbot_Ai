from flask import Blueprint, request, jsonify
import paypalrestsdk, os

payment_api = Blueprint('payment_api', __name__)

paypalrestsdk.configure({
  "mode": "sandbox",
  "client_id": os.getenv("PAYPAL_CLIENT_ID"),
  "client_secret": os.getenv("PAYPAL_SECRET")
})

@payment_api.route("/api/payment_success", methods=["POST"])
def payment_success():
    data = request.get_json()
    print(f"✅ Payment from {data.get('user')} successful.")
    return jsonify({"message": "Payment recorded successfully"}), 200
  
