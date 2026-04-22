from flask import Flask, render_template, request, jsonify, session
import os
from vertexai.generative_models import GenerativeModel, GenerationConfig
from dotenv import load_dotenv
import vertexai

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("flask_secret_key", os.urandom(24))

project_id = os.getenv("project_id")
region = os.getenv("region", "us-central1")

vertexai.init(project=project_id, location=region)

SYSTEM_INSTRUCTION = """You are a helpful, knowledgeable, and friendly AI assistant powered by Google Gemini.
- Be concise but thorough.
- Use markdown formatting when it improves readability (code blocks, lists, bold text).
- If you don't know something, say so honestly.
- Keep a conversational, approachable tone."""

model = GenerativeModel(
    "gemini-2.0-flash",
    system_instruction=SYSTEM_INSTRUCTION,
    generation_config=GenerationConfig(
        temperature=0.7,
        max_output_tokens=2048,
    )
)

chat_sessions = {}


def get_chat(session_id):
    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat()
    return chat_sessions[session_id]


@app.route("/")
def home():
    if "session_id" not in session:
        session["session_id"] = os.urandom(16).hex()
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = (data or {}).get("message", "").strip()

    if not user_input:
        return jsonify(content="Please enter a message."), 400

    session_id = session.get("session_id", "default")
    chat_session = get_chat(session_id)

    try:
        response = chat_session.send_message(user_input)
        return jsonify(content=response.text)
    except Exception as e:
        return jsonify(content=f"Error: {str(e)}"), 500


@app.route("/clear", methods=["POST"])
def clear():
    session_id = session.get("session_id", "default")
    chat_sessions.pop(session_id, None)
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
