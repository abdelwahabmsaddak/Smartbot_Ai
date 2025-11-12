from flask import Blueprint, request, jsonify
import openai, os

chat_ai = Blueprint('chat_ai', __name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@chat_ai.route("/api/chat", methods=["POST"])
def chat():
    msg = request.json.get("message")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"system","content":"أنت مساعد تداول ذكي."},
                  {"role":"user","content":msg}]
    )
    return jsonify({"reply": response["choices"][0]["message"]["content"]})
