from google.genai import types

# Minimal ANSI color helper (replace with colorama if you prefer)
class _Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    WHITE = "\033[97m"
    CYAN = "\033[36m"
    BG_RED = "\033[41m"
    BG_BLUE = "\033[44m"
    BR_BLUE = "\033[94m"  # bright blue

def _log(text):
    print(text, flush=True)

class DisplayState:
    def __init__(self, session_service, app_name, user_id, session_id, message):
        self.session_service = session_service
        self.app_name = app_name
        self.user_id = user_id
        self.session_id = session_id
        self.message = message

async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    _log(f"\n{_Color.BG_RED}{_Color.WHITE}{_Color.BOLD} User Query: {query} {_Color.RESET}")

    # (Optional) display state hook
    _ = DisplayState(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "State before processing the query",
    )

    final_response_text = None

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        _log(f"Error during agent processing: {e}")

    return final_response_text

def _safe_get(obj, name, default=None):
    return getattr(obj, name, default)

async def process_agent_response(event):
    """Process and display agent response events."""
    # Basic event info (guarded)
    ev_id = _safe_get(event, "id", "unknown")
    author = _safe_get(event, "author", "agent")
    _log(f"Event ID: {ev_id}, Author: {author}")

    # Parts (text, code, tool responses, etc.)
    content = _safe_get(event, "content")
    if content and _safe_get(content, "parts"):
        for part in content.parts:
            # 1) Executable code (SDK uses `executable_code` for code blocks)
            code_obj = _safe_get(part, "executable_code")
            if code_obj and _safe_get(code_obj, "code"):
                _log(f" Debug: Agent generated code:\n```{code_obj.code}\n```")

            # 2) Tool / code execution result (common name: tool_response)
            tool_resp = _safe_get(part, "tool_response")
            if tool_resp is not None:
                # Try typical fields safely
                output = _safe_get(tool_resp, "output")
                if output is None:
                    # fallback to other common names
                    output = _safe_get(tool_resp, "result", _safe_get(tool_resp, "text"))
                _log(f" Tool Response: {output}")

            # 3) Plain text
            text = _safe_get(part, "text")
            if isinstance(text, str) and text.strip():
                _log(f" Text: {text.strip()}")

    # Final response (guard `.is_final_response()` existence)
    final_response = None
    is_final = False
    try:
        if callable(_safe_get(event, "is_final_response")):
            is_final = event.is_final_response()
    except Exception:
        is_final = False

    if is_final:
        # Try to get first text part as final
        if content and _safe_get(content, "parts"):
            first = content.parts[0]
            text = _safe_get(first, "text")
            if isinstance(text, str) and text.strip():
                final_response = text.strip()
                _log(
                    f"\n{_Color.BR_BLUE}{_Color.WHITE}{_Color.BOLD} Final Response: {final_response} {_Color.RESET}"
                )
                _log(
                    f"\n{_Color.CYAN}{_Color.BOLD} Final Response: {final_response} {_Color.RESET}"
                )
                _log(
                    f"\n{_Color.BG_BLUE}{_Color.WHITE}{_Color.BOLD} Final Response: {final_response} {_Color.RESET}"
                )
            else:
                _log(
                    f"\n{_Color.BG_RED}{_Color.WHITE}{_Color.BOLD} No final response text found in event {_Color.RESET}"
                )

    return final_response
