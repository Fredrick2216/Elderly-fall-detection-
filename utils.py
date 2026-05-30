import numpy as np

class AdaptiveLearner:
    def __init__(self):
        self.angle_history = []
        self.baseline_threshold = 45 
        self.is_ready = False

    def calibrate(self, current_angle):
        if len(self.angle_history) < 50:
            self.angle_history.append(current_angle)
            return False
        self.baseline_threshold = np.mean(self.angle_history) + 20
        self.is_ready = True
        return True

def get_midpoint(p1, p2):
    return [(p1.x + p2.x) / 2, (p1.y + p2.y) / 2]

def calculate_physics(prev_y, curr_y, prev_vel, dt):
    """
    Calculates movement velocity and Jerk (change in acceleration).
    Jerk is essential for detecting the 'thud' of a fall.
    """
    if prev_y is None or dt <= 0: 
        return 0.0, 0.0
    
    # Calculate Velocity: (Change in position / change in time)
    curr_vel = abs(curr_y - prev_y) / dt
    
    # Calculate Jerk: (Change in velocity / change in time)
    # Multiplied by 15.0 to ensure camera-detected impacts are significant
    jerk_raw = abs(curr_vel - prev_vel) / dt
    jerk_final = round(jerk_raw * 15.0, 2) 
    
    return round(curr_vel, 3), jerk_final

def calculate_gait_metrics(lm):
    """
    Analyzes horizontal sway. High sway indicates instability or tripping.
    """
    l_hip, r_hip = lm[23], lm[24]
    # Measure distance between hips relative to camera frame
    sway = abs(l_hip.x - r_hip.x)
    # Scale to a 0-100 range for better readability on graphs
    return round(sway * 150, 2)




