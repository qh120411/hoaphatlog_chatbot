from data_access.vehicle_data import VehicleDataService
from data_access.trailer_data import TrailerDataService
from data_access.ls_bdsc import BdscDataService
from data_access.pair_data import PairDataService
from data_access.plan_inspec_data import PlanInspecDataService
from data_access.khbd_data import PlanInspecDataService as KhbdDataService
from data_access.thaydau import PlanChangeOilDataService
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
        "intents" : ["nearest_vehicle_inspection_due", "nearest_inspection_due"],
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
        "intents" : ["nearest_vehicle_insurance_due", "nearest_insurance_due"],
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
        "intents" : ["nearest_vehicle_bank_extension_due", "nearest_bank_extension_due"],
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
    
    "get_vehicles_by_age_or_year": {
        "description":  "Lấy danh sách và số lượng xe theo tuổi xe hoặc năm sản xuất.",
        "intents": ["vehicles_by_age_or_year"],
        "args": {"required": ["value"], "optional": ["filter_type", "comparison"]},
        "handler": VehicleDataService.get_vehicles_by_age_or_year,
    },
    
    "get_vehicles_by_unit": {
        "description": "Lấy danh sách xe theo đơn vị quản lý. Nếu người dùng hỏi về một đơn vị cụ thể thì truyền tên đơn vị vào unit_name, nếu người dùng hỏi về tất cả đơn vị thì để trống unit_name hoặc truyền all vào unit_name",
        "intents": ["vehicles_by_unit"],
        "args": {"required": ["unit_name"], "optional": []},
        "handler": VehicleDataService.get_vehicles_by_unit,
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
    "get_missing_vehicle_info": {
        "description": "Lấy danh sách xe chưa có thông tin hoặc đang thiếu thông tin",
        "intents": ["missing_vehicle_info"],
        "args": {
            "required": [],
            "optional": ["info_type"]
        },
        "handler": VehicleDataService.get_missing_vehicle_info
    },


    "get_vehicle_due_items": {
        "description": "Lấy danh sách các mục của xe sắp hết hạn trong N ngày tới.",
        "intents": ["vehicle_due_items"],
        "args": {
            "required": [],
            "optional": ["document_type", "days"]
        },
        "handler": VehicleDataService.get_vehicle_due_items
    },
    
    "get_inspection_trailer": {
        "description": "Lấy danh sách rơ mooc sắp hết hạn đăng kiểm trong N ngày tới.",
        "intents": ["trailer_inspection_due"],
        "args": {"required": [], "optional": ["days"]},
        "handler": TrailerDataService.get_inspection_trailer,
    },
    "get_trailer_inspection_due_top_unit": {
        "description": "Lấy đơn vị quản lý có nhiều rơ mooc sắp hết hạn đăng kiểm nhất trong N ngày tới.",
        "intents": ["trailer_inspection_due_top_unit"],
        "args": {"required": [], "optional": ["day"]},
        "handler": TrailerDataService.get_trailer_inspection_due_top_unit,
    },
    "get_trailer_bank_extension": {
        "description": "Lấy thông tin gia hạn giấy ngân hàng của rơ mooc theo biển số",
        "intents": ["trailer_bank_extension_lookup"],
        "args": {"required": ["plate_number"], "optional": []},
        "handler": TrailerDataService.get_trailer_bank_extension,
    },
    "get_trailer_by_bank": {
        "description": "Lấy danh sách rơ mooc hiện đang vay tại một ngân hàng cụ thể",
        "intents": ["trailers_by_bank"],
        "args": {"required": ["bank_name"], "optional": []},
        "handler": TrailerDataService.get_trailer_by_bank,
    },
    "get_trailer_by_insurance_company": {
        "description": "Lấy danh sách rơ mooc theo công ty bảo hiểm cụ thể",
        "intents": ["trailers_by_insurance_company"],
        "args": {"required": ["insurance_company"], "optional": []},
        "handler": TrailerDataService.get_trailer_by_insurance_company,
    },
    "get_trailer_count_by_management_unit": {
        "description": "Đếm số lượng rơ mooc theo đơn vị quản lý",
        "intents": ["trailer_count_by_management_unit"],
        "args": {"required": [], "optional": ["units"]},
        "handler": TrailerDataService.get_trailer_count_by_management_unit,
    },
    "get_trailer_by_managemein_unit": {
        "description": "Lấy danh sách rơ mooc theo đơn vị quản lý",
        "intents": ["trailers_by_management_unit"],
        "args": {"required": ["unit"], "optional": []},
        "handler": TrailerDataService.get_trailer_by_managemein_unit,
    },
    "get_inactive_trailers": {
        "description": "Lấy danh sách rơ mooc không hoạt động hoặc đang nằm bãi",
        "intents": ["inactive_trailers"],
        "args": {"required": [], "optional": []},
        "handler": TrailerDataService.get_inactive_trailers,
    },
    "get_trailers_by_age_or_year": {
        "description": "Lấy danh sách và số lượng rơ mooc theo tuổi mooc hoặc năm sản xuất.",
        "intents": ["trailers_by_age_or_year"],
        "args": {"required": ["value"], "optional": ["filter_type", "comparison"]},
        "handler": TrailerDataService.get_trailers_by_age_or_year,
    },
    "get_trailer_due_items": {
        "description": "Lấy các mục sắp hết hạn của rơ mooc như đăng kiểm, đăng ký, bảo hiểm, ngân hàng, ...",
        "intents": ["trailer_due_items"],
        "args": {"required": [], "optional": ["document_type", "days", "plate_number"]},
        "handler": TrailerDataService.get_trailer_due_items,
    },
    "get_trailer_insurance_due": {
        "description": "Lấy danh sách rơ mooc sắp hết hạn bảo hiểm trong N ngày tới.",
        "intents": ["trailer_insurance_due"],
        "args": {"required": [], "optional": ["days"]},
        "handler": TrailerDataService.get_trailer_insurance_due,
    },
    
    # === GHEP XE - missing from pair_data.py ===
    "get_pair_data": {
        "description": "Lấy thông tin về xe, rơ mooc, cont và họ tên lái xe theo biển số",
        "intents": ["pair_lookup"],
        "args": {"required": ["plate_number"], "optional": ["fields"]},
        "handler": PairDataService.get_pair_data,
    },
    "get_data_by_name": {
        "description": "Lấy thông tin xe, rơ mooc, cont theo tên lái xe.",
        "intents": ["pair_by_driver_name"],
        "args": {"required": ["name"], "optional": []},
        "handler": PairDataService.get_data_by_name,
    },
    "get_pair_by_cont": {
        "description": "Lấy thông tin xe, rơ mooc đang ghép với số container cụ thể.",
        "intents": ["pair_by_cont"],
        "args": {"required": ["cont_number"], "optional": []},
        "handler": PairDataService.get_pair_by_cont,
    },
    "get_driver_info": {
        "description": "Lấy thông tin của người lái xe theo biển số xe hoặc biển số rơ mooc.",
        "intents": ["driver_info_by_vehicle_or_trailer"],
        "args": {"required": [], "optional": ["plate_number", "mooc_number"]},
        "handler": PairDataService.get_driver_info,
    },
    "get_info_by_name": {
        "description": "Lấy thông tin cá nhân của lái xe dựa trên họ và tên của lái xe.",
        "intents": ["driver_info_by_name"],
        "args": {"required": ["name"], "optional": []},
        "handler": PairDataService.get_info_by_name,
    },
    "get_pair_by_vehicle": {
        "description": "Lấy thông tin xe đang ghép với rơ mooc nào, cont nào và họ tên người lái xe",
        "intents": ["pair_by_vehicle"],
        "args": {"required": ["plate_number"], "optional": []},
        "handler": PairDataService.get_pair_by_vehicle,
    },
    "get_pair_by_ro_mooc_or_cont": {
        "description": "Lấy thông tin rơ mooc hoặc cont đang ghép với xe nào và ai là người lái xe/ sử dụng",
        "intents": ["pair_by_ro_mooc_or_cont"],
        "args": {"required": [], "optional": ["ro_mooc_number", "cont_number"]},
        "handler": PairDataService.get_pair_by_ro_mooc_or_cont,
    },
    "get_latest_pair_change": {
        "description": "Lấy lần thay đổi gần nhất và các thông tin đã thay đổi so với lần trước.",
        "intents": ["latest_pair_change"],
        "args": {"required": [], "optional": ["value", "plate_number", "ro_mooc_number", "cont_number"]},
        "handler": PairDataService.get_latest_pair_change,
    },
    "get_vehicle_changes_by_period": {
        "description": "Lấy danh sách xe có thay đổi thông tin trong tháng hoặc không thời gian nhất định",
        "intents": ["vehicle_changes_by_period"],
        "args": {"required": [], "optional": ["period", "from_date", "to_date"]},
        "handler": PairDataService.get_vehicle_changes_by_period,
    },

    # === KE HOACH DANG KIEM - missing from plan_inspec_data.py ===
    "check_vehicle_inspection": {
        "description": "Kiểm tra xe chưa thực hiện đăng kiểm theo kế hoạch đăng kiểm tháng này.",
        "intents": ["check_vehicle_inspection"],
        "args": {"required": [], "optional": []},
        "handler": PlanInspecDataService.check_vehicle_inspection,
    },
    "check_trailer_inspection": {
        "description": "Kiểm tra rơ mooc chưa thực hiện đăng kiểm theo kế hoạch đăng kiểm tháng này",
        "intents": ["check_trailer_inspection"],
        "args": {"required": [], "optional": []},
        "handler": PlanInspecDataService.check_trailer_inspection,
    },
    "check_vehicle_inspection_time": {
        "description": "Kiểm tra xe chưa thực hiện đăng kiểm theo kế hoạch đăng kiểm tháng này và thời gian thực hiện đăng kiểm.",
        "intents": ["check_vehicle_inspection_time"],
        "args": {"required": [], "optional": []},
        "handler": PlanInspecDataService.check_vehicle_inspection_time,
    },
    "check_trailer_inspection_time": {
        "description": "Kiểm tra rơ mooc chưa thực hiện đăng kiểm theo kế hoạch đăng kiểm tháng này.",
        "intents": ["check_trailer_inspection_time"],
        "args": {"required": [], "optional": []},
        "handler": PlanInspecDataService.check_trailer_inspection_time,
    },
    "check_vehicle_inspection_plan": {
        "description": "Kiểm tra danh sách xe đã thực hiện đăng kiểm theo kế hoạch đăng kiểm tháng này.",
        "intents": ["check_vehicle_inspection_plan"],
        "args": {"required": [], "optional": []},
        "handler": PlanInspecDataService.check_vehicle_inspection_plan,
    },
    "check_inspection_plan": {
        "description": "Kiểm tra xe va rơ mooc đã thực hiện đăng kiểm theo kế hoạch tháng này.",
        "intents": ["check_inspection_plan"],
        "args": {"required": [], "optional": []},
        "handler": PlanInspecDataService.check_inspection_plan,
    },
    "get_sum_cost": {
        "description": "Tính tổng chi phí thực hiện đăng kiểm theo kế hoạch tháng này.",
        "intents": ["inspection_sum_cost"],
        "args": {"required": [], "optional": []},
        "handler": PlanInspecDataService.get_sum_cost,
    },
    "compare_cost_with_plan": {
        "description": "So sánh tổng chi phí thực hiện với kế hoạch đăng kiểm.",
        "intents": ["inspection_compare_cost_with_plan"],
        "args": {"required": [], "optional": []},
        "handler": PlanInspecDataService.compare_cost_with_plan,
    },
    "count_cost_comparison": {
        "description": "Đếm xe và rơ mooc có chi phí thực hiện cao hơn, thấp hơn hoặc bằng kế hoạch.",
        "intents": ["inspection_count_cost_comparison"],
        "args": {"required": [], "optional": []},
        "handler": PlanInspecDataService.count_cost_comparison,
    },
    "get_dang_kiem_status_by_bks": {
        "description": "Lấy trạng thái đăng kiểm trong tháng này từ 1 hoặc nhiều biển số.",
        "intents": ["inspection_status_by_bks"],
        "args": {"required": ["bks"], "optional": []},
        "handler": PlanInspecDataService.get_dang_kiem_status_by_bks,
    },
    
    "get_inspection_not_done_this_month": {
        "description": "Lấy danh sách xe và rơ mooc chưa thực hiện đăng kiểm trong tháng này theo kế hoạch.",
        "intents": ["inspection_done_this_month"],
        "args": {"required": [], "optional": []},
        "handler": PlanInspecDataService.get_inspection_not_done_this_month,
    },

    # === KE HOACH BAO DUONG SUA CHUA - missing from khbd_data.py ===
    "get_vehicle_due": {
        "description": "Lấy danh sách xe cần bảo dưỡng sửa chữa trong N ngày tới",
        "intents": ["maintenance_vehicle_due"],
        "args": {"required": [], "optional": ["days"]},
        "handler": KhbdDataService.get_vehicle_due,
    },
    "get_recently_serviced": {
        "description": "Lấy danh sách xe đã sửa chữa trong tuần này hoặc tháng này.",
        "intents": ["recently_serviced"],
        "args": {"required": [], "optional": ["period"]},
        "handler": KhbdDataService.get_recently_serviced,
    },
    "get_not_serviced": {
        "description": "Lấy danh sách xe chưa sửa chữa trong tuần này hoặc tháng này.",
        "intents": ["not_serviced"],
        "args": {"required": [], "optional": ["period"]},
        "handler": KhbdDataService.get_not_serviced,
    },
    "get_cost_discrepancy": {
        "description": "Lấy các xe có chi phí thực tế nhỏ hơn hoặc lớn hơn giá thành tiền.",
        "intents": ["maintenance_cost_discrepancy"],
        "args": {"required": [], "optional": ["comparison"]},
        "handler": KhbdDataService.get_cost_discrepancy,
    },
    "get_team_with_highest_cost": {
        "description": "Lấy đội xe có tổng chi phí thực hiện lớn nhất",
        "intents": ["team_with_highest_cost"],
        "args": {"required": [], "optional": []},
        "handler": KhbdDataService.get_team_with_highest_cost,
    },
    "get_team_with_most_vehicles": {
        "description": "Lấy đội xe có số lượng xe cần sữa chữa nhiều nhất trong tuần hoặc tháng",
        "intents": ["team_with_most_vehicles"],
        "args": {"required": [], "optional": ["period"]},
        "handler": KhbdDataService.get_team_with_most_vehicles,
    },
    "get_total_actual_cost": {
        "description": "Tính tổng chi phí thực tế của kế hoạch bảo dưỡng sửa chữa.",
        "intents": ["total_actual_cost"],
        "args": {"required": [], "optional": []},
        "handler": KhbdDataService.get_total_actual_cost,
    },
    "get_registration_cost_difference": {
        "description": "Tính chênh lệch giữa thành tiền và chi phí thực hiện",
        "intents": ["registration_cost_difference"],
        "args": {"required": [], "optional": []},
        "handler": KhbdDataService.get_registration_cost_difference,
    },
    "get_vehicle_repairs_this_month": {
        "description": "Lấy danh sách xe tron tháng này có sửa chữa gì.",
        "intents": ["vehicle_repairs_this_month"],
        "args": {"required": ["bks"], "optional": []},
        "handler": KhbdDataService.get_vehicle_repairs_this_month,
    },

    # === THAY DAU - missing from thaydau.py ===
    "get_name_oil_by_plate": {
        "description": "Lấy thông tin loại dầu theo biển số xe",
        "intents": ["oil_name_by_plate"],
        "args": {"required": ["plate_number"], "optional": []},
        "handler": PlanChangeOilDataService.get_name_oil_by_plate,
    },
    "get_scl_by_plate": {
        "description": "Lấy số km còn lại đến thay dầu theo biển số xe",
        "intents": ["oil_remaining_km_by_plate"],
        "args": {"required": ["plate_number"], "optional": []},
        "handler": PlanChangeOilDataService.get_scl_by_plate,
    },
    "get_near_date_by_plate": {
        "description": "Lấy ngày thay dầu gàn nhất theo biển số xe",
        "intents": ["oil_nearest_date_by_plate"],
        "args": {"required": ["plate_number"], "optional": []},
        "handler": PlanChangeOilDataService.get_near_date_by_plate,
    },
    "get_vehicle_by_scl": {
        "description": "Lấy danh sách xe còn số km đến thay dầu nhỏ hơn hoặc bằng một giá trị cụ thể.",
        "intents": ["vehicles_by_remaining_oil_km"],
        "args": {"required": ["scl"], "optional": []},
        "handler": PlanChangeOilDataService.get_vehicle_by_scl,
    },
    "get_km_since_last_oil_change": {
        "description": "Lấy số km xe đã chạy từ lần thay dầu gần nhất theo biển số xe.",
        "intents": ["km_since_last_oil_change"],
        "args": {"required": ["plate_number"], "optional": []},
        "handler": PlanChangeOilDataService.get_km_since_last_oil_change,
    },
    "get_vehicles_by_km_since_last_oil_change": {
        "description": "Lấy danh sách xe đã chạy trên N km kể từ lần thay dầu gần nhất.",
        "intents": ["vehicles_by_km_since_last_oil_change"],
        "args": {"required": ["km"], "optional": []},
        "handler": PlanChangeOilDataService.get_vehicles_by_km_since_last_oil_change,
    },
    "get_oil_change_count_by_management_unit": {
        "description": "Đếm số xe theo đơn vị quản lý còn N km đến thay dầu.",
        "intents": ["oil_change_count_by_management_unit"],
        "args": {"required": [], "optional": ["units", "skm_con_lai"]},
        "handler": PlanChangeOilDataService.get_oil_change_count_by_management_unit,
    },
    "get_oil_change_vehicles_by_management_unit": {
        "description": "Lấy danh sách xe theo đơn vị quản lý đã chạy trên N km kể từ lần thay dầu gần nhất.",
        "intents": ["oil_change_vehicles_by_management_unit"],
        "args": {"required": ["units", "km"], "optional": []},
        "handler": PlanChangeOilDataService.get_oil_change_vehicles_by_management_unit,
    },
    
    # -- lsu --

    "get_vehicle_repair_items": {
        "description": "Lấy danh sách xe đã sửa chữa những gì trong khoảng thời gian nhất định.",
        "intents": ["vehicle_repair_items"],
        "args": {
            "required": ["bks"],
            "optional": ["period", "from_date", "to_date"]
        },
        "handler": BdscDataService.get_vehicle_repair_items
    },

    "get_total_repair_cost_by_vehicle": {
        "description": "Tính tổng tiền sửa xe trong khoảng thời gian nhất định.",
        "intents": ["total_repair_cost_by_vehicle"],
        "args": {
            "required": ["bks"],
            "optional": ["period", "from_date", "to_date"]
        },
        "handler": BdscDataService.get_total_repair_cost_by_vehicle
    },

    "get_fully_depreciated_items": {
        "description": "Lấy danh sách các hạng mục đã khấu hao xong của xe.",
        "intents": ["fully_depreciated_items"],
        "args": {
            "required": ["bks"],
            "optional": []
        },
        "handler": BdscDataService.get_fully_depreciated_items
    },

    "get_not_fully_depreciated_items": {
        "description": "Lấy danh sách các hạng mục chưa khấu hao xong của xe.",
        "intents": ["not_fully_depreciated_items"],
        "args": {
            "required": ["bks"],
            "optional": []
        },
        "handler": BdscDataService.get_not_fully_depreciated_items
    },

    "get_not_depreciated_items_by_cost_type": {
        "description": "Lấy các hạng mục thuộc phân loại chi phí chưa khấu hao xong của xe.",
        "intents": ["not_depreciated_items_by_cost_type"],
        "args": {
            "required": ["bks", "phan_loai"],
            "optional": []
        },
        "handler": BdscDataService.get_not_depreciated_items_by_cost_type
    },

    "get_total_cost_by_vehicle_and_cost_type": {
        "description": "Tính tổng tiền sửa xe theo phân loại chi phí trong khoảng thời gian nhất định.",
        "intents": ["total_cost_by_vehicle_and_cost_type"],
        "args": {
            "required": ["bks", "phan_loai"],
            "optional": ["period", "from_date", "to_date"]
        },
        "handler": BdscDataService.get_total_cost_by_vehicle_and_cost_type
    },

    "get_remaining_depreciation_time": {
        "description": "Lấy thời gian phân bổ và thời gian còn lại của phân loại chi phí theo xe.",
        "intents": ["remaining_depreciation_time"],
        "args": {
            "required": ["bks", "phan_loai"],
            "optional": []
        },
        "handler": BdscDataService.get_remaining_depreciation_time
    },

    "get_total_cost_by_gara": {
        "description": "Tính tổng chi phí trả cho gara trong khoảng thời gian nhất định.",
        "intents": ["total_cost_by_gara"],
        "args": {
            "required": ["gara"],
            "optional": ["period", "from_date", "to_date"]
        },
        "handler": BdscDataService.get_total_cost_by_gara
    },

    "get_repair_items_by_gara": {
        "description": "Lấy danh sách xe và nội dung sửa chữa tại gara trong khoảng thời gian nhất định.",
        "intents": ["repair_items_by_gara"],
        "args": {
            "required": ["gara"],
            "optional": ["period", "from_date", "to_date"]
        },
        "handler": BdscDataService.get_repair_items_by_gara
    },

    "get_depreciation_ending_items": {
        "description": "Lấy danh sách hạng mục hết khấu hao trong tháng này hoặc tháng sau.",
        "intents": ["depreciation_ending_items"],
        "args": {
            "required": [],
            "optional": ["month_offset"]
        },
        "handler": BdscDataService.get_depreciation_ending_items
    }
    
    
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
