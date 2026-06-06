from typing import Any
from database.db_connect import Database


class VehicleDataService:
    @staticmethod
    def search_by_plate(plate: str) -> dict[str, Any]:
        try:
            with Database() as db:
                sql = """
                    SELECT *
                    FROM thong_tin_xe
                    WHERE bks = %s OR bks_moi = %s
                """
                db.cursor.execute(sql, (plate, plate))
                row = db.cursor.fetchone()

            if not row:
                return {
                    "found": False,
                    "message": f"No vehicle found with plate {plate}",
                }

            return {
                "found": True,
                "vehicle": VehicleDataService.format_vehicle_detail(row),
            }
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }

    @staticmethod
    def get_inspection_due(days: int = 30) -> list[dict[str, Any]] | dict[str, Any]:
        try:
            days = int(days)
            with Database() as db:
                sql = """
                    SELECT
                        stt,
                        bks,
                        bks_moi,
                        loai_xe_chung_loai,
                        loai_xe,
                        don_vi_quan_ly,
                        ngay_het_han_dang_kiem,
                    FROM thong_tin_xe
                    WHERE ngay_het_han_dang_kiem >= CURDATE()
                        AND ngay_het_han_dang_kiem <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
                    ORDER BY ngay_het_han_dang_kiem ASC
                """
                db.cursor.execute(sql, (days,))
                rows = db.cursor.fetchall()

            return [
                VehicleDataService.format_vehicle_summary(row)
                for row in rows
            ]
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }

    @staticmethod
    def get_expired() -> list[dict[str, Any]] | dict[str, Any]:
        try:
            with Database() as db:
                sql = """
                    SELECT
                        stt,
                        bks,
                        bks_moi,
                        loai_xe_chung_loai,
                        loai_xe,
                        don_vi_quan_ly,
                        ngay_het_han_dang_kiem,
                    FROM thong_tin_xe
                    WHERE ngay_het_han_dang_kiem < CURDATE()
                    ORDER BY ngay_het_han_dang_kiem ASC
                """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()

            return [
                VehicleDataService.format_vehicle_summary(row)
                for row in rows
            ]
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }

    @staticmethod
    def get_vehicle_inspection(plate: str) -> dict[str, Any]:
        try:
            with Database() as db:
                sql = """
                SELECT bks, bks_moi, loai_xe_chung_loai, so_dang_kiem, ngay_het_han_dang_kiem
                FROM thong_tin_xe
                WHERE bks = %s OR bks_moi = %s
                """
                db.cursor.execute(sql, (plate, plate))
                rows = db.cursor.fetchone()
            return [
                VehicleDataService.format_vehicle_summary(row)
                for row in rows
            ]
        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
                
    
    @staticmethod
    def format_vehicle_detail(row: tuple) -> dict[str, Any]:
        # Keep this order the same as the SELECT columns in search_by_plate().
        return {
            "stt": row[0],
            "bks": row[1],
            "bks_moi": row[2],
            "loai_xe_chung_loai": row[3],
            "loai_xe": row[4],
            "don_vi_quan_ly": row[5],
            "nam_sx": row[6],
            "so_may": row[7],
            "so_khung": row[8],
            "so_dang_kiem": row[9],
            "ngay_het_han_dang_kiem": VehicleDataService.date_to_str(row[10]),
            "so_dang_ky": row[11],
            "dang_ky_goc": row[12],
            "han_gia_han_giay_ngan_hang": VehicleDataService.date_to_str(row[13]),
            "cong_ty_or_ngan_hang": row[14],
            "han_bao_hiem": VehicleDataService.date_to_str(row[15]),
            "cong_ty_bao_hiem": row[16],
            "han_bao_hiem_vc": VehicleDataService.date_to_str(row[17]),
            "cong_ty_bao_hiem_vc": row[18],
            "han_phu_hieu": VehicleDataService.date_to_str(row[19]),
            "thiet_bi_gsht": row[20],
            "ngay_het_han_camera": VehicleDataService.date_to_str(row[21]),
            "camera_giam_sat": row[22],
            "tinh_trang": row[23],
            "mau": row[24],
            "kich_thuoc_thung_xe": row[25],
            "tai_trong_ban_than": row[26],
            "khoi_luong_cho_phep_tren_mam_keo_tggt": row[27],
            "khoi_luong_hang_cc_theo_tk_cp_tggt": row[28],
            "khoi_luong_toan_bo_theo_tk_cp_tggt": row[29],
        }

    @staticmethod
    def format_vehicle_summary(row: tuple) -> dict[str, Any]:
        # Keep this order the same as the SELECT columns in list queries.
        return {
            "stt": row[0],
            "bks": row[1],
            "bks_moi": row[2],
            "loai_xe_chung_loai": row[3],
            "loai_xe": row[4],
            "don_vi_quan_ly": row[5],
            "ngay_het_han_dang_kiem": VehicleDataService.date_to_str(row[6]),
            "tinh_trang": row[7],
        }

    @staticmethod
    def date_to_str(value) -> str | None:
        if value is None:
            return None
        return str(value)
