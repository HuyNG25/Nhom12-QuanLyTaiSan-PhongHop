import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class ChiTietPhieuMuon(models.Model):
    _name = 'chi_tiet_phieu_muon'
    _description = 'Chi tiết phiếu mượn'

    phieu_muon_id = fields.Many2one('phieu_muon', string='Phiếu mượn', ondelete='cascade')
    tai_san_id = fields.Many2one('tai_san', string='Tài sản', required=True, domain=[('trang_thai', '=', 'LuuTru')])
    ghi_chu = fields.Char('Ghi chú')
    trang_thai = fields.Selection([
        ('dang_muon', 'Đang mượn'),
        ('da_tra', 'Đã trả')
    ], string='Trạng thái', default='dang_muon')

class PhieuMuon(models.Model):
    _name = 'phieu_muon'
    _description = 'Phiếu mượn tài sản'
    _order = 'ma_phieu_muon'

    ma_phieu_muon = fields.Char("Mã phiếu mượn",  copy=False, readonly=True, default="New",
                                states={'draft': [('readonly', False)]})
    ngay_muon_du_kien = fields.Datetime("Thời gian mượn dự kiến", required=True,
                                        states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                                'cancelled': [('readonly', True)]})
    ngay_muon_thuc_te = fields.Datetime("Thời gian mượn thực tế", required=False,
                                        states={'draft': [('readonly', True)], 'approved': [('readonly', False)],
                                                'done': [('readonly', True)], 'cancelled': [('readonly', True)]})
    ngay_tra_du_kien = fields.Datetime("Thời gian trả dự kiến", required=True,
                                       states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                               'cancelled': [('readonly', True)]})
    ngay_tra_thuc_te = fields.Datetime("Thời gian trả thực tế", required=False,
                                       states={'draft': [('readonly', True)], 'approved': [('readonly', False)],
                                               'done': [('readonly', True)], 'cancelled': [('readonly', True)]})
    ghi_chu = fields.Char("Ghi chú", states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                             'cancelled': [('readonly', True)]})
    nhan_vien_id = fields.Many2one(comodel_name="nhan_vien", string="Nhân sự", required=True, store=True,
                                   states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                           'cancelled': [('readonly', True)]})
    
    chi_tiet_ids = fields.One2many('chi_tiet_phieu_muon', 'phieu_muon_id', string='Danh sách tài sản',
                                   states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                           'cancelled': [('readonly', True)]})

    state = fields.Selection(
        [('draft', 'Nháp'), ('approved', 'Đã duyệt'), ('done', 'Hoàn thành'), ('cancelled', 'Hủy')],
        default='draft', string="Trạng thái")
    trang_thai_muon = fields.Char('Trạng thái mượn', compute='_compute_trang_thai_muon', store=True)

    @api.constrains('ma_phieu_muon')
    def _check_ma_phieu_muon_format(self):
        for record in self:
            if not re.fullmatch(r'PM-\d{5}', record.ma_phieu_muon):
                raise ValidationError("Mã phải có định dạng PM-XXXXX (ví dụ: PM-12345)")

    @api.model
    def create(self, vals):
        if vals.get('ma_phieu_muon', 'New') == 'New':
            last_record = self.search([], order='ma_phieu_muon desc', limit=1)
            if last_record and last_record.ma_phieu_muon:
                last_number = int(last_record.ma_phieu_muon.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
            vals['ma_phieu_muon'] = f'PM-{new_number:05d}'
        return super(PhieuMuon, self).create(vals)


    @api.depends('ngay_muon_du_kien', 'ngay_muon_thuc_te', 'ngay_tra_du_kien', 'ngay_tra_thuc_te')
    def _compute_trang_thai_muon(self):
        for record in self:
            muon_do_muon = (
                record.ngay_muon_thuc_te
                and record.ngay_muon_du_kien
                and record.ngay_muon_thuc_te > record.ngay_muon_du_kien
            )
            tra_do_muon = (
                record.ngay_tra_thuc_te
                and record.ngay_tra_du_kien
                and record.ngay_tra_thuc_te > record.ngay_tra_du_kien
            )
            if muon_do_muon and tra_do_muon:
                record.trang_thai_muon = 'Mượn muộn và trả muộn'
            elif muon_do_muon:
                record.trang_thai_muon = 'Mượn muộn'
            elif tra_do_muon:
                record.trang_thai_muon = 'Trả muộn'
            elif record.ngay_muon_thuc_te and record.ngay_tra_thuc_te:
                record.trang_thai_muon = 'Đúng hạn'
            elif record.ngay_muon_thuc_te:
                record.trang_thai_muon = 'Đang mượn'
            else:
                record.trang_thai_muon = 'Chưa mượn'

    def action_approve(self):
        for record in self:
            if not record.chi_tiet_ids:
                raise UserError("Vui lòng chọn ít nhất một tài sản để mượn!")
                
            if record.state == 'draft':
                for item in record.chi_tiet_ids:
                    if item.tai_san_id.trang_thai != 'LuuTru':
                        raise UserError(f"Tài sản {item.tai_san_id.ten_tai_san} không sẵn sàng để mượn!")
                        
                    self.env['lich_su_su_dung'].create({
                        'ma_lich_su_su_dung': self.env['ir.sequence'].next_by_code('lich_su_su_dung') or 'New',
                        'ngay_muon': record.ngay_muon_du_kien,
                        'ngay_tra': record.ngay_tra_du_kien,
                        'ghi_chu': record.ghi_chu,
                        'nhan_vien_id': record.nhan_vien_id.id,
                        'tai_san_id': item.tai_san_id.id,
                    })
                    item.tai_san_id.write({
                        'trang_thai': 'Muon',
                        'nguoi_dang_dung_id': record.nhan_vien_id.id
                    })
                record.state = 'approved'

    def action_done(self):
        for record in self:
            if record.state == 'approved':
                if not record.ngay_muon_thuc_te or not record.ngay_tra_thuc_te:
                    raise UserError('Vui lòng nhập Ngày mượn thực tế và Ngày trả thực tế trước khi hoàn thành.')
                
                record.state = 'done'
                for item in record.chi_tiet_ids:
                    lich_su = self.env['lich_su_su_dung'].search([
                        ('nhan_vien_id', '=', record.nhan_vien_id.id),
                        ('tai_san_id', '=', item.tai_san_id.id),
                        ('ngay_muon', '=', record.ngay_muon_du_kien),
                        ('ngay_tra', '=', record.ngay_tra_du_kien)
                    ], limit=1)
                    
                    if lich_su:
                        lich_su.write({
                            'ngay_muon': record.ngay_muon_thuc_te,
                            'ngay_tra': record.ngay_tra_thuc_te
                        })
                    
                    item.tai_san_id.write({
                        'trang_thai': 'LuuTru',
                        'nguoi_dang_dung_id': False
                    })
                    item.trang_thai = 'da_tra'

    def action_cancel(self):
        for record in self:
            if record.state in ['draft', 'approved']:
                for item in record.chi_tiet_ids:
                    lich_su_su_dung = self.env['lich_su_su_dung'].search([
                        ('nhan_vien_id', '=', record.nhan_vien_id.id),
                        ('tai_san_id', '=', item.tai_san_id.id),
                        ('ngay_muon', '=', record.ngay_muon_du_kien),
                        ('ngay_tra', '=', record.ngay_tra_du_kien),
                        ('ghi_chu', '=', record.ghi_chu)
                    ])
                    if lich_su_su_dung:
                        lich_su_su_dung.unlink()
                    
                    item.tai_san_id.write({
                        'trang_thai': 'LuuTru',
                        'nguoi_dang_dung_id': False
                    })
                record.state = 'cancelled'

    def action_reset_to_draft(self):
        for record in self:
            if record.state == 'cancelled':
                record.state = 'draft'

    @api.model
    def cron_canh_bao_qua_han(self):
        """
        Quét các phiếu mượn đã duyệt, chưa hoàn thành và quá hạn trả.
        """
        today = fields.Datetime.now()
        # Tìm phiếu: Đã duyệt AND Ngày trả dự kiến < Hiện tại
        overdue_slips = self.search([
            ('state', '=', 'approved'),
            ('ngay_tra_du_kien', '<', today)
        ])
        
        template = self.env.ref('quan_ly_tai_san.email_template_canh_bao_qua_han')
        for slip in overdue_slips:
            # Gửi mail nếu nhân viên có email
            if slip.nhan_vien_id and slip.nhan_vien_id.work_email:
                template.send_mail(slip.id, force_send=True)
