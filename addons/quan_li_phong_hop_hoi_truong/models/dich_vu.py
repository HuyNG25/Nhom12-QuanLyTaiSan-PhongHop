from odoo import models, fields

class DichVuDiKem(models.Model):
    _name = 'dich_vu_di_kem'
    _description = 'Dịch vụ đi kèm'

    name = fields.Char(string="Tên dịch vụ", required=True)
    don_gia = fields.Float(string="Đơn giá", default=0.0)
    mo_ta = fields.Text(string="Mô tả")
