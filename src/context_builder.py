from src.scraper import PageEvidence


PAGE_TYPE_PRIORITY = {
    "about": 10,
    "contact": 10,
    "team": 10,
    "leadership": 10,
    "homepage": 9,
    "company": 8,
    "customers": 6,
    "customer-stories": 5,
    "solutions": 4,
    "pricing": 3,
    "careers": 2,
    "press": 1,
    "other": 0,
}


def build_context(
    pages: list[PageEvidence],
    max_chars: int = 30000,
) -> str:
    """
    Build a focused context from scraped page evidence.
    """

    ranked_pages = sorted(
        pages,
        key=lambda page: PAGE_TYPE_PRIORITY.get(page.page_type, 0),
        reverse=True,
    )

    context_parts = []
    total_chars = 0

    for page in ranked_pages:
        page_text = (
            f"PAGE TYPE: {page.page_type}\n"
            f"SOURCE URL: {page.url}\n\n"
            f"{page.content}"
        )

        if total_chars + len(page_text) > max_chars:
            continue

        context_parts.append(page_text)
        total_chars += len(page_text)

    return "\n\n" + ("\n\n" + "=" * 80 + "\n\n").join(context_parts)