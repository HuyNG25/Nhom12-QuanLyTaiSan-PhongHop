from odoo import models, fields, api, exceptions
from datetime import datetime

class DatPhong(models.Model):
    _name = "dat_phong"
    _description = "Đăng ký mượn phòng"

    phong_id = fields.Many2one("quan_ly_phong_hop", string="Phòng họp", required=True)
    nguoi_muon_id = fields.Many2one("nhan_vien", string="Người mượn", required=True)  
    thoi_gian_muon_du_kien = fields.Datetime(string="Thời gian mượn dự kiến", required=True)
    thoi_gian_muon_thuc_te = fields.Datetime(string="Thời gian mượn thực tế")
    thoi_gian_tra_du_kien = fields.Datetime(string="Thời gian trả dự kiến", required=True)

    thoi_gian_tra_thuc_te = fields.Datetime(string="Thời gian trả thực tế")

    # Liên kết với tài sản (Shared Resource)
    tai_san_ids = fields.Many2many(
        comodel_name="tai_san",
        relation="dat_phong_tai_san_rel",
        column1="dat_phong_id",
        column2="tai_san_id",
        string="Tài sản mượn kèm",
        domain=[('trang_thai', '=', 'LuuTru')]
    )
    
    dich_vu_ids = fields.Many2many(
        comodel_name="dich_vu_di_kem",
        string="Dịch vụ đi kèm"
    )

    kieu_lap = fields.Selection([
        ('khong_lap', 'Không lặp'),
        ('hang_ngay', 'Hàng ngày'),
        ('hang_tuan', 'Hàng tuần'),
        ('hang_thang', 'Hàng tháng')
    ], string="Lặp lại", default='khong_lap', required=True)
    
    ngay_ket_thuc_lap = fields.Date(string="Kết thúc lặp")

    @api.model
    def create(self, vals):
        # Tạo bản ghi gốc
        record = super(DatPhong, self).create(vals)
        
        # Xử lý logic tạo các bản ghi lặp lại
        if vals.get('kieu_lap') and vals.get('kieu_lap') != 'khong_lap' and vals.get('ngay_ket_thuc_lap'):
            record.tao_ban_ghi_lap_lai()
            
        return record

    def tao_ban_ghi_lap_lai(self):
        self.ensure_one()
        from dateutil.relativedelta import relativedelta
        import datetime
        
        start_date = self.thoi_gian_muon_du_kien
        end_date = self.thoi_gian_tra_du_kien
        repeat_until = self.ngay_ket_thuc_lap
        
        if not start_date or not end_date or not repeat_until:
            return

        current_start = start_date
        current_end = end_date
        
        while True:
            # Tính toán thời gian tiếp theo
            if self.kieu_lap == 'hang_ngay':
                delta = relativedelta(days=1)
            elif self.kieu_lap == 'hang_tuan':
                delta = relativedelta(weeks=1)
            elif self.kieu_lap == 'hang_thang':
                delta = relativedelta(months=1)
            else:
                break
                
            current_start += delta
            current_end += delta
            
            # Kiểm tra điều kiện dừng
            if current_start.date() > repeat_until:
                break
                
            # Tạo bản ghi mới (copy từ bản ghi gốc)
            self.copy({
                'thoi_gian_muon_du_kien': current_start,
                'thoi_gian_tra_du_kien': current_end,
                'kieu_lap': 'khong_lap', # Bản ghi con không lặp tiếp
                'ngay_ket_thuc_lap': False,
                'trang_thai': 'chờ_duyệt'
            })

    trang_thai = fields.Selection([
        ("chờ_duyệt", "Chờ duyệt"),
        ("cho_duyet_cap_2", "Chờ Lãnh đạo duyệt"),
        ("đã_duyệt", "Đã duyệt"),
        ("đang_sử_dụng", "Đang sử dụng"),
        ("đã_hủy", "Đã hủy"),
        ("đã_trả", "Đã trả")
    ], string="Trạng thái", default="chờ_duyệt")

    lich_su_ids = fields.One2many("lich_su_thay_doi", "dat_phong_id", string="Lịch sử mượn trả")

    def xac_nhan_duyet_phong(self):
        """ Xác nhận duyệt phòng và tự động hủy các yêu cầu bị trùng thời gian (cùng phòng hoặc khác phòng) """
        for record in self:
            if record.trang_thai != "chờ_duyệt":
                raise exceptions.UserError("Chỉ có thể duyệt yêu cầu có trạng thái 'Chờ duyệt'.")
            
            # Kiểm tra xung đột tài sản
            for asset in record.tai_san_ids:
                if asset.trang_thai != 'LuuTru':
                     raise exceptions.UserError(f"Tài sản {asset.ten_tai_san} đang không sẵn sàng (Trạng thái: {asset.trang_thai}).")

            # Duyệt yêu cầu hiện tại
            # Kiểm tra loại phòng để phân quyền duyệt
            if record.phong_id.loai_phong == 'hoi_truong_lon':
                record.write({"trang_thai": "cho_duyet_cap_2"})
            else:
                record.write({"trang_thai": "đã_duyệt"})
            
            self.lich_su(record)

    def xac_nhan_duyet_cap_2(self):
        for record in self:
            if record.trang_thai != "cho_duyet_cap_2":
                raise exceptions.UserError("Chỉ có thể duyệt yêu cầu đang chờ cấp 2 duyệt.")
            
            record.write({"trang_thai": "đã_duyệt"})
            self.lich_su(record)

            # Logic hủy các yêu cầu trùng (đã copy từ trên xuống để đảm bảo chạy khi duyệt chính thức)
            # Hủy các yêu cầu cùng phòng có thời gian trùng lặp
            cung_phong_trung_thoi_gian = [
                ('phong_id', '=', record.phong_id.id),
                ('id', '!=', record.id),
                ('trang_thai', 'in', ['chờ_duyệt', 'cho_duyet_cap_2']),
                ('thoi_gian_muon_du_kien', '<', record.thoi_gian_tra_du_kien),
                ('thoi_gian_tra_du_kien', '>', record.thoi_gian_muon_du_kien)
            ]
            xu_li_cung_phong_trung_thoi_gian = self.search(cung_phong_trung_thoi_gian)
            for other in xu_li_cung_phong_trung_thoi_gian:
                other.write({"trang_thai": "đã_hủy"})
                self.lich_su(other)


            # Hủy các yêu cầu cùng phòng có thời gian trùng lặp
            cung_phong_trung_thoi_gian = [
                ('phong_id', '=', record.phong_id.id),
                ('id', '!=', record.id),
                ('trang_thai', '=', 'chờ_duyệt'),
                ('thoi_gian_muon_du_kien', '<', record.thoi_gian_tra_du_kien),
                ('thoi_gian_tra_du_kien', '>', record.thoi_gian_muon_du_kien)
            ]
            xu_li_cung_phong_trung_thoi_gian = self.search(cung_phong_trung_thoi_gian)
            for other in xu_li_cung_phong_trung_thoi_gian:
                other.write({"trang_thai": "đã_hủy"})
                self.lich_su(other)

            # Hủy các yêu cầu khác phòng nhưng của cùng một người mượn nếu bị trùng thời gian
            khac_phong_trung_thoi_gian = [
                ('nguoi_muon_id', '=', record.nguoi_muon_id.id),
                ('id', '!=', record.id),
                ('trang_thai', '=', 'chờ_duyệt'),
                ('thoi_gian_muon_du_kien', '<', record.thoi_gian_tra_du_kien),
                ('thoi_gian_tra_du_kien', '>', record.thoi_gian_muon_du_kien)
            ]
            xu_li_khac_phong_trung_thoi_gian = self.search(khac_phong_trung_thoi_gian)
            for other in xu_li_khac_phong_trung_thoi_gian:
                other.write({"trang_thai": "đã_hủy"})
                self.lich_su(other)

    def huy_muon_phong(self):
        """ Hủy đăng ký mượn phòng """
        for record in self:
            if record.trang_thai != "chờ_duyệt":
                raise exceptions.UserError("Chỉ có thể hủy yêu cầu có trạng thái 'Chờ duyệt'.")
            record.write({"trang_thai": "đã_hủy"})
            self.lich_su(record)

    def huy_da_duyet(self):
        """ Hủy yêu cầu đã duyệt """
        for record in self:
            if record.trang_thai != "đã_duyệt":
                raise exceptions.UserError("Chỉ có thể hủy yêu cầu có trạng thái 'Đã duyệt'.")
            
            record.write({"trang_thai": "đã_hủy"})
            self.lich_su(record)

    def bat_dau_su_dung(self):
        """ Bắt đầu sử dụng phòng - Cập nhật thời gian mượn thực tế """
        for record in self:
            if record.trang_thai != "đã_duyệt":
                raise exceptions.UserError("Chỉ có thể bắt đầu sử dụng phòng có trạng thái 'Đã duyệt'.")

            # Kiểm tra nếu đã có người đang sử dụng phòng này
            kiem_tra_phong = self.env["dat_phong"].search([
                ("phong_id", "=", record.phong_id.id),
                ("trang_thai", "=", "đang_sử_dụng"),
                ("id", "!=", record.id)
            ])

            if kiem_tra_phong:
                raise exceptions.UserError(f"Phòng {record.phong_id.name} hiện đang được sử dụng. Vui lòng chờ đến khi phòng trống.")

            # Nếu không có ai đang sử dụng, cho phép bắt đầu
            record.write({
                "trang_thai": "đang_sử_dụng",
                "thoi_gian_muon_thuc_te": datetime.now()
            })
            self.lich_su(record)


    def tra_phong(self):
        """ Trả phòng - Cập nhật thời gian trả thực tế và đảm bảo thời gian mượn thực tế có giá trị """
        for record in self:
            if record.trang_thai != "đang_sử_dụng":
                raise exceptions.UserError("Chỉ có thể trả phòng đang ở trạng thái 'Đang sử dụng'.")
            current_time = datetime.now()
            record.write({
                "trang_thai": "đã_trả",
                "thoi_gian_tra_thuc_te": current_time,
                "thoi_gian_muon_thuc_te": record.thoi_gian_muon_thuc_te or current_time
            })
            self.lich_su(record)

    @api.model
    def lich_su(self, record):
        """ Ghi vào lịch sử mượn trả """
        self.env["lich_su_thay_doi"].create({
            "dat_phong_id": record.id,
            "nguoi_muon_id": record.nguoi_muon_id.id,
            "thoi_gian_muon_du_kien": record.thoi_gian_muon_du_kien,
            "thoi_gian_muon_thuc_te": record.thoi_gian_muon_thuc_te,
            "thoi_gian_tra_du_kien": record.thoi_gian_tra_du_kien,
            "thoi_gian_tra_thuc_te": record.thoi_gian_tra_thuc_te,
            "trang_thai": record.trang_thai
        })
