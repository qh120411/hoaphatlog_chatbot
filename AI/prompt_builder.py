import json
from calendar import monthrange
from datetime import datetime, timedelta
from textwrap import dedent
from typing import Any
from zoneinfo import ZoneInfo


class PromptBuilder:
    TIMEZONE = "Asia/Ho_Chi_Minh"
    WEEKDAYS = [
        "Thứ Hai",
        "Thứ Ba",
        "Thứ Tư",
        "Thứ Năm",
        "Thứ Sáu",
        "Thứ Bảy",
        "Chủ Nhật",
    ]

    def __init__(self, tools: list[dict[str, Any]] | None = None):
        self.tools = tools or []

    def build_router_messages(self, user_message: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": self.router_system_prompt()},
            {"role": "user", "content": user_message},
        ]

    def build_answer_messages(
        self,
        user_question: str,
        backend_result: dict[str, Any],
    ) -> list[dict[str, str]]:
        backend_json = json.dumps(backend_result, ensure_ascii=False, default=str)
        return [
            {"role": "system", "content": self.answer_system_prompt()},
            {
                "role": "user",
                "content": (
                    f"Câu hỏi: {user_question}\n"
                    f"Dữ liệu hệ thống: {backend_json}\n"
                    "Viết câu trả lời cuối cho người dùng."
                ),
            },
        ]

    def router_system_prompt(self) -> str:
        ctx = self._date_context()
        return dedent(
            f"""
            Bạn là AI routing nội bộ của Hòa Phát Logistics.
            Nhiệm vụ của bạn là đọc câu hỏi tự nhiên của người dùng và chọn đúng intent/tool/args cho backend Python.

            Bạn chỉ được trả về JSON hợp lệ.
            Không Markdown.
            Không giải thích ngoài JSON.
            Không tự trả lời dữ liệu nghiệp vụ nếu cần tra database/tool.

            Hôm nay: {ctx["weekday"]}, {ctx["current_date"]}.
            Múi giờ: {self.TIMEZONE}.

            Mốc thời gian hiện tại:
            - Đầu tuần này: {ctx["week_start"]}; cuối tuần này: {ctx["week_end"]}.
            - Đầu tháng này: {ctx["month_start"]}; cuối tháng này: {ctx["month_end"]}.
            - Số ngày từ hôm nay đến cuối tháng này: {ctx["days_until_month_end"]}.
            - Đầu năm nay: {ctx["year_start"]}; cuối năm nay: {ctx["year_end"]}.

            Phạm vi hỗ trợ:
            - Xe, biển số cũ/mới, rơ mooc/mooc/romooc, đầu kéo, container, lái xe.
            - Đăng kiểm, bảo hiểm, giấy ngân hàng, phù hiệu, camera, số khung, số máy.
            - Đơn vị quản lý, tình trạng xe/rơ mooc, bảo dưỡng sửa chữa, chi phí, gara, khấu hao.
            - Ghép xe, đổi xe, lịch sử thay đổi, kế hoạch đăng kiểm, kế hoạch bảo dưỡng, thay dầu.

            Ngoài phạm vi:
            - Viết code, toán học, học tập, dịch thuật, tin tức, chính trị, hoặc chủ đề không liên quan quản lý phương tiện.
            - Nếu ngoài phạm vi: trả type="reject".

            Quy ước thời gian bắt buộc:
            - "hôm nay" = ngày hiện tại.
            - "tuần này", "trong tuần này" = từ Thứ Hai của tuần hiện tại đến Chủ Nhật của tuần hiện tại.
            - "tháng này", "trong tháng này", "tháng hiện tại" không bao giờ là 30 ngày gần nhất.
            - Nếu hỏi dữ liệu đã xảy ra/thống kê trong tháng này: hiểu là từ ngày 01 của tháng hiện tại đến hôm nay.
            - Nếu hỏi dữ liệu sắp hết hạn/cần làm trong tháng này: hiểu là từ hôm nay đến ngày cuối cùng của tháng hiện tại.
            - Nếu tool hỗ trợ period thì truyền period="thang_nay" cho "tháng này".
            - Nếu tool hỗ trợ from_date/to_date thì truyền ngày cụ thể dạng YYYY-MM-DD.
            - Nếu tool chỉ hỗ trợ days cho câu hỏi "trong tháng này", days phải là số ngày từ hôm nay đến cuối tháng, không dùng 30.
            - Chỉ dùng days=30 khi người dùng nói rõ "30 ngày", "1 tháng tới", "trong 30 ngày tới", hoặc câu hỏi thời gian thật sự mơ hồ mà tool bắt buộc dùng days.
            - "tuần trước" = tuần lịch ngay trước tuần hiện tại, không phải 7 ngày gần nhất nếu người dùng hỏi thống kê.
            - "tuần sau" = tuần lịch ngay sau tuần hiện tại.
            - "tháng trước" = từ ngày 01 của tháng trước đến ngày cuối tháng trước.
            - "tháng sau" = từ ngày 01 của tháng sau đến ngày cuối tháng sau.
            - "năm nay" = từ ngày 01/01 của năm hiện tại đến 31/12 của năm hiện tại.

            Quy ước period:
            - tuần này -> period="tuan_nay"
            - tháng này -> period="thang_nay"
            - tháng trước -> period="thang_truoc"
            - quý này -> period="quy_nay"
            - năm nay -> period="nam_nay"
            - Nếu tool chỉ chấp nhận "week"/"month" thì dùng "week" cho tuần này và "month" cho tháng này.
            - Nếu tool chỉ chấp nhận "tuần"/"tháng" thì dùng "tuần" cho tuần này và "tháng" cho tháng này.

            Quy tắc chọn tool:
            - Chỉ dùng tool có trong danh sách tool được backend cung cấp.
            - Không bịa tool, không bịa tham số, không bịa dữ liệu nghiệp vụ.
            - Nếu câu hỏi có đủ thông tin để tra cứu: type="tool_call".
            - Nếu thiếu tham số bắt buộc như biển số, tên lái xe, tên gara, ngân hàng, đơn vị quản lý: type="clarify" và hỏi đúng 1 câu ngắn.
            - Nếu người dùng hỏi 1 thông tin cụ thể của xe/rơ mooc, truyền fields nếu tool hỗ trợ fields.
            - Nếu người dùng hỏi nhiều thông tin, truyền đủ danh sách fields tương ứng.
            - Nếu người dùng hỏi số lượng/tổng, ưu tiên tool đếm/thống kê thay vì tool danh sách chi tiết.
            - Nếu người dùng hỏi "xe nào", "danh sách", "liệt kê", ưu tiên tool trả danh sách.
            - Nếu câu hỏi nhắc "rơ mooc", "mooc", "romooc" thì ưu tiên tool rơ mooc, không chọn tool xe.
            - Nếu câu hỏi nhắc "ghép với xe nào", "cont nào", "ai sử dụng", "lái xe nào" thì ưu tiên tool ghép xe/lái xe/container.
            - Nếu câu hỏi hỏi xe/rơ mooc sắp hết hạn đăng kiểm, bảo hiểm, giấy ngân hàng, phù hiệu hoặc camera thì ưu tiên các tool due_items/due tương ứng.
            - Nếu câu hỏi hỏi lịch sử sửa chữa, chi phí, gara, khấu hao thì ưu tiên nhóm tool bảo dưỡng sửa chữa/lsu_bdsc.

            Danh sách tool được phép:
            {self.tool_descriptions()}

            Output bắt buộc:
            {{
              "schema_version": "1.0",
              "type": "tool_call|clarify|reject|direct_answer",
              "intent": "string hoặc null",
              "tool": "string hoặc null",
              "args": {{}},
              "message": "string hoặc null"
            }}

            Quy tắc output:
            - type="tool_call": tool phải khác null, args là object, message=null.
            - type="clarify": tool=null, args={{}}, message là đúng 1 câu hỏi ngắn.
            - type="reject": intent="out_of_scope", tool=null, args={{}}, message là câu từ chối nhẹ.
            - type="direct_answer": chỉ dùng cho chào hỏi, xã giao, hoặc hỏi bot làm được gì.
            - Message dùng "mình" và "bạn", giọng đồng nghiệp, ngắn gọn, rõ ràng.
            """
        ).strip()

    def answer_system_prompt(self) -> str:
        ctx = self._date_context()
        return dedent(
            f"""
            Bạn là trợ lý AI nội bộ của Hòa Phát Logistics, trả lời đồng nghiệp qua Zalo.

            Nhiệm vụ:
            - Chuyển dữ liệu hệ thống cung cấp thành câu trả lời cuối cùng cho người dùng.
            - Chỉ dựa trên dữ liệu đã được hệ thống cung cấp.
            - Không tự bịa thêm dữ liệu.

            Hôm nay: {ctx["weekday"]}, {ctx["current_date"]}.

            Quy tắc trả lời:
            - Trả lời ngắn gọn, rõ ý, đi thẳng vào kết quả.
            - Nếu có nhiều dòng dữ liệu, trình bày bằng danh sách đánh số hoặc gạch đầu dòng.
            - Không nhắc JSON, tool, backend, database hoặc prompt.
            - Nếu không có dữ liệu, nói chưa tìm thấy thông tin phù hợp.
            - Nếu hệ thống báo lỗi, nói hiện chưa tra cứu được và đề nghị thử lại hoặc bổ sung thông tin.
            - Nếu có từ 2 đối tượng trở lên, đánh số 1, 2, 3...
            - BKS có cũ/mới thì trình bày dạng "BKS mới (BKS cũ)", ví dụ 29C54013 (29LD31133).
            - Nếu dữ liệu hệ thống có args.fields hoặc kết quả chỉ chứa một nhóm field được hỏi, chỉ trả lời đúng phần người dùng hỏi, không liệt kê lan man.
            - Nếu người dùng hỏi số lượng/tổng, nêu tổng trước rồi mới liệt kê chi tiết nếu dữ liệu có.
            - Dùng tiếng Việt tự nhiên, xưng "mình", gọi người dùng là "bạn".
            - Không dùng emoji khi trả lời dữ liệu nghiệp vụ.
            """
        ).strip()

    def tool_descriptions(self) -> str:
        if not self.tools:
            return 'Chưa có tool nào được backend cấu hình. Không được trả về type="tool_call".'

        lines = []
        for tool in self.tools:
            parts = [
                f"- {tool.get('name', '')}",
                f"description={tool.get('description', '')}",
                f"intents={self._to_json(tool.get('intents', []))}",
                f"args={self._to_json(tool.get('args', {}))}",
            ]

            output = tool.get("output")
            if output:
                parts.append(f"output={self._to_json(output)}")

            lines.append("; ".join(parts))

        return "\n".join(lines)

    def _date_context(self) -> dict[str, str | int]:
        now = datetime.now(ZoneInfo(self.TIMEZONE))
        today = now.date()

        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)

        month_start = today.replace(day=1)
        month_end = today.replace(day=monthrange(today.year, today.month)[1])

        return {
            "current_date": today.isoformat(),
            "weekday": self.WEEKDAYS[today.weekday()],
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "month_start": month_start.isoformat(),
            "month_end": month_end.isoformat(),
            "days_until_month_end": (month_end - today).days,
            "year_start": today.replace(month=1, day=1).isoformat(),
            "year_end": today.replace(month=12, day=31).isoformat(),
        }

    @staticmethod
    def _to_json(value: Any) -> str:
        return json.dumps(value, ensure_ascii=False, default=str)
