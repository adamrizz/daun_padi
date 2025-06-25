from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ROBOFLOW_API_URL = "https://detect.roboflow.com/penyakit-daun-padi-kumqp/1?api_key=gyZFta9jhWeEDO9nlnZo"

@app.route("/")
def home():
    return "YOLO Flask Backend is running"

@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    response = requests.post(
        ROBOFLOW_API_URL,
        files={"file": file}
    )

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
