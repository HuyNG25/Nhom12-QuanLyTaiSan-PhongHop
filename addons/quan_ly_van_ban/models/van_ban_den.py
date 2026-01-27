from odoo import models, fields

class VanBanDen(models.Model):
    _name = 'quanly.vanbanden'
    _description = 'Văn Bản Đến'
    _rec_name = 'so_hieu'

    so_hieu = fields.Char(string='Số hiệu', required=True)
    tieu_de = fields.Char(string='Tiêu đề', required=True)
    ngay_den = fields.Date(string='Ngày đến', default=fields.Date.today)
    noi_gui = fields.Char(string='Nơi gửi')
    
    # Liên kết tới bảng Loại Văn Bản ở trên
    loai_vb_id = fields.Many2one('quanly.loaivanban', string='Loại văn bản')
    
    tep_dinh_kem = fields.Binary(string='Tệp đính kèm')
    noi_dung = fields.Text(string='Trích yếu nội dung')