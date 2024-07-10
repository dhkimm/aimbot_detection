import cv2
import torch
import os
import time

from face_detector import FaceDetector
from aim_tracker import AimTracker
from simple_cnn import SimpleCNN
from custom_detector import CustomDetector


model = SimpleCNN()

model.eval()

custom_detector = CustomDetector(model)
face_detector = FaceDetector()

video_path = 'D:/works/code/Aimbot_detection/video/clip.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Error: Could not open video file {video_path}")
    exit()

aim_tracker = AimTracker()
enemy_detected_time = None

output_dir = 'output_frames'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

frame_count = 0
resize_width = 640
resize_height = 360

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break
    
    frame = cv2.resize(frame, (resize_width, resize_height))
    height, width, _ = frame.shape
    
    boxes = custom_detector.detect(frame)
    
    for box in boxes:
        x, y, w, h = box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Ensure the region of interest is valid
        if x < 0 or y < 0 or x + w > width or y + h > height:
            continue

        roi = frame[y:y+h, x:x+w]
        if roi.size == 0:
            continue

        face_boxes = face_detector.detect(roi)
        for (fx, fy, fw, fh) in face_boxes:
            cv2.rectangle(frame, (x + fx, y + fy), (x + fx + fw, y + fy + fh), (255, 0, 0), 2)
    
    aim_x, aim_y = width // 2, height // 2
    
    aim_tracker.update(aim_x, aim_y, boxes)
    
    for box in boxes:
        x, y, w, h = box
        if x < aim_x < x + w and y < aim_y < y + h:
            if enemy_detected_time is None:
                enemy_detected_time = time.time()
            reaction_time = time.time() - enemy_detected_time
            cv2.putText(frame, f"Reaction Time: {reaction_time:.2f} s", (width - 250, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            aim_tracker.increment_hits()

            for (fx, fy, fw, fh) in face_boxes:
                if x + fx < aim_x < x + fx + fw and y + fy < aim_y < y + fy + fh:
                    aim_tracker.increment_face_hits()
        else:
            enemy_detected_time = None
    
    left_to_right_ratio, right_to_left_ratio = aim_tracker.get_ratios()
    
    cv2.putText(frame, f"L->R Ratio: {left_to_right_ratio:.2f}", (width - 250, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(frame, f"R->L Ratio: {right_to_left_ratio:.2f}", (width - 250, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    face_hit_ratio = aim_tracker.get_face_hit_ratio()
    cv2.putText(frame, f"Face Hit Ratio: {face_hit_ratio:.2f}", (width - 250, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    
    aim_bot_suspicion = aim_tracker.get_aim_bot_suspicion()
    cv2.putText(frame, f"Aim Bot Suspicion: {aim_bot_suspicion:.2f}", (width - 250, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
  
    cv2.imshow('Frame', frame)
    
    frame_filename = os.path.join(output_dir, f"frame_{frame_count:04d}.png")
    cv2.imwrite(frame_filename, frame)
    frame_count += 1
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()