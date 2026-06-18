import hashlib
from dataclasses import dataclass
import gspread
from google.oauth2.service_account import Credentials
from config.config import Config
from database.db_connect import Database
from services.sheet_validator import SheetValidator


def build_upsert_sql( table_name: str, columns: tuple[str, ...], key_columns: set[str], ) -> str:
    columns_sql = ",\n        ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    update_columns = [column for column in columns if column not in key_columns]
    update_sql = ",\n        ".join(
        f"{column} = VALUES({column})"
        for column in update_columns
    )

    return f"""
    INSERT INTO {table_name} (
        {columns_sql}
    )
    VALUES (
        {placeholders}
    )
    ON DUPLICATE KEY UPDATE
        {update_sql},
        updated_at = NOW()
    """
    
@dataclass(frozen=True)
class SheetConfig:
    table_name: str
    field_map: tuple[tuple[str, str, str], ...]
    key_columns: set[str]
    required_headers: tuple[str, ...] 
    
    @property
    def headers(self) -> tuple[str, ...]:
        return tuple(header for _, header, _ in self.field_map)
    
    @property
    def columns(self) -> tuple[str, ...]:
        return tuple(column for column, _, _ in self.field_map) + ("row_hash",)
    
    @property
    def upsert_sql(self) -> str:
        return build_upsert_sql(
            self.table_name,
            self.columns,
            key_columns=self.key_columns,
        )


class SheetService:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    
    #Sheet 1: Thông tin xe
    VEHICLE_FIELD_MAP = (
        ("stt", "STT", "stt"),
        ("bks", "BKS XE cũ", "text"),
        ("bks_moi", "BKS XE mới", "text"),

        ("loai_xe_chung_loai", "Loại xe chủng loại xe", "text"),
        ("loai_xe", "LOẠI XE", "text"),

        ("don_vi_quan_ly", "Đơn vị quản lý", "text"),
        ("nam_sx", "Năm sx", "int"),

        ("so_may", "Số máy", "text"),
        ("so_khung", "Số khung", "text"),

        ("so_dang_kiem", "Số đăng kiểm", "text"),
        ("ngay_het_han_dang_kiem", "Ngày hết hạn đăng kiểm", "date"),

        ("so_dang_ky", "Số đăng ký", "text"),
        ("dang_ky_goc", "Đăng ký gốc", "date"),

        ("han_gia_han_giay_ngan_hang", "Hạn gia hạn Giấy ngân hàng", "date"),
        ("cong_ty_or_ngan_hang", "Công ty or ngân hàng", "text"),

        ("han_bao_hiem", "Hạn Bảo hiểm", "date"),
        ("cong_ty_bao_hiem", "Công ty Bảo hiểm", "text"),

        ("han_bao_hiem_vc", "Hạn Bảo hiểm VC", "date"),
        ("cong_ty_bao_hiem_vc", "Công ty Bảo hiểm VC", "text"),

        ("han_phu_hieu", "Hạn Phù hiệu", "date"),
        ("thiet_bi_gsht", "Thiết bị GSHT", "text"),

        ("ngay_het_han_camera", "Ngày hết hạn", "date"),
        ("camera_giam_sat", "Camera giám sát", "text"),

        ("tinh_trang", "Tình trạng", "text"),
        ("mau", "Màu", "text"),

        ("kich_thuoc_thung_xe", "Kích thước thùng xe", "text"),
        ("tai_trong_ban_than", "Tải trọng bản thân", "text"),

        ("khoi_luong_cho_phep_tren_mam_keo_tggt", "Khối lượng cho phép trên mâm kéo/ TGGT", "text"),
        ("khoi_luong_hang_cc_theo_tk_cp_tggt", "Khối lượng hàng CC theo TK/CP TGGT", "text"),
        ("khoi_luong_toan_bo_theo_tk_cp_tggt", "Khối lượng toàn bộ theo TK/CP TGGT", "text"),
    )

    VEHICLE_CONFIG = SheetConfig(
        table_name="thong_tin_xe",
        field_map=VEHICLE_FIELD_MAP,
        key_columns={"stt"},
        required_headers=("STT",),
    )
    
    #Sheet 2: Thông tin rơ móc
    
    TRAILER_FIELD_MAP = (
        ("stt", "STT", "stt"),
        ("bks_ro_mooc_cu", "BKS RMOOC cũ", "text"),
        ("bks_ro_mooc_moi", "BKS RMOOC mới", "text"),
        ("loai", "Loại", "text"),
        ("loai_mooc", "Loại mooc", "text"),
        ("don_vi_quan_ly", "Đơn vị quản lý", "text"),
        ("nam_san_xuat", "Năm sản xuất", "int"),
        ("so_khung", "Số khung", "text"),
        ("so_dang_kiem", "Số đăng kiểm", "text"),
        ("ngay_het_han_dang_kiem", "Ngày hết hạn đăng kiểm", "date"),
        ("so_dang_ky", "Số Đăng ký", "text"),
        ("ngay_het_han", "Ngày hết hạn", "date"),
        ("ngay_het_han_giay_ngan_hang", "Ngày hết hạn giấy ngân hàng", "date"),
        ("ngan_hang", "Ngân hàng", "text"),
        ("ngay_het_han_bao_hiem", "Ngày hết hạn bảo hiểm", "date"),
        ("cong_ty_bao_hiem", "Công ty Bảo hiểm", "text"),
        ("mau", "Màu", "text"),
        ("khoi_luong_ban_than", "Khối lượng bản thân", "text"),
        ("khoi_luong_chuyen_cho", "Khối lượng chuyên chở", "text"),
        ("hien_trang", "Hiện trạng", "text"),
    )
    
    TRAILER_CONFIG = SheetConfig(
        table_name="thong_tin_ro_mooc",
        field_map=TRAILER_FIELD_MAP,
        key_columns={"stt"},
        required_headers=("STT",),
    )
    
    #Sheet kế hoạch đăng kiểm
    INSPECTION_FIELD_MAP = (
        ("stt", "STT", "stt"),
        ("bks_xe_cu", "BKS XE cũ", "text"),
        ("bks_xe_moi", "BKS XE mới", "text"),
        ("phan_loai_doi", "Phân loại đội", "text"),
        ("chung_loai_xe", "Chủng loại xe", "text"),
        ("han_dang_kiem_xe", "Hạn đăng kiểm", "date"),
        ("bks_ro_mooc", "BKS RMOOC", "text"),
        ("chung_loai_mooc", "Chủng loại mooc", "text"),
        ("han_dang_kiem_ro_mooc", "Hạn đăng kiểm rơ mooc", "date"),
        ("dang_kiem_tai", "Đăng kiểm tại", "text"),
        ("ngay_thuc_hien", "Ngày thực hiện", "date"),
        ("so_luong", "Số lượng", "int"),
        ("don_gia", "Đơn giá", "text"),
        ("thanh_tien", "Thành tiền", "text"),
        ("chi_phi_thuc_hien", "Chi phí thực hiện", "text"),
        ("tinh_trang_thanh_toan", "Tình trạng thanh toán", "text"),
        ("ghi_chu", "Ghi chú", "text"),
    )
    
    INSPECTION_CONFIG = SheetConfig(
        table_name="kh_dang_kiem",
        field_map=INSPECTION_FIELD_MAP,
        key_columns={"stt"},
        required_headers=("STT",),
    )

    #Ghép xe
    Ghep_xe_FIELD_MAP = (
        ("stt", "STT", "stt"),
        ("bks_xe_cu", "BSỐ XE", "text"),
        ("bks_xe_moi", "BSỐ XE mới", "text"),
        ("chung_loai_xe", "CHỦNG LOẠI XE", "text"),
        ("bks_ro_mooc_cu", "SỐ RMOOC", "text"),
        ("bks_ro_mooc_moi", "SỐ RMOOC mới", "text"),
        ("so_cont", "SỐ CONT", "text"),
        ("loai_cont", "LOẠI CONT", "text"),
        ("ngay_thay_doi", "NGÀY THAY ĐỔI", "date"),
        ("ho_ten_lx", "HỌ VÀ TÊN LX", "text"),
        ("cccd", "CCCD", "text"),
        ("gplx", "GPLX", "text"),
        ("sdt", "SỐ ĐT", "text"),
        ("dv_quan_ly", "ĐV quản lý", "text"),
        ("nguoi_dieu_hanh", "NGƯỜI ĐIỀU HÀNH", "text"),
    )
    
    GHEP_CONFIG = SheetConfig(
        table_name="ghep_xe",
        field_map=Ghep_xe_FIELD_MAP,
        key_columns={"stt"},
        required_headers=("STT",),
    )
    
    #Thay dầu
    Thay_dau_FIELD_MAP = (
        ("stt", "STT", "stt"),
        ("bks_xe_cu", "BKS", "text"),
        ("bks_xe_moi", "BKS2", "text"),
        ("loai_xe_chung_loai", "Loại xe chủng loại xe", "text"),
        ("loai_xe", "LOẠI XE", "text"),
        ("don_vi_quan_ly", "Đơn vị quản lý", "text"),
        ("mau", "Màu", "text"),
        ("loai_dau", "Loại dầu", "text"),
        ("muc_thay_dau", "Mức thay dầu", "text"),
        ("ngay_thay_dau_gan_nhat", "Ngày thay dầu gần nhất", "date"),
        ("km_lan_thay_dau_truoc", "KM lần thay dầu trước", "text"),
        ("km_hien_tai", "KM hiện tại", "text"),
        ("ngay_cap_nhat", "Ngày cập nhật", "date"),
        ("km_da_chay", "KM đã chạy", "text"),
        ("skm_con_lai_den_thay_dau", "Số km còn lại đến thay dầu" , "text"),
    )
    
    THAY_DAU_CONFIG = SheetConfig(
        table_name="thay_dau",
        field_map=Thay_dau_FIELD_MAP,
        key_columns={"stt"},
        required_headers=("STT",),
    )
    
    #lịch sử bdsc
    LICH_SU_BDSC_FIELD_MAP = (
        ("stt", "STT", "stt"),
        ("bks_xe_cu", "BKS XE cũ", "text"),
        ("bks_xe_moi", "BKS XE mới", "text"),
        ("gara", "Gara", "text"),
        ("ngay_phat_sinh", "Ngày phát sinh", "date"),
        ("ky_phat_sinh", "Kỳ phát sinh", "text"),
        ("ten_cs", "Tên CS", "text"),
        ("noi_dung", "Nội dung", "text"),
        ("phan_loai_chi_phi", "Phân loại chi phí", "text"),
        ("tk_14421", "14421", "text"),
        ("gia_tri_mua_chua_vat", "Giá trị mua (chưa VAT)", "text"),
        ("gia_tri_mua_da_vat", "Giá trị mua (đã VAT)", "text"),
        ("thoi_gian_phan_bo", "Thời gian phân bổ", "text"),
        ("thoi_gian_con_lai", "Thời gian còn lại", "text"),
        ("gia_tri_con_lai", "Giá trị còn lại", "text"),
        ("luy_ke_2025", "Lũy kế 2025", "text"),
        ("luy_ke_2026", "Lũy kế 2026", "text"),
        ("thang_1", "1/2026", "text"),
        ("thang_2", "2/2026", "text"),
        ("thang_3", "3/2026", "text"),
        ("thang_4", "4/2026", "text"),
        ("thang_5", "5/2026", "text"),
        ("thang_6", "6/2026", "text"),
        ("thang_7", "7/2026", "text"),
        ("thang_8", "8/2026", "text"),
        ("thang_9", "9/2026", "text"),  
        ("thang_10", "10/2026", "text"),
        ("thang_11", "11/2026", "text"),
        ("thang_12", "12/2026", "text"),
    )
    
    LICH_SU_BDSC_CONFIG = SheetConfig(
        table_name="lsu_bdsc",
        field_map=LICH_SU_BDSC_FIELD_MAP,
        key_columns={"stt"},
        required_headers=("STT",),
    )
    
    #kế hoạch
    KE_HOACH_FIELD_MAP = (
        ("stt", "STT", "stt"),
        ("bks", "BKS", "text"),
        ("tach_5_so", "Tách 5 số", "text"),
        ("phan_loai_doi", "Phân loại đội", "text"),
        ("chung_loai", "Chủng loại", "text"),
        ("ngay_du_kien_thuc_hien", "Ngày dự kiến thực hiện", "date"),
        ("ngay_thuc_hien", "Ngày thực hiện", "date"),
        ("noi_dung_sua_chua", "Nội dung sửa chữa", "text"),
        ("don_vi", "Đơn vị", "text"),
        ("so_luong", "Số lượng", "int"),
        ("don_gia", "Đơn giá", "text"),
        ("thanh_tien", "Thành tiền", "text"),
        ("chi_phi_thuc_te", "Chi phí thực tế", "text"),
        ("tinh_trang_thanh_toan", "Tình trạng thanh toán", "text"),
        ("ghi_chu", "Ghi chú", "text"),
    )
    
    KE_HOACH_CONFIG = SheetConfig(
        table_name="khbd_sc",
        field_map=KE_HOACH_FIELD_MAP,
        key_columns={"stt"},
        required_headers=("STT",),
    )
    
    @staticmethod
    def connect_worksheet(sheet_name: str):
        credentials = Credentials.from_service_account_file(
            Config.CREDENTIALS_PATH,
            scopes=SheetService.SCOPES
        )
        client = gspread.authorize(credentials)
        spreadsheet = client.open_by_key(Config.GOOGLE_SHEET_ID)
        return spreadsheet.worksheet(sheet_name)

    @staticmethod
    def get_connect(sheet_name: str):
        return SheetService.connect_worksheet(sheet_name)

    @staticmethod
    def read_records(
        worksheet,
        header_row: int,
        headers: tuple[str, ...] | None = None,
        required_headers: tuple[str, ...] | None = None,
    ) -> list[dict]:
        values = worksheet.get_all_values()
        if header_row < 1 or header_row > len(values):
            raise ValueError(f"Header row {header_row} is outside sheet data")

        # Google Sheet row numbers start at 1, Python list indexes start at 0.
        sheet_headers = [str(header).strip() for header in values[header_row - 1]]
        selected_headers = headers or tuple(header for header in sheet_headers if header)
        required_headers = required_headers or selected_headers
        column_indexes = SheetService.find_column_indexes(
            sheet_headers,
            selected_headers,
            required_headers,
        )

        records = []
        for row_values in values[header_row:]:
            if SheetService.is_empty_row(row_values):
                continue

            record = {}
            for header, column_index in column_indexes.items():
                value = row_values[column_index] if column_index < len(row_values) else ""
                record[header] = str(value).strip()

            records.append(record)

        return records

    @staticmethod
    def find_column_indexes(
        sheet_headers: list[str],
        selected_headers: tuple[str, ...],
        required_headers: tuple[str, ...],
    ) -> dict[str, int]:
        missing_headers = [
            header for header in required_headers
            if header not in sheet_headers
        ]
        if missing_headers:
            raise ValueError(f"Missing required headers: {', '.join(missing_headers)}")

        return {
            header: sheet_headers.index(header)
            for header in selected_headers
            if header in sheet_headers
        }

    @staticmethod
    def is_empty_row(row_values: list) -> bool:
        return not any(str(value).strip() for value in row_values)

    @staticmethod
    def build_batch(rows: list[dict], config: SheetConfig) -> list[tuple]:
        batch = []
        key_header = config.required_headers[0]
        for row in rows:
            stt_value = str(row.get(key_header) or "").strip()
            
            if not stt_value:
                continue
            
            if key_header in ("STT",) and not stt_value.isdigit():
                continue 
            
            batch.append(SheetService.build_row_values(row, config))
            
        return batch

    @staticmethod
    def has_vehicle_stt(row: dict) -> bool:
        return bool(str(row.get("STT") or "").strip())

    @staticmethod
    def build_row_values(row: dict, config: SheetConfig) -> tuple:
        values = [
            SheetService.normalize_value(row.get(header), value_type)
            for _, header, value_type in config.field_map
        ]
        values.append(SheetService.make_row_hash(row, config))
        return tuple(values)

    @staticmethod
    def parse_stt(value) -> int:
        stt_value = str(value or "").strip()
        if not stt_value:
            raise ValueError("STT is empty")

        try:
            return int(stt_value)
        except ValueError as exc:
            raise ValueError(f"Invalid STT value: {stt_value}") from exc

    @staticmethod
    def parse_optional_int(value) -> int | None:
        int_value = str(value or "").strip()
        if not int_value:
            return None

        try:
            return int(float(int_value))
        except ValueError:
            return None

    @staticmethod
    def normalize_value(value, value_type: str):
        # Each sheet value is normalized before it is sent to MySQL.
        if value_type == "stt":
            return SheetService.parse_stt(value)
        if value_type == "int":
            return SheetService.parse_optional_int(value)
        if value_type == "date":
            return SheetValidator.validate_date(value)
        return SheetValidator.empty_to_none(value)

    @staticmethod
    def make_row_hash(row: dict, config: SheetConfig) -> str:
        row_str = "|".join(
            str(row.get(header, "")).strip().upper()
            for header in config.headers
        )
        return hashlib.sha256(row_str.encode("utf-8")).hexdigest()

    @staticmethod
    def sync_data(sheet_name: str, header_row: int, config: SheetConfig ) -> int:
        worksheet = SheetService.connect_worksheet(sheet_name)
        rows = SheetService.read_records(
            worksheet,
            header_row,
            config.headers,
            required_headers=config.required_headers,
        )
        batch = SheetService.build_batch(rows, config)
        
        with Database() as db:
            db.upsert_many(config.upsert_sql, batch)
            
        print(f"Synced {len(batch)} rows to {config.table_name}!")
        return len(batch)
    
    @staticmethod
    def sync_vehicle_data(sheet_name: str, header_row: int) -> int:
        return SheetService.sync_data(
            sheet_name,
            header_row,
            SheetService.VEHICLE_CONFIG,
        )
        
    @staticmethod
    def sync_trailer_data(sheet_name: str, header_row: int) -> int:
        return SheetService.sync_data(
            sheet_name,
            header_row,
            SheetService.TRAILER_CONFIG,
        )
        
    @staticmethod
    def sync_inspection_data(sheet_name: str, header_row: int) -> int:
        return SheetService.sync_data(
            sheet_name,
            header_row,
            SheetService.INSPECTION_CONFIG,
        )

    @staticmethod
    def sync_ghep_data(sheet_name: str, header_row: int) -> int:
        return SheetService.sync_data(
            sheet_name,
            header_row,
            SheetService.GHEP_CONFIG,
        )
        
    @staticmethod
    def sync_thay_dau_data(sheet_name: str, header_row: int) -> int:
        return SheetService.sync_data(
            sheet_name,
            header_row,
            SheetService.THAY_DAU_CONFIG,
        )
        
    @staticmethod
    def sync_lsu_bdsc_data(sheet_name: str, header_row: int) -> int:
        return SheetService.sync_data(
            sheet_name,
            header_row,
            SheetService.LICH_SU_BDSC_CONFIG,
        )
        
    @staticmethod
    def sync_ke_hoach_data(sheet_name: str, header_row: int) -> int:
        return SheetService.sync_data(
            sheet_name,
            header_row,
            SheetService.KE_HOACH_CONFIG,
        )