from typing import Any
from AI.prompt_builder import PromptBuilder
from AI.router_client import LLM_Router
from AI.tools.executor import execute_tool_call
from AI.tools.parse import parse_llm_response
from AI.tools.registry import get_prompt_tools

class ChatOrchestrator:
    def __init__(self):
        self.router = LLM_Router()
        self.prompt_builder = PromptBuilder(tools = get_prompt_tools())
    
    async def handle(self, user_message: str) -> str:
        user_message = user_message.strip()
        if not user_message:
            return "Vui lòng nhập câu hỏi."
        decison = await self.route(user_message)
        return await self.handle_decision(user_message, decison)

    async def route(self, user_message: str) -> dict:
        router = self.prompt_builder.build_router_messages(user_message)
        router_response = await self.router.call_llm(router)
        
        return parse_llm_response(router_response)
    
    async def handle_decision(self, user_message: str, decision: dict[str, Any]) -> str:
        decision_type = decision.get("type")
        if decision_type in { "clarify", "reject", "direct_answer"}:
            return decision.get("message") or self.fallback_message()
        
        if decision_type == "tool_call":
            backend_result = await execute_tool_call(decision)
            return await self.answer(user_message, backend_result)
        return self.fallback_message()
    
    async def answer(self, user_message: str, backend_result: dict[str, Any]) -> str:
        answer_prompt = self.prompt_builder.build_answer_messages(user_question = user_message, backend_result = backend_result)
        answer = await self.router.call_llm(answer_prompt)
        if not answer:
            return self.fallback_message()
        return answer.strip()  
    
    def fallback_message(self) -> str:
        return "Mình chưa xử lý được yêu cầu này. Bạn nói rõ hơn một chút hoặc thử lại giúp mình nhé."
