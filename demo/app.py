from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/hello")
def hello():
    return jsonify(message="Hello, World!")

@app.route("/")
def index():
    return "Hello, this is the backend API server!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
