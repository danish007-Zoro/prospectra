from dataclasses import dataclass
from src.browser import BrowserManager
from src.cleaner import clean_html

from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

@dataclass
class PageEvidence:
    """
    Represents useful evidence collected from a single web page.
    """

    url: str
    content: str
    page_type: str


RELEVANT_KEYWORDS = [
    "about",
    "company",
    "team",
    "leadership",
    "contact",
    "pricing",
    "customer",
    "customers",
]

PAGE_PRIORITIES = {
    "about": 10,
    "company": 8,
    "team": 10,
    "leadership": 10,
    "contact": 10,
    "pricing": 9,
    "customer-stories": 6,
    "customers": 6,
    "solutions": 5,
    "careers": 3,
    "press": 2,
}


def score_link(url: str, link_text: str) -> int:
    """
    Assign a deterministic relevance score to an internal link.
    """

    parsed_url = urlparse(url)
    path = parsed_url.path.lower().rstrip("/")

    searchable_text = f"{path} {link_text.lower()}"

    score = 0

    for keyword, points in PAGE_PRIORITIES.items():
        if keyword in searchable_text:
            score += points

    # Individual customer case studies are lower priority.
    if "/customers/" in path:
        remaining_path = path.split("/customers/", 1)[1]

        if "/" not in remaining_path:
            score = min(score, 3)

    return score

def get_page_type(url: str) -> str:
    """
    Determine the likely type of a page from its URL.
    """

    path = urlparse(url).path.lower().strip("/")

    if not path:
        return "homepage"

    page_patterns = [
        ("customer-stories", "customer-stories"),
        ("about-postman", "about"),
        ("contact-us", "contact"),
        ("leadership", "leadership"),
        ("pricing", "pricing"),
        ("careers", "careers"),
        ("press-media", "press"),
        ("team", "team"),
        ("about", "about"),
        ("contact", "contact"),
        ("customers", "customers"),
        ("company", "company"),
        ("solutions", "solutions"),
    ]

    for pattern, page_type in page_patterns:
        if pattern in path:
            return page_type

    return "other"

def discover_relevant_links(
    html: str,
    base_url: str,
    max_links: int = 10,
) -> list[str]:
    """
    Discover and rank internal links that are likely to contain
    useful company intelligence.
    """

    soup = BeautifulSoup(html, "html.parser")

    base_domain = urlparse(base_url).netloc

    scored_links = {}

    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()

        absolute_url = urljoin(base_url, href)
        parsed_url = urlparse(absolute_url)

        # Only keep links belonging to the same website.
        if parsed_url.netloc != base_domain:
            continue

        # Remove fragments such as #main-content.
        clean_url = absolute_url.split("#")[0]

        # Avoid revisiting the homepage.
        if clean_url.rstrip("/") == base_url.rstrip("/"):
            continue

        link_text = anchor.get_text(" ", strip=True)

        score = score_link(clean_url, link_text)

        if score > 0:
            scored_links[clean_url] = max(
                scored_links.get(clean_url, 0),
                score,
            )

    ranked_links = sorted(
        scored_links.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return [url for url, score in ranked_links[:max_links]]

def scrape_relevant_pages(
    manager: BrowserManager,
    base_url: str,
) -> list[PageEvidence]:
    """
    Fetch the homepage, discover relevant internal pages,
    and return structured page evidence.
    """

    homepage_html = manager.fetch_page(base_url)

    relevant_links = discover_relevant_links(
        homepage_html,
        base_url,
    )

    pages = [
        PageEvidence(
            url=base_url,
            content=clean_html(homepage_html),
            page_type="homepage",
        )
    ]

    for url in relevant_links:
        try:
            html = manager.fetch_page(url)

            pages.append(
                PageEvidence(
                    url=url,
                    content=clean_html(html),
                    page_type=get_page_type(url),
                )
            )

        except Exception as exc:
            print(f"Failed to scrape {url}: {exc}")

    return pages