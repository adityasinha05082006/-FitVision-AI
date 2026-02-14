import cv2
import mediapipe as mp
import numpy as np
import time
import requests

# ---------------------------
# INITIALIZATION
# ---------------------------
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

pose = mp_pose.Pose(min_detection_confidence=0.7,
                    min_tracking_confidence=0.7)

# Recording control
recording = False
out = None

mode_list = ["Squat", "Pushup", "Bicep"]
mode_index = 0
mode = mode_list[mode_index]

counter = 0
stage = None
score = 0

pTime = 0

# ---------------------------
# ANGLE FUNCTION
# ---------------------------
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
              np.arctan2(a[1]-b[1], a[0]-b[0])

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

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

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        if mode == "Squat":
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * w,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * h]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * w,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * h]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * w,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * h]

            angle = calculate_angle(hip, knee, ankle)

            if angle > 160:
                stage = "UP"
            if angle < 90 and stage == "UP":
                stage = "DOWN"
                counter += 1
                score += 10

        elif mode == "Pushup":
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * w,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * h]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * w,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * h]

            angle = calculate_angle(shoulder, elbow, wrist)

            if angle > 160:
                stage = "UP"
            if angle < 70 and stage == "UP":
                stage = "DOWN"
                counter += 1
                score += 10

        elif mode == "Bicep":
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * w,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * h]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * w,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * h]

            angle = calculate_angle(shoulder, elbow, wrist)

            if angle > 160:
                stage = "DOWN"
            if angle < 40 and stage == "DOWN":
                stage = "UP"
                counter += 1
                score += 10

        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # ---------------------------
    # FPS
    # ---------------------------
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # ---------------------------
    # UI PANEL
    # ---------------------------
    overlay = image.copy()
    cv2.rectangle(overlay, (0, 0), (350, 200), (0, 0, 0), -1)
    alpha = 0.6
    image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

    cv2.putText(image, "POSEPLAY PRO", (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.putText(image, f"Mode: {mode}", (20, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.putText(image, f"Reps: {counter}", (20, 95),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.putText(image, f"Score: {score}", (20, 125),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.putText(image, f"Stage: {stage}", (20, 155),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.putText(image, f"FPS: {int(fps)}", (w - 150, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    # Recording status
    rec_text = "REC: ON" if recording else "REC: OFF"
    rec_color = (0, 0, 255) if recording else (200, 200, 200)
    cv2.putText(image, rec_text, (w - 150, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, rec_color, 2)

    # ---------------------------
    # RECORD VIDEO
    # ---------------------------
    if recording and out is not None:
        out.write(image)

    cv2.imshow("PosePlay Pro", image)

    key = cv2.waitKey(1) & 0xFF

    # Toggle Recording
    if key == ord('r'):
        recording = not recording

        if recording:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(
                f'poseplay_{int(time.time())}.avi',
                fourcc,
                20.0,
                (w, h)
            )
            print("Recording Started")
        else:
            if out is not None:
                out.release()
                out = None
            print("Recording Stopped")

    # Switch Mode
    if key == ord('m'):
        mode_index = (mode_index + 1) % len(mode_list)
        mode = mode_list[mode_index]
        counter = 0
        score = 0

    # Quit
    if key == ord('q'):
        break

# Cleanup
if out is not None:
    out.release()

cap.release()
cv2.destroyAllWindows()
