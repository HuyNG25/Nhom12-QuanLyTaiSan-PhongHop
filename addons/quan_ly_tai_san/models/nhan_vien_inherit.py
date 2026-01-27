# -*- coding: utf-8 -*-
from odoo import models, fields

class NhanVien(models.Model):
    _inherit = 'nhan_vien'

    tai_san_ids = fields.One2many(
        comodel_name='tai_san',
        inverse_name='nguoi_dang_dung_id',
        string="Tài sản đang giữ",
        domain=[('trang_thai', '=', 'Muon')],
        readonly=True
    )
