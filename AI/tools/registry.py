from typing import Any, Awaitable, Callable

from data_access.vehicle_data import VehicleDataService


ToolHandler = Callable[..., dict[str, Any] | list[dict[str, Any]] | Awaitable[Any]]


TOOL_REGISTRY: dict[str, dict[str, Any]] = {
    "search_vehicle": {
        "description": "Tra cứu thông tin xe theo biển số cũ hoặc biển số mới.",
        "intents": ["vehicle_lookup", "plate_lookup"],
        "args": {
            "required": ["plate"],
            "optional": [],
        },
        "handler": VehicleDataService.search_by_plate,
    },
    "get_inspection_due": {
        "description": "Lấy danh sách xe sắp hết hạn đăng kiểm trong số ngày tới.",
        "intents": ["inspection_due"],
        "args": {
            "required": [],
            "optional": ["days"],
        },
        "handler": VehicleDataService.get_inspection_due,
    },
    "get_inspection_expired": {
        "description": "Lấy danh sách xe đã quá hạn đăng kiểm.",
        "intents": ["inspection_expired"],
        "args": {
            "required": [],
            "optional": [],
        },
        "handler": VehicleDataService.get_expired,
    },
}


def get_prompt_tools() -> list[dict[str, Any]]:
    return [
        {
            "name": name,
            "description": spec["description"],
            "intents": spec["intents"],
            "args": spec["args"],
        }
        for name, spec in TOOL_REGISTRY.items()
    ]


def get_tool_spec(tool_name: str) -> dict[str, Any] | None:
    return TOOL_REGISTRY.get(tool_name)
