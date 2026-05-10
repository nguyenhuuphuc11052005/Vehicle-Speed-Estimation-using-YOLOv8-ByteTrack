

import cv2
import numpy as np
import os
from src.core.detection_tracking import VehicleTracker
from src.core.speed_calc import SpeedEstimator

class SpeedEstimationApp:
    def __init__(self, video_path, calibration_matrix_path, output_path="output_demo.mp4"):
        self.video_path = video_path
        self.output_path = output_path
        
        # 1. Khởi tạo Camera
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Không thể mở video tại: {video_path}")
            
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # 2. Setup Video Writer (Để xuất video demo)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Codec chuẩn cho MP4
        self.writer = cv2.VideoWriter(self.output_path, fourcc, self.fps, (self.width, self.height))
        
        # 3. Khởi tạo Modules
        # Chú ý: Hãy dùng file .onnx đã export để chứng minh khả năng tối ưu
        self.tracker = VehicleTracker(model_path="models/yolov8n.onnx") 
        homography_matrix = np.load(calibration_matrix_path)
        self.speed_estimator = SpeedEstimator(homography_matrix, self.fps)
        
    def process_frame(self, frame):
        # Tracking
        result = self.tracker.track(frame)
        
        if result.boxes.id is not None:
            boxes = result.boxes.xyxy.cpu().numpy()
            ids = result.boxes.id.int().cpu().numpy()
            
            for box, track_id in zip(boxes, ids):
                x1, y1, x2, y2 = box
                center_x = (x1 + x2) / 2
                center_y = y2  
                
                # Cập nhật và Tính toán
                self.speed_estimator.update_history(track_id, (center_x, center_y))
                trajectory = self.speed_estimator.get_trajectory(track_id)
                raw_speed = self.speed_estimator.estimate_speed(track_id, trajectory)
                smooth_speed = self.speed_estimator.smooth_speed(track_id, raw_speed)
                
                # Vẽ lên frame
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                
                # Nền đen cho Text dễ đọc (UI/UX)
                text = f"ID: {track_id} | {int(smooth_speed)} km/h"
                cv2.rectangle(frame, (int(x1), int(y1) - 25), (int(x1) + 200, int(y1)), (0, 0, 0), -1)
                cv2.putText(frame, text, (int(x1) + 5, int(y1) - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        return frame

    def run(self):
        print("Đang xử lý video... Hãy kiên nhẫn đợi.")
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success: 
                break
                
            processed_frame = self.process_frame(frame)
            
            # Lưu vào file video output
            self.writer.write(processed_frame)
            
            # (Tùy chọn) Vẫn hiển thị lên màn hình để quan sát
            cv2.imshow("Processing...", cv2.resize(processed_frame, (1080, 720)))
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break
                
        self.cap.release()
        self.writer.release()
        cv2.destroyAllWindows()
        print(f"Hoàn thành! Video demo đã được lưu tại: {self.output_path}")

# --- Điểm chạy chương trình ---
if __name__ == "__main__":
    VIDEO_SRC = "data/raw/traffic_video.mp4"
    CALIB_MAT = "models/calibration_matrix.npy"
    OUTPUT_VIDEO = "data/processed/demo_result.mp4"
    
    app = SpeedEstimationApp(VIDEO_SRC, CALIB_MAT, OUTPUT_VIDEO)
    app.run()