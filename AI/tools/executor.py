import inspect
from typing import Any

from AI.tools.registry import get_tool_spec


# Execute a parsed router decision that contains tool and args.
async def execute_tool_call(decision: dict[str, Any]) -> dict[str, Any]:
    return await execute_tool(
        tool_name=decision.get("tool"),
        args=decision.get("args", {}),
    )


# Validate and run a registered tool handler.
async def execute_tool(tool_name: str | None, args: dict[str, Any] | None = None) -> dict[str, Any]:
    if not tool_name:
        return build_error("missing_tool", "Tool name is required.")

    # Registry lookup is the only place where tool names are trusted.
    tool_spec = get_tool_spec(tool_name)
    if not tool_spec:
        return build_error("unknown_tool", f"Tool '{tool_name}' is not registered.")

    # LLM output can be malformed, so normalize args before validation.
    args = args if isinstance(args, dict) else {}
    args_error = validate_args(tool_spec, args)
    if args_error:
        return build_error("invalid_args", args_error, tool_name=tool_name)

    handler = tool_spec.get("handler")
    if not callable(handler):
        return build_error("invalid_handler", f"Tool '{tool_name}' has no callable handler.")

    safe_args = filter_allowed_args(tool_spec, args)

    try:
        # Handlers may be sync database functions or async service calls.
        result = handler(**safe_args)
        if inspect.isawaitable(result):
            result = await result
    except Exception as exc:
        return build_error("handler_error", str(exc), tool_name=tool_name)

    return {
        "success": True,
        "tool": tool_name,
        "args": safe_args,
        "data": result,
    }


# Check required arguments before calling the handler.
def validate_args(tool_spec: dict[str, Any], args: dict[str, Any]) -> str | None:
    args_schema = tool_spec.get("args", {})
    required_args = args_schema.get("required", [])

    # Empty strings count as missing because the handler cannot use them.
    missing_args = [
        arg_name
        for arg_name in required_args
        if arg_name not in args or args[arg_name] in (None, "")
    ]

    if missing_args:
        return f"Missing required args: {', '.join(missing_args)}"

    return None


# Keep only args declared in registry so handlers do not receive random keys.
def filter_allowed_args(tool_spec: dict[str, Any], args: dict[str, Any]) -> dict[str, Any]:
    args_schema = tool_spec.get("args", {})
    allowed_args = set(args_schema.get("required", [])) | set(args_schema.get("optional", []))

    # Tools with no declared args should receive no user/LLM arguments.
    if not allowed_args:
        return {}

    return {
        key: value
        for key, value in args.items()
        if key in allowed_args
    }


# Build a consistent error result for the orchestrator.
def build_error(code: str, message: str, tool_name: str | None = None) -> dict[str, Any]:
    return {
        "success": False,
        "tool": tool_name,
        "error": {
            "code": code,
            "message": message,
        },
    }
