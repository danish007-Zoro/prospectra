import pytest
from pydantic import ValidationError

from src.schemas import CompanyIntelligence


def test_company_intelligence_accepts_valid_data():
    result = CompanyIntelligence(
        company_overview=(
            "Postman is an API platform used to build and test APIs. "
            "It helps teams collaborate throughout the API lifecycle."
        ),
        target_audience="Software developers and engineering teams.",
        contact_points=[],
        key_leadership=[
            {
                "name": "Abhinav Asthana",
                "role": "CEO & Co-founder",
                "linkedin_url": None,
                "source_url": "https://postman.com/company/about-postman/",
            }
        ],
        confidence_score=0.9,
    )

    assert result.target_audience == "Software developers and engineering teams."
    assert len(result.key_leadership) == 1
    assert result.confidence_score == 0.9


def test_confidence_score_must_be_between_zero_and_one():
    with pytest.raises(ValidationError):
        CompanyIntelligence(
            company_overview="Test company.",
            target_audience="Developers.",
            contact_points=[],
            key_leadership=[],
            confidence_score=1.5,
        )


def test_extra_fields_are_rejected():
    with pytest.raises(ValidationError):
        CompanyIntelligence(
            company_overview="Test company.",
            target_audience="Developers.",
            contact_points=[],
            key_leadership=[],
            confidence_score=0.5,
            unexpected_field="not allowed",
        )