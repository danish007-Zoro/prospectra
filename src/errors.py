def classify_error(exc: Exception) -> str:
    """
    Classify an exception into a simple, useful error category.
    """

    message = str(exc).lower()

    if "err_name_not_resolved" in message:
        return "DNS_ERROR"

    if "timeout" in message:
        return "TIMEOUT"

    if "http error" in message:
        return "HTTP_ERROR"

    if "json" in message or "validation" in message:
        return "VALIDATION_ERROR"

    if "openai" in message or "groq" in message:
        return "LLM_ERROR"

    if "page.goto" in message or "browser" in message:
        return "BROWSER_ERROR"

    return "UNKNOWN_ERROR"