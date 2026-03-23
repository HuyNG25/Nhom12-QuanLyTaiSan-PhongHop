
<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
    ERP: HỆ THỐNG QUẢN LÝ TÀI SẢN CHUNG VÀ PHÒNG HỌP
</h2>
<div align="center">
    <p align="center">
        <img src="docs/logo/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/logo/fitdnu_logo.png" alt="FIT DNU Logo" width="180"/>
        <img src="docs/logo/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of IT](https://img.shields.io/badge/Faculty%20of%20IT-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)
[![Odoo 15](https://img.shields.io/badge/Odoo-15.0-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

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
git clone https://github.com/HuyNG25/Nhom12-QuanLyTaiSan-PhongHop.git
cd Nhom12-QuanLyTaiSan-PhongHop
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
Học Phần: Hội nhập và quản trị phần mềm doanh - Đề Tài 6

