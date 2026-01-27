# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date


class TinhLuong(models.Model):
    _name = 'tinh_luong'
    _description = 'Bảng tính lương nhân viên'
    _rec_name = 'ten_bang_luong'
    _order = 'nam desc, thang desc'

    nhan_vien_id = fields.Many2one(
        'nhan_vien', 
        string='Nhân viên', 
        required=True
    )
    ten_bang_luong = fields.Char(
        string='Tên bảng lương',
        compute='_compute_ten_bang_luong',
        store=True
    )
    thang = fields.Selection(
        [
            ('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'),
            ('4', 'Tháng 4'), ('5', 'Tháng 5'), ('6', 'Tháng 6'),
            ('7', 'Tháng 7'), ('8', 'Tháng 8'), ('9', 'Tháng 9'),
            ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12'),
        ],
        string='Tháng', 
        required=True, 
        default=lambda self: str(date.today().month)
    )
    nam = fields.Selection(
        [(str(y), str(y)) for y in range(2020, 2031)],
        string='Năm', 
        required=True, 
        default=lambda self: str(date.today().year)
    )
    
    # Lương cơ bản
    luong_co_ban = fields.Float(string='Lương cơ bản', default=0.0)
    
    # Lương ngày = Lương cơ bản / 26
    luong_ngay = fields.Float(
        string='Lương/ngày',
        compute='_compute_luong',
        store=True
    )
    
    # Số công (tổng từ chấm công)
    tong_so_cong = fields.Float(
        string='Tổng số công', 
        compute='_compute_luong',
        store=True
    )
    
    # Tổng giờ tăng ca
    tong_gio_tang_ca = fields.Float(
        string='Tổng giờ tăng ca',
        compute='_compute_luong',
        store=True
    )
    
    # Tiền tăng ca (1.5 lần lương giờ)
    tien_tang_ca = fields.Float(
        string='Tiền tăng ca',
        compute='_compute_luong',
        store=True
    )
    
    # Tổng tiền phạt từ chấm công
    tong_tien_phat = fields.Float(
        string='Tổng tiền phạt',
        compute='_compute_luong',
        store=True
    )
    
    # Thưởng (nhập thủ công)
    thuong = fields.Float(string='Thưởng', default=0.0)
    
    # Phạt bổ sung (nhập thủ công)
    phat_bo_sung = fields.Float(string='Phạt bổ sung', default=0.0)
    
    # Tổng lương
    tong_luong = fields.Float(
        string='Tổng lương', 
        compute='_compute_luong',
        store=True
    )
    
    trang_thai = fields.Selection(
        [
            ('draft', 'Nháp'),
            ('confirmed', 'Đã xác nhận'),
            ('paid', 'Đã thanh toán'),
        ],
        string='Trạng thái',
        default='draft'
    )
    ghi_chu = fields.Text(string='Ghi chú')

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_ten_bang_luong(self):
        for record in self:
            if record.nhan_vien_id and record.thang and record.nam:
                record.ten_bang_luong = f"{record.nhan_vien_id.ho_va_ten} - T{record.thang}/{record.nam}"
            else:
                record.ten_bang_luong = "Bảng lương mới"

    @api.depends('nhan_vien_id', 'thang', 'nam', 'luong_co_ban', 'thuong', 'phat_bo_sung')
    def _compute_luong(self):
        NGAY_CONG_CHUAN = 26
        HE_SO_TANG_CA = 1.5
        
        for record in self:
            # Lương ngày
            record.luong_ngay = record.luong_co_ban / NGAY_CONG_CHUAN if NGAY_CONG_CHUAN > 0 else 0
            
            if record.nhan_vien_id and record.thang and record.nam:
                # Tìm tất cả bản ghi chấm công trong tháng
                thang_int = int(record.thang)
                nam_int = int(record.nam)
                
                cham_cong_records = self.env['cham_cong'].search([
                    ('nhan_vien_id', '=', record.nhan_vien_id.id),
                    ('ngay_cham_cong', '>=', f'{nam_int}-{thang_int:02d}-01'),
                    ('ngay_cham_cong', '<=', f'{nam_int}-{thang_int:02d}-31'),
                ])
                
                # Tổng số công
                record.tong_so_cong = sum(cc.so_cong for cc in cham_cong_records)
                
                # Tổng giờ tăng ca
                record.tong_gio_tang_ca = sum(cc.so_gio_tang_ca for cc in cham_cong_records)
                
                # Tiền tăng ca = Giờ tăng ca × (Lương giờ × 1.5)
                luong_gio = record.luong_ngay / 8  # Lương theo giờ
                record.tien_tang_ca = record.tong_gio_tang_ca * luong_gio * HE_SO_TANG_CA
                
                # Tổng tiền phạt từ đi muộn/về sớm
                record.tong_tien_phat = sum(cc.tien_phat for cc in cham_cong_records)
            else:
                record.tong_so_cong = 0.0
                record.tong_gio_tang_ca = 0.0
                record.tien_tang_ca = 0.0
                record.tong_tien_phat = 0.0
            
            # Tổng lương = Lương ngày × Số công + Thưởng + Tiền tăng ca - Tiền phạt - Phạt bổ sung
            record.tong_luong = (
                record.luong_ngay * record.tong_so_cong 
                + record.thuong 
                + record.tien_tang_ca 
                - record.tong_tien_phat 
                - record.phat_bo_sung
            )

    _sql_constraints = [
        ('unique_tinh_luong', 
         'unique(nhan_vien_id, thang, nam)', 
         'Mỗi nhân viên chỉ có một bảng lương cho mỗi tháng!')
    ]
