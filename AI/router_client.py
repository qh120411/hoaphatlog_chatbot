import httpx
from config.config import Config

class LLM_Router:
    def __init__(self):
        self.base_url = f"{Config.LLM_BASE_URL}/chat/completions"
        self.llm_model = Config.LLM_MODEL
        self.system_prompt = (
            "Bạn là trợ lý ảo của công ty Hòa Phát Logistics. "
            "Hãy trả lời ngắn gọn, rõ ràng và dễ hiểu."
        )

    async def call_llm(self, user_message: str) -> str:
        user_message = user_message.strip() if isinstance(user_message, str) else ""
        if not user_message:
            return "Tin nhắn không hợp lệ, vui lòng thử lại."
        payload = {
            "model": self.llm_model,
            "messages": [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "stream": False
        }
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                res = await client.post(
                    self.base_url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
            print(f"LLM status: {res.status_code}")

            if res.status_code == 429:
                return "LLM đang quá tải hoặc hết quota. Vui lòng thử lại sau."
            if res.status_code >= 500:
                return "Máy chủ LLM đang lỗi. Vui lòng thử lại sau."
            if res.status_code != 200:
                print(f"LLM error: {res.text}")
                return "Không thể kết nối LLM. Vui lòng thử lại sau."

            data = res.json()
            response_text = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
                .strip()
            )

            if not response_text:
                return "LLM không trả lời được. Vui lòng thử lại."
            print("✅ LLM response received")
            return response_text

        except httpx.TimeoutException:
            print("❌ LLM timeout")
            return "Kết nối LLM bị timeout. Vui lòng thử lại sau."

        except httpx.RequestError as e:
            print(f"❌ LLM request error: {e}")
            return "Không thể kết nối tới LLM. Vui lòng thử lại sau."

        except Exception as e:
            print(f"❌ Error: {e}")
            return "Có lỗi xảy ra khi gọi LLM. Bạn thử lại sau nhé."
            
