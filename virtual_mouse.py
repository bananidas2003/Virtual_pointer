import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)

screen_width, screen_height = pyautogui.size()
dragging = False

while cap.isOpened():
    success, img = cap.read()
    if not success:
        continue

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_tip = hand.landmark[mp_hands.HandLandmark.THUMB_TIP]

        # Corrected mouse mapping
        x = screen_width - int(index_tip.x * screen_width)
        y = int(index_tip.y * screen_height)

        pyautogui.moveTo(x, y, duration=0.05)

        dist = ((index_tip.x - thumb_tip.x)**2 + (index_tip.y - thumb_tip.y)**2)**0.5

        if dist < 0.1 and not dragging:
            pyautogui.click()
            dragging = True
        elif dist > 0.1:
            dragging = False

    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
