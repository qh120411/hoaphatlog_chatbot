from typing import Any
from database.db_connect import Database

class PlanChangeOilDataService:
    #lấy thông tin thay dầu theo biển số xe
    @staticmethod
    def get_name_oil_by_plate(plate_number: str | None = None) -> dict[str, Any]:
        plate_value = plate_number or ""
        try:
            with Database() as db:
                sql = """
                SELECT
                    bks_xe_cu,
                    bks_xe_moi,
                    loai_xe_chung_loai,
                    loai_dau
                FROM thay_dau
                WHERE bks_xe_moi = %s OR bks_xe_cu = %s
                """
                db.cursor.execute(sql, (plate_value, plate_value))
                rows = db.cursor.fetchall()
                
            if not rows:
                return {
                    "found": False,
                    "message": f"No data found for plate number: {plate_number}"
                }
            return rows
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving data for plate number: {plate_number}. Error: {str(e)}"
            }
        
    @staticmethod
    #Xe còn chạy bnh lâu thì thay dầu
    def get_scl_by_plate(plate_number: str | None = None) -> dict[str, Any]:
        plate_value = plate_number or ""
        try:
            with Database() as db:
                sql = """
                SELECT
                    bks_xe_cu,
                    bks_xe_moi,
                    loai_xe_chung_loai,
                    km_da_chay,
                    skm_con_lai_den_thay_dau
                FROM thay_dau
                WHERE bks_xe_moi = %s OR bks_xe_cu = %s
                """
                db.cursor.execute(sql, (plate_value, plate_value))
                rows = db.cursor.fetchall()
                
            if not rows:
                return {
                    "found": False,
                    "message": f"No data found for plate number: {plate_number}"
                }
            return rows
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving data for plate number: {plate_number}. Error: {str(e)}"
            }
    
    @staticmethod
    #Xe thay dầu gần nhất ngày nào
    def get_near_date_by_plate(plate_number: str | None = None) -> dict[str, Any]:
        plate_value = plate_number or ""
        try:
            with Database() as db:
                sql = """
                SELECT
                    bks_xe_cu,
                    bks_xe_moi,
                    loai_xe_chung_loai,
                    ngay_thay_dau_gan_nhat,
                    km_lan_thay_dau_truoc
                FROM thay_dau
                WHERE bks_xe_moi = %s OR bks_xe_cu = %s
                """
                db.cursor.execute(sql, (plate_value, plate_value))
                rows = db.cursor.fetchall()
                
            if not rows:
                return {
                    "found": False,
                    "message": f"No data found for plate number: {plate_number}"
                }
            return rows
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving data for plate number: {plate_number}. Error: {str(e)}"
            }
            
    @staticmethod
    #Các xe nào còn bnh km còn lại đổ xuống / dưới ...
    def get_vehicle_by_scl ( scl: int ) -> list[dict[str, Any]]:
        try:
            with Database() as db:
                sql = """
                SELECT
                    bks_xe_cu,
                    bks_xe_moi,
                    loai_xe_chung_loai,
                    km_hien_tai,
                    ngay_cap_nhat,
                    skm_con_lai_den_thay_dau,
                    COUNT(*) OVER() as  total_vehicles
                FROM thay_dau
                WHERE skm_con_lai_den_thay_dau <= %s
                """
                db.cursor.execute(sql, (scl,))
                rows = db.cursor.fetchall()
                
            if not rows:
                return []
            return rows
        except Exception as e:
            print(f"Error retrieving vehicles with remaining km <= {scl}. Error: {str(e)}")
            return []
        
    @staticmethod
    #Xe đã chạy bnh km kể từ lần thay dầu gần nhất
    def get_km_since_last_oil_change(plate_number: str | None = None) -> dict[str, Any]:
        plate_value = plate_number or ""
        try:
            with Database() as db:
                sql = """
                SELECT
                    bks_xe_cu,
                    bks_xe_moi,
                    loai_xe_chung_loai,
                    km_hien_tai,
                    ngay_cap_nhat,
                    km_da_chay
                FROM thay_dau
                WHERE bks_xe_moi = %s OR bks_xe_cu = %s
                """
                db.cursor.execute(sql, (plate_value, plate_value))
                rows = db.cursor.fetchall()
                
            if not rows:
                return {
                    "found": False,
                    "message": f"No data found for plate number: {plate_number}"
                }
            return rows
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving data for plate number: {plate_number}. Error: {str(e)}"
            }
            
    @staticmethod
    #Các xe nào đã chạy bnh km kể từ lần thay dầu gần nhất
    def get_vehicles_by_km_since_last_oil_change(km: int) -> list[dict[str, Any]]:
        try:
            with Database() as db:
                sql = """
                SELECT
                    bks_xe_cu,
                    bks_xe_moi,
                    loai_xe_chung_loai,
                    km_hien_tai,
                    ngay_cap_nhat,
                    km_da_chay,
                    COUNT(*) OVER() as total_vehicles
                FROM thay_dau
                WHERE km_da_chay >= %s
                """
                db.cursor.execute(sql, (km,))
                rows = db.cursor.fetchall()
                
            if not rows:
                return []
            return rows
        except Exception as e:
            print(f"Error retrieving vehicles with km since last oil change >= {km}. Error: {str(e)}")
            return []
        
    @staticmethod
    #Có bao nhiêu xe thuộc đơn vị ... còn ... km còn lại đến thay dầu
    def get_oil_change_count_by_management_unit( units: list[str] | str | None = None,skm_con_lai: int = 0) -> dict[str, Any]:
        try:
            if isinstance(units, str):
                units = [units]

            if units:
                units = [u.strip() for u in units if u and u.strip()]

            sql = """
                WITH RECURSIVE tmp AS (
                    SELECT
                        bks_xe_cu,
                        bks_xe_moi,
                        loai_xe_chung_loai,
                        km_hien_tai,
                        ngay_cap_nhat,
                        skm_con_lai_den_thay_dau,
                        TRIM(SUBSTRING_INDEX(dv_quan_ly, '-', 1)) AS don_vi,
                        CASE
                            WHEN LOCATE('-', dv_quan_ly) > 0
                            THEN SUBSTRING(dv_quan_ly, LOCATE('-', dv_quan_ly) + 1)
                            ELSE ''
                        END AS phan_con_lai
                    FROM thay_dau
                     WHERE dv_quan_ly IS NOT NULL
                    AND TRIM(dv_quan_ly) <> ''

                    UNION ALL

                    SELECT
                        bks_xe_cu,
                        bks_xe_moi,
                        loai_xe_chung_loai,
                        km_hien_tai,
                        ngay_cap_nhat,
                        skm_con_lai_den_thay_dau,
                        TRIM(SUBSTRING_INDEX(phan_con_lai, '-', 1)) AS don_vi,
                        CASE
                            WHEN LOCATE('-', phan_con_lai) > 0
                            THEN SUBSTRING(phan_con_lai, LOCATE('-', phan_con_lai) + 1)
                            ELSE ''
                        END AS phan_con_lai
                    FROM tmp
                    WHERE phan_con_lai <> ''
                )
            """

            with Database(dictionary=True) as db:
                if not units:
                    sql += """
                        SELECT
                            don_vi AS dv_quan_ly,
                            COUNT(*) AS vehicle_count
                        FROM tmp
                        WHERE don_vi <> ''
                        AND skm_con_lai_den_thay_dau <= %s
                        GROUP BY don_vi
                        ORDER BY vehicle_count DESC, don_vi ASC;
                    """
                    db.cursor.execute(sql, (skm_con_lai,))
                else:
                    placeholders = ", ".join(["%s"] * len(units))

                    sql += f"""
                        SELECT
                            don_vi AS dv_quan_ly,
                            COUNT(*) AS vehicle_count
                        FROM tmp
                        WHERE don_vi IN ({placeholders})
                        AND skm_con_lai_den_thay_dau <= %s
                        GROUP BY don_vi
                        ORDER BY vehicle_count DESC, don_vi ASC;
                    """
                    db.cursor.execute(sql, tuple(units) + (skm_con_lai,))

                rows = db.cursor.fetchall()

            return rows

        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }
            
    @staticmethod
    #Có bao nhiêu xe thuộc đơn vị ... đã chạy trên bnh km kể từ lần thay dầu gần nhất
    def get_oil_change_vehicles_by_management_unit( units: list[str] | str, km: int ) -> dict[str, Any]:
        try:
            if isinstance(units, str):
                units = [units]

            units = [u.strip() for u in units if u and u.strip()]

            if not units:
                return {
                    "found": False,
                    "error": "Chưa truyền đơn vị quản lý",
                }

            placeholders = ", ".join(["%s"] * len(units))

            sql = f"""
                WITH RECURSIVE tmp AS (
                    SELECT
                        bks_xe_cu,
                        bks_xe_moi,
                        loai_xe_chung_loai,
                        km_hien_tai,
                        ngay_cap_nhat,
                        km_da_chay,
                        TRIM(SUBSTRING_INDEX(dv_quan_ly, '-', 1)) AS don_vi,
                        CASE
                            WHEN LOCATE('-', dv_quan_ly) > 0
                            THEN SUBSTRING(dv_quan_ly, LOCATE('-', dv_quan_ly) + 1)
                            ELSE ''
                        END AS phan_con_lai
                    FROM thay_dau
                    WHERE dv_quan_ly IS NOT NULL
                        AND TRIM(dv_quan_ly) <> ''

                    UNION ALL

                    SELECT
                        bks_xe_cu,
                        bks_xe_moi,
                        loai_xe_chung_loai,
                        km_hien_tai,
                        ngay_cap_nhat,
                        km_da_chay,
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
                        don_vi,
                        bks_xe_cu,
                        bks_xe_moi,
                        loai_xe_chung_loai,
                        km_hien_tai,
                        ngay_cap_nhat,
                        km_da_chay
                    FROM tmp
                    WHERE don_vi <> ''
                )
                SELECT
                    don_vi AS dv_quan_ly,
                    bks_xe_cu,
                    bks_xe_moi,
                    loai_xe_chung_loai,
                    km_hien_tai,
                    ngay_cap_nhat,
                    km_da_chay,
                    COUNT(*) OVER() AS so_luong
                FROM dedup
                WHERE don_vi IN ({placeholders})
                AND km_da_chay > %s
                ORDER BY km_da_chay DESC, bks ASC;
            """

            with Database(dictionary=True) as db:
                db.cursor.execute(sql, tuple(units) + (km,))
                rows = db.cursor.fetchall()

            if not rows:
                return {
                    "found": False,
                    "message": "Không tìm thấy xe nào phù hợp",
                }

            return {
                "found": True,
                "so_luong": rows[0]["so_luong"],
                "vehicles": rows,
            }

        except Exception as exc:
            return {
                "found": False,
                "error": str(exc),
            }