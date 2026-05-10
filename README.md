

```markdown
# 🚗 Vehicle Speed Estimation using YOLOv8 & ByteTrack

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![YOLOv8](https://img.shields.io/badge/YOLO-v8-yellow.svg)
![ONNX](https://img.shields.io/badge/ONNX-Optimized-red.svg)

## 📌 Introduction
This project estimates the speed of moving vehicles on highways using a fixed-perspective traffic camera. By combining **Object Detection**, **Multi-Object Tracking (MOT)**, and **Projective Geometry (Homography)**, the system can calculate real-time vehicle speed in km/h.

**🚀 Demo:**
*(Chèn ảnh GIF hoặc link YouTube của bạn vào đây. Cú pháp: `![Demo](data/processed/demo_result.mp4`)*

## ⚙️ Key Technologies & Skills Demonstrated
- **Detection & Tracking:** Ultralytics YOLOv8, ByteTrack (robust tracking against occlusion).
- **Computer Vision Geometry:** Perspective Transformation (Bird's Eye View mapping).
- **Signal Processing:** Simple Moving Average (SMA) filter to handle bounding box jitter and stabilize speed calculation.
- **MLOps & Optimization:** Exported PyTorch model to **ONNX** format for faster inference latency.
- **Code Architecture:** Object-Oriented Programming (OOP) design.

## 🛠️ Project Structure
```text
Vehicle-Speed-Estimation/
├── data/raw/              # Input traffic videos
├── models/                # YOLOv8 weights (.pt & .onnx) & Calibration matrix
├── src/core/              # Main modules (Tracker, Speed Estimator)
├── src/utils/             # Calibration and model export scripts
└── main.py                # Pipeline execution
```

## 🚀 Installation & Usage

**1. Clone the repository and install dependencies:**
```bash
git clone [https://github.com/your-username/Vehicle-Speed-Estimation.git](https://github.com/your-username/Vehicle-Speed-Estimation.git)
cd Vehicle-Speed-Estimation
pip install -r requirements.txt
```

**2. Calibrate the Camera (Perspective Transform):**
*Run the calibration script and click 4 points on the road to define the measurement area.*
```bash
python src/utils/calibration.py
```

**3. Run the Inference Pipeline:**
```bash
python main.py
```

## 🧠 Methodology (How it works)
1. **Object Detection:** YOLOv8 detects vehicles (cars, trucks, buses).
2. **Object Tracking:** ByteTrack assigns a unique ID to each detected vehicle and maintains its trajectory.
3. **Perspective Transform:** Pixel coordinates are mapped to real-world metric coordinates (Meters) using a calibrated Homography Matrix to simulate a Bird's Eye View.
4. **Speed Calculation:** Velocity is calculated using $v = d / \Delta t$ over a designated frame window, applying a smoothing filter to eliminate noise.
```