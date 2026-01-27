# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ChamCong(models.Model):
    _name = 'cham_cong'
    _description = 'Bảng chấm công nhân viên'
    _order = 'ngay_cham_cong desc'

    nhan_vien_id = fields.Many2one(
        'nhan_vien', 
        string='Nhân viên', 
        required=True
    )
    ngay_cham_cong = fields.Date(
        string='Ngày chấm công', 
        required=True, 
        default=fields.Date.today
    )
    
    # Giờ vào/ra (float: 8.0 = 8:00, 8.5 = 8:30, 17.0 = 17:00)
    gio_vao = fields.Float(string='Giờ vào', default=8.0)
    gio_ra = fields.Float(string='Giờ ra', default=17.0)
    
    # Số giờ làm thực tế
    so_gio_lam = fields.Float(
        string='Số giờ làm', 
        compute='_compute_cham_cong',
        store=True
    )
    
    # Số công trong ngày (0.5, 1.0, 1.5, 2.0...)
    so_cong = fields.Float(
        string='Số công',
        compute='_compute_cham_cong',
        store=True
    )
    
    # Đi muộn (phút)
    di_muon = fields.Integer(
        string='Đi muộn (phút)',
        compute='_compute_cham_cong',
        store=True
    )
    
    # Về sớm (phút)
    ve_som = fields.Integer(
        string='Về sớm (phút)',
        compute='_compute_cham_cong',
        store=True
    )
    
    # Số giờ tăng ca
    so_gio_tang_ca = fields.Float(
        string='Giờ tăng ca',
        compute='_compute_cham_cong',
        store=True
    )
    
    # Tiền phạt (50.000đ/lần đi muộn hoặc về sớm)
    tien_phat = fields.Float(
        string='Tiền phạt',
        compute='_compute_cham_cong',
        store=True
    )
    
    trang_thai = fields.Selection(
        [
            ('di_lam', 'Đi làm'),
            ('nghi_phep', 'Nghỉ phép'),
            ('nghi_khong_luong', 'Nghỉ không lương'),
        ],
        string='Trạng thái',
        default='di_lam',
        required=True
    )
    ghi_chu = fields.Text(string='Ghi chú')

    @api.depends('gio_vao', 'gio_ra', 'trang_thai')
    def _compute_cham_cong(self):
        GIO_VAO_CHUAN = 8.0   # 8:00
        GIO_RA_CHUAN = 17.0   # 17:00
        GIO_LAM_CHUAN = 8.0   # 8 tiếng
        TIEN_PHAT_MOI_LAN = 50000  # 50.000đ
        
        for record in self:
            if record.trang_thai == 'di_lam':
                # Tính số giờ làm
                record.so_gio_lam = max(0, record.gio_ra - record.gio_vao)
                
                # Tính đi muộn (phút)
                if record.gio_vao > GIO_VAO_CHUAN:
                    record.di_muon = int((record.gio_vao - GIO_VAO_CHUAN) * 60)
                else:
                    record.di_muon = 0
                
                # Tính về sớm (phút)
                if record.gio_ra < GIO_RA_CHUAN:
                    record.ve_som = int((GIO_RA_CHUAN - record.gio_ra) * 60)
                else:
                    record.ve_som = 0
                
                # Tính số công
                if record.so_gio_lam >= GIO_LAM_CHUAN:
                    record.so_cong = 1.0  # Đủ công
                elif record.so_gio_lam >= 4.0:
                    record.so_cong = 0.5  # Nửa công
                else:
                    record.so_cong = 0.0  # Không tính công
                
                # Tính giờ tăng ca (làm quá 8 tiếng)
                if record.so_gio_lam > GIO_LAM_CHUAN:
                    record.so_gio_tang_ca = record.so_gio_lam - GIO_LAM_CHUAN
                    # Cộng thêm công cho tăng ca (mỗi 4h = 0.5 công)
                    record.so_cong += record.so_gio_tang_ca / 8.0
                else:
                    record.so_gio_tang_ca = 0.0
                
                # Tính tiền phạt
                so_lan_phat = 0
                if record.di_muon > 0:
                    so_lan_phat += 1
                if record.ve_som > 0:
                    so_lan_phat += 1
                record.tien_phat = so_lan_phat * TIEN_PHAT_MOI_LAN
                
            elif record.trang_thai == 'nghi_phep':
                record.so_gio_lam = 0.0
                record.so_cong = 1.0  # Nghỉ phép vẫn tính công
                record.di_muon = 0
                record.ve_som = 0
                record.so_gio_tang_ca = 0.0
                record.tien_phat = 0.0
            else:
                record.so_gio_lam = 0.0
                record.so_cong = 0.0
                record.di_muon = 0
                record.ve_som = 0
                record.so_gio_tang_ca = 0.0
                record.tien_phat = 0.0

    _sql_constraints = [
        ('unique_cham_cong', 
         'unique(nhan_vien_id, ngay_cham_cong)', 
         'Mỗi nhân viên chỉ được chấm công một lần trong ngày!')
    ]
