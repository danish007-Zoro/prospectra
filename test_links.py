from src.browser import BrowserManager
from src.scraper import discover_relevant_links


DOMAINS = [
    "https://postman.com",
    "https://supabase.com",
    "https://vapi.ai",
]


manager = BrowserManager()

try:
    manager.start()

    for domain in DOMAINS:
        print(f"\n{'=' * 60}")
        print(f"DOMAIN: {domain}")
        print(f"{'=' * 60}")

        html = manager.fetch_page(domain)

        links = discover_relevant_links(
            html,
            domain,
            max_links=10,
        )

        for link in links:
            print(link)

finally:
    manager.close()