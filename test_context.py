from src.context_builder import build_context
from src.scraper import PageEvidence


def test_context_respects_character_limit():
    pages = [
        PageEvidence(
            url="https://example.com/about",
            content="A" * 10000,
            page_type="about",
        ),
        PageEvidence(
            url="https://example.com/contact",
            content="B" * 10000,
            page_type="contact",
        ),
        PageEvidence(
            url="https://example.com/team",
            content="C" * 10000,
            page_type="team",
        ),
    ]

    context = build_context(
        pages,
        max_chars=30000,
    )

    assert len(context) <= 30000