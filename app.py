from flask import Flask, request, render_template, redirect, url_for
import cv2
import numpy as np
import torch

app = Flask(__name__)

# Load your pre-trained AI model (replace 'your_model_path' with the actual path or URL)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='"C:\Users\user\Downloads\furniture.h5"')

# Function to detect furniture
def detect_furniture(image_path):
    image = cv2.imread(image_path)
    results = model(image)
    return results.xyxy[0]  # returns bounding boxes and confidence

# Function to overlay wall panel
def overlay_panel(image_path, panel_path):
    image = cv2.imread(image_path)
    panel = cv2.imread(panel_path)

    # Assuming the panel image has the same dimensions as the original image
    if image.shape[:2] != panel.shape[:2]:
        panel = cv2.resize(panel, (image.shape[1], image.shape[0]))

    combined_image = cv2.addWeighted(image, 0.5, panel, 0.5, 0)
    output_path = 'static/output.jpg'
    cv2.imwrite(output_path, combined_image)
    return output_path

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            image_path = 'static/' + file.filename
            file.save(image_path)

            # Detect furniture
            detections = detect_furniture(image_path)
            if len(detections) == 0:  # No furniture detected
                panel_path = 'static/panel.jpg'  # Example panel path
                output_path = overlay_panel(image_path, panel_path)
                return render_template('result.html', user_image=output_path)
            else:
                return "Furniture detected. Please upload a different image."

    return render_template('upload.html')

@app.route('/gallery')
def gallery():
    # Code to display wall panel gallery
    return render_template('gallery.html')

if __name__ == '__main__':
    app.run(debug=True)
