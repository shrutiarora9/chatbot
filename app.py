from flask import Flask, request, jsonify
import chatbot_logic

app = Flask(__name__)

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
    app.run(host="0.0.0.0", port=10000)
