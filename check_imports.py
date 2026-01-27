
import sys
import os

# Add addons path
sys.path.append('/home/dmin/Business-Internship/odoo')
sys.path.append('/home/dmin/Business-Internship/addons')

print("Checking imports for quan_ly_tai_san...")

try:
    from quan_ly_tai_san.models import tai_san
    print("Import tai_san: OK")
except Exception as e:
    print(f"Import tai_san FAILED: {e}")

try:
    from quan_ly_tai_san.models import thong_ke
    print("Import thong_ke: OK")
except Exception as e:
    print(f"Import thong_ke FAILED: {e}")

try:
    from quan_ly_tai_san.models import phieu_muon
    print("Import phieu_muon: OK")
except Exception as e:
    print(f"Import phieu_muon FAILED: {e}")

print("Import check complete.")
