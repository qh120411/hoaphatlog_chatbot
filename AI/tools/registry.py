from data_access.vehicle_data import VehicleDataService
from data_access.trailer_data import TrailerDataService
TOOL_REGISTRY = {
    
    # === XE ===
    
    "search_vehicle": {
        "description": "Tìm kiếm thông tin mong muốn dựa trên biển số xe hoặc biển số xe mới.",
        "intents" : ["vehicle_lookup", "plate_lookup"],
        "args": {
            "required": ["plate_number"],
            "optional": ["fields"]
        },
        "output" : {
            "found": "Có tìm thấy xe không?",
            "vehicle" : {
                "description": "Thông tin về xe nếu tìm thấy.",    
                "fields": {
                    "stt": "Số thứ tự",
                    "bks": "Biển số xe cũ",
                    "bks_moi": "Biển số xe mới",
                    "loai_xe_chung_loai": "Chủng loại xe",
                    "loai_xe": "Loại xe",
                    "don_vi_quan_ly": "Đơn vị quản lý",
                    "nam_sx": "Năm sản xuất",
                    "so_may": "Số máy",
                    "so_khung": "Số khung",
                    "so_dang_kiem": "Số đăng kiểm",
                    "ngay_het_han_dang_kiem": "Ngày hết hạn đăng kiểm",
                    "so_dang_ky": "Số đăng ký",
                    "dang_ky_goc": "Đăng ký gốc",
                    "han_gia_han_giay_ngan_hang": "Hạn gia hạn giấy ngân hàng",
                    "cong_ty_or_ngan_hang": "Công ty hoặc ngân hàng",
                    "han_bao_hiem": "Hạn bảo hiểm",
                    "cong_ty_bao_hiem": "Công ty bảo hiểm",
                    "han_bao_hiem_vc": "Hạn bảo hiểm vật chất",
                    "cong_ty_bao_hiem_vc": "Công ty bảo hiểm vật chất",
                    "han_phu_hieu": "Hạn phụ hiệu",
                    "thiet_bi_gsht": "Thiết bị giám sát hành trình",
                    "ngay_het_han_camera": "Ngày hết hạn camera",
                    "camera_giam_sat": "Camera giám sát",
                    "tinh_trang": "Tình trạng",
                    "mau": "Màu",
                    "kich_thuoc_thung_xe": "Kích thước thùng xe",
                    "tai_trong_ban_than": "Tải trọng bản thân",
                    "khoi_luong_cho_phep_tren_mam_keo_tggt": "Khối lượng cho phép trên mâm kéo tham gia giao thông",
                    "khoi_luong_hang_cc_theo_tk_cp_tggt": "Khối lượng hàng hóa theo thiết kế cho phép tham gia giao thông",
                    "khoi_luong_toan_bo_theo_tk_cp_tggt": "Khối lượng toàn bộ theo thiết kế cho phép tham gia giao thông"
                },   
            }
        },
        "handler": VehicleDataService.search_vehicle
        
    },

    "get_inspection_due": {
        "description": "Lấy danh sách xe có hạn đăng kiểm trong một khoảng thời gian nhất định.",
        "intents" : ["inspection_due"],
        "args": {
            "required": ["days"],
            "optional": []
        },
        "output" : {
            "found": {
                "type": "bool",
                "description": "Cho biết có tìm thấy xe nào sắp hết hạn đăng kiểm hay không."
            },
            "total": {
                "type": "int",
                "description": "Tổng số xe có hạn đăng kiểm trong khoảng thời gian đã chỉ định."
            },
            "days": {
                "type": "int",
                "description": "Số ngày được kiểm tra tính từ ngày hôm nay."
            },
            "vehicles": {
                "type": "list",
                "description": "Danh sách xe sắp hết hạn đăng kiểm.",
                "items": {
                    "type": "object",
                    "fields": {
                        "bien_so": {
                            "type": "str",
                            "description": "Biển số xe."
                        },
                        "han_dang_kiem": {
                            "type": "str",
                            "description": "Ngày hết hạn đăng kiểm."
                        },
                        "songay_con_lai": {
                            "type": "int",
                            "description": "Số ngày còn lại trước khi hết hạn đăng kiểm."
                        }
                    }
                }
            }
        },
        "handler": VehicleDataService.get_inspection_due
    },

    "get_inspection_expired": {
        "description": "Lấy danh sách xe đã hết hạn đăng kiểm.",
        "intents" : ["inspection_expired"],
        "args": {
            "required": [],
            "optional": []
        },
        "handler": VehicleDataService.get_inspection_expired
    },

    "get_vehicle_inspection": {
        "description": "Lấy thông tin đăng kiểm của xe dựa trên biển số xe.",
        "intents" : ["inspection_lookup"],
        "args": {
            "required": ["plate_number"],
            "optional": []
        },
        "handler": VehicleDataService.get_vehicle_inspection
    },
    #chưa nghĩ ra dc intent nào cho tool này, để tạm trống
    "get_nearest_inspection_due": {
        "description": "Lấy ra danh sách các xe cùng hạn đăng kiểm gần nhất",
        "intents" : [""],
        "args": {
            "required": [],
            "optional": []
        },
        "handler": VehicleDataService.get_nearest_inspection_due
    },
    
    "get_inspection_due_top_unit" : {
        "description": "Lấy ra đơn vị có nhiều xe sắp hết hạn đăng kiểm nhất trong N ngày tới hoặc tháng tới.",
        "intents" : ["top_due_inspection_units"],
        "args": {
            "required": ["days"],
            "optional": []
        },
        "handler": VehicleDataService.get_inspection_due_top_unit
    },

    "get_insurance_due": {
        "description": "Lấy danh sách xe có hạn bảo hiểm trong một khoảng thời gian nhất định.",
        "intents" : ["insurance_due"],
        "args": {
            "required": ["days"],
            "optional": []
        },
        "handler": VehicleDataService.get_insurance_due
    },
    
    #chưa nghĩ ra dc intent nào cho tool này, để tạm trống
    "get_nearest_insurance_due": {
        "description": "Lấy ra danh sách các xe cùng hạn bảo hiểm gần nhất",
        "intents" : [""],
        "args": {
            "required": [],
            "optional": []
        },
        "handler": VehicleDataService.get_nearest_insurance_due
    },
    
    "get_insurance_due_top_unit" : {
        "description": "Lấy ra đơn vị có nhiều xe sắp hết hạn bảo hiểm nhất trong N ngày tới hoặc tháng tới.",
        "intents" : ["top_due_insurance_units"],
        "args": {
            "required": ["days"],
            "optional": []
        },
        "handler": VehicleDataService.get_insurance_due_top_unit
    },
    
    "get_vehicle_bank_extension": {
        "description": "Lấy thông tin về giấy gia hạn ngân hàng của xe dựa trên biển số xe.",
        "intents" : ["bank_extension_lookup"],
        "args": {
            "required": ["plate_number"],
            "optional": []
        },
        "handler": VehicleDataService.get_vehicle_bank_extension
    },
    
    #chưa nghĩ ra dc intent
    "get_nearest_bank_extension_due": {
        "description": "Lấy ra danh sách các xe cùng hạn gia hạn ngân hàng gần nhất",
        "intents" : [""],
        "args": {
            "required": [],
            "optional": []
        },
        "handler": VehicleDataService.get_nearest_bank_extension_due
    },
    
    "get_vehicles_by_insurance_company": {
        "description": "Lấy danh sách xe được bảo hiểm bởi một công ty bảo hiểm cụ thể.",
        "intents" : ["vehicles_by_insurance_company"],
        "args": {
            "required": ["insurance_company"],
            "optional": []
        },
        "handler": VehicleDataService.get_vehicles_by_insurance_company
    },
    
    "get_inactive_vehicles": {
        "description": "Lấy danh sách xe không hoạt động hoặc đang nằm trong bãi giữ xe.",
        "intents" : ["inactive_vehicles"],
        "args": {
            "required": [],
            "optional": []
        },
        "handler": VehicleDataService.get_inactive_vehicles
    },
    
    "get_vehicle_count_by_management_unit": {
        "description": "Đếm số lượng xe theo đơn vị quản lý. Nếu người dùng hỏi thống kê tất cả đơn vị thì không truyền units. Nếu người dùng hỏi một hoặc nhiều đơn vị cụ thể thì truyền danh sách tên dơn vị vào units ",
        "intents" : ["vehicle_count_by_management_unit", "count_vehicles_by_unit", "management_unit_vehicle_count", "specific_units_vehicle_count"],
        "args": {
            "required": [],
            "optional": ["units"]
        },
        "output": {
            "found": "Có tìm thấy dữ liệu hay không?",
            "data": {
                "description": "Danh sách đơn vị quản lý và số lượng xe tương ứng.",
                "fields": {
                    "don_vi_quan_ly": "Tên đơn vị quản lý",
                    "so_luong_xe": "Số lượng xe thuộc đơn vị quản lý đó"
                }
            }
        },
        "handler": VehicleDataService.get_vehicle_count_by_management_unit
    },
    "get_vehicles_by_bank" : {
        "description": "Lấy danh sách xe đang vay tại một ngân hàng cụ thể.",
        "intents" : ["vehicles_by_bank"],
        "args": {
            "required": ["bank_name"],
            "optional": []
        },
        "handler": VehicleDataService.get_vehicles_by_bank
    },
    
    # === RƠ MÓC === 
    
    "search_trailer": {
        "description": "Tìm kiếm thông tin mong muốn dựa trên biển số rơ moóc.",
        "intents" : ["trailer_lookup"],
        "args": {
            "required": ["plate_number"],
            "optional": ["fields"]
        },
        "output" : {
            "found": "Có tìm thấy rơ moóc không?",
            "vehicle" : {
                "description": "Thông tin về rơ moóc nếu tìm thấy.",  
                "fields": {
                    "bks_ro_mooc_cu": "Biển số rơ moóc cũ",
                    "bks_ro_mooc_moi": "Biển số rơ moóc mới",
                    "loai": "Loại mooc của công ty nào",
                    "loai_mooc": "Loại rơ moóc",
                    "don_vi_quan_ly": "Đơn vị quản lý",
                    "nam_san_xuat": "Năm sản xuất",
                    "so_khung": "Số khung",
                    "so_dang_kiem": "Số đăng kiểm",
                    "ngay_het_han_dang_kiem": "Ngày hết hạn đăng kiểm",
                    "so_dang_ky": "Số đăng ký",
                    "ngay_het_han": "Ngày hết hạn đăng ký",
                    "ngay_het_han_giay_ngan_hang": "Ngày hết hạn giấy ngân hàng",
                    "ngan_hang": "Ngân hàng",
                    "ngay_het_han_bao_hiem": "Ngày hết hạn bảo hiểm",
                    "cong_ty_bao_hiem": "Công ty bảo hiểm",
                    "mau": "Màu rơ moóc",
                    "khoi_luong_ban_than": "Khối lượng bản thân",
                    "khoi_luong_chuyen_cho": "Khối lượng chuyên chở",
                    "hien_trang": "Hiện trạng"
                }
            }
        },
        "handler": TrailerDataService.search_trailer
    },
    


    
}

def get_prompt_tools() -> list[dict]:
    return [
        {
            "name": tool_name,
            "description": tool_info["description"],
            "intents": tool_info["intents"],
            "args": tool_info["args"],
            "output": tool_info.get("output", {})
        }
        for tool_name, tool_info in TOOL_REGISTRY.items()
    ]

def get_tool_spec(tool_name: str) -> dict | None:
    if not tool_name:
        return None
    return TOOL_REGISTRY.get(tool_name)
