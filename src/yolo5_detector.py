import torch
import numpy as np

class YoloV5Detector:
    def __init__(self, model_path):
        # Load YOLOv5 model from PyTorch Hub
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
    
    def detect(self, frame):
        # Perform inference on the frame
        results = self.model(frame)
        
        boxes = []
        for result in results.xyxy[0]:
            if result[4] > 0.5:  # confidence threshold
                x1, y1, x2, y2 = map(int, result[:4])
                boxes.append([x1, y1, x2 - x1, y2 - y1])
        
        return boxes