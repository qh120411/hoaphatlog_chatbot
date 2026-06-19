from typing import Any
from database.db_connect import Database


class VehicleDataService:
    @staticmethod
    
    # Thông tin chung về 1 xe
    def search_vehicle( plate_number: str | None = None, plate: str | None = None, fields: list[str] | str | None = None, ) -> dict[str, Any]:
        plate_value = plate_number or plate or ""
        try:
            with Database(dictionary=True) as db:
                sql = """
                    SELECT
                        stt,
                        bks,
                        bks_moi,
                        loai_xe_chung_loai,
                        loai_xe,
                        don_vi_quan_ly,
                        nam_sx,
                        so_may,
                        so_khung,
                        so_dang_kiem,
                        ngay_het_han_dang_kiem,
                        so_dang_ky,
                        dang_ky_goc,
                        han_gia_han_giay_ngan_hang,
                        cong_ty_or_ngan_hang,
                        han_bao_hiem,
                        cong_ty_bao_hiem,
                        han_bao_hiem_vc,
                        cong_ty_bao_hiem_vc,
                        han_phu_hieu,
                        thiet_bi_gsht,
                        ngay_het_han_camera,
                        camera_giam_sat,
                        tinh_trang,
                        mau,
                        kich_thuoc_thung_xe,
                        tai_trong_ban_than,
                        khoi_luong_cho_phep_tren_mam_keo_tggt,
                        khoi_luong_hang_cc_theo_tk_cp_tggt,
                        khoi_luong_toan_bo_theo_tk_cp_tggt
                    FROM thong_tin_xe
                    WHERE bks = %s OR bks_moi = %s
                    LIMIT 1
                """
                db.cursor.execute(sql, (plate_value, plate_value))
                row = db.cursor.fetchone()

            if not row:
                return {
                    "found": False,
                    "message": f"No vehicle found with plate {plate_value}",
                }

            selected_fields = VehicleDataService.normalize_fields(fields, row)
            vehicle = (
                {
                    field: row.get(field) for field in selected_fields
                    }
                if selected_fields
                else row
            )

            return {
                "found": True,
                "vehicle": vehicle,
            }
            
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }

    #Lấy ra các xe có hạn đăng kiểm trong khoảng thời gian nhất định (mặc định 7 ngày)
    @staticmethod
    def get_inspection_due(days: int = 7) -> list[dict[str, Any]] | dict[str, Any]:
        try:
            days = min(max(1, int(days)), 365) 
            with Database(dictionary=True) as db:
                sql = """
                    SELECT
                        bks,
                        bks_moi,
                        loai_xe_chung_loai,
                        ngay_het_han_dang_kiem,
                        DATEDIFF(ngay_het_han_dang_kiem, CURDATE()) as songay_con_lai,
                        count(*) OVER() as so_luong
                    FROM thong_tin_xe
                    WHERE ngay_het_han_dang_kiem >= CURDATE()
                        AND ngay_het_han_dang_kiem <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
                    ORDER BY ngay_het_han_dang_kiem ASC
                """
                db.cursor.execute(sql, (days,))
                rows = db.cursor.fetchall()

            return rows
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }

    #Lấy ra các xe đã hết hạn đăng kiểm
    @staticmethod
    def get_inspection_expired() -> list[dict[str, Any]] | dict[str, Any]:
        try:
            with Database(dictionary=True) as db:
                sql = """
                    SELECT
                        stt,
                        bks,
                        bks_moi,
                        ngay_het_han_dang_kiem,
                    FROM thong_tin_xe
                    WHERE ngay_het_han_dang_kiem < CURDATE()
                    ORDER BY ngay_het_han_dang_kiem ASC
                """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()

            return rows
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }

    #Lấy thông tin đăng kiểm của 1 xe dựa trên biển số xe.
    @staticmethod
    def get_vehicle_inspection( plate_number: str | None = None, plate: str | None = None, ) -> dict[str, Any]:
        plate_value = plate_number or plate or ""

        try:
            with Database(dictionary=True) as db:
                sql = """
                    SELECT
                        stt,
                        bks,
                        bks_moi,
                        loai_xe_chung_loai,
                        so_dang_kiem,
                        ngay_het_han_dang_kiem
                        DATEDIFF(ngay_het_han_dang_kiem, CURDATE()) as songay_con_lai
                    FROM thong_tin_xe
                    WHERE bks = %s OR bks_moi = %s
                """
                db.cursor.execute(sql, (plate_value, plate_value))
                rows = db.cursor.fetchone()

            if not rows:
                return {
                    "found": False,
                    "message": f"No vehicle inspection found with plate {plate_value}",
                }

            return {
                "found": True,
                "vehicle": rows,
            }
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }

    #
    @staticmethod
    #đưa ra các xe thuộc đơn vị quản lý nào đó
    def get_vehicles_by_unit(unit_name: str) -> list[dict[str, Any]] | dict[str, Any]:
        try:
            with Database(dictionary=True) as db:
                sql = """
                    SELECT
                        bks,
                        bks_moi,
                        loai_xe_chung_loai,
                        don_vi_quan_ly
                        
                    FROM thong_tin_xe
                    WHERE don_vi_quan_ly = %s
                """
                db.cursor.execute(sql, (unit_name,))
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": f"No vehicles found for unit {unit_name}",
                }
            return rows
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
            
    @staticmethod
    #Đưa ra các xe cùng hạn đăng kiểm gần nhất
    def get_nearest_inspection_due() -> list[dict[str, Any]] | dict[str, Any]:
        try:
            with Database(dictionary = True ) as db:
                sql = """
                    SELECT
                        bks,
                        bks_moi,
                        so_dang_kiem,
                        ngay_het_han_dang_kiem,
                        DATEDIFF(ngay_het_han_dang_kiem, CURDATE()) as songay_con_lai
                    FROM thong_tin_xe
                    WHERE ngay_het_han_dang_kiem = (
                        SELECT MIN(ngay_het_han_dang_kiem)
                        FROM thong_tin_xe
                        WHERE ngay_het_han_dang_kiem >= CURDATE()
                    )
                    ORDER BY bks ASC;
                """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()
            return rows
        
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
    
    @staticmethod
    #Đơn vị nào có nhiều xe sắp đăng kiểm nhất trong ... ngày tới/ tháng sau?
    def get_inspection_due_top_unit(days: int = 7 ) -> list[dict[str, Any]] | dict[str, Any]:
        try:
            day = min(max(1, int(day)), 365)
            with Database(dictionary=True) as db:
                sql = """
                    WITH top_unit AS (
                        SELECT
                            don_vi_quan_ly,
                            COUNT(*) AS tong_so_xe
                        FROM thong_tin_xe
                        WHERE ngay_het_han_dang_kiem >= CURDATE()
                            AND ngay_het_han_dang_kiem <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
                            AND don_vi_quan_ly IS NOT NULL
                            AND don_vi_quan_ly <> ''
                        GROUP BY don_vi_quan_ly
                        ORDER BY tong_so_xe DESC, don_vi_quan_ly ASC
                        LIMIT 1
                    )
                        SELECT
                            top_unit.don_vi_quan_ly,
                            top_unit.tong_so_xe,
                            xe.bks,
                            xe.bks_moi,
                            xe.loai_xe_chung_loai,
                            xe.ngay_het_han_dang_kiem
                        FROM top_unit
                        JOIN thong_tin_xe AS xe ON xe.don_vi_quan_ly = top_unit.don_vi_quan_ly
                    WHERE xe.ngay_het_han_dang_kiem >= CURDATE()
                        AND xe.ngay_het_han_dang_kiem <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
                    ORDER BY xe.ngay_het_han_dang_kiem ASC, xe.bks ASC;
                """
                db.cursor.execute(sql, (day, day))
                rows = db.cursor.fetchall()
            return rows
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
            
    @staticmethod
    #Lấy ra các xe có hạn bảo hiểm trong thời gian nhất định (mặc định 7 ngày)
    def get_insurance_due(days: int = 7) -> list[dict[str, Any]] | dict[str, Any]:
        try:
            days = min(max(1, int(days)), 365) 
            with Database(dictionary=True) as db:
                sql = """
                    SELECT
                        bks,
                        bks_moi,
                        loai_xe_chung_loai,
                        han_bao_hiem,
                        cong_ty_bao_hiem,
                        DATEDIFF(han_bao_hiem, CURDATE()) AS so_ngay_con_lai
                    FROM thong_tin_xe
                    WHERE han_bao_hiem >= CURDATE()
                        AND han_bao_hiem <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
                    ORDER BY han_bao_hiem ASC
                """
                db.cursor.execute(sql, (days,))
                rows = db.cursor.fetchall()

            return rows
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
    
    @staticmethod
    #Lấy ra các xe cùng hết hạn bảo hiểm gần nhất
    def get_nearest_insurance_due() -> list[dict[str, Any]] | dict[str, Any]:
        try:
            with Database(dictionary=True) as db:
                sql = """
                    SELECT
                        bks,
                        bks_moi,
                        loai_xe_chung_loai,
                        han_bao_hiem,
                        cong_ty_bao_hiem,
                        DATEDIFF(han_bao_hiem, CURDATE()) AS so_ngay_con_lai
                    FROM thong_tin_xe
                    WHERE han_bao_hiem = (
                        SELECT MIN(han_bao_hiem)
                        FROM thong_tin_xe
                        WHERE han_bao_hiem >= CURDATE()
                    )
                    ORDER BY bks ASC;
                """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()
            return rows
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
            
    @staticmethod
    #Đơn vị nào có nhiều xe sắp hết hạn bảo hiểm nhất trong ... ngày tới/ tháng sau?
    def get_insurance_due_top_unit(day: int = 7) -> list[dict[str, Any]] | dict[str, Any]:
        try:
            day = min(max(1, int(day)), 365)
            with Database(dictionary=True) as db:
                sql = """
                    WITH top_unit AS (
                        SELECT
                            don_vi_quan_ly,
                            COUNT(*) AS tong_so_xe
                        FROM thong_tin_xe
                        WHERE han_bao_hiem >= CURDATE()
                            AND han_bao_hiem <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
                            AND don_vi_quan_ly IS NOT NULL
                            AND don_vi_quan_ly <> ''
                        GROUP BY don_vi_quan_ly
                        ORDER BY tong_so_xe DESC, don_vi_quan_ly ASC
                        LIMIT 1
                    )
                    SELECT
                        top_unit.don_vi_quan_ly,
                        top_unit.tong_so_xe,
                        xe.bks,
                        xe.bks_moi,
                        xe.loai_xe_chung_loai,
                        xe.han_bao_hiem,
                        xe.cong_ty_bao_hiem
                    FROM top_unit
                    JOIN thong_tin_xe AS xe ON xe.don_vi_quan_ly = top_unit.don_vi_quan_ly
                    WHERE xe.han_bao_hiem >= CURDATE()
                        AND xe.han_bao_hiem <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
                    ORDER BY xe.han_bao_hiem ASC, xe.bks ASC;
                """
                db.cursor.execute(sql, (day, day))
                rows = db.cursor.fetchall()
            return rows
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
    @staticmethod
    #Lấy ngày gia hạn ngân hàng của 1 xe dựa trên biển số xe.        
    def get_vehicle_bank_extension(plate_number: str | None = None, plate: str | None = None) -> dict[str, Any]:
        plate_value = plate_number or plate or ""
        try:
            with Database(dictionary=True) as db:
                sql = """
                    SELECT
                        bks,
                        bks_moi,
                        loai_xe_chung_loai,
                        han_gia_han_giay_ngan_hang,
                        cong_ty_or_ngan_hang
                    FROM thong_tin_xe
                    WHERE bks = %s OR bks_moi = %s
                """
                db.cursor.execute(sql, (plate_value, plate_value))
                rows = db.cursor.fetchone()

            if not rows:
                return {
                    "found": False,
                    "message": f"No vehicle bank extension found with plate {plate_value}",
                }

            return {
                "found": True,
                "vehicle": rows,
            }
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
            
    @staticmethod
    #Lấy ra các xe có hạn gia hạn gần nhất
    #khi sync lại data cần validate lại 
    def get_nearest_bank_extension_due() -> list[dict[str, Any]] | dict[str, Any]:
        try:
            with Database(dictionary=True) as db:
                sql = """
                    SELECT
                        bks,
                        bks_moi,
                        loai_xe_chung_loai,
                        han_gia_han_giay_ngan_hang,
                        cong_ty_or_ngan_hang,
                        DATEDIFF(han_gia_han_giay_ngan_hang, CURDATE()) AS so_ngay_con_lai
                    FROM thong_tin_xe
                    WHERE han_gia_han_giay_ngan_hang = (
                        SELECT MIN(han_gia_han_giay_ngan_hang)
                        FROM thong_tin_xe
                        WHERE han_gia_han_giay_ngan_hang >= CURDATE()
                    )
                    ORDER BY bks ASC;
                """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()
            return rows
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
            
    @staticmethod
    #Đưa ra các xe đang dùng bào hiểm của công ty ... nào đó?
    def get_vehicles_by_insurance_company(company_name: str) -> list[dict[str, Any]] | dict[str, Any]:
        try:
            with Database(dictionary=True) as db:
                sql = """
                    SELECT
                        bks,
                        bks_moi,
                        loai_xe_chung_loai,
                        han_bao_hiem,
                        cong_ty_bao_hiem
                        COUNT(*) OVER() AS so_luong
                    FROM thong_tin_xe
                    WHERE cong_ty_bao_hiem = %s
                """
                db.cursor.execute(sql, (company_name,))
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": f"No vehicles found for insurance company {company_name}",
                }
            return rows
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
    @staticmethod
    #Lấy ra các xe đang nằm bài hoặc không hoạt động
    def get_inactive_vehicles() -> list[dict[str, Any]] | dict[str, Any]:
        try:
            with Database(dictionary=True) as db:
                sql = """
                    SELECT
                        bks,
                        bks_moi,
                        loai_xe_chung_loai,
                        tinh_trang,
                        COUNT(*) OVER() AS so_luong
                    FROM thong_tin_xe
                    WHERE tinh_trang IS NULL
                        OR TRIM(tinh_trang) = ''
                        OR TRIM(tinh_trang) <> 'Xe đang hoạt động'
                    ORDER BY tinh_trang ASC, bks ASC;
                """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()

            return rows
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
            
    @staticmethod
    #Thống kê sl xe theo từng đv quản lý
    def get_vehicle_count_by_management_unit(units: list[str] | str | None = None) -> dict[str, Any]:
        try:
            if isinstance(units, str):
                units = [units]
                
            with Database(dictionary=True) as db:
                if not units:
                    sql = """
                        SELECT
                            don_vi_quan_ly,
                            COUNT(*) AS so_luong_xe
                        FROM thong_tin_xe
                        WHERE don_vi_quan_ly IS NOT NULL
                            AND TRIM(don_vi_quan_ly) <> ''
                        GROUP BY don_vi_quan_ly
                        ORDER BY so_luong_xe DESC, don_vi_quan_ly ASC;
                    """
                else:
                    placeholders = ', '.join(['%s'] * len(units))
                    sql = """
                        SELECT
                            don_vi_quan_ly,
                            COUNT(*) AS so_luong_xe
                        FROM thong_tin_xe
                        WHERE don_vi_quan_ly IN ({placeholders})
                        GROUP BY don_vi_quan_ly
                        ORDER BY so_luong_xe DESC, don_vi_quan_ly ASC;
                    """
                    db.cursor.execute(sql, tuple(units))
                rows = db.cursor.fetchall()
            return rows
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
            
    @staticmethod
    #Lấy ra có bao nhiêu xe đang vay ngân hàng ... nào đó
    def get_vehicles_by_bank(bank_name: str) -> list[dict[str, Any]] | dict[str, Any]:
        try:
            with Database(dictionary = True ) as db:
                sql = """
                    SELECT
                        bks,
                        bks_moi,
                        loai_xe_chung_loai,
                        COUNT(*) OVER() AS so_luong
                    FROM thong_tin_xe
                    WHERE cong_ty_or_ngan_hang = %s
                    """
                db.cursor.execute(sql, (bank_name,))
                rows = db.cursor.fetchall()
            if not rows:
                return {
                    "found": False,
                    "message": f"No vehicles found for bank {bank_name}",
                }
            return rows
        except Exception as exc:            
            return {
                "found": False,
                "error": str(exc),
            }
                
    MISSING_GROUPS = {
        "bks": ["bks", "bks_moi"],
        "dang_kiem": ["so_dang_kiem", "ngay_het_han_dang_kiem"],
        "bao_hiem": ["han_bao_hiem", "cong_ty_bao_hiem"],
        "bao_hiem_vc": ["han_bao_hiem_vc", "cong_ty_bao_hiem_vc"],
        "ngan_hang": ["han_gia_han_giay_ngan_hang", "cong_ty_or_ngan_hang"],
        "phu_hieu": ["han_phu_hieu"],
        "camera": ["ngay_het_han_camera", "camera_giam_sat"],
    }

    DUE_FIELDS = {
        "dang_kiem": ("ngay_het_han_dang_kiem", "so_dang_kiem"),
        "bao_hiem": ("han_bao_hiem", "cong_ty_bao_hiem"),
        "bao_hiem_vc": ("han_bao_hiem_vc", "cong_ty_bao_hiem_vc"),
        "ngan_hang": ("han_gia_han_giay_ngan_hang", "cong_ty_or_ngan_hang"),
        "phu_hieu": ("han_phu_hieu", "''"),
        "camera": ("ngay_het_han_camera", "camera_giam_sat"),
    }

    @staticmethod
    def _fetch(sql: str, params: tuple = ()) -> list[dict[str, Any]] | dict[str, Any]:
        try:
            with Database(dictionary=True) as db:
                db.cursor.execute(sql, params)
                return db.cursor.fetchall()
        except Exception as exc:
            return {"found": False, "error": str(exc)}

    @staticmethod
    # Xe nao chua co thong tin cua bks, dang kiem, bao hiem, ngan hang...
    def get_missing_vehicle_info(info_type: str = "all") -> list[dict[str, Any]] | dict[str, Any]:
        all_cols = sorted({c for cols in VehicleDataService.MISSING_GROUPS.values() for c in cols})
        cols = all_cols if info_type == "all" else VehicleDataService.MISSING_GROUPS.get(info_type, [info_type])
        cols = [c for c in cols if c in all_cols]

        if not cols:
            return {"found": False, "message": "Thong tin can kiem tra khong hop le"}

        union_sql = " UNION ALL ".join(
            f"""
            SELECT bks, bks_moi, loai_xe_chung_loai, don_vi_quan_ly, '{col}' AS cot_trong
            FROM thong_tin_xe
            WHERE {col} IS NULL OR TRIM(CAST({col} AS CHAR)) = ''
            """
            for col in cols
        )

        sql = f"""
            SELECT
                bks,
                bks_moi,
                loai_xe_chung_loai,
                don_vi_quan_ly,
                cot_trong,
                COUNT(*) OVER(PARTITION BY cot_trong) AS so_luong
            FROM ({union_sql}) AS t
            ORDER BY cot_trong ASC, bks ASC
        """
        return VehicleDataService._fetch(sql)

    @staticmethod
    # Dem va lay xe theo tuoi xe hoac nam san xuat
    def get_vehicles_by_age_or_year(
        value: int,
        filter_type: str = "tuoi_xe",
        comparison: str = "tren",
    ) -> list[dict[str, Any]] | dict[str, Any]:
        operators = {
            "tren": ">",
            "duoi": "<",
            "duoc": "=",
            "bang": "=",
            "truoc": "<",
            "sau": ">",
            "vao": "=",
        }
        operator = operators.get(comparison, "=")
        compare_expr = "YEAR(CURDATE()) - nam_sx" if filter_type == "tuoi_xe" else "nam_sx"

        sql = f"""
            SELECT
                bks,
                bks_moi,
                loai_xe_chung_loai,
                loai_xe,
                don_vi_quan_ly,
                nam_sx,
                YEAR(CURDATE()) - nam_sx AS tuoi_xe,
                COUNT(*) OVER() AS so_luong
            FROM thong_tin_xe
            WHERE nam_sx IS NOT NULL
              AND {compare_expr} {operator} %s
            ORDER BY nam_sx ASC, bks ASC
        """
        return VehicleDataService._fetch(sql, (int(value),))

    @staticmethod
    # Xe co dang kiem, bao hiem, ngan hang, phu hieu... sap het han trong N ngay toi
    def get_vehicle_due_items(document_type: str = "all", days: int = 30) -> list[dict[str, Any]] | dict[str, Any]:
        keys = list(VehicleDataService.DUE_FIELDS) if document_type == "all" else [document_type]
        keys = [k for k in keys if k in VehicleDataService.DUE_FIELDS]

        if not keys:
            return {"found": False, "message": "Loai han can kiem tra khong hop le"}

        union_sql = " UNION ALL ".join(
            f"""
            SELECT
                bks,
                bks_moi,
                loai_xe_chung_loai,
                '{key}' AS loai_han,
                {info_col} AS thong_tin_lien_quan,
                {date_col} AS ngay_den_han,
                DATEDIFF({date_col}, CURDATE()) AS so_ngay_con_lai
            FROM thong_tin_xe
            WHERE {date_col} >= CURDATE()
              AND {date_col} <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
            """
            for key, (date_col, info_col) in VehicleDataService.DUE_FIELDS.items()
            if key in keys
        )

        sql = f"""
            SELECT
                bks,
                bks_moi,
                loai_xe_chung_loai,
                loai_han,
                thong_tin_lien_quan,
                ngay_den_han,
                so_ngay_con_lai,
                COUNT(*) OVER(PARTITION BY loai_han) AS so_luong
            FROM ({union_sql}) AS t
            ORDER BY ngay_den_han ASC, bks ASC
        """
        days = min(max(1, int(days)), 365)
        return VehicleDataService._fetch(sql, tuple([days] * len(keys)))
            
    @staticmethod
    def normalize_fields(fields: list[str] | str | None, row: dict[str, Any]) -> list[str]:
        if not fields:
            return []

        requested_fields = [fields] if isinstance(fields, str) else fields
        if not isinstance(requested_fields, list):
            return []

        return [
            field
            for field in requested_fields
            if isinstance(field, str) and field in row
        ]
