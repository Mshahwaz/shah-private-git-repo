from flask import Flask, jsonify
app = Flask(__name__)

@app.get("/")
def hello():
    return jsonify(
        message="✨ Welcome to Cloud ✨",
        tip="Built with Flask, shipped by Jenkins, running in Docker.--> V.1",
        UI="This is new feature added on request of customer"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
