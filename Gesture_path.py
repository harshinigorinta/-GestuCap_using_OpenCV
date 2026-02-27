import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from PIL import ImageGrab
import time

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

# Tkinter overlay
root = tk.Tk()
root.attributes('-fullscreen', True)
root.attributes('-alpha', 0.3)
root.attributes('-topmost', True)
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack()

# Initialize variables
start_point = None
end_point = None
drawing = False
rect_id = None
last_seen_time = time.time()
capture_delay = 1.5  # seconds after hand disappears

def draw_rectangle(x1, y1, x2, y2):
    global rect_id
    canvas.delete("all")
    rect_id = canvas.create_rectangle(x1, y1, x2, y2, outline='lime green', width=4)

# Open webcam
cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    print("[INFO] Show index finger and move to draw rectangle...")
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            last_seen_time = time.time()
            hand_landmarks = results.multi_hand_landmarks[0]

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            x = hand_landmarks.landmark[8].x
            y = hand_landmarks.landmark[8].y
            abs_x, abs_y = int(x * screen_width), int(y * screen_height)

            if not drawing:
                start_point = (abs_x, abs_y)
                drawing = True
            else:
                end_point = (abs_x, abs_y)
                draw_rectangle(start_point[0], start_point[1], end_point[0], end_point[1])
        else:
            # No hand detected
            if drawing and (time.time() - last_seen_time) > capture_delay:
                if start_point and end_point:
                    x1 = min(start_point[0], end_point[0])
                    y1 = min(start_point[1], end_point[1])
                    x2 = max(start_point[0], end_point[0])
                    y2 = max(start_point[1], end_point[1])
                    bbox = (x1, y1, x2, y2)
                    img = ImageGrab.grab(bbox)
                    img.save("gesture_capture.png")
                    print("[✔] Screenshot saved as gesture_capture.png")
                break

        cv2.imshow("Webcam (show your finger)", frame)
        root.update()
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
canvas.delete("all")
root.destroy()
