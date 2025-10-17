# 🎛️ Smart Volume Control v3

Control your computer’s volume using **hand gestures** — no keyboard, no mouse, just pure AI magic.

Built with **OpenCV, MediaPipe, and Python**, this project uses real-time hand-tracking to detect finger distance and dynamically adjust system volume.

---

## 🚀 Features

- ✅ Real-time hand tracking using MediaPipe Hands  
- ✅ Smooth volume adjustment based on finger distance  
- ✅ Works on Windows, Linux, and macOS  
- ✅ Lightweight and fast — runs on CPU  
- ✅ Intuitive gesture control (thumb–index distance)  
- ✅ Live FPS counter for performance feedback  

---

## 🧠 Tech Stack

| Component       | Description                        |
|-----------------|------------------------------------|
| Python          | Core programming language           |
| OpenCV          | Real-time video capture & processing|
| MediaPipe       | Hand landmark detection             |
| PyCaw (Windows) | Volume control API                  |
| NumPy           | Mathematical operations             |

---

## ⚙️ Installation

### Clone the repository
```bash
git clone https://github.com/Dubal-prayag/Smart-Volume-Control-v3.git
cd Smart-Volume-Control-v3

Install dependencies
pip install -r requirements.txt

Run the app
python volume_control.py


Make sure your webcam is connected and you’re in a well-lit environment for best results.

🖐️ How It Works

Open your webcam.

Show your thumb and index finger.

The system measures the distance:

🔊 Increase distance → Volume goes up

🔉 Decrease distance → Volume goes down

Real-time volume feedback is displayed on screen.

| Gesture              | Action                |
| -------------------- | --------------------- |
| 🤏 Close fingers     | Volume ↓              |
| ✋ Open fingers       | Volume ↑              |
| ✌️ Hand not detected | Volume stays constant |

📦 Folder Structure

Smart-Volume-Control-v3/
│
├── volume_control_using_hand/
│   ├── volume_control.py
│   ├── HandTrackingModule.py
│   └── ...
│
├── assets/
│   └── demo.png
│
├── requirements.txt
└── README.md

🧰 Requirements

Python 3.8+
Webcam
Works best under good lighting conditions


