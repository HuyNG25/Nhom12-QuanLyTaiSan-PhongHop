<<<<<<< HEAD
<h2 align="center">
    OFFICE RESOURCE MANAGER
</h2>
<div align="center">

[![Odoo](https://img.shields.io/badge/Odoo-16.0-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

## 📖 1. Giới thiệu
**Office Resource Manager** là hệ thống quản lý tài nguyên doanh nghiệp được xây dựng trên nền tảng Odoo. Hệ thống tập trung vào việc số hóa quy trình quản lý hành chính nội bộ.

### Các module chính:
1.  **Quản lý Nhân sự (`nhan_su`)**: Hồ sơ nhân viên, quản lý thông tin cá nhân.
2.  **Quản lý Tài sản (`quan_ly_tai_san`)**: Theo dõi tài sản, khấu hao, bảo trì, cấp phát tài sản cho nhân viên.
3.  **Quản lý Phòng họp (`quan_li_phong_hop_hoi_truong`)**: Đặt phòng họp, duyệt yêu cầu, tránh trùng lịch.

## 🚀 2. Hướng dẫn Cài đặt & Sử dụng

### 2.1. Clone dự án
Tải mã nguồn về máy:
```bash
git clone https://github.com/HOANGTHI2509/office-resource-manager.git
cd office-resource-manager
```

### 2.2. Cài đặt môi trường
Yêu cầu: `Python 3.10`, `PostgreSQL`, `Docker` (tùy chọn).

1.  **Cài đặt thư viện hệ thống (Ubuntu/WSL):**
    ```bash
    sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-dev build-essential libpq-dev
    ```

2.  **Tạo môi trường ảo & cài dependencies:**
    ```bash
    python3.10 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

### 2.3. Cấu hình Database
Sử dụng Docker để chạy PostgreSQL nhanh chóng:
```bash
sudo docker-compose up -d
```

### 2.4. Cấu hình Odoo
Tạo file `odoo.conf` (hoặc copy từ template):
```ini
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5431
xmlrpc_port = 8069
```

### 2.5. Chạy hệ thống
```bash
python3 odoo-bin.py -c odoo.conf -u nhan_su,quan_ly_tai_san,quan_li_phong_hop_hoi_truong
```
Truy cập: `http://localhost:8069`
Tài khoản mặc định (nếu dùng demo data): `admin` / `admin`

## 🤝 Đóng góp
Dự án được phát triển dựa trên nền tảng Business Internship của Khoa CNTT - Đại học Đại Nam.
=======
# office-resource-manager
Học Phần: Hội nhập và quản trị phần mềm doanh - Đề Tài 6
>>>>>>> 69e84f43b41b1bccf3526d7ca2f6d55f5afc6986
