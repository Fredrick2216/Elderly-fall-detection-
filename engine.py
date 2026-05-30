class FallEngine:
    def __init__(self):
        self.floor_start = None
        self.unseen_start = None

    def is_in_fall_zone(self, y_coord, angle):
        """
        If the Y coordinate is high (bottom of screen) and angle is high, 
        it's a high-probability fall.
        """
        # Landmarks > 0.7 are in the bottom 30% of the frame
        return y_coord > 0.70 or angle > 75

    def check_immobility(self, is_on_floor, current_time):
        if is_on_floor:
            if self.floor_start is None: self.floor_start = current_time
            return current_time - self.floor_start
        self.floor_start = None
        return 0

    def check_unseen(self, current_time):
        if self.unseen_start is None: self.unseen_start = current_time
        return current_time - self.unseen_start

    def reset_unseen(self):
        self.unseen_start = None
