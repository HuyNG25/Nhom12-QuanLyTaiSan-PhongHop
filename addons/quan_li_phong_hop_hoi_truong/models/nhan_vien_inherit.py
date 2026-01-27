# -*- coding: utf-8 -*-
from odoo import models, fields

class NhanVien(models.Model):
    _inherit = 'nhan_vien'

    lich_su_dat_phong_ids = fields.One2many(
        comodel_name='dat_phong',
        inverse_name='nguoi_muon_id',
        string="Lịch sử đặt phòng",
        readonly=True
    )
