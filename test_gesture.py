from Gesture_tracker import detect_gesture

if detect_gesture():
    print("[INFO] Hand detected. Gesture triggered.")
else:
    print("[INFO] No gesture detected.")
