from src.browser import BrowserManager
from src.scraper import scrape_relevant_pages


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
        print(f"SCRAPING: {domain}")
        print(f"{'=' * 60}")

        try:
            pages = scrape_relevant_pages(manager, domain)

            print(f"Pages successfully scraped: {len(pages)}")

            for url, text in pages.items():
                print(f"  {len(text):>6} chars | {url}")

        except Exception as exc:
            print(f"FAILED: {exc}")

finally:
    manager.close()