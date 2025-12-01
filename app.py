from flask import Flask, request, jsonify
from flask_cors import CORS
import chatbot_logic
import os

app = Flask(_name_)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Chatbot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    # Force JSON parsing because Render often sends None
    data = request.get_json(force=True, silent=True)

    print("RAW DATA RECEIVED:", data)  # Debug (remove later)

    if not data:
        return jsonify({"reply": "Backend received no JSON!"})

    message = data.get("message", "").strip()
    reply = chatbot_logic.get_response(message)
    return jsonify({"reply": reply})

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
