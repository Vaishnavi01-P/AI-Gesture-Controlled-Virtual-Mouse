import cv2  # Can be installed using "pip install opencv-python"
import mediapipe as mp  # Can be installed using "pip install mediapipe"
import time
import math
import numpy as np
import pyautogui  # For system shortcuts
import subprocess  # For system commands
import threading  # For non-blocking operations


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=False, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        
        # Gesture recognition variables
        self.gesture_history = []
        self.gesture_threshold = 5  # Frames to confirm gesture
        self.last_gesture_time = 0
        self.gesture_cooldown = 1.0  # Seconds between gestures
        
        # Dual-hand mode variables
        self.left_hand_active = False
        self.right_hand_active = False
        self.mouse_enabled = True
        
        # Pinch gesture variables
        self.pinch_threshold = 30
        self.is_pinching = False
        self.pinch_start_pos = None
        self.drag_mode = False

    def findHands(self, img, draw=True):    # Finds all hands in a frame
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):   # Fetches the position of hands
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)

        return self.lmList, bbox

    def findMultiHands(self, img, draw=True):   # Finds all hands and returns their data
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        hands_data = []
        if self.results.multi_hand_landmarks:
            for hand_idx, handLms in enumerate(self.results.multi_hand_landmarks):
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
                
                # Get hand landmarks
                xList = []
                yList = []
                lmList = []
                
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    xList.append(cx)
                    yList.append(cy)
                    lmList.append([id, cx, cy])
                
                # Calculate bounding box
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                bbox = xmin, ymin, xmax, ymax
                
                # Determine hand type (left or right)
                hand_type = self.getHandType(handLms, img.shape)
                
                hands_data.append({
                    'hand_idx': hand_idx,
                    'lmList': lmList,
                    'bbox': bbox,
                    'hand_type': hand_type,
                    'fingers': self.getFingersUp(lmList)
                })
                
                if draw:
                    # Color code hands
                    color = (0, 255, 0) if hand_type == 'right' else (255, 0, 0)
                    cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), color, 2)
                    cv2.putText(img, f"{hand_type.upper()} HAND", (xmin, ymin - 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        return img, hands_data

    def getHandType(self, handLms, img_shape):
        """Determine if hand is left or right based on landmark positions"""
        # Get wrist and middle finger base positions
        wrist = handLms.landmark[0]
        middle_base = handLms.landmark[9]
        
        # If middle finger base is to the right of wrist, it's a right hand
        if middle_base.x > wrist.x:
            return 'right'
        else:
            return 'left'

    def getFingersUp(self, lmList):
        """Get which fingers are up for a given hand"""
        fingers = []
        if len(lmList) < 21:  # Ensure we have all landmarks
            return [0, 0, 0, 0, 0]
            
        # Thumb
        if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers
        for id in range(1, 5):
            if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers

    def fingersUp(self):    # Checks which fingers are up
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):

            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # totalFingers = fingers.count(1)

        return fingers

    def findDistance(self, p1, p2, img, lmList=None, draw=True, r=15, t=3):   # Finds distance between two fingers
        if lmList is None:
            lmList = self.lmList if hasattr(self, 'lmList') else []
        
        if len(lmList) < max(p1, p2) + 1:
            return 0, img, [0, 0, 0, 0, 0, 0]
            
        x1, y1 = lmList[p1][1:]
        x2, y2 = lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]

    def recognizeGesture(self, fingers):
        """Recognize specific gestures based on finger positions"""
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return None
            
        # Victory sign (index and middle finger up, others down)
        if fingers == [0, 1, 1, 0, 0]:
            return "victory"
        
        # Rock sign (index and pinky up, others down)
        elif fingers == [0, 1, 0, 0, 1]:
            return "rock"
        
        # Fist (all fingers down)
        elif fingers == [0, 0, 0, 0, 0]:
            return "fist"
        
        # Open palm (all fingers up)
        elif fingers == [1, 1, 1, 1, 1]:
            return "open_palm"
        
        # Pinch gesture (thumb and index finger close)
        elif fingers == [1, 1, 0, 0, 0]:
            return "pinch"
        
        return None

    def executeGestureAction(self, gesture, hand_type="right"):
        """Execute system actions based on recognized gestures"""
        current_time = time.time()
        
        if gesture == "victory":
            self.takeScreenshot()
            self.last_gesture_time = current_time
            return "Screenshot taken!"
            
        elif gesture == "rock":
            self.toggleAudio()
            self.last_gesture_time = current_time
            return "Audio toggled!"
            
        elif gesture == "fist":
            self.lockScreen()
            self.last_gesture_time = current_time
            return "Screen locked!"
            
        elif gesture == "open_palm" and hand_type == "left":
            self.toggleMouseControl()
            self.last_gesture_time = current_time
            return "Mouse control toggled!"
        
        return None

    def takeScreenshot(self):
        """Take a screenshot using pyautogui"""
        try:
            # Disable pyautogui failsafe temporarily
            pyautogui.FAILSAFE = False
            screenshot = pyautogui.screenshot()
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            screenshot.save(filename)
            print(f"Screenshot saved as {filename}")
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            # Try alternative method
            try:
                import mss
                with mss.mss() as sct:
                    screenshot = sct.grab(sct.monitors[1])  # Primary monitor
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"screenshot_{timestamp}.png"
                    mss.tools.to_png(screenshot.rgb, screenshot.size, filename)
                    print(f"Screenshot saved as {filename} (alternative method)")
            except ImportError:
                print("Install mss for better screenshot support: pip install mss")
            except Exception as e2:
                print(f"Alternative screenshot method also failed: {e2}")

    def toggleAudio(self):
        """Toggle system audio mute/unmute"""
        try:
            # Use pyautogui for audio control (simpler and more reliable)
            import pyautogui
            pyautogui.press('volumemute')
        except Exception as e:
            print(f"Error toggling audio: {e}")

    def lockScreen(self):
        """Lock the computer screen"""
        try:
            # Windows screen lock
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=False)
        except Exception as e:
            print(f"Error locking screen: {e}")

    def toggleMouseControl(self):
        """Toggle mouse control on/off"""
        self.mouse_enabled = not self.mouse_enabled
        print(f"Mouse control: {'ENABLED' if self.mouse_enabled else 'DISABLED'}")

    def detectPinchGesture(self, lmList, img, draw=True):
        """Detect pinch gesture between thumb and index finger"""
        if len(lmList) < 21:
            return False, img, None
            
        # Get thumb tip and index finger tip
        thumb_tip = lmList[4]
        index_tip = lmList[8]
        
        # Calculate distance
        distance = math.hypot(thumb_tip[1] - index_tip[1], thumb_tip[2] - index_tip[2])
        
        # Check if fingers are close enough for pinch
        is_pinching = distance < self.pinch_threshold
        
        if draw:
            if is_pinching:
                cv2.circle(img, (thumb_tip[1], thumb_tip[2]), 10, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (index_tip[1], index_tip[2]), 10, (0, 255, 0), cv2.FILLED)
                cv2.line(img, (thumb_tip[1], thumb_tip[2]), (index_tip[1], index_tip[2]), (0, 255, 0), 3)
            else:
                cv2.circle(img, (thumb_tip[1], thumb_tip[2]), 8, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (index_tip[1], index_tip[2]), 8, (255, 0, 0), cv2.FILLED)
        
        return is_pinching, img, distance

    def handleDragAndDrop(self, lmList, img, screen_width, screen_height, frameR, width, height):
        """Handle drag and drop functionality with pinch gesture"""
        is_pinching, img, distance = self.detectPinchGesture(lmList, img)
        
        if is_pinching and not self.is_pinching:
            # Start pinch
            self.is_pinching = True
            self.pinch_start_pos = (lmList[8][1], lmList[8][2])
            self.drag_mode = True
            print("Drag started")
            
        elif is_pinching and self.is_pinching:
            # Continue dragging
            if self.drag_mode:
                # Convert to screen coordinates
                x3 = np.interp(lmList[8][1], (frameR, width-frameR), (0, screen_width))
                y3 = np.interp(lmList[8][2], (frameR, height-frameR), (0, screen_height))
                
                # Move mouse while dragging
                import autopy
                autopy.mouse.move(screen_width - x3, y3)
                
                # Draw drag indicator
                cv2.circle(img, (lmList[8][1], lmList[8][2]), 15, (0, 255, 255), cv2.FILLED)
                cv2.putText(img, "DRAGGING", (lmList[8][1] - 50, lmList[8][2] - 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
        elif not is_pinching and self.is_pinching:
            # End pinch - perform drop
            self.is_pinching = False
            self.drag_mode = False
            print("Drop performed")
            
            # Perform click to complete drag and drop
            import autopy
            autopy.mouse.click()
        
        return img


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(1)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()