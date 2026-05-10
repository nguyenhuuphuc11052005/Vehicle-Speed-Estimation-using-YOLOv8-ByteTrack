import cv2
import numpy as np

# Danh sách lưu 4 điểm người dùng click
points = []

def select_points(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Calibration", img)
        if len(points) == 4:
            print("Đã chọn đủ 4 điểm:", points)

# Load một frame từ video để calibrate
video_path = 'data/raw/traffic_video.mp4' 
# Thay bằng path của bạn
cap = cv2.VideoCapture(video_path)
success, img = cap.read()
cap.release()

if not success:
    print("Không thể mở video")
    exit()

cv2.imshow("Calibration", img)
cv2.setMouseCallback("Calibration", select_points)

print("Hướng dẫn: Click vào 4 điểm theo thứ tự: Trên-Trái, Trên-Phải, Dưới-Phải, Dưới-Trái.")
cv2.waitKey(0)
cv2.destroyAllWindows()

# Sau khi có 4 điểm, tính ma trận Homography 
if len(points) == 4:
    src_pts = np.float32(points)
    # Định nghĩa kích thước vùng quan sát thực tế 
    dst_pts = np.float32([[0, 0], [320, 0], [320, 1400], [0, 1400]])
    
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    np.save("models/calibration_matrix.npy", matrix)
    print("Đã lưu ma trận calibration vào models/calibration_matrix.npy")