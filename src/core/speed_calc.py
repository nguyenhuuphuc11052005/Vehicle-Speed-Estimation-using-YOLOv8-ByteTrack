from collections import defaultdict, deque

import numpy as np

class SpeedEstimator:
    def __init__(self, homography_matrix, fps):
        self.matrix = homography_matrix
        self.fps = fps
        self.frame_window = 15
        self.pixel_to_meter_ratio = 0.0025
        self.speeds_history = {} # Lưu vận tốc để làm mượt
        self.history = defaultdict(lambda: deque(maxlen=30))
        
    def update_history(self, track_id, center_point):
        # Cập nhật tọa độ tâm mới vào vùng nhớ của ID tương ứng
        if track_id not in self.history:
            self.history[track_id] = deque(maxlen=30)
        self.history[track_id].append(center_point)
        
    def get_trajectory(self, track_id):
        return list(self.history[track_id])
    
    def transform_point(self, point):
        """Chuyển tọa độ pixel sang tọa độ Bird's Eye View"""
        p = np.array([point[0], point[1], 1.0]).reshape(3, 1)
        transformed_p = np.dot(self.matrix, p)
        transformed_p /= transformed_p[2] # Normalize
        return transformed_p[0][0], transformed_p[1][0]

    def estimate_speed(self, track_id, trajectory):
        if len(trajectory) < self.frame_window:
            return 0.0
        
        p1_pix = trajectory[-self.frame_window]
        p2_pix = trajectory[-1]
        
        p1_real = self.transform_point(p1_pix)
        p2_real = self.transform_point(p2_pix)
        
        d_pixels = np.sqrt((p2_real[0] - p1_real[0])**2 + (p2_real[1] - p1_real[1])**2)
        d_meters = d_pixels * self.pixel_to_meter_ratio
        
        # SỬA LỖI 3: Số bước di chuyển thực tế = frame_window - 1
        intervals = self.frame_window - 1
        time_elapsed = intervals / self.fps
        
        speed_mps = d_meters / time_elapsed
        speed_kmh = speed_mps * 3.6
        # if speed_kmh > 0:
        #     print(f"ID: {track_id} | Di chuyển pixel BEV: {d_pixels:.2f} px | Quãng đường: {d_meters:.2f} m | Vận tốc: {speed_kmh:.2f} km/h")
        return speed_kmh*100
    
    def smooth_speed(self, track_id, new_speed):
        # SỬA LỖI 2: Không lưu giá trị 0.0 vào bộ nhớ làm mượt
        if new_speed == 0.0:
            # Nếu xe chưa có vận tốc, trả về 0 để hiển thị tạm
            return 0.0
            
        if track_id not in self.speeds_history:
            self.speeds_history[track_id] = []
            
        self.speeds_history[track_id].append(new_speed)
        
        if len(self.speeds_history[track_id]) > 10:
            self.speeds_history[track_id].pop(0)
            
        return sum(self.speeds_history[track_id]) / len(self.speeds_history[track_id])