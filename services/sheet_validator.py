from datetime import date, datetime, timedelta

DATE_FORMATS = [
    "%Y-%m-%d",   # 2024-06-15
    "%d/%m/%Y",   # 15/06/2024
    "%m/%d/%Y",   # 06/15/2024
    "%d-%m-%Y",   # 15-06-2024
    "%m-%d-%Y",   # 06-15-2024
    "%d.%m.%Y",   # 15.06.2024
    "%Y.%m.%d",   # 2024.06.15
    "%d %m %Y",   # 15 06 2024
    "%Y%m%d",     # 20240615
]


class SheetValidator:
    @staticmethod
    def validate_date(date_str: str) -> str | None:
        if not date_str or date_str.strip() == "":
            return None
        # Remove leading/trailing whitespace to avoid parsing issues
        date_str = date_str.strip()

        # Try all formats in DATE_FORMATS until one matches. If none matches, return None.
        for fmt in DATE_FORMATS:
            try:
                dt = datetime.strptime(date_str, fmt)
                if 1000 <= dt.year <= 9999 :
                    return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        return None

    @staticmethod
    def empty_to_none(value):
        if value is None:
            return None
        if isinstance(value, str) and value.strip() == "":
            return None
        return value
        
