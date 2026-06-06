import httpx
from config.config import Config


class LLM_Router:
    def __init__(self):
        self.base_url = f"{Config.LLM_BASE_URL}/chat/completions"
        self.llm_model = Config.LLM_MODEL

    async def call_llm(self, messages: list[dict]) -> str:
        payload = {
            "model": self.llm_model,
            "messages": messages,
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                res = await client.post(
                    self.base_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )
        except httpx.RequestError as exc:
            print(f"LLM request error: {exc}")
            return "Mình chưa kết nối được tới LLM. Bạn thử lại sau giúp mình nhé."

        if res.status_code == 429:
            return "LLM đang quá tải hoặc hết quota. Bạn thử lại sau giúp mình nhé."
        if res.status_code >= 500:
            return "Máy chủ LLM đang lỗi. Bạn thử lại sau giúp mình nhé."
        if res.status_code != 200:
            print(f"LLM error: {res.text}")
            return "Mình chưa kết nối được tới LLM. Bạn thử lại sau giúp mình nhé."

        data = res.json()
        return (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )
