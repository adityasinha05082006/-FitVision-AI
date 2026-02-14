import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import time
import math
import requests
import os


# ---------------------------
# INITIALIZATION
# ---------------------------
# Download model if not present
model_path = 'pose_landmarker.task'
if not os.path.exists(model_path):
    import urllib.request
    print("Downloading pose landmark model...")
    url = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
    try:
        urllib.request.urlretrieve(url, model_path)
        print(f"Model downloaded to {model_path}")
    except Exception as e:
        print(f"Warning: Could not download model: {e}")

# Create detector
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    output_segmentation_masks=False)
detector = vision.PoseLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

# Video Recorder
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('poseplay_record.avi', fourcc, 20.0, (640, 480))

mode_list = ["Squat", "Pushup", "Bicep"]
mode_index = 0
mode = mode_list[mode_index]

counter = 0
stage = None
score = 0

pTime = 0

# ---------------------------
# ANGLE CALCULATION FUNCTION
# ---------------------------
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
              np.arctan2(a[1]-b[1], a[0]-b[0])

    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    return angle


# ---------------------------
# MAIN LOOP
# ---------------------------
cv2.namedWindow("PosePlay Pro", cv2.WINDOW_NORMAL)

while cap.isOpened():

    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]

    # Convert to MediaPipe format
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    
    # Detect pose
    detection_result = detector.detect(mp_image)
    image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    if detection_result.pose_landmarks and len(detection_result.pose_landmarks) > 0:
        landmarks = detection_result.pose_landmarks[0]

        # Landmark indices
        LEFT_HIP = 23
        LEFT_KNEE = 25
        LEFT_ANKLE = 27
        LEFT_SHOULDER = 11
        LEFT_ELBOW = 13
        LEFT_WRIST = 15

        # Get coordinates based on mode
        if mode == "Squat":
            hip = [landmarks[LEFT_HIP].x * w,
                   landmarks[LEFT_HIP].y * h]
            knee = [landmarks[LEFT_KNEE].x * w,
                    landmarks[LEFT_KNEE].y * h]
            ankle = [landmarks[LEFT_ANKLE].x * w,
                     landmarks[LEFT_ANKLE].y * h]

            angle = calculate_angle(hip, knee, ankle)

            if angle > 160:
                stage = "UP"
            if angle < 90 and stage == "UP":
                stage = "DOWN"
                counter += 1
                score += 10

        elif mode == "Pushup":
            shoulder = [landmarks[LEFT_SHOULDER].x * w,
                        landmarks[LEFT_SHOULDER].y * h]
            elbow = [landmarks[LEFT_ELBOW].x * w,
                     landmarks[LEFT_ELBOW].y * h]
            wrist = [landmarks[LEFT_WRIST].x * w,
                     landmarks[LEFT_WRIST].y * h]

            angle = calculate_angle(shoulder, elbow, wrist)

            if angle > 160:
                stage = "UP"
            if angle < 70 and stage == "UP":
                stage = "DOWN"
                counter += 1
                score += 10

        elif mode == "Bicep":
            shoulder = [landmarks[LEFT_SHOULDER].x * w,
                        landmarks[LEFT_SHOULDER].y * h]
            elbow = [landmarks[LEFT_ELBOW].x * w,
                     landmarks[LEFT_ELBOW].y * h]
            wrist = [landmarks[LEFT_WRIST].x * w,
                     landmarks[LEFT_WRIST].y * h]

            angle = calculate_angle(shoulder, elbow, wrist)

            if angle > 160:
                stage = "DOWN"
            if angle < 40 and stage == "DOWN":
                stage = "UP"
                counter += 1
                score += 10

        # Draw landmarks
        for landmark in landmarks:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

    # ---------------------------
    # FPS CALCULATION
    # ---------------------------
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # ---------------------------
    # UI PANEL (Transparent)
    # ---------------------------
    overlay = image.copy()
    cv2.rectangle(overlay, (0, 0), (350, 180), (0, 0, 0), -1)
    alpha = 0.6
    image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

    cv2.putText(image, "POSEPLAY PRO", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(image, f"Mode: {mode}", (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.putText(image, f"Reps: {counter}", (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.putText(image, f"Score: {score}", (20, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.putText(image, f"Stage: {stage}", (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.putText(image, f"FPS: {int(fps)}", (w - 150, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    # ---------------------------
    # SHOW + RECORD
    # ---------------------------
    out.write(image)
    cv2.imshow("PosePlay Pro", image)

    key = cv2.waitKey(1) & 0xFF

    # Switch Mode
    if key == ord('m'):
        mode_index = (mode_index + 1) % len(mode_list)
        mode = mode_list[mode_index]
        counter = 0
        score = 0

    # Quit
    if key == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
