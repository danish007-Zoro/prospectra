import pytest
from pydantic import ValidationError

from src.schemas import CompanyResult


def test_success_result_allows_missing_usage():
    result = CompanyResult(
        domain="postman.com",
        status="success",
        intelligence=None,
        error=None,
    )

    assert result.usage is None


def test_failed_result_requires_error_details():
    result = CompanyResult(
        domain="bad-domain.com",
        status="failed",
        intelligence=None,
        error={
            "stage": "scraping",
            "error_type": "NetworkError",
            "message": "Unable to resolve domain",
        },
    )

    assert result.status == "failed"
    assert result.error.error_type == "NetworkError"


def test_invalid_status_is_rejected():
    with pytest.raises(ValidationError):
        CompanyResult(
            domain="postman.com",
            status="invalid",
        )