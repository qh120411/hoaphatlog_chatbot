import json
from typing import Any

ALLOWED_TYPES = {"tool_call", "clarify", "reject", "direct_answer"}

DEFAULT_CLARIFY_MESSAGE = (
    "Mình chưa rõ bạn muốn tra cứu thông tin nào. "
    "Bạn nói rõ hơn một chút nhé?"
)


def parse_llm_response(response: str) -> dict[str, Any]:
    #Parse the raw LLM router response into a safe decision dict.
    try:
        data = json.loads(clean_response(response))
    except (json.JSONDecodeError, TypeError):
        return fallback()

    if not isinstance(data, dict):
        return fallback()

    decision = normalize(data)

    if not is_valid(decision):
        return fallback()

    return decision


def clean_response(response: str) -> str:
    #Remove markdown code fences so json.loads can read the response.
    text = (response or "").strip()

    if text.startswith("```json"):
        text = text.removeprefix("```json").strip()
    elif text.startswith("```"):
        text = text.removeprefix("```").strip()

    if text.endswith("```"):
        text = text.removesuffix("```").strip()

    return text


def normalize(data: dict[str, Any]) -> dict[str, Any]:
    #Ensure the decision always has the expected fields and default shapes.
    args = data.get("args")

    return {
        "schema_version": data.get("schema_version", "1.0"),
        "type": data.get("type"),
        "intent": data.get("intent"),
        "tool": data.get("tool"),
        "args": args if isinstance(args, dict) else {},
        "message": data.get("message"),
    }


def is_valid(decision: dict[str, Any]) -> bool:
    #Check whether the normalized decision follows the router contract.
    decision_type = decision["type"]

    if decision_type not in ALLOWED_TYPES:
        return False

    if decision_type == "tool_call":
        return (
            isinstance(decision["tool"], str)
            and bool(decision["tool"].strip())
            and decision["message"] is None
        )

    return (
        decision["tool"] is None
        and decision["args"] == {}
        and isinstance(decision["message"], str)
        and bool(decision["message"].strip())
    )


def fallback() -> dict[str, Any]:
    #Return a safe clarify decision when the LLM output is invalid.
    return {
        "schema_version": "1.0",
        "type": "clarify",
        "intent": "unclear",
        "tool": None,
        "args": {},
        "message": DEFAULT_CLARIFY_MESSAGE,
    }
