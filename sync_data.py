import time
from services.sheet_service import SheetService

def sync_data():
    SheetService.sync_vehicle_data("Thông tin xe", 3)
    print("✅ Sync data thông tin xe thành công")
    time.sleep(2)
    SheetService.sync_trailer_data("Thông tin Rơ mooc", 3)
    print("✅ Sync data thông tin rơ mooc thành công")
    time.sleep(2)
    SheetService.sync_inspection_data("KH Đăng kiểm T6.26", 6)
    print("✅ Sync data thông tin KH Đăng kiểm thành công")
    time.sleep(2)
    SheetService.sync_ghep_data("Ghép xe - mooc - cont", 2)
    print("✅ Sync data thông tin ghép xe - mooc - cont thành công")
    time.sleep(2)
    SheetService.sync_thay_dau_data("Theo dõi thay dầu", 4)
    print("✅ Sync data thông tin thay dầu thành công")
    time.sleep(2)
    SheetService.sync_lsu_bdsc_data("Lịch sử BDSC", 1)
    print("✅ Sync data thông tin LSU - BDSC thành công")
    time.sleep(2)
    SheetService.sync_ke_hoach_data("BDSC - TTVT6.26", 6)
    print("✅ Sync data thông tin kế hoạch BDSC thành công")
    
if __name__ == "__main__":
    sync_data()