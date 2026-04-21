from flask import Flask, render_template, request, jsonify
import os
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv
import vertexai

load_dotenv()

app = Flask(__name__)

project_id = os.getenv("project_id")
region = os.getenv("region")

vertexai.init(project=project_id, location=region)

model = GenerativeModel("gemini-1.5-flash")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/gemini", methods=["GET", "POST"])
def vertex_ai():
    if request.method == "GET":
        user_input = request.args.get("user_input", "")
    else:
        user_input = request.form["user_input"]

    if not user_input:
        return jsonify(content="Please enter a message.")

    try:
        response = model.generate_content(user_input)
        return jsonify(content=response.text)
    except Exception as e:
        return jsonify(content=f"Error: {str(e)}"), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
