from ultralytics import YOLO

# Load mô hình PyTorch
model = YOLO("models/yolov8n.pt")

# Export sang định dạng ONNX
path = model.export(format="onnx", opset=12, simplify=True)
print(f"Mô hình đã được export thành công tại: {path}")