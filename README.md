```markdown
# 🚗 Vehicle Speed Estimation using Computer Vision

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg?style=for-the-badge&logo=opencv)
![YOLOv8](https://img.shields.io/badge/YOLO-v8-yellow.svg?style=for-the-badge&logo=yolo)
![ONNX](https://img.shields.io/badge/ONNX-Optimized-red.svg?style=for-the-badge&logo=onnx)

> An end-to-end Machine Learning pipeline to estimate real-time vehicle speed using a single fixed-perspective traffic camera.

---

## 📌 The Problem & Objective
In modern Smart City infrastructure, monitoring traffic speed traditionally requires expensive hardware like RADAR or LiDAR sensors. 

**The Objective:** This project provides a cost-effective, software-based alternative. By leveraging deep learning and projective geometry, we can transform standard 2D CCTV footage into an accurate speed-estimation system without the need for complex physical sensors.

---

## 🚀 Demo
*(💡 **Lưu ý cho bạn:** Nếu bạn dùng **Cách 1** (kéo thả file MP4 dưới 10MB vào GitHub), hãy xóa đoạn code dưới đây và dán link GitHub tự tạo vào. Nếu bạn dùng **Cách 2** (YouTube), hãy thay `YOUR_YOUTUBE_VIDEO_ID` bằng ID video của bạn).*

https://drive.google.com/file/d/14lWDklmzpPBrHTm5xwjaN__HAfD34UPx/view?usp=drive_link
*Click the image above to watch the full HD demonstration.*

---

## ⚙️ Key Technologies & Skills Demonstrated

* **Detection & Tracking:** Ultralytics YOLOv8 combined with ByteTrack for robust Multi-Object Tracking (MOT), highly effective against occlusion.
* **Computer Vision Geometry:** Implementation of Perspective Transformation (Homography Matrix) to map 2D pixel coordinates to 3D real-world metrics (Bird's Eye View).
* **Signal Processing:** Applied a Simple Moving Average (SMA) filter to mitigate bounding box jitter and stabilize velocity calculations.
* **MLOps & Optimization:** Exported the base PyTorch model to **ONNX** format, significantly reducing inference latency for real-time processing.
* **Software Architecture:** Clean, modular, Object-Oriented Programming (OOP) design.

---

## 🧠 Methodology: How it works

1.  **Detection:** YOLOv8 identifies vehicles (cars, trucks, buses) in the current frame.
2.  **Tracking:** ByteTrack assigns a unique, persistent ID to each detected vehicle and records its trajectory history.
3.  **Transformation:** Using a calibrated Homography Matrix, the bottom-center coordinates of the vehicle's bounding box are transformed from the camera's perspective into a flattened "Bird's Eye View" (Real-world meters).
4.  **Speed Calculation:** Velocity is calculated using the physical distance traveled over a designated frame window ($v = d / \Delta t$). The raw speed is then passed through a smoothing filter to output a stable km/h reading.

---

## 🛠️ Project Structure

```text
Vehicle-Speed-Estimation/
├── data/
│   ├── raw/               # Input traffic videos (.mp4)
│   └── processed/         # Output demo videos
├── models/                # YOLOv8 weights (.pt & .onnx) & calibration_matrix.npy
├── src/
│   ├── core/              # Core ML algorithms
│   │   ├── detection_tracking.py
│   │   └── speed_calc.py
│   └── utils/             # Helper scripts
│       ├── calibration.py # GUI tool to pick 4 perspective points
│       └── export_model.py# Convert .pt to .onnx
├── main.py                # Main pipeline execution
└── requirements.txt       
```

---

## 🚀 Installation & Usage

### 1. Setup Environment
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/nguyenhuuphuc11052005/Vehicle-Speed-Estimation-using-YOLOv8-ByteTrack.git
cd Vehicle-Speed-Estimation
pip install -r requirements.txt
```

### 2. Calibrate the Camera
Before running the tracker, you need to define the measurement area on the road. Run the calibration script and click 4 points forming a rectangle on the road surface (Top-Left, Top-Right, Bottom-Right, Bottom-Left).
```bash
python src/utils/calibration.py
```
*This will generate a `calibration_matrix.npy` file in the models directory.*

### 3. Run Inference
Execute the main pipeline to process the video and display the real-time speed.
```bash
python main.py
```

---
