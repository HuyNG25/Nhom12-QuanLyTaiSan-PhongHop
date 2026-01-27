from odoo import models, fields

class VanBanDi(models.Model):
    _name = 'quanly.vanbandi'
    _description = 'Văn Bản Đi'
    _rec_name = 'so_hieu'

    so_hieu = fields.Char(string='Số hiệu', required=True)
    tieu_de = fields.Char(string='Tiêu đề', required=True)
    ngay_di = fields.Date(string='Ngày đi', default=fields.Date.today)
    noi_nhan = fields.Char(string='Nơi nhận')
    nguoi_ky = fields.Char(string='Người ký')
    
    # Liên kết tới bảng Loại Văn Bản
    loai_vb_id = fields.Many2one('quanly.loaivanban', string='Loại văn bản')
    
    tep_dinh_kem = fields.Binary(string='Tệp đính kèm')
    noi_dung = fields.Text(string='Trích yếu nội dung')