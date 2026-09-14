from src.errors import classify_error


def test_classify_dns_error():
    error = Exception("net::ERR_NAME_NOT_RESOLVED")
    assert classify_error(error) == "DNS_ERROR"


def test_classify_timeout_error():
    error = Exception("Page timeout exceeded")
    assert classify_error(error) == "TIMEOUT"


def test_classify_http_error():
    error = Exception("HTTP error 404 while fetching URL")
    assert classify_error(error) == "HTTP_ERROR"


def test_classify_validation_error():
    error = Exception("JSON validation failed")
    assert classify_error(error) == "VALIDATION_ERROR"


def test_classify_llm_error():
    error = Exception("Groq API request failed")
    assert classify_error(error) == "LLM_ERROR"


def test_classify_browser_error():
    error = Exception("Browser failed to create page")
    assert classify_error(error) == "BROWSER_ERROR"


def test_classify_unknown_error():
    error = Exception("Something completely unexpected happened")
    assert classify_error(error) == "UNKNOWN_ERROR"