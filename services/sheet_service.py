import gspread
from google.oauth2.service_account import Credentials
import os


class SheetService:
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    def __init__(self, credentials_path="config/credentials.json"): 
        #Create a SheetService instance
        self.credentials_path = credentials_path
        self.sheet_id = os.getenv("GOOGLE_SHEET_ID")
        self.client = self._get_client()
    
    def _get_client(self):
        #Initialize gspread client using service account credentials
        if not os.path.exists(self.credentials_path):
            raise FileNotFoundError(f"❌ Not found file {self.credentials_path}")
        
        creds = Credentials.from_service_account_file(
            self.credentials_path,
            scopes=self.SCOPES
        )
        return gspread.authorize(creds)
    
    def open_sheet(self, sheet_id = os.getenv("GOOGLE_SHEET_ID")):
        """Open a Google sheet by it's ID"""
        try:
            return self.client.open_by_key(sheet_id)
        except Exception as e:
            raise Exception(f"Error opening sheet: {e}")
    
    def get_all_data(self, sheet_id = None, sheet_name="Sheet1"):
        if sheet_id is None:
            sheet_id = os.getenv("GOOGLE_SHEET_ID")
        spreadsheet = self.open_sheet(sheet_id)
        worksheet = spreadsheet.worksheet(sheet_name)
        
        return worksheet.get_all_records()
    
    def get_sheet_info(self, sheet_id = None):
        """Get basic info about the sheet"""
        if sheet_id is None:
            sheet_id = os.getenv("GOOGLE_SHEET_ID")
        spreadsheet = self.open_sheet(sheet_id)
        
        return {
            "title": spreadsheet.title,
            "sheet_count": len(spreadsheet.worksheets()),
            "sheets": [
                {
                    "name": sheet.title,
                    "rows": sheet.row_count,
                    "cols": sheet.col_count
                }
                for sheet in spreadsheet.worksheets()
            ]
        }
    
    def get_columns(self, sheet_id=None, sheet_name="Sheet1"):
        """Get column names (header row)"""
        if sheet_id is None:
            sheet_id = os.getenv("GOOGLE_SHEET_ID")
        
        data = self.get_all_data(sheet_id, sheet_name)
        
        if data:
            return list(data[0].keys())
        return []
    
   
                