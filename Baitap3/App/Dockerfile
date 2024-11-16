# Sử dụng image python 3.12
FROM python:3.11

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file requirements và cài đặt các gói cần thiết
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ nội dung của thư mục App vào thư mục làm việc trong container
COPY . .

# Mở cổng mà ứng dụng chạy
EXPOSE 5000

# Chạy ứng dụng Flask
CMD ["python", "app.py"]
