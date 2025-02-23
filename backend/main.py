from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
import cv2
import mediapipe as mp
import base64
import io
from PIL import Image

app = Flask(__name__)
CORS(app)  # Allow frontend to access the backend

# Load trained model
MODEL_PATH = r"C:\Users\IRA SURATI\Desktop\GestureDetection\backend\sign_language_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

if model:
    print("Model loaded successfully.") 

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.5)

# Gesture labels (should match the labels used in training)
GESTURES = ["hello", "thanks", "yes", "no", "please"]

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json.get("image")
    if not data:
        return jsonify({"error": "No image provided"}), 400

    # Decode base64 image
    image_bytes = base64.b64decode(data.split(",")[1])
    image = Image.open(io.BytesIO(image_bytes))
    image = np.array(image)

    # Convert to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = [coord for lm in hand_landmarks.landmark for coord in (lm.x, lm.y, lm.z)]
            
            # Convert landmarks to numpy and reshape for model prediction
            landmarks = np.array(landmarks).reshape(1, -1)
            prediction = model.predict(landmarks)
            gesture = GESTURES[np.argmax(prediction)]

            return jsonify({"gesture": gesture})

    return jsonify({"gesture": "Unknown"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
