import math

class AimTracker:
    def __init__(self):
        self.previous_aim_x = None
        self.previous_aim_y = None
        self.left_to_right_count = 0
        self.right_to_left_count = 0
        self.hit_count = 0
        self.face_hit_count = 0
        self.reaction_times = []
        self.aim_speeds = []
        self.hit_accuracy = []

    def update(self, aim_x, aim_y, boxes):
        if self.previous_aim_x is not None and self.previous_aim_y is not None:
            distance = math.sqrt((aim_x - self.previous_aim_x) ** 2 + (aim_y - self.previous_aim_y) ** 2)
            self.aim_speeds.append(distance)
        
        self.previous_aim_x = aim_x
        self.previous_aim_y = aim_y

        if boxes:
            target_box = boxes[0]
            if target_box[0] < aim_x < target_box[0] + target_box[2] and target_box[1] < aim_y < target_box[1] + target_box[3]:
                self.hit_accuracy.append(1)
            else:
                self.hit_accuracy.append(0)
        else:
            self.hit_accuracy.append(0)
    
    def increment_hits(self):
        self.hit_count += 1
    
    def increment_face_hits(self):
        self.face_hit_count += 1
    
    def get_ratios(self):
        total_moves = self.left_to_right_count + self.right_to_left_count
        if total_moves > 0:
            left_to_right_ratio = self.left_to_right_count / total_moves
            right_to_left_ratio = self.right_to_left_count / total_moves
        else:
            left_to_right_ratio = 0
            right_to_left_ratio = 0
        
        return left_to_right_ratio, right_to_left_ratio
    
    def get_face_hit_ratio(self):
        if self.hit_count > 0:
            return self.face_hit_count / self.hit_count
        return 0

    def get_aim_bot_suspicion(self):
        if self.aim_speeds:
            average_speed = sum(self.aim_speeds) / len(self.aim_speeds)
        else:
            average_speed = 0
        
        if self.hit_accuracy:
            accuracy = sum(self.hit_accuracy) / len(self.hit_accuracy)
        else:
            accuracy = 0
        
        suspicion_score = (average_speed * 0.5) + (accuracy * 0.5)
        return suspicion_score