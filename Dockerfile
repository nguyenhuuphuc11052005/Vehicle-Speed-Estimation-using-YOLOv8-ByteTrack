# 1. Dùng image Python bản nhẹ (slim)
FROM python:3.9-slim

# 2. Đặt thư mục làm việc trong container
WORKDIR /app

# 3. SỬA TÊN GÓI THƯ VIỆN Ở ĐÂY: Dùng libgl1 thay vì libgl1-mesa-glx
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy file requirements và cài đặt thư viện Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy toàn bộ mã nguồn và model vào container
COPY src/ src/
COPY models/ models/
COPY main.py .

# 6. Lệnh mặc định khi container chạy
CMD ["python", "main.py"]