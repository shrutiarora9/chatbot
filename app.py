from flask import Flask, request, jsonify
from flask_cors import CORS

import chatbot_logic
import os

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return "Chatbot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    reply = chatbot_logic.get_response(message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
     port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

