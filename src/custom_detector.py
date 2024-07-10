import cv2
import torch

class CustomDetector:
    def __init__(self, model):
        self.model = model
    
    def detect(self, frame):
        frame_resized = cv2.resize(frame, (32, 32))
        frame_tensor = torch.from_numpy(frame_resized).permute(2, 0, 1).float().unsqueeze(0)
        
        with torch.no_grad():
            outputs = self.model(frame_tensor)
        
        boxes = []
        for output in outputs:
            x, y, w, h = map(int, output)
            boxes.append([x, y, w, h])
        
        return boxes