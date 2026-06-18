from typing import Any
from database.db_connect import Database

class TrailerDataService:
    @staticmethod
    #thông tin chung về rơ mooc
    def search_trailer( plate_number: str | None = None, plate: str | None = None, fields: list[str] | str | None = None, ) -> dict[str, Any]:
        plate_value = plate_number or plate or ""
        try:
            with Database() as db:
                sql = """
                    SELECT
                    bks_ro_mooc_cu,
                    bks_ro_mooc_moi,
                    loai_mooc,
                    don_vi_quan_ly,
                    nam_san_xuat,
                    so_khung,
                    so_dang_kiem,
                    ngay_het_han_dang_kiem,
                    so_dang_ky,
                    ngay_het_han,
                    ngay_het_han_giay_ngan_hang,
                    ngan_hang,
                    ngay_het_han_bao_hiem,
                    cong_ty_bao_hiem,
                    loai,
                    mau,
                    khoi_luong_ban_than,
                    khoi_luong_chuyen_cho,
                    hien_trang
                    FROM thong_tin_ro_mooc
                    WHERE bks_ro_mooc_cu = %s OR bks_ro_mooc_moi = %s
                    """
                
                db.cursor.execute(sql, (plate_value, plate_value))
                row = db.cursor.fetchone()
            if not row:
                return {
                    "found": False,
                    "message": f"Không tìm thấy thông tin rơ mooc với biển số: {plate_value}",
                }
            selected_fields = TrailerDataService.normalize_fields(fields, row)
            trailer = (
                {
                    field: row[field]
                    for field in selected_fields
                }
                if selected_fields else row
            )
            return {
                "found": True,
                "trailer": trailer,
            }
        except Exception as e:
            return {
                "found": False,
                "error": str(e),
            }
            
    @staticmethod
    #Lấy ra các rơ mooc có hạn nhất định ( min 7 ngày)
    def get_inspection_trailer(days: int = 7 ) -> list[dict[str, Any]] | dict[str, Any]:
        try:
            with Database() as db:
                sql = """
                    SELECT
                    bks_ro_mooc_cu,
                    bks_ro_mooc_moi,
                    loai,
                    so_dang_kiem,
                    ngay_het_han_dang_kiem
                    FROM thong_tin_ro_mooc
                    WHERE ngay_het_han_dang_kiem >= CURDATE() AND ngay_het_han_dang_kiem <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
                    ORDER BY ngay_het_han_dang_kiem ASC;
                """
                db.cursor.execute(sql, (days,))
                row = db.cursor.fetchall()
            return row
        except Exception as e:
            return {
                "error": str(e),
            }   
            
    @staticmethod
    #đưa ra đơn vị quản lý có số lượng rơ mooc hết hạn đăng kiểm trong khoảng thời gian nhất định (min 7 ngày)
    def get__trailer_inspection_due_top_unit(day: int = 7 ) -> list[dict[str, Any]] | dict[str, Any]:
        try:
            day = min(max(1, int(day)), 365)
            with Database(dictionary=True) as db:
                sql = """
                    WITH top_unit AS (
                        SELECT
                            don_vi_quan_ly,
                            COUNT(*) AS tong_so_xe
                        FROM thong_tin_ro_mooc
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
                            rm.bks_ro_mooc_cu,
                            rm.bks_ro_mooc_moi,
                            rm.loai_mooc,
                            rm.ngay_het_han_dang_kiem
                        FROM top_unit
                        JOIN thong_tin_ro_mooc AS rm ON rm.don_vi_quan_ly = top_unit.don_vi_quan_ly
                    WHERE rm.ngay_het_han_dang_kiem >= CURDATE()
                        AND rm.ngay_het_han_dang_kiem <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
                    ORDER BY rm.ngay_het_han_dang_kiem ASC, rm.bks_ro_mooc_cu ASC;
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
    def get_trailer_bank_extension(plate_number: str | None = None, plate: str | None = None) -> dict[str, Any]:
        plate_value = plate_number or plate or ""
        try:
            with Database(dictionary=True) as db:
                sql = """
                    SELECT
                        bks_ro_mooc_cu,
                        bks_ro_mooc_moi,
                        loai,
                        ngay_het_han_giay_ngan_hang,
                        ngan_hang
                    FROM thong_tin_ro_mooc
                    WHERE bks_ro_mooc_cu = %s OR bks_ro_mooc_moi = %s
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
    #Lấy ra có bao nhiêu mooc đang vay ngân hàng ... nào đó
    def get_trailer_by_bank(bank_name: str) -> list[dict[str, Any]] | dict[str, Any]:
        try:
            with Database(dictionary=True) as db:
                sql = """
                    SELECT
                        bks_ro_mooc_cu,
                        bks_ro_mooc_moi,
                        loai,
                        ngay_het_han_giay_ngan_hang,
                        ngan_hang,
                        Count(*) OVER() as tong
                    FROM thong_tin_ro_mooc
                    WHERE ngan_hang = %s
                """
                db.cursor.execute(sql, (bank_name,))
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": f"No vehicles found for bank {bank_name}",
                }

            return {
                "found": True,
                "vehicles": rows,
            }
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
    
    @staticmethod 
    #Lấy ra rơ mooc đang dùng bảo hiểm công ty nào
    def get_trailer_by_insurance_company(insurance_company: str) -> list[dict[str, Any]] | dict[str, Any]:
        try:
            with Database(dictionary=True) as db:
                sql = """
                    SELECT
                        bks_ro_mooc_cu,
                        bks_ro_mooc_moi,
                        loai,
                        ngay_het_han_bao_hiem,
                        cong_ty_bao_hiem,
                        Count(*) OVER() as tong
                    FROM thong_tin_ro_mooc
                    WHERE cong_ty_bao_hiem = %s
                """
                db.cursor.execute(sql, (insurance_company,))
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": f"No vehicles found for insurance company {insurance_company}",
                }

            return {
                "found": True,
                "vehicles": rows,
            }
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
            
    @staticmethod
    #Thống kê sl rơ mooc theo từng đv quản lý
    def get_trailer_count_by_management_unit(units: list[str] | str | None = None) -> dict[str, Any]:
        try:
            if isinstance(units, str):
                units = [units]
                
            if units:
                units = [u.strip() for u in units if u and u.strip()]
                
            with Database(dictionary=True) as db:
                if not units:
                    sql = """
                        WITH RECURSIVE tmp AS (
                            SELECT
                                t.bks_ro_mooc_cu,
                            TRIM(SUBSTRING_INDEX(t.don_vi_quan_ly, '-', 1)) AS don_vi,
                        CASE
                            WHEN LOCATE('-', t.don_vi_quan_ly) > 0
                            THEN SUBSTRING(t.don_vi_quan_ly, LOCATE('-', t.don_vi_quan_ly) + 1)
                            ELSE ''
                        END AS phan_con_lai
                    FROM thong_tin_ro_mooc t
                    WHERE t.don_vi_quan_ly IS NOT NULL
                      AND TRIM(t.don_vi_quan_ly) <> ''

                    UNION ALL

                    SELECT
                        bks_ro_mooc_cu,
                        TRIM(SUBSTRING_INDEX(phan_con_lai, '-', 1)) AS don_vi,
                        CASE
                            WHEN LOCATE('-', phan_con_lai) > 0
                            THEN SUBSTRING(phan_con_lai, LOCATE('-', phan_con_lai) + 1)
                            ELSE ''
                        END AS phan_con_lai
                    FROM tmp
                    WHERE phan_con_lai <> ''
                ),
                
                dedup AS (
                    SELECT DISTINCT
                        bks_ro_mooc_cu,
                        don_vi
                    FROM tmp
                    WHERE don_vi <> ''
                )
            """

            if not units:
                sql = sql + """
                    SELECT
                        don_vi AS don_vi_quan_ly,
                        COUNT(*) AS so_luong_xe
                    FROM dedup
                    GROUP BY don_vi
                    ORDER BY so_luong_xe DESC, don_vi ASC;
                """
                db.cursor.execute(sql)
            else:
                placeholders = ", ".join(["%s"] * len(units))

                sql = sql + f"""
                    SELECT
                        don_vi AS don_vi_quan_ly,
                        COUNT(*) AS so_luong_xe
                    FROM dedup
                    WHERE don_vi IN ({placeholders})
                    GROUP BY don_vi
                    ORDER BY so_luong_xe DESC, don_vi ASC;
                """
                db.cursor.execute(sql, tuple(units))

            rows = db.cursor.fetchall()

            return rows
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
   
    #Đưa ra số lượng rơ mooc của 1 đvql nào đó
    @staticmethod
    def get_trailer_by_managemein_unit(unit: str) -> list[dict[str, Any]] | dict[str, Any]:
        try:
            with Database(dictionary=True) as db:
                sql = """
                    WITH RECURSIVE tmp AS (
                        SELECT
                            t.bks_ro_mooc_moi,
                            t.bks_ro_mooc_cu,
                            t.loai,
                            TRIM(SUBSTRING_INDEX(t.don_vi_quan_ly, '-', 1)) AS don_vi,
                            CASE
                                WHEN LOCATE('-', t.don_vi_quan_ly) > 0
                                THEN SUBSTRING(t.don_vi_quan_ly, LOCATE('-', t.don_vi_quan_ly) + 1)
                                ELSE ''
                            END AS phan_con_lai
                        FROM thong_tin_ro_mooc t
                        WHERE t.don_vi_quan_ly IS NOT NULL
                            AND TRIM(t.don_vi_quan_ly) <> ''

                        UNION ALL

                        SELECT
                            bks_ro_mooc_moi,
                            bks_ro_mooc_cu,
                            loai,
                            TRIM(SUBSTRING_INDEX(phan_con_lai, '-', 1)) AS don_vi,
                            CASE
                                WHEN LOCATE('-', phan_con_lai) > 0
                                THEN SUBSTRING(phan_con_lai, LOCATE('-', phan_con_lai) + 1)
                                ELSE ''
                            END AS phan_con_lai
                        FROM tmp
                        WHERE phan_con_lai <> ''
                    ),
                    dedup AS (
                        SELECT DISTINCT
                        bks_ro_mooc_moi,
                        bks_ro_mooc_cu,
                        loai,
                        don_vi
                        FROM tmp
                        WHERE don_vi <> ''
                    )
                    SELECT
                    don_vi AS don_vi_quan_ly,
                    bks_ro_mooc_moi,
                    bks_ro_mooc_cu,
                    loai,
                    COUNT(*) OVER (PARTITION BY don_vi) AS tong_so_ro_mooc
                    FROM dedup
                    WHERE don_vi = %s
                    ORDER BY bks_ro_mooc_moi, bks_ro_mooc_cu;
                """
                db.cursor.execute(sql, (unit,))
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": f"No vehicles found for management unit {unit}",
                }

            return {
                "found": True,
                "vehicles": rows,
            }
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
            
    
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