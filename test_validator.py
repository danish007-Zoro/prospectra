from src.scraper import PageEvidence
from src.schemas import CompanyIntelligence
from src.validator import (
    validate_contact_points,
    verify_team_member,
)


def create_test_pages():
    return [
        PageEvidence(
            url="https://example.com/contact",
            content=(
                "Contact us at info@example.com "
                "for general enquiries."
            ),
            page_type="contact",
        ),
        PageEvidence(
            url="https://example.com/about",
            content=(
                "Abhinav Sharma is the Chief Executive Officer "
                "and co-founder of Example Company."
            ),
            page_type="about",
        ),
    ]


def test_validate_contact_points():
    pages = create_test_pages()

    intelligence = CompanyIntelligence(
        company_overview="Test company.",
        target_audience="Developers.",
        contact_points=[
            {
                "email": "info@example.com",
                "source_url": "https://example.com/contact",
            },
            {
                "email": "fake@example.com",
                "source_url": "https://example.com/contact",
            },
        ],
        key_leadership=[],
        confidence_score=0.5,
    )

    total, verified, unverified = validate_contact_points(
        intelligence,
        pages,
    )

    assert total == 2
    assert verified == 1
    assert unverified == ["fake@example.com"]


def test_verify_team_member_accepts_matching_name_and_role():
    pages = create_test_pages()

    result = verify_team_member(
        pages,
        "Abhinav Sharma",
        "Chief Executive Officer",
        "https://example.com/about",
    )

    assert result is True


def test_verify_team_member_rejects_wrong_role():
    pages = create_test_pages()

    result = verify_team_member(
        pages,
        "Abhinav Sharma",
        "Chief Financial Officer",
        "https://example.com/about",
    )

    assert result is False


def test_verify_team_member_rejects_unknown_person():
    pages = create_test_pages()

    result = verify_team_member(
        pages,
        "John Doe",
        "Chief Executive Officer",
        "https://example.com/about",
    )

    assert result is False