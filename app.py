from flask import Flask, render_template, request
import requests
import base64
import os
from PIL import Image, ImageDraw

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

API_KEY = "gyZFta9jhWeEDO9nlnZo"
MODEL_ENDPOINT = f"https://detect.roboflow.com/penyakit-daun-padi-kumqp/7?api_key={API_KEY}"

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil = None
    image_path = None
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Baca dan encode ke base64
            with open(filepath, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode("utf-8")

            # Kirim ke Roboflow
            response = requests.post(
                MODEL_ENDPOINT,
                data=img_base64,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            hasil = response.json()

            # Tambah bounding box ke gambar
            if "predictions" in hasil and hasil["predictions"]:
                image = Image.open(filepath).convert("RGB")
                draw = ImageDraw.Draw(image)

                for pred in hasil["predictions"]:
                    x = pred["x"]
                    y = pred["y"]
                    w = pred["width"]
                    h = pred["height"]
                    class_name = pred["class"]
                    conf = pred["confidence"]

                    left = x - w / 2
                    top = y - h / 2
                    right = x + w / 2
                    bottom = y + h / 2

                    draw.rectangle([left, top, right, bottom], outline="red", width=2)
                    draw.text((left, top - 10), f"{class_name} ({conf:.2f})", fill="red")

                # Simpan gambar hasil ke static folder
                result_path = os.path.join(app.config['STATIC_FOLDER'], 'hasil.jpg')
                image.save(result_path)
                image_path = 'static/hasil.jpg'

    return render_template('index.html', hasil=hasil, image_path=image_path)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
