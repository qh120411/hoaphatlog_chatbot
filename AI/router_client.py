import httpx
import json
from config.config import Config


class LLM_Router:
    def __init__(self, llm_clients=None):
        self.llm_clients = llm_clients
        self.base_url = f"{Config.LLM_BASE_URL}/chat/completions"
        self.llm_model = Config.LLM_MODEL
        self.system_prompt = (
            "Bạn là trợ lý ảo của công ty Hòa Phát Logistics. "
            "Hãy trả lời ngắn gọn, rõ ràng và dễ hiểu."
        )
    
    async def call_llm(self, user_message: str) -> str:
        # Validate input
        if not user_message or not isinstance(user_message, str):
            return "❌ Lỗi: Tin nhắn không hợp lệ"
        
        try:
            # Tạo payload cho LLM
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
            
            print(f"📤 Calling LLM: {self.base_url}")
            print(f"   Model: {self.llm_model}")
            print(f"   Message: {user_message}")
            
            # Gọi API
            async with httpx.AsyncClient(timeout=30) as client:
                res = await client.post(self.base_url, json=payload)
                print(f"   Status: {res.status_code}")
                
                if res.status_code != 200:
                    print(f"❌ Error: {res.text}")
                    return "Xin lỗi, không thể kết nối LLM"
                
                data = res.json()
                print(f"   Response: {data}")
                
                # Trích xuất content từ response
                response_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                if not response_text:
                    return "Xin lỗi, LLM không trả lời được"
                
                print(f"✅ Response: {response_text}")
                return response_text
        
        except httpx.TimeoutException:
            print("❌ Error: LLM API timeout (30s)")
            return "Xin lỗi, kết nối LLM bị timeout"
        except Exception as e:
            print(f"❌ Error calling LLM: {e}")
            return "Xin lỗi, có lỗi xảy ra. Bạn thử lại sau nhé!"
            
