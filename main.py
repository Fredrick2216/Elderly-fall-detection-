import cv2
import mediapipe as mp
import time
import numpy as np
import face_recognition
import os
import threading
from datetime import datetime
from alerts import DynamicNotifier
from utils import get_midpoint, calculate_physics, calculate_gait_metrics
from database import DataArchiver
from engine import FallEngine # Ensure this is imported

# --- 1. INITIALIZATION ---
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7, model_complexity=1)

notifier = DynamicNotifier()
archiver = DataArchiver()
engine = FallEngine()

def draw_hud(frame, status, patient_id, timer_val, angle, vel, jerk, gait):
    overlay = frame.copy()
    h, w, _ = frame.shape
    curr_time = time.time()
    
    scan_y = int((curr_time * 200) % h)
    cv2.line(overlay, (0, scan_y), (w, scan_y), (255, 255, 0), 1)
    
    color_cyan = (255, 255, 0) 
    color_alert = (0, 0, 255) 
    current_color = color_alert if "CRITICAL" in status or "FALL" in status else color_cyan
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.rectangle(overlay, (30, 30), (450, 150), (20, 20, 20), -1)
    cv2.rectangle(overlay, (30, 30), (450, 150), current_color, 1)
    cv2.putText(overlay, "AEGIS PRO - BIO MONITOR", (45, 60), font, 0.7, current_color, 2)
    cv2.line(overlay, (45, 75), (435, 75), (100, 100, 100), 1)
    cv2.putText(overlay, f"ID: {patient_id}", (45, 105), font, 0.6, (255, 255, 255), 1)
    cv2.putText(overlay, f"STATE: {status}", (45, 135), font, 0.6, (255, 255, 255), 1)

    cv2.rectangle(overlay, (w-250, 30), (w-30, 250), (20, 20, 20), -1)
    cv2.rectangle(overlay, (w-250, 30), (w-30, 250), current_color, 1)
    cv2.putText(overlay, "TELEMETRY", (w-235, 60), font, 0.6, current_color, 2)
    
    metrics = [(f"TILT: {angle} DEG", angle > 45), (f"VEL: {vel:.2f} m/s", vel > 0.5),
               (f"JERK: {jerk:.2f}", jerk > 1.0), (f"GAIT: {gait:.2f}", gait < 0.3 and gait > 0)]
    
    for i, (text, warning) in enumerate(metrics):
        y_pos = 100 + (i * 35)
        text_color = (0, 165, 255) if warning else (255, 255, 255) 
        cv2.putText(overlay, text, (w-235, y_pos), font, 0.5, text_color, 1)

    if timer_val > 0:
        cv2.rectangle(overlay, (w//2-120, h-100), (w//2+120, h-40), (0, 0, 150), -1)
        # Reduced to 10s for faster demo response
        cv2.putText(overlay, f"ALERT IN: {max(0, 10-timer_val)}s", (w//2-100, h-60), font, 0.7, (255, 255, 255), 2)

    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

# --- FACE LOADING ---
known_face_encodings, known_face_names = [], []
encoding_path = "encodings"
if os.path.exists(encoding_path):
    for file in os.listdir(encoding_path):
        img = face_recognition.load_image_file(f"{encoding_path}/{file}")
        enc = face_recognition.face_encodings(img)
        if enc:
            known_face_encodings.append(enc[0])
            known_face_names.append(os.path.splitext(file)[0])

# --- STATE ---
active_id = "UNKNOWN"
fall_timer_start = None      
missing_timer_start = None   
bending_sent = False
fall_sent = False
missing_sent = False
prev_y, prev_vel = None, 0

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        curr_time = time.time()
        
        if active_id == "UNKNOWN" or int(curr_time) % 5 == 0:
            small_rgb = cv2.cvtColor(cv2.resize(frame, (0,0), fx=0.25, fy=0.25), cv2.COLOR_BGR2RGB)
            face_encs = face_recognition.face_encodings(small_rgb)
            for enc in face_encs:
                if known_face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, enc)
                    if True in matches: active_id = known_face_names[matches.index(True)]

        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        status = "SCANNING..."
        gait, jerk, vel, angle = 0, 0, 0, 0

        if results.pose_landmarks:
            missing_timer_start = None 
            missing_sent = False
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            lm = results.pose_landmarks.landmark
            sh_mid = get_midpoint(lm[11], lm[12])
            angle = int(np.degrees(np.arctan2(abs(lm[11].x-lm[23].x), abs(lm[11].y-lm[23].y))))
            vel, jerk = calculate_physics(prev_y, sh_mid[1], prev_vel, 0.03)
            gait = calculate_gait_metrics(lm)
            prev_y, prev_vel = sh_mid[1], vel

            # --- DETECTION LOGIC ---
            if engine.is_in_fall_zone(sh_mid[1], angle):
                status = "CRITICAL: FALL DETECTED"
                if fall_timer_start is None: fall_timer_start = curr_time
                # Trigger after 10 seconds for more efficient demo
                if (curr_time - fall_timer_start > 10) and not fall_sent:
                    notifier.trigger_emergency_all(active_id, "CRITICAL FALL")
                    fall_sent = True
            
            elif 40 < angle < 75:
                status = "WARNING: BENDING"
                fall_timer_start = None
                if not bending_sent:
                    notifier.trigger_staff_only(active_id, "BENDING")
                    bending_sent = True
            
            else:
                fall_timer_start, bending_sent, fall_sent = None, False, False
                status = "STABLE" if abs(lm[0].y - lm[28].y) > 0.6 else "SITTING"

        else:
            # --- PERSISTENCE LOGIC (THE FIX) ---
            # If tracking is lost, but the person was low on the screen:
            if prev_y is not None and prev_y > 0.65:
                status = "CRITICAL: FALL (SIGNAL LOST)"
                if fall_timer_start is None: fall_timer_start = curr_time
                if (curr_time - fall_timer_start > 10) and not fall_sent:
                    notifier.trigger_emergency_all(active_id, "FALL AFTER SIGNAL LOSS")
                    fall_sent = True
            else:
                # Normal Missing Logic (Person walked away)
                fall_timer_start, fall_sent = None, False
                if missing_timer_start is None: missing_timer_start = curr_time
                status = "CRITICAL: PATIENT MISSING"
                if (curr_time - missing_timer_start > 10) and not missing_sent:
                    notifier.trigger_emergency_all(active_id, "MISSING ALERT")
                    missing_sent = True

        archiver.save_record({"Timestamp": datetime.now().strftime("%H:%M:%S"), "Patient": active_id, 
                              "Status": status, "Angle": angle, "Velocity": vel, "Jerk": jerk, "Gait": gait})

        timer_val = int(curr_time - fall_timer_start) if fall_timer_start else (int(curr_time - missing_timer_start) if missing_timer_start else 0)
        draw_hud(frame, status, active_id, timer_val, angle, vel, jerk, gait)
        cv2.imshow("AEGIS PRO NEXT-GEN HUD", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

finally:
    if len(archiver.data_list) > 0: archiver.generate_comprehensive_report()
    cap.release()
    cv2.destroyAllWindows()
