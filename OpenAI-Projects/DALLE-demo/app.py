import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generateimages/<prompt>')
def generate(prompt):
    print("prompt:", prompt)
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        n=5,
        size="256x256"
    )
    return jsonify({"data": [{"url": img.url} for img in response.data]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
