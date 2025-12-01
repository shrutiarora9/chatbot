from flask import Flask, request, jsonify
from flask_cors import CORS
import chatbot_logic
import os
import json

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Chatbot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    print("------ NEW REQUEST RECEIVED ------")

    # 1️⃣ Try normal JSON first
    data = request.get_json(silent=True)
    print("JSON parsed:", data)

    # 2️⃣ If JSON is None, try raw body
    if data is None:
        try:
            raw = request.data.decode("utf-8")
            print("RAW BODY:", raw)
            data = json.loads(raw)
        except:
            pass

    # 3️⃣ If still nothing, try form-data
    if not data:
        print("FORM DATA:", dict(request.form))
        data = dict(request.form)

    print("FINAL DATA:", data)

    if not data:
        return jsonify({"reply": "No data received by backend."})

    message = data.get("message", "").strip()
    print("MESSAGE RECEIVED:", message)

    reply = chatbot_logic.get_response(message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
