from src.browser import BrowserManager
from src.scraper import scrape_relevant_pages


manager = BrowserManager()

try:
    manager.start()

    pages = scrape_relevant_pages(
        manager,
        "https://postman.com",
    )

    print(f"\nPages scraped: {len(pages)}")

    for page in pages:
        print("\n" + "=" * 60)
        print(f"TYPE: {page.page_type}")
        print(f"URL:  {page.url}")
        print(f"TEXT: {len(page.content)} characters")

finally:
    manager.close()