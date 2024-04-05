#!/usr/bin/env python
import torch
from torchvision import models, transforms
from PIL import Image
from transformers import ResNetForImageClassification, ConvNextFeatureExtractor

from flask import Flask, render_template, request, jsonify

import random
import string
import hashlib
import os

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 4096 * 4096
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

ANGULAR_LEAF_SPOT_PREDICTION = 0
BEAN_RUST_PREDICTION = 1
HEALTHY_PREDICTION = 2

id2label = {
    ANGULAR_LEAF_SPOT_PREDICTION: "angular_leaf_spot",
    BEAN_RUST_PREDICTION: "bean_rust",
    HEALTHY_PREDICTION: "healthy"
}

model_path = "fxmarty/resnet-tiny-beans"
model = ResNetForImageClassification.from_pretrained(model_path)
feature_extractor = ConvNextFeatureExtractor(do_resize=True, do_normalize=True, image_mean=[0.45, 0.45, 0.45], image_std=[0.22, 0.22, 0.22])

def predict_image(image):

    if image.mode != 'RGB':
        image = image.convert('RGB')
    inputs = feature_extractor(images=image, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    predictions = outputs.logits.softmax(dim=-1)
    predicted_class_idx = predictions.argmax(-1).item()

    return predicted_class_idx

@app.route('/')
def challenge_desc():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if 'healthyLeaf' not in request.files or 'rustLeaf' not in request.files:
        return jsonify({"error": "Missing files"}), 400
    file1 = request.files['healthyLeaf']
    file2 = request.files['rustLeaf']
    fname1 = ''.join(random.choices(string.ascii_letters, k=8)) + '.jpg'
    fname2 = ''.join(random.choices(string.ascii_letters, k=8)) + '.jpg'
    file1.save(fname1)
    file2.save(fname2)
    img1 = Image.open(file1.stream)
    img2 = Image.open(file2.stream)

    same_file = hashlib.md5(open(fname1, 'rb').read()).hexdigest() == hashlib.md5(open(fname2, 'rb').read()).hexdigest()
    img1_prediction = predict_image(img1)
    img2_prediction = predict_image(img2)
    if os.path.isfile(fname1):
        os.remove(fname1)
    if os.path.isfile(fname2):
        os.remove(fname2)
    if same_file and img1_prediction == HEALTHY_PREDICTION and img2_prediction == BEAN_RUST_PREDICTION:
        return render_template('result_cm9ja3NhcmVoYXJk.html')
    else:
        return jsonify({"File1": id2label[img1_prediction], "File2": id2label[img2_prediction], "SameImage": same_file}), 400


if __name__ == "__main__":
    app.run()
