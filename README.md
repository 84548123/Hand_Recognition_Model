# ✋ Real-Time Hand Tracking & Gesture Recognition

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Google-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📖 Overview

This project implements a real-time computer vision system that detects hands, tracks 21 distinct landmarks on the fingers/palm, and classifies specific hand gestures (e.g., "Thumbs Up", "Open Palm", "Fist").

Leveraging **Google's MediaPipe** framework and **OpenCV**, this application runs efficiently on a standard CPU, enabling touchless control interfaces or sign language interpretation prototypes.

---

## ✨ Key Features

* **⚡ High-Performance Tracking:** Detects single or multiple hands with low latency (30+ FPS).
* **📍 Landmark Detection:** Accurately maps 21 3D coordinates for each hand.
* **✌️ Gesture Recognition:** Identifies gestures based on the geometric relationship between finger tips.
* **🎮 Application Ready:** Modular design that can be easily integrated into games or virtual mouse control.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Vision Framework:** MediaPipe (Solutions API)
* **Image Processing:** OpenCV (`cv2`)
* **Math/Logic:** NumPy, Math

---

## 🧠 How It Works

The system operates in a three-stage pipeline:

1.  **Detection:** The model analyzes the video frame to locate the hand Region of Interest (ROI).
2.  **Landmark Extraction:** It identifies 21 key points (knuckles, fingertips, wrist).
3.  **Gesture Logic:** By calculating the Euclidean distance between specific landmarks (e.g., thumb tip vs. index tip), the code determines the state of the hand (Open vs. Closed).



---

## 🚀 Installation & Usage

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/hand-recognition.git](https://github.com/yourusername/hand-recognition.git)
cd hand-recognition

📂 Project Structure
Plaintext

hand-recognition/
├── src/
│   ├── HandTrackingModule.py  # Class for MediaPipe detection logic
│   └── main.py                # Main script running the webcam loop
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
📸 Screenshots
Landmark Tracking
Visualizing the 21-point skeleton overlay.

Gesture Classification
System recognizing a "Three Fingers" gesture.

🔮 Future Improvements
Virtual Mouse: Map finger movement to the mouse cursor to control the OS.

Volume Control: Use the distance between Thumb and Index finger to adjust system volume.

ASL Alphabet: Expand the gesture library to recognize American Sign Language letters.

🤝 Contributing
Contributions are welcome! Please open an issue if you encounter bugs or want to suggest new gestures.

```bash
git clone [https://github.com/yourusername/hand-recognition.git](https://github.com/yourusername/hand-recognition.git)
cd hand-recognition
