from src.scraper import PageEvidence


IMPORTANT_PAGE_TYPES = {
    "homepage",
    "about",
    "company",
    "contact",
    "team",
    "leadership",
}


def calculate_coverage_score(
    pages: list[PageEvidence],
) -> float:
    """
    Calculate evidence coverage based on important page categories.
    """

    available_types = {
        page.page_type
        for page in pages
    }

    categories_found = 0

    if "homepage" in available_types:
        categories_found += 1

    if {"about", "company"} & available_types:
        categories_found += 1

    if "contact" in available_types:
        categories_found += 1

    if {"team", "leadership"} & available_types:
        categories_found += 1

    return categories_found / 4


def calculate_confidence(
    llm_confidence: float,
    total_contacts: int,
    verified_contacts: int,
    total_members: int,
    verified_members: int,
    coverage_score: float,
) -> float:
    """
    Calculate final confidence using LLM confidence,
    evidence verification, and page coverage.
    """

    total_extracted = total_contacts + total_members
    total_verified = verified_contacts + verified_members

    if total_extracted == 0:
        verification_score = 1.0
    else:
        verification_score = total_verified / total_extracted

    final_score = (
        (llm_confidence * 0.50)
        + (verification_score * 0.30)
        + (coverage_score * 0.20)
    )

    return round(final_score, 2)