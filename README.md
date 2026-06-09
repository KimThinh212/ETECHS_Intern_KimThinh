# Metadata Normalizer - ETECHS

Module chuẩn hóa dữ liệu cho MongoDB metadata collections trong dự án Data Warehouse & Middleware - ETECHS.

## 1. Cấu trúc thư mục (Hoàn thành cả 5 Tasks)
```text
metadata_normalizer/
│
├── config/
│   ├── __init__.py             # Đóng gói package config (rỗng)
│   ├── .env                    # MONGO_URI, MONGO_DB_NAME, MONGO_TEST_DB_NAME
│   └── database.py             # Database singleton class (kết nối MongoDB)
│
├── models/
│   ├── __init__.py             # Export tất cả models ra package root
│   ├── base.py                 # BaseMetaModel (class cha) + PyObjectId (tương thích Pydantic v2)
│   ├── student_profile_meta.py # StudentProfileMeta + enums + sub-models (Task 2)
│   └── education_meta.py       # EducationMeta + VerificationStatus (Task 3)
│
├── services/
│   ├── __init__.py             # Đóng gói package services
│   └── metadata_service.py     # MetadataService cung cấp các hàm CRUD và đánh index MongoDB (Task 3)
│
├── tests/
│   ├── __init__.py             # Đóng gói package tests (rỗng)
│   ├── test_student_profile_meta.py  # 8+ test cases cho StudentProfileMeta (Task 2/4)
│   └── test_education_meta.py        # 10+ test cases cho EducationMeta (Task 4)
│
├── main.py                     # Script demo tích hợp toàn bộ hệ thống (Task 5)
├── requirements.txt            # Thư viện phụ thuộc của dự án
└── README.md                   # Hướng dẫn cài đặt, chạy thử và kiểm thử dự án
```

## 2. Các thư viện chính sử dụng
* **pymongo** (v4.10.1): Thư viện Python driver chính thức kết nối và làm việc với MongoDB.
* **pydantic** (v2.10.4): Hỗ trợ validate dữ liệu, định nghĩa data schema mạnh mẽ và chuẩn hóa kiểu dữ liệu.
* **python-dotenv** (v1.0.1): Tự động nạp các biến cấu hình từ file `.env` vào biến môi trường hệ thống.
* **pytest** & **pytest-cov**: Hỗ trợ viết test cases và đo lường độ bao phủ (code coverage) của unit tests.

## 3. Hướng dẫn cài đặt & Thiết lập môi trường ảo
Từ thư mục gốc của dự án `metadata_normalizer/`, thực hiện các bước sau:

### Bước 3.1: Tạo Virtual Environment (venv)
```bash
python -m venv venv
```

### Bước 3.2: Kích hoạt môi trường ảo
* **Trên Windows (PowerShell/CMD):**
  ```powershell
  venv\Scripts\activate
  ```
* **Trên macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### Bước 3.3: Cài đặt Dependencies
```bash
pip install -r requirements.txt
```

## 4. Cấu hình Kết nối CSDL (`config/.env`)
Tạo file `config/.env` với nội dung cấu hình phù hợp với môi trường local của bạn:
```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=etechs_metadata
MONGO_TEST_DB_NAME=etechs_metadata_test
```

## 5. Chạy Demo Tích Hợp (`main.py`)
Đảm bảo bạn đã khởi động MongoDB Server trên cổng `27017`.
Chạy lệnh sau để kiểm tra tích hợp đầy đủ hệ thống:
```bash
python main.py
```
Script sẽ tự động tạo index, thêm (Create), đọc (Read), cập nhật trạng thái (Update) dữ liệu của cả hai collections `student_profile_meta` và `education_meta` xuống database thực tế.

## 6. Chạy Unit Tests (pytest)
Để chạy toàn bộ các bài kiểm thử tự động (Task 4):
```bash
pytest tests/ -v
```

Để đo độ bao phủ code coverage:
```bash
pytest tests/ -v --cov=models --cov-report=term-missing
```
