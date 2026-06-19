from typing import Any
from database.db_connect import Database


class BdscDataService:
    GIA_TRI_CON_LAI_NUM = """
        COALESCE(
            NULLIF(
                REPLACE(REPLACE(REPLACE(TRIM(gia_tri_con_lai), '.', ''), ',', ''), ' ', ''),
                ''
            ) + 0,
            0
        )
    """

    @staticmethod
    def _normalize_list(values: list[str] | str | None) -> list[str]:
        if isinstance(values, str):
            values = [values]

        if values:
            values = [x.strip() for x in values if x and x.strip()]

        return values or []

    @staticmethod
    def _date_condition(column: str, period: str = "thang_nay", from_date: str | None = None, to_date: str | None = None) -> tuple[str, tuple]:
        if from_date and to_date:
            return f"{column} BETWEEN %s AND %s", (from_date, to_date)

        if period == "tuan_nay":
            return f"YEARWEEK({column}, 1) = YEARWEEK(CURDATE(), 1)", ()

        if period == "thang_nay":
            return f"MONTH({column}) = MONTH(CURDATE()) AND YEAR({column}) = YEAR(CURDATE())", ()

        if period == "thang_truoc":
            return f"{column} >= DATE_FORMAT(CURDATE() - INTERVAL 1 MONTH, '%Y-%m-01') AND {column} <= LAST_DAY(CURDATE() - INTERVAL 1 MONTH)", ()

        if period == "quy_nay":
            return f"QUARTER({column}) = QUARTER(CURDATE()) AND YEAR({column}) = YEAR(CURDATE())", ()

        if period == "nam_nay":
            return f"YEAR({column}) = YEAR(CURDATE())", ()

        raise ValueError("Invalid period. Use tuan_nay, thang_nay, thang_truoc, quy_nay, nam_nay.")

    @staticmethod
    # Xe trong khoang thoi gian nhat dinh da sua chua nhung gi
    def get_vehicle_repair_items(
        bks: list[str] | str | None = None,
        period: str = "thang_nay",
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> dict[str, Any]:
        try:
            bks = BdscDataService._normalize_list(bks)

            if not bks:
                return {
                    "found": False,
                    "error": "Chua truyen bien so xe",
                }

            date_condition, date_params = BdscDataService._date_condition("ngay_phat_sinh", period, from_date, to_date)
            placeholders = ", ".join(["%s"] * len(bks))

            sql = f"""
            SELECT
                bks_xe_cu,
                bks_xe_moi,
                gara,
                ngay_phat_sinh,
                noi_dung,
                gia_tri_mua_da_vat,
                COUNT(*) OVER() AS so_luong
            FROM lsu_bdsc
            WHERE {date_condition}
              AND (bks_xe_cu IN ({placeholders}) OR bks_xe_moi IN ({placeholders}))
            ORDER BY ngay_phat_sinh ASC, stt ASC
            """

            params = date_params + tuple(bks) + tuple(bks)

            with Database(dictionary=True) as db:
                db.cursor.execute(sql, params)
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": "Khong tim thay noi dung sua chua cua xe trong khoang thoi gian nay",
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
    # Tong tien sua xe trong khoang thoi gian nhat dinh
    def get_total_repair_cost_by_vehicle(
        bks: list[str] | str | None = None,
        period: str = "thang_nay",
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> dict[str, Any]:
        try:
            bks = BdscDataService._normalize_list(bks)

            if not bks:
                return {
                    "found": False,
                    "error": "Chua truyen bien so xe",
                }

            date_condition, date_params = BdscDataService._date_condition("ngay_phat_sinh", period, from_date, to_date)
            placeholders = ", ".join(["%s"] * len(bks))

            sql = f"""
            SELECT
                bks_xe_cu,
                bks_xe_moi,
                SUM(COALESCE(gia_tri_mua_da_vat, 0)) AS tong_tien,
                COUNT(*) AS so_luong_muc_sua
            FROM lsu_bdsc
            WHERE {date_condition}
              AND (bks_xe_cu IN ({placeholders}) OR bks_xe_moi IN ({placeholders}))
            GROUP BY bks_xe_cu, bks_xe_moi
            ORDER BY tong_tien DESC
            """

            params = date_params + tuple(bks) + tuple(bks)

            with Database(dictionary=True) as db:
                db.cursor.execute(sql, params)
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": "Khong tim thay chi phi sua xe trong khoang thoi gian nay",
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
    # Xe da khau hao xong nhung hang muc nao
    def get_fully_depreciated_items(bks: list[str] | str | None = None) -> dict[str, Any]:
        try:
            bks = BdscDataService._normalize_list(bks)

            if not bks:
                return {
                    "found": False,
                    "error": "Chua truyen bien so xe",
                }

            placeholders = ", ".join(["%s"] * len(bks))

            sql = f"""
            SELECT
                bks_xe_cu,
                bks_xe_moi,
                noi_dung,
                phan_loai_chi_phi,
                gia_tri_con_lai,
                COUNT(*) OVER() AS so_luong
            FROM lsu_bdsc
            WHERE (bks_xe_cu IN ({placeholders}) OR bks_xe_moi IN ({placeholders}))
              AND ({BdscDataService.GIA_TRI_CON_LAI_NUM}) = 0
            ORDER BY ngay_phat_sinh ASC, stt ASC
            """

            with Database(dictionary=True) as db:
                db.cursor.execute(sql, tuple(bks) + tuple(bks))
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": "Khong tim thay hang muc da khau hao xong",
                }

            return {
                "found": True,
                "items": rows,
            }

        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }

    @staticmethod
    # Xe con hang muc nao chua khau hao xong
    def get_not_fully_depreciated_items(bks: list[str] | str | None = None) -> dict[str, Any]:
        try:
            bks = BdscDataService._normalize_list(bks)

            if not bks:
                return {
                    "found": False,
                    "error": "Chua truyen bien so xe",
                }

            placeholders = ", ".join(["%s"] * len(bks))

            sql = f"""
            SELECT
                bks_xe_cu,
                bks_xe_moi,
                noi_dung,
                thoi_gian_con_lai,
                gia_tri_con_lai,
                COUNT(*) OVER() AS so_luong
            FROM lsu_bdsc
            WHERE (bks_xe_cu IN ({placeholders}) OR bks_xe_moi IN ({placeholders}))
              AND ({BdscDataService.GIA_TRI_CON_LAI_NUM}) > 0
            ORDER BY thoi_gian_con_lai ASC, ngay_phat_sinh ASC
            """

            with Database(dictionary=True) as db:
                db.cursor.execute(sql, tuple(bks) + tuple(bks))
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": "Khong tim thay hang muc chua khau hao xong",
                }

            return {
                "found": True,
                "items": rows,
            }

        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }

    @staticmethod
    # Xe co nhung muc nao thuoc ten phan loai chi phi chua khau hao xong
    def get_not_depreciated_items_by_cost_type(
        bks: list[str] | str | None = None,
        phan_loai: str | None = None,
    ) -> dict[str, Any]:
        try:
            bks = BdscDataService._normalize_list(bks)

            if not bks:
                return {
                    "found": False,
                    "error": "Chua truyen bien so xe",
                }

            if not phan_loai:
                return {
                    "found": False,
                    "error": "Chua truyen ten phan loai chi phi",
                }

            placeholders = ", ".join(["%s"] * len(bks))

            sql = f"""
            SELECT
                bks_xe_cu,
                bks_xe_moi,
                COUNT(*) OVER(PARTITION BY bks_xe_cu, bks_xe_moi) AS so_luong_hang_muc,
                noi_dung,
                gia_tri_mua_da_vat,
                gia_tri_con_lai,
                thoi_gian_con_lai
            FROM lsu_bdsc
            WHERE (bks_xe_cu IN ({placeholders}) OR bks_xe_moi IN ({placeholders}))
              AND phan_loai_chi_phi LIKE CONCAT('%%', %s, '%%')
              AND ({BdscDataService.GIA_TRI_CON_LAI_NUM}) > 0
            ORDER BY thoi_gian_con_lai ASC, ngay_phat_sinh ASC
            """

            params = tuple(bks) + tuple(bks) + (phan_loai,)

            with Database(dictionary=True) as db:
                db.cursor.execute(sql, params)
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": "Khong tim thay hang muc chua khau hao theo phan loai chi phi nay",
                }

            return {
                "found": True,
                "items": rows,
            }

        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }

    @staticmethod
    # Tong tien sua xe theo ten phan loai chi phi trong khoang thoi gian
    def get_total_cost_by_vehicle_and_cost_type(
        bks: list[str] | str | None = None,
        phan_loai: str | None = None,
        period: str = "thang_nay",
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> dict[str, Any]:
        try:
            bks = BdscDataService._normalize_list(bks)

            if not bks:
                return {
                    "found": False,
                    "error": "Chua truyen bien so xe",
                }

            if not phan_loai:
                return {
                    "found": False,
                    "error": "Chua truyen ten phan loai chi phi",
                }

            date_condition, date_params = BdscDataService._date_condition("ngay_phat_sinh", period, from_date, to_date)
            placeholders = ", ".join(["%s"] * len(bks))

            sql = f"""
            SELECT
                bks_xe_cu,
                bks_xe_moi,
                SUM(COALESCE(gia_tri_mua_da_vat, 0)) AS tong_tien,
                COUNT(*) AS so_luong_muc_sua
            FROM lsu_bdsc
            WHERE {date_condition}
              AND (bks_xe_cu IN ({placeholders}) OR bks_xe_moi IN ({placeholders}))
              AND phan_loai_chi_phi LIKE CONCAT('%%', %s, '%%')
            GROUP BY bks_xe_cu, bks_xe_moi
            ORDER BY tong_tien DESC
            """

            params = date_params + tuple(bks) + tuple(bks) + (phan_loai,)

            with Database(dictionary=True) as db:
                db.cursor.execute(sql, params)
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": "Khong tim thay tong tien theo phan loai chi phi nay",
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
    # Thoi gian khau hao con lai cua ten phan loai chi phi theo xe
    def get_remaining_depreciation_time(
        bks: list[str] | str | None = None,
        phan_loai: str | None = None,
    ) -> dict[str, Any]:
        try:
            bks = BdscDataService._normalize_list(bks)

            if not bks:
                return {
                    "found": False,
                    "error": "Chua truyen bien so xe",
                }

            if not phan_loai:
                return {
                    "found": False,
                    "error": "Chua truyen ten phan loai chi phi",
                }

            placeholders = ", ".join(["%s"] * len(bks))

            sql = f"""
            SELECT
                bks_xe_cu,
                bks_xe_moi,
                noi_dung,
                phan_loai_chi_phi,
                thoi_gian_phan_bo,
                thoi_gian_con_lai,
                gia_tri_con_lai,
                COUNT(*) OVER() AS so_luong
            FROM lsu_bdsc
            WHERE (bks_xe_cu IN ({placeholders}) OR bks_xe_moi IN ({placeholders}))
              AND phan_loai_chi_phi LIKE CONCAT('%%', %s, '%%')
              AND ({BdscDataService.GIA_TRI_CON_LAI_NUM}) > 0
            ORDER BY thoi_gian_con_lai ASC
            """

            params = tuple(bks) + tuple(bks) + (phan_loai,)

            with Database(dictionary=True) as db:
                db.cursor.execute(sql, params)
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": "Khong tim thay thoi gian khau hao con lai",
                }

            return {
                "found": True,
                "items": rows,
            }

        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }

    @staticmethod
    # Tong chi phi tra cho gara trong khoang thoi gian nhat dinh
    def get_total_cost_by_gara(
        gara: str | None = None,
        period: str = "thang_nay",
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> dict[str, Any]:
        try:
            if not gara:
                return {
                    "found": False,
                    "error": "Chua truyen ten gara",
                }

            date_condition, date_params = BdscDataService._date_condition("ngay_phat_sinh", period, from_date, to_date)

            sql = f"""
            SELECT
                gara,
                SUM(COALESCE(gia_tri_mua_da_vat, 0)) AS tong_chi_phi,
                COUNT(*) AS so_luong_muc_sua
            FROM lsu_bdsc
            WHERE {date_condition}
              AND gara LIKE CONCAT('%%', %s, '%%')
            GROUP BY gara
            ORDER BY tong_chi_phi DESC
            """

            with Database(dictionary=True) as db:
                db.cursor.execute(sql, date_params + (gara,))
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": "Khong tim thay chi phi theo gara trong khoang thoi gian nay",
                }

            return {
                "found": True,
                "garas": rows,
            }

        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }

    @staticmethod
    # Cong ty da sua nhung gi o gara trong khoang thoi gian nhat dinh
    def get_repair_items_by_gara(
        gara: str | None = None,
        period: str = "thang_nay",
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> dict[str, Any]:
        try:
            if not gara:
                return {
                    "found": False,
                    "error": "Chua truyen ten gara",
                }

            date_condition, date_params = BdscDataService._date_condition("ngay_phat_sinh", period, from_date, to_date)

            sql = f"""
            SELECT
                COUNT(*) OVER() AS so_luong_muc_sua,
                bks_xe_cu,
                bks_xe_moi,
                gara,
                noi_dung,
                ngay_phat_sinh,
                gia_tri_mua_da_vat
            FROM lsu_bdsc
            WHERE {date_condition}
              AND gara LIKE CONCAT('%%', %s, '%%')
            ORDER BY ngay_phat_sinh ASC, stt ASC
            """

            with Database(dictionary=True) as db:
                db.cursor.execute(sql, date_params + (gara,))
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": "Khong tim thay noi dung sua chua theo gara trong khoang thoi gian nay",
                }

            return {
                "found": True,
                "items": rows,
            }

        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }

    @staticmethod
    # Trong thang nay hoac thang sau xe nao co hang muc het khau hao
    def get_depreciation_ending_items(month_offset: int = 0) -> dict[str, Any]:
        if month_offset not in [0, 1]:
            raise ValueError("Invalid month_offset. Use 0 for thang nay or 1 for thang sau.")

        try:
            sql = """
            WITH data_month AS (
                SELECT
                    bks_xe_cu,
                    bks_xe_moi,
                    noi_dung,
                    phan_loai_chi_phi,
                    ngay_phat_sinh,
                    thoi_gian_phan_bo,
                    thoi_gian_con_lai,
                    gia_tri_con_lai,
                    CASE MONTH(CURDATE())
                        WHEN 1 THEN thang_1
                        WHEN 2 THEN thang_2
                        WHEN 3 THEN thang_3
                        WHEN 4 THEN thang_4
                        WHEN 5 THEN thang_5
                        WHEN 6 THEN thang_6
                        WHEN 7 THEN thang_7
                        WHEN 8 THEN thang_8
                        WHEN 9 THEN thang_9
                        WHEN 10 THEN thang_10
                        WHEN 11 THEN thang_11
                        WHEN 12 THEN thang_12
                    END AS gia_tri_thang_hien_tai
                FROM lsu_bdsc
            )
            SELECT
                bks_xe_cu,
                bks_xe_moi,
                noi_dung,
                phan_loai_chi_phi,
                ngay_phat_sinh,
                thoi_gian_phan_bo,
                thoi_gian_con_lai,
                gia_tri_con_lai,
                DATE_ADD(ngay_phat_sinh, INTERVAL COALESCE(thoi_gian_phan_bo, 0) MONTH) AS ngay_du_kien_het_khau_hao,
                COUNT(*) OVER() AS so_luong
            FROM data_month
            WHERE thoi_gian_con_lai = CASE
                WHEN gia_tri_thang_hien_tai IS NULL OR TRIM(gia_tri_thang_hien_tai) = '' THEN %s + 1
                ELSE %s
            END
            ORDER BY ngay_du_kien_het_khau_hao ASC, bks_xe_moi ASC
            """

            with Database(dictionary=True) as db:
                db.cursor.execute(sql, (month_offset, month_offset))
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": "Khong tim thay hang muc het khau hao",
                }

            return {
                "found": True,
                "items": rows,
            }

        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
