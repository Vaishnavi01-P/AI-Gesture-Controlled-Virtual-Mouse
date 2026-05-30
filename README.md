# Virtual Mouse Using OpenCV - Complete Edition

A comprehensive virtual mouse application that uses hand tracking to control your computer without physical mouse interaction. This project combines basic mouse functionality with advanced gesture recognition and dual-hand control.

## 🎯 Project Description

This project transforms your hand into a virtual mouse using computer vision and machine learning. The system uses your webcam to detect hand movements and gestures, allowing you to:

- **Move the cursor** using your index finger
- **Click** by bringing index and middle fingers together
- **Perform system shortcuts** using specific hand gestures
- **Control with both hands** for advanced functionality
- **Drag and drop** using pinch gestures

## ✨ Features

### 🎯 Basic Mouse Functionality
- **👆 Fore finger (Index)** → Move cursor around the screen
- **👆👆 Fore + Middle finger together** → Click functionality
- **📦 Bounding box** around detected hand
- **📏 Distance detection** between fingers for precise clicking
- **🎯 Smooth cursor movement** with anti-shake algorithm

### 🎮 Advanced Gesture Recognition
- **✌️ Victory Sign** (Index + Middle finger up) → Take Screenshot
- **🤟 Rock Sign** (Index + Pinky finger up) → Mute/Unmute Audio
- **👊 Fist** (All fingers down) → Lock Screen
- **✋ Open Palm** (All fingers up) → Enable/Pause Mouse Control

### 🤏 Drag & Drop with Pinch Gesture
- **Pinch gesture** (Thumb + Index finger close) → Grab and drag items
- **Move hand while pinching** to drag objects
- **Release pinch** to drop items

### 🔧 Dual-Hand Mode
- **Left Hand ✋ Open Palm** → Enable/Pause mouse control
- **Right Hand 👆 Index Finger** → Control cursor movement and clicks
- **Independent hand tracking** for complex operations

### 📊 Visual Feedback System
- **Real-time status display** showing mouse state
- **Gesture feedback** with confirmation messages
- **Hand count indicator** for multi-hand detection
- **Distance measurements** for precise control
- **FPS counter** for performance monitoring
- **Comprehensive instructions** displayed on screen

## 🚀 Quick Start

### Installation
```bash
# Install required dependencies
pip install -r requirements.txt

# Or install individually
pip install opencv-python mediapipe autopy pyautogui numpy
```

### Running the Application
```bash
python "Virtual Mouse ALL FEATURES.py"
```

## 📋 Requirements

### Python Dependencies
- **OpenCV** (opencv-python) - Computer vision library
- **MediaPipe** (mediapipe) - Hand tracking and gesture recognition
- **AutoPy** (autopy) - Mouse and keyboard automation
- **PyAutoGUI** (pyautogui) - System shortcuts and screenshots
- **NumPy** (numpy) - Mathematical operations

### System Requirements
- **Python 3.7+** (compatible with newer versions)
- **Webcam** for hand detection
- **Windows/Linux/Mac** support
- **Good lighting** for optimal hand detection

## 🎮 How to Use

### Basic Mouse Control
1. **Enable Mouse Control:**
   - Show **left hand open palm** (all fingers up)
   - You'll see "Mouse control: ENABLED"

2. **Move Cursor:**
   - Use **right hand index finger** to move mouse
   - Keep other fingers down for precise control

3. **Click:**
   - Use **right hand index + middle finger** together
   - Bring them close (distance < 40 pixels) to click

### Advanced Gestures
- **✌️ Victory Sign** → Take screenshot (saved with timestamp)
- **🤟 Rock Sign** → Toggle audio mute/unmute
- **👊 Fist** → Lock computer screen
- **🤏 Pinch** → Drag and drop functionality

### Visual Indicators
- **Green Box** = Right hand detected
- **Blue Box** = Left hand detected
- **Purple Circle** = Cursor movement active
- **Yellow Circles** = Pinch gesture detected
- **Status Text** = Current mode and feedback

## 🔧 Technical Details

### Hand Detection
- Uses **MediaPipe** for robust hand tracking
- Supports **up to 2 hands** simultaneously
- **Automatic left/right hand** classification
- **Real-time gesture recognition** with cooldown periods

### Gesture Recognition
- **Multi-finger detection** for complex gestures
- **Distance-based clicking** for precise control
- **Gesture cooldown** to prevent accidental triggers
- **Visual feedback** for all gestures

### System Integration
- **Screenshot capture** with timestamp
- **Audio control** using system shortcuts
- **Screen lock** using OS commands
- **Drag & drop** with full mouse simulation

## 🛠️ Customization

### Adjusting Sensitivity
Edit these parameters in the code:
```python
smoothening = 8         # Cursor movement smoothing
frameR = 100            # Frame rate
pinch_distance < 50     # Pinch gesture sensitivity
length < 40            # Click distance threshold
```

### Camera Settings
```python
width = 640             # Camera width
height = 480            # Camera height
```

## 🐛 Troubleshooting

### Common Issues
1. **Hands not detected:**
   - Ensure good lighting
   - Keep hands clearly visible in camera frame
   - Check camera permissions

2. **Gestures not working:**
   - Wait for gesture cooldown period
   - Ensure proper finger positioning
   - Check if mouse control is enabled

3. **Camera not working:**
   - Close other applications using camera
   - Try different camera index (0, 1, 2)
   - Run as administrator if needed

4. **System shortcuts not working:**
   - Run as administrator for system-level operations
   - Check Windows permissions

### Performance Tips
- Use good lighting conditions
- Keep hands within camera frame
- Avoid rapid gesture changes
- Close unnecessary applications

## 📁 Project Structure

```
Virtual-Mouse-using-OpenCV-main/
├── Virtual Mouse ALL FEATURES.py    # Main application (ALL FEATURES)
├── HandTracking.py                  # Hand detection and gesture recognition
├── requirements.txt                 # Python dependencies
├── Virtual Mouse.py                 # Original basic version
└── README_COMPLETE.md              # This documentation
```

## 🎉 Feature Summary

✅ **Multi-hand detection** and tracking  
✅ **Advanced gesture recognition** with visual feedback  
✅ **System shortcuts** (screenshot, audio, lock)  
✅ **Drag & drop** with pinch gestures  
✅ **Dual-hand coordination** for advanced control  
✅ **Real-time visual feedback** and status display  
✅ **Configurable sensitivity** settings  
✅ **Cross-platform compatibility**  
✅ **Smooth cursor movement** with anti-shake  
✅ **Distance-based precision** control  

## 🔮 Future Enhancements

- Voice commands integration
- Custom gesture programming
- Multi-monitor support
- Gesture recording and playback
- Advanced drag & drop with visual indicators
- Machine learning-based gesture improvement

## 📫 Contact

For questions, issues, or contributions, please contact:
- **Email:** chhxnshah@gmail.com
- **GitHub:** [HxnDev](https://github.com/HxnDev)
- **LinkedIn:** [Hassan Shahzad](https://www.linkedin.com/in/hassan-shahzad-2a6617212/)

---

**Note:** This enhanced version maintains backward compatibility with the original virtual mouse while adding powerful new features for advanced hand gesture control. The system works with Python 3.7+ and doesn't require version downgrading.


