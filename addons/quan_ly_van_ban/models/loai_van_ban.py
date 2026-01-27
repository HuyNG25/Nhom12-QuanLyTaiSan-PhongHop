from odoo import models, fields

class LoaiVanBan(models.Model):
    _name = 'quanly.loaivanban'
    _description = 'Loại Văn Bản'
    _rec_name = 'ten_loai'

    ten_loai = fields.Char(string='Tên Loại', required=True)
    mo_ta = fields.Text(string='Mô tả')