from typing import Any
from database.db_connect import Database

class PlanInspecDataService:
    @staticmethod
    #lấy ra danh sách xe cần bảo dưỡng trong ... ngày tới
    def get_vehicle_due(days: int = 7) -> list[dict[str, Any]]:
        days = min(max(days, 1), 365)  
        try:
            with Database() as db:
                sql = """
                SELECT
                        bks,
                        chung_loai,
                        phan_loai_doi,
                        noi_dung_sua_chua,
                        ngay_du_kien_thuc_hien,
                        DATEDIFF(ngay_du_kien_thuc_hien, CURDATE()) as songay_con_lai,
                        count(*) OVER() as so_luong
                    FROM khbd_sc
                    WHERE ngay_du_kien_thuc_hien >= CURDATE()
                        AND ngay_du_kien_thuc_hien <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
                    ORDER BY ngay_du_kien_thuc_hien ASC
                """
                db.cursor.execute(sql, (days,))
                rows = db.cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error retrieving vehicle due data: {str(e)}")
            return []
        
    @staticmethod
    #Lấy ra danh sách các xe đã sửa chữa trong tuần này hoặc tháng này
    def get_recently_serviced(period: str = "tuan_nay") -> list[dict[str, Any]]:
        if period not in ["tuan_nay", "thang_nay"]:
            raise ValueError("Invalid period. Use 'week' or 'month'.")
        try:
            with Database() as db:
                if period == "week":
                    sql = """
                    SELECT
                        bks,
                        chung_loai,
                        phan_loai_doi,
                        noi_dung_sua_chua,
                        ngay_thuc_hien,
                        count(*) OVER() as so_luong
                    FROM khbd_sc
                    WHERE YEARWEEK(ngay_thuc_hien, 1) = YEARWEEK(CURDATE(), 1)
                    ORDER BY ngay_thuc_hien DESC
                    """
                else:  # month
                    sql = """
                    SELECT
                        bks,
                        chung_loai,
                        phan_loai_doi,
                        noi_dung_sua_chua,
                        ngay_thuc_hien,
                        count(*) OVER() as so_luong
                    FROM khbd_sc
                    WHERE MONTH(ngay_thuc_hien) = MONTH(CURDATE())
                      AND YEAR(ngay_thuc_hien) = YEAR(CURDATE())
                    ORDER BY ngay_thuc_hien DESC
                    """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error retrieving recently serviced data: {str(e)}")
            return []
        
    @staticmethod
    #Lấy ra các xe chưa sửa chữa trong tháng này hoặc tuần này
    def get_not_serviced(period: str = "tuan_nay") -> list[dict[str, Any]]:
        if period not in ["tuan_nay", "thang_nay"]:
            raise ValueError("Invalid period. Use 'week' or 'month'.")
        try:
            with Database() as db:
                if period == "tuần":
                    sql = """
                    SELECT
                        bks,
                        chung_loai,
                        phan_loai_doi,
                        noi_dung_sua_chua,
                        ngay_du_kien_thuc_hien,
                        count(*) OVER() as so_luong
                    FROM khbd_sc
                    WHERE YEARWEEK(ngay_du_kien_thuc_hien, 1) = YEARWEEK(CURDATE(), 1)
                      AND ngay_thuc_hien IS NULL
                    ORDER BY ngay_du_kien_thuc_hien ASC
                    """
                else:  # month
                    sql = """
                    SELECT
                        bks,
                        chung_loai,
                        phan_loai_doi,
                        noi_dung_sua_chua,
                        ngay_du_kien_thuc_hien,
                        count(*) OVER() as so_luong
                    FROM khbd_sc
                    WHERE MONTH(ngay_du_kien_thuc_hien) = MONTH(CURDATE())
                      AND YEAR(ngay_du_kien_thuc_hien) = YEAR(CURDATE())
                      AND ngay_thuc_hien IS NULL
                    ORDER BY ngay_du_kien_thuc_hien ASC
                    """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error retrieving not serviced data: {str(e)}")
            return []
        
    #Lấy ra các xe có chi phí thục tế nhỏ hơn hoặc lớn hơn thành tiền
    @staticmethod
    def get_cost_discrepancy(comparison: str = "nhỏ hơn") -> list[dict[str, Any]]:
        if comparison not in ["nhỏ hơn", "lớn hơn"]:
            raise ValueError("Invalid comparison. Use 'nhỏ hơn' or 'nhiều hơn'.")
        try:
            with Database() as db:
                if comparison == "nhỏ hơn":
                    sql = """
                    SELECT
                        bks,
                        chung_loai,
                        phan_loai_doi,
                        noi_dung_sua_chua,
                        thanh_tien,
                        chi_phi_thuc_te,
                        count(*) OVER() as so_luong
                    FROM khbd_sc
                    WHERE chi_phi_thuc_te < thanh_tien
                    ORDER BY ngay_thuc_hien DESC
                    """
                else:  # greater
                    sql = """
                    SELECT
                        bks,
                        chung_loai,
                        phan_loai_doi,
                        noi_dung_sua_chua,
                        thanh_tien,
                        chi_phi_thuc_te,
                        count(*) OVER() as so_luong
                    FROM khbd_sc
                    WHERE chi_phi_thuc_te > thanh_tien
                    ORDER BY ngay_thuc_hien DESC
                    """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error retrieving cost discrepancy data: {str(e)}")
            return []
        
    @staticmethod
    #Đội xe nào có chi phí thực hiện lớn nhất
    def get_team_with_highest_cost() -> dict[str, Any] | None:
        try:
            with Database() as db:
                sql = """
                SELECT
                    phan_loai_doi,
                    REPLACE(
                        FORMAT(COALESCE(SUM(REPLACE(chi_phi_thuc_te, ',', '') + 0), 0), 0),
                        ',',
                        '.'
                    ) AS tong_chi_phi,
                    COUNT(*) AS so_luong_xe
                FROM khbd_sc
                GROUP BY phan_loai_doi
                ORDER BY tong_chi_phi DESC
                LIMIT 1
                """
                db.cursor.execute(sql)
                row = db.cursor.fetchone()
            return row if row else {
                "found": False,
                "message": "No data found for team with highest cost."
            }
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving team with highest cost. Error: {str(e)}"
            }
            
    #ĐỘi xe nào có số lượng xe cần sửa chữa nhiều nhất trong tuần này hoặc tháng này
    @staticmethod
    def get_team_with_most_vehicles(period: str = "tuần") -> dict[str, Any] | None:
        if period not in ["tuần", "tháng"]:
            raise ValueError("Thời gian không hợp lệ. Dùng 'tuần' hoặc 'tháng'.")

        try:
            with Database(dictionary=True) as db:
                if period == "tuần":
                    date_condition = """
                        YEARWEEK(ngay_du_kien_thuc_hien, 1) = YEARWEEK(CURDATE(), 1)
                    """
                else:
                    date_condition = """
                        MONTH(ngay_du_kien_thuc_hien) = MONTH(CURDATE())
                        AND YEAR(ngay_du_kien_thuc_hien) = YEAR(CURDATE())
                    """

                sql = f"""
                    WITH team_count AS (
                        SELECT
                            phan_loai_doi,
                            COUNT(*) AS so_luong_xe
                        FROM khbd_sc
                        WHERE ngay_du_kien_thuc_hien IS NOT NULL
                            AND {date_condition}
                        GROUP BY doi_xe
                        ORDER BY so_luong_xe DESC
                        LIMIT 1
                    )
                    SELECT
                        tc.so_luong_xe,
                        k.bks,
                        k.chung_loai,
                        k.noi_dung_sua_chua,
                        COALESCE(k.ngay_thuc_hien, k.ngay_du_kien_thuc_hien) AS ngay
                    FROM khbd_sc k
                    JOIN team_count tc ON k.phan_loai_doi = tc.phan_loai_doi
                    WHERE k.ngay_du_kien_thuc_hien IS NOT NULL
                    AND {date_condition}
                    ORDER BY ngay ASC, k.bks ASC;
                """

                db.cursor.execute(sql)
                rows = db.cursor.fetchall()

            return rows if rows else {
                "found": False,
                "message": f"Không có dữ liệu trong {period} này."
            }

        except Exception as e:
            return {
                "found": False,
                "message": f"Lỗi khi lấy đội xe có nhiều xe nhất trong {period}: {str(e)}"
            }

    #tổng chi phí thực hiện
    @staticmethod
    def get_total_actual_cost() -> dict[str, Any] | None: 
        try:
            with Database() as db:
                sql = """
                SELECT
                    REPLACE(
                        FORMAT(COALESCE(SUM(REPLACE(chi_phi_thuc_te, ',', '') + 0), 0), 0),
                        ',',
                        '.'
                    ) AS tong_chi_phi_thuc_te
                FROM khbd_sc
                """
                db.cursor.execute(sql)
                row = db.cursor.fetchone()
            return row if row else {
                "found": False,
                "message": "No data found for total actual cost."
            }
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving total actual cost. Error: {str(e)}"
            }
            
    @staticmethod
    #chênh lệch giữa thành tiền và chi phí hiện tại, đưa ra % chênh lệch
    def get_registration_cost_difference() -> dict[str, Any]:
        try:
            sql = """
            SELECT
                tong_thanh_tien,
                tong_chi_phi,
                tong_chi_phi - tong_thanh_tien AS muc_chenh_lech,
                CASE
                    WHEN tong_chi_phi > tong_thanh_tien THEN 'Cao hơn'
                    WHEN tong_chi_phi < tong_thanh_tien THEN 'Thấp hơn'
                    ELSE 'Bằng nhau'
                END AS trang_thai,
                CASE
                    WHEN tong_thanh_tien = 0 THEN 0
                    ELSE ROUND(((tong_chi_phi - tong_thanh_tien) / tong_thanh_tien) * 100, 2)
                END AS ti_le_chenh_lech
            FROM (
                SELECT
                    COALESCE(SUM(REPLACE(thanh_tien, ',', '') + 0), 0) AS tong_thanh_tien,
                    COALESCE(SUM(REPLACE(chi_phi_thuc_hien, ',', '') + 0), 0) AS tong_chi_phi
                FROM kh_dang_kiem
                WHERE ngay_thuc_hien IS NOT NULL
            ) AS t;
        """

            with Database(dictionary=True) as db:
                db.cursor.execute(sql)
                row = db.cursor.fetchone()

            return row

        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
            
    # ds Xe trong tháng này có sửa chữa gì
    def get_vehicle_repairs_this_month(bks: list[str] | str | None = None) -> dict[str, Any]:
        try:
            if isinstance(bks, str):
                bks = [bks]

            if bks:
                bks = [x.strip() for x in bks if x and x.strip()]

            if not bks:
                return {
                    "found": False,
                    "error": "Chưa truyền biển số xe",
                }

            placeholders = ", ".join(["%s"] * len(bks))

            sql = f"""
            SELECT
                bks,
                chung_loai,
                phan_loai_doi,
                noi_dung_sua_chua,
                CASE
                    WHEN ngay_thuc_hien IS NOT NULL THEN 'Đã hoàn thành'
                    ELSE 'Chưa hoàn thành'
                END AS trang_thai,
                CASE
                    WHEN ngay_thuc_hien IS NOT NULL THEN ngay_thuc_te
                    ELSE ngay_du_kien_thuc_hien
                END AS ngay,
                CASE
                    WHEN ngay_thuc_hien IS NOT NULL THEN chi_phi_thuc_hien
                    ELSE thanh_tien
                END AS chi_phi
            FROM khbd_sc
            WHERE bks IN ({placeholders})
              AND COALESCE(ngay_thuc_hien, ngay_du_kien_thuc_hien) IS NOT NULL
              AND MONTH(COALESCE(ngay_thuc_hien, ngay_du_kien_thuc_hien)) = MONTH(CURDATE())
              AND YEAR(COALESCE(ngay_thuc_hien, ngay_du_kien_thuc_hien)) = YEAR(CURDATE())
            ORDER BY bks ASC, ngay ASC;
            """

            with Database(dictionary=True) as db:
                db.cursor.execute(sql, tuple(bks))
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": "Không tìm thấy sửa chữa trong tháng này",
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