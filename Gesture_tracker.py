import cv2
import mediapipe as mp

def detect_gesture():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    gesture_detected = False

    print("[INFO] Starting webcam. Press 'q' to quit...")

    while True:
        success, img = cap.read()
        if not success:
            print("[ERROR] Could not read from webcam.")
            break

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gesture_detected = True

        cv2.imshow("Hand Gesture Detection", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return gesture_detected
