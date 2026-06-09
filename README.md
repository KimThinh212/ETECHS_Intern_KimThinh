# Metadata Normalizer - ETECHS

Module chuẩn hóa dữ liệu cho MongoDB metadata collections trong dự án Data Warehouse & Middleware - ETECHS.

## 1. Cấu trúc thư mục
```text
metadata_normalizer/
├── config/
│   ├── __init__.py          # Khởi tạo config package
│   ├── .env                 # Biến môi trường kết nối MongoDB (Không commit lên Git)
│   └── database.py          # Singleton class quản lý kết nối MongoDB
├── models/
│   ├── __init__.py          # Export tất cả các model ra package root
│   ├── base.py              # BaseMetaModel (class cha) & PyObjectId (validator v2)
│   ├── student_profile_meta.py # Schema & validation cho student_profile_meta (Task 2)
│   └── education_meta.py    # Schema & validation cho education_meta (Task 3)
├── services/
│   ├── __init__.py          # Export MetadataService ra package root
│   └── metadata_service.py  # MetadataService dùng chung để CRUD và đánh index MongoDB (Task 3)
├── tests/
│   ├── __init__.py          # Khởi tạo tests package
│   ├── test_student_profile_meta.py # Unit tests cho class StudentProfileMeta (Task 2)
│   └── test_education_meta.py       # Unit tests cho class EducationMeta (Task 4)
├── .gitignore               # Loại bỏ venv, file cấu hình bảo mật .env, cache
├── README.md                # Tài liệu hướng dẫn dự án
└── requirements.txt         # Khai báo các thư viện phụ thuộc (pinned versions)
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
Tạo file `config/.env` với nội dung cấu hình phù hợp với môi trường local của bạn (Sử dụng cổng `27018` để tránh xung đột cổng):
```env
MONGO_URI=mongodb://localhost:27018
MONGO_DB_NAME=etechs_metadata
MONGO_TEST_DB_NAME=etechs_metadata_test
```

## 5. Chạy kiểm tra kết nối Database
Để đảm bảo cấu hình kết nối MongoDB thông qua `config/database.py` hoạt động chính xác:
```bash
python -c "import sys; sys.path.insert(0, '.'); from config.database import Database; print('Kết nối:', Database.get_client())"
```

## 6. Chạy Unit Tests (pytest)
Để chạy toàn bộ các bài kiểm thử tự động (Task 4):
```bash
pytest tests/ -v
```

Để chạy riêng lẻ từng bộ kiểm thử:
* **Kiểm thử StudentProfileMeta (Task 2):**
  ```bash
  pytest tests/test_student_profile_meta.py -v
  ```
* **Kiểm thử EducationMeta (Task 4):**
  ```bash
  pytest tests/test_education_meta.py -v
  ```

Để đo độ bao phủ code coverage:
```bash
pytest tests/ -v --cov=models --cov-report=term-missing
```
