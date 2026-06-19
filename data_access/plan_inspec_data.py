from typing import Any
from database.db_connect import Database

class PlanInspecDataService:
    @staticmethod
    #check xe thực hiện đăng kiểm chưa
    def check_vehicle_inspection():
        try:
            with Database() as db:
                sql = """
                SELECT
                    bks_xe_cu,
                    bks_xe_moi,
                    chung_loai_xe,
                    han_dang_kiem,
                    COUNT(*) OVER() AS tong
                FROM kh_dang_kiem
                WHERE ngay_thuc_hien IS NULL
                """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()
            
            if not rows:
                return {
                    "found": False,
                    "message": "No inspection data found."
                }
            return rows
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving inspection data. Error: {str(e)}"
            }
    
    @staticmethod
    #check mooc thực hiện đăng kiểm chưa
    def check_trailer_inspection():
        try:
            with Database() as db:
                sql = """
                SELECT
                    bks_ro_mooc,
                    chung_loai_mooc,
                    han_dang_kiem_ro_mooc,
                    COUNT(*) OVER() AS tong
                FROM kh_dang_kiem
                WHERE ngay_thuc_hien IS NULL
                """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()
            
            if not rows:
                return {
                    "found": False,
                    "message": "No inspection data found."
                }
            return rows
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving inspection data. Error: {str(e)}"
            }
    
    @staticmethod
    #check xe thực hiện đăng kiểm theo kế hoạch tháng này chưa
    def check_vehicle_inspection_time():
        try:
            with Database() as db:
                sql = """
                SELECT
                    bks_xe_cu,
                    bks_xe_moi,
                    chung_loai_xe,
                    han_dang_kiem,
                    COUNT(*) OVER() AS tong
                FROM kh_dang_kiem
                WHERE ngay_thuc_hien IS NULL AND MONTH(han_dang_kiem_xe) = MONTH(CURRENT_DATE())
                """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()
            
            if not rows:
                return {
                    "found": False,
                    "message": "No inspection data found for this month."
                }
            return rows
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving inspection data for this month. Error: {str(e)}"
            }
        
    @staticmethod
    #check mooc thực hiện đăng kiểm theo kế hoạch tháng này chưa
    def check_trailer_inspection_time():
        try:
            with Database() as db:
                sql = """
                SELECT
                    bks_ro_mooc,
                    chung_loai_mooc,
                    han_dang_kiem_ro_mooc,
                    COUNT(*) OVER() AS tong
                FROM kh_dang_kiem
                WHERE ngay_thuc_hien IS NULL AND MONTH(han_dang_kiem_ro_mooc) = MONTH(CURRENT_DATE())
                """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()
            
            if not rows:
                return {
                    "found": False,
                    "message": "No inspection data found for this month."
                }
            return rows
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving inspection data for this month. Error: {str(e)}"
            }
            
    @staticmethod
    #check xe thực hiện đăng kiểm theo kế hoạch
    def check_vehicle_inspection_plan():
        try:
            with Database() as db:
                sql = """
                SELECT
                    bks_xe_cu,
                    bks_xe_moi,
                    chung_loai_xe,
                    han_dang_kiem_xe,
                    ngay_thuc_hien,
                    dang_kiem_tai,
                    chi_phi_thuc_hien,
                    COUNT(*) OVER() AS tong
                FROM kh_dang_kiem
                WHERE ngay_thuc_hien IS NOT NULL AND MONTH(han_dang_kiem_xe) = MONTH(CURRENT_DATE())
                """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()
            
            if not rows:
                return {
                    "found": False,
                    "message": "No inspection data found for this month."
                }
            return rows
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving inspection data for this month. Error: {str(e)}"
            }
            
    @staticmethod
    #check mooc thực hiện đăng kiểm theo kế hoạch
    def check_vehicle_inspection_plan():
        try:
            with Database() as db:
                sql = """
                SELECT
                    bks_ro_mooc,
                    chung_loai_mooc,
                    han_dang_kiem_ro_mooc,
                    ngay_thuc_hien,
                    dang_kiem_tai,
                    chi_phi_thuc_hien,
                    COUNT(*) OVER() AS tong
                FROM kh_dang_kiem
                WHERE ngay_thuc_hien IS NOT NULL AND MONTH(han_dang_kiem_ro_mooc) = MONTH(CURRENT_DATE())
                """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()
            
            if not rows:
                return {
                    "found": False,
                    "message": "No inspection data found for this month."
                }
            return rows
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving inspection data for this month. Error: {str(e)}"
            }
            
    ### lúc test hỏi thử xem chọn dc 2 tool k
    @staticmethod
    #check xe lẫn mooc thực hiện đăng kiểm theo kế hoạch
    def check_inspection_plan():
        try:
            with Database() as db:
                sql = """SELECT
                        loai_doi_tuong,
                        bks_cu,
                        bks_moi,
                        chung_loai,
                        han_dang_kiem,
                        ngay_thuc_hien,
                        dang_kiem_tai,
                        chi_phi_thuc_hien,
                        COUNT(*) OVER() AS tong
                    FROM (
                        SELECT
                        'XE' AS loai_doi_tuong,
                        bks_xe_cu AS bks_cu,
                        bks_xe_moi AS bks_moi,
                        chung_loai_xe AS chung_loai,
                        han_dang_kiem_xe AS han_dang_kiem,
                        ngay_thuc_hien,
                        dang_kiem_tai,
                        chi_phi_thuc_hien
                        FROM kh_dang_kiem
                     WHERE ngay_thuc_hien IS NOT NULL
                    AND MONTH(han_dang_kiem_xe) = MONTH(CURRENT_DATE())

                    UNION ALL

                    SELECT
                    'RO_MOOC' AS loai_doi_tuong,
                    bks_ro_mooc AS bks_cu,
                    NULL AS bks_moi,
                    chung_loai_mooc AS chung_loai,
                    han_dang_kiem_ro_mooc AS han_dang_kiem,
                    ngay_thuc_hien,
                    dang_kiem_tai,
                    chi_phi_thuc_hien
                    FROM kh_dang_kiem
                    WHERE ngay_thuc_hien IS NOT NULL
                    AND MONTH(han_dang_kiem_ro_mooc) = MONTH(CURRENT_DATE())
                    ) AS dk;"""
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()
            return rows if rows else {
                "found": False,
                "message": "No inspection data found for this month."
            }
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving inspection data for this month. Error: {str(e)}"
            }
    
    #Tính tổng chi phí thực hiện
    @staticmethod
    def get_sum_cost():
        try:
            with Database() as db:
                sql = """
                SELECT
                    REPLACE(
                        FORMAT(COALESCE(SUM(REPLACE(chi_phi_thuc_hien, ',', '') + 0), 0), 0),
                        ',',
                        '.'
                    ) AS tong_chi_phi
                    FROM kh_dang_kiem
                    WHERE ngay_thuc_hien IS NOT NULL
                    AND MONTH(han_dang_kiem_xe) = MONTH(CURRENT_DATE());
                """
                db.cursor.execute(sql)
                row = db.cursor.fetchone()
            return row["tong_chi_phi"] if row and row["tong_chi_phi"] is not None else 0
        except Exception as e:
            return {
                "found": False,
                "message": f"Error calculating total cost for this month. Error: {str(e)}"
            }
                
    @staticmethod
    #so sánh tổng chi phí thực hiện với kế hoạch
    def compare_cost_with_plan():
            with Database() as db:
                sql = """
                SELECT
            tong_thanh_tien,
            tong_chi_phi_thuc_hien,
            tong_chi_phi_thuc_hien - tong_thanh_tien AS so_tien_chenh_lech,
            CASE
                WHEN tong_chi_phi_thuc_hien - tong_thanh_tien > 0 THEN 'Cao hơn'
                WHEN tong_chi_phi_thuc_hien - tong_thanh_tien < 0 THEN 'Thấp hơn'
                ELSE 'Bằng nhau'
            END AS trang_thai_chenh_lech,
            CASE
                WHEN tong_thanh_tien = 0 THEN 0
                ELSE ((tong_chi_phi_thuc_hien - tong_thanh_tien) / tong_thanh_tien) * 100
            END AS ti_le_phan_tram_chenh_lech
        FROM (
            SELECT
                COALESCE(SUM(REPLACE(thanh_tien, ',', '') + 0), 0) AS tong_thanh_tien,
                COALESCE(SUM(REPLACE(chi_phi_thuc_hien, ',', '') + 0), 0) AS tong_chi_phi_thuc_hien
            FROM kh_dang_kiem
            WHERE ngay_thuc_hien IS NOT NULL
              AND MONTH(han_dang_kiem_xe) = MONTH(CURRENT_DATE())
              AND YEAR(han_dang_kiem_xe) = YEAR(CURRENT_DATE())
        ) AS t
                """
                db.cursor.execute(sql)
                row = db.cursor.fetchone()
                return row
            
    @staticmethod
    #Đếm xe và mooc có chi phí thực hiện cao hoặc nhỏ hoặc bằng
    def count_cost_comparison():
        try:
            with Database() as db:
                sql = """
                SELECT
                    loai_doi_tuong,
                    bks,
                    chung_loai,
                    thanh_tien,
                    chi_phi_thuc_te,
                    trang_thai,
                    chenh_lech,
                    COUNT(*) OVER(PARTITION BY loai_doi_tuong, trang_thai) AS tong_theo_loai_va_trang_thai,
                    COUNT(*) OVER(PARTITION BY trang_thai) AS tong_theo_trang_thai
                FROM (
                    SELECT
                        loai_doi_tuong,
                        bks,
                        chung_loai,
                        thanh_tien,
                        chi_phi_thuc_te,
                CASE
                WHEN chi_phi_thuc_te > thanh_tien THEN 'Lớn hơn'
                WHEN chi_phi_thuc_te < thanh_tien THEN 'Nhỏ hơn'
                ELSE 'Bằng'
                END AS trang_thai,
                CASE
                    WHEN chi_phi_thuc_te > thanh_tien THEN chi_phi_thuc_te - thanh_tien
                    WHEN chi_phi_thuc_te < thanh_tien THEN thanh_tien - chi_phi_thuc_te
                ELSE 0
                END AS chenh_lech
                FROM (
                    SELECT
                    'XE' AS loai_doi_tuong,
                    bks_xe_cu AS bks,
                    chung_loai_xe AS chung_loai,
                    REPLACE(thanh_tien, ',', '') + 0 AS thanh_tien,
                    REPLACE(chi_phi_thuc_hien, ',', '') + 0 AS chi_phi_thuc_te
                    FROM kh_dang_kiem
                    WHERE ngay_thuc_hien IS NOT NULL
                    AND bks_xe_cu IS NOT NULL

                UNION ALL

                SELECT
                'RO_MOOC' AS loai_doi_tuong,
                bks_ro_mooc AS bks,
                chung_loai_mooc AS chung_loai,
                REPLACE(thanh_tien, ',', '') + 0 AS thanh_tien,
                REPLACE(chi_phi_thuc_hien, ',', '') + 0 AS chi_phi_thuc_te
                FROM kh_dang_kiem
                WHERE ngay_thuc_hien IS NOT NULL
                    AND bks_ro_mooc IS NOT NULL
                ) AS raw_data
                    ) AS compared_data
                    ORDER BY loai_doi_tuong, trang_thai, bks;
                """
                db.cursor.execute(sql)
                rows = db.cursor.fetchall()
            return rows if rows else {
                "found": False,
                "message": "No cost comparison data found for this month."
            }
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving cost comparison data for this month. Error: {str(e)}"
            }
    
    @staticmethod
    #2 trường hợp
    def get_dang_kiem_status_by_bks(bks: list[str] | str | None = None) -> dict[str, Any]:
        try:
            if isinstance(bks, str):
                bks = [bks]

            if not bks:
                return {
                    "found": False,
                    "error": "Chưa truyền biển số",
                }

            placeholders = ", ".join(["%s"] * len(bks))

            sql = f"""
                SELECT
                    'XE' AS loai,
                    COALESCE(bks_xe_moi, bks_xe_cu) AS bks,
                    chung_loai_xe AS chung_loai,
                    han_dang_kiem_xe AS han_dang_kiem,
                    ngay_thuc_hien,
                    dang_kiem_tai,
                    chi_phi_thuc_hien,
                    CASE
                        WHEN ngay_thuc_hien IS NOT NULL THEN 'Đã đăng kiểm'
                        ELSE 'Chưa đăng kiểm'
                    END AS trang_thai,
                    CASE
                        WHEN ngay_thuc_hien IS NULL THEN DATEDIFF(han_dang_kiem_xe, CURRENT_DATE())
                        ELSE NULL
                    END AS so_ngay_con_lai
                    FROM kh_dang_kiem
                WHERE bks_xe_cu IN ({placeholders})
                    OR bks_xe_moi IN ({placeholders})

                UNION ALL

                SELECT
                    'RO_MOOC' AS loai,
                    bks_ro_mooc AS bks,
                    chung_loai_mooc AS chung_loai,
                    han_dang_kiem_ro_mooc AS han_dang_kiem,
                    ngay_thuc_hien,
                    dang_kiem_tai,
                    chi_phi_thuc_hien,
                    CASE
                        WHEN ngay_thuc_hien IS NOT NULL THEN 'Đã đăng kiểm'
                        ELSE 'Chưa đăng kiểm'
                    END AS trang_thai,
                    CASE
                        WHEN ngay_thuc_hien IS NULL THEN DATEDIFF(han_dang_kiem_ro_mooc, CURRENT_DATE())
                        ELSE NULL
                    END AS so_ngay_con_lai
                    FROM kh_dang_kiem
                WHERE bks_ro_mooc IN ({placeholders});
            """

            params = tuple(bks) * 3

            with Database(dictionary=True) as db:
                db.cursor.execute(sql, params)
                rows = db.cursor.fetchall()

            return {
                "found": True,
                "data": rows,
            }

        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }   
            
    @staticmethod
    #xe và rơ mooc chưa thực hiện đăng kiểm trong tháng này
    def get_inspection_not_done_this_month () -> list[dict[str, Any]]:
        with Database() as db:
            sql = """
                SELECT
    loai_doi_tuong,
    bks_cu,
    bks_moi,
    chung_loai,
    han_dang_kiem,
    ngay_thuc_hien,
    dang_kiem_tai,
    chi_phi_thuc_hien,
    COUNT(*) OVER() AS tong
FROM (
    SELECT
        'XE' AS loai_doi_tuong,
        bks_xe_cu AS bks_cu,
        bks_xe_moi AS bks_moi,
        chung_loai_xe AS chung_loai,
        han_dang_kiem_xe AS han_dang_kiem,
        ngay_thuc_hien,
        dang_kiem_tai,
        chi_phi_thuc_hien
    FROM kh_dang_kiem
    WHERE ngay_thuc_hien IS NULL
      AND han_dang_kiem_xe >= DATE_FORMAT(CURRENT_DATE(), '%Y-%m-01')
      AND han_dang_kiem_xe < DATE_ADD(DATE_FORMAT(CURRENT_DATE(), '%Y-%m-01'), INTERVAL 1 MONTH)

    UNION ALL

    SELECT
        'RO_MOOC' AS loai_doi_tuong,
        bks_ro_mooc AS bks_cu,
        NULL AS bks_moi,
        chung_loai_mooc AS chung_loai,
        han_dang_kiem_ro_mooc AS han_dang_kiem,
        ngay_thuc_hien,
        dang_kiem_tai,
        chi_phi_thuc_hien
    FROM kh_dang_kiem
    WHERE ngay_thuc_hien IS NULL
      AND han_dang_kiem_ro_mooc >= DATE_FORMAT(CURRENT_DATE(), '%Y-%m-01')
      AND han_dang_kiem_ro_mooc < DATE_ADD(DATE_FORMAT(CURRENT_DATE(), '%Y-%m-01'), INTERVAL 1 MONTH)
) AS dk;"""

            db.cursor.execute(sql)
            rows = db.cursor.fetchall()
            if not rows:
                return {
                    "found": False,
                    "message": "No inspection data found for this month."
                }
            return rows