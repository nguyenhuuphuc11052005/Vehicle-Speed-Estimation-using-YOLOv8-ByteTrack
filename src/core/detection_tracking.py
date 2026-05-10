from ultralytics import YOLO

class VehicleTracker:
    def __init__(self, model_path="models/yolov8n.pt"):
        # Khởi tạo model YOLO
        self.model = YOLO(model_path)
        
    def track(self, frame):
        # Chạy tracking trực tiếp với ByteTrack được tích hợp sẵn trong Ultralytics
        # persist=True: Giữ ID của vật thể qua các khung hình
        # tracker="bytetrack.yaml": Chỉ định thuật toán tracking
        results = self.model.track(
            source=frame, 
            persist=True, 
            tracker="bytetrack.yaml", 
            classes=[2, 3, 5, 7], # car, motorcycle, bus, truck (COCO dataset)
            verbose=False
        )
        return results[0]