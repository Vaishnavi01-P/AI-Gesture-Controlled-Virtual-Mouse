import cv2
import numpy as np
import time
import math
import HandTracking as ht
import autopy
import pyautogui
import subprocess

### Variables Declaration
pTime = 0               # Used to calculate frame rate
width = 640             # Width of Camera
height = 480            # Height of Camera
frameR = 100            # Frame Rate
smoothening = 8         # Smoothening Factor
prev_x, prev_y = 0, 0   # Previous coordinates
curr_x, curr_y = 0, 0   # Current coordinates

# Enhanced features
gesture_feedback = ""   # Display gesture feedback
feedback_timer = 0      # Timer for feedback display

cap = cv2.VideoCapture(0)   # Getting video feed from the webcam
cap.set(3, width)           # Adjusting size
cap.set(4, height)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera. Trying alternative camera index...")
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: No camera found. Please check your camera connection.")
        exit()

detector = ht.handDetector(maxHands=2)                  # Detecting up to 2 hands
screen_width, screen_height = autopy.screen.size()      # Getting the screen size

print("=== VIRTUAL MOUSE - ALL FEATURES ===")
print("")
print("BASIC FEATURES:")
print("Fore finger (Index) -> Move cursor")
print("Fore + Middle finger together -> Click")
print("Bounding box around hand")
print("Distance detection for clicking")
print("")
print("ENHANCED GESTURES:")
print("Victory sign (Index + Middle) -> Screenshot")
print("Rock sign (Index + Pinky) -> Mute/Unmute Audio")
print("Fist (All down) -> Lock Screen")
print("Open Palm (Left hand) -> Enable/Pause Mouse")
print("Pinch (Thumb + Index) -> Drag & Drop")
print("")
print("DUAL-HAND MODE:")
print("Left hand open palm -> enables/pauses mouse")
print("Right hand index finger -> controls cursor & clicks")
print("")
print("================================")

while True:
    success, img = cap.read()
    
    # Check if frame was read successfully
    if not success or img is None:
        print("Error: Could not read frame from camera")
        break
        
    img = cv2.flip(img, 1)  # Flip image horizontally for mirror effect
    
    # Use enhanced multi-hand detection
    img, hands_data = detector.findMultiHands(img)
    
    # Process each detected hand
    left_hand = None
    right_hand = None
    
    for hand in hands_data:
        if hand['hand_type'] == 'left':
            left_hand = hand
        elif hand['hand_type'] == 'right':
            right_hand = hand
    
    # Handle left hand gestures (control mouse enable/disable)
    if left_hand:
        fingers = left_hand['fingers']
        gesture = detector.recognizeGesture(fingers)
        
        if gesture:
            action_result = detector.executeGestureAction(gesture, "left")
            if action_result:
                gesture_feedback = action_result
                feedback_timer = time.time()
                print(action_result)
    
    # Handle right hand mouse control
    if right_hand and detector.mouse_enabled:
        lmList = right_hand['lmList']
        fingers = right_hand['fingers']
        
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]   # Fore finger (Index) tip coordinates
            x2, y2 = lmList[12][1:]  # Middle finger tip coordinates
            
            # Create boundary box around the hand
            cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255), 2)
            
            # Check for enhanced gesture recognition first
            gesture = detector.recognizeGesture(fingers)
            if gesture:
                action_result = detector.executeGestureAction(gesture, "right")
                if action_result:
                    gesture_feedback = action_result
                    feedback_timer = time.time()
                    print(action_result)
            
            # BASIC FEATURE: Mouse movement (fore finger only)
            elif fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                # Convert coordinates to screen coordinates
                x3 = np.interp(x1, (frameR, width-frameR), (0, screen_width))
                y3 = np.interp(y1, (frameR, height-frameR), (0, screen_height))

                # Smooth the movement
                curr_x = prev_x + (x3 - prev_x) / smoothening
                curr_y = prev_y + (y3 - prev_y) / smoothening

                # Move the cursor
                autopy.mouse.move(screen_width - curr_x, curr_y)
                
                # Draw circle on fore finger tip
                cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
                
                # Show "MOVING" text
                cv2.putText(img, "MOVING CURSOR", (x1 - 60, y1 - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
                
                prev_x, prev_y = curr_x, curr_y

            # BASIC FEATURE: Click gesture (fore finger + middle finger together)
            elif fingers[1] == 1 and fingers[2] == 1:
                # Calculate distance between fore finger and middle finger
                length = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                
                # Draw line between fingers
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                
                # Show distance on screen
                cv2.putText(img, f"Distance: {int(length)}", (10, 150), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                
                # If fingers are close enough together - PERFORM CLICK
                if length < 40:
                    # Show "CLICKING" text
                    cv2.putText(img, "CLICKING!", (cx - 40, cy - 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    # Perform the click
                    autopy.mouse.click()
                else:
                    # Show "Too far" when fingers are not close enough
                    cv2.putText(img, "Too far - bring fingers closer", (cx - 80, cy - 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            # ENHANCED FEATURE: Pinch gesture for drag and drop
            elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                # Calculate distance between thumb and index finger
                thumb_tip = lmList[4]
                index_tip = lmList[8]
                pinch_distance = math.sqrt((thumb_tip[1] - index_tip[1])**2 + (thumb_tip[2] - index_tip[2])**2)
                
                # Check if fingers are close enough for pinch
                if pinch_distance < 50:
                    # Convert to screen coordinates
                    x3 = np.interp(index_tip[1], (frameR, width-frameR), (0, screen_width))
                    y3 = np.interp(index_tip[2], (frameR, height-frameR), (0, screen_height))
                    
                    # Move mouse while pinching
                    autopy.mouse.move(screen_width - x3, y3)
                    
                    # Visual feedback for pinch
                    cv2.circle(img, (thumb_tip[1], thumb_tip[2]), 10, (0, 255, 255), cv2.FILLED)
                    cv2.circle(img, (index_tip[1], index_tip[2]), 10, (0, 255, 255), cv2.FILLED)
                    cv2.line(img, (thumb_tip[1], thumb_tip[2]), (index_tip[1], index_tip[2]), (0, 255, 255), 3)
                    cv2.putText(img, "PINCHING - DRAG & DROP", (index_tip[1] - 80, index_tip[2] - 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                    
                    # Perform click when pinch is detected
                    autopy.mouse.click()
                else:
                    # Show pinch gesture is being attempted but not close enough
                    cv2.circle(img, (thumb_tip[1], thumb_tip[2]), 8, (255, 255, 0), cv2.FILLED)
                    cv2.circle(img, (index_tip[1], index_tip[2]), 8, (255, 255, 0), cv2.FILLED)
                    cv2.putText(img, f"Pinch Distance: {int(pinch_distance)}", (index_tip[1] - 80, index_tip[2] - 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
    
    # Display status information
    status_y = 30
    cv2.putText(img, f"Mouse: {'ENABLED' if detector.mouse_enabled else 'DISABLED'}", 
                (10, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                (0, 255, 0) if detector.mouse_enabled else (0, 0, 255), 2)
    
    # Display gesture feedback
    if gesture_feedback and time.time() - feedback_timer < 2.0:
        cv2.putText(img, gesture_feedback, (10, status_y + 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    
    # Display hand count
    hand_count = len(hands_data)
    cv2.putText(img, f"Hands: {hand_count}", (10, status_y + 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Display comprehensive instructions
    instructions = [
        "BASIC: Index=Move, Index+Middle=Click",
        "GESTURES: Victory=Screenshot, Rock=Mute, Fist=Lock",
        "DUAL-HAND: Left=Toggle, Right=Control",
        "PINCH: Thumb+Index=Drag&Drop"
    ]
    
    for i, instruction in enumerate(instructions):
        cv2.putText(img, instruction, (10, height - 100 + i * 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    # Calculate and display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (width - 120, 30), 
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    
    cv2.imshow("Virtual Mouse - ALL FEATURES", img)
    
    # Exit on 'q' key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


