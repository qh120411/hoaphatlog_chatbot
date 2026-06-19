from typing import Any
from database.db_connect import Database

class PairDataService:
    @staticmethod
    def get_pair_data( plate_number: str | None = None, plate: str | None = None, fields: list[str] | str | None = None, ) -> dict[str, Any]:
        plate_value = plate_number or ""
        try:
            with Database() as db:
                sql = """
                SELECT
                    bks_xe_cu,
                    bks_xe_moi,
                    chung_loai_xe,
                    bks_ro_mooc_cu,
                    bks_ro_mooc_moi,
                    so_cont,
                    loai_cont,
                    ho_ten_lx,
                    dv_quan_ly,
                    nguoi_dieu_hanh
                FROM ghep_xe
                WHERE bks_xe_moi = %s OR bks_xe_cu = %s OR bks_ro_mooc_moi = %s OR bks_ro_mooc_cu = %s
                """
                db.cursor.execute(sql, (plate_value, plate_value, plate_value, plate_value))
                rows = db.cursor.fetchall()
                
            if not rows:
                return {
                    "found": False,
                    "message": f"No data found for plate number: {plate_number}"
                }
            selected_fields = PairDataService.normalize_fields(fields, rows)
            pair = (
                {
                    field: rows.get(field) for field in selected_fields
                }
                if selected_fields else rows
            )
            return {
                "found": True,
                "pair": pair
            }
            
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving data for plate number: {plate_number}. Error: {str(e)}"
            }

    @staticmethod
    #Họ tên ng lái xe hiện đang lái xe nào
    def get_data_by_name(name: str) -> dict[str, Any] | None:
        name_value = name or ""
        try:
            with Database() as db:
                sql = """
                SELECT
                    bks_xe_cu,
                    bks_xe_moi,
                    chung_loai_xe,
                    bks_ro_mooc_cu,
                    bks_ro_mooc_moi,
                    so_cont,
                    loai_cont,
                    ho_ten_lx,
                    sdt,
                    dv_quan_ly,
                    nguoi_dieu_hanh
                FROM ghep_xe
                WHERE ho_ten_lx = %s
                """
                db.cursor.execute(sql, (name_value,))
                rows = db.cursor.fetchall()
            return rows if rows else {
                "found": False,
                "message": f"No data found for name: {name}"
            }
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving data for name: {name}. Error: {str(e)}"
            }
    
    @staticmethod
    #Mooc này đang ghép với xe nào cont nào 
    
    
    @staticmethod
    #cont dang ghép với xe nào mooc nào
    def get_pair_by_cont ( cont_number: str) -> dict[str, Any] | None:
        cont_value = cont_number or ""
        try:
            with Database() as db:
                sql = """
                SELECT
                    bks_xe_cu,
                    bks_xe_moi,
                    chung_loai_xe,
                    bks_ro_mooc_cu,
                    bks_ro_mooc_moi,
                    so_cont,
                    ho_ten_lx,
                    sdt,
                    dv_quan_ly,
                    nguoi_dieu_hanh
                FROM ghep_xe
                WHERE so_cont = %s
                """
                db.cursor.execute(sql, (cont_value,))
                rows = db.cursor.fetchall()
            return rows if rows else {
                "found": False,
                "message": f"No data found for container number: {cont_number}"
            }
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving data for container number: {cont_number}. Error: {str(e)}"
            }
    
    #Hỏi thông tin người lái xe dựa trên bks | mooc 
    @staticmethod
    def get_driver_info( plate_number: str | None = None, mooc_number: str | None = None) -> dict[str, Any] | None:
        plate_value = plate_number or ""
        mooc_value = mooc_number or ""
        try:
            with Database() as db:
                sql = """
                SELECT
                    ho_ten_lx,
                    cccd,
                    sdt,
                    dv_quan_ly,
                    nguoi_dieu_hanh
                FROM ghep_xe
                WHERE bks_xe_moi = %s OR bks_xe_cu = %s OR bks_ro_mooc_moi = %s OR bks_ro_mooc_cu = %s
                """
                db.cursor.execute(sql, (plate_value, plate_value, mooc_value, mooc_value))
                rows = db.cursor.fetchall()
            return rows if rows else {
                "found": False,
                "message": f"No driver information found for plate number: {plate_number} or mooc number: {mooc_number}"
            }
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving driver information for plate number: {plate_number} or mooc number: {mooc_number}. Error: {str(e)}"
            }
            
    @staticmethod
    def get_info_by_name(name: str) -> dict[str, Any] | None:
        name_value = name or ""
        try:
            with Database() as db:
                sql = """
                SELECT
                    ho_ten_lx,
                    sdt,
                    cccd,
                    gplx,
                    dv_quan_ly,
                    nguoi_dieu_hanh
                FROM ghep_xe
                WHERE ho_ten_lx = %s
                """
                db.cursor.execute(sql, (name_value,))
                rows = db.cursor.fetchall()
            return rows if rows else {
                "found": False,
                "message": f"No data found for name: {name}"
            }
        except Exception as e:
            return {
                "found": False,
                "message": f"Error retrieving data for name: {name}. Error: {str(e)}"
            }
            
    COLUMNS = """
        stt,
        bks_xe_cu,
        bks_xe_moi,
        chung_loai_xe,
        bks_ro_mooc_cu,
        bks_ro_mooc_moi,
        so_cont,
        loai_cont,
        ngay_thay_doi,
        ho_ten_lx,
        cccd,
        gplx,
        sdt,
        dv_quan_ly,
        nguoi_dieu_hanh
    """

    @staticmethod
    def _fetch(sql: str, params: tuple = ()) -> list[dict[str, Any]] | dict[str, Any]:
        try:
            with Database(dictionary=True) as db:
                db.cursor.execute(sql, params)
                return db.cursor.fetchall()
        except Exception as exc:
            return {"found": False, "error": str(exc)}

    @staticmethod
    def _where(
        value: str | None = None,
        plate_number: str | None = None,
        ro_mooc_number: str | None = None,
        cont_number: str | None = None,
    ) -> tuple[str, tuple]:
        if plate_number:
            return "(bks_xe_cu = %s OR bks_xe_moi = %s)", (plate_number, plate_number)
        if ro_mooc_number:
            return "(bks_ro_mooc_cu = %s OR bks_ro_mooc_moi = %s)", (ro_mooc_number, ro_mooc_number)
        if cont_number:
            return "so_cont = %s", (cont_number,)
        if value:
            return """
                (
                    bks_xe_cu = %s OR bks_xe_moi = %s
                    OR bks_ro_mooc_cu = %s OR bks_ro_mooc_moi = %s
                    OR so_cont = %s
                )
            """, (value, value, value, value, value)
        return "", ()

    @staticmethod
    # Xe nay dang ghep voi ro mooc nao, cont nao, ai lai
    def get_pair_by_vehicle(plate_number: str | None = None, plate: str | None = None) -> list[dict[str, Any]] | dict[str, Any]:
        plate_value = plate_number or plate
        if not plate_value:
            return {"found": False, "message": "Chua truyen bien so xe"}

        sql = f"""
            SELECT
                {PairDataService.COLUMNS},
                COUNT(*) OVER() AS so_luong
            FROM ghep_xe
            WHERE bks_xe_cu = %s OR bks_xe_moi = %s
            ORDER BY ngay_thay_doi DESC, stt DESC
            LIMIT 1
        """
        return PairDataService._fetch(sql, (plate_value, plate_value))

    @staticmethod
    # Ro mooc hoac cont nay dang ghep voi xe nao, ai su dung
    def get_pair_by_ro_mooc_or_cont(
        ro_mooc_number: str | None = None,
        cont_number: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        if ro_mooc_number:
            where_sql = "bks_ro_mooc_cu = %s OR bks_ro_mooc_moi = %s"
            params = (ro_mooc_number, ro_mooc_number)
        elif cont_number:
            where_sql = "so_cont = %s"
            params = (cont_number,)
        else:
            return {"found": False, "message": "Chua truyen so ro mooc hoac so cont"}

        sql = f"""
            SELECT
                {PairDataService.COLUMNS},
                COUNT(*) OVER() AS so_luong
            FROM ghep_xe
            WHERE {where_sql}
            ORDER BY ngay_thay_doi DESC, stt DESC
            LIMIT 1
        """
        return PairDataService._fetch(sql, params)

    @staticmethod
    # Lan cap nhat/thay doi gan nhat da thay doi thong tin gi so voi lan truoc do
    def get_latest_pair_change(
        value: str | None = None,
        plate_number: str | None = None,
        ro_mooc_number: str | None = None,
        cont_number: str | None = None,
    ) -> dict[str, Any]:
        where_sql, params = PairDataService._where(value, plate_number, ro_mooc_number, cont_number)
        if not where_sql:
            return {"found": False, "message": "Chua truyen bien so xe, ro mooc hoac so cont"}

        sql = f"""
            SELECT {PairDataService.COLUMNS}
            FROM ghep_xe
            WHERE {where_sql}
            ORDER BY ngay_thay_doi DESC, stt DESC
            LIMIT 2
        """
        rows = PairDataService._fetch(sql, params)
        if isinstance(rows, dict) or len(rows) < 2:
            return {"found": False, "message": "Khong du du lieu de so sanh thay doi"}

        latest, previous = rows[0], rows[1]
        check_cols = [
            "bks_xe_cu",
            "bks_xe_moi",
            "chung_loai_xe",
            "bks_ro_mooc_cu",
            "bks_ro_mooc_moi",
            "so_cont",
            "loai_cont",
            "ho_ten_lx",
            "cccd",
            "gplx",
            "sdt",
            "dv_quan_ly",
            "nguoi_dieu_hanh",
        ]
        changes = [
            {
                "cot_thay_doi": col,
                "gia_tri_cu": previous.get(col),
                "gia_tri_moi": latest.get(col),
            }
            for col in check_cols
            if previous.get(col) != latest.get(col)
        ]

        return {
            "found": True,
            "latest": latest,
            "previous": previous,
            "changes": changes,
        }
    
    @staticmethod
    # Trong thang/khoang thoi gian nhat dinh, nhung xe nao co thay doi thong tin
    def get_vehicle_changes_by_period(
        period: str = "thang_nay",
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> dict[str, Any]:
        if from_date and to_date:
            date_condition = "ngay_thay_doi BETWEEN %s AND %s"
            params = (from_date, to_date)
        elif period == "tuan_nay":
            date_condition = "YEARWEEK(ngay_thay_doi, 1) = YEARWEEK(CURDATE(), 1)"
            params = ()
        elif period == "thang_truoc":
            date_condition = "ngay_thay_doi >= DATE_FORMAT(CURDATE() - INTERVAL 1 MONTH, '%Y-%m-01') AND ngay_thay_doi <= LAST_DAY(CURDATE() - INTERVAL 1 MONTH)"
            params = ()
        else:
            date_condition = "MONTH(ngay_thay_doi) = MONTH(CURDATE()) AND YEAR(ngay_thay_doi) = YEAR(CURDATE())"
            params = ()

        check_cols = [
            "bks_xe_cu",
            "bks_xe_moi",
            "chung_loai_xe",
            "bks_ro_mooc_cu",
            "bks_ro_mooc_moi",
            "so_cont",
            "loai_cont",
            "ho_ten_lx",
            "dv_quan_ly",
            "nguoi_dieu_hanh",
        ]
        prev_cols = ",\n".join(
            f"LAG({col}) OVER(PARTITION BY COALESCE(NULLIF(bks_xe_cu, ''), NULLIF(bks_xe_moi, ''), stt) ORDER BY ngay_thay_doi ASC, stt ASC) AS prev_{col}"
            for col in check_cols
        )

        sql = f"""
            WITH history AS (
                SELECT
                    {PairDataService.COLUMNS},
                    {prev_cols}
                FROM ghep_xe
            )
            SELECT *
            FROM history
            WHERE {date_condition}
            ORDER BY ngay_thay_doi DESC, stt DESC
        """
        rows = PairDataService._fetch(sql, params)
        if isinstance(rows, dict):
            return rows

        result = []
        for row in rows:
            changes = [
                {
                    "cot_thay_doi": col,
                    "gia_tri_cu": row.get(f"prev_{col}"),
                    "gia_tri_moi": row.get(col),
                }
                for col in check_cols
                if row.get(f"prev_{col}") is not None and row.get(f"prev_{col}") != row.get(col)
            ]
            if changes:
                result.append({
                    "bks_xe_cu": row.get("bks_xe_cu"),
                    "bks_xe_moi": row.get("bks_xe_moi"),
                    "chung_loai_xe": row.get("chung_loai_xe"),
                    "ngay_thay_doi": row.get("ngay_thay_doi"),
                    "changes": changes,
                })

        return {
            "found": bool(result),
            "vehicles": result,
        }
    
    
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