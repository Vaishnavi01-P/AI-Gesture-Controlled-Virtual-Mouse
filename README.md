# AI Gesture-Controlled Virtual Mouse Using OpenCV & MediaPipe

A computer vision-based virtual mouse system that enables touchless cursor control using real-time hand gesture recognition. Built with OpenCV, MediaPipe, and Python, this project allows users to interact with their computers without a physical mouse.

---

## 🎯 Project Overview

This project transforms your hand into a virtual mouse using real-time hand tracking and gesture recognition. The system captures video from a webcam, detects hand landmarks, and interprets gestures to perform mouse actions such as cursor movement, clicking, dragging, scrolling, and executing system shortcuts.

The application provides a natural and intuitive human-computer interaction experience while demonstrating the capabilities of computer vision and gesture-based control systems.

---

## ✨ Features

### 🎯 Basic Mouse Controls

* 👆 Move cursor using the index finger
* 👆👆 Left click by bringing index and middle fingers together
* 📦 Real-time hand detection with bounding box visualization
* 📏 Finger distance measurement for precise click detection
* 🎯 Smooth cursor movement with anti-shake filtering

### 🎮 Advanced Gesture Recognition

* ✌️ Victory Sign (Index + Middle Finger Up) → Take Screenshot
* 🤟 Rock Sign (Index + Pinky Finger Up) → Mute / Unmute Audio
* 👊 Fist Gesture → Lock Screen
* ✋ Open Palm → Enable / Pause Mouse Control

### 🤏 Drag and Drop Support

* Pinch Gesture (Thumb + Index Finger Close) → Grab Objects
* Move hand while pinching to drag items
* Release pinch gesture to drop items

### 🔧 Dual-Hand Mode

* ✋ Left Hand Open Palm → Enable / Disable Mouse Control
* 👆 Right Hand Index Finger → Cursor Movement
* 👆👆 Right Hand Index + Middle Finger → Mouse Click
* Enhanced control using both hands simultaneously

---

## 🛠️ Tech Stack

* Python
* OpenCV
* MediaPipe
* NumPy
* PyAutoGUI
* Computer Vision
* Hand Tracking
* Gesture Recognition

---

## 📂 Project Structure

```text
AI-Gesture-Controlled-Virtual-Mouse/
│
├── HandTracking.py
├── Virtual Mouse.py
├── Virtual Mouse ALL FEATURES.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI-Gesture-Controlled-Virtual-Mouse.git
cd AI-Gesture-Controlled-Virtual-Mouse
```

### 2. Create Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate the environment:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Basic Version:

```bash
python "Virtual Mouse.py"
```

Advanced Version:

```bash
python "Virtual Mouse ALL FEATURES.py"
```

---

## 🎥 How It Works

1. Webcam captures real-time video.
2. MediaPipe detects hand landmarks.
3. Finger positions are analyzed.
4. Gestures are recognized.
5. Corresponding mouse or system actions are executed.
6. Cursor movements are smoothed for better user experience.

---

## 📚 Learning Outcomes

Through this project, I gained practical experience in:

* Real-time hand tracking using MediaPipe
* Computer vision techniques with OpenCV
* Gesture recognition systems
* Human-computer interaction design
* Mouse automation using PyAutoGUI
* Image processing and landmark detection
* Real-time application development

---

## 🚀 Future Enhancements

* Multi-monitor support
* Custom gesture mapping
* Gesture-based volume control
* Gesture-based presentation controller
* AI-powered gesture customization
* Mobile camera integration

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

## 👨‍💻 Developed By

**Vaishnavi Padmashali**
