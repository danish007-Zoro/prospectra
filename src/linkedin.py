from ddgs import DDGS
from urllib.parse import urlparse

def get_company_name(domain: str) -> str:
    """
    Derive a readable company name from a company domain.
    """

    hostname = urlparse(domain).netloc.lower()

    if hostname.startswith("www."):
        hostname = hostname[4:]

    company_name = hostname.split(".")[0]

    return company_name.capitalize()


def build_linkedin_query(
    name: str,
    company_name: str,
) -> str:
    """
    Build an external search query for a person's public LinkedIn profile.
    """

    return f'"{name}" "{company_name}" LinkedIn'


def search_linkedin(
    name: str,
    company_name: str,
) -> str | None:
    """
    Search the web for a public LinkedIn profile and
    return a candidate URL only when the result appears
    to match the requested person's name.
    """

    query = (
        f'"{name}" "{company_name}" '
        f'site:linkedin.com/in/'
    )

    try:
        results = DDGS().text(
            query,
            max_results=5,
        )

        name_parts = name.lower().split()

        for result in results:
            url = result.get("href", "")
            title = result.get("title", "").lower()
            snippet = result.get("body", "").lower()

            if not is_valid_linkedin_url(url):
                continue

            evidence = f"{title} {snippet}"

            if all(part in evidence for part in name_parts):
                return url

    except Exception as exc:
        print(
            f"LinkedIn search failed for {name}: {exc}"
        )

    return None

def enrich_team_members_with_linkedin(
    members,
    company_name: str,
):
    """
    Discover LinkedIn profiles for team members when possible.
    """

    for member in members:
        if member.linkedin_url:
            continue

        linkedin_url = search_linkedin(
            member.name,
            company_name,
        )

        if linkedin_url:
            member.linkedin_url = linkedin_url

    return members

def is_valid_linkedin_url(url: str | None) -> bool:
    """
    Check whether a URL is a LinkedIn profile URL.
    """

    if not url:
        return False

    return "linkedin.com/in/" in url.lower()