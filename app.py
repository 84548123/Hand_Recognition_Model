import flask
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import base64
import logging
import mediapipe as mp

# Set up logging to provide clear output
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)

# --- 1. INITIALIZE MEDIAPE HANDS MODEL ---
mp_hands = mp.solutions.hands

# THE FIX IS ON THIS LINE: static_image_mode is now set to True
# This tells MediaPipe to treat each image independently, which solves the timestamp error.
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.7)

print("✅ MediaPipe Hands model loaded successfully.")


# --- 2. GESTURE RECOGNITION LOGIC ---
def landmarks_to_gesture(landmarks):
    """Takes hand landmarks and returns a string representing the gesture."""
    try:
        # Get the coordinates of the fingertips and other key points
        thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
        
        index_mcp = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

        # Rule for "Fist"
        if (index_tip.y > index_mcp.y and
            middle_tip.y > index_mcp.y and
            ring_tip.y > index_mcp.y and
            pinky_tip.y > index_mcp.y):
            return "Fist"

        # Rule for "Open Palm" (Five)
        if (index_tip.y < index_mcp.y and
            middle_tip.y < index_mcp.y and
            ring_tip.y < index_mcp.y and
            pinky_tip.y < index_mcp.y):
            return "Open Palm"
            
        # Rule for "Peace"
        if (index_tip.y < index_mcp.y and
            middle_tip.y < index_mcp.y and
            ring_tip.y > index_mcp.y and
            pinky_tip.y > index_mcp.y):
            return "Peace Sign"
            
        # Rule for "Like" (Thumbs Up)
        if (thumb_tip.y < index_mcp.y and
            index_tip.y > index_mcp.y and
            middle_tip.y > index_mcp.y):
            return "Like"

        return "Unknown Gesture"
        
    except Exception as e:
        print(f"Error in gesture logic: {e}")
        return "Error"


# --- 3. PREDICTION FUNCTION ---
def process_and_predict(image_data):
    """Decodes image data, uses MediaPipe to find landmarks, and determines the gesture."""
    try:
        header, encoded = image_data.split(",", 1)
        decoded_image = base64.b64decode(encoded)
        image_np = np.frombuffer(decoded_image, dtype=np.uint8)
        img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Failed to decode image.")
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            gesture = landmarks_to_gesture(hand_landmarks)
            return gesture, 1.0
        else:
            return "No Gesture", 0.0

    except Exception as e:
        print(f"❌ An error occurred during prediction: {e}")
        return None, 0.0

# --- 4. FLASK ROUTES (Unchanged) ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if 'image' not in data:
            return jsonify({"error": "No image data found"}), 400

        gesture, confidence = process_and_predict(data['image'])
        
        if gesture is None:
            return jsonify({"error": "Failed to process image"}), 500

        return jsonify({'gesture': gesture, 'confidence': confidence})

    except Exception as e:
        print(f"❌ Error in /predict endpoint: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

# --- 5. RUN THE FLASK APP (Unchanged) ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


#port: http://127.0.0.1:5000
