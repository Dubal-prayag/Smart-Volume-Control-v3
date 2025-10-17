import cv2
import mediapipe as mp
import numpy as np
import math
import collections
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time

# -------------------- CONFIG --------------------
MIN_HAND_DISTANCE = 25
MAX_HAND_DISTANCE = 200
SMOOTHING_WINDOW = 5
SHOW_FPS = True
MIN_AUDIBLE_PERCENT = 10  # Never below 10% audible volume
# ------------------------------------------------

# MediaPipe setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Access system volume controls
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
min_vol, max_vol, _ = volume.GetVolumeRange()  # Typically (-65, 0)

# Webcam setup
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("❌ Cannot open webcam. Try changing camera index.")

# Initialize variables
last_vol = volume.GetMasterVolumeLevel()
vol_history = collections.deque(maxlen=SMOOTHING_WINDOW)
prev_time = 0

print("✅ Smart Volume Control v3.0 Started — Move thumb & index to adjust volume. Press ESC to exit.")

with mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
) as hands:
    while True:
        success, image = cap.read()
        if not success:
            break

        image = cv2.flip(image, 1)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        h, w, _ = image.shape

        # FPS display
        if SHOW_FPS:
            cur_time = time.time()
            fps = 1 / (cur_time - prev_time + 1e-6)
            prev_time = cur_time
            cv2.putText(image, f"FPS: {fps:.1f}", (10, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            # Get thumb tip (4) and index tip (8)
            x1, y1 = int(hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h)
            x2, y2 = int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h)

            # Draw points and line
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.circle(image, (x1, y1), 10, (255, 0, 255), -1)
            cv2.circle(image, (x2, y2), 10, (255, 0, 255), -1)
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # Distance between thumb and index
            length = math.hypot(x2 - x1, y2 - y1)
            length = np.clip(length, MIN_HAND_DISTANCE, MAX_HAND_DISTANCE)

            # --- Nonlinear mapping with perceptual correction ---
            norm = (length - MIN_HAND_DISTANCE) / (MAX_HAND_DISTANCE - MIN_HAND_DISTANCE)
            vol_percent = (norm ** 0.8) * 100  # Adjust power for sensitivity
            vol_percent = np.clip(vol_percent, MIN_AUDIBLE_PERCENT, 100)

            # Map perceptual % to dB (log curve)
            vol_db = np.interp(np.log10(vol_percent / 100 * 9 + 1), [0, 1], [min_vol, max_vol])

            # Smooth changes
            vol_history.append(vol_db)
            smooth_vol = np.mean(vol_history)

            # Apply volume
            if abs(smooth_vol - last_vol) > 0.8:
                volume.SetMasterVolumeLevel(float(smooth_vol), None)
                last_vol = smooth_vol

            # Draw volume bar and % text
            bar_y = np.interp(vol_percent, [0, 100], [400, 150])
            cv2.rectangle(image, (50, 150), (85, 400), (0, 255, 0), 2)
            cv2.rectangle(image, (50, int(bar_y)), (85, 400), (0, 255, 0), -1)
            cv2.putText(image, f'Vol: {int(vol_percent)}%', (40, 430),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            # Debug distance
            cv2.putText(image, f'Dist: {int(length)}', (40, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        else:
            cv2.putText(image, "No Hand Detected", (40, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        cv2.imshow("🖐️ Smart Volume Control v3.0", image)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
print("👋 Exited Smart Volume Control v3.0.")
